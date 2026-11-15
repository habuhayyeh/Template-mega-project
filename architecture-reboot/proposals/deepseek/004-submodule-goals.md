# DeepSeek proposal 004 — a goal for each submodule, and what is still open

One goal per submodule, one guarantee it must make. Where a goal is contested, the question is listed at the end rather than hidden.

---

## INGEST

| Submodule | Goal | Must guarantee |
|---|---|---|
| **Source Map** | Turn the paste into an ordered, identified set of sources — who, what, when — so every later claim can name where it came from. | Every character of the paste belongs to exactly one source, or is explicitly ignored (separator, whitespace). |
| **Span Accounting** | Make coverage a fact rather than a hope: every span ends with a disposition. | No span is unaccounted; no object exists without a span. |
| **Object Extraction** | Decompose spans into atomic clinical propositions, in the source's own words. | High recall — over-production allowed, silent loss not; no paraphrase. |
| **Object Annotation** | Attach provenance, source temporality, speaker, and span pointer to each object. | Every object traceable to one span; no metadata the source does not support. |

## STRUCTURE

| Submodule | Goal | Must guarantee |
|---|---|---|
| **Clinical / Problem Model** | Decide which problems the note is about, in what order, and which reasoning object is the claim of each. | One claim per problem; no problem without a claim; order justified by acuity/weight. |
| **Object Adjudication** | Decide what each object means for this encounter: duplicates, current adoption, whether it is used at all. | Every object ends used, covered, or dispositioned with a reason. |
| **View Projection** | Decide *which objects are used, under which problem* — a set, not a shape. | No operator choice, no ordering, no wording. |
| **Render-Unit Compilation** | Give that set a shape: membership and roles, section, operator, order, bucket. | Units typecheck against their operator; no object added or dropped relative to projection. |
| **Coverage Completion** | Guarantee the IR is structurally complete before rendering. | Every problem has a claim unit; every current plan item has a plan unit; every surviving reasoning object has a unit; a section exists only if it has a unit. |

## RENDER

| Submodule | Goal | Must guarantee |
|---|---|---|
| **Unit Realization** | Render one unit as one line, inside the operator's allowances. | One line per unit; no content outside the unit and the transformation table; malformed unit yields `CONTRACT_ERROR`. |
| **Section Composition** | Join realized lines into a section's paragraphs. | Join only, in unit order; no deletion, reordering, or new connectives. |
| **Note Assembly** | Emit the sections in the order it is given, with headings. | May not add, omit, or reorder sections; may not edit their content. |

---

## What is still open

**Q1. Projection vs Compilation — cut or merge.** My cut is above: projection is a set, compilation is a shape. If ChatGPT prefers one `Unit Composition` submodule, the goal statement collapses to one line and one owner. Either is workable; the current tree leaves it ambiguous, which is not.

**Q2. Where section list, order and empty-section omission live.** They are structural and belong in STRUCTURE, but not obviously to one of its four. Candidate homes: `Clinical / Problem Model` (it already orders problems) or `Coverage Completion` (it already decides whether a section has a unit). **Unresolved, and it needs one owner.** My preference: `Coverage Completion`, because "a section with no unit is omitted" is the same decision as completeness.

**Q3. Is Coverage Completion its own submodule?** It has a distinct goal and a distinct failure (missing unit). It could also be the last step of Compilation. I prefer it separate, because a failure there should be attributable to completeness, not to unit construction.

**Q4. Does Section Composition exist for the A/P at all?** The A/P is bullets under a line; there is nothing to compose. If composition applies only to HPI/history/exam prose, that should be stated, or the submodule will start merging A/P bullets into paragraphs.

**Q5. Units with no objects.** A standing item (`Seizure precautions`) is a required line with no source object. Nothing in the current tree says whether that is legal. It must be: a unit whose operator is `STANDING_ITEM` and whose members are empty, admitted only for entries on the closed list. **This is a gap, not a preference.**

**Q6. Who owns the note's fixed furniture** — title, patient identifiers, section headings. My assumption is Note Assembly, with the values coming from an `IDENTIFIER` object. Not stated anywhere.

---

## What I would not do yet

Schema, field names, operator list, unit ids. Those are downstream of Q1–Q6, and settling them first would lock in answers to questions we have not asked.
