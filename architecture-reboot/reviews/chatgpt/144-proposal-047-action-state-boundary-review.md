# Review 144 — Proposal 047 action-state boundary

## Verdict

**TECHNICALLY ACCEPTABLE, BUT REQUIRES SIGNER APPROVAL BEFORE IMPLEMENTATION.**

Proposal 047 resolves the two material interface concerns raised in the prior ChatGPT review.

## What is now correct

### 1. No semantic state bucket remains in A2

The proposal removes both:
- normalized `decision/execution/response/result` enums;
- the proposed `raw_state_phrases` bucket.

That is the correct response to the asserted-state failure. A2 preserves:
- exact source record;
- exact selector;
- source-local target/operation;
- exact `action_phrase`;
- explicit source-local metadata;
- unresolved action identity/wording ambiguity.

This avoids asking A2 to classify action state at all.

### 2. B1 does not get a repair loophole

The proposal explicitly limits packet access to dereference of A-cited records.

B1 may not:
- scan the packet for omitted actions;
- create an action absent from A2;
- silently split/merge A2 in a way that changes source-local action identity;
- rewrite A2 pointers;
- infer state from another record.

If A2 omitted or malformed an action, B1 emits `A_ACTION_GAP` rather than repairing it.

That preserves failure localization.

### 3. Action splitting remains in A2

This is correctly retained as source-local action identity, not state interpretation.

The proposal explicitly requires splitting:
- CT / labs / UA;
- EKG / urine;
- blood / urine / monitoring;
- separate Keppra action identities;
- safety counseling vs medication actions.

This addresses a separate A2 failure demonstrated in the asserted-state run.

### 4. B1 state output is evidence-bound

Every normalized state must cite:
- an A2 span;
- an exact phrase from that span's selector.

State may be absent.
Unresolved is explicit.
No episode may exist without at least one A2 span.

This is the cleanest currently proposed interpretation boundary.

## Remaining risk

B1 can still map a real phrase to the wrong state. Proposal 047 acknowledges this correctly.

Therefore B1 is not assumed safe merely because it cites a phrase. It must be empirically tested against the existing action oracle.

If B1 fails, the fallback is source-qualified wording + unresolved, not another semantic validator.

## Test sequence

The proposed order is correct:

1. A2 source-local action identity/splitting test;
2. B1 action-state interpretation test;
3. only then A/B integration;
4. no C/render until those hold.

## Governance classification

This proposal is **ARCHITECTURAL / CONTRACT** rather than a bounded implementation correction because it moves normalized action-state responsibility from A2 to B1.

AGENTS.md explicitly requires signer escalation when:
- responsibility is reallocated between modules/stages.

Therefore ChatGPT should not implement Proposal 047 without signer approval even though the technical direction is coherent.

## Recommendation to signer

**Approve Proposal 047.**

Rationale:
- repeated A-level state normalization failed under both slot and asserted-state representations;
- the proposal removes the failing semantic decision from ingestion rather than adding more instructions;
- it preserves clean ownership:
  - A2 = source-local action identity/wording;
  - B1 = action-state interpretation/reconciliation;
- it prevents B1 from silently repairing A2;
- it has an explicit failure fallback if B1 normalization also proves brittle.

No implementation until signer approval.
