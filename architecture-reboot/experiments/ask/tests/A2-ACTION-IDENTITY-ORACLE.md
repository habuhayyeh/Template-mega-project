# A2 Source-Local Action Identity Oracle

**Status:** FIXED BEFORE A2 V2 OUTPUT  
**Purpose:** human-score the wording-only A2 experiment after D-049.  
**Not:** a runtime validator, production artifact, or B1 state test.

## Scoring

- PASS — materially preserved within A2's source-local boundary;
- FAIL — omitted, bundled, synthesized, misattributed, state-normalized, or cross-record grouped;
- N/A — pattern is not present in the frozen packet.

## Completion / boundary

1. Output completes with `@@END`.
2. Output contains ACTION_SPAN entries only.
3. No normalized `decision`, `execution`, `response`, or `result` fields appear.
4. No asserted-state or raw-state-phrase surrogate appears.
5. No cross-record action episode/grouping appears.
6. No problem role, section allocation, final-plan choice, or prose appears.

## Source fidelity

7. Every `source_record` exists.
8. Every selector is an exact contiguous substring of that record.
9. Every `action_phrase` is an exact contiguous substring of its selector.
10. Raw speaker/source labels are preserved.
11. No adjacent-turn context is used to invent setting, actor, provenance, time, or condition.
12. Local identity is absent unless explicit in the same record.

## Action splitting / coverage

13. The ED CT head, basic labs, and urinalysis actions are separate spans.
14. EKG and urine-testing actions are separate spans where they occur together.
15. Blood-testing, urine-testing, and monitoring actions are separate spans where they occur together.
16. Neurology consultation is preserved as its own action.
17. Admission/disposition discussion is preserved as its own action.
18. EEG and MRI actions are preserved separately.
19. Prior/reported levetiracetam administration is distinct from a current load/order/recommendation.
20. Current levetiracetam continuation is distinct from prior administration.
21. Levetiracetam discontinuation is distinct from other levetiracetam actions.
22. Seizure precautions are preserved as action content.
23. Driving/activity/water/heights counseling or restrictions are preserved as action content.
24. Safety action content is not duplicated into the non-action semantic lane solely to preserve it.

## Fatal failures

Any of these fails A2:
- normalized action state emitted in A2;
- fabricated source pointer/selector for a care-changing action;
- material action omitted;
- materially distinct actions bundled so B1 cannot interpret them separately;
- cross-record action episode invented.

## Interpretation

A2 holds only if source-local action identity and wording are preserved without normalized action state.

If A2 fails, do not run B1 on that output as if it were valid evidence. Localize and correct A2 first.
