# D-S â†’ D-T handoff test V2 â€” strict contract

This fixes the previous test.

Stage A must carry every value Stage B needs, plus a sentinel. Stage B may use **only** Stage A. It may not reread FACTS.

---

BEGIN HANDOFF TEST

You are one prompt with two stages.

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

STAGE A â€” ROUTE AND CARRY

Create one JSON object with a single key `items`, an array in ascending `order`.

Every item has:
- `id`
- `section`
- `order`
- `kind`
- `sentinel`: exactly `[A]`
- plus its payload:
  - problem: `label`
  - current_event: `label`, `chronology`
  - baseline_comparator: `label`, `chronology`
  - exam: `label`
  - action: `target`
  - unresolved: `topic`

Routing:
- current_event -> HPI
- baseline_comparator -> HPI
- exam -> Exam
- PRIMARY problem -> Assessment
- action -> Plan
- unresolved -> Plan

Output exactly one line:

STAGE_A=<items JSON>

STAGE B â€” TRANSFORM

Use only STAGE_A. Do not read FACTS. If a value is missing, output `HANDOFF_ERROR`; do not fill it from memory.

Templates:
- HPI current_event: "HPI: {chronology}, {label} {sentinel}."
- HPI baseline_comparator: "HPI: Baseline: {label} {sentinel}."
- Exam: "Exam: {label} {sentinel}."
- Assessment: "Assessment: {label} {sentinel}."
- Plan action: "Plan: {target} {sentinel}."
- Plan unresolved: "Plan: Unresolved: {topic} {sentinel}."

Output:

STAGE_B
<one line per item, in STAGE_A order>

Do not output anything else.

END HANDOFF TEST

---

# Expected Stage A

```json
{"items":[{"id":"P001","section":"Assessment","order":1,"kind":"problem","label":"new recurrent seizure-like events","sentinel":"[A]"},{"id":"CU001","section":"HPI","order":2,"kind":"current_event","label":"Wednesday collapse","chronology":"Wednesday evening","sentinel":"[A]"},{"id":"CU002","section":"HPI","order":3,"kind":"baseline_comparator","label":"longstanding staring","chronology":"baseline","sentinel":"[A]"},{"id":"CU003","section":"Exam","order":4,"kind":"exam","label":"no focal deficit","sentinel":"[A]"},{"id":"AV001","section":"Plan","order":5,"kind":"action","target":"EEG and MRI","sentinel":"[A]"},{"id":"X001","section":"Plan","order":6,"kind":"unresolved","topic":"CT result","sentinel":"[A]"}]}
```

# Expected Stage B

```text
Assessment: new recurrent seizure-like events [A].
HPI: Wednesday evening, Wednesday collapse [A].
HPI: Baseline: longstanding staring [A].
Exam: no focal deficit [A].
Plan: EEG and MRI [A].
Plan: Unresolved: CT result [A].
```

Run three times.

- Stage A shape differs: fail.
- Any Stage B line lacks `[A]`: Stage B reread FACTS; fail.
- Both exact all three: handoff passes.

