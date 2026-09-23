# Course Notes Pipeline (shared engine)

This project turns each week's course materials into study material. It supports several courses. Everything that is **the same for every course** lives in this file. Everything that is **specific to a course** (its inputs, stages, outputs and templates) lives in that course's profile at `courses/<course>/COURSE.md`.

**Always read the course's `COURSE.md` before doing any work for that course.** Where it conflicts with this file, `COURSE.md` wins.

---

## Folder layout

```
school-notes/
├── CLAUDE.md                     ← this file (shared rules)
├── README.md                     ← student's quick-start
├── requirements.txt              ← Python packages for tools/
├── .claude/commands/
│   ├── prep.md                   ← /prep <course> <week>
│   ├── notes.md                  ← /notes <course> <week> [part]
│   └── practice.md               ← /practice <course> <week> [part|mode]
├── tools/
│   ├── README.md                 ← how to use the tools (read before using them)
│   ├── verify_lp.py              ← solves LPs / integer LPs and checks claimed answers
│   ├── render_pdf.sh             ← optional: markdown → PDF with typeset math
│   └── examples/                 ← tested example inputs
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

- Week folders are always two digits: `week01` … `week13`.
- Each course's `COURSE.md` defines exactly which files go in `input/` and what their names are.
- `input/` (and `textbook/`, where a course has it) belong to the student. **Never edit, rename or delete anything in them.**
- Claude writes only to `work/` (intermediate files) and `notes/` (final outputs) inside the week being processed, plus any other location the course's `COURSE.md` explicitly allows. Ask before touching anything else, including `tools/`, `templates/` and the command files.

## The three stages

Every course uses the same three commands. What each stage does is defined in `COURSE.md` under the headings **Stage: prep**, **Stage: notes** and **Stage: practice**.

| Command | Purpose | Typical output |
|---|---|---|
| `/prep` | Read the raw inputs, extract structure, and produce anything the student must check or act on | `work/manifest.md` (+ course-specific work files) |
| `/notes` | Write the main study notes | `notes/weekNN-notes.md` |
| `/practice` | Write practice problems with worked solutions | `notes/weekNN-practice.md` |

Between `/prep` and `/notes` there is usually a **manual checkpoint** (defined per course). `/notes` must confirm the checkpoint was done before proceeding. If it wasn't, say what's missing and ask whether to continue.

If a course's `COURSE.md` says a stage doesn't exist, the command says so and stops.

---

## Universal rules

### Accuracy
- **Don't invent content.** Anything unclear that the sources don't resolve gets written as "unclear in source" and listed under Gaps.
- Never guess page numbers, problem numbers, values or symbols. If a handwritten or spoken value is ambiguous, mark it **⚠ uncertain** and give the most likely reading(s).
- If sources conflict, state the conflict explicitly. Don't quietly pick one.
- Any numerical answer that can be checked by running code should be checked by running code (see the course profile for how, and `tools/README.md`). Final outputs must say what was machine-verified and what wasn't. If a needed Python package is missing, tell the student to run `pip install -r requirements.txt`. Don't skip the check.

### Citations
Cite sources inline and compactly. Use only the tags a course has:

| Tag | Meaning |
|---|---|
| `[L1 S12]` | Lecture 1, slide 12 |
| `[L2 23:10]` | Lecture 2 recording, timestamp 23:10 |
| `[T p.114]` | Textbook page 114 |
| `[Tut Q3]` | Tutorial sheet, question 3 (`[Tut Q3b]` for parts) |
| `[TA p2]` | TA's handwritten notes, page 2 |

### Emphasis
Mark anything an instructor or TA signals as important ("this will be tested," "common mistake," boxed or starred items, repeated explanations) with **⭐** at the start of the line, followed by the course's label (e.g. **⭐ Quiz flag:** or **⭐ Exam flag:**).

### Writing style
- Plain-language explanation first, then precise details, then an example.
- Paraphrase sources. Quote only when exact wording matters (definitions, theorem statements).
- Use LaTeX for math: `$...$` inline, `$$...$$` display. Use aligned environments or tables for multi-line work.
- Every notes file ends with a **Gaps & conflicts** section.

### Multiple parts in a week
Courses may have several lectures or other parts per week, labelled `L1`, `L2`, … Process them one at a time (read, then write that part) to keep context small. `/notes` and `/practice` accept an optional part argument (e.g. `L2`) to do just one part. `/practice` may also accept course-defined modes (e.g. `exam`), listed in that course's `COURSE.md`. When run for a single part, only that part's section of the output file is written or replaced, and the rest is left untouched.

### Usage limits (Claude Pro)
- Read each input once per stage. Don't re-read large files you already have in context.
- Don't spawn subagents.
- If a stage is getting long, finish the current part cleanly, tell the student where you stopped, and tell them the exact command to continue in a fresh session.

### Ending every stage
Finish with a 3–6 line summary: what was produced, counts (topics, flags, problems), anything the student must check, and the next command to run.

---

## Adding a new course
1. Create `courses/<short-name>/` with `COURSE.md`, `templates/notes-template.md`, `templates/practice-template.md` and `weeks/`.
2. Write `COURSE.md` using an existing profile as the model. It must define: **Course info, Inputs, Stage: prep, Manual checkpoint, Stage: notes, Stage: practice, Source priority, Course-specific rules.**
3. The commands work immediately; no changes to this file or `.claude/commands/` should be needed. If they are, that's a sign something course-specific leaked into the shared engine.
