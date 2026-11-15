# FILE A — INTERPRET AND RECONCILE

**Experimental version:** A-INTERPRET-RECONCILE-V1

## Purpose

Transform one complete canonical `SCRIBE_EVIDENCE_V2_2` packet into a **sparse semantic decision ledger** that preserves what the sources actually support without building the problem list or writing the note.

This is the first semantic pass.

It must determine:
- what assertion is being made;
- about whom or what;
- when it applies;
- whether it is affirmed, negated, uncertain, historical, current, future, or unresolved;
- whether multiple records describe the same event/state, evolution, conflict, or independent material;
- whether an action was merely discussed, decided, executed, responded to, or resulted.

It must preserve source linkage so later files can dereference the Scribe packet directly.

## Input

One complete canonical `SCRIBE_EVIDENCE_V2_2` packet only.

Do not require:
- a pointer index;
- an atomic-fact corpus;
- a prior semantic handoff;
- a validator output.

## Output

Return up to three lanes:

```text
@@HANDOFF A_INTERPRET_RECONCILE_V1

DECISION_LEDGER

UNIT U001
  concept=<short non-problem label>
  evidence=<record ID>[selector=<minimal clause or field>; role=<support|counter|context|provenance|conflict>], ...
  kind=<statement|question|observation|result|diagnosis|action>
  attribution=<source/speaker chain or unmapped>
  time=<event/source time if established>; scope=<current_episode|current_encounter|longitudinal|historical|future|unknown>
  polarity=<affirmed|negated|unresolved>
  certainty=<possible|likely|suspected|unlikely|unstated>
  relation=<same_event|same_state|evolution|conflict|possible_overlap|independent|none>
  disposition=<carry_forward|nonproblem_section_material|exclude_nonassertion>
  unresolved=<material limitation if present>

ACTION_LANE

ACTION A001
  target=<short label>
  operation=<short action label>
  decision=<state>@<record ID>[selector=<...>]
  execution=<state>@<record ID>[selector=<...>]
  response=<state>@<record ID>[selector=<...>]
  result=<state>@<record ID>[selector=<...>]
  actor=<source-supported actor>
  time_scope=<...>
  condition=<source-supported condition>@<record ID>[selector=<...>]

UNRESOLVED_REGISTER

UNRESOLVED X001
  topic=<short label>
  evidence=<record IDs + selectors>
  issue=<precise source limitation or conflict>

@@END
```

Use only lanes that have entries.

Unknown ACTION fields stay absent. Do not fill them with guessed intermediate states.

## Required unit fields

Every UNIT must carry:

1. `concept`
2. `evidence`
3. `kind`
4. `attribution`
5. `time` and `scope`
6. `polarity`
7. `certainty`
8. `relation`
9. `disposition`
10. `unresolved` when a material limitation exists

## Evidence syntax

A record ID alone is insufficient when the record contains more than one assertion.

Use:

```text
<record ID>[selector=<minimal clause/field>; role=<role>]
```

The selector may be:
- a short exact phrase;
- a section field;
- a compact locator for the relevant clause.

Do not copy long source narrative.

The evidence role describes how the cited assertion participates:
- `support`
- `counter`
- `context`
- `provenance`
- `conflict`

## Semantic order of operations

For each source assertion:

### Step 1 — establish assertion type

Classify the relevant assertion as:
- statement;
- question;
- observation;
- result;
- diagnosis;
- action.

A question is never an answer.

### Step 2 — establish referent and event/state identity

Determine which person, event, disease, finding, test, medication, or action the assertion refers to.

Do not merge assertions merely because they share words.

### Step 3 — establish provenance and attribution

Preserve:
- direct speaker/source;
- nested provenance such as EMS/ship/family report;
- unmapped speaker identity when the packet does not establish it.

Do not infer that an unmapped `SPK#` is patient, family, clinician, or witness.

### Step 4 — establish time and scope

Separate:
- source date;
- event time;
- current encounter;
- current episode;
- longitudinal state;
- historical state;
- future/planned state.

Historical identity does not become current state merely because it is mentioned now.

### Step 5 — establish polarity and certainty

Preserve polarity separately from certainty.

`certainty` is only a source-supported epistemic qualifier:
- `possible`
- `likely`
- `suspected`
- `unlikely`
- `unstated`

Do not use provenance/status words such as `reported` or `documented` as certainty. Those belong in `attribution`.

Do not strengthen certainty.

### Step 6 — reconcile records

Only after Steps 1-5, determine whether records describe:
- the same event;
- the same state;
- evolution;
- conflict;
- possible overlap;
- independent material.

Repeated documentation does not automatically create a second event.

Different assertion types do not automatically conflict.

### Step 7 — assign carry-forward disposition

`disposition` is **not problem eligibility**.

Use:
- `carry_forward` for semantic material that later architecture may need;
- `nonproblem_section_material` for exam, medication-at-presentation, workup, history, or other note material that must survive even if it never becomes a neurologic problem;
- `exclude_nonassertion` only for greetings, conversational repair, empty acknowledgements, or material with no usable assertion.

Do not assign:
- problem candidate;
- PRIMARY;
- BACKGROUND;
- NOT_RENDERED;
- containment;
- note section.

Those belong downstream.

## Action lane

Action state is a typed lane inside A, not a separate pass.

For each clinically meaningful action, keep these dimensions separate when explicitly established:

- `target`
- `operation`
- `decision`
- `execution`
- `response`
- `result`
- `actor`
- `time_scope`
- `condition`

Never infer:

```text
recommended -> ordered -> performed -> resulted
```

or:

```text
discontinued -> previously administered
```

A source may establish one field without establishing the others.

If an action record is only a question or consideration, preserve that state rather than upgrading it.

## Unresolved register

Use UNRESOLVED only when a material source limitation remains after reconciliation, such as:
- conflicting timing;
- uncertain attribution;
- incompatible action states;
- unavailable result;
- unresolved referent;
- uncertain event identity.

Do not use UNRESOLVED to invent:
- a new differential;
- a diagnostic question not raised by source material;
- a management recommendation;
- a problem identity;
- a note placement decision.

## What A owns

A owns:
- assertion type;
- referent/event identity;
- provenance and attribution;
- source time vs fact time;
- temporal scope;
- polarity/negation scope;
- certainty;
- current vs historical;
- durable identity vs source-specific state;
- duplicate/evolution/conflict/independent reconciliation;
- source reasoning vs source fact;
- action decision/execution/response/result/actor/condition;
- unresolved source limitations;
- preservation of nonproblem evidence.

## What A must not decide

A must not decide:
- candidate-problem status;
- independent neurologic problem threshold;
- disease-centered vs syndrome-centered organization;
- PRIMARY/BACKGROUND;
- containment;
- causal/contributory problem relations;
- problem order;
- primary action holder;
- note section placement;
- note inclusion/exclusion;
- final plan ownership;
- note prose.

## Sparsity rule

Do not recreate the Scribe packet as a second corpus.

Create a UNIT only when semantic reconciliation or downstream preservation requires one.

Prefer one unit for the same supported event/state when multiple records are duplicates or corroboration.

Split when polarity, time, attribution, assertion type, or event identity materially differs.

Do not globally atomize every sentence.

## Structural checks

Before returning:

1. every UNIT has all required fields;
2. every evidence reference exists in the Scribe packet;
3. multi-assertion records use selectors;
4. question records are not treated as answers;
5. historical scope is not promoted to current;
6. patient/collateral report is not promoted to objective finding;
7. action decision/execution/response/result remain separate;
8. nonproblem note material is preserved when clinically relevant;
9. no candidate-problem, role, containment, section, plan-ownership, or prose decision appears;
10. output ends with `@@END`.

Return the handoff only.
