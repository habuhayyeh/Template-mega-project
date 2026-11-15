# 06 — ORACLE AUDIT OF THE DISPUTED OBJECTS

2026-11-14. No file modified. The disputed set is every object that differed from the oracle in either Doximity run, plus O55 and O58–O60, which both runs agreed on and the audit finds wrong.

Classes: **A** routable and oracle correct; **B** oracle should change; **C** unresolvable from the frozen representation.

| O# | Object | Oracle | Proposed | Class | Reason |
|---|---|---|---|---|---|
| O12 | apixaban held since admission | AP_ONLY | AP_ONLY | A | Encounter status change, contract 32. |
| O13 | no prior seizures | HPI | HPI | A | Decisive presenting negative, contract 18. |
| O16 | fluid restriction | AP_ONLY | AP_ONLY | A | Plan action. |
| O26 | no fever | EXAM | undecidable | C | `denies fever` is history; `afebrile` is exam. The object keeps neither. |
| O27 | no neck stiffness | EXAM | undecidable | C | Same. `denies` versus examined meningismus. |
| O28 | She wants to drive | HPI | SOCIAL | B | Functional baseline, not presentation chronology. Consistent with O41. |
| O32 | family's concern about her memory | ROS | NEURO_HISTORY | B | Family-reported. ROS is patient-reported by rule 20, so ROS never had a claim on it. |
| O34 | family's concern … is not today's issue | AP_ONLY | AP_ONLY | A | Clinician framing; the A/P ledger uses it as P2.EVIDENCE. |
| O36 | memory has been getting worse for a year | ROS | NEURO_HISTORY | B | Family-reported chronic concern, same as O32. |
| O40 | sometimes these turn out to be something we can't find a cause for | AP_ONLY | undecidable | C | Nothing in the object says the clinician said it. As patient speech it would be meaningless; as clinician speech it is framing. |
| O46 | fluid restriction started | AP_ONLY | AP_ONLY | A | Plan action. |
| O48 | mild word-finding difficulty at baseline per family | NEURO_HISTORY | NEURO_HISTORY | A | Reported baseline; the object says so in its own words. |
| O51 | MMSE 24 | WORKUP | WORKUP | A | Historical disease-specific study, contract 38. Carries its date. |
| O56 | 5 mm incidental right cavernous ICA aneurysm | NEURO_HISTORY | NEURO_HISTORY | A | A durable finding, not a result of this encounter. Provenance is 2024 radiology. |
| O57 | neurosurgery recommended follow-up imaging in two years | NEURO_HISTORY | NEURO_HISTORY | A | A prior recommendation is history. `06`'s AP_ONLY wording swallows it — that is a `06` defect, not an oracle defect. |
| O55 | apixaban started | MEDICATIONS | NEURO_HISTORY | B | A start date is not the active regimen. Not disputed by either run; same defect as O58–O60. |
| O58 | propranolol started for migraine | MEDICATIONS | NEURO_HISTORY | B | Stopped 2025-03, eight months before. Not the presenting regimen; contract 32's exception does not apply. |
| O59 | propranolol stopped because of fatigue | MEDICATIONS | NEURO_HISTORY | B | Same. |
| O60 | propranolol stopped 2025-03 | MEDICATIONS | NEURO_HISTORY | B | Same. |

Counts: 9 A, 7 B, 3 C.

## What this does to the previous verdict

Last round I called six differences unacceptable and attributed the rest to model instability. That was partly wrong. O32 was an oracle error — run 2's NEURO_HISTORY was better than the oracle, and the same holds for O28 and O36, which I had already excused as equivalents. The revised reading:

- Run 2 genuine errors: O34, O51, O56, O57 — four.
- Run 2 unresolvable: O40.
- Run 2 correct where the oracle was not: O28, O32, O36.

So the model was better than I scored it, and the oracle was worse. The instability claim survives only in weakened form: O34, O40 and O51 did move between runs, and those three are the residue.

## Unresolvable objects

O26, O27, O40. Three objects where the section depends on a property the substrate dropped. No prompt wording recovers it: `no fever` is the same string whether it was asked and denied or observed and recorded.

## Smallest metadata addition

One field, `mode`, on objects of kind `OBSERVATION`, `COURSE`, `MANAGEMENT`:

```text
patient_report | family_report | examined | test_result | prior_record | clinician_comment
```

- O26, O27: `examined` versus `patient_report` — decides EXAM versus HPI/ROS.
- O40: `clinician_comment` — removes it from the narrative entirely.
- O32, O36: `family_report` — fixes attribution wording and confirms NEURO_HISTORY over ROS.
- O56, O57: `prior_record` — makes the historical reading explicit without relying on the date string.

Speaker alone is not enough: O26/O27 need examined-versus-reported, which is not a speaker question. So the field is broader than speaker, and three objects require it.

## Recommendation

Both, in this order.

1. **Enrich the substrate** with `mode` for the three unresolvable objects — that is a v2 frozen table and a fresh oracle, and it is the only thing that fixes them.
2. **Revise the oracle** on the seven B entries. This does not need metadata and can be done now.
3. **One `06` clarification**: AP_ONLY covers recommendations made *in this encounter*; a prior clinician's recommendation is history. Nothing else — the audit found no other prompt defect.

`06` does not need another broad revision. It needs three objects it cannot read and one sentence it over-applies.
