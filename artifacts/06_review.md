# 06 — FIRST ACCEPTANCE RUN AND REVIEW

2026-11-14. One candidate. Not rerun.

- Input: `step8/PASTE06.txt`, byte-identical object lines to `step7/ORACLE_frozen_objects.txt` (60 objects, verified by comparison).
- Candidate: `step8/raw06_ledger.txt`, produced once from `06_SECTION_ROUTE.md` with no other context.
- Mechanical: `check_sections.py` PASS — 60 assignments, 1 reuse, accounting 60/60.
- Oracle: `step8/ORACLE_ledger_06.txt`, 6 reassignments, 1 added reuse. `check_sections.py` PASS.
- Validator was tested against a seeded bad ledger: duplicate primary, invented ID, illegal section, illegal discard reason, wrong structural route (×3), reuse of an unassigned object, duplicate reuse, wrong accounting — 10 of 10 fired.

## Corrections

| O# | Candidate | Oracle | Reason |
|---|---|---|---|
| O12 | `MEDICATIONS` | `AP_ONLY` | `apixaban held since admission` is this encounter's status change, not a home-regimen fact. Contract 32 puts the changed status in the A/P. In the medication list it prints a plan state as a medication. |
| O26 | `ROS` | `EXAM` | `no fever` is an assessed vital, not a patient report. Contract 20 defines ROS as patient-reported. |
| O27 | `ROS` | `EXAM` | `no neck stiffness` is an examined sign. Same reason as O26. |
| O28 | `ROS` | `HPI` | `She wants to drive` is a stated wish raised in the presenting conversation. It is neither a symptom nor a negative, so ROS has no claim on it. |
| O49 | `ROS` | `NEURO_HISTORY` | `progressive memory difficulty` is a prior neurology finding dated 2025-06, not a current patient report. ROS would strip the date and the attribution. |
| O57 | `AP_ONLY` | `NEURO_HISTORY` | The A/P oracle discards O56–O57 entirely. Routing the surveillance recommendation to `AP_ONLY` as well would delete the only record of it from the note. It belongs with the aneurysm in history. |
| O8 | — | `REUSE: O8 → HPI` | Contract 11 requires an identifying clause naming the disease framing the encounter. O7/O8 are the only source. Without the reuse, HPI cannot open correctly. |

## Accepted without change

- O41 `SOCIAL` and O28 `HPI` split: current practice is functional baseline; the wish is presenting context.
- O55, O58–O60 `MEDICATIONS`: `apixaban started` and the propranolol stop are medication-list facts; contract 32 explicitly allows a recently stopped drug.
- O48 `NEURO_HISTORY`: "at baseline per family" is a reported baseline, not an examined finding.
- O13 `HPI`: the decisive negative for a first-seizure presentation (contract 18).
- O40 `AP_ONLY`: clinician framing, contains no body-section fact.

## Consequence

ROS holds two objects (O32, O36) and HPI six (O1–O6, O13, O28, O43). `07` decides whether ROS survives at all under contract 24. The oracle is the acceptance target for any future `06` change; the raw candidate is kept unchanged beside it.
