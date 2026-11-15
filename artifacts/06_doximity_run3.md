# 06 — DOXIMITY RUN 3 (v2 substrate, EVIDENCE_MODE)

Payload: `step9/PASTE06_v2.txt` (5999 bytes, table byte-identical to `step9/frozen_objects_v2.txt`). Raw: `step9/raw06_doximity_v2.txt`.

## Mechanical — FAIL

`check_sections.py` exit 1, one failure:

```text
FAIL [5] malformed REUSE line:
REUSE: O43 → REASON_FOR_CONSULT, duplicate source addressing same event, secondary attribution
```

The reuse schema requires `distinct function: <text>`. The model wrote free text. Accounting, destinations, discard reasons and primary assignments are otherwise clean: 60/60, 1 reuse, no invented or missing IDs.

The validator originally crashed while printing this failure — the arrow character broke a cp1252 console and the traceback replaced the failure list. Fixed by forcing UTF-8 stdout in `check_sections.py`. The failure list is now readable; the checker still exits 1.

## Semantic — 9 differences, none acceptable

| O# | Doximity | Oracle | Note |
|---|---|---|---|
| O28 | ROS | AP_ONLY | A preference is not a symptom. Put in ROS, the bucket it least belongs to. |
| O32 | ROS | NEURO_HISTORY | Chronic concern already under neurologic care. Wrong in all three runs. |
| O41 | ROS | SOCIAL | Current driving practice is functional baseline. Regressed from SOCIAL in run 2. |
| O51 | NEURO_HISTORY | WORKUP | Regressed: caused by the `06` clause I added this round. |
| O55 | MEDICATIONS | NEURO_HISTORY | A start date is not the active regimen. |
| O57 | AP_ONLY | NEURO_HISTORY | Prior recommendation swallowed by AP_ONLY. Wrong in all three runs. |
| O58 | MEDICATIONS | NEURO_HISTORY | Stopped eight months before presentation. |
| O59 | MEDICATIONS | NEURO_HISTORY | Same. |
| O60 | MEDICATIONS | NEURO_HISTORY | Same. |

Reuse: `O8 → HPI` missing for the third run; replaced by an `O43 → REASON_FOR_CONSULT` line that is also malformed.

ROS ends with three objects, none of which is a review-of-systems symptom (preference, chronic concern, driving practice). This is the same catch-all behaviour that failed in run 1, on different objects.

## My own defect

The `EVIDENCE_MODE` section I added says a prior-record result belongs with its finding in `NEURO_HISTORY`. `SECTION_CONTRACT` rule 38 says historical disease-specific studies belong in `WORKUP`. These disagree, and O51 moved from `WORKUP` in run 2 to `NEURO_HISTORY` in run 3 immediately after the clause was added. The clause is wrong, not the model. It should be reverted or narrowed before any further run.

## Where the three runs stand

| Run | Unacceptable differences | Wrong in every run |
|---|---|---|
| 1 (v1) | 12 | O32, O57 |
| 2 (v1, seven clauses) | 6 | O32, O57 |
| 3 (v2, mode) | 9 | O32, O57 |

The count has not converged and the membership moves each time. Only two objects are stable failures; everything else drifts in and out. Run 3 also broke the output schema, which the previous two did not.

## Verdict

**FAIL.** Mechanically invalid, semantically worse than run 2, and one of the differences was caused by my own edit.

`06` should not be frozen for unattended use.

## Diagnosis

Model instability, not a missing boundary, with one self-inflicted contract contradiction. Each prompt revision moves the error set rather than shrinking it: run 2 fixed O12/O13/O16/O26/O27/O46/O48 and lost O41/O51; run 3 recovered O34/O40 and lost O32/O41/O51. A proposer that changes six objects in and out on each pass cannot be stabilised by more prose.

The schema failure is the stronger signal: the same model that routed 51 objects correctly could not follow a five-token output format it had followed twice before.

## Recommendation

Stop revising `06`. Two defensible paths, neither of which needs another prompt edit:

1. `07` proceeds against `step9/ORACLE_ledger_06_v2.txt`. `06` stays a reviewed proposer — a human pass per run, as it already requires.
2. The three closed-set decisions that recur (`REPORTED` → HPI vs history vs ROS; medication event vs active regimen; prior recommendation vs current plan) move into deterministic code, with the model handling only the residual. Larger build, but it removes the classes that never converge.

Not recommended: a fifth prompt revision. There is no evidence that wording is the constraint any more.
