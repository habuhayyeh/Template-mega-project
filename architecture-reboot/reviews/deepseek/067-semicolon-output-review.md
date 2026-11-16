# DeepSeek review — semicolon protocol output

**Verdict:** closer, but still invalid. Do not feed to C.

The `;;` delimiter survived. The structure did not.

## 1. Two coverage categories are missing

Present:

- baseline_comparator_records
- neuro_history_records
- medication_context_records
- exam_records
- workup_records
- context_records

Missing:

- current_event_records
- action_bearing_records

That breaks the coverage contract and means event/action records are not discoverable by category.

Every `@@UNIT`/`@@ACTION` source ID must appear in coverage. With `current_event_records` missing, the
event units cite IDs that are not in the census.

## 2. `@@PROBLEM` is malformed

Current line:

```text
@@PROBLEM;;P001;;PRIMARY;;current recurrent seizure-like events on  brief staring spells when relaxed as
baseline comparator T016,T017;;NONE;;1
```

That is 6 fields, not 9.

It is missing:

- evidence
- counterevidence
- contains
- separate_from
- order

The label also absorbed the baseline comparator and `T016,T017`.

Expected shape:

```text
@@PROBLEM;;P001;;PRIMARY;;current recurrent seizure-like events;;T001,T004,T005,...;;NONE;;longstanding brief staring spells as baseline comparator;;NONE;;1
```

## 3. `AV003` upgrades “needed” to “ordered or recommended”

Source:

> EEG and MRI brain are needed.

Output:

> EEG and MRI brain ordered or recommended.

That is a state upgrade. Keep source-qualified wording:

> EEG and MRI brain needed for further evaluation.

## 4. What improved

- `;;` protocol survived.
- P002 is gone; baseline spells are comparator units under P001.
- Patient and family history are split.
- Supplements are split from levetiracetam.
- Workup states are split.
- Actions now include ship evaluation, treatment, EEG/MRI, CT status, continuation, disposition and
  counseling.

## 5. Required prompt fix

Add a hard pre-emission count check:

1. Exactly eight `@@COV` records, one per category, in the listed order.
2. `@@PROBLEM` has exactly nine fields; count them before emitting.
3. Every synthesis source ID appears in a coverage record.
4. Do not write “ordered/recommended” unless the cited source says it.

The parser should fail closed on this output. Do not hand-correct it silently; rerun after the prompt fix.

No C. No acceptance.
