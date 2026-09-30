# Course profile: Environment & Society (`envs`)

## Course info
- Assessment: **weekly quizzes**, due Sunday at midnight, covering the previous week's lectures.
- Emphasis label: **⭐ Quiz flag:**
- Each week normally has **two lectures**. Each has its own slides and recording. Slides and recordings are released Monday morning.
- Lectures are numbered **cumulatively across the semester**, not reset per week (e.g. week 3 may be lectures 5 and 6, not 1 and 2). Never assume a week's two lectures are `L1`/`L2` — detect the actual numbers from the filenames present.
- Textbook: physical copy only. The student provides screenshots of the pages the professor references.

## Inputs

```
weeks/weekNN/
├── input/
│   ├── slides-L<A>.pdf
│   ├── transcript-L<A>.txt
│   ├── slides-L<B>.pdf
│   └── transcript-L<B>.txt
└── textbook/            ← student's screenshots, added after /prep
    ├── ch4_p112.png
    └── ch4_p113.png
```

- `<A>` and `<B>` are that week's actual lecture numbers (e.g. `L5`/`L6`). Detect them by finding whatever `slides-L*.pdf`/`transcript-L*.txt` pairs exist in `input/` — don't assume any specific numbers.
- Screenshot names are `chX_pYYY.png`. If one page needs two images, name them `chX_pYYYa.png` and `chX_pYYYb.png`.
- If only one lecture exists that week (holiday or cancellation), process it alone and say so.
- If slides come as .pptx, ask the student to export them to PDF.

## Stage: prep (find textbook pages)
Detect the week's two lecture numbers from the input filenames. Process the lower-numbered lecture fully (slides, then transcript), then the higher-numbered one. Write `work/manifest.md`, tagging every item by its actual lecture number (e.g. `L5`, `L6`) rather than `L1`/`L2`:

1. **Textbook references**, split by lecture number. Make a table with the columns Chapter, Pages, what the pages cover, evidence (a timestamp or short quote) and confidence (high/medium/low).
   - List only pages the professor said aloud or that appear on the slides.
   - If he names a section but gives no pages, write "student to look up."
   - Ambiguous or garbled numbers get low confidence, with the reason.
   - Flag any reference that doesn't match the lecture's slide topics.
2. **Screenshot checklist (whole week).** List the exact filenames, deduplicated across lectures and sorted by chapter and page. Tag each one by lecture number or "both". If the later lecture continues an earlier topic, note it in one line.
3. **Professor emphasis**, split by lecture number, with timestamps and the related slide.
4. **Off-slide content**, split by lecture number: examples, clarifications and analogies he gave that aren't on the slides.
5. **Transcript fixes**: likely auto-caption errors on terms, names and numbers, with the corrected version and evidence.

## Manual checkpoint
The student reviews the page list (especially low-confidence rows) and saves every screenshot on the checklist into `textbook/`.
`/notes` checks that each filename on the checklist exists. If any are missing, list them and ask whether to continue.

## Stage: notes
Work one lecture at a time, in ascending order of lecture number. For each lecture, read its slides, its transcript and only the screenshots tagged for that lecture or both, then write its part. Output `notes/weekNN-notes.md` using `templates/notes-template.md`:
- Week header, then **Quiz flags at a glance** (tagged by lecture number).
- **Part 1: Lecture \<A\> — [title]**, organized by its slides.
- **Part 2: Lecture \<B\> — [title]**, organized by its slides. If it continues a topic from lecture \<A\>, link back instead of repeating.
- **Gaps & conflicts** (tagged by lecture number).
- Fix transcript errors silently in the notes. They're already listed in the manifest.

## Stage: practice
Read `notes/weekNN-notes.md` and write `notes/weekNN-practice.md`: 10–15 quiz-style questions covering both lectures roughly evenly (tag each by lecture number), weighted toward ⭐ items, mixing recall, conceptual and applied questions. Put the answers, with a short explanation and a citation, in a separate section at the bottom.

## Source priority
1. **Slides:** structure and order of the notes.
2. **Textbook:** the authority on definitions, facts and figures.
3. **Transcript:** emphasis, intuition, examples, and what the professor expects students to know.

For quiz purposes, the professor's stated expectation usually wins a conflict, but flag the conflict anyway.

## Course-specific rules
- Auto-captions garble technical terms, names and numbers. Check them against the slides and textbook.
- Citations used: `[L<n> S12]` (slide number), `[L<n> 23:10]` (recording timestamp), `[T p.114]` (textbook page), where `<n>` is the lecture's actual number, e.g. `[L5 S12]`.
- No computation to verify in this course; practice answers are checked against the notes and cited sources.
