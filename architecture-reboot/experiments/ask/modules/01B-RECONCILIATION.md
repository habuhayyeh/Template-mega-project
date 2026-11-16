# SUPERSEDED — DO NOT RUN

This experimental split was retired after peer convergence on one source-local A ingestion phase with
separate semantic and action lanes.

Use instead:

`01-SOURCE-LOCAL-INGESTION.md`

Cross-record reconciliation now begins downstream in B.

---

# FILE A2 — RECONCILIATION

**Experimental version:** A2-RECONCILIATION-V1

## Purpose

Reconcile the material source-local assertions preserved by File A1 into the sparse semantic state used by
problem architecture and note compilation.

A2 answers:

> Which preserved source-local assertions describe the same event/state, corroborate one another, evolve,
> conflict, or belong to distinct action episodes?

A2 may compress.
A2 may not rewrite what A1 says each source span actually asserted.

## Inputs

Provide both:

1. complete A1 `SOURCE_SEMANTIC_LEDGER`;
2. canonical `SCRIBE_EVIDENCE_V2_2` packet for direct dereference only.

A1 is authoritative for:
- source pointer;
- selector;
- assertion type;
- raw speaker/source;
- explicit local identity/provenance;
- source-local polarity;
- source-stated certainty;
- explicit local action state;
- source-local unresolved state.

A2 may not change those fields.

## Output

Return the same three downstream lanes expected by File B:

```text
@@HANDOFF A2_RECONCILED_V1

DECISION_LEDGER

UNIT U001
  concept=<short non-problem label>
  evidence=<A1 SPAN IDs + source record IDs/selectors + role>
  kind=<statement|question|observation|result|diagnosis|reasoning>
  attribution=<reconciled provenance without changing A1 source identity>
  time=<reconciled event/source time if established>
  scope=<current_episode|current_encounter|longitudinal|historical|future|unknown>
  polarity=<affirmed|negated|unresolved>
  certainty=<possible|likely|suspected|unlikely|unstated>
  relation=<same_event|same_state|evolution|conflict|possible_overlap|independent|none>
  disposition=<carry_forward|nonproblem_section_material|exclude_redundant>
  unresolved=<material cross-record limitation>

ACTION_LANE

ACTION A001
  target=<short label>
  operation=<short action label>
  setting=<source-supported setting>
  time_scope=<episode time>
  source_spans=<A1 SPAN IDs>
  decision=<state>@<SPAN/source>
  execution=<state>@<SPAN/source>
  response=<state>@<SPAN/source>
  result=<state>@<SPAN/source>
  actor=<source-supported actor/provenance>
  condition=<source-supported condition>
  unresolved=<cross-record limitation>

UNRESOLVED_REGISTER

UNRESOLVED X001
  topic=<short label>
  evidence=<A1 SPAN IDs + source references>
  issue=<cross-record conflict/uncertainty>

A1_DISPOSITION

SPAN S001
  disposition=<represented_in:U001|represented_in:A001|redundant_with:S002|carry_to_C|excluded_nonclinical>
  reason=<short reason>

@@END
```

Use only lanes with entries, except `A1_DISPOSITION`, which is required.

## Core invariant

A2 may reconcile **relationships between preserved assertions**.

A2 may not change the source-local assertion itself.

If A1 says:
- `assertion_type=question`, A2 cannot turn it into a statement;
- raw speaker `SPK3`, A2 cannot invent a patient/mother identity;
- `decision:planned`, A2 cannot turn it into `execution:ordered`;
- `execution:reported_performed`, A2 cannot upgrade it to direct `performed`;
- `polarity=unresolved`, A2 cannot resolve it without another explicit A1 span supporting resolution.

## What A2 owns

A2 owns:
- duplicate/corroboration;
- same event/state;
- evolution;
- conflict;
- possible overlap;
- event/course chronology across records;
- longitudinal synthesis;
- cross-source unresolved;
- action-episode grouping;
- sparse semantic compression;
- preservation/disposition accounting for every A1 span.

## What A2 must not do

A2 must not:
- discover a new clinical assertion from the packet that A1 did not preserve;
- repair A1 by silently rereading the source;
- change A1 source pointers/selectors;
- change A1 assertion type;
- change A1 raw speaker/source;
- globally infer speaker identity;
- change A1 source-local polarity/certainty;
- infer an action state absent from A1;
- decide candidate-problem status;
- decide PRIMARY/BACKGROUND;
- decide containment;
- decide causal/contributory problem relationships;
- decide final note sections;
- write final note prose.

If A2 discovers that material source evidence is missing from A1:
- do not silently add it;
- add an `UNRESOLVED` item with `return_to_A1=yes`.

## Reconciliation order

For each cluster of potentially related A1 spans:

### 1. Check referent

Do they concern the same:
- person;
- event;
- disease;
- symptom;
- test;
- medication/action;
- time episode?

Do not merge merely because words overlap.

### 2. Preserve assertion-type boundaries

A question cannot corroborate a statement.

A diagnosis/formulation cannot silently become an observed fact.

A management action remains separate from diagnostic reasoning.

### 3. Reconcile provenance

Multiple sources may corroborate the same event while preserving their distinct source roles.

Do not erase:
- patient vs collateral vs documentation source;
- direct vs mediated report;
- source-specific uncertainty.

### 4. Reconcile time

Only after source-local times are preserved may A2 determine:
- same event;
- sequence;
- evolution;
- historical vs current scope.

If timing remains incompatible, preserve conflict/unresolved.

### 5. Reconcile polarity/certainty

Do not average or strengthen.

If sources disagree:
- preserve conflict;
- carry counterevidence;
- do not choose a cleaner value without support.

### 6. Reconcile actions by episode

One ACTION object represents one action episode/trajectory keyed approximately by:

```text
target + operation + setting + time/encounter episode
```

Do not merge:
- cruise administration;
- ED proposed load;
- ED cancel/stop;
- current continuation decision;

merely because all involve Keppra.

A2 may group source-local action states into one trajectory only when they clearly concern the same episode.

## Sparse compression

A2 should be sparse.

It may combine corroborative A1 spans into one UNIT when:
- same referent;
- same material state/event;
- no material provenance/polarity/time distinction is lost.

Do not recreate the packet.

But compression may **never silently delete material A1 content**.

That is why `A1_DISPOSITION` is required.

## A1 disposition accounting

Every A1 SPAN must receive one disposition.

Allowed:
- `represented_in:U###`
- `represented_in:A###`
- `redundant_with:S###`
- `carry_to_C`
- `excluded_nonclinical`

Use `carry_to_C` for material source-local content that does not require semantic reconciliation but must survive for later note compilation, such as:
- current exam;
- medication-at-presentation;
- straightforward workup result;
- history-only content;
- safety/function material.

This prevents A2's sparsity rule from deleting content needed downstream.

Do not use `excluded_nonclinical` for clinically relevant content merely because it is not a problem.

## Action lane rules

Action fields remain field-specific.

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

Rules:
- only states already present in A1 source spans may appear;
- unknown fields stay absent;
- no template completion;
- no `planned -> ordered`;
- no `ordered -> performed`;
- no `not_started -> pending result`;
- no discontinuation of one episode erases prior reported execution in another episode.

## Nonproblem material

A2 is not allowed to make current exam, medications, history, workup, or safety/function disappear because
they do not form a reconciled problem-relevant UNIT.

Such spans may remain:
- represented in a UNIT;
- represented in an ACTION;
- or explicitly `carry_to_C`.

B determines problem architecture.
C later decides note placement.

## Structural checks

Before returning:

1. every evidence pointer traces to an A1 SPAN and source record;
2. no selector is invented or moved to the wrong record;
3. question spans never support statement assertions;
4. raw speaker/source identity is not rewritten;
5. cross-record relation appears only in A2;
6. action states come only from A1;
7. action episodes are not merged across distinct settings/times;
8. every A1 SPAN has an `A1_DISPOSITION`;
9. no material A1 span disappears silently;
10. missing A1 source evidence is flagged back to A1 rather than repaired;
11. no problem/role/section/prose decision appears;
12. output ends with `@@END`.

Return the handoff only.
