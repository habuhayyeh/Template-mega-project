# A2-ONLY TEST — ASSERTED-STATE SCHEMA

**Experimental condition:** A2-ASSERTED-STATE-V1  
**Purpose:** test whether state-with-evidence triples prevent action-slot schema completion.

## Input

One complete canonical `SCRIBE_EVIDENCE_V2_2` packet only.

## Task

Emit every material **source-local action assertion** needed for downstream neurologic note construction.

Do not emit semantic/non-action spans.

Do not:
- reconcile records;
- group action episodes across records;
- infer chronology across records;
- infer speaker identity;
- decide problems, roles, sections, or prose.

## Output

```text
@@HANDOFF A2_ASSERTED_STATE_V1

ACTION_SPAN A001
  source_record=<exact record ID>
  selector=<exact contiguous substring from that record>
  target=<source-local target>
  operation=<source-local action wording>
  action_phrase=<exact substring of selector expressing the action>
  speaker_source=<raw SPK/source label>
  local_identity=<only if explicitly established in this record>
  provenance=<explicit source-local nested provenance if stated>
  setting=<explicit source-local setting if stated>
  time=<explicit source-local time if stated>
  ASSERTED_STATE field=<decision|execution|response|result> value=<allowed value> phrase=<exact supporting substring of selector>
  condition=<explicit source-local condition if stated>
  unresolved=<source-local ambiguity/garble/limitation>

@@END
```

`ASSERTED_STATE` may appear zero or more times.

There are **no decision/execution/response/result slots** outside `ASSERTED_STATE`.

## Allowed state values

### decision
- considered
- planned
- recommended
- continue
- discontinue
- hold
- not_indicated
- deferred

### execution
- not_started
- ordered
- reported_performed
- performed
- held
- resumed
- stopped
- canceled

### response
- agrees
- declines
- undecided
- prefers_alternative

### result
- unavailable
- pending
- preliminary
- final

## Structural state rule

A state may be emitted **only** when an exact phrase inside the selector explicitly supports that state.

Every state requires:

```text
ASSERTED_STATE field=<field> value=<value> phrase=<exact supporting phrase>
```

Hard rules:
- `phrase` must be an exact contiguous substring of `selector`;
- no state value without a supporting phrase;
- no empty state fields;
- absence is represented by **no ASSERTED_STATE line**;
- do not use `unavailable` or `not_started` merely to fill absent state dimensions;
- plan does not imply ordered;
- recommended does not imply ordered;
- ordered does not imply performed;
- continue does not imply not_started;
- a future test does not automatically have result unavailable/pending;
- ambiguous state stays absent; use `unresolved` if needed.

Examples:

```text
selector=Plan: CT head, basic labs, urinalysis
action_phrase=Plan
ASSERTED_STATE field=decision value=planned phrase=Plan
```

No execution or result state is emitted unless separately stated in the same selector.

```text
selector=started on a Keppra drip
action_phrase=started on
ASSERTED_STATE field=execution value=reported_performed phrase=started on
```

No decision or result state is emitted.

## Action inclusion

Include material source-local assertions of:
- diagnostic/workup plans and actions;
- medication recommendations/orders/administration/continuation/hold/stop;
- consultations;
- admission/disposition decisions;
- safety precautions;
- driving/activity/water/heights counseling or restrictions;
- other management actions relevant to neurologic interpretation or care.

One action span = one source-local action assertion.

If one record contains materially distinct actions, split them.

## Source rules

- `source_record` must be one exact record ID;
- `selector` must be an exact contiguous substring of that record;
- `action_phrase` must be an exact contiguous substring of selector;
- no merged adjacent records;
- preserve raw speaker/source label;
- local identity only if this record explicitly establishes it.

Return the handoff only.
