# DeepSeek review — third semicolon output

**Verdict:** structurally invalid again. Do not parse or send to C.

## 1. Missing coverage categories

Only six `@@COV` records appear:

- baseline_comparator
- neuro_history
- medication_context
- exam
- workup
- context

Missing:

- current_event_records
- action_bearing_records

That alone fails the eight-category contract.

## 2. ID lists use the wrong separator

The output uses single `;` inside ID lists:

```text
@@COV;;baseline_comparator_records;;T016;T017
```

The field separator is `;;`. IDs must be comma-separated:

```text
@@COV;;baseline_comparator_records;;T016,T017
```

As written, `T016;T017` is one malformed ID, not two.

## 3. `@@PROBLEM` is truncated

```text
@@PROBLEM;;P001;;PRIMARY;;new recurrent seizure-like events on
```

That is five fields, not nine. It is missing evidence, counterevidence, contains, separate_from and order.
The label is also incomplete.

## 4. Regressions in unit splitting

- `CU004` merges patient no-prior-seizure history and family history again.
- `CU005` merges levetiracetam treatment and supplements again.
- `CU008` merges CT status and EEG/MRI needed again.

## 5. Action lane

`action_bearing_records` is missing entirely, so action recoverability is not auditable.

`AV004` “CT head completed” is a test/result status, not a management action.

## 6. What is good

- No pipes.
- Most records use `;;` fields.
- P002 is gone.
- Many units are source-qualified.

## 7. Root cause

This does not look like a small formatting miss. The prompt is doing too much in one generation:

- coverage census;
- problem architecture;
- units;
- actions;
- unresolved.

Coverage records and the problem line are being dropped/truncated while the model spends output on units
and actions.

## Recommendation

Split into two Ask calls:

1. **Coverage-only prompt**: emit exactly eight `@@COV` records. No synthesis. Validate with parser; retry
   if invalid.
2. **Synthesis-only prompt**: input packet + frozen coverage; emit problems/units/actions/unresolved; no
   coverage generation.

This removes the dual-task pressure and makes coverage recoverability enforceable.

If you insist on one call, add hard gates for:

- exactly 8 coverage records;
- comma-separated IDs;
- `;;` fields only;
- complete 9-field problem;
- no line-ending truncation.

The parser should fail closed. No C. No acceptance.
