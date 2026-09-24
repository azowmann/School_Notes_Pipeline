---
description: Write practice problems with worked solutions from a week's notes, or run a course-defined mode such as exam.
argument-hint: <course> <week> [part|mode]
---

Run the **practice** stage for a course week.

Arguments given: `$ARGUMENTS`

## 1. Parse the arguments

Expected form: `<course> <week> [part|mode]`.

- **course** — a directory name under `courses/`.
- **week** — either `weekNN` or a bare number. Pad bare numbers to two digits: `3` → `week03`.
- **third argument** — optional, and it is either:
  - a **part** (e.g. `L1`, `L2`) — write or replace only that part's problems and leave the rest of the file untouched; or
  - a **mode** — the profile's **`## Stage: practice`** section lists the modes this course defines (e.g. `exam`). Only modes listed there are valid.

  Decide which it is by checking the profile's listed modes first, then the week's parts. If the argument matches neither, say so, list the valid parts and modes, and ask.

Do not guess. Stop and ask if the course or week is missing, if `courses/<course>/` does not exist (list what does), or if `courses/<course>/weeks/<week>/` does not exist.

## 2. Load the course profile

Read `courses/<course>/COURSE.md` in full. Where it conflicts with `CLAUDE.md`, it wins.

Find its **`## Stage: practice`** section. If the profile has no such section, say this course defines no practice stage and stop.

## 3. Check the prerequisites

This stage normally builds on the week's notes. If `weeks/<week>/notes/weekNN-notes.md` does not exist, say so and ask whether to run `/notes <course> <week>` first.

If a mode was given, follow that mode's own instructions in the profile for what to read and where to write — they may differ from the default (a cumulative mode, for instance, may read several weeks' notes and write outside the week folder). Only write outside `weeks/<week>/` where the profile explicitly allows it.

## 4. Run the stage

Read `courses/<course>/templates/practice-template.md` and follow its structure.

Carry out the profile's **`## Stage: practice`** section exactly as written — problem counts, the mix of sections and question types, how solutions are presented, and any scope limit on which techniques may appear. All of that comes from the profile, not from this command.

Apply the shared rules in `CLAUDE.md`: cite sources with the course's tags, weight toward **⭐** items, keep solutions in the course's notation, and use LaTeX for math.

**Verify every checkable answer by running code**, in the way the profile describes, and record the results where the profile says to. If the profile requires that no failed check remains in the final file, fix the problem or the solution and re-run until that holds. Mark anything that cannot be machine-checked as such.

Process one part at a time if the week has several, and only the named part if one was given.

Default output is `weeks/<week>/notes/weekNN-practice.md`, unless the profile or the chosen mode says otherwise. Never write to `input/` or `textbook/`.

## 5. Finish

End with a 3–6 line summary: what was produced, the problem count and the mix, the verification result, anything the student must check, and the exact next command to run.
