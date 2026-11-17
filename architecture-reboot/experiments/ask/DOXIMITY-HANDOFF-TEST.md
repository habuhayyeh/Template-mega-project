# D-S → D-T handoff test — one prompt

This tests whether Doximity can pass a routed JSON from Stage A into Stage B inside the same prompt.

No packet is needed. Use the fixed facts below.

---

BEGIN HANDOFF TEST

You are one prompt with two stages. Do not skip Stage A. Do not reroute in Stage B.

FACTS:

{
  "problems": [
    {"id": "P001", "label": "new recurrent seizure-like events", "order": 1}
  ],
  "units": [
    {"id": "CU001", "type": "current_event", "label": "Wednesday collapse", "chronology": "Wednesday evening", "problem": "P001", "order": 2},
    {"id": "CU002", "type": "baseline_comparator", "label": "longstanding staring", "chronology": "baseline", "problem": "P001", "order": 3},
    {"id": "CU003", "type": "exam", "label": "no focal deficit", "problem": "P001", "order": 4}
  ],
  "actions": [
    {"id": "AV001", "target": "EEG and MRI", "owner": "P001", "unresolved": null, "order": 5}
  ],
  "unresolved": [
    {"id": "X001", "topic": "CT result", "issue": "no result", "order": 6}
  ]
}

STAGE A — ROUTE

Rules:
- current_event -> HPI
- baseline_comparator -> HPI
- exam -> Exam
- PRIMARY problem -> Assessment
- actions -> Plan
- unresolved -> Plan
- sort by numeric order ascending

Output exactly one line:

STAGE_A=<sections JSON>

STAGE B — TRANSFORM

Use only STAGE_A and FACTS. Do not change the route.

Templates, in this order:
- each HPI current_event: "HPI: {chronology}, {label}."
- each HPI baseline_comparator: "HPI: Baseline: {label}."
- each Exam: "Exam: {label}."
- each Assessment problem: "Assessment: {label}."
- each Plan action: "Plan: {target}."
- each Plan unresolved: "Plan: Unresolved: {topic}."

Output:

STAGE_B
<one line per item>

Do not output anything else.

END HANDOFF TEST

---

# Expected

```text
STAGE_A={"sections":{"HPI":["CU001","CU002"],"Meds":[],"Exam":["CU003"],"Workup":[],"Assessment":["P001"],"Plan":["AV001","X001"]}}
STAGE_B
HPI: Wednesday evening, Wednesday collapse.
HPI: Baseline: longstanding staring.
Exam: no focal deficit.
Assessment: new recurrent seizure-like events.
Plan: EEG and MRI.
Plan: Unresolved: CT result.
```

Run three times. Exact match all three = the handoff survived one prompt.
