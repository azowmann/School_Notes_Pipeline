# Course profile: Linear Optimization (`linopt`)

## Course info
- Assessment: **assignments, a midterm and a final exam**. There are no quizzes.
- Emphasis label: **⭐ Exam flag:**
- There is no lecture recording or transcript, and no textbook is used by the pipeline.
- Weekly materials: lecture slides, a tutorial sheet, and the TA's handwritten tutorial solutions.
- The number of lectures per week isn't fixed. Process however many `slides-L*.pdf` files are present.

## Inputs

```
weeks/weekNN/
└── input/
    ├── slides-L1.pdf          ← one file per lecture: slides-L1.pdf, slides-L2.pdf, …
    ├── slides-L2.pdf
    ├── tutorial.pdf           ← the tutorial question sheet (tutorial-2.pdf etc. if more than one)
    └── ta-notes/              ← the TA's handwritten solutions
        ├── p1.jpg             ← photos or scans, one per page, in order: p1, p2, p3 …
        └── p2.jpg             ← (a single ta-notes.pdf instead of this folder is also fine)
```

- The tutorial sheet goes in the week the tutorial **happened**. Tutorials often cover the previous week's lectures, so `/prep` maps each question to lecture topics from this week or earlier weeks.
- If a week has no tutorial (holiday, midterm week), process the slides only and say so.
- If slides come as .pptx, ask the student to export them to PDF.
- Photos of handwriting should be well lit, flat and in focus. If a page is too blurry to read with confidence, say so and ask for a better photo rather than guessing.

## Stage: prep (transcribe and map)
1. **Read the slides**, one lecture at a time. For each lecture, list its topics, definitions, theorems or results, algorithms, and any worked examples on the slides. Mark anything the slides visibly emphasize (boxed, starred, "important", "exam") as ⭐.
2. **Read the tutorial sheet.** Type out every question in full in LaTeX, keeping the original numbering (Q1, Q2a …).
3. **Transcribe the TA's handwritten notes** into `work/ta-transcription.md`:
   - Put the student-review line at the very top: `Reviewed by student: NO`.
   - Organize it by tutorial question. For each question give the TA's full working, typed in LaTeX, in the order the TA wrote it. Use aligned environments for algebra and markdown tables for simplex tableaux.
   - Transcribe faithfully. **Don't fix the TA's working here**, even if it looks wrong. That comes later.
   - Mark every symbol, subscript, sign or number you can't read with certainty as **⚠**, followed by your best reading and any alternatives, e.g. `x_2 ⚠(x_3?)`.
   - End each question with a line **TA's final answer:** stating the answer as written.
   - Note anything the TA underlined, boxed or wrote as a tip ("common mistake", "always check…"). These become ⭐ items.
4. **Verify the TA's answers.** For every tutorial question with a numerical LP answer (optimal value, optimal solution, shadow prices), encode the problem as JSON and run `.venv/Scripts/python tools/verify_lp.py <file>` (see `tools/README.md`). Save the specs to `work/verify/tutorial-QN.json`. Record the result for each question: ✅ matches, ❌ doesn't match (give both values), or — not machine-checkable (proofs, conceptual questions, formulation-only).
   - A ❌ usually means a transcription misread, not a TA error. Check the ⚠ marks for that question first and say which reading would make it match.
5. **Write `work/manifest.md`:**
   - **Lecture topics**, per lecture: a bullet list with slide ranges, e.g. "Simplex method: pivoting [L1 S8–S15]".
   - **Tutorial map:** a table with the columns Question, Topic, Lecture it relies on (this or an earlier week, e.g. `week04 L2`), Question type (formulation / graphical / simplex / duality / sensitivity / proof / other) and Verification (✅/❌/—).
   - **Emphasis:** ⭐ items from slides and TA notes, with citations.
   - **Student checklist:** the number of ⚠ marks in the transcription, every ❌, and any page that was hard to read.

## Manual checkpoint
The student opens `work/ta-transcription.md`, checks it against the handwritten pages, fixes any wrong ⚠ readings directly in the file, and changes the top line to `Reviewed by student: YES`. The student may edit this file even though it's in `work/`.
`/notes` checks for `Reviewed by student: YES`. If it isn't there, say so and ask whether to continue with the unreviewed transcription. If the student fixed ⚠ readings, re-run the verification for the affected questions before writing the notes.

## Stage: notes
Output `notes/weekNN-notes.md` using `templates/notes-template.md`. Read the slides one lecture at a time, plus the reviewed transcription and manifest.

- **Exam flags at a glance** at the top: every ⭐ item, tagged by source.
- **One part per lecture**, organized by the slides' topics. For each topic give:
  - **Intuition:** what the idea is for, in plain language (a geometric picture where one helps).
  - **Definitions and results:** stated precisely in LaTeX, with conditions. Include a proof sketch only if the slides give one.
  - **Method:** algorithms written as numbered steps (e.g. how to choose the entering and leaving variable, how to form the dual).
  - **Worked example:** the slide example, or the matching tutorial question solved cleanly. If the TA's working was ❌ and the student confirmed the transcription, present the corrected solution and note the discrepancy in Gaps.
  - **Common mistakes:** from TA tips and slide warnings. Don't invent pitfalls with no source unless they're standard (e.g. sign errors when converting ≥ constraints), and label those "(general tip)".
- **Tutorial solutions:** every tutorial question with a clean, complete solution in the lecture's notation, cited `[Tut Qn]` and `[TA pN]`, and its verification status (✅ / — ).
- **Gaps & conflicts** at the end, including anything the slides skip that a solution needed, notation that differs between slides and TA, and unresolved ⚠ items.
- **Notation:** follow the lecture slides' notation (e.g. whether the standard form is max or min, what the basic and non-basic variables are called, tableau layout). If the TA uses different notation, convert to the slides' notation and note it once.

## Stage: practice
Output `notes/weekNN-practice.md` using `templates/practice-template.md`. Base it on this week's notes (and earlier weeks' notes only for prerequisites). **Only use techniques covered up to this week.** Don't set a duality question before duality has been taught.

Three sections of problems, 8–14 problems in total:

1. **Tutorial variants (≈ 1 per tutorial question):** same structure and skill as the original question, with new numbers and a new word-problem context. Cite the original, e.g. "(variant of [Tut Q3])".
2. **From the slides (≈ 1–2 per major topic):** new problems testing each slide concept, including topics the tutorial didn't cover.
3. **Exam-style (2–3):** multi-part problems that chain skills the way midterm and exam questions do, e.g. formulate, then solve, then interpret a shadow price. Weight these toward ⭐ items.

Mix question types to match what was taught: formulation from a word problem, graphical solution (2 variables), simplex iterations, identifying special cases (unbounded, infeasible, degenerate, alternative optima), duality, sensitivity analysis, and short conceptual or "true/false, justify" questions.

**Solutions** go in a separate section after all the problems. Each one is fully worked in the slides' notation, with the method shown the way it would be marked on an exam (not just the final answer).

**Design for clean numbers:** choose coefficients so optimal solutions are integers or simple fractions. Solve with `verify_lp.py` while designing, and adjust the numbers until the answer is clean.

**Verification is required.** Every problem with a numerical LP answer gets a JSON spec in `work/verify/practice-PN.json`, run through `verify_lp.py` with the claimed answer included. The practice file ends with a **Verification table**: problem, what was checked, ✅/❌. **No ❌ may remain in the final file.** Fix the solution or the problem and re-run. For intermediate tableaux, check at least that the final tableau's solution and objective match the solver. Non-numerical parts are marked "not machine-checked".

### Exam mode
`/practice linopt weekNN exam` writes a cumulative practice set covering week01 through weekNN into `exam-prep/weekNN-cumulative.md` (the student allows writing to `courses/linopt/exam-prep/`). It has 10–15 problems, weighted toward ⭐ Exam flags across all weeks' notes, mostly exam-style multi-part, with solutions and a verification table at the end. Read the notes files only, not the raw inputs, to save usage.

## Source priority
1. **Lecture slides:** notation, definitions, the version of each algorithm the student is expected to use, and what's in scope.
2. **Solver verification:** the authority on numerical answers. If a (reviewed) TA answer disagrees with the solver, trust the solver and flag it.
3. **TA notes:** worked methods, tips and what the TA stresses.
4. **Tutorial sheet:** the exact wording of questions.

## Course-specific rules
- Citations used: `[L1 S12]`, `[Tut Q3b]`, `[TA p2]`.
- Show all LP working in LaTeX. Use markdown tables for tableaux, with the basis in the first column and the RHS in the last. Bold or mark the pivot element and state the entering and leaving variables and the ratio test each iteration.
- State whether each problem is max or min and whether the variables are non-negative. Never leave sign restrictions implicit.
- For special cases (unbounded, infeasible, alternative optima, degeneracy), say how to recognize them in the tableau, not only the conclusion.
- Proofs and conceptual answers can't be machine-checked. Base them on results stated in the slides and cite them.
