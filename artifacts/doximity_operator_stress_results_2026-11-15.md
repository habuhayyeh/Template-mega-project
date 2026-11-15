# Doximity operator stress-suite results — 2026-11-15

## Purpose

Adversarially test the typed-group + canonical-operator boundary with both valid and intentionally malformed inputs.

Synthetic engineering evidence only. No real patient data.

The suite contained 36 isolated trials and was executed in 3 fresh Doximity conversations under the same contract, for 108 total trial executions.

## Headline result

### Semantic/pass-fail boundary

- Valid trials: 21 per run × 3 = **63/63 rendered correctly**
- Invalid trials: 15 per run × 3 = **45/45 rejected**
- Total correct valid-vs-invalid behavior: **108/108**

No malformed trial was silently repaired into clinical prose.
No valid trial was incorrectly rejected.
No cross-trial content leakage was observed.

### Reproducibility

All valid rendered outputs were textually stable across the three fresh runs.

The only observed run-to-run variation was the **error label** on T34:

- run 1: `CONTRADICTORY_PAYLOAD`
- run 2: `INVALID_COVERAGE`
- run 3: `CONTRADICTORY_PAYLOAD`

Both labels were explicitly acceptable in the answer key because the malformed group is simultaneously contradictory and invalid as a COVERED relation.

## Exact answer-key comparison

The following trials rejected correctly but used a different error code than the preferred answer-key code in all three runs:

| Trial | Preferred key | Doximity | Interpretation |
|---|---|---|---|
| T2 | CONTRADICTORY_PAYLOAD | INVALID_COMPOSITION | Correct rejection; taxonomy overlap between wrong semantic target and invalid composition |
| T10 | UNSUPPORTED_TRANSFORMATION | MISSING_REQUIRED_FIELD | Correct rejection; attribution requirement can reasonably be framed as missing required input |
| T24 | INVALID_COVERAGE | CONTRADICTORY_PAYLOAD | Correct rejection; two different sodium values are both contradictory and invalid to collapse as COVERED |
| T32 | CLASS_MISMATCH | INVALID_COMPOSITION | Correct rejection; illegal object reuse across rhetorical roles is not cleanly represented by either code |

Thus:

- **108/108** correct behavioral decisions
- **63/63** valid renders correct
- **45/45** invalid inputs rejected
- **33/45** invalid cases used the preferred/accepted error taxonomy exactly
- **12/45** invalid cases used a different but semantically plausible error label
- only T34 showed run-to-run label variation, and the schema itself explicitly permitted both labels

## Trial classes successfully stress-tested

The renderer correctly handled or rejected:

- duration folding;
- provenance versus event-time separation;
- covered-duplicate suppression;
- invalid coverage;
- negation;
- double-negative preservation;
- speaker attribution;
- incomplete reasoning payloads;
- structured test-purpose rendering;
- simple plans;
- conditional plan composition;
- cross-problem composition;
- if/then and unless scope;
- historical versus current management;
- rhetorical class mismatch;
- problem-line rendering;
- cross-problem duplicate text;
- conflicting numeric values;
- exact ordering;
- duplicate ORDER entries;
- ambiguous anaphora;
- historical diagnosis attribution;
- current reasoning coexisting with historical diagnosis;
- unused condition leakage;
- object reuse across groups;
- semantic-role reuse;
- punctuation preserving conditional scope;
- contradictory histories;
- unassigned-object leakage.

## Most important bug discovered

The largest defect exposed by this suite is **error-code ontology overlap**, not rendering instability.

Several malformed cases satisfy more than one available error category.

Examples:

### T24

`sodium 128` and `sodium 131` placed in a COVERED relation.

This is both:

- contradictory payload, and
- invalid coverage.

The model consistently chose `CONTRADICTORY_PAYLOAD`, while the preferred key chose `INVALID_COVERAGE`.

### T34

`patient denies fever` and `ED note documents fever 38.5 C` placed in a COVERED relation.

Across three runs the model alternated between:

- `CONTRADICTORY_PAYLOAD`
- `INVALID_COVERAGE`

This is not evidence that the semantic boundary failed. The input genuinely satisfies both labels.

### T32

One object is reused across PLAN and REASONING groups.

The answer key calls this `CLASS_MISMATCH`; Doximity calls it `INVALID_COMPOSITION`.

A better schema would likely have a dedicated accounting error such as `OBJECT_REUSE` or `MULTIPLE_GROUP_MEMBERSHIP`.

## Architectural lesson

The system appears substantially more reliable when the final writer receives:

- explicit problem ownership;
- explicit rhetorical class;
- explicit group membership;
- explicit operator;
- explicit order;
- explicit failure behavior.

The stress suite did **not** reproduce the earlier semantic merge/split instability.

This supports the B+ architecture.

## Validation-design implication

Production should not depend on a nuanced free-form error taxonomy unless those categories are made mutually exclusive.

Preferred options, in order:

1. deterministic pre-render validation for structural errors where possible;
2. a small mutually exclusive failure taxonomy with explicit precedence;
3. or, if precise diagnosis is unnecessary in production, a generic fail-closed `CONTRACT_ERROR` plus a separate audit/diagnostic step.

The most important production property is:

> malformed input does not get silently repaired into plausible clinical prose.

This suite achieved that in 45/45 invalid executions.

## Recommended next step

Do not add more adversarial synthetic operators before integrating this evidence into P006.

Revise P006 so that:

- each group has an explicit canonical operator;
- operator payload requirements are explicit;
- structural invalidity is checked before rendering when feasible;
- malformed/under-specified groups fail closed;
- error-code precedence is either simplified or formalized.

Then test the canonical seizure case under the production-shaped package in 3 fresh Doximity conversations.
