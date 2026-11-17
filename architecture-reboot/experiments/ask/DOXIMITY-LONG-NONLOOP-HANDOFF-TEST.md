# Long non-loop handoff test

This is a long, one-prompt handoff test. It is not a loop. Seven distinct stages pass data forward.

Run once per fresh conversation. Compare every line.

---

BEGIN LONG NON-LOOP HANDOFF TEST

You are one prompt with seven stages. Do not loop. Do not skip a stage. Each stage must use the previous
stage output.

FACTS:

{
  "problems": [
    {
      "id": "P001",
      "role": "PRIMARY",
      "label": "new recurrent seizure-like events",
      "order": 1
    },
    {
      "id": "P002",
      "role": "BACKGROUND",
      "label": "baseline staring spells",
      "order": 2
    },
    {
      "id": "P003",
      "role": "BACKGROUND",
      "label": "prior migraine",
      "order": 3
    }
  ],
  "units": [
    {
      "id": "CU001",
      "type": "current_event",
      "label": "Wednesday collapse",
      "chronology": "Wednesday evening",
      "problem": "P001",
      "order": 4
    },
    {
      "id": "CU002",
      "type": "current_event",
      "label": "Thursday cluster",
      "chronology": "Thursday evening",
      "problem": "P001",
      "order": 5
    },
    {
      "id": "CU003",
      "type": "baseline_comparator",
      "label": "longstanding staring",
      "chronology": "prior to cruise",
      "problem": "P002",
      "order": 6
    },
    {
      "id": "CU004",
      "type": "neuro_history",
      "label": "no prior seizures",
      "chronology": "NONE",
      "problem": "P001",
      "order": 7
    },
    {
      "id": "CU005",
      "type": "neuro_history",
      "label": "no family history of seizures",
      "chronology": "NONE",
      "problem": "P001",
      "order": 8
    },
    {
      "id": "CU006",
      "type": "medication_context",
      "label": "no prior antiseizure medication",
      "chronology": "NONE",
      "problem": "P001",
      "order": 9
    },
    {
      "id": "CU007",
      "type": "medication_context",
      "label": "levetiracetam treatment on ship",
      "chronology": "Thursday",
      "problem": "P001",
      "order": 10
    },
    {
      "id": "CU008",
      "type": "medication_context",
      "label": "longstanding vitamins and supplements",
      "chronology": "ongoing",
      "problem": "nonproblem",
      "order": 11
    },
    {
      "id": "CU009",
      "type": "exam",
      "label": "no focal neurologic deficit",
      "chronology": "ED exam",
      "problem": "P001",
      "order": 12
    },
    {
      "id": "CU010",
      "type": "workup",
      "label": "cruise ship labs reported normal",
      "chronology": "cruise",
      "problem": "P001",
      "order": 13
    },
    {
      "id": "CU011",
      "type": "workup",
      "label": "CT head completed not reviewed",
      "chronology": "prior to consult",
      "problem": "P001",
      "order": 14
    },
    {
      "id": "CU012",
      "type": "workup",
      "label": "EEG and MRI needed",
      "chronology": "pending",
      "problem": "P001",
      "order": 15
    },
    {
      "id": "CU013",
      "type": "reasoning",
      "label": "PNES considered but not established",
      "chronology": "consult",
      "problem": "P001",
      "order": 16
    },
    {
      "id": "CU014",
      "type": "context",
      "label": "events occurred on cruise",
      "chronology": "cruise",
      "problem": "P001",
      "order": 17
    },
    {
      "id": "CU015",
      "type": "context",
      "label": "neurology consultation in ED",
      "chronology": "ED",
      "problem": "P001",
      "order": 18
    }
  ],
  "actions": [
    {
      "id": "AV001",
      "target": "neurology evaluation",
      "owner": "P001",
      "order": 19
    },
    {
      "id": "AV002",
      "target": "ship medical evaluation and testing",
      "owner": "P001",
      "order": 20
    },
    {
      "id": "AV003",
      "target": "levetiracetam treatment",
      "owner": "P001",
      "order": 21
    },
    {
      "id": "AV004",
      "target": "EEG and MRI brain",
      "owner": "P001",
      "order": 22
    },
    {
      "id": "AV005",
      "target": "levetiracetam continuation",
      "owner": "P001",
      "order": 23
    },
    {
      "id": "AV006",
      "target": "inpatient workup disposition",
      "owner": "P001",
      "order": 24
    },
    {
      "id": "AV007",
      "target": "safety and driving counseling",
      "owner": "P001",
      "order": 25
    }
  ],
  "unresolved": [
    {
      "id": "X001",
      "topic": "CT result",
      "order": 26
    },
    {
      "id": "X002",
      "topic": "supplement regimen",
      "order": 27
    },
    {
      "id": "X003",
      "topic": "event etiology",
      "order": 28
    },
    {
      "id": "X004",
      "topic": "disposition completion",
      "order": 29
    }
  ]
}

STAGE 1 — ROUTE

Route by fixed rules:
- current_event -> HPI
- baseline_comparator -> HPI
- context -> HPI
- medication_context -> Meds
- exam -> Exam
- workup -> Workup
- reasoning -> Assessment
- all problems -> Assessment
- actions -> Plan
- unresolved -> Plan

Sort each section by numeric `order` ascending.

Output exactly:

S1_ROUTE=<sections JSON>

STAGE 2 — HPI

Use S1_ROUTE HPI IDs. Render:
- current_event: "HPI: {chronology}, {label}."
- baseline_comparator: "HPI: Baseline: {label}."
- context: "HPI: Context: {label}."

Output exactly:

S2_HPI=<JSON array of lines>

STAGE 3 — MEDS AND EXAM

Use S1_ROUTE Meds and Exam IDs. Render:
- Meds: "Meds: {label}."
- Exam: "Exam: {label}."

Output exactly:

S3_MEDS_EXAM={"meds":[...],"exam":[...]}

STAGE 4 — WORKUP

Use S1_ROUTE Workup IDs. Render:
- "Workup: {label}."

Output exactly:

S4_WORKUP=<JSON array of lines>

STAGE 5 — ASSESSMENT

Use S1_ROUTE Assessment IDs. Render:
- problem: "Assessment: {label}."
- reasoning: "Assessment: Reasoning: {label}."

Output exactly:

S5_ASSESSMENT=<JSON array of lines>

STAGE 6 — PLAN

Use S1_ROUTE Plan IDs. Render:
- action: "Plan: {target}."
- unresolved: "Plan: Unresolved: {topic}."

Output exactly:

S6_PLAN=<JSON array of lines>

STAGE 7 — FINAL

Use S2_HPI, S3_MEDS_EXAM, S4_WORKUP, S5_ASSESSMENT and S6_PLAN. Do not reread FACTS.

Output exactly:

FINAL:
<HPI lines>
<Meds lines>
<Exam lines>
<Workup lines>
<Assessment lines>
<Plan lines>

Do not output anything else.

END LONG NON-LOOP HANDOFF TEST

---

# Expected — do not paste into Doximity

```text
S1_ROUTE={"sections":{"HPI":["CU001","CU002","CU003","CU014","CU015"],"Meds":["CU006","CU007","CU008"],"Exam":["CU009"],"Workup":["CU010","CU011","CU012"],"Assessment":["P001","P002","P003","CU013"],"Plan":["AV001","AV002","AV003","AV004","AV005","AV006","AV007","X001","X002","X003","X004"]}}
S2_HPI=["HPI: Wednesday evening, Wednesday collapse.","HPI: Thursday evening, Thursday cluster.","HPI: Baseline: longstanding staring.","HPI: Context: events occurred on cruise.","HPI: Context: neurology consultation in ED."]
S3_MEDS_EXAM={"meds":["Meds: no prior antiseizure medication.","Meds: levetiracetam treatment on ship.","Meds: longstanding vitamins and supplements."],"exam":["Exam: no focal neurologic deficit."]}
S4_WORKUP=["Workup: cruise ship labs reported normal.","Workup: CT head completed not reviewed.","Workup: EEG and MRI needed."]
S5_ASSESSMENT=["Assessment: new recurrent seizure-like events.","Assessment: baseline staring spells.","Assessment: prior migraine.","Assessment: Reasoning: PNES considered but not established."]
S6_PLAN=["Plan: neurology evaluation.","Plan: ship medical evaluation and testing.","Plan: levetiracetam treatment.","Plan: EEG and MRI brain.","Plan: levetiracetam continuation.","Plan: inpatient workup disposition.","Plan: safety and driving counseling.","Plan: Unresolved: CT result.","Plan: Unresolved: supplement regimen.","Plan: Unresolved: event etiology.","Plan: Unresolved: disposition completion."]
FINAL:
HPI: Wednesday evening, Wednesday collapse.
HPI: Thursday evening, Thursday cluster.
HPI: Baseline: longstanding staring.
HPI: Context: events occurred on cruise.
HPI: Context: neurology consultation in ED.
Meds: no prior antiseizure medication.
Meds: levetiracetam treatment on ship.
Meds: longstanding vitamins and supplements.
Exam: no focal neurologic deficit.
Workup: cruise ship labs reported normal.
Workup: CT head completed not reviewed.
Workup: EEG and MRI needed.
Assessment: new recurrent seizure-like events.
Assessment: baseline staring spells.
Assessment: prior migraine.
Assessment: Reasoning: PNES considered but not established.
Plan: neurology evaluation.
Plan: ship medical evaluation and testing.
Plan: levetiracetam treatment.
Plan: EEG and MRI brain.
Plan: levetiracetam continuation.
Plan: inpatient workup disposition.
Plan: safety and driving counseling.
Plan: Unresolved: CT result.
Plan: Unresolved: supplement regimen.
Plan: Unresolved: event etiology.
Plan: Unresolved: disposition completion.
```
