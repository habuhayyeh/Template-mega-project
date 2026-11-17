# D-S / D-T tests â€” all inside Doximity

Use synthetic facts only. No PHI. Run each test three times in fresh conversations.

The point is exact repetition, not clinical quality.

---

# Test 1 â€” D-S routing

## Prompt

```text
You are a deterministic section router. Do not rewrite text. Do not add facts.

Input JSON:

{
  "problems": [
    {"id": "P001", "role": "PRIMARY", "label": "seizure-like events"}
  ],
  "units": [
    {"id": "CU001", "type": "current_event", "label": "Thursday cluster", "problem": "P001"},
    {"id": "CU002", "type": "exam", "label": "no focal deficit", "problem": "nonproblem"}
  ],
  "actions": []
}

Route by these fixed rules:
- current_event -> HPI
- exam -> Exam
- PRIMARY problem -> Assessment
- actions -> Plan

Return only this JSON shape, with IDs in input order:

{"sections":{"HPI":[],"Exam":[],"Assessment":[],"Plan":[]}}
```

## Expected

```json
{"sections":{"HPI":["CU001"],"Exam":["CU002"],"Assessment":["P001"],"Plan":[]}}
```

## Pass

Three identical outputs. Exact keys, order, and IDs. No prose.

---

# Test 2 â€” D-T transformation

## Prompt

```text
You are a deterministic sentence transformer. Use only the input fields and the template. Do not add facts.

Input JSON:

{"section":"HPI","chronology":"Thursday evening","label":"recurrent staring episodes"}

Template:

"{chronology}, the patient had {label}."

Return only the completed sentence.
```

## Expected

```text
Thursday evening, the patient had recurrent staring episodes.
```

## Pass

Three identical outputs. Exact sentence. No extra words.

---

# Test 3 â€” combined D-S + D-T

## Prompt

```text
You are a deterministic note assembler. Use only the input JSON and the fixed templates. Do not add facts.

Input JSON:

{
  "problems": [
    {"id": "P001", "role": "PRIMARY", "label": "seizure-like events"}
  ],
  "units": [
    {"id": "CU001", "type": "current_event", "chronology": "Thursday evening", "label": "recurrent staring episodes", "problem": "P001"},
    {"id": "CU002", "type": "exam", "label": "no focal deficit", "problem": "nonproblem"}
  ],
  "actions": []
}

Rules:
- current_event sentence template: "{chronology}, the patient had {label}."
- exam sentence: "{label}."
- PRIMARY problem: "{label}."
- no actions: "None."

Return only:

HPI: <sentence>
Exam: <sentence>
Assessment: <sentence>
Plan: <sentence>
```

## Expected

```text
HPI: Thursday evening, the patient had recurrent staring episodes.
Exam: no focal deficit.
Assessment: seizure-like events.
Plan: None.
```

## Pass

Three identical outputs. Exact text. No rephrasing.

---

# Test 4 â€” malformed input

## Prompt

```text
You are a deterministic section router. If the input is missing a required key, return only:

{"error":"INVALID_INPUT"}

Input JSON:

{"problems":[{"id":"P001","role":"PRIMARY"}],"units":[]}
```

## Expected

```json
{"error":"INVALID_INPUT"}
```

## Pass

Three identical error outputs. It must not invent the missing label.

---

# Results to record

For each test, record:

- run 1 output;
- run 2 output;
- run 3 output;
- exact match: yes/no;
- failure type: drift, extra prose, missing key, invented content.

Do not average. One drift means D-S/D-T are not deterministic inside Doximity.

