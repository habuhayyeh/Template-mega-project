# Proposal 047 — action-state boundary between A2 and B1

**Status:** PROPOSED interface contract. No implementation.
**Scope:** A2 source-local action spans; B1 action-state interpretation.

## Decision

A2 must not normalize action state.

A2 preserves source-local action identity and wording. B1 interprets action state, but only from A2
spans and the exact cited source text. B1 may not discover or repair actions A2 omitted.

## 1. A2 output schema — no normalized state enums

```text
ACTION_SPAN A001
  source_record=<exact Scribe record ID>
  selector=<exact contiguous substring of that record>
  target=<source-local target>
  operation=<source-local action wording>
  action_phrase=<exact substring of selector expressing the action>
  speaker_source=<raw SPK/source label>
  local_identity=<only if explicitly established in this record>
  provenance=<only if explicit in this record>
  setting=<only if explicit>
  time=<only if explicit>
  condition=<only if explicit>
  unresolved=<source-local ambiguity or gap>
```

No `decision=`, `execution=`, `response=`, `result=` fields.

No `raw_state_phrases` bucket.

### Why no `raw_state_phrases`

`selector` already preserves the full source wording, and `action_phrase` identifies which words express
the action. A separate state-phrase bucket would require A2 to decide which words are state words. That is
the same semantic selection that caused the failure.

If B1 needs the state wording, it reads the selector.

### Action splitting

A2 must split materially distinct source-local actions:

- CT vs labs vs UA;
- EKG vs urine;
- blood vs urine vs monitoring;
- Keppra prior administration vs current load vs continuation vs discontinuation;
- safety counseling vs medication action.

One span = one source-local action identity. Splitting is identity, not state interpretation.

## 2. B1 input contract

B1 receives:

1. the complete A handoff;
2. the canonical Scribe packet for **dereference of cited records only**.

B1 may:

- read the exact record cited by an A span;
- verify that the selector is present;
- interpret action state from `selector`/`action_phrase`;
- group A spans into action episodes;
- mark state unresolved.

B1 may not:

- scan the packet for a new action A2 omitted;
- create an action absent from A2;
- split or merge A2 spans in a way that changes source-local action identity;
- rewrite A2 `source_record`, `selector` or `action_phrase`;
- infer a state from clinical plausibility, management intensity, or another record.

If A2 omitted or malformed a material action, B1 emits:

```text
A_ACTION_GAP
  issue=<what is missing or malformed>
  evidence=<record ID + selector, if visible during dereference>
```

It does not repair the action.

This keeps failure localization: A owns action preservation; B1 owns interpretation.

## 3. B1 output schema — normalized state with evidence

```text
ACTION_EPISODE AE001
  spans=<A2 ACTION_SPAN IDs>
  target=<normalized target>
  operation=<normalized operation>
  actor=<source-supported actor or unresolved>
  setting=<source-supported setting or unresolved>
  time=<source-supported time or unresolved>
  STATE field=<decision|execution|response|result> value=<allowed value>
        phrase=<exact phrase from the cited span> span=<A2 span ID>
  unresolved=<state or episode ambiguity>
```

Rules:

- `STATE` may appear zero or more times.
- No empty state field.
- Every state must have an exact `phrase` and an A2 `span`.
- The phrase must be a substring of that span's `selector`.
- Absence of a state is no `STATE` line, not `unavailable`/`not_started`.
- B1 may group spans into one episode only when target/operation/setting/time support the grouping.
- B1 may not create an episode without at least one A2 span.

Allowed normalized values remain the ones already accepted:

```text
decision  = considered | planned | recommended | continue | discontinue | hold |
            not_indicated | deferred
execution = not_started | ordered | reported_performed | performed | held | resumed |
            stopped | canceled
response  = agrees | declines | undecided | prefers_alternative
result    = unavailable | pending | preliminary | final
```

## 4. Immutability rule

B1’s normalized state is an interpretation, not a source fact. It may not flow back into A.

If B1 cannot ground a state in an A2 phrase:

- omit the state;
- write `unresolved`;
- if the action itself is missing, write `A_ACTION_GAP`.

B1 may not use the packet to “fill in” a state A2 failed to preserve. The packet is for dereference, not
discovery.

## 5. Unresolved representation

A2:

```text
unresolved=<action identity or wording ambiguity>
```

No state field.

B1:

```text
unresolved=<state cannot be determined from the cited phrase>
```

or:

```text
A_ACTION_GAP
  issue=<A2 omitted or bundled a material action>
  evidence=<record/selector>
```

## 6. Test plan

### Test 1 — A2 source-local action identity

Run A2 alone on the frozen packet. Check:

- exact `source_record`;
- exact selector substring;
- no state enums;
- CT/labs/UA split;
- EKG/urine split;
- blood/urine/monitoring split;
- Keppra episodes separate;
- safety counseling present as action;
- no cross-record grouping;
- no semantic lane.

### Test 2 — B1 action-state interpretation

Use the frozen A2 output + packet for dereference. Check:

- every action episode cites A2 spans;
- no action absent from A2;
- every `STATE` phrase is in the cited selector;
- no state when the phrase does not entail it;
- plan != ordered;
- recommendation != ordered;
- reported performance != objective performance;
- continuation decision != execution;
- future test != pending result;
- ambiguous state = unresolved;
- A_ACTION_GAP for omissions.

### Test 3 — unified integration

Only after Tests 1 and 2 pass. Run A/B integration on the same packet; compare against the existing action
oracle. Do not build C/render from this test.

## 7. What this does not solve

B1 can still over-interpret. That is now visible at the interpretation layer, with phrase and span
evidence. If B1 also fails, the fallback is:

- preserve source wording;
- render source-qualified action language;
- mark state unresolved;
- do not add a same-model validator.

## 8. Deleted / rejected

- asserted-state enums in A2;
- `raw_state_phrases`;
- B1 packet discovery of omitted actions;
- B1 repair of A2;
- same-model action validator;
- state slots with empty fields.

No acceptance, production change or Phase 0.
