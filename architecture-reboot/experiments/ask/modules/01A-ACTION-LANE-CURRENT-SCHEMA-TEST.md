# A2-ONLY TEST — CURRENT SLOT SCHEMA

**Experimental condition:** A2-CURRENT-SLOT-V1  
**Purpose:** isolate the current action-lane representation from the semantic lane.

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
@@HANDOFF A2_CURRENT_SLOT_V1

ACTION_SPAN A001
  source_record=<exact record ID>
  selector=<exact contiguous substring from that record>
  target=<source-local target>
  operation=<source-local action wording>
  speaker_source=<raw SPK/source label>
  local_identity=<only if explicitly established in this record>
  provenance=<explicit source-local nested provenance if stated>
  setting=<explicit source-local setting if stated>
  time=<explicit source-local time if stated>
  decision=<considered|planned|recommended|continue|discontinue|hold|not_indicated|deferred>
  execution=<not_started|ordered|reported_performed|performed|held|resumed|stopped|canceled>
  response=<agrees|declines|undecided|prefers_alternative>
  result=<unavailable|pending|preliminary|final>
  condition=<explicit source-local condition if stated>
  unresolved=<source-local ambiguity/garble/limitation>

@@END
```

Use only supported fields. Unknown fields stay absent.

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

## State rules

Preserve only a state explicitly supported by the selector.

- plan does not imply ordered;
- recommended does not imply ordered;
- ordered does not imply performed;
- reported administration does not become objective performed;
- a future test does not automatically have execution=not_started;
- a future test does not automatically have result=unavailable or pending;
- continue does not imply execution=not_started;
- unknown fields remain absent;
- do not fill a template.

If exact state is ambiguous, omit the uncertain state field and explain in `unresolved`.

## Source rules

- `source_record` must be one exact record ID;
- `selector` must be an exact contiguous substring of that record;
- no merged adjacent records;
- preserve raw speaker/source label;
- local identity only if this record explicitly establishes it.

Return the handoff only.
