# Real-packet long handoff test

This uses the frozen real-packet facts from synthesis run 2, reduced to routing fields. Seven stages, no loop.

Paste only the prompt block. Run three times.

---

BEGIN REAL-PACKET LONG HANDOFF TEST

You are one prompt with seven stages. Do not loop. Do not skip a stage. Each stage uses the previous stage
output.

FACTS:

{
  "problems": [
    {
      "id": "P001",
      "role": "PRIMARY",
      "label": "New recurrent seizure-like events on cruise",
      "order": 1
    }
  ],
  "units": [
    {
      "id": "CU001",
      "type": "current_event",
      "label": "Initial episode with chest tightness, throat-closing sensation followed by loss of tone, unresponsiveness, eyelid fluttering and abnormal eye movements with amnesia for event",
      "chronology": "Wednesday evening (cruise)",
      "problem": "P001",
      "order": 2
    },
    {
      "id": "CU002",
      "type": "current_event",
      "label": "Recurrent cluster the following evening with chest discomfort, throat-closing sensation, staring/unresponsiveness, eye deviation/rolling, eyelid fluttering and intermittent head movement lasting ~20-30 minutes with limited responsiveness between events",
      "chronology": "Thursday evening (following evening on cruise)",
      "problem": "P001",
      "order": 3
    },
    {
      "id": "CU003",
      "type": "baseline_comparator",
      "label": "Longstanding brief staring when relaxed, responsive to name/touch, not interrupting active conversation; neurology stated distinct from current events and not clearly seizures",
      "chronology": "Pre-cruise baseline, intermittent",
      "problem": "P001",
      "order": 4
    },
    {
      "id": "CU004",
      "type": "neuro_history",
      "label": "No prior history of seizures, 18-year-old with first-time events",
      "chronology": "NONE",
      "problem": "P001",
      "order": 5
    },
    {
      "id": "CU005",
      "type": "neuro_history",
      "label": "No known family history of seizures per mother",
      "chronology": "NONE",
      "problem": "P001",
      "order": 6
    },
    {
      "id": "CU006",
      "type": "medication_context",
      "label": "No prescribed antiseizure medication prior to current episode",
      "chronology": "Prior to cruise events",
      "problem": "P001",
      "order": 7
    },
    {
      "id": "CU007",
      "type": "medication_context",
      "label": "Longstanding multiple vitamins and supplements, exact regimen not fully reconciled",
      "chronology": "Ongoing prior to presentation",
      "problem": "nonproblem",
      "order": 8
    },
    {
      "id": "CU008",
      "type": "medication_context",
      "label": "Levetiracetam given on ship after recurrent cluster with no further events reported; neurology stated will be continued pending EEG and MRI reassessment",
      "chronology": "Starting Thursday on ship, continued at consultation",
      "problem": "P001",
      "order": 9
    },
    {
      "id": "CU009",
      "type": "exam",
      "label": "Alert and oriented to person, place and time, no focal neurologic deficit identified",
      "chronology": "2026-11-13 ED exam",
      "problem": "P001",
      "order": 10
    },
    {
      "id": "CU010",
      "type": "workup",
      "label": "Cruise ship testing including CBC, CMP, lactate, electrolytes and blood glucose reported without significant abnormality, with monitoring and release to cabin",
      "chronology": "On ship after initial episode",
      "problem": "P001",
      "order": 11
    },
    {
      "id": "CU011",
      "type": "workup",
      "label": "CT head completed but not yet reviewed by neurology and no radiology result in ED record",
      "chronology": "Completed prior to consultation, result pending at that time",
      "problem": "P001",
      "order": 12
    },
    {
      "id": "CU012",
      "type": "workup",
      "label": "EEG and MRI brain needed to further evaluate events per neurology",
      "chronology": "At neurology consultation",
      "problem": "P001",
      "order": 13
    },
    {
      "id": "CU013",
      "type": "reasoning",
      "label": "New events not clearly epileptic based on semiology, not a slam-dunk seizure; PNES/nonepileptic events suspected/considered but cannot be established from history alone, epileptic seizure remains under evaluation",
      "chronology": "At neurology consultation",
      "problem": "P001",
      "order": 14
    }
  ],
  "actions": [
    {
      "id": "AV001",
      "target": "neurology evaluation",
      "owner": "P001",
      "order": 15
    },
    {
      "id": "AV002",
      "target": "ship medical evaluation and testing",
      "owner": "P001",
      "order": 16
    },
    {
      "id": "AV003",
      "target": "levetiracetam treatment",
      "owner": "P001",
      "order": 17
    },
    {
      "id": "AV004",
      "target": "EEG and MRI brain",
      "owner": "P001",
      "order": 18
    },
    {
      "id": "AV005",
      "target": "levetiracetam continuation",
      "owner": "P001",
      "order": 19
    },
    {
      "id": "AV006",
      "target": "inpatient workup disposition",
      "owner": "P001",
      "order": 20
    },
    {
      "id": "AV007",
      "target": "safety and driving counseling",
      "owner": "P001",
      "order": 21
    }
  ],
  "unresolved": [
    {
      "id": "X001",
      "topic": "CT head result",
      "order": 22
    },
    {
      "id": "X002",
      "topic": "supplement regimen",
      "order": 23
    }
  ]
}

STAGE 1 — ROUTE

Route:
- current_event, baseline_comparator, context -> HPI
- medication_context -> Meds
- exam -> Exam
- workup -> Workup
- reasoning -> Assessment
- all problems -> Assessment
- actions -> Plan
- unresolved -> Plan

Sort each section by numeric `order`.

Output exactly:

S1_ROUTE={"sections":{"HPI":["<IDs>"],"Meds":["<IDs>"],"Exam":["<IDs>"],"Workup":["<IDs>"],"Assessment":["<IDs>"],"Plan":["<IDs>"]}}

The `sections` key is mandatory. Do not flatten it.

STAGE 2 — HPI

Render HPI IDs:
- current_event: "HPI: {chronology}, {label}."
- baseline_comparator: "HPI: Baseline: {label}."

Output exactly:

S2_HPI=<JSON array of lines>

STAGE 3 — MEDS AND EXAM

Render:
- medication_context: "Meds: {label}."
- exam: "Exam: {label}."

Output exactly:

S3_MEDS_EXAM={"meds":[...],"exam":[...]}

STAGE 4 — WORKUP

Render:
- workup: "Workup: {label}."

Output exactly:

S4_WORKUP=<JSON array of lines>

STAGE 5 — ASSESSMENT

Render:
- problem: "Assessment: {label}."
- reasoning: "Assessment: Reasoning: {label}."

Output exactly:

S5_ASSESSMENT=<JSON array of lines>

STAGE 6 — PLAN

Render:
- action: "Plan: {target}."
- unresolved: "Plan: Unresolved: {topic}."

Output exactly:

S6_PLAN=<JSON array of lines>

STAGE 7 — FINAL

Use S2_HPI, S3_MEDS_EXAM, S4_WORKUP, S5_ASSESSMENT and S6_PLAN. Do not reread FACTS.

Output exactly:

FINAL:
<one HPI line>
<one Meds line>
<one Exam line>
<one Workup line>
<one Assessment line>
<one Plan line>

FORMAT RULES:
- `FINAL:` alone on its line.
- one item per line.
- do not join lines with spaces.
- no blank lines between items.
- stop after the last line.

COUNT CHECK:
- S2_HPI: 3 lines.
- S3: 3 meds, 1 exam.
- S4: 3 lines.
- S5: 2 lines.
- S6: 9 lines.
- FINAL: 21 item lines.

END REAL-PACKET LONG HANDOFF TEST

---

# Expected — do not paste into Doximity

```text
S1_ROUTE={"sections":{"HPI":["CU001","CU002","CU003"],"Meds":["CU006","CU007","CU008"],"Exam":["CU009"],"Workup":["CU010","CU011","CU012"],"Assessment":["P001","CU013"],"Plan":["AV001","AV002","AV003","AV004","AV005","AV006","AV007","X001","X002"]}}
S2_HPI=["HPI: Wednesday evening (cruise), Initial episode with chest tightness, throat-closing sensation followed by loss of tone, unresponsiveness, eyelid fluttering and abnormal eye movements with amnesia for event.","HPI: Thursday evening (following evening on cruise), Recurrent cluster the following evening with chest discomfort, throat-closing sensation, staring/unresponsiveness, eye deviation/rolling, eyelid fluttering and intermittent head movement lasting ~20-30 minutes with limited responsiveness between events.","HPI: Baseline: Longstanding brief staring when relaxed, responsive to name/touch, not interrupting active conversation; neurology stated distinct from current events and not clearly seizures."]
S3_MEDS_EXAM={"meds":["Meds: No prescribed antiseizure medication prior to current episode.","Meds: Longstanding multiple vitamins and supplements, exact regimen not fully reconciled.","Meds: Levetiracetam given on ship after recurrent cluster with no further events reported; neurology stated will be continued pending EEG and MRI reassessment."],"exam":["Exam: Alert and oriented to person, place and time, no focal neurologic deficit identified."]}
S4_WORKUP=["Workup: Cruise ship testing including CBC, CMP, lactate, electrolytes and blood glucose reported without significant abnormality, with monitoring and release to cabin.","Workup: CT head completed but not yet reviewed by neurology and no radiology result in ED record.","Workup: EEG and MRI brain needed to further evaluate events per neurology."]
S5_ASSESSMENT=["Assessment: New recurrent seizure-like events on cruise.","Assessment: Reasoning: New events not clearly epileptic based on semiology, not a slam-dunk seizure; PNES/nonepileptic events suspected/considered but cannot be established from history alone, epileptic seizure remains under evaluation."]
S6_PLAN=["Plan: neurology evaluation.","Plan: ship medical evaluation and testing.","Plan: levetiracetam treatment.","Plan: EEG and MRI brain.","Plan: levetiracetam continuation.","Plan: inpatient workup disposition.","Plan: safety and driving counseling.","Plan: Unresolved: CT head result.","Plan: Unresolved: supplement regimen."]
FINAL:
HPI: Wednesday evening (cruise), Initial episode with chest tightness, throat-closing sensation followed by loss of tone, unresponsiveness, eyelid fluttering and abnormal eye movements with amnesia for event.
HPI: Thursday evening (following evening on cruise), Recurrent cluster the following evening with chest discomfort, throat-closing sensation, staring/unresponsiveness, eye deviation/rolling, eyelid fluttering and intermittent head movement lasting ~20-30 minutes with limited responsiveness between events.
HPI: Baseline: Longstanding brief staring when relaxed, responsive to name/touch, not interrupting active conversation; neurology stated distinct from current events and not clearly seizures.
Meds: No prescribed antiseizure medication prior to current episode.
Meds: Longstanding multiple vitamins and supplements, exact regimen not fully reconciled.
Meds: Levetiracetam given on ship after recurrent cluster with no further events reported; neurology stated will be continued pending EEG and MRI reassessment.
Exam: Alert and oriented to person, place and time, no focal neurologic deficit identified.
Workup: Cruise ship testing including CBC, CMP, lactate, electrolytes and blood glucose reported without significant abnormality, with monitoring and release to cabin.
Workup: CT head completed but not yet reviewed by neurology and no radiology result in ED record.
Workup: EEG and MRI brain needed to further evaluate events per neurology.
Assessment: New recurrent seizure-like events on cruise.
Assessment: Reasoning: New events not clearly epileptic based on semiology, not a slam-dunk seizure; PNES/nonepileptic events suspected/considered but cannot be established from history alone, epileptic seizure remains under evaluation.
Plan: neurology evaluation.
Plan: ship medical evaluation and testing.
Plan: levetiracetam treatment.
Plan: EEG and MRI brain.
Plan: levetiracetam continuation.
Plan: inpatient workup disposition.
Plan: safety and driving counseling.
Plan: Unresolved: CT head result.
Plan: Unresolved: supplement regimen.
```
