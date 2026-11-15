# ChatGPT review 008 — implementation guidance by submodule

## Verdict

DeepSeek proposal 006 is substantially aligned with the agreed architecture and with ChatGPT proposal 007.

The implementation layer is **not quite frozen** because three wording rules should be corrected before freeze. These are local corrections; they do not reopen any function or interface.

The shared implementation principle remains:

> Use LLM judgment for semantic decisions, precise prose for policy/boundaries, and typed DSL/pseudocode/canonical operators for accounting, composition, ordering, completeness, and fail-closed execution.

And globally:

> A submodule may not widen its remit to rescue an ambiguous or malformed input.

---

# I1 — Source Map

## Do
- Use explicit headings, labels, delimiters, blank lines, and speaker turns first.
- Preserve pasted source order.
- Classify source family when adequately supported.
- Use UNKNOWN/UNLABELLED when source family is not supportable.
- Keep source boundaries explicit.

## Avoid
- Merging sources.
- Reordering sources for neatness.
- Guessing source family from weak plausibility.
- Synthesizing across sources.
- Deciding note relevance.

## Control
- LLM_JUDGMENT for source-family recognition.
- PROSE_POLICY for conservative classification.
- TYPED_DSL / MECHANICAL_RULE for registry, IDs, ordering, and coverage.

---

# I2 — Span Registry

## Do
- Split only at approved mechanical boundaries.
- Preserve source order.
- Keep back-pointers/offsets.
- If a block cannot be safely segmented, retain it as one flagged span.

## Avoid
- Semantic splitting.
- Merging speaker turns.
- Rewriting text.
- Renumbering/reconstructing spans later.

## Control
- MECHANICAL_RULE dominant.
- Minimal LLM_JUDGMENT.

---

# I3 — Object Extraction

## Do
- Enumerate independently useful clinical propositions.
- Create one stable object per proposition.
- Preserve negation, uncertainty, attribution, numbers, and clinically meaningful qualifiers.
- Remain lexically conservative and source-faithful.
- Link every object to exact source evidence.
- Prefer over-extraction to silent loss.

## Avoid
- Deciding relevance.
- Combining propositions from different spans.
- Cleaning up into note prose.
- Adding unsupported clinical content.
- Dropping hedges/negations.
- Treating a failed extraction as evidence that the source span was nonclinical.

## Anti-fabrication
Use the agreed lexical-support guard:
- source anchor required;
- content tokens supported after closed morphology/abbreviation/source-preserving normalization;
- unsupported candidate -> EXTRACTION_ERROR / UNRESOLVED, not NOT_CLINICAL.

## Control
- LLM_JUDGMENT dominant.
- PROSE_POLICY strong.
- TYPED_DSL / MECHANICAL_RULE for object accounting and lexical guard.

---

# I4 — Source Annotation

## Do
- Attach supported source, date, speaker, span, source temporality, and other source-grounded attributes.
- Leave unsupported metadata absent.
- Preserve explicit clinician stance/adoption statements as source evidence.

## Avoid
- Inferring event date from source date.
- Guessing speaker.
- Inferring encounter-level adoption.
- Converting implications into provenance.

## Control
- Structured/mechanical copying where possible.
- LLM_JUDGMENT only where source interpretation is genuinely required.
- PROSE_POLICY defines temporality/provenance boundaries.

---

# S1 — Problem Model

## Do
- Group by clinical subject/problem concept.
- Define the current neurologic claim/problem at appropriate granularity.
- Keep neurologic claims as the organizing unit.
- Include non-neurologic problems separately only when materially necessary.
- Order problems according to encounter importance using the note contract.

## Avoid
- Deciding duplicate identity.
- Assigning sections/operators.
- Writing prose.
- Creating a problem solely from a medication or isolated historical diagnosis.
- Forcing every chronic diagnosis into a separate problem.

## Correction to DeepSeek 006
Do **not** freeze `acuity then management weight` as the universal ordering algorithm.

Problem order is a semantic/documentation policy that may depend on:
- reason for consult/current dominant neurologic issue;
- acuity;
- management consequence;
- encounter emphasis.

The exact ordering policy should be specified later and tested, not assumed to be a mechanical acuity sort.

## Control
- LLM_JUDGMENT dominant.
- PROSE_POLICY strong.
- Minimal DSL for problem accounting.

---

# S2 — Semantic Adjudication

## Do
- Resolve duplicate/related/distinct relationships.
- Attach modifiers and conditions.
- Assign reasoning roles.
- Decide encounter-level adoption where supported.
- Preserve original object identity/text; express interpretation through relationships/status.

## Avoid
- Rewriting objects.
- Assigning sections/operators.
- Inferring adoption from drug class or generic plausibility.
- Collapsing distinct numeric/time propositions as duplicates.
- Forcing ambiguous duplicate identity; unresolved is safer than false equivalence.

## Control
- LLM_JUDGMENT dominant.
- PROSE_POLICY defines semantic categories.
- TYPED_DSL constrains outputs to explicit relation/status vocabulary and object IDs.

---

# S3 — Content Selection & Problem Use

## Do
- Decide retained vs omitted content.
- Give every omitted clinical object an explicit disposition/reason.
- Assign each retained object to one or more problems.
- Preserve same object ID for cross-problem reuse.
- Account for every object exactly once at the usage/disposition level.

## Avoid
- Silent dropping.
- Cloning objects for another problem.
- Choosing sections/operators.
- Creating new clinical facts.
- Treating duplicate coverage as deletion from source accounting.

## Control
- LLM_JUDGMENT for relevance/problem fit.
- PROSE_POLICY for note-content rules.
- TYPED_DSL / MECHANICAL_RULE for total accounting and reuse.

---

# S4 — Note Blueprint / Render-Unit Compilation

## Do
- Determine ordered section list.
- Assign section, unit membership, member roles, rhetorical class, operator, and order.
- Enforce completeness.
- Typecheck every unit.
- Allow zero-member standing-item units only under the closed standing-item contract and satisfied trigger.

## Avoid
- Writing prose.
- Adding unsupported clinical content.
- Leaving retained content without representation.
- Emitting malformed units.
- Allowing RENDER to make missing semantic decisions.

## Correction to DeepSeek 006
Replace:

> "Don't invent a unit."

with:

> **Do not create an unsupported unit.**

S4 necessarily *creates render units* from structured content, and it may create an explicitly authorized zero-member standing-item unit. The prohibited behavior is creating a unit with no supported object use or approved standing-item trigger.

## Control
- TYPED_DSL / pseudocode dominant.
- LLM_JUDGMENT only for decisions still semantically open, such as section/operator choice where contracts do not mechanically determine them.
- MECHANICAL_RULE for typing/completeness/uniqueness/order.

---

# R1 — Unit Realization

## Do
- Execute the selected canonical operator.
- Use referenced object payload plus operator-fixed text.
- Apply only approved folds and section-scoped style transformations.
- Emit exactly the specified output cardinality.
- Fail closed on malformed units.

## Avoid
- Selecting/omitting/reordering content.
- Changing operators.
- Repairing incomplete payloads.
- Adding new clinical meaning.
- Looking back at raw source to rescue the unit.

## Correction to DeepSeek 006
Replace:

> "Don't add a word."

with:

> **Do not add any content outside referenced object payload, operator-fixed text, or explicitly allowed surface transformations.**

Operators necessarily add fixed function/clinical framing words.

## Control
- CANONICAL_OPERATOR / TYPED_DSL dominant.
- Minimal generative freedom.

---

# R2 — Section Composition

## Do
- Apply only to prose-composed sections.
- Preserve unit order and every unit's meaning.
- Join with allowed punctuation/whitespace/local grammatical continuity.
- Fall back to uncomposed unit-per-line output when safe composition cannot be maintained.

## Avoid
- Applying to A/P.
- Dropping/reordering units.
- Semantic merging.
- New causal/temporal relationships.
- New certainty/uncertainty.
- Global polishing/rewrite.

## Control
- LLM language ability within hard PROSE_POLICY.
- Mechanical order/coverage guard.
- No broad free-form rewrite instruction.

---

# R3 — Note Assembly

## Do
- Follow the Case IR section order exactly.
- Emit approved headings/furniture.
- Insert prose-section output or direct bullet/unit output as specified.
- Apply final formatting only.

## Avoid
- Adding/removing/reordering sections.
- Rewriting content.
- Moving content between sections.
- Final global polish.

## Control
- MECHANICAL_RULE / template assembly dominant.

---

# Cross-cutting implementation rule

For every function:

1. **Semantic decision?**
   - LLM_JUDGMENT + PROSE_POLICY.
2. **Closed structural/accounting decision?**
   - TYPED_DSL / MECHANICAL_RULE.
3. **Stable wording required?**
   - CANONICAL_OPERATOR.
4. **Cannot satisfy contract?**
   - fail/flag within that submodule;
   - do not perform the neighboring submodule's job.

---

# Freeze status

With the three corrections above, I would consider the **broad implementation guidance** frozen:

- what each submodule should do;
- what it should avoid;
- which control mechanism should dominate.

Still downstream and not yet frozen:
- exact prompt prose;
- exact pseudocode syntax;
- exact schemas/field names;
- exact operator vocabulary;
- exact problem-order policy;
- exact normalization/lexical-support tables;
- exact failure-code vocabulary.

Those details should be designed and experimentally validated after this implementation layer is accepted.
