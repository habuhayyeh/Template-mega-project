# Mega D-S / D-T test — attached packet

This test has three parts. Run it three times in fresh conversations.

Attach the Scribe packet; do not paste it unless Part 0 fails.

---

# Part 0 — attachment check

## Prompt

```text
Read the attached Scribe packet. Return exactly one line:

ATTACHMENT_OK;;first_record=<first record ID>

If no packet is attached or readable, return exactly:

ATTACHMENT_NOT_READ
```

## Expected

```text
ATTACHMENT_OK;;first_record=T001
```

If this fails, stop. Paste the packet in the next attempt.

---

# Part A — mega D-S routing

## Prompt

```text
You are a deterministic section router. Do not rewrite text. Do not add facts.

Input JSON:

{
  "problems": [
    {"id": "P001", "role": "PRIMARY", "label": "seizure-like events", "order": 1},
    {"id": "P002", "role": "BACKGROUND", "label": "baseline staring spells", "order": 2},
    {"id": "P003", "role": "BACKGROUND", "label": "prior migraine", "order": 3}
  ],
  "units": [
    {"id": "CU001", "type": "current_event", "label": "Wednesday collapse", "problem": "P001", "order": 4},
    {"id": "CU002", "type": "current_event", "label": "Thursday cluster", "problem": "P001", "order": 5},
    {"id": "CU003", "type": "baseline_comparator", "label": "longstanding staring", "problem": "P002", "order": 6},
    {"id": "CU004", "type": "medication_context", "label": "levetiracetam", "problem": "P001", "order": 7},
    {"id": "CU005", "type": "medication_context", "label": "supplements", "problem": "P001", "order": 8},
    {"id": "CU006", "type": "exam", "label": "no focal deficit", "problem": "nonproblem", "order": 9},
    {"id": "CU007", "type": "workup", "label": "CT completed", "problem": "P001", "order": 10},
    {"id": "CU008", "type": "workup", "label": "EEG and MRI needed", "problem": "P001", "order": 11},
    {"id": "CU009", "type": "reasoning", "label": "PNES considered", "problem": "P001", "order": 12},
    {"id": "CU010", "type": "context", "label": "events on cruise", "problem": "P001", "order": 13}
  ],
  "actions": [
    {"id": "AV001", "target": "EEG and MRI", "owner": "P001", "unresolved": false, "order": 14},
    {"id": "AV002", "target": "continue levetiracetam", "owner": "P001", "unresolved": false, "order": 15},
    {"id": "AV003", "target": "inpatient workup", "owner": "P001", "unresolved": false, "order": 16},
    {"id": "AV004", "target": "driving counseling", "owner": "nonproblem", "unresolved": false, "order": 17}
  ],
  "unresolved": [
    {"id": "X001", "topic": "CT result", "order": 18},
    {"id": "X002", "topic": "supplement regimen", "order": 19}
  ]
}

Fixed routing:
- current_event -> HPI
- baseline_comparator -> HPI
- context -> HPI
- medication_context -> Meds
- exam -> Exam
- workup -> Workup
- reasoning -> Assessment
- PRIMARY and BACKGROUND problems -> Assessment
- actions -> Plan
- unresolved -> Plan

Sort each section by numeric `order` ascending.

Return only:

{"sections":{"HPI":[],"Meds":[],"Exam":[],"Workup":[],"Assessment":[],"Plan":[]}}
```

## Expected

```json
{"sections":{"HPI":["CU001","CU002","CU003","CU010"],"Meds":["CU004","CU005"],"Exam":["CU006"],"Workup":["CU007","CU008"],"Assessment":["P001","P002","P003","CU009"],"Plan":["AV001","AV002","AV003","AV004","X001","X002"]}}
```

---

# Part B — mega D-T transformation

## Prompt

```text
You are a deterministic note assembler. Use only the input fields and templates. Do not add facts.

Input JSON:

{
  "events": [
    {"chronology": "Wednesday evening", "label": "collapse with chest tightness"},
    {"chronology": "Thursday evening", "label": "recurrent staring cluster"}
  ],
  "baseline": [{"label": "longstanding brief staring"}],
  "context": [{"label": "events occurred on cruise"}],
  "medications": [{"label": "levetiracetam"}, {"label": "supplements"}],
  "exam": [{"label": "no focal deficit"}],
  "workup": [{"label": "CT completed"}, {"label": "EEG and MRI needed"}],
  "assessment": [
    {"label": "seizure-like events"},
    {"label": "baseline staring spells"},
    {"label": "prior migraine"}
  ],
  "reasoning": [{"label": "PNES considered"}],
  "actions": [
    {"label": "EEG and MRI"},
    {"label": "continue levetiracetam"},
    {"label": "inpatient workup"},
    {"label": "driving counseling"}
  ],
  "unresolved": [{"label": "CT result"}, {"label": "supplement regimen"}]
}

Templates, one output line each, in this exact order:

- each event: "HPI: {chronology}, {label}."
- each baseline: "HPI: Baseline: {label}."
- each context: "HPI: Context: {label}."
- each medication: "Meds: {label}."
- each exam: "Exam: {label}."
- each workup: "Workup: {label}."
- each assessment: "Assessment: {label}."
- each reasoning: "Assessment: Reasoning: {label}."
- each action: "Plan: {label}."
- each unresolved: "Plan: Unresolved: {label}."

Return only the output lines.
```

## Expected

```text
HPI: Wednesday evening, collapse with chest tightness.
HPI: Thursday evening, recurrent staring cluster.
HPI: Baseline: longstanding brief staring.
HPI: Context: events occurred on cruise.
Meds: levetiracetam.
Meds: supplements.
Exam: no focal deficit.
Workup: CT completed.
Workup: EEG and MRI needed.
Assessment: seizure-like events.
Assessment: baseline staring spells.
Assessment: prior migraine.
Assessment: Reasoning: PNES considered.
Plan: EEG and MRI.
Plan: continue levetiracetam.
Plan: inpatient workup.
Plan: driving counseling.
Plan: Unresolved: CT result.
Plan: Unresolved: supplement regimen.
```

---

# Pass criteria

Part 0: exact line.

Part A: exact JSON, three runs identical.

Part B: exact 19 lines, three runs identical.

Any drift, extra line, reorder, or prose fails that part.
