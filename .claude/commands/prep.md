---
description: Read a week's raw course materials and produce work/manifest.md plus whatever else that course's prep stage defines.
argument-hint: <course> <week>
---

Run the **prep** stage for a course week.

Arguments given: `$ARGUMENTS`

## 1. Parse the arguments

Expected form: `<course> <week>`.

- **course** — a directory name under `courses/`.
- **week** — either `weekNN` or a bare number. Pad bare numbers to two digits: `3` → `week03`, `12` → `week12`.

Do not guess. Stop and ask if:
- No arguments were given, or either argument is missing.
- `courses/<course>/` does not exist. List the directories that do exist under `courses/` and ask which was meant.
- `courses/<course>/weeks/<week>/` does not exist. Say so and ask whether to create it, and remind the student that `input/` is theirs to fill.

## 2. Load the course profile

Read `courses/<course>/COURSE.md` in full. It is the authority on this course; where it conflicts with `CLAUDE.md`, it wins.

Find its **`## Stage: prep`** section. If the profile has no such section, say that this course defines no prep stage and stop.

## 3. Check the inputs

The profile's **Inputs** section lists exactly which files belong in `weeks/<week>/input/` and what they are named. List what is actually present.

- If required inputs are missing, say which ones and ask whether to continue with what's there or wait.
- Honour whatever the profile says about optional or variable inputs (e.g. a week with only one lecture, or a missing tutorial). Follow its instruction rather than treating the absence as an error.
- If an input is in a format the profile says to reject (e.g. `.pptx` slides), ask the student to convert it before continuing.

Reading anything else in the repo the profile needs — earlier weeks' manifests, `tools/README.md`, course templates — is fine. The restriction is on writing: write only inside `weeks/<week>/work/`, plus any location the profile explicitly allows (e.g. `weeks/<week>/work/verify/`). Never write to `input/` or `textbook/`, and never modify anything outside the current week's folder.

## 4. Check for existing work

Look at what's already in `weeks/<week>/work/` before writing anything.

- **Files the student may have edited** — the profile's **Manual checkpoint** section says which files, if any, the student is allowed to edit in `work/` (e.g. a transcription they review and correct). If such a file already exists, do not overwrite it silently. Show its current status (e.g. a "reviewed" line at the top, if the profile defines one) and ask whether to:
  - **keep it as is** and skip regenerating it,
  - **regenerate it from scratch** (discarding any edits — confirm this is intended), or
  - **only add what's missing** (e.g. a new lecture part that wasn't there before) while leaving the rest of the file untouched.
- **Purely generated files** (nothing the profile lists as student-editable, e.g. `manifest.md`) can be regenerated freely. Note in the final summary that they were regenerated.

If `work/` doesn't exist yet, or is empty, skip this check and proceed normally.

## 5. Run the stage

Carry out the numbered steps in the profile's **`## Stage: prep`** section exactly as written, in order. Everything course-specific — which files to read, what to extract, what to write, which tools to run — comes from that section, not from this command.

While doing it, apply the shared rules in `CLAUDE.md`: don't invent content, mark uncertain readings **⚠**, state conflicts rather than resolving them silently, use the course's citation tags, mark emphasis with **⭐** and the course's label, and verify any checkable numbers by running code.

If the week has multiple parts (lectures), process them one at a time — read a part, write its section, then move to the next — to keep context small.

Write output only to `weeks/<week>/work/` (creating it if needed), plus any other location the profile explicitly allows.

## 6. Finish

End with a 3–6 line summary: what was produced, the relevant counts, which files (if any) were regenerated vs. kept vs. partially updated, anything the student must check or act on (the profile's **Manual checkpoint** section says what), and the exact next command to run.
