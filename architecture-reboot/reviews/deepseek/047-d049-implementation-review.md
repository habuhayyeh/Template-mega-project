# DeepSeek review — D-049 A2/B1 implementation

**Reviewed:** active A V2, A2 wording-only test, B1 test, A2/B1 oracles, Proposal 047.
**Status:** peer review. No implementation.

## Verdict

The implementation matches D-049. It is clean enough to run the A2 wording-only test first, then B1 on the
frozen A2 output.

No blocker. Three caveats.

## 1. Active A V2 retains no normalized action state

Searched the active A contract:

- no `decision=`, `execution=`, `response=`, `result=` schema;
- no `ASSERTED_STATE`;
- no `raw_state_phrases`;
- only the prohibitions remain.

A2 now preserves selector, target, operation, action phrase and source-local wording. Correct.

## 2. A2 splitting rules are general enough

The rules cover:

- distinct tests/procedures;
- distinct medication actions;
- administration/loading/continuation/hold/discontinuation;
- safety/counseling actions;
- one source-local action identity per span.

The active A contract still uses target-packet examples (`Plan: CT...`). That is not a test-module
confound, but it is case-shaped. Use generic examples later if A overfits. Not a blocker.

## 3. B1 dereference-only is a contract, not a mechanical guarantee

B1 is told to read only cited records. That cannot be mechanically enforced inside Doximity. The oracle
can catch invented actions, but the boundary is behavioral.

The useful protections are:

- every episode must cite A2 spans;
- no action absent from A2;
- `A_ACTION_GAP` instead of repair;
- oracle scoring.

Do not call this deterministic isolation. It is constrained behavior plus audit.

One real limit: if A2 omits an entire record, B1 may never see it. That is an A2 coverage failure, caught
by the A2 oracle, not B1.

## 4. Oracles separate the failures cleanly

- A2 oracle: identity, splitting, source fidelity, no state normalization.
- B1 oracle: state interpretation, grounding, no invented actions, no repair.

They are case-specific operationalizations, not general proof. That is appropriate for this stage.

## 5. Signer’s final-writer constraint

The constraint is consistent with the current direction, but it changes C later:

- C must emit typed groups/units and canonical render operators, not free prose instructions;
- renderer must be a deterministic lexicalizer over the frozen blueprint;
- no late grouping, section reassignment, action interpretation, or clinical decision in render;
- do not add stages; strengthen contracts.

Do not change C now. Record it as the C/render design constraint after A/B pass.

## Next

1. Run A2 wording-only on the frozen packet.
2. Score A2 identity oracle.
3. If pass, freeze A2 and run B1.
4. Score B1 state oracle.
5. Only then unified A/B.

No C/render changes. No acceptance, production change or Phase 0.
