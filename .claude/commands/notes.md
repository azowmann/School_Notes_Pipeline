---
description: Write a week's study notes from the prepped materials, after checking the course's manual checkpoint.
argument-hint: <course> <week> [part]
---

Run the **notes** stage for a course week.

Arguments given: `$ARGUMENTS`

## 1. Parse the arguments

Expected form: `<course> <week> [part]`.

- **course** — a directory name under `courses/`.
- **week** — either `weekNN` or a bare number. Pad bare numbers to two digits: `3` → `week03`.
- **part** — optional, e.g. `L1`, `L2`. If given, write or replace only that part's section of the notes file and leave the rest untouched. If omitted, do every part the week has.

Do not guess. Stop and ask if:
- No arguments were given, or the course or week is missing.
- `courses/<course>/` does not exist. List what does exist under `courses/` and ask.
- `courses/<course>/weeks/<week>/` does not exist.
- A part was named but the week has no such part. Say which parts are present.

## 2. Load the course profile

Read `courses/<course>/COURSE.md` in full. Where it conflicts with `CLAUDE.md`, it wins.

Find its **`## Stage: notes`** section. If the profile has no such section, say this course defines no notes stage and stop.

## 3. Check the manual checkpoint — before doing anything else

Read the profile's **`## Manual checkpoint`** section. It states what the student was supposed to do between `/prep` and `/notes`, and how this command verifies it.

Perform that verification exactly as the profile describes. If it has not been satisfied:
- Say precisely what is missing (name the missing files, or quote the line that should have changed).
- **Ask whether to continue anyway.** Do not proceed until the student answers.

Also confirm the prep stage actually ran — `weeks/<week>/work/manifest.md` should exist. If it doesn't, say so and ask whether to run `/prep <course> <week>` first.

If the profile says to redo any work when the student changed something during the checkpoint (for example re-running a verification), do that now, before writing.

## 4. Run the stage

Read `courses/<course>/templates/notes-template.md` and follow its structure.

Carry out the profile's **`## Stage: notes`** section exactly as written. All course detail — which sources to read, how to organize the notes, what each section must contain, the notation to follow — comes from that section and the template, not from this command.

Apply the shared rules in `CLAUDE.md`: source priority as the profile defines it, inline citations using only the course's tags, **⭐** plus the course's emphasis label for flagged items, **⚠** for uncertain readings, plain-language explanation before precise detail, LaTeX for math, and a **Gaps & conflicts** section at the end.

Verify by running code any number that can be checked, and state in the output what was machine-verified and what was not.

Process one part at a time — read that part's sources, write its section, then move on. If a part was named in the arguments, do only that one.

Write to `weeks/<week>/notes/weekNN-notes.md` (creating `notes/` if needed), using the week folder's own name for `weekNN`. Never write to `input/` or `textbook/`.

## 5. Finish

End with a 3–6 line summary: what was produced, counts (topics, flags, unresolved gaps), anything the student must check, and the exact next command to run.

If the profile mentions an optional PDF render, mention it here.
