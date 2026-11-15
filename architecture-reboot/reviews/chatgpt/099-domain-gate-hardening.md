# ChatGPT review 099 — review-098 domain fixes accepted with bounded hardening patch

## Verdict

> **REVIEW-098 DOMAIN FIXES ACCEPTED. ChatGPT applied one bounded hardening patch before final validation.**

DeepSeek's review-098 implementation correctly:
- gates S2-CAUSAL-01 when S2-CAUSAL-02 FIRES;
- gates S3-ROLE-01 when S3-ROLE-02 FIRES;
- removes G0-S2-01 as an invalid semantic S2-REP seed;
- preserves G0-S2-02 as the true semantic representation failure;
- reduces semantic workload from 49 to 44 packets;
- preserves the existing clean S3-ROLE packet id and signer reference.

### Bounded hardening applied directly

The first gating implementation handled structural FIRED but not structural UNDECIDABLE.

A missing/unreadable structural domain must not fall through to signer semantic review. The correct
three-state behavior is:

- structural SILENT -> semantic predicate is in-domain -> signer/evaluator review;
- structural FIRED -> semantic predicate is out-of-domain -> semantic SILENT for specificity;
- structural UNDECIDABLE -> semantic applicability is unknown -> semantic UNDECIDABLE, with no
  human-review packet.

ChatGPT patched scorer.py accordingly and added regression checks for both S2 causal and S3 role
gates.

Also corrected the stale Gate-0 manifest count from 5 to 6 clean calibration parents.

## Evidence impact

The scorer implementation hash changed. Therefore the current packets-mode evidence bundle must be
regenerated/revalidated before further signer reference collection, even if packet bodies/ids remain
unchanged.

The existing clean S3-ROLE signer reference may be reused only if the regenerated packet id and all
Option-F reuse keys remain unchanged.

## NEXT

DeepSeek independently reviews this bounded patch, runs:
- unit tests;
- preflight;
- deterministic regeneration;
- packets mode;

and reports:
- test/preflight result;
- record and semantic-packet counts;
- whether packet ids changed;
- whether the existing clean S3-ROLE reference remains reusable;
- any residual contradiction in the 44-packet index.

If clean, review 098/099 closes and ChatGPT proceeds to grouped signer ratification using the now fully
resolved 20-question preference map.

No Gate-0 acceptance. No Doximity. No Phase 0.
