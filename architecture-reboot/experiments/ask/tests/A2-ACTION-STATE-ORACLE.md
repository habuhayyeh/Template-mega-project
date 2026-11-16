# SUPERSEDED BY D-049 — DO NOT RUN

The action-state-at-A experiment is closed. Normalized action state now belongs to B1. Retained only as historical experiment evidence.

# A2 Action-State Isolation Oracle

**Status:** FIXED BEFORE A2-ONLY OUTPUT  
**Purpose:** compare the current slot schema with the asserted-state schema.  
**Source:** operational subset of the frozen File A oracle + already accepted A action invariants.  
**Not:** a runtime validator, production artifact, or new clinical semantic policy.

## Scoring

Score each condition independently:
- PASS — preserved without unsupported state;
- FAIL — state invented, promoted, merged, omitted, or misattributed;
- N/A — source packet does not contain the tested pattern.

## Completion and boundary

1. Output completes with `@@END`.
2. Output contains action spans only; no semantic/non-action ledger.
3. No cross-record reconciliation or episode grouping appears.
4. No problem/role/section/prose decisions appear.

## Source fidelity

5. Every `source_record` exists.
6. Every selector is an exact contiguous substring of that record.
7. No selector merges adjacent records.
8. Raw speaker/source label is preserved; identity is not globally inferred.

## Action identity and coverage

9. Materially distinct actions in one record are split when their downstream action identity differs.
10. Keppra recommendation/load, prior/reported administration, current continuation, and discontinuation remain distinguishable where source-local records distinguish them.
11. ED CT/labs/UA plans survive.
12. EEG/MRI plans survive.
13. Neurology consult/admission actions survive.
14. Seizure precautions survive as actions.
15. Driving/activity/water/heights counseling or restrictions survive as actions.

## State fidelity

16. Plan does not become ordered.
17. Recommendation does not become ordered.
18. Ordered does not become performed.
19. Reported performance/administration remains reported rather than objective performance when source-mediated.
20. Future/planned tests do not acquire `not_started` merely because execution is unstated.
21. Future/planned tests do not acquire `unavailable` or `pending` result state merely because no result is stated.
22. Continue decision does not acquire `not_started`.
23. Admission recommendation does not acquire an execution state unless locally stated.
24. Decision, execution, response, and result remain distinct.
25. Unknown state dimensions are absent rather than schema-filled.
26. Discontinued/held status does not establish prior administration.
27. Actor/owner remains source-local and unresolved when not established.

## Asserted-state-only mechanical checks

For the asserted-state condition:

28. Every `action_phrase` is an exact substring of selector.
29. Every `ASSERTED_STATE` has field, allowed value, and phrase.
30. Every `ASSERTED_STATE.phrase` is an exact substring of selector.
31. No state value appears outside an `ASSERTED_STATE` line.
32. No empty state field or placeholder state line appears.

## Fatal failures

Any of these is fatal for the condition:
- material recommendation/plan upgraded to order/performance;
- material reported execution upgraded to objective performance;
- cross-record action episodes merged;
- source pointer/selector fabricated for a care-changing action;
- clinically material action omitted.

## Interpretation

- current FAIL + asserted PASS -> schema-completion hypothesis supported; asserted-state representation is the candidate A2 fix;
- both FAIL -> representation remains insufficient;
- both PASS in isolation + unified A FAIL -> lane interference becomes leading explanation.

Do not use this test to advance B/C.
