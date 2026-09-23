# Course profile: Environment & Society (`envs`)

## Course info
- Assessment: **weekly quizzes**, due Sunday at midnight, covering the previous week's lectures.
- Emphasis label: **⭐ Quiz flag:**
- Each week has **two lectures (L1, L2)**. Each has its own slides and recording. Slides and recordings are released Monday morning.
- Textbook: physical copy only. The student provides screenshots of the pages the professor references.

## Inputs

```
weeks/weekNN/
├── input/
│   ├── slides-L1.pdf
│   ├── transcript-L1.txt
│   ├── slides-L2.pdf
│   └── transcript-L2.txt
└── textbook/            ← student's screenshots, added after /prep
    ├── ch4_p112.png
    └── ch4_p113.png
```

- Screenshot names are `chX_pYYY.png`. If one page needs two images, name them `chX_pYYYa.png` and `chX_pYYYb.png`.
- If only L1 exists that week (holiday or cancellation), process L1 only and say so.
- If slides come as .pptx, ask the student to export them to PDF.

## Stage: prep (find textbook pages)
Process L1 fully (slides, then transcript), then L2. Write `work/manifest.md`:

1. **Textbook references**, split into Lecture 1 and Lecture 2. Make a table with the columns Chapter, Pages, what the pages cover, evidence (a timestamp or short quote) and confidence (high/medium/low).
   - List only pages the professor said aloud or that appear on the slides.
   - If he names a section but gives no pages, write "student to look up."
   - Ambiguous or garbled numbers get low confidence, with the reason.
   - Flag any reference that doesn't match the lecture's slide topics.
2. **Screenshot checklist (whole week).** List the exact filenames, deduplicated across lectures and sorted by chapter and page. Tag each one L1, L2 or both. If L2 continues an L1 topic, note it in one line.
3. **Professor emphasis**, split by lecture, with timestamps and the related slide.
4. **Off-slide content**, split by lecture: examples, clarifications and analogies he gave that aren't on the slides.
5. **Transcript fixes**: likely auto-caption errors on terms, names and numbers, with the corrected version and evidence.

## Manual checkpoint
The student reviews the page list (especially low-confidence rows) and saves every screenshot on the checklist into `textbook/`.
`/notes` checks that each filename on the checklist exists. If any are missing, list them and ask whether to continue.

## Stage: notes
Work one lecture at a time. For each lecture, read its slides, its transcript and only the screenshots tagged for that lecture or both, then write its part. Output `notes/weekNN-notes.md` using `templates/notes-template.md`:
- Week header, then **Quiz flags at a glance** (tagged L1/L2).
- **Part 1: Lecture 1 — [title]**, organized by L1's slides.
- **Part 2: Lecture 2 — [title]**, organized by L2's slides. If it continues an L1 topic, link back instead of repeating.
- **Gaps & conflicts** (tagged L1/L2).
- Fix transcript errors silently in the notes. They're already listed in the manifest.

## Stage: practice
Read `notes/weekNN-notes.md` and write `notes/weekNN-practice.md`: 10–15 quiz-style questions covering both lectures roughly evenly (tag each L1/L2), weighted toward ⭐ items, mixing recall, conceptual and applied questions. Put the answers, with a short explanation and a citation, in a separate section at the bottom.

## Source priority
1. **Slides:** structure and order of the notes.
2. **Textbook:** the authority on definitions, facts and figures.
3. **Transcript:** emphasis, intuition, examples, and what the professor expects students to know.

For quiz purposes, the professor's stated expectation usually wins a conflict, but flag the conflict anyway.

## Course-specific rules
- Auto-captions garble technical terms, names and numbers. Check them against the slides and textbook.
- Citations used: `[L1 S12]`, `[L1 23:10]`, `[T p.114]`.
- No computation to verify in this course; practice answers are checked against the notes and cited sources.
