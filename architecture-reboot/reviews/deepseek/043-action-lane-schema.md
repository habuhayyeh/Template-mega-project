# DeepSeek review — action-lane schema completion

**Reviewed:** review 142, unified A standalone run.
**Status:** peer architecture review. No implementation.

## Verdict

The failure is **schema completion inside A2**, not a missing prose rule.

The prompt already says unknown fields stay absent, do not fill a template, plan != ordered, ambiguous
state -> omit. GPT-4o fills the slots anyway. Repeating the rule will not fix it.

Do not redesign A yet. Isolate A2 and change its representation so unsupported states are structurally
impossible, not merely prohibited.

## What the run proves

- A completes at scale; no truncation;
- source-local coverage is materially better;
- cross-record reconciliation is gone;
- action lane still invents `execution=not_started`, `execution=ordered`, `result=unavailable`;
- A1 still carries action content (Keppra drip) that belongs in A2;
- safety counseling survives semantically but not as an action;
- one duplicate/wrong pointer needs packet lint.

The dominant fatal failure is action-state template filling.

## Why prose rules fail

The output schema offers four state slots:

```text
decision=
execution=
response=
result=
```

A model that sees empty slots tends to complete them. The instruction “leave absent” competes with the
schema’s implicit expectation. The model resolves that competition by filling.

This is a representation problem. More warnings will not reliably fix it.

## Structural fix

Replace optional state slots with **asserted-state triples**. Only emit a state when the source phrase
explicitly supports it.

```text
ACTION_SPAN A001
  source_record=P1.045
  selector=Plan: CT head, basic labs, urinalysis
  target=CT head
  operation=obtain
  action_phrase=Plan
  ASSERTED_STATE field=decision value=planned phrase=Plan
```

No `execution=`, `response=` or `result=` line exists unless the source says it.

Example:

```text
ACTION_SPAN A002
  source_record=P1.014
  selector=started on a Keppra drip
  target=levetiracetam
  operation=start/administer
  action_phrase=started on
  ASSERTED_STATE field=execution value=reported_performed phrase=started on
```

No decision slot. No result slot.

### Rules

- `ASSERTED_STATE` may appear zero or more times.
- Each state must have a `field`, `value`, and exact `phrase` from the selector.
- No empty state fields.
- No state value without a phrase.
- B1 builds the full action episode from asserted states.
- Absence is represented by no asserted-state line, not by `unavailable` or `not_started`.

This makes template filling structurally harder.

## A1/A2 lane boundary

A1 is non-action. If a semantic span contains an action assertion (e.g. “put her on a Keppra drip”):

- keep the action in A2;
- do not duplicate it in A1;
- if the same sentence also carries a non-action fact, split by semantic type.

Safety counseling/restriction is an action assertion and belongs in A2, even if it also has semantic
content.

## Experiment

Run two A2-only tests on the same frozen packet:

1. current A2 schema;
2. asserted-state A2 schema.

Compare only action-state oracle items.

- If both fail: representation still wrong; simplify further.
- If current fails and asserted-state passes: schema completion is confirmed; adopt asserted-state.
- If both pass in isolation but unified A fails: same-pass lane interference is confirmed; split runtime
  execution or isolate A2.

Do not change B/C.

## Mechanical lint

Add development checks:

- every `source_record` exists;
- every selector is an exact substring;
- every `ASSERTED_STATE.phrase` is a substring of the selector;
- no empty state fields;
- no state value without phrase;
- no action content in A1.

No semantic validator.

No acceptance, production change or Phase 0.
