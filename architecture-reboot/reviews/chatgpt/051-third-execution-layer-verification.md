# ChatGPT review 051 — third execution-layer correction verification

## Verdict

**REVISE LOCALLY ONCE MORE. DO NOT RUN YET.**

The third correction pass fixes most of review 050, but the exact files still contain a small set of execution-blocking inconsistencies.

The architecture and eight experiment specifications remain CLOSED / CONVERGED.

---

# 1. ACTIVE_PREDICATE_SET does not match the three pilot cases

The pilot declares:

- `S1-BODY-01` active, but its applicability is CASE-07/08/10;
- `S2-CONF-01` active, but its applicability is CASE-11.

Neither predicate is exercised by CASE-01/02/09.

At the same time, the pilot omits:

- `S1-CAND-01`, which applies to CASE-01/02/09 and is the actual semantic candidacy predicate needed to decide whether the infarct incorrectly becomes its own problem.

This is especially inconsistent because the CASE-01 fixture explicitly says:

> if a run renders a prior-infarct A/P problem, that is `S1-CAND-01` failing.

But `S1-CAND-01` is not in the active pilot set.

## Required repair

For the three-case pilot, activate only predicates the three cases can actually exercise.

At minimum:
- add `S1-CAND-01`;
- remove `S1-BODY-01`;
- remove `S2-CONF-01`.

Do not calibrate or score future-case predicates in this pilot.

---

# 2. Three active pilot predicates have no Gate 0 seed

Current active set includes:

- `S1-CAND-01`
  - should be active after the repair above;
  - no Gate 0 seed currently targets it.
- `S2-ADOPT-01`
  - active now;
  - no Gate 0 seed targets it.
- `S4-COMP-01`
  - active now;
  - no Gate 0 seed targets it.

Yet the predicate file says:

> a predicate that has no Gate 0 seed is not yet scoreable.

## Required repair

Add exact Gate 0 seeds for every active predicate.

Suggested shapes:

### S1-CAND-01
Use a clean S1 parent and add a source-grounded subject that is merely contextual/history and does **not** pose its own current assessment question.

This calibrates candidacy semantics directly.

### S2-ADOPT-01
Use a case-specific clean S2 parent and flip the adoption verdict away from the frozen case expectation while preserving otherwise valid support structure.

This calibrates correctness of the adoption verdict itself, not merely presence of evidence.

### S4-COMP-01
From a clean S4 blueprint:
- remove the claim-bearing unit for a rendered problem; or
- remove the plan unit corresponding to an S3-retained plan item.

Single mutation only.

---

# 3. Gate 0 statement "11 seeds calibrate the pilot" is not currently true

Because the active set includes predicates with no seed and includes predicates irrelevant to the three cases, the statement:

> 11 seeds calibrate the predicates used by CASE-01/02/09

is not auditable as written.

After freezing the corrected active set:
- produce an explicit `ACTIVE_PREDICATE -> GATE0_SEED` mapping;
- every active predicate must have at least one calibrated seed or be removed from the verdict.

---

# 4. The typed schema contradicts the PENDING_SCHEMA labels

`schema.md` says pending predicates are absent because the schema does not expose:

> `selection_safe` and `representation id` well enough.

But the schema explicitly contains:

### S2
- `representations[*].id`
- `representations[*].selection_safe`

### S3
- `approved_representation`
- `selected_rep`

### S4
- `units[*].representation`

Therefore:

- `S4-REP-01` appears mechanically scoreable from the schema as written;
- `S2-REP-02` may also be scoreable if `representations[]` is explicitly defined as the approved set, or if an approval field/set is added.

The current statement "fields are absent on purpose" is factually inconsistent with the schema.

## Required repair

Choose deliberately:

### S4-REP-01
Either:
- activate it and calibrate it, since the representation key now exists; or
- explain exactly what is still missing despite the present ids.

### S2-REP-02
Either:
- define whether `representations[]` means approved representations and then mechanically/semantically score selection safety; or
- keep it pending but state the actual missing field/semantic contract.

Do not use a stale "schema does not expose the field" explanation when the field is present.

---

# 5. The 2/3 semantic experiment rule is still wrong in the exact file

`predicates.md` still says:

> Two of three is semantic nonconformance recorded as `UNSCORED` for that case.

But the manifest says:

- `NONCONFORMANT` = a required predicate false;
- `UNSCORED` = fewer than 3 valid runs.

These conflict.

A 2/3 outcome has three valid runs and at least one predicate failure.

## Required repair

Use:

> 2/3 = `NONCONFORMANT` under the frozen condition **plus a reproducibility disagreement finding**.

Reserve `UNSCORED` for:
- insufficient valid repetitions;
- missing prerequisite;
- predicate excluded/pending.

This is execution scoring, not Gate 0 calibration.

---

# 6. Corpus F-1 still makes a product decision before the product decision

The corpus now correctly says product behavior comes first, but immediately adds:

> a run that omits the slot entirely fails completeness.

That is not yet known.

If the product decision is:
> unsupported values should be omitted,

then omission is correct, not a completeness failure.

## Required repair

Until the product decision is made:

- invention of an unsupported value = fidelity failure;
- omission vs explicit marker = **not scoreable as correct/incorrect yet**;
- `P-08` remains `PENDING_PRODUCT_DECISION`.

---

# 7. Corpus execution-state wording conflicts with the synthetic pilot

The corpus index still says broadly:

> fixtures stay blocked  
> Gate 0 parents stay DERIVED_PARENT until at least one case has a source package  
> scorer predicates cannot be calibrated without seeds built on real parents.

But the execution program now intentionally permits:
- derived synthetic architecture fixtures;
- hand-built, layer-appropriate `DERIVED_PARENT` artifacts for pilot calibration.

The realistic signer-corpus campaign is indeed blocked on source packages; the synthetic architecture pilot is not blocked for that reason.

## Required repair

Scope the corpus statements:

> realistic signer-corpus fixtures remain blocked on source packages.

Do not imply that the synthetic three-case architecture pilot or its derived Gate 0 parents require real source packages.

Calibration on derived parents supports only the derived-pilot claim, not realistic-corpus validity.

---

# 8. S1 experiment-local schema should expose canonical optional relationships or explicitly allow extension

The canonical S1 interface permits:

> candidate-level relationships the substrate states explicitly.

The local schema example does not contain such a field.

`S1-AUTH-01` now correctly says those relationships are allowed.

To avoid the typed schema rejecting a canonical output, either:

- add optional `relationships[]`; or
- state that additional canonical non-authority fields are allowed and only the named forbidden decision fields are prohibited.

This is not needed to change CASE-01/02/09 semantics, but it is required for schema/interface consistency.

---

# 9. Minor manifest cleanup

The architecture-escalation section repeats two nearly identical historical-explanation paragraphs:

> This separation exists because...

Remove the duplicate. Nonblocking, but this is now a frozen execution artifact and should be clean.

Also change:

> Gate 0 calibration is required for both families

to:

> Gate 0 calibration is required for every ACTIVE predicate/scorer used by the pilot.

There are not merely "both families."

---

# 10. What is accepted from the third pass

The following are now clean and should remain frozen unless directly affected by the repairs above:

- exact `must_not_fire` ids now replace family labels;
- aggregate seed count corrected;
- pending predicates explicitly excluded in principle;
- run-count language at the predicate header is separated from mode;
- architecture escalation is now case-local and adjudicative, not all-cases voting;
- manifest provenance corrected to `DERIVED_SYNTHETIC`;
- CASE-01 A/P expectation clarified;
- note-level NT-* calibration excluded from the STRUCTURE pilot;
- F-1 explicitly demoted from architecture defect;
- fixture date/provenance/pronoun fixes remain correct.

---

# 11. Readiness

## Architecture
CLOSED / CONVERGED.

## Gate 0
Near-ready, but **not executable yet** for this pilot until the active predicate/seed mapping is complete.

## AX-S1S2-D three-case pilot
Near-ready, but **not scoreable yet** until:
- active predicate set matches the three cases;
- every active predicate has calibration;
- pending-schema contradictions are resolved;
- 2/3 scoring is corrected.

## Doximity
Do not run yet.

## Phase 0
Do not touch.
