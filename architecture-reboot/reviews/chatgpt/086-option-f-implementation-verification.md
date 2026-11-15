# ChatGPT review 086 — Option F implementation verification

## Verdict

> **OPTION F APPROVED BY SIGNER. IMPLEMENTATION IS SOUND IN PRINCIPLE; THREE BOUNDED EVIDENCE-INTEGRITY FIXES APPLIED DIRECTLY.**

The signer explicitly confirmed approval of Option F for the Gate 0 harness.

## Workload correction

The previously stated "7 semantic packets" was not the actual harness workload.

Because Gate 0 requires FULL_SILENCE-WITHIN-LAYER, semantic predicates must also be judged on mechanical
S1/S2 seeds to prove that unrelated mutations do not make those semantic predicates fire.

Current semantic packet instances:

- S1: 1 clean + 5 seeds = 6 artifacts × 1 semantic predicate = **6**
- S2: 1 clean + 4 seeds = 5 artifacts × 2 semantic predicates = **10**

Total: **16 semantic packet instances**.

That is part of the specificity calibration, not merely overhead.

## Bounded fixes in 4cadef1

1. REFERENCE records must declare `authority: SIGNER_CLINICIAN`.
2. The two LLM evaluators must have distinct `session_id` values as well as distinct judge ids and model families.
3. `EVIDENCE.json` now writes top-level merged `references[]` and `evaluators[]`, making the prior evidence file directly reusable as `--baseline`.

Regression coverage was added for all three.

## Governance clarification

The signer explicitly ratified Option F. Separately, `.` / `sync` remains synchronization shorthand
only and does not by itself approve pending proposals.

## NEXT

DeepSeek independently reviews commit `4cadef1d07e0e6a839b4d7bcc301a3b8e0df01e5` and runs preflight.

If PASS:
1. close the Option F implementation layer under D-019;
2. run Gate 0 **packets mode only** for GATE0-C1;
3. produce an index of all 16 semantic packet instances grouped by artifact and predicate;
4. do not run acceptance and do not fabricate signer/evaluator evidence.

After that, the signer reference step can be performed as one compact batch, followed by two fresh
packet-only evaluator passes.
