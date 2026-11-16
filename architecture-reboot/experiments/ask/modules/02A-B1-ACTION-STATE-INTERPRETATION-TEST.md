# B1 TEST — ACTION-STATE INTERPRETATION

**Experimental condition:** B1-ACTION-STATE-V1  
**Purpose:** interpret action state from a frozen A2 source-local action handoff.

## Inputs

Provide both:

1. the `ACTION_SPANS` lane from the immediately preceding `A_SOURCE_LOCAL_INGESTION_V2_1` handoff (or an equivalent isolated `A2_ACTION_WORDING_V1` development handoff);
2. the same canonical `SCRIBE_EVIDENCE_V2_2` packet.

The immediately preceding A action lane is authoritative for which actions advance downstream. The Scribe packet is available only to dereference records already cited by those A action spans.

## Task

Interpret normalized action state and supported action-episode grouping from the frozen A action spans.

Do not discover, repair, replace, or silently split actions that A2 failed to preserve.

Do not decide problem identity, problem role, note section placement, final plan adoption, or prose.

## Dereference-only rule

For an A ACTION_SPAN, B1 may:
- read only that span's cited `source_record`;
- verify its `selector` and `action_phrase`;
- interpret action state from that cited source-local wording;
- group A action spans into an episode only when the A action spans themselves support the grouping.

B1 must not:
- scan uncited records for additional actions;
- create an action absent from A2;
- repair an omitted A2 action;
- silently split a bundled A action span into new actions;
- rewrite A2 source_record, selector, action_phrase, or source identity;
- infer a state from another record, expected workflow, clinical plausibility, or treatment intensity.

## Output

```text
@@HANDOFF B1_ACTION_STATE_V1

ACTION_EPISODE AE001
  spans=<one or more A ACTION_SPAN IDs>
  target=<normalized target>
  operation=<normalized operation>
  actor=<source-supported actor or unresolved>
  setting=<source-supported setting or unresolved>
  time=<source-supported time or unresolved>
  STATE field=<decision|execution|response|result> value=<allowed value> phrase=<exact phrase from cited A2 selector> span=<A action span ID>
  unresolved=<state or episode ambiguity>

A_ACTION_GAP G001
  issue=<A2 omitted, bundled, or malformed a material action visible while dereferencing a cited record>
  evidence=<cited record ID + exact visible phrase>

@@END
```

`STATE` may appear zero or more times.
`A_ACTION_GAP` may appear zero or more times.
Omit optional fields when unsupported.

## Allowed state values

```text
decision  = considered | planned | recommended | continue | discontinue | hold |
            not_indicated | deferred

execution = not_started | ordered | reported_performed | performed | held | resumed |
            stopped | canceled

response  = agrees | declines | undecided | prefers_alternative

result    = unavailable | pending | preliminary | final
```

## State grounding

Every STATE requires:
- one A action span;
- one exact phrase from that span's selector;
- a state value semantically entailed by that phrase in that cited record.

Use the **smallest exact source phrase that actually carries the state**. Do not cite neighboring target
text as the state evidence merely because it occurs in the same selector.

Exact phrase presence is necessary but not sufficient.

Do not infer:
- an order from a plan or recommendation;
- performance from an order;
- an execution state merely because an action is future or not yet documented;
- a result state merely because a test is planned or performed;
- objective performance from source-mediated reporting;
- execution from continuation wording;
- any state from ordinary clinical workflow when the cited wording does not establish it.

If a selector is governed by explicit plan language (for example a plan heading followed by several
actions), that supports `decision=planned` for those listed actions and **does not** support execution.

Bare action shorthand without a governing verb/state phrase does not establish planned/ordered/performed
state; leave state absent and mark unresolved when clinically material.

A service/specialty label followed by an intervention shorthand (for example `Service: medication dose` or
`Consultant: procedure`) is still bare shorthand unless the same cited selector contains an explicit state verb
such as plan, recommend, order, give/administer, perform, hold, stop, or discontinue. A colon label plus drug/dose
must **not** be normalized to `ordered` merely because it resembles an order.

A source/speaker label such as `P1`, `SPK0`, or `SPK1` is not an actor identity. Populate
`actor` only when the A span or its cited source text explicitly establishes the actor/service; otherwise
use `actor=unresolved`.

If the selector expresses a preference but the preference owner is ambiguous, do not convert it into
clinician recommendation or patient agreement/response. Keep the state unresolved.

If a normalized state cannot be safely determined:
- emit no STATE for that dimension;
- use `unresolved` when the ambiguity is clinically material.

## State dimensions remain separate

Keep decision, execution, response, and result distinct.

One supported dimension does not fill another.

## Episode grouping

Group multiple A action spans only when the A2-supported target, operation, setting, time, and source-local
relationship support one episode.

When grouping is not safely supported, **keep separate episodes** and mark the relationship unresolved.

Do not group first and then state that same-episode identity is unresolved.

Do not use uncited records to establish grouping.

## A_ACTION_GAP

If dereferencing an A2-cited record reveals that the A action span bundled or malformed materially distinct
actions, emit `A_ACTION_GAP`.

A span whose target/action phrase contains multiple distinct clinical actions (for example two distinct
tests joined by "and") is bundled. Do not selectively use that bundled span as evidence for only one child
action.

Do not repair or split the A2 handoff.

Do not scan other records looking for gaps.

## End checks

Before returning:

1. every ACTION_EPISODE cites at least one A action span;
2. every STATE cites an A action span and an exact phrase from its selector;
3. no unsupported state was added merely because a phrase exists;
4. decision/execution/response/result remain separate;
5. source-mediated performance remains source-mediated;
6. no action absent from A2 was created;
7. A2 defects are surfaced as A_ACTION_GAP rather than repaired;
8. no problem architecture, section allocation, final-plan adoption, or prose appears;
9. output ends with `@@END`.

Return the handoff only.
