# Proposal 119 — Ask Semantic Contract V1

**Status:** first-run experimental contract. Compact by design. Not a frozen production ontology.

## Purpose

Given a Scribe V2.2 evidence packet and the final neurology note template, determine the neurologically meaningful current encounter structure and render the final note.

Use the packet as evidence. Do not treat any single source as the final truth merely because it is already written in note form.

## Output

Return exactly two parts:

1. `AUDIT LEDGER`
2. `FINAL NOTE`

The ledger is for the experiment. The final note is the usable clinical output.

## Core rules

### 1. Source evidence is not automatically final stance

Every statement in the packet is a source proposition.

A diagnosis, assessment, problem label, medication, plan, historical statement, consultant opinion, collateral statement, imaging interpretation, or provisional A/P entry is evidence only until reconciled with the whole encounter.

Do not blindly inherit a source label into the final A/P.

Do not invent patient-specific facts.

Preserve meaningful uncertainty, negation, attribution, chronology, and disagreement.

### 2. Build independent neurologic problems, not a problem for every manifestation

Create a separate problem only when the item has an independent clinical identity in this encounter.

A symptom, deficit, manifestation, status descriptor, consequence, or piece of evidence that is adequately explained by and belongs to an existing problem stays contained under that problem.

Do not create a separate problem merely because a finding is important, current, examined, monitored, or mentioned repeatedly.

A distinct downstream neurologic disorder may be its own problem.

If the relationship is genuinely unresolved and the syndrome/finding is itself being substantively evaluated, it may remain an independent temporary problem.

### 3. Decide the current encounter stance separately from problem identity

For each independent problem, state in plain language what the current encounter supports.

Distinguish:

- current vs historical information;
- established vs suspected vs unresolved;
- stable/control/status vs active worsening or new syndrome;
- a source-documented proposition vs the stance adopted after considering the full encounter.

Do not strengthen certainty beyond the evidence.

### 4. Decide encounter role separately from causality

For each independent neurologic problem:

- `PRIMARY` = actively evaluated/managed now or independently driving the current neurologic assessment/management;
- `BACKGROUND` = neurologically relevant established/suspected disease that is not itself a primary current problem;
- `NOT_RENDERED` = does not warrant its own A/P problem representation.

Historical relevance alone does not make a problem PRIMARY.

Background problems should be compact.

### 5. Relations must be source/evidence supported

Do not infer causality merely because two findings coexist.

When a causal/contributory relation is used, preserve:

- direction;
- degree of certainty;
- the most specific source-supported acting participant/formulation.

Do not invent an intermediate mechanism.

Do not strengthen `possible` to `likely`, or an association to a cause.

### 6. Neurologic focus

Prioritize neurologic claims and neurologic problem structure.

Non-neurologic information belongs in the final note when it supports, refutes, contextualizes, or changes neurologic assessment or management, or is required by the final template.

Do not create separate non-neurologic A/P problems unless they materially affect the neurologic assessment/plan.

### 7. Use and realization

Select the smallest sufficient set of source-supported facts needed to explain the current neurologic assessment and plan.

Avoid repeating the same proposition in multiple places unless the repetition serves a distinct note function.

Keep historical/background problems compact.

Do not manufacture normal findings from template boilerplate or missing data.

Preserve documented normal findings when actually supplied as evidence.

Use an impersonal A/P voice; avoid first-person `I` or `we` in rendered assessment/plan prose.

## AUDIT LEDGER format

List independent neurologic problems only.

```text
AUDIT LEDGER

PROBLEM P1
  label: <plain-language independent problem>
  evidence: <packet record IDs supporting the problem and current reasoning>
  contained: <important symptoms/deficits/status/evidence that belong inside this problem>
  stance: <plain-language current encounter stance, including uncertainty>
  role: PRIMARY | BACKGROUND | NOT_RENDERED
  relations: <supported causal/contributory relations or none>
  render: <brief note-use instruction>

PROBLEM P2
  ...
```

Do not create a PROBLEM record for a contained manifestation.

Evidence IDs should be sufficient to audit the problem-level reasoning; do not annotate every sentence of the final note.

## FINAL NOTE rules

After the ledger, render the final note using the supplied template.

The final note must:

- use only supplied patient-specific facts plus clinical conclusions traceable to those facts;
- preserve uncertainty;
- distinguish current findings from historical/background information;
- keep manifestations contained under their parent problem when appropriate;
- avoid unsupported causal claims;
- include source-supported neurologic reasoning and plans;
- include non-neurologic material only where neurologically relevant or template-required;
- not treat placeholder/default template text as observed patient data;
- not expose the audit IDs or internal ledger syntax unless the final template explicitly requires them.

## Final self-check before output

Before returning the answer, verify:

1. No patient-specific fact was invented.
2. No source label was adopted merely because it appeared in a note/problem list.
3. No contained manifestation was promoted to an unnecessary independent problem.
4. No causal relation was invented or strengthened.
5. Current vs historical status and uncertainty are preserved.
6. The final A/P contains the neurologic problems that actually matter for this encounter and keeps background problems compact.

Return `AUDIT LEDGER` followed by `FINAL NOTE`.