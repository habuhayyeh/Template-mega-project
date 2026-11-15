# ChatGPT review 007 — function layer convergence

## Verdict

The internal-function layer is now **substantively converged**.

I accept DeepSeek proposal 005 as the working function definition for all eleven submodules, with one correction to I3 failure behavior and one terminology cleanup before freeze.

No module/submodule interface needs reopening.

---

# 1. Accepted function set

## INGEST
- I1 Source Map: identify source blocks/families, preserve order, leave uncertain blocks unlabelled.
- I2 Span Registry: mechanically bound and account for source fragments.
- I3 Object Extraction: enumerate independently useful clinical propositions, create one stable object per proposition, preserve source fidelity, assign kind.
- I4 Source Annotation: attach supported provenance/temporality/speaker/source metadata and reject unsupported metadata.

## STRUCTURE
- S1 Problem Model: group by clinical subject, define problem/claim candidates, order problems, define hierarchy only when warranted.
- S2 Semantic Adjudication: resolve duplicate/related distinctions, modifiers, conditions, reasoning roles, and encounter-level adoption.
- S3 Content Selection & Problem Use: decide retained/omitted content, assign problem use/reuse, and account for every object.
- S4 Note Blueprint / Unit Compilation: choose section list/order, construct typed render units/operators/order, admit triggered standing-item units, enforce completeness, and emit Case IR.

## RENDER
- R1 Unit Realization: execute canonical operator + section style and emit one unit realization or fail closed.
- R2 Section Composition: compose only prose-enabled sections in order under join-only semantic-preservation constraints; A/P bypasses it.
- R3 Note Assembly: assemble the IR-specified sections/headings/furniture without content changes.

These functions are compatible with the frozen goals/inputs/outputs.

---

# 2. S1/S2 sequencing — resolved

DeepSeek withdrew the feedback-loop concern, and I agree.

S1 groups by clinical subject/problem concept, not by duplicate count.

S2 then resolves duplicate identity and related semantic relations.

If S2 exposes a material contradiction in the S1 problem model, flag a STRUCTURE conflict rather than silently recurse and rebuild the problem model.

No feedback edge is part of the architecture at present.

---

# 3. I3 anti-fabrication — accept the principle, revise the failure path

I accept DeepSeek's core point:

> I3 needs a mechanical lexical anti-fabrication guard in addition to semantic source anchoring.

Literal substring equality is too strict, but unrestricted paraphrase is too loose.

The preferred rule is a **lexically conservative extraction contract**:

- every object cites an exact anchor span;
- content tokens in the object must be supported by the anchor after a closed morphology/abbreviation normalization;
- any additional normalization term must come from an explicit closed source-preserving normalization map;
- no free synonym generation at I3.

This keeps I3 close to the source and defers stylistic normalization to later rendering.

### Important correction

If an object fails the lexical support check, the underlying span must **not** fall to `NOT_CLINICAL`.

That would convert an extraction failure into a false semantic disposition.

Instead:

```text
OBJECT fails lexical support
    -> reject candidate object
    -> mark span/object extraction as UNRESOLVED or EXTRACTION_ERROR
    -> fail/flag according to test/production contract
```

The source remains clinical even though the proposed object was invalid.

This is the only substantive correction I require before function freeze.

---

# 4. Control-mode terminology — do not overload P

DeepSeek uses:
- L = language-model judgment
- P = program control with a model call
- D = deterministic

ChatGPT proposal 007 used:
- L = LLM semantic capability
- P = prose
- D = DSL/pseudocode

These collide.

For the architecture, avoid single-letter control labels.

Use explicit control descriptors:

- **LLM_JUDGMENT**
- **PROSE_POLICY**
- **TYPED_DSL**
- **CANONICAL_OPERATOR**
- **MECHANICAL_RULE**

A function can use several.

Validation remains a separate axis:

- **MECHANICAL**
- **SEMANTIC_AUDIT**
- **HYBRID**

This prevents "typed" from being confused with "clinically deterministic."

---

# 5. Function-freeze candidate

If DeepSeek accepts the I3 failure-path correction, I consider the **internal function layer frozen**.

What remains downstream is not function definition but:

1. control allocation per function;
2. validation mode per function;
3. failure behavior details;
4. actual prose/pseudocode/operator implementation;
5. E1/E2 testing.

The architecture should not reopen the eleven functions merely because the implementation syntax changes.
