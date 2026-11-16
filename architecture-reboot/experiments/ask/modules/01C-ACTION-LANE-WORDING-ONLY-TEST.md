# A2-ONLY TEST — SOURCE-LOCAL ACTION WORDING

**Experimental condition:** A2-ACTION-WORDING-V1  
**Purpose:** isolate source-local action identity and wording preservation.

## Input

One complete canonical `SCRIBE_EVIDENCE_V2_2` packet only.

## Task

Emit every material source-local action assertion needed for downstream neurologic note construction.

Do not emit semantic/non-action spans.

A2 preserves action identity and wording only. It does not normalize action state.

## Output

```text
@@HANDOFF A2_ACTION_WORDING_V1

ACTION_SPAN A001
  source_record=<exact record ID>
  selector=<exact contiguous substring from that record>
  target=<source-local target>
  operation=<source-local action wording>
  action_phrase=<exact contiguous substring of selector expressing this action>
  speaker_source=<raw SPK/source label>
  local_identity=<only if explicitly established in this record>
  provenance=<explicit source-local nested provenance if stated>
  setting=<explicit source-local setting if stated>
  time=<explicit source-local time if stated>
  condition=<explicit source-local condition if stated>
  unresolved=<source-local action identity/wording ambiguity>

@@END
```

Use only supported fields.

## Inclusion

Include material source-local actions involving:
- diagnostic or workup actions;
- medication actions;
- consultations;
- admission/disposition actions;
- precautions;
- driving/activity/water/heights counseling or restrictions;
- other management actions relevant to neurologic interpretation or care.

## One span = one source-local action identity

If one source record contains multiple materially distinct actions, split them into separate ACTION_SPAN
entries.

Do not bundle distinct tests, procedures, medication actions, counseling actions, or disposition actions
merely because they occur in one sentence or one record.

Splitting is based on source-local action identity, not normalized state.

## No state normalization

Do not emit:
- `decision=`;
- `execution=`;
- `response=`;
- `result=`;
- `ASSERTED_STATE`;
- `raw_state_phrases=`;
- any equivalent normalized action-state field.

State-like words remain literal source wording inside `selector` and `action_phrase`.

Do not map source wording to a decision/execution/response/result category.

## Source fidelity

- `source_record` must be one exact record ID;
- `selector` must be an exact contiguous substring of that exact record;
- `action_phrase` must be an exact contiguous substring of `selector`;
- preserve raw speaker/source label;
- local identity only if explicitly established in that same record;
- provenance, setting, time, and condition only when explicit in that same record;
- do not use adjacent turns to fill a field.

## No reconciliation

Do not:
- group actions across records;
- infer one action episode across records;
- infer chronology across records;
- infer speaker identity across records;
- decide problems, roles, sections, or prose.

If a source-local action identity or wording is ambiguous, preserve the exact wording and use
`unresolved`.

Return the handoff only.
