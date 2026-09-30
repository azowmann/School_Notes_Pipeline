# tools/

## verify_lp.py

Solves an LP or integer LP from a JSON file and, if the file includes a claimed
answer, checks it against the solver.

### Setup

From the repo root, run `.\setup.ps1` once (see the main `README.md`). That creates `.venv` and installs everything below into it.

### Usage

```
.venv/Scripts/python tools/verify_lp.py <problems.json>
```

Exits 0 if every claimed check passes (or there was nothing to check), 1 if any
claimed check fails.

### Input format

The JSON file is either one problem object, or a list of them (processed in
order, one report each).

```json
{
  "name": "optional label, shown in the report",
  "sense": "max",
  "vars": ["x1", "x2"],
  "c": [3, 5],
  "constraints": [
    {"coef": [1, 0], "op": "<=", "rhs": 4, "label": "c1"},
    {"coef": [0, 2], "op": "<=", "rhs": 12},
    {"coef": [3, 2], "op": "<=", "rhs": 18}
  ],
  "bounds": [[0, null], [0, null]],
  "integer": false,
  "claimed": {
    "status": "optimal",
    "z": 36,
    "x": [2, 6],
    "duals": [0, 1.5, 1]
  }
}
```

Field notes:

| Field | Required | Meaning |
|---|---|---|
| `sense` | yes | `"max"` or `"min"` |
| `c` | yes | objective coefficients, one per variable |
| `constraints` | yes | list of `{coef, op, rhs, label?}`. `op` is `"<="`, `">="`, or `"="`. `coef` has one entry per variable. `label` defaults to `c1`, `c2`, … in order |
| `vars` | no | variable names, default `x1`, `x2`, … |
| `bounds` | no | one `[lo, hi]` per variable; `null` means unbounded in that direction. Default is every variable `>= 0` with no upper bound (`[0, null]`) |
| `integer` | no | `true`/`false` for all variables, or a list of booleans (one per variable). Default `false`. Integer problems are solved with `scipy.optimize.milp` instead of `linprog` |
| `claimed` | no | any subset of `status`, `z`, `x`, `duals` — only the keys present are checked |

`claimed.status` is one of `optimal`, `infeasible`, `unbounded`.

### What gets printed

For each problem: status, `z*`, `x*`, and per constraint its slack and shadow
price (`dz*/d(rhs)`, in the problem's own max/min sense — already sign-adjusted
for `>=` and `=` constraints, so a positive number always means "increasing
this constraint's right-hand side by 1 improves `z*` by this much"). Numbers
print as simple fractions when the value is close to one (e.g. `3/2`), and as
a short decimal otherwise. Integer programs have no dual values, so their
constraints print `shadow price=n/a (integer program)`.

If `claimed` is present, a `Claimed check:` block follows with one line per
claimed field:

- **status** — exact match required.
- **z** — numeric match within tolerance.
- **x** — matches the solver's `x*` directly, **or**, if it differs, PASSes
  anyway as an "alternative optimum" when it is feasible and has the same `z`
  (checked independently of the solver's own vertex). Otherwise FAILs and says
  whether the claimed point is infeasible or has the wrong objective.
- **duals** — numeric match within tolerance. On a mismatch, the report
  reminds you that degenerate LPs can have more than one valid set of shadow
  prices — a mismatch here doesn't automatically mean the claimed duals are
  wrong, only that they differ from the ones this solver's basis produced.

### Examples

`examples/` has one JSON file per case, runnable directly:

```
.venv/Scripts/python tools/verify_lp.py tools/examples/01_max_diet.json
```

| File | What it tests |
|---|---|
| `01_max_diet.json` | classic all-`<=` max problem, correct claim → all PASS |
| `02_min_ge.json` | min problem with `>=` constraints, correct claim → all PASS |
| `03_unbounded.json` | unbounded LP, claimed status only → PASS |
| `04_integer.json` | integer program via `milp`, correct claim → PASS (no duals) |
| `05_wrong_claim.json` | deliberately wrong `z` → FAIL |
| `06_alt_optimum.json` | claimed `x` is a different optimal vertex than the solver's → PASS (alternative optimum) |
