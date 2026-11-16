# B1 Action-State Interpretation Oracle

**Status:** FIXED BEFORE B1 OUTPUT  
**Purpose:** human-score B1 state interpretation under D-049 / Proposal 047.  
**Not:** a runtime validator or final-note test.

## Prerequisite

Use only after the A2 wording-only output has passed the A2 action-identity oracle.

## Scoring

- PASS — state/grouping is supported by the cited A2 span and exact phrase;
- FAIL — state/grouping is invented, upgraded, conflated, repaired, or misattributed;
- N/A — source pattern is not applicable.

## Boundary

1. Output completes with `@@END`.
2. Every ACTION_EPISODE cites one or more A2 spans.
3. No action absent from A2 is created.
4. B1 does not silently repair an A2 omission or bundled action.
5. A2 defects visible during dereference are surfaced as `A_ACTION_GAP`.
6. No problem architecture, section allocation, final-plan adoption, or prose appears.

## Evidence grounding

7. Every STATE cites an A2 span.
8. Every STATE phrase is an exact substring of the cited span's selector.
9. Exact phrase presence is not treated as sufficient semantic entailment.
10. Actor/setting/time are source-supported or unresolved.
11. B1 does not use uncited records to establish state or grouping.

## State fidelity

12. A plan is not upgraded to an order.
13. A recommendation is not upgraded to an order.
14. An order is not upgraded to performance.
15. A future/planned test does not acquire `execution=not_started` merely because execution is unstated.
16. A future/planned or performed test does not acquire `result=pending` or `result=unavailable` merely because no result is stated.
17. Continuation wording remains a decision and is not converted into execution.
18. Source-mediated administration/performance remains `reported_performed`, not objective `performed`.
19. Discontinuation/stop wording does not prove a prior dose was administered.
20. Decision, execution, response, and result remain distinct.
21. Ambiguous shorthand does not receive multiple incompatible state interpretations; unresolved is acceptable.

## Frozen-packet challenge patterns

22. The ED CT/labs/UA plan remains planned without an inferred order/execution/result state.
23. EEG/MRI future-workup wording does not gain unsupported execution/result state.
24. Current levetiracetam continuation does not gain unsupported execution state.
25. The ambiguous current levetiracetam-load shorthand is not simultaneously normalized as recommendation + order unless the cited wording independently supports both; unresolved is acceptable.
26. Prior/report-of-administration remains distinct from current load/continuation/discontinuation.
27. Seizure precautions/counseling preserve the performed-vs-recommended distinction supported by their own source wording.
28. Admission/disposition wording is not upgraded beyond what its cited phrase entails.

## Episode grouping

29. Prior medication administration is not grouped with a distinct current action merely because the target drug is the same.
30. Continuation, loading, hold/stop/discontinuation remain separate unless source-supported episode identity justifies grouping.
31. Unrelated tests are not grouped merely because they occur in one encounter.
32. Uncertain episode relationships remain separate or unresolved rather than forced.

## Fatal failures

Any of these is fatal:
- material plan/recommendation upgraded to order/performance;
- source-mediated execution upgraded to objective performance;
- action absent from A2 invented by B1;
- B1 repairs an A2 gap rather than surfacing it;
- distinct care-changing action episodes merged in a way that changes interpretation.

## Interpretation

If B1 passes:
- proceed to unified A/B integration testing;
- do not yet assume C/render is safe.

If B1 fails:
- do not add a same-model validator;
- preserve source-qualified action wording and unresolved state as the fallback;
- return the architecture failure to DeepSeek.
