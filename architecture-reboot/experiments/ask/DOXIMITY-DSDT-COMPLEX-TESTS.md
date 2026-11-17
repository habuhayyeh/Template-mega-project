# D-S / D-T complex tests â€” all inside Doximity

Synthetic facts only. No PHI. Run each test three times in fresh conversations.

Exact match is required. One drift fails the test.

---

# Test 5 â€” multi-section routing

## Prompt

```text
You are a deterministic section router. Do not rewrite text. Do not add facts.

Input JSON:

{
  "problems": [
    {"id": "P001", "role": "PRIMARY", "label": "seizure-like events"},
    {"id": "P002", "role": "BACKGROUND", "label": "baseline staring spells"}
  ],
  "units": [
    {"id": "CU001", "type": "current_event", "label": "Thursday cluster", "problem": "P001"},
    {"id": "CU002", "type": "baseline_comparator", "label": "longstanding staring", "problem": "P002"},
    {"id": "CU003", "type": "medication_context", "label": "levetiracetam", "problem": "P001"},
    {"id": "CU004", "type": "exam", "label": "no focal deficit", "problem": "nonproblem"},
    {"id": "CU005", "type": "workup", "label": "EEG pending", "problem": "P001"},
    {"id": "CU006", "type": "reasoning", "label": "PNES considered", "problem": "P001"}
  ],
  "actions": [
    {"id": "AV001", "target": "EEG and MRI", "owner": "P001", "unresolved": false},
    {"id": "AV002", "target": "driving counseling", "owner": "nonproblem", "unresolved": false}
  ],
  "unresolved": [
    {"id": "X001", "topic": "CT result"}
  ]
}

Fixed routing:
- current_event -> HPI
- baseline_comparator -> HPI
- medication_context -> Meds
- exam -> Exam
- workup -> Workup
- reasoning -> Assessment
- PRIMARY and BACKGROUND problems -> Assessment
- actions -> Plan
- unresolved -> Plan

Preserve input order within each section.

Return only:

{"sections":{"HPI":[],"Meds":[],"Exam":[],"Workup":[],"Assessment":[],"Plan":[]}}
```

## Expected

```json
{"sections":{"HPI":["CU001","CU002"],"Meds":["CU003"],"Exam":["CU004"],"Workup":["CU005"],"Assessment":["P001","P002","CU006"],"Plan":["AV001","AV002","X001"]}}
```

## Pass

Three identical outputs. Exact section keys and order.

---

# Test 6 â€” multi-line transformation

## Prompt

```text
You are a deterministic note assembler. Use only the input fields and templates. Do not add facts.

Input JSON:

{
  "sections": {
    "HPI": [{"chronology": "Thursday evening", "label": "recurrent staring episodes lasting 20-30 minutes"}],
    "Meds": [{"label": "levetiracetam 500 mg twice daily"}],
    "Exam": [{"label": "no focal neurologic deficit"}],
    "Workup": [{"label": "EEG and MRI pending"}],
    "Assessment": [{"label": "seizure-like events, etiology uncertain"}],
    "Plan": [{"label": "continue levetiracetam"}, {"label": "driving restriction"}]
  }
}

Templates:
- HPI: "{chronology}, the patient had {label}."
- Meds: "{label}."
- Exam: "{label}."
- Workup: "{label}."
- Assessment: "{label}."
- Plan: join all Plan labels with "; " and end with a period.

Return only these six lines, in this order:

HPI: <sentence>
Meds: <sentence>
Exam: <sentence>
Workup: <sentence>
Assessment: <sentence>
Plan: <sentence>
```

## Expected

```text
HPI: Thursday evening, the patient had recurrent staring episodes lasting 20-30 minutes.
Meds: levetiracetam 500 mg twice daily.
Exam: no focal neurologic deficit.
Workup: EEG and MRI pending.
Assessment: seizure-like events, etiology uncertain.
Plan: continue levetiracetam; driving restriction.
```

## Pass

Three identical outputs. Exact punctuation and semicolon join.

---

# Test 7 â€” extra keys and missing optional key

## Prompt

```text
You are a deterministic section router. Ignore unknown extra keys. Do not add facts.

Input JSON:

{
  "problems": [
    {"id": "P001", "role": "PRIMARY", "label": "seizure-like events", "extra": "ignore-me"}
  ],
  "units": [
    {"id": "CU001", "type": "exam", "label": "normal", "problem": "nonproblem"}
  ],
  "actions": []
}

Fixed routing:
- exam -> Exam
- PRIMARY problem -> Assessment
- actions -> Plan

Missing "unresolved" is allowed and routes nothing.

Return only:

{"sections":{"HPI":[],"Meds":[],"Exam":[],"Workup":[],"Assessment":[],"Plan":[]}}
```

## Expected

```json
{"sections":{"HPI":[],"Meds":[],"Exam":["CU001"],"Workup":[],"Assessment":["P001"],"Plan":[]}}
```

## Pass

Three identical outputs. Extra key ignored. No invented content.

---

# Test 8 â€” duplicate ID must fail

## Prompt

```text
You are a deterministic section router. If the input contains a duplicate ID, return only:

{"error":"DUPLICATE_ID"}

Input JSON:

{
  "problems": [{"id": "P001", "role": "PRIMARY", "label": "seizure-like events"}],
  "units": [
    {"id": "CU001", "type": "exam", "label": "normal", "problem": "nonproblem"},
    {"id": "CU001", "type": "exam", "label": "repeat", "problem": "nonproblem"}
  ],
  "actions": []
}
```

## Expected

```json
{"error":"DUPLICATE_ID"}
```

## Pass

Three identical error outputs. No routing.

---

# Record

For each test:

- run 1, run 2, run 3;
- exact match: yes/no;
- failure: drift, extra prose, missing section, wrong order, invented field, duplicate routed.

One drift means D-S/D-T are not deterministic for that case.

