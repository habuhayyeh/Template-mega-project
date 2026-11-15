# AX-R2 — R2 expressivity and representation burden

**Status:** DESIGN ONLY / UNRUN

## Question

Can weak R2 produce signer-quality HPI/history prose without making new semantic decisions, and without requiring an upstream discourse representation more complex than the clinical content itself?

## Architecture claim under test

R2 can remain a bounded composition layer:
- preserves unit order;
- joins already-decided content;
- does not invent temporal/causal/contrast relations.

## Case set

Use 5–10 realistic signer-quality HPI/history targets containing combinations of:
- chronology;
- progression;
- source attribution;
- negatives;
- uncertainty;
- symptom linkage;
- mixed current/history;
- competing explanations;
- transitions from symptom onset to presentation.

The executable manifest freezes the actual selected cases and count.

Before testing, the signer marks:
- clinically mandatory content/relations;
- material chronology/attribution requirements;
- acceptable stylistic variation where needed.

Do not require signer approval of every wording difference.

## Independent upstream constructors

The "minimum sufficient upstream representation" is not objective if one experimenter constructs it.

For each case:
1. two independent constructors, preferably the two LLMs, receive the same source + signer-approved target;
2. each proposes the minimum upstream representation believed sufficient for weak R2;
3. neither sees the other's representation before freezing its own;
4. both representations are tested;
5. differences are analyzed rather than silently reconciled before the experiment.

## Experimental method

For each frozen representation:
1. render with R1/R2 under frozen contracts;
2. identify every discourse feature in the target:
   - already represented upstream;
   - safely mechanical/stylistic in R2;
   - would require R2 to invent semantics.

Iterative redesign may follow a failed representation, but post-hoc additions cannot be used to claim the original representation passed.

## Primary metrics

- semantic fidelity to target;
- chronology preservation;
- progression preservation;
- attribution preservation;
- no invented causality;
- no invented contrast;
- no dropped uncertainty;
- representation burden:
  - number/type of upstream relations or unit constraints needed;
  - amount of upstream structure relative to source clinical content;
  - constructor-to-constructor difference in required representation.

## Run design

- Gate 0 scorer calibration first;
- freeze exact cases, constructor artifacts, package/scorer versions;
- use the default repeated-run protocol for each frozen representation.

## Interpretation

### Weak R2 succeeds with modest upstream structure
Keep R2 boundary.

### Weak R2 succeeds only with a large discourse graph
Architecture may be over-structuring ordinary language generation.

### R2 repeatedly must invent clinically meaningful connectives
Reopen R2 allowed-operations boundary or move a clearly owned discourse-planning decision upstream.

## Reopen criterion

Do not relax R2 merely for prettier prose.
Reopen only if signer-quality factual chronology/relationship expression cannot be achieved without either:
- semantic invention in R2; or
- disproportionate upstream representation complexity.
