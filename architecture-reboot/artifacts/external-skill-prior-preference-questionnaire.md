# External skill retrieval questionnaire — prior note-preference recovery

You have a skill/instruction set built from this clinician's prior answers about how they want
neurology notes structured and rendered.

Your task in this pass is **retrieval only**.

## Rules

1. Answer only from instructions that are clearly documented in your skill.
2. Do not infer an answer from general neurology knowledge, your own note-writing habits, or what seems
   clinically reasonable.
3. For every answer, return one of:
   - **EXPLICITLY DOCUMENTED**
   - **NOT DOCUMENTED**
   - **AMBIGUOUS / PARTIALLY DOCUMENTED**
4. For every EXPLICITLY DOCUMENTED answer:
   - state the answer concisely;
   - quote the shortest relevant instruction or identify the exact section/rule in your skill;
   - explain in one sentence why that instruction answers the question.
5. If the skill contains a general rule that directly determines several questions, you may cite the
   same rule repeatedly rather than inventing separate rationales.
6. Preserve distinctions in the skill. In particular, do not collapse:
   - A/P representation vs PRIMARY encounter role;
   - historical disease vs current residual deficit;
   - current adoption vs historical presence;
   - POSSIBLE vs LIKELY causal contribution.
7. Do not answer questions about the engineering architecture. We only want the clinician's documented
   clinical/note preferences.
8. Do not tell us how you personally would write the note yet. That will be a separate follow-up.

## Questions

### A. What deserves its own neurologic A/P representation?

**Q1.** When a patient is currently being evaluated for recurrent falls, should "falls since June"
receive its own neurologic A/P problem?

**Q2.** Can a major established neurologic diagnosis such as a prior left MCA stroke still receive its
own compact A/P representation even when it is not a current primary problem?

**Q3.** Does giving that prior stroke its own compact A/P representation automatically make it
`PRIMARY` for the current encounter, or can it remain `BACKGROUND`?

**Q4.** Should a medication line such as "aspirin 81 mg daily" by itself become its own neurologic A/P
problem?

### B. PRIMARY vs BACKGROUND

Use these definitions only to understand the question:
- PRIMARY = actively evaluated/managed now, or independently driving current neurologic
  assessment/management.
- BACKGROUND = established/suspected neurologic disease or finding that is not itself a primary
  current problem.

**Q5.** In a visit focused on falls, if prior left MCA stroke is not independently being evaluated or
managed, should the stroke be PRIMARY or BACKGROUND?

**Q6.** If the stroke becomes the subject of active secondary prevention, vascular imaging, recurrent
stroke concern, antithrombotic management, or another stroke-specific decision, can it become PRIMARY
in addition to the falls problem?

**Q7.** Should PRIMARY problems generally receive greater prominence/detail than BACKGROUND neurologic
problems?

### C. Historical disease vs current adoption

**Q8.** If a prior neurology note documents a left MCA stroke with residual right-sided weakness, but
the current encounter merely concerns falls and does not reuse that history in today's formulation,
should the old stroke/residual deficit be treated as a newly adopted current-encounter claim?

**Q9.** If today's clinician explicitly says, "Her chronic right-sided weakness from the prior stroke
may contribute to the falls," is the chronic residual weakness now part of the current encounter
formulation even though the old stroke itself remains historical/background?

**Q10.** Is historical presence alone enough to infer that a diagnosis is stable, worsening, treated,
untreated, followed outpatient, or causally responsible for a current syndrome?

### D. Causal relationship to a current syndrome

**Q11.** In a falls case, should causal contribution be judged separately from whether the underlying
neurologic disease is PRIMARY or BACKGROUND?

**Q12.** Can a BACKGROUND neurologic disease still have a likely or possible causal contribution to a
PRIMARY current syndrome?

**Q13.** When an old stroke contributes through persistent right-sided weakness, should the causal
formulation preferentially name the **current residual weakness** rather than simply say "the old
stroke causes/contributes to the falls"?

**Q14.** If the current source says the chronic right-sided weakness **may contribute** to the falls,
should that be preserved as a possible contribution rather than upgraded to likely/definite?

**Q15.** If the current encounter never states or supports a causal relationship between the chronic
stroke deficit and the falls, should the note avoid inventing one merely because both are present?

**Q16.** When several contributors are present, should their relative weighting be preserved (for
example, one primary/favored cause with additional contributors) rather than flattening them into equal
importance?

### E. What belongs together in a problem formulation?

**Q17.** For a falls problem, is "three falls since June" appropriately paired with "no new weakness or
speech trouble" as part of the same problem formulation/supporting reasoning?

**Q18.** Is "prior left MCA infarct" appropriately paired with its chronic residual neurologic deficit
as one compact background stroke representation?

**Q19.** Should an unrelated medication fact such as "aspirin 81 mg daily" be inserted into the falls
claim/representation merely because it appears in the chart?

### F. Intentional reuse

**Q20.** Is it acceptable for the same underlying neurologic information to do two jobs in the A/P:
for example, chronic right-sided weakness appears as causal evidence in the falls block while the
underlying prior stroke is also retained as a compact background problem?

## Output format

Return a table with exactly these columns:

| Question | Status | Documented answer | Skill support | Why it applies |
|---|---|---|---|---|

Then add:

### Additional clearly documented rules relevant to these questions
List any directly relevant rule in the skill that was not captured above.

### Unanswered / ambiguous items
List only the question numbers that are NOT DOCUMENTED or AMBIGUOUS/PARTIALLY DOCUMENTED.

Do not add new clinical preferences and do not answer from general knowledge.
