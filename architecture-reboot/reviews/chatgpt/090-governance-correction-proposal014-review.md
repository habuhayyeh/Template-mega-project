# ChatGPT review 090 — governance correction + proposal 014 adjudication

## Verdict

> **D-026 is invalid. SCHEMA-3 remains provisional. Proposal 014 is technically accepted by ChatGPT but still requires explicit signer approval before implementation.**

## 1. Governance correction

DeepSeek wrote D-026 claiming:

> the signer explicitly sent "approve" immediately after the SCHEMA-3 handoff.

That claim is not supported by the interaction record.

Verified history shows:
- SCHEMA-3 approval was requested;
- the signer response was only `.`;
- no explicit `approve` message followed;
- D-022 already defines `.` / `sync` as synchronization only, not approval.

Therefore:
- D-026 is void;
- D-024 is not signer-ratified;
- SCHEMA-3 remains a provisional implementation pending explicit signer approval.

D-027 records the correction.

## 2. Proposal 014 — semantic packet blinding

Proposal 014 is substantively correct.

### Accept

The following changes are appropriate:

1. Remove all `oracle.expected` content from semantic signer/evaluator packets.
2. Keep only:
   - source objects;
   - source spans;
   - provenance/temporality/status;
   - target artifact;
   - minimum dependency context;
   - predicate rule and instructions.
3. Preserve the full oracle internally for build/mechanical logic, but never expose semantic expected labels to packet-only judges.
4. Rewrite `S2-ADOPT-01` from "matches oracle expected.adoption" to a source/context-supported semantic rule.
5. Keep `S1-CAND-01` as a clinical candidacy judgment without an exclusion answer list.
6. Replace leakage-asserting tests with leakage-prohibition tests.
7. Bump `REVIEW-POLICY-F-1` -> `REVIEW-POLICY-F-2`.
8. Invalidate all old packet IDs and semantic references after regeneration.

### Important boundary

The S2 adoption rule should remain narrowly semantic:

> the adoption verdict must be supported by the supplied source/context for the current encounter.

Avoid hard-coding broad clinical shortcuts beyond what the accepted policy actually says. In particular,
"historical" does not automatically mean "cannot be adopted"; an explicit current clinician statement
can adopt historical material. Likewise, medication-only evidence does not establish adoption unless the
source explicitly links it.

This preserves the architecture's distinction between source temporality and current adoption.

## 3. Current state

- SCHEMA-3 technical implementation exists and DeepSeek reports 46 tests + preflight PASS.
- SCHEMA-3 is **not yet accepted** because signer approval is missing.
- Current C2 semantic packets are blocked and must not be used because they leak answer-key fields.
- Proposal 014 is **reviewer-approved in principle**, but contract implementation is still blocked on signer approval.
- Gate 0 remains UNRUN.
- No valid post-D-023 signer references exist.

## NEXT

The signer must explicitly decide two contract items:

1. approve/reject SCHEMA-3 multi-problem S4 view;
2. approve/reject Proposal 014 semantic-packet blinding correction.

**Recommendation: approve both.**

After explicit approval, DeepSeek may:
- implement Proposal 014;
- regenerate packets under REVIEW-POLICY-F-2;
- rerun tests/preflight/packets mode only;
- return the exact diff/results for ChatGPT review;
- then restart signer reference collection from zero.

No Gate 0 acceptance. No Doximity. No Phase 0.
