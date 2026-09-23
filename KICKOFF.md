# Kickoff: building the pipeline with Claude Code

This folder holds only the **design**. Claude Code builds everything else.

| File | What it is |
|---|---|
| `CLAUDE.md` | Shared rules for every course. Claude Code reads this automatically in every session. |
| `courses/envs/COURSE.md` | Spec for Environment & Society |
| `courses/linopt/COURSE.md` | Spec for Linear Optimization |

Read the three specs first and change anything you disagree with, such as note style, number of practice problems or file names. It's much cheaper to change the design now than after it's built.

---

## Step 1: Build the shared engine and tools

Open Claude Code in this folder, switch to **plan mode**, and paste:

```
Read CLAUDE.md and both courses/*/COURSE.md files. They're the design for a multi-course study-notes pipeline. Your job is to build what they describe. Don't change the design without asking me.

Build in this order, and stop for my review after each numbered step:

1. The three generic slash commands in .claude/commands/: prep.md, notes.md, practice.md.
   - Each parses $ARGUMENTS as <course> <week> [part|mode], pads bare week numbers to weekNN, and asks rather than guesses if anything is missing.
   - Each loads courses/<course>/COURSE.md and runs the matching "Stage:" section. The commands must contain NO course-specific logic: all course detail comes from COURSE.md.
   - /notes must check the course's Manual checkpoint before proceeding.
   - Add frontmatter with a description and argument-hint.

2. tools/verify_lp.py plus tools/README.md and requirements.txt. Requirements:
   - Input is a JSON file with one problem or a list: sense (max/min), c, constraints [{coef, op (<=, >=, =), rhs, optional label}], optional vars, bounds (default all >= 0), integer, and an optional "claimed" block (status, z, x, duals).
   - Solve with scipy (linprog with HiGHS; milp for integer problems).
   - Print status, z*, x*, and per constraint the slack and shadow price, meaning dz*/d(rhs) in the problem's own max/min sense, with the correct sign for >= and = constraints. Print numbers as simple fractions where possible.
   - Compare against "claimed" and print PASS/FAIL per item. A claimed x that differs from the solver's but is feasible with the same z counts as PASS (alternative optimum). On a dual mismatch, warn that degenerate LPs can have several valid duals.
   - Exit code 1 if any check fails.
   - Put test cases in tools/examples/ and run them. Include: max 3x1+5x2 s.t. x1<=4, 2x2<=12, 3x1+2x2<=18 (answer z=36 at (2,6), duals 0, 3/2, 1); a min problem with >= constraints; an unbounded problem; an integer program; one deliberately wrong claim that must FAIL; and one alternative optimum that must PASS. Show me the output.

3. tools/render_pdf.sh: markdown to PDF via pandoc and xelatex, with a clear error if pandoc is missing.

4. Templates: courses/<course>/templates/notes-template.md and practice-template.md for both courses, matching the structure each COURSE.md describes (flags at a glance, one part per lecture, Gaps & conflicts, and for linopt a tutorial-solutions section and a verification table).

5. README.md with one-time setup (pip install, optional pandoc) and a short weekly checklist per course. Also create the empty week and exam-prep folders.

Finally, check consistency: every path, section heading and file name referenced across CLAUDE.md, the COURSE.md files, the commands and the templates must line up. Report any mismatch.
```

Take your time with each review stop. Step 2 matters most, because every Linear Optimization answer depends on the verifier being right.

## Step 2: Test with one real week per course

After the build, `/clear` and run the pipeline on a real week:

```
/prep envs week03
```
…take the screenshots, then `/notes envs week03` and `/practice envs week03`.

```
/prep linopt week03
```
…review `work/ta-transcription.md`, then `/notes linopt week03` and `/practice linopt week03`.

## Step 3: Tune it

Tell Claude what to change, for example "the linopt notes are too long, keep full tableaux only in the tutorial solutions". Ask it to put the change in the course's `COURSE.md` or template, not just this week's notes, so it applies every week.
