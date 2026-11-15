# ChatGPT review 048 — Gate 0, corpus findings, and AX-S1S2-D executable review

## Verdict

**REVISE EXECUTION ARTIFACTS. DO NOT RUN YET.**

The architecture experiment specification layer remains CLOSED / CONVERGED.

DeepSeek has correctly moved into the execution layer, but the current Gate 0 and AX-S1S2-D artifacts are not yet safe to use as acceptance evidence.

The main issues are:
1. one new corpus observation was promoted to an architecture change without sufficient evidence;
2. Gate 0 contains several seeds that do not actually isolate the predicate they claim to calibrate;
3. the AX-S1S2-D manifest currently conflates model nonconformance with architecture failure;
4. several "mechanical" predicates are not mechanically scoreable from the artifact schema as written;
5. some fixtures contain internal inconsistencies or unresolved applicability markers.

No Phase 0 change is authorized.

---

# 1. Corpus F-1 — placeholder/unknown-slot claim is premature

DeepSeek states:

> placeholders are part of the target ... the Case IR needs an explicit unknown slot ... this is a genuine architecture addition.

I do **not** accept that conclusion yet.

The four baselines are explicitly described as:
> fictional teaching cases / templates

and contain authoring scaffolds such as:
- `[date]`
- `[confirm]`
- `[Add details here]`
- `"[Insert radiology impression verbatim]"`

Those markers can mean at least three different things:

1. **template scaffolding** — the author intentionally left a slot to be filled before clinical use;
2. **known-unknown clinical content** — the source explicitly establishes that a value is unknown/unavailable;
3. **missing source package in our test corpus** — the target note contains information we have not supplied as input.

Those are not the same requirement.

A template placeholder is **not evidence** that a production Doximity note should render a placeholder.

The current architecture already permits:
- source-grounded unknown/uncertain content;
- explicit unresolved/failure states;
- fail-closed behavior;
- downstream schema decisions.

## Correct classification

F-1 is currently:

> **OPEN PRODUCT / REPRESENTATION-SCHEMA QUESTION**

not:
> proven architecture defect.

Before any design change, establish the product rule:

> When a clinically relevant field is unknown at generation time, should the production final note:
> - omit it;
> - render an explicit marker;
> - preserve a source-stated "unknown";
> - fail/flag;
> - or vary by section/field contract?

That decision cannot be inferred from template placeholders alone.

Do **not** draft an architecture design change for unknown slots yet.

---

# 2. Corpus F-2 — ACCEPT

The baseline can contain an error or incomplete sentence.

BASELINE-01's:
> "...other differentials including radiculopathy and"

is a valid example.

Therefore:

- do not use literal text equality as the semantic oracle;
- maintain a baseline-defect/exclusion register;
- use property-based assertions;
- do not penalize a generated artifact for correcting a known target typo/truncation unless exact wording is itself contractual.

This is an execution/acceptance rule, not an architecture change.

---

# 3. Draft style properties P-01...P-10 are candidates, not frozen signer rules

The corpus index currently derives ten cross-note properties and a style contract from four notes.

Keep these labeled:

> **OBSERVED / CANDIDATE**

until signer-approved or independently supported by the canonical note-style contract.

Several may be true preferences, but four template notes do not establish universal production rules.

Examples that should not silently freeze yet:

- `P-03` approximate quantities always use `~`;
- `P-04` time expressions never use bare "ago";
- `P-05` all explicit negatives must remain separate bullets;
- `P-09` one proposition appears once per problem block;
- `P-10` lab-summary behavior as a universal rule;
- "do not expand the signer's abbreviations" as an absolute style rule.

Use them as candidate scorer predicates only after their scope is explicitly accepted.

---

# 4. Gate 0 overall design — directionally good

Accepted:

- calibration before scored evidence;
- predicate-family scoping;
- clean parent + single mutation;
- specificity controls;
- attribution checking;
- recalibration when scorer/predicate changes;
- real production misses becoming future seeds.

The 3/3 rule for semantic scorer calibration may remain as a **local gate** if it is explicitly described as:

> passed 3/3 under this scorer/prompt condition

not as a statistical reliability estimate.

---

# 5. Gate 0 seed G0-S1-03 calibrates the wrong predicate

Current seed:

> promote a body-only historical fact into an A/P problem candidate

Expected predicate:
> `S1_CANDIDACY_SOURCE_GROUNDED`

But the historical fact **is source-grounded**.

The defect is:
> it does not warrant its own current assessment question/status.

So this seed cannot calibrate source grounding.

## Required repair

Split the concepts:

- source grounding / anchor support;
- candidacy / independent assessment relevance.

G0-S1-03 should target a candidacy predicate such as:
> body-only/context-only subject must not become an independent S1 candidate.

G0-S1-04 can remain the true source-grounding seed:
> candidate with no source anchor/support.

---

# 6. Gate 0 seed G0-S2-04 is semantically underspecified

Current mutation:

> S2 marks a problem approved while its only candidate is contradicted

This is not automatically invalid.

A contradiction may legitimately yield:
- a differential;
- unresolved representation;
- an explicitly adjudicated selected representation with the conflicting assertion retained.

The architecture does **not** say:
> contradicted candidate can never participate in an approved representation.

## Required repair

Make the planted defect explicit, for example:

> S2 emits a settled/single approved representation that silently discards an explicit conflicting source assertion and records no adjudicated contradiction/unresolved relation.

Then the expected predicate is truly:
> contradiction was improperly collapsed/deleted.

---

# 7. Gate 0 generic seeds need artifact-level scoping

Examples:

### G0-X-01
> insert "resolved" absent from source and IR

Owner is listed as R1.

That is valid **only if the mutated parent artifact is explicitly an R1 unit realization**.

If the mutation is applied to a composed section/final note, the earliest owner may be R2/R3.

### G0-X-02
> render one proposition twice within a section+problem

Owner is listed as S4.

That is valid only if the duplicated representation is already present in the S4 blueprint.

If S4 is correct and R2/R3 duplicates prose, S4 is not the owner.

## Required repair

Every seed record must name:
- parent artifact type;
- exact mutated field/location;
- earliest owner implied by that artifact.

Gate 0 cannot calibrate attribution without this.

---

# 8. Gate 0 parent-status text is stale / conceptually imprecise

The seed file says:

> when the signer's notes arrive, real parents replace them

Signer target notes have now arrived, but target notes alone are not valid clean parents for S1/S2/S3/S4 artifact seeds.

A clean parent must be an artifact at the layer the seed is calibrating.

## Required wording

Use:

> DERIVED_PARENT remains until a suitable independently reviewed clean artifact exists at the relevant layer; signer target notes alone do not replace STRUCTURE parents without source/substrate-derived artifacts.

This avoids conflating:
- target note;
- source package;
- intermediate artifact.

---

# 9. AX-S1S2-D manifest — primary verdict rule is unsafe

Current manifest:

> any structural predicate false in >=1 run -> FAIL_STRUCTURAL

and:

> only FAIL_STRUCTURAL supports reopening the interface

That is too strong.

A single model execution can violate a canonical boundary even when the architecture itself is coherent.

Example:
- S1 outputs an adoption verdict despite being told not to.

That proves:
> implementation/model nonconformance in that run.

It does **not** prove:
> the interface architecture is impossible.

We explicitly closed this distinction in the experiment specification.

## Required repair

Separate three levels:

### Run/result state
Examples:
- `STRUCTURAL_NONCONFORMANCE`
- `SEMANTIC_NONCONFORMANCE`
- `EXECUTION_INVALID`

### Experiment verdict
Examples:
- passed under frozen condition;
- reproducible implementation failure;
- semantic contract/substrate defect;
- unresolved.

### Architecture escalation
Only after review establishes:

> satisfying the correct clinical requirement requires violating the canonical responsibility boundary, after excluding fixture/scorer/implementation/downstream-schema explanations.

Do not let a label named `FAIL_STRUCTURAL` automatically imply architecture reopening.

---

# 10. Missing/truncated artifacts should not be called BLOCKED

Current manifest says:

> any run missing an artifact is BLOCKED, not FAIL: a missing artifact is a harness or truncation problem.

This collapses different states.

A missing artifact can be:
- missing prerequisite before the run -> BLOCKED;
- platform truncation -> execution integrity failure;
- model failed to follow required output contract -> execution nonconformance;
- harness capture failure -> harness failure.

These matter differently.

## Required repair

Reserve `BLOCKED` for:
> experiment cannot be meaningfully attempted because a prerequisite is absent/undecidable.

Use a separate execution state for:
> run was attempted but output was missing/truncated/malformed.

Per the frozen protocol, execution integrity is Gate 1 and lower-gate failure prevents higher semantic claims.

Do not silently convert an attempted failed execution into a non-result.

---

# 11. S1-AUTH-01 is not a valid mechanical predicate as written

Current predicate:

> no `adopted`, `current`, `resolved`, `ruled out` in candidate or claim fields

This is a lexical ban, not an authority check.

A source-grounded candidate could legitimately contain words like:
- "current headache";
- "current symptoms";
- a quoted historical phrase containing "resolved".

The violation is:
> S1 expresses an adoption/final-state verdict in a field that owns only candidacy/source-grounded candidate formulations.

## Required repair

Score the **artifact structure/semantics**, not banned vocabulary.

Prefer:
- no adoption-status field in S1;
- no S1-owned adoption decision;
- candidate claim values remain source-grounded candidates rather than S1-selected final state.

If mechanical checking is desired, define a typed S1 schema that makes forbidden decision fields mechanically detectable.

Until then this predicate is HYBRID/SEMANTIC, not purely mechanical.

---

# 12. S2-REP-02 is not mechanically scoreable until the representation schema exists

Current predicate:

> at most one approved representation unless more than one is approved and each is marked selection-safe

But the executable artifact format only says:

> `representations[]`

It does not define:
- representation identity;
- support refs;
- approval state;
- selection-safe relation/field.

The architecture deliberately left exact representation schema downstream.

That is fine, but the experiment must define its **test schema** before a mechanical scorer can inspect it.

## Required repair

Either:

1. define an experiment-local representation schema sufficient to expose:
   - representation id;
   - members/source refs;
   - approved status;
   - selection-safe relation/state;
   - structured support refs;

or:

2. score the property semantically/hybrid until such a schema exists.

Do not call a predicate mechanical when its required fields are not in the emitted contract.

---

# 13. S3-INC-01 should apply to every rendered A/P problem

Current applicability:
> cases 01,03

But the invariant is universal:

> every rendered A/P problem requires an S2-approved representation.

The predicate should apply to **all cases that render an A/P problem**, not only two case IDs.

Case-specific expectations can still determine whether a problem should render.

---

# 14. S4-COMP-01 currently steals S3 selection authority

Current predicate:

> every current plan item has a plan unit

S4 does not decide which source plan items belong in the note.

S3 owns content selection.

The S4 invariant should be:

> every S3-retained / render-designated plan item has a corresponding plan unit, or an explicit allowed disposition already established upstream.

Otherwise an S3 omission will be misattributed to S4.

---

# 15. S4-ORD-01 is not yet scoreable

Current predicate:

> problem and unit order follow the ordering contract using S1 salience inputs

But the executable package does not yet freeze:
- the concrete ordering contract;
- the salience fields/values for these fixtures;
- expected order where ties/constraints exist.

So the predicate is declared before its oracle exists.

## Required repair

For the first executable batch either:
- freeze the actual test-ordering contract and salience values; or
- mark S4-ORD-01 `PENDING_DEPENDENCY` and do not score it.

Do not manufacture an order oracle after seeing the output.

---

# 16. Predicate applicability cannot contain question marks

Current S1-CAND-01 applicability includes:

> `07?,08?`

An executable manifest cannot have uncertain applicability.

For pending fixtures:
- keep predicate applicability pending;
- do not include a question mark in a frozen scored set.

Before a fixture becomes runnable, every predicate applicability state must be:
- applies;
- does not apply;
- conditional on an explicit predeclared finding.

---

# 17. Fixture CASE-01 has an internal sex/pronoun inconsistency

Scenario:
> 72M

Transcript:
> "check **her** vitamin D"

This is avoidable noise in a discriminating fixture.

Correct it before freezing/running.

A fixture testing adoption should not simultaneously contain an irrelevant identity/pronoun contradiction.

---

# 18. CASE-09 expected-outcome wording contains an unexplained "both"

Predicates file says:

> shared plan line references both

But CASE-09 is not a shared-action/multi-problem fixture.

Clarify exactly what "both" refers to, or delete that phrase.

Do not let AX-S1S2-D accidentally inherit AX-SHARED semantics.

---

# 19. The three derived substrates are legitimate micro-fixtures, but label their evidentiary scope correctly

The hand-built fixed substrates are appropriate for:

> can the STRUCTURE interfaces be obeyed under a controlled input substrate?

They are **not** evidence that:
- real source ingestion yields those substrates;
- realistic notes behave the same;
- signer target style is preserved.

This limitation is already mostly present and should remain prominent.

Do not wait for a real patient source package to run every architecture micro-fixture; synthetic/derived fixtures are legitimate for structural invariants when clearly labeled.

---

# 20. Recommended next sequence

Before any Doximity run:

1. **Do not pursue F-1 unknown-slot design change yet.**
2. Revise Gate 0 seeds/parent wording.
3. Define the exact scorer artifact type + test schema for the predicate families actually needed first.
4. Revise AX-S1S2-D verdict/execution states.
5. Fix predicate ownership/applicability issues.
6. Fix CASE-01 and CASE-09 fixture wording.
7. Independently review the revised Gate 0 + 3-case executable.
8. Run Gate 0 only after a real scorer exists.
9. If Gate 0 passes, run the three-case AX-S1S2-D pilot as a **pilot under derived substrates**, not the full 11-case acceptance batch.

The eight-experiment design remains closed.
The execution layer is not yet ready to run.
