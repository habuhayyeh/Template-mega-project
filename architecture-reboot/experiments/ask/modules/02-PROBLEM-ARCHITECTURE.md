# FILE B — PROBLEM ARCHITECTURE

**Experimental version:** B-PROBLEM-ARCHITECTURE-V1

## Purpose

Transform File A's reconciled semantic ledger into the **neurologic problem structure for this encounter**.

File B decides which supported subjects have independent problem identity, which findings remain contained
within another problem, which distinct downstream neurologic disorders remain separate, how problems relate,
and which problems are PRIMARY or BACKGROUND for this encounter.

File B does **not** reinterpret the source record from scratch and does **not** write the note.

## Inputs

Provide both:

1. the complete File A handoff:
   - `DECISION_LEDGER`
   - `ACTION_LANE`
   - `UNRESOLVED_REGISTER`
2. the canonical `SCRIBE_EVIDENCE_V2_2` packet for direct dereference of cited record IDs/selectors.

File A remains the semantic reconciliation layer.
The Scribe packet remains the canonical source store.

## Output

Return `PROBLEM_MAP` only.

```text
@@HANDOFF B_PROBLEM_ARCHITECTURE_V1

PROBLEM_MAP

PROBLEM P001
  label=<minimal source-supported problem formulation>
  identity_evidence=<record IDs + selectors>
  adoption=<current_adopted|longitudinal|reported|historical|unresolved>
  certainty=<possible|likely|suspected|unlikely|unstated>
  encounter_role=<PRIMARY|BACKGROUND|unresolved>
  role_evidence=<record IDs + selectors>
  status=<source-supported descriptors/status + evidence>
  contains=<contained manifestation/unit handles + relationship evidence>
  separate_from=<distinct problem handles + reason/evidence>
  contributors=<handle or source concept; relation; certainty; evidence>
  counterevidence=<record IDs + selectors>
  actions=<ACTION IDs>
  primary_action_holder=<ACTION IDs>
  order=<integer>

@@END
```

Use only fields that have supported content, except:
- `label`
- `identity_evidence`
- `adoption`
- `certainty`
- `encounter_role`
- `order`

which are required for every rendered problem.

When the packet is insufficient, use `unresolved` rather than inventing a decision.

## Core ownership

File B owns:

- candidate-problem threshold;
- independent problem identity;
- disease-centered vs syndrome-centered organization;
- manifestation containment;
- distinct downstream neurologic disorder separation;
- multifactorial syndrome representation;
- PRIMARY vs BACKGROUND encounter role;
- supported causal/contributory relations;
- problem order;
- action ownership and primary action holder.

## What File B must not do

File B must not:

- create new source meaning;
- alter File A's polarity, certainty, temporality, attribution, event identity, or action state;
- resolve an `UNRESOLVED` conflict from File A unless the canonical source packet explicitly supplies
  evidence that File A failed to carry;
- change action decision/execution/response/result state;
- invent causality because two findings coexist;
- promote a historical disease into a current problem merely because it is mentioned;
- give every symptom, manifestation, residual deficit, or examination finding its own problem;
- decide note section placement;
- decide final note inclusion mechanics;
- write note prose;
- rewrite the final plan.

## Problem threshold

A subject receives its own problem only when it has **independent clinical identity** or its own current
assessment question/status.

A separate problem is justified when one or more of the following are supported:

1. it is an established neurologic disease/disorder with independent clinical identity;
2. it is the current presenting neurologic syndrome under substantive evaluation when no disease identity
   adequately organizes it;
3. it is a distinct downstream neurologic disorder, even when caused by another problem;
4. it is an active multifactorial syndrome whose contributors cannot be represented adequately as one
   parent disease;
5. its relationship to another problem is unresolved and it must temporarily function as its own syndrome
   or finding-level problem to preserve the clinical question.

Do not create a separate problem merely because a finding is:
- current;
- important;
- abnormal;
- examined;
- monitored;
- treated;
- mentioned repeatedly.

## Disease-centered vs syndrome-centered organization

Prefer a **disease-centered** problem when a supported disease identity adequately organizes the current
manifestations, status, evidence, and management.

Use a **syndrome-centered** problem when:
- no disease identity is sufficiently supported;
- the encounter is substantively evaluating a presenting syndrome;
- forcing a disease label would overstate the evidence.

Do not force a syndrome fallback when an established disease already explains and owns the manifestation.

## Containment

Manifestations, symptoms, deficits, status descriptors, and established consequences remain contained
within the parent problem when they are adequately explained by that problem and do not have independent
clinical identity.

Examples of contained material:
- seizure-free duration under established epilepsy;
- residual hemiparesis after established stroke;
- improving weakness as a stroke consequence/trajectory;
- examination findings that describe the current state of an existing problem.

Containment does not mean the finding is unimportant.
It means the finding does not become a separate problem block.

Represent contained material in:

```text
contains=<unit/manifestation>; evidence=<record IDs + selectors>
```

## Distinct downstream disorders

A downstream disorder may remain a separate problem when it has its own established clinical identity.

Example pattern:

```text
prior stroke
  -> epilepsy
```

The downstream disorder does not collapse into the upstream disease merely because a causal relation is
supported.

Use `separate_from` to preserve this distinction and cite the evidence/reason.

## Multifactorial syndromes

A syndrome may receive its own problem when:

- it is actively evaluated in the encounter;
- multiple contributors are plausible or supported;
- no single disease identity adequately owns the syndrome.

Do not manufacture a multifactorial syndrome merely because several abnormalities coexist.

Contributors remain relations, not automatically separate neurologic problems.

## Adoption and currentness

`adoption` answers how the problem identity is held in this encounter.

Allowed values:

- `current_adopted` — currently endorsed problem identity in this encounter;
- `longitudinal` — established disease identity carried longitudinally, with current relevance/status;
- `reported` — source-reported/outside formulation not clearly adopted in the encounter;
- `historical` — established past disease without evidence that it is currently active as a problem;
- `unresolved` — source support is insufficient to determine adoption/currentness.

Do not confuse:
- historical identity with current activity;
- outside diagnosis with Neurology adoption;
- mention with endorsement.

## Certainty

Use only the certainty supported by File A/source evidence:

- `possible`
- `likely`
- `suspected`
- `unlikely`
- `unstated`

Do not strengthen certainty because the problem is PRIMARY or because it receives management.

## Encounter role

`encounter_role` is independent of disease severity.

Allowed values:

- `PRIMARY`
- `BACKGROUND`
- `unresolved`

### PRIMARY

Use when the problem is central to why Neurology is substantively evaluating/managing the encounter.

### BACKGROUND

Use when the problem is established and clinically relevant but is not the main neurologic focus of this
encounter.

A major established neurologic diagnosis may remain BACKGROUND even if inactive.

Do not make a problem PRIMARY merely because:
- it is severe historically;
- it appears first in the chart;
- it has an important residual deficit;
- it caused another disorder.

## Role evidence

Every PRIMARY/BACKGROUND assignment must cite evidence that supports the encounter role.

Role evidence may come from:
- current evaluation focus;
- current management;
- current symptom/problem framing;
- explicit encounter reasoning.

Do not use diagnosis severity alone as role evidence.

## Causal and contributory relations

Only represent causal/contributory relations when source-supported.

Use:

```text
contributors=<handle or concept>; relation=<causal|contributory|possible_contributor>; certainty=<...>; evidence=<...>
```

Rules:

- use the most specific source-supported acting entity/formulation;
- do not invent an intermediate mechanism;
- do not increase certainty;
- coexistence is not causality;
- a residual deficit can contribute to another syndrome without becoming its own independent problem;
- a BACKGROUND problem may still causally contribute to a PRIMARY problem.

## Counterevidence

Preserve clinically meaningful counterevidence that changes interpretation of the problem.

Do not discard counterevidence merely because a problem was selected.

Use exact File A/Scribe references with selectors.

## Actions and action ownership

File B does not change action state.

It may associate existing File A `ACTION` entries with problems.

Use:

```text
actions=<ACTION IDs>
primary_action_holder=<ACTION IDs>
```

Rules:

- one action may relate to more than one problem;
- one problem should be the primary rendering/ownership home when a single home is needed;
- ownership does not imply the action was executed;
- do not infer an action state absent from File A;
- do not create a new action solely to complete a problem.

## Problem order

Assign `order` after problem identity and encounter role are resolved.

Order should reflect encounter logic, generally:
1. PRIMARY active problems;
2. other active/current problems;
3. BACKGROUND established neurologic problems.

Do not use chart source order as the problem order by default.

Do not force a problem count.

Sparse evidence should produce a sparse problem map.

## Relationship to nonproblem evidence

File A may contain:
- examination findings;
- medication-at-presentation material;
- workup/results;
- other history;
- functional/safety context;

that never becomes a problem.

File B must not discard or reclassify such material merely because it does not enter `PROBLEM_MAP`.

That material remains available to File C through File A + the canonical packet.

## Unresolved states

When problem identity, containment, role, or relation cannot be safely resolved from the available evidence:

- use `unresolved`;
- preserve the relevant evidence;
- do not guess;
- do not convert uncertainty into a new diagnosis.

File B may carry forward an unresolved architecture question but may not rewrite File A's source conflict.

## Structural checks

Before returning:

1. every problem has independent clinical identity or its own current assessment question/status;
2. no symptom/manifestation receives a separate problem solely because it is current or important;
3. contained manifestations remain inside the appropriate parent problem;
4. distinct downstream disorders remain separate when independently established;
5. historical disease is not promoted to current without supporting evidence;
6. PRIMARY/BACKGROUND reflects encounter role, not disease severity;
7. causal/contributory relations are source-supported;
8. counterevidence is preserved when clinically meaningful;
9. action IDs preserve File A action state and are not rewritten;
10. no note section, prose, or final-plan decision appears;
11. no forced problem count;
12. output contains only `PROBLEM_MAP` and ends with `@@END`.

Return the problem map only.
