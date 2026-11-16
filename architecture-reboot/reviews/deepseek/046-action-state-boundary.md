# DeepSeek architecture verdict — action-state normalization belongs in B1

**Question:** is typed action-state normalization too brittle for GPT-4o at A?
**Answer:** yes, at A. Move interpretation to B1; A preserves source-local action wording only.

## Why the asserted-state fix failed

The exact-phrase constraint proves only that the phrase exists. It does not prove the phrase entails the
state.

Observed:

- `Plan` -> `execution=ordered`;
- `need EEG` -> `execution=not_started`;
- `will keep on Keppra` -> `execution=reported_performed`;
- `Keppra load 1500` -> both `recommended` and `ordered`.

The model can attach a false state to a real phrase. No schema that asks A to choose an enum fixes that;
it only changes the form of the error.

## A should preserve, not normalize

A’s action lane should carry:

```text
ACTION_SPAN
  source_record=<exact ID>
  selector=<exact substring>
  target=<source-local target>
  operation=<source-local action wording>
  action_phrase=<exact substring expressing the action>
  raw_state_phrases=<zero or more exact source phrases>
  speaker_source=<raw label>
  local_identity=<only if explicit>
  setting=<explicit>
  time=<explicit>
  condition=<explicit>
  unresolved=<source-local ambiguity>
```

No `decision=`, `execution=`, `response=`, `result=` enums in A.

The model may quote “Plan”, “started on”, “will keep on”, “need”, “recommend”, “discontinue” as raw
phrases. It may not map them to state categories.

This removes the opportunity for A to promote state. It does not remove the need for state interpretation
later.

## B1 owns action-state interpretation

B1 receives A’s action spans + packet and decides:

- decision;
- execution;
- response;
- result;
- episode grouping;
- unresolved.

B1 must cite the A phrase and source record for every state. It may say `unresolved` when the phrase does
not entail a state.

This is the right layer: B1 is clinical synthesis, not ingestion.

## What this does not solve

B1 can still over-interpret. But now:

- the error is in the layer that owns interpretation;
- A cannot pre-commit a false state;
- failure localization is clean;
- the final note can fall back to source-qualified wording (“plan per ED note”) if B1 is uncertain.

If B1 also fails the action oracle, then typed action normalization is brittle for this model anywhere.
The fallback is to preserve source wording and mark state unresolved, not to add another validator.

## Action splitting stays in A

A must still split materially distinct actions:

- CT vs labs vs UA;
- EKG vs urine;
- blood vs urine vs monitoring.

That is source-local identity, not state interpretation. The run also failed this; fix it in A.

## Invalid control

Do not score the translated current-slot block. It was not an independent packet run. The asserted arm
alone is enough to reject asserted-state enums at A.

## Decision

- Do not adopt asserted-state enums in A.
- Remove all state enums from A2.
- Preserve raw action/state phrases.
- Move state interpretation to B1.
- Test B1 against the same action oracle.
- Keep A/B/C structure; no new stage.

No acceptance, production change or Phase 0.
