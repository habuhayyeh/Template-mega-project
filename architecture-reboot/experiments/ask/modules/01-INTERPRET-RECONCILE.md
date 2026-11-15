# FILE A — INTERPRET AND RECONCILE

**Experimental version:** A-INTERPRET-RECONCILE-V1.1

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
  setting=<source-supported setting>
  time_scope=<source-supported time/encounter episode>
  decision=<considered|planned|recommended|continue|discontinue|hold|not_indicated|deferred>@<record ID>[selector=<...>]
  execution=<not_started|ordered|reported_performed|performed|held|resumed|stopped|canceled>@<record ID>[selector=<...>]
  response=<agrees|declines|undecided|prefers_alternative>@<record ID>[selector=<...>]
  result=<unavailable|pending|preliminary|final>@<record ID>[selector=<...>]
  actor=<source-supported actor>
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

Speaker role may be assigned only from explicit identity evidence in the packet.
If an explicit mapping exists, preserve it exactly.
If no explicit mapping exists, keep the raw speaker label and write `role unmapped`.
Do not infer or broaden role from conversational context, surrounding turns, or clinical plausibility.

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

Absence of documentation is not negation.
Expressions such as `not on file`, `not documented`, or an empty chart field cannot support `polarity=negated`.
Preserve the source limitation in `unresolved` or as contextual evidence instead.

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

Keep clinically distinct referents separate even when their polarity matches.
Examples:
- patient seizure history and family seizure history;
- patient report and collateral report;
- diagnosis and management action.

Do not combine distinct referents merely to make a shorter unit.

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

### One ACTION object = one action episode or trajectory

Do not create one ACTION object for every mention of the same drug/test.

Also do not merge distinct action episodes merely because the target is the same.

Use this episode identity:

```text
target + operation + setting + time/encounter episode
```

Examples that must remain separate when supported:
- cruise Keppra administration;
- ED Keppra load decision;
- discontinuation/cancelation of that ED load;
- current longitudinal decision to continue Keppra.

### Field-specific state vocabularies

Keep action dimensions separate.

#### decision

Allowed values:

- `considered`
- `planned`
- `recommended`
- `continue`
- `discontinue`
- `hold`
- `not_indicated`
- `deferred`

#### execution

Allowed values:

- `not_started`
- `ordered`
- `reported_performed`
- `performed`
- `held`
- `resumed`
- `stopped`
- `canceled`

#### response

Allowed values:

- `agrees`
- `declines`
- `undecided`
- `prefers_alternative`

#### result

Allowed values:

- `unavailable`
- `pending`
- `preliminary`
- `final`

Unknown fields stay absent.
Do not populate missing fields with `unknown`, `none_stated`, or an inferred intermediate state.

### Hard invariants

A decision state can never substitute for an execution state.

Examples:
- `Plan: CT head` -> `decision=planned`; do not infer `ordered`.
- `started on a Keppra drip` from a source report -> `execution=reported_performed`; do not infer an order.
- `keep on Keppra for now` -> `decision=continue`; this must not hide inside a diagnosis unit.
- `discontinued Keppra load` -> `decision=discontinue` or `execution=canceled/stopped` only for that current load episode; it does not erase prior reported doses.

Never infer:

```text
recommended -> ordered -> performed -> resulted
```

or:

```text
discontinued -> previously administered
```

or:

```text
planned -> pending execution
```

A source may establish one field without establishing the others.

If an action record is only a question or consideration, preserve that state rather than upgrading it.

### Mixed assertion rule

When one source span contains both diagnostic reasoning and a management action:
- keep the diagnostic/assessment assertion in the DECISION_LEDGER;
- create a separate ACTION entry for the management action;
- do not hide the management decision inside `kind=diagnosis`.

Do not split every mixed sentence.
Split only when the action state is clinically meaningful downstream.

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

Split when polarity, time, attribution, assertion type, event identity, or referent materially differs.

Distinct patient-history and family-history questions are separate referents and must remain separate even when both are negative.

Do not globally atomize every sentence.

## Structural checks

Before returning:

1. every UNIT has all required fields;
2. every evidence reference exists in the Scribe packet;
3. multi-assertion records use selectors;
4. question records are not treated as answers;
5. historical scope is not promoted to current;
6. patient/collateral report is not promoted to objective finding;
7. action decision/execution/response/result remain separate and use only their field-specific allowed values;
8. one ACTION does not merge distinct settings/time episodes for the same target;
9. explicit speaker mappings are preserved exactly; unmapped speakers are not role-inferred;
10. `not on file` / undocumented status is never converted to a negative;
11. clinically distinct referents such as patient history vs family history remain separate;
12. clinically meaningful management actions are not hidden inside diagnosis units;
13. nonproblem note material is preserved when clinically relevant;
14. no candidate-problem, role, containment, section, plan-ownership, or prose decision appears;
15. output ends with `@@END`.

Return the handoff only.
