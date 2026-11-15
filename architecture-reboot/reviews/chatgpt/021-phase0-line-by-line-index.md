# 021 — Phase 0 adversarial line-by-line review index

## Status

**PHASE 0 NOT FREEZEABLE. PHASE 1 BLOCKED.**

The signer requested a deeper review of each Phase 0 file individually, challenging substantive claims line by line rather than checking only requested edits.

Reviews:

1. `021a-build-lint-line-review.md`
2. `021b-audit-protocol-line-review.md`
3. `021c-acceptance-brief-line-review.md`
4. `021d-change-control-line-review.md`
5. `021e-fixture-register-line-review.md`
6. `021f-phase0-readme-line-review.md`

## Response protocol for DeepSeek

Do not patch the Phase 0 files first.

For every challenged row, respond:

```text
FILE / LINE(S)
POSITION: ACCEPT | REJECT | PARTIAL | NEEDS EVIDENCE
REASON:
FROZEN SUPPORT / HISTORICAL EVIDENCE:
CONSEQUENCE IF ACCEPTED:
```

A rejection without exact frozen support/evidence is not resolved.

If the review exposes a true defect in a frozen upstream design rather than Phase 0, label it **REOPEN UPSTREAM DESIGN** rather than quietly changing Phase 0.

## Highest-risk claims requiring explicit defense

### BUILD_LINT
- normative prose supposedly does not compile despite frozen PROSE_POLICY;
- contradiction detection assumes correctly shared DECISION_ID;
- applicability/conditional overlap absent;
- out-of-scope detection presented as mechanical without mechanism;
- test coverage reduced to presence of fixture/check pointer;
- no executable enforcement exists despite claims it runs every build.

### AUDIT
- post-hoc assertion creation after observing output;
- underdefined acceptance evidence packet;
- signer as first escalation for any unresolved review;
- reviewer independence defined only as "did not write artifact."

### ACCEPTANCE_BRIEF
- no version pinning;
- no severity/prerequisite authority;
- unratified examples risk becoming hidden policy;
- five-field limit only works if missing manifest/assertion authorities exist elsewhere.

### CHANGE_CONTROL
- unsafe patch classification by edit type;
- checker implementation vs acceptance-check specification conflated;
- semantic authority omitted;
- global invalidation after design change;
- no-retroactive-rescoring rule absent;
- root CHANGELOG authority ambiguous.

### FIXTURE_REGISTER
- observation vs inferred cause/guard conflated;
- severity and prerequisites absent;
- mechanical assertions declared before their schemas/tables exist;
- same-(section,problem) uniqueness may conflict with explicit reuse consensus;
- F-11 only covers S2 despite downstream selection failure possibility;
- noncanonical `MEASURED` validation mode;
- C12 lacks semantic operator adequacy;
- apixaban conditional-composition regression and explicit F5 reproducibility fixture missing;
- narrative structure will not scale to signer multi-case corpus.

### README
- missing implementation manifest/status ledger;
- paper BUILD control represented as active;
- lifecycle conflicts with frozen workflow;
- C14 prevention attributed to wrong control.

## Freeze rule

Phase 0 does not freeze by exhaustion of comments.

It freezes only when:
- every surviving control claim has an implementable mechanism or an explicit pending dependency;
- authority/state/version provenance is unambiguous;
- no Phase 0 assertion silently changes frozen runtime semantics;
- the control plane can actually support the signer’s multi-case Doximity experimental protocol.
