# ChatGPT review 049 — exact review of execution-layer corrections

## Verdict

**REVISE AGAIN. DO NOT RUN GATE 0 OR AX-S1S2-D YET.**

DeepSeek corrected several important items from review 048, but the exact files do not support the claim that all 17 corrections are fully applied.

The architecture-spec layer remains CLOSED / CONVERGED.
This review is execution-layer only.

---

# 1. Gate 0 seed IDs do not match the scorer predicates they are supposed to calibrate

Gate 0 currently names predicates such as:

- `S1_NO_ADOPTION_VERDICT`
- `S1_NO_FINAL_CLAIM`
- `S1_CANDIDACY_SOURCE_GROUNDED`
- `S2_REP_SOURCE_GROUNDED`
- `S2_APPROVAL_SAFETY`
- `S3_INCLUSION_REQUIRES_APPROVAL`
- `S4_INCLUSION_IMMUTABLE`

But the actual AX-S1S2-D predicate file uses:

- `S1-AUTH-01`
- `S1-AUTH-02`
- `S1-CAND-01` / `S1-CAND-02`
- `S2-REP-01`
- `S2-REP-02`
- `S3-INC-01`
- `S4-INC-01`
- etc.

Therefore Gate 0, as written, does **not** calibrate the exact predicate set that will score AX-S1S2-D.

## Required repair

Every runnable seed must reference the exact current predicate id from the scorer predicate registry.

If a seed calibrates a different/general predicate registry, that registry must exist and the mapping to AX predicates must be frozen explicitly.

Do not rely on name similarity.

---

# 2. G0-S1-03 remains the same mis-specified seed

Review 048 explicitly rejected:

> body-only historical fact -> `S1_CANDIDACY_SOURCE_GROUNDED`

The revised file still contains exactly that logic.

A body-only historical fact is source-grounded.

The defect is:
> it does not warrant an independent current assessment question/problem candidate.

## Required repair

Target the actual candidacy predicate:
> `S1-CAND-01` or the exact experiment-local candidacy predicate that encodes independent assessment relevance.

The source-anchor seed remains separate:
> invented candidate without source anchor -> `S1-CAND-02`.

---

# 3. G0-S2-04 remains underspecified

Review 048 required replacing:

> "S2 marks a problem approved while its only candidate is contradicted"

because contradiction does not by itself prohibit an approved representation.

The revised seed still says exactly that.

## Required repair

Seed a true violation, e.g.:

> S2 emits a settled/single approved representation while silently deleting or failing to preserve an explicit conflicting source assertion and without recording the contradiction/adjudication.

That calibrates `S2-CONF-01`.

---

# 4. Gate 0 only declares parent_type/mutation_path requirements; it does not instantiate them

The file now says every seed **must** name:
- `parent_type`;
- `mutation_path`;
- exact `expected_fire`;
- exact `must_not_fire`.

But the tables still omit them "for brevity."

That means the seeds are still **not runnable**.

A calibration manifest may describe the future seed schema, but it cannot be called execution-ready until each seed record actually contains the required fields.

## Required repair

Create explicit per-seed records or expand the tables with:
- parent artifact id/type;
- exact mutation path;
- exact predicate id(s);
- exact unrelated predicate ids that must remain silent.

---

# 5. G0-S1-01 is not aligned with revised S1-AUTH-01

Gate 0 still mutates:

> add an adoption verdict string ("current", "adopted")

But revised `S1-AUTH-01` deliberately rejected lexical checking and now tests:

> presence of an adoption **field/decision** in S1.

A string mutation can trigger false semantics and does not necessarily calibrate the schema predicate.

## Required repair

Mutate the S1 artifact structure:
> add a forbidden adoption-status field/value at a declared path.

Do not calibrate a field-level predicate with a banned-word seed.

---

# 6. Generic Gate 0 attribution remains unresolved

The generic table still says:

> G0-X-01 owner R1  
> G0-X-02 owner S4

but no actual `parent_type` or mutation path has been attached to those rows.

Therefore review 048's attribution problem remains.

Examples:

- inserted new word in an R1 realization -> R1;
- same word inserted only in R3 final assembly -> not R1;
- duplicate already present in S4 blueprint -> S4;
- duplicate introduced only during R2/R3 composition -> not S4.

Until artifact level is instantiated per seed, owner calibration is not valid.

---

# 7. Gate 0 and AX predicate files conflate scorer-calibration repetitions with experiment repetitions

The AX predicate file says:

> `MECHANICAL` — deterministic, one run.  
> `SEMANTIC` — judged, three runs, must agree 3/3.

and later:

> semantic predicates require 3/3 agreement; 2/3 is a **calibration failure** and blocks the verdict.

This is incorrect in the experiment file.

There are two separate things:

## Gate 0 calibration
- mechanical scorer predicate may need one deterministic calibration execution;
- semantic scorer calibration uses the frozen 3/3 seeded-defect gate.

## AX-S1S2-D experiment
- the experiment itself has 3 fresh Doximity repetitions;
- every valid repetition is scored;
- a semantic predicate that passes 2/3 is an **experiment reproducibility/nonconformance result**, not a Gate 0 calibration failure.

Gate 0 has already happened before the experiment verdict exists.

## Required repair

In `predicates.md`:

- define `MECHANICAL` vs `SEMANTIC/HYBRID` as **scoring mode**, not experiment run count;
- say all valid experiment repetitions are scored;
- reserve "calibration failure" for Gate 0 only;
- specify how 2/3 experiment disagreement is reported, without relabeling the scorer uncalibrated.

---

# 8. Architecture-escalation rule is still too permissive

The manifest now says:

> `FAIL_STRUCTURAL` requires a structural predicate false in all valid runs, and substrate/scorer excluded as causes.

That is better, but still not the architecture-reopen rule we froze.

A model can violate a perfectly coherent interface 3/3 because:
- the implementation prompt is bad;
- Doximity cannot reliably follow the implementation;
- the test schema is underspecified;
- a downstream contract needed for the behavior is missing.

Three repeated misses show reproducible nonconformance. They do **not** prove the architecture requires an authority violation.

## Required repair

Architecture escalation requires a separate adjudication showing:

> the correct requirement cannot be satisfied under the canonical interfaces without violating their responsibility boundary,

after excluding:
- fixture/substrate defect;
- scorer defect;
- implementation noncompliance;
- missing downstream schema/contract;
- execution/platform artifact.

A repeated structural predicate failure is evidence prompting that adjudication, not the adjudication itself.

Do not let `FAIL_STRUCTURAL` be synonymous with "reopen architecture."

---

# 9. F-1 placeholder logic is still backwards

The corpus now correctly demotes F-1 to an observation, but says:

> only the third outcome — model marks the absence — sustained across cases argues for a schema addition.

That does not follow.

If the current architecture reliably marks the absence correctly **without** a new schema, that is evidence that a new schema may **not** be needed.

The real sequence is:

1. decide the product behavior for unknown-but-clinically-relevant fields;
2. construct source packages that establish the relevant unknown state;
3. test whether the current architecture can meet that required behavior;
4. only if the required behavior cannot be represented/reliably preserved should a schema/design change be proposed.

Inventing or silently omitting a required unknown marker would be evidence of failure **if explicit marking is actually required**.

## Required repair

Keep F-1 as:
> OPEN PRODUCT / REPRESENTATION-SCHEMA QUESTION.

Remove the "only the third argues for schema" inference.

Also mark `P-08` as `PENDING_PRODUCT_DECISION`; it currently assumes "unknown values render as slots" before that product behavior is settled.

---

# 10. S1-AUTH-01 over-restricts S1's canonical output

The revised predicate says:

> a candidate carries only subject, anchors, salience, and candidate claims.

But canonical DC-001 S1 output also permits:

> candidate-level relationships the substrate states explicitly.

Therefore the predicate accidentally forbids a canonical S1 output field.

## Required repair

Test only the prohibited authority:

> S1 contains no S1-owned adoption/final-state decision field.

Do not whitelist the entire S1 schema unless the experiment-local schema includes every allowed canonical output.

---

# 11. S2-ADOPT-02 is not mechanical as written

Current:

> no adoption is inferred from medication, drug class, or convention; an adoption must cite a source span.

A source-span citation is mechanically checkable.

But whether that span contains **explicit adoption linkage** rather than merely a medication mention is semantic.

CASE-01 vs CASE-09 exists precisely because this distinction depends on the meaning of the sentence.

## Required repair

Either:

- classify this predicate HYBRID/SEMANTIC; or
- define a test-schema field carrying the already-adjudicated explicit-link relation and mechanically check that field.

Do not label "not inferred from convention" mechanical without a structured oracle.

---

# 12. S3-ACCT-01 adds a mandatory "reason" that the emitted schema does not define

Current:

> every substrate object is used or dispositioned **with a reason**.

The canonical interface requires:
- retained use;
- explicit disposition for unused clinical objects;
- complete accounting.

It does not currently freeze a mandatory free-text disposition reason field.

The experiment artifact format says only:
> dispositions

not:
> disposition reason.

## Required repair

For this pilot either:
- require only used-or-explicitly-dispositioned; or
- define an experiment-local typed disposition code/reason field before calling this mechanical.

Do not silently turn "reason" into a new architecture requirement.

---

# 13. S4-REP-01 needs representation identity in the experiment-local schema

Current predicate is mechanical:

> S4 consumes the exact representation S3 selected.

But the frozen artifact-format summary does not specify a representation id/key that can be compared mechanically across S3 and S4.

## Required repair

The experiment-local test schema must expose a stable representation reference/key for:
- S2 approved representations;
- S3 selected representation;
- S4 claim-bearing use.

This is local test schema, not a global architecture freeze.

Without that, `S4-REP-01` is not yet mechanical.

---

# 14. S2-REP-02 cannot be both PENDING_SCHEMA and currently human-scoreable without a defined semantic predicate

Current text says:

> PENDING_SCHEMA ... not scoreable until schema exposes marker; until then a human decides and records the reasoning.

Those statements conflict.

If it is not scoreable, it must not contribute to the pilot verdict.

If a human semantic judgment is intended before schema exists, define the exact semantic predicate and its oracle.

## Required repair

Choose one:
- `PENDING_DEPENDENCY` and exclude from pilot verdict; or
- define a SEMANTIC/HYBRID predicate now with a frozen human judgment rule.

---

# 15. S4-ORD-01 is correctly pending; Gate 0 must not pretend to calibrate it yet

AX predicate:
> `S4-ORD-01` = PENDING_DEPENDENCY

Gate 0 still includes:
> G0-S4-03 reorder ignoring ordering contract

Until the ordering contract/salience oracle exists, that seed cannot be calibrated for this pilot.

## Required repair

Mark the Gate 0 ordering seed pending too, or supply the missing test oracle.

Gate 0 should calibrate only predicate families/instances actually scoreable in the pilot.

---

# 16. Fixture provenance statement is misleading

The manifest says:

> CASE-01/02/09 are reconstructed from BASELINE-01 and the signer's prior-stroke material.

But BASELINE-01 is the 46F carpal-tunnel teaching case, whereas these fixtures are a 72F prior-stroke/falls/seizure counterexample set.

That wording creates false provenance.

## Required repair

Describe them accurately as:
> DERIVED synthetic architecture fixtures based on the prior-stroke/adoption counterexamples developed during architecture review.

If there is an exact durable source artifact for the prior-stroke material, cite/name it.

Do not imply that the 72F stroke fixtures were reconstructed from BASELINE-01.

---

# 17. Fixture dates are future-dated relative to the current project date

All three transcript spans use:
> 2026-11-16

The current project date is 2026-11-15.

Because these fixtures specifically test temporality/adoption, an accidental future encounter date is unnecessary confounding.

## Required repair

Use the intended encounter date consistently, preferably 2026-11-15, or explicitly declare a synthetic future-date convention if future dating itself is intentional.

Do not introduce temporal noise into the adoption discriminator.

---

# 18. CASE-01 expected wording remains ambiguous

Manifest/predicates say:

> infarct not adopted; problem renders with historical attribution or not at all

But the frozen fixture also says:
> exactly one A/P problem: falls.

Clarify that "problem renders..." refers specifically to the **infarct subject**:
> infarct does not render as an A/P problem; infarct information may appear only as attributed body/history context if selected.

That removes ambiguity.

---

# 19. Current readiness

## Conceptual architecture
CLOSED / CONVERGED.

## Gate 0
AUTHORED / UNRUN, but **not yet executable** because exact seed records, predicate IDs, and several seed definitions remain unresolved.

## AX-S1S2-D pilot
AUTHORED / UNRUN, but **not yet scoreable** because:
- calibration mapping is not exact;
- some predicates are misclassified or dependency-pending;
- experiment vs calibration repetition logic is conflated;
- escalation logic is still too strong;
- local schema lacks fields needed for several "mechanical" checks.

## Doximity
Do not run yet.

## Phase 0
Do not touch.

---

# 20. Required next revision

DeepSeek should revise only the execution artifacts:

1. exact Gate 0 seed records mapped to current predicate ids;
2. correct G0-S1-03 / G0-S2-04 / G0-S1-01 mutations;
3. artifact-level parent type/path per seed;
4. separate calibration repetition rules from experiment scoring rules;
5. architecture-escalation adjudication separated from repeated model nonconformance;
6. F-1/P-08 product-decision correction;
7. S1-AUTH-01/S2-ADOPT-02/S3-ACCT-01/S4-REP-01/S2-REP-02 corrections;
8. mark ordering seed/predicate pending consistently;
9. fix fixture provenance/date/CASE-01 wording.

Then send the exact files back for review.

No architecture redesign.
No Phase 0.
No Doximity run.
