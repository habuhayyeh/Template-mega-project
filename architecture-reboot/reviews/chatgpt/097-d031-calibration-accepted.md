# ChatGPT review 097 — D-031 calibration rebuild ACCEPTED

## Verdict

> **ACCEPTED. D-031 is closed under D-019. Signer reference collection may restart from the current C3 packet set.**

Review target: DeepSeek implementation through commit `8e68a36`.

## Accepted contract state

- schema: `SCHEMA-4`
- registry: `PILOT-3`
- active set: `ACTIVE-PILOT-3`
- oracle: `ORACLE-4.0`
- campaign: `GATE0-C3`
- review policy: `REVIEW-POLICY-F-2`

D-030 is now represented and calibrated on both axes:

1. encounter role:
   - `PRIMARY`
   - `BACKGROUND`

2. causal relation:
   - relation noun/type;
   - `LIKELY | POSSIBLE | UNLIKELY` strength;
   - direction;
   - source support;
   - acting residual deficit/mechanism vs historical disease label.

## CASE-01

Accepted truth:

- falls = PRIMARY;
- prior L MCA infarct = BACKGROUND;
- compact A/P representation of the infarct remains allowed;
- no causal relation to falls is inferred from historical coexistence alone.

## CASE-10 positive causal calibration

Current source explicitly states that chronic right-sided weakness from prior stroke may contribute to
falls.

Clean S2 truth:

- O01 prior stroke: adoption=false;
- O02 chronic right-sided weakness: adoption=true, evidence=[S05];
- O03 falls: adoption=true, evidence=[S02];
- causal relation:
  - from O02;
  - to O03;
  - CONTRIBUTOR;
  - POSSIBLE;
  - support [S05].

The clean blinded packets are semantically coherent:

- S2-ADOPT-01: SILENT;
- S2-CAUSAL-01: SILENT.

The isolated semantic mutations are also coherent:

- G0-S2-09 substitutes O01 historical stroke for O02 residual weakness -> S2-CAUSAL-01 FIRED;
- G0-S2-10 changes POSSIBLE -> LIKELY despite source wording "may contribute" -> S2-CAUSAL-01 FIRED.

Both remain structurally valid; the intended failure is semantic, not mechanical.

## Mechanical/validation state

DeepSeek reports:

- 49 tests OK;
- preflight PASS 7/7;
- deterministic regeneration;
- 43 records;
- 49 semantic packet instances;
- 0 references;
- 0 evaluators;
- campaign INCOMPLETE;
- no FAIL records;
- no `oracle.expected` leakage.

The packet set at `runs/gate0-packets-c3-d031/` is the only current semantic calibration set.
All earlier packet sets/references are stale.

## Closure

The D-030/D-031 contract and calibration work is closed under D-019. Reopen only for new evidence:
a failing packet, contradictory signer judgment, evaluator disagreement, or implementation failure.

## NEXT

Restart signer/clinician reference collection from the current C3 F-2 packets in concise
clinician-readable form. Record each answer durably before proceeding.

After signer references are complete, obtain two eligible packet-only cross-family LLM evaluator
passes. Only then run Gate 0 acceptance aggregation.

No Doximity. No Phase 0.
