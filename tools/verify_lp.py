#!/usr/bin/env python3
"""Solve LPs / integer LPs from a JSON spec and check any claimed answer against the solver.

Usage:
    python tools/verify_lp.py <problems.json>

See tools/README.md for the JSON schema and what the output means.
"""

import argparse
import json
import sys
from fractions import Fraction

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, linprog, milp

TOL = 1e-6

LINPROG_STATUS = {
    0: "optimal",
    1: "iteration_limit",
    2: "infeasible",
    3: "unbounded",
    4: "error",
}

MILP_STATUS = {
    0: "optimal",
    1: "iteration_limit",
    2: "infeasible",
    3: "unbounded",
    4: "error",
}


def fmt_num(x, max_denom=100):
    """Render a float as a simple fraction when it's close to one, else a short decimal."""
    if x is None:
        return "-"
    if abs(x) < 1e-9:
        x = 0.0
    frac = Fraction(x).limit_denominator(max_denom)
    if abs(float(frac) - x) < TOL * max(1.0, abs(x)):
        if frac.denominator == 1:
            return str(frac.numerator)
        return f"{frac.numerator}/{frac.denominator}"
    return f"{x:.6g}"


def close(a, b, tol=TOL):
    return abs(a - b) < tol * max(1.0, abs(a), abs(b))


def fmt_vec(vals):
    return "(" + ", ".join(fmt_num(v) for v in vals) + ")"


def load_problems(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data if isinstance(data, list) else [data]


def expr_str(coef, vars_):
    terms = []
    for c, v in zip(coef, vars_):
        if c == 0:
            continue
        if c == 1:
            term = v
        elif c == -1:
            term = f"-{v}"
        else:
            term = f"{fmt_num(c)}{v}"
        if terms and not term.startswith("-"):
            terms.append("+ " + term)
        elif terms:
            terms.append("- " + term[1:])
        else:
            terms.append(term)
    return " ".join(terms) if terms else "0"


def normalize_bounds(bounds_in, n):
    if bounds_in is None:
        return [(0, None)] * n
    return [(b[0], b[1]) for b in bounds_in]


def normalize_integrality(integer_spec, n):
    if isinstance(integer_spec, bool):
        return [1 if integer_spec else 0] * n
    if integer_spec is None:
        return [0] * n
    return [1 if v else 0 for v in integer_spec]


def solve_continuous(sense, c, constraints, bounds):
    c_internal = [-x for x in c] if sense == "max" else list(c)
    A_ub, b_ub, A_eq, b_eq = [], [], [], []
    row_map = []
    for row in constraints:
        coef, op, rhs = row["coef"], row["op"], row["rhs"]
        if op == "<=":
            A_ub.append(list(coef))
            b_ub.append(rhs)
            row_map.append(("ub", len(A_ub) - 1, op))
        elif op == ">=":
            A_ub.append([-x for x in coef])
            b_ub.append(-rhs)
            row_map.append(("ub", len(A_ub) - 1, op))
        elif op == "=":
            A_eq.append(list(coef))
            b_eq.append(rhs)
            row_map.append(("eq", len(A_eq) - 1, op))
        else:
            raise ValueError(f"unknown constraint op: {op!r}")

    res = linprog(
        c_internal,
        A_ub=A_ub or None,
        b_ub=b_ub or None,
        A_eq=A_eq or None,
        b_eq=b_eq or None,
        bounds=bounds,
        method="highs",
    )

    status = LINPROG_STATUS.get(res.status, "error")
    out = {"status": status, "z": None, "x": None, "shadow_prices": None, "message": res.message}

    if status == "optimal":
        z_internal = res.fun
        z = -z_internal if sense == "max" else z_internal
        out["z"] = z
        out["x"] = list(res.x)

        sense_sign = -1 if sense == "max" else 1
        ineq_marg = res.ineqlin.marginals if A_ub else []
        eq_marg = res.eqlin.marginals if A_eq else []
        shadow = []
        for kind, idx, op in row_map:
            marg = ineq_marg[idx] if kind == "ub" else eq_marg[idx]
            op_sign = -1 if op == ">=" else 1
            d_internal_d_rhs = marg * op_sign
            shadow.append(d_internal_d_rhs * sense_sign)
        out["shadow_prices"] = shadow

    return out


def solve_integer(sense, c, constraints, bounds, integrality):
    c_internal = [-x for x in c] if sense == "max" else list(c)
    A_rows, lb_rows, ub_rows = [], [], []
    for row in constraints:
        coef, op, rhs = row["coef"], row["op"], row["rhs"]
        A_rows.append(list(coef))
        if op == "<=":
            lb_rows.append(-np.inf)
            ub_rows.append(rhs)
        elif op == ">=":
            lb_rows.append(rhs)
            ub_rows.append(np.inf)
        elif op == "=":
            lb_rows.append(rhs)
            ub_rows.append(rhs)
        else:
            raise ValueError(f"unknown constraint op: {op!r}")

    lin_constraints = LinearConstraint(A_rows, lb_rows, ub_rows) if A_rows else None
    lb = [b[0] if b[0] is not None else -np.inf for b in bounds]
    ub = [b[1] if b[1] is not None else np.inf for b in bounds]
    scipy_bounds = Bounds(lb, ub)

    res = milp(c_internal, integrality=integrality, bounds=scipy_bounds, constraints=lin_constraints)

    status = MILP_STATUS.get(res.status, "error")
    out = {"status": status, "z": None, "x": None, "shadow_prices": None, "message": res.message}

    if status == "optimal":
        z_internal = res.fun
        z = -z_internal if sense == "max" else z_internal
        out["z"] = z
        out["x"] = list(res.x)
        # No dual values for MIPs.

    return out


def constraint_slack(row, x):
    coef, op, rhs = row["coef"], row["op"], row["rhs"]
    value = sum(a * xi for a, xi in zip(coef, x))
    if op == "<=":
        return rhs - value
    if op == ">=":
        return value - rhs
    return 0.0  # equality


def check_feasible(problem, x):
    for row in problem["constraints"]:
        slack = constraint_slack(row, x)
        if slack < -TOL:
            return False
    n = len(problem["c"])
    bounds = normalize_bounds(problem.get("bounds"), n)
    for xi, (lo, hi) in zip(x, bounds):
        if lo is not None and xi < lo - TOL:
            return False
        if hi is not None and xi > hi + TOL:
            return False
    return True


def compare_claimed(problem, result, vars_):
    """Return (checks, any_fail) where checks is a list of (label, verdict, detail)."""
    claimed = problem.get("claimed")
    if not claimed:
        return [], False

    checks = []
    any_fail = False
    is_integer = any(normalize_integrality(problem.get("integer"), len(problem["c"])))

    if "status" in claimed:
        ok = claimed["status"] == result["status"]
        checks.append(("status", "PASS" if ok else "FAIL", f"claimed {claimed['status']!r}, solver {result['status']!r}"))
        any_fail = any_fail or not ok

    if result["status"] != "optimal":
        return checks, any_fail

    if "z" in claimed:
        ok = close(claimed["z"], result["z"])
        checks.append((
            "z", "PASS" if ok else "FAIL",
            f"claimed {fmt_num(claimed['z'])}, solver {fmt_num(result['z'])}",
        ))
        any_fail = any_fail or not ok

    if "x" in claimed:
        x_claim = claimed["x"]
        elementwise = all(close(a, b) for a, b in zip(x_claim, result["x"]))
        if elementwise:
            checks.append(("x", "PASS", "matches solver"))
        else:
            feasible = check_feasible(problem, x_claim)
            z_at_claim = sum(ci * xi for ci, xi in zip(problem["c"], x_claim))
            same_z = "z" in claimed or close(z_at_claim, result["z"])
            if feasible and same_z:
                checks.append((
                    "x", "PASS",
                    f"differs from solver's {fmt_vec(result['x'])} "
                    f"but is feasible with the same z (alternative optimum)",
                ))
            else:
                reason = "infeasible" if not feasible else "objective doesn't match"
                checks.append((
                    "x", "FAIL",
                    f"claimed {fmt_vec(x_claim)} vs solver "
                    f"{fmt_vec(result['x'])} ({reason})",
                ))
                any_fail = True

    if "duals" in claimed:
        if is_integer:
            checks.append(("duals", "-", "not applicable (integer program has no dual)"))
        elif result["shadow_prices"] is None:
            checks.append(("duals", "-", "not applicable"))
        else:
            duals_claim = claimed["duals"]
            ok = all(close(a, b) for a, b in zip(duals_claim, result["shadow_prices"]))
            detail = (
                f"claimed {fmt_vec(duals_claim)}, "
                f"solver {fmt_vec(result['shadow_prices'])}"
            )
            if not ok:
                detail += " — note: degenerate LPs can have several valid dual solutions"
            checks.append(("duals", "PASS" if ok else "FAIL", detail))
            any_fail = any_fail or not ok

    return checks, any_fail


def print_problem(idx, problem, result, checks, vars_):
    name = problem.get("name", f"Problem {idx}")
    print(f"=== {name} ===")
    print(f"sense: {problem['sense']}   status: {result['status']}")

    if result["status"] == "optimal":
        print(f"z* = {fmt_num(result['z'])}")
        x_str = ", ".join(f"{v}={fmt_num(xi)}" for v, xi in zip(vars_, result["x"]))
        print(f"x* = ({x_str})")

        is_integer = any(normalize_integrality(problem.get("integer"), len(problem["c"])))
        print("Constraints:")
        for i, row in enumerate(problem["constraints"]):
            label = row.get("label", f"c{i + 1}")
            lhs = expr_str(row["coef"], vars_)
            slack = constraint_slack(row, result["x"])
            if is_integer:
                shadow_str = "n/a (integer program)"
            else:
                shadow_str = fmt_num(result["shadow_prices"][i])
            print(f"  {label}: {lhs} {row['op']} {fmt_num(row['rhs'])}    slack={fmt_num(slack)}    shadow price={shadow_str}")
    else:
        print(f"({result['message']})")

    if checks:
        print("Claimed check:")
        for label, verdict, detail in checks:
            print(f"  {label}: {verdict} ({detail})")

    print()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="JSON file: one problem object, or a list of them")
    args = parser.parse_args()

    problems = load_problems(args.input)
    any_fail = False

    for idx, problem in enumerate(problems, start=1):
        n = len(problem["c"])
        vars_ = problem.get("vars") or [f"x{i + 1}" for i in range(n)]
        bounds = normalize_bounds(problem.get("bounds"), n)
        integrality = normalize_integrality(problem.get("integer"), n)

        if any(integrality):
            result = solve_integer(problem["sense"], problem["c"], problem["constraints"], bounds, integrality)
        else:
            result = solve_continuous(problem["sense"], problem["c"], problem["constraints"], bounds)

        checks, problem_failed = compare_claimed(problem, result, vars_)
        any_fail = any_fail or problem_failed

        print_problem(idx, problem, result, checks, vars_)

    sys.exit(1 if any_fail else 0)


if __name__ == "__main__":
    main()
