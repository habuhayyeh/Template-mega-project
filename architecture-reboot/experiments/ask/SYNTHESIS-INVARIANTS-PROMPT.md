# Synthesis invariants prompt — real packet

This replaces the invalid free-synthesis test. It fixes structure and coverage. Labels may vary; the IDs,
types, source records, action set and unresolved set may not.

Use with the packet attached and the accepted coverage JSON pasted.

---

BEGIN SYNTHESIS INSTRUCTIONS

Read the attached packet and the frozen coverage JSON.

Return exactly one JSON object. No prose, no Markdown, no code fence, no `@@` records.

Shape:

{
  "problems": [],
  "units": [],
  "actions": [],
  "unresolved": []
}

FIXED PROBLEM

Create exactly one problem:

```json
{"id":"P001","role":"PRIMARY","label":"<short label for new recurrent seizure-like events>","evidence":["<IDs>"],"counterevidence":[],"contains":[],"separate_from":[],"order":1}
```

- No P002.
- Longstanding staring is a baseline comparator unit, not a problem.
- `contains` and `separate_from` must be `[]`.
- `counterevidence` must be `[]`. Diagnostic uncertainty belongs in a reasoning unit.

FIXED UNITS

Create exactly these units, in this order. Fill `label` and `chronology` from the packet; keep the IDs,
types, source records and problem handles exactly.

```json
[
  {"id":"CU001","type":"current_event","source_records":["T004","T005","T006","T007"],"problem":"P001","order":2},
  {"id":"CU002","type":"current_event","source_records":["T009","T010","T011","T012","T013","T014"],"problem":"P001","order":3},
  {"id":"CU003","type":"baseline_comparator","source_records":["T016","T017"],"problem":"P001","order":4},
  {"id":"CU004","type":"neuro_history","source_records":["T002","P1.002"],"problem":"P001","order":5},
  {"id":"CU005","type":"neuro_history","source_records":["T003"],"problem":"P001","order":6},
  {"id":"CU006","type":"medication_context","source_records":["P1.005"],"problem":"P001","order":7},
  {"id":"CU007","type":"medication_context","source_records":["T025"],"problem":"nonproblem","order":8},
  {"id":"CU008","type":"medication_context","source_records":["T015","T022"],"problem":"P001","order":9},
  {"id":"CU009","type":"exam","source_records":["P1.003"],"problem":"P001","order":10},
  {"id":"CU010","type":"workup","source_records":["T008","P1.004"],"problem":"P001","order":11},
  {"id":"CU011","type":"workup","source_records":["T021","P1.006"],"problem":"P001","order":12},
  {"id":"CU012","type":"workup","source_records":["T020"],"problem":"P001","order":13},
  {"id":"CU013","type":"reasoning","source_records":["T018","T019"],"problem":"P001","order":14}
]
```

Each unit needs `label` and `chronology` added. Use `NONE` for absent chronology.

FIXED ACTIONS

Create exactly these actions, in this order. One action per source record. Do not split T020 into EEG and MRI.

```json
[
  {"id":"AV001","source_records":["T001"],"target":"neurology evaluation","owner":"P001","unresolved":null,"order":15},
  {"id":"AV002","source_records":["T008"],"target":"ship medical evaluation and testing","owner":"P001","unresolved":null,"order":16},
  {"id":"AV003","source_records":["T015"],"target":"levetiracetam treatment","owner":"P001","unresolved":null,"order":17},
  {"id":"AV004","source_records":["T020"],"target":"EEG and MRI brain","owner":"P001","unresolved":null,"order":18},
  {"id":"AV005","source_records":["T022"],"target":"levetiracetam continuation","owner":"P001","unresolved":null,"order":19},
  {"id":"AV006","source_records":["T023"],"target":"inpatient workup disposition","owner":"P001","unresolved":null,"order":20},
  {"id":"AV007","source_records":["T024"],"target":"safety and driving counseling","owner":"P001","unresolved":null,"order":21}
]
```

Each action needs `wording` added, source-qualified. Do not use “ordered” or “recommended” unless the source
does.

FIXED UNRESOLVED

Create exactly these two:

```json
[
  {"id":"X001","source_records":["T021","P1.006"],"topic":"CT head result","issue":"<short issue>","order":22},
  {"id":"X002","source_records":["T025"],"topic":"supplement regimen","issue":"<short issue>","order":23}
]
```

Do not add unresolved for EEG/MRI, disposition or etiology; those are represented elsewhere.

RULES

- Labels may vary, but IDs, types, source_records, problem handles and order may not.
- Every source ID must appear in the coverage JSON.
- No coverage records.
- No note text.
- Exactly one JSON object.

FINAL CHECK

1. exactly one problem, P001, with empty contains/separate_from/counterevidence;
2. exactly 13 units, CU001–CU013, with the listed types and source records;
3. exactly 7 actions, AV001–AV007, one per listed source record;
4. exactly 2 unresolved, X001–X002;
5. unique order 1–23;
6. no prose, code fence, `@@`, `;;`, or Markdown table.

If the attached packet is unreadable, return only:

{"error":"NO_PACKET"}

END SYNTHESIS INSTRUCTIONS

BEGIN FROZEN COVERAGE

<paste the accepted coverage JSON here>

END FROZEN COVERAGE
