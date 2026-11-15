# DeepSeek response 006 — module granularity

**Answer:** three runtime modules is correct. No fourth is justified by any failure we can point at.

---

## 1. `STRUCTURE` accepted as the label

`PLAN` is overloaded against the clinical plan, and the module is not a plan — it is the adjudication that produces the Case IR. `STRUCTURE` is the better name and I will use it.

## 2. Why three, with an argument rather than a preference

The count is not a matter of taste. **We have two audit instruments, and each audits one seam.**

- `CHECK` audits IR → note.
- `AUDIT` audits source → IR.

Two seams means three modules: source | INGEST | objects … STRUCTURE … IR | RENDER | note. A module boundary that no instrument audits is a label, not an architecture.

This gives a test for adding a fourth that is better than "it feels like a lot for one module":

> Add a runtime module only when a third instrument exists to audit the seam it creates.

Under that test, none of the candidate fourth modules qualifies today:

| Candidate | Why it fails the test |
|---|---|
| problem selection as its own module | its output is part of the IR; `AUDIT` audits it there, no separate seam |
| reasoning extraction as its own module | same — it produces objects, audited by source→IR |
| a second renderer pass ("polish") | nothing audits the polish; it would be unchecked rewriting |
| a deduplication module | dedup is a decision inside STRUCTURE, not a stage |

## 3. What would justify a fourth

Not complexity, and not the size of the IR. Evidence:

1. a measured failure class that is *systematically* owned by neither ingest nor structure — for example, if E1 shows ingest is stable but structure drifts on a specific decision type that could be isolated and audited on its own;
2. a third instrument that can audit the new seam mechanically or by oracle;
3. the new module removing a decision from STRUCTURE rather than moving it around.

Until one of those holds, a fourth module is a place to hide a decision, not a place to check one.

## 4. On the boundary clarification

Agreed, and it is worth stating precisely because it is easy to blur:

- **INGEST** records an explicit source-level adoption statement as an object — "the clinician said to resume apixaban once MRI excludes haemorrhage" is a fact about what was said.
- **STRUCTURE** decides the encounter-level adoption and use: whether a prior recommendation is adopted now, and whether it renders.

Ingest must not decide adoption from tone or plausibility; structure must not invent an adoption statement that the source never made. The two are different questions with different evidence.

## 5. What this settles

Three runtime modules, three external instruments, one build step. The granularity question is closed for me, and the test for reopening it is stated above in a form that can be applied to a future proposal without re-arguing.
