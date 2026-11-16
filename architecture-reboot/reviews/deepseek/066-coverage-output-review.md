# DeepSeek review — coverage/synthesis output

**Verdict:** clinically strong, structurally non-compliant. Do not feed this to C yet.

The run captures the story, but it violates the coverage and problem-architecture contract in several
places.

## 1. Formatting

`SOURCE_COVERAGE` is emitted as one long line, not a block with indented key=value fields. The synthesis
entries are also not indented.

If downstream parsing expects block labels and indented fields, this output is not parseable as specified.

## 2. P002 should not be a problem

The output creates:

```text
PROBLEM P002
  label=longstanding brief staring spells when relaxed
  encounter_role=baseline_comparator
  separate_from=P001
```

Baseline spells are comparator evidence under P001, not a separate problem. They have no independent
disease identity, separate assessment, or separate management.

Expected instead:

```text
PROBLEM P001
  contains=longstanding brief staring spells as baseline comparator
```

and `CU002 problem_relation=P001`.

## 3. Encounter-role values are incompatible

The output uses:

```text
encounter_role=presenting_problem
encounter_role=baseline_comparator
```

Those are not the downstream problem roles. Use:

```text
PRIMARY | BACKGROUND | unresolved
```

If you want a finer label, put it in `diagnostic_stance` or `label`, not `encounter_role`.

## 4. Action recoverability is incomplete

`action_bearing_records`:

```text
T015, T020, T022, T023, T024
```

Missing material action-bearing records:

- `T008` — ship medical evaluated, obtained blood testing, monitored, released;
- `T021` / `P1.006` — CT completed, result not available (if tests are actions).

`T015` is also listed under `workup_records`, although it is a treatment record.

Define whether diagnostic tests are `workup` only or also `action_bearing`. Right now the output is
inconsistent.

## 5. Overmerged units

### CU003

Combines:

- no prior patient seizures;
- no known family history.

These are different referents. Split them.

### CU004

Combines:

- levetiracetam treatment;
- longstanding vitamins/supplements.

Split medication contexts.

### CU006

Combines:

- ship labs reportedly normal;
- CT completed without available result;
- EEG/MRI still needed.

These are different workup states. Split them so C can place them correctly.

### CU001

Combines the Wednesday event and Thursday cluster. One unit with chronology may be acceptable, but if C
needs separate HPI event units, split. At minimum, state that the unit covers both events.

## 6. What is good

- Source IDs are record-level, no selectors.
- No copied source text.
- P001 stance is clinically faithful.
- Actions are source-qualified.
- No action-state enums.
- No final note prose.
- CT result availability is explicitly unresolved.

## 7. Fix the prompt, not just this output

Add:

1. problem threshold: baseline comparator stays under the primary problem;
2. `encounter_role=PRIMARY|BACKGROUND|unresolved`;
3. exact action-bearing definition, including diagnostic/therapeutic actions;
4. unit-splitting rules by referent and state;
5. block/indentation output rule with a parser-safe example.

Do not send this output to C. No acceptance or production change.
