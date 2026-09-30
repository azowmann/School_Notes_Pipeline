# School Notes Pipeline

A [Claude Code](https://claude.com/claude-code) slash-command pipeline that turns a week's raw
course materials (lecture slides, recordings/transcripts, tutorial sheets, textbook pages) into
polished, cited study notes and practice problems — with LP/ILP answers checked by an actual
solver instead of taken on faith.

> **Status:** work in progress. The shared engine, both course profiles, and the LP verifier are
> built and tested; this has not yet been run end-to-end against a full semester. Expect rough
> edges.

## Why this exists

Turning a week of lectures into good study notes is repetitive but easy to get subtly wrong —
mis-transcribed numbers, silently dropped conflicts between the slides and the textbook, LP
answers that "look right." This project pushes that work onto Claude Code under a strict set of
rules (`CLAUDE.md`): never invent content, always cite, always flag uncertainty, and verify every
checkable answer by running code rather than eyeballing it.

The engine is **shared** across courses; everything course-specific (inputs, stages, templates,
citation tags, verification rules) lives in that course's own `COURSE.md` profile. Adding a new
course means writing a profile, not touching the pipeline.

## How it works

Three slash commands, run in order, once per week:

| Command | Purpose | Typical output |
|---|---|---|
| `/prep <course> <week>` | Read the raw inputs, transcribe/extract structure, verify any numerical claims | `work/manifest.md` (+ course-specific work files) |
| `/notes <course> <week> [part]` | Write the week's study notes | `notes/weekNN-notes.md` + `.pdf` |
| `/practice <course> <week> [part\|mode]` | Write practice problems with worked, verified solutions | `notes/weekNN-practice.md` + `.pdf` |

Between `/prep` and `/notes` there's a **manual checkpoint**: the student reviews something
`/prep` produced (a screenshot checklist, a TA-notes transcription) before Claude builds on it.
`/notes` refuses to silently skip this — it checks and asks.

Every numerical answer that can be checked by code *is* checked by code (`tools/verify_lp.py`),
and every notes/practice file ends with a **Gaps & conflicts** section naming anything the sources
didn't resolve.

## Courses currently supported

- **`envs`** — Environment & Society. Two cumulatively-numbered lectures/week (slides +
  transcript), plus student-provided textbook screenshots. Weekly quiz flags (**⭐ Quiz flag:**).
- **`linopt`** — Linear Optimization. Lecture slides, a tutorial sheet, and the TA's handwritten
  solutions, with every LP/ILP claim verified against a solver. Exam flags
  (**⭐ Exam flag:**), plus a cumulative `/practice linopt weekNN exam` mode for exam prep.

See each course's `courses/<course>/COURSE.md` for its exact inputs, stages, and rules.

## One-time setup

Run `.\setup.ps1` from the repo root. It creates `.venv`, installs the Python packages `tools/`
needs (`scipy`, `numpy`), and runs the LP verifier's example checks as a smoke test.

```powershell
.\setup.ps1
```

If PowerShell blocks the script, run it once with:

```powershell
powershell -ExecutionPolicy Bypass -File setup.ps1
```

After setup, run any tool in this repo as `.venv/Scripts/python <script>` (not plain `python`,
and no need to activate the venv).

PDF rendering (`tools/render_pdf.sh`, run automatically by `/notes` and `/practice`) additionally
needs [pandoc](https://pandoc.org/installing.html) and a LaTeX engine (`xelatex`). If either is
missing, the script prints the exact install command for your OS; the `.md` file is still written
either way — the PDF is a rendered copy, not the source of truth.

## Weekly checklist

1. Drop the week's raw files into `courses/<course>/weeks/weekNN/input/` (see that course's
   `COURSE.md` for exact filenames).
2. `/prep <course> <week>` — review the manual checkpoint it asks for (approve a screenshot
   checklist, correct a TA-notes transcription, etc.).
3. `/notes <course> <week>`
4. `/practice <course> <week>` (or `/practice linopt weekNN exam` for cumulative exam prep).

Each command asks rather than guesses whenever something's missing or ambiguous — read what it
says before answering.

## Folder layout

```
school-notes/
├── CLAUDE.md                     ← shared rules for every course
├── README.md                     ← this file
├── setup.ps1                     ← one-command setup: creates .venv, installs requirements, runs examples
├── requirements.txt               ← Python packages for tools/
├── .claude/commands/
│   ├── prep.md                   ← /prep <course> <week>
│   ├── notes.md                  ← /notes <course> <week> [part]
│   └── practice.md               ← /practice <course> <week> [part|mode]
├── tools/
│   ├── README.md                 ← how to use the tools
│   ├── verify_lp.py              ← solves LPs/ILPs and checks claimed answers (scipy: linprog/milp)
│   ├── render_pdf.sh             ← markdown → PDF with typeset math (pandoc + xelatex)
│   └── examples/                 ← tested example LP inputs
└── courses/
    ├── envs/                     ← Environment & Society
    │   ├── COURSE.md
    │   ├── templates/{notes,practice}-template.md
    │   └── weeks/weekNN/{input,textbook,work,notes}/
    └── linopt/                   ← Linear Optimization
        ├── COURSE.md
        ├── templates/{notes,practice}-template.md
        ├── exam-prep/            ← cumulative practice sets
        └── weeks/weekNN/{input,work,notes}/
```

`input/` and `textbook/` belong to the student and are never edited by Claude. Lecture slides,
recordings/transcripts, and textbook scans are git-ignored (see `.gitignore`) — this repo tracks
the pipeline and the generated notes, not copyrighted course material.

## The LP/ILP verifier

`tools/verify_lp.py` takes a JSON spec (objective, constraints, optional claimed answer) and
solves it with `scipy` (`linprog`/HiGHS for LPs, `milp` for integer programs), printing the
optimal value, solution, and per-constraint shadow prices — then PASS/FAILs any claimed answer
against the actual solve (correctly handling alternative optima and degenerate duals). See
[`tools/README.md`](tools/README.md) for the input format and worked examples.

## Design docs

`KICKOFF.md` and the two `courses/*/COURSE.md` files are the original design spec this pipeline
was built from — useful background if you're extending it or adding a new course.
