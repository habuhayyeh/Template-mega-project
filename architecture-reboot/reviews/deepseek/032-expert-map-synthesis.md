# DeepSeek synthesis — two expert maps, adopted architecture

**Status:** architecture recommendation. No implementation.

## Verdict

Both experts converge on the missing piece: **section allocation / note blueprinting**. That is the
main correction to our previous four-pass proposal.

Adopt the **four-pass operational shape** from expert 2, with the **explicit action-state fields** and
**detailed edge cases** from expert 1:

```text
Scribe V2.2 packet
  -> A. Interpret and reconcile
       sparse decision ledger
       + action-state lane
       + unresolved register
  -> B. Problem architecture
       ordered problem map
       + containment
       + role
       + causal structure
       + action ownership
  -> C. Note compiler
       note blueprint
       -> render
  -> final note
```

No separate action pass, no separate renderer call, no validator pass.

## Why this synthesis

Expert 1 is right that action state is orthogonal and dangerous. He is wrong to make it a sequential
pass by default. A typed action lane inside A preserves the state machine without another handoff.

Expert 2 is right that action can be a lane and that the renderer should be operationally merged into
the compiler. He is wrong to put candidate-problem eligibility in A. Problem identity belongs to B.

Both are right that:

- F1 pointer index is not enough;
- a sparse semantic ledger is needed;
- section allocation must happen before prose;
- record IDs need selectors and roles;
- nonproblem content must not disappear;
- same-model validation is not a quality gate;
- the renderer may not reopen clinical decisions.

## Pass contracts

### A. Interpret and reconcile

**Purpose:** determine what the source actually supports, for whom, when, with what certainty, and in
what action state.

**Input:** canonical Scribe packet only.

**Output:** sparse decision ledger + action lane + unresolved register.

**Owns:**
- assertion type (statement, question, observation, result, diagnosis, action);
- referent and event identity;
- provenance and attribution;
- source date vs fact time;
- temporal scope;
- polarity and negation scope;
- certainty;
- current vs historical;
- disease identity vs state;
- current adoption vs outside/historical formulation;
- conflict vs evolution vs different assertion type;
- action decision, execution, response, result, owner, condition.

**Must not decide:**
- candidate problem threshold;
- PRIMARY/BACKGROUND;
- containment;
- problem order;
- section placement;
- final plan;
- note prose.

**Critical rule:** establish assertion type, referent and event identity **before** reconciling. A
question is not a negative. Repeated documentation is not a second event. A record with several
assertions needs a selector, not a whole-record citation.

**Failure modes:** atomic explosion; source-wide buckets; question-as-answer; stale status becoming
current; patient report becoming objective fact; outside-service diagnosis becoming Neurology adoption;
false conflict; action-state promotion.

### B. Problem architecture

**Purpose:** turn supported meaning into neurologic problem structure.

**Input:** A ledger + action lane + packet.

**Output:** ordered problem map.

**Owns:**
- candidate-problem threshold;
- independent problem identity;
- disease-centered vs syndrome-centered organizer;
- manifestation containment;
- distinct downstream disorder;
- multifactorial syndrome;
- PRIMARY/BACKGROUND;
- supported causal/contributory relations;
- problem order;
- primary action holder.

**Must not decide:** new source meaning; unresolved conflicts; action execution; section layout; note
wording.

**Failure modes:** every symptom becomes a problem; residual deficit gets its own block; historical
stroke becomes active; possible contributor becomes likely; competing differentials become separate
confirmed problems; non-neurologic contributor gets a neurologic block.

### C. Note compiler

**Purpose:** select and place source-supported content into a complete note blueprint before prose.

**Input:** A + B + packet.

**Output:** note blueprint.

**Owns:**
- reason for consult;
- HPI chronology;
- neurologic history;
- other PMH;
- medication-at-presentation;
- current exam;
- workup/result placement;
- A/P claim/evidence/reasoning/action composition;
- minimum-sufficient selection;
- legitimate cross-section reuse;
- shared-action ownership placement.

**Must not decide:** diagnosis certainty, causal relation, currentness, action state, problem
identity/classification.

**Failure modes:** HPI follows source order; entire chart copied into history; reasoning leaks into HPI;
pending test shown as result; medication changes rewrite presentation regimen; evidence duplicated
everywhere; counterevidence dropped; nonproblem content lost.

**Mandatory coverage:** C must include nonproblem content — exam, medications, history, workup — even
when it never became a problem. If A does not carry it, C must reread the packet.

### Render

**Purpose:** express the frozen blueprint in note style.

**Input:** note blueprint + packet for exact qualifiers.

**Output:** final note.

**Owns:** syntax, compression, grammar, headings, formatting, wording.

**Must not decide:** any clinical relationship or state. No new diagnosis, currentness, causality,
containment, role or action state.

**Failure modes:** paraphrase strengthens certainty; attribution lost; historical becomes current;
recommended becomes ordered; two action states compressed into one; evidence becomes interpretation.

Errors here are final-note corruption; there is no downstream recovery.

## Critical corrections to both experts

### 1. Candidate-problem eligibility belongs in B, not A

Expert 2 puts “candidate-problem eligibility” in A. That pre-empts S1/problem architecture. A can label
an assertion as a statement, observation, result, diagnosis, question or action. It should not decide
whether that assertion qualifies as a problem.

### 2. A must carry nonproblem evidence

If A only emits problem-relevant units, exam, medications, history and workup can disappear. A must
carry note-relevant units with a disposition (problem candidate, evidence/context, nonproblem section
material, exclude as nonassertion). B decides which become problems; C selects the rest.

### 3. Record IDs alone are insufficient

Use:

```text
record ID + selector + evidence role
```

because one record may contain several assertions. `P1.001` alone does not say which clause it supports.

### 4. No copied source narrative, but allow short labels and qualifiers

Handoffs should not duplicate the packet. Short semantic labels and exact qualifiers are allowed. The
renderer must be able to reread the canonical record for exact wording.

### 5. Action state is a lane, not a ladder

Keep separate fields:

```text
decision | execution | response | result | owner | condition | time
```

Do not infer:

```text
recommended -> ordered -> performed -> resulted
```

Unknown fields stay absent/NA.

### 6. Blueprint before prose

C must emit a `NOTE_BLUEPRINT` before rendering. The renderer receives the blueprint and may not reopen
its decisions.

### 7. No same-model audit

Use structural invariants at handoffs, not a separate PASS/FAIL validator:

- historical scope cannot render as current without a current unit;
- ordered cannot render as performed;
- performed cannot render as resulted;
- BACKGROUND cannot render as PRIMARY;
- contained manifestation cannot become an independent problem.

## Adopted handoff shapes

### A. Decision ledger + action lane

```text
UNIT U01
  concept=<short label>
  evidence=<record ID>[selector=<field>; role=<role>], ...
  kind=<statement|question|observation|result|diagnosis|action>
  attribution=<source/speaker chain>
  time=<event time>; scope=<current_episode|current_encounter|longitudinal|historical|future|unknown>
  polarity=<affirmed|negated|unresolved>
  certainty=<source-supported qualification|unstated>
  relation=<same event|possible overlap|evolution|conflict|independent>
  disposition=<problem candidate|evidence/context|nonproblem section material|exclude>
  unresolved=<material limitation, if any>

ACTION A01
  target=<label>; operation=<...>
  decision=<state>@<record ID>
  execution=<state>@<record ID>
  response=<state>@<record ID>
  result=<state>@<record ID>
  actor=<...>; time_scope=<...>; condition=<...>@<record ID>
```

### B. Problem map

```text
PROBLEM P01
  label=<minimal source-supported formulation>
  identity_evidence=<record IDs + selectors>
  adoption=<current adopted|longitudinal|reported|unresolved>
  certainty=<...>
  encounter_role=<PRIMARY|BACKGROUND|unresolved>
  role_evidence=<record IDs + selectors>
  status=<descriptor>@<record IDs>
  contains=<handles; relationship evidence>
  separate_from=<handles; reason>
  contributors=<handle; relationship; certainty; record IDs>
  counterevidence=<record IDs + selectors>
  actions=<action IDs>
  primary_holder=<action IDs>
  position=<order>
```

### C. Note blueprint

```text
SECTION RFC/HPI/NEURO_HX/OTHER_PMH/MEDS/EXAM/WORKUP
  sequence=<unit/action IDs + selectors, only when supported>
  function=<why here>
  preserve=<attribution/time/negation/conflict qualifiers>

AP <problem handle>
  claim=<B label + permitted status>
  support=<record IDs + selectors>
  counter=<record IDs + selectors>
  reasoning=<source-supported synthesis or none>
  plan=<action IDs>
  shared_action_home=<action ID -> problem>
  references_only=<shared actions rendered elsewhere>
```

Then render from this blueprint only.

## First test

Use the smallest three-record packet:

```text
T001 :: SPK2 :: Three falls since June.
P1.001 :: SEC=HPI :: VIA=EMS report :: Patient reports three falls.
P1.002 :: SEC=PMH :: Prior left MCA stroke in 2022.
```

Before prose, the map must produce:

- one falls unit with refs `T001`, `P1.001`;
- one historical left MCA stroke unit with ref `P1.002`;
- unclear speaker role for `SPK2`;
- no inferred count total;
- no stroke–falls causality;
- no residual deficit;
- no current stroke problem;
- no consult reason unless source establishes it;
- no action, test or result.

If the architecture cannot preserve that boundary, richer cases will only hide the failure.

## What to delete

- atomic fact corpus;
- pointer-only topic index;
- synthesized `fact:` prose;
- separate action pass by default;
- separate renderer call by default;
- same-model validator;
- final audit pass.

No Gate-0 acceptance. No Doximity production change. No Phase 0.
