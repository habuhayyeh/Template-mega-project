# Review 146 — A V2.1 -> B1 integration run

## Verdict

**Execution shape works. One bounded semantic patch is required before B2.**

The single-call A -> B1 controller executed correctly and returned both requested handoffs.

This is not an architecture failure. The remaining defects are narrow contract failures in A1 semantic
splitting/certainty and B1 action-state interpretation.

## What works

### A execution shape

- complete A handoff is produced;
- semantic and action lanes remain distinct;
- action-state enums do not reappear in A;
- compound ED CT/labs/UA are split;
- Keppra continuation, future continue/stop decision, MRI plan, precautions, driving restriction survive;
- action target for the conditional Keppra decision is correctly Keppra, with EEG/MRI as condition.

### B1 execution shape

- B1 consumes the A action lane in the same Ask invocation;
- no new problem architecture or note prose is produced;
- plan/order/result dimensions are usually kept separate;
- source-mediated prior Keppra administration is labeled reported_performed rather than objective performed;
- continuation remains a decision rather than execution.

## Hidden A1 defects that must be patched

### 1. Mixed-polarity selector collapsed into one polarity

A semantic span combines:

- `no focal deficit present`
- `alert and oriented to person, place, and time`

but assigns `polarity=negated` to the entire span.

This can invert a normal mental-status finding downstream.

Required contract change:
- if clauses differ materially in polarity, certainty, attribution, or semantic role, split them before
  assigning fields.

### 2. Topic mention converted to epistemic certainty

`medical resident already brought up PNES` receives `certainty=unlikely`.

The source says PNES was raised; it does not say PNES is unlikely.

Required contract change:
- mention/discussion/consideration as a topic does not itself establish possible/likely/suspected/unlikely;
- if no epistemic qualifier is stated, certainty=unstated.

Also distinguish uncertainty in a numeric estimate from epistemic certainty of the clinical proposition.

## Hidden B1 defects that must be patched

### 1. Planned consult upgraded to reported performance — fatal

From A004:
`Plan: ... consult neurology ...`

B1 emits:
- `execution=reported_performed`;
- `decision=planned`.

The same phrase cannot establish both. The plan context supports planned only.

This violates the predeclared oracle and is care-changing.

### 2. Source labels used as actors

B1 repeatedly emits `actor=P1` or `actor=SPK1`.

Those are source/speaker labels, not source-supported actor identities.

Actor must remain unresolved unless A/source text explicitly establishes the actor.

### 3. Ambiguous preference converted to recommendation + agreement

For:
`discussed inpatient vs outpatient workup and being on the fence; preference for doing workup`

B1 emits:
- decision=recommended;
- response=agrees;

while simultaneously stating patient vs clinician preference is ambiguous.

If actor/owner is ambiguous, neither recommendation nor patient agreement is supported.

### 4. Uncertain Keppra administrations grouped despite unresolved identity

A009 and A010 are grouped into one episode while B1 itself says it is unresolved whether they are the same
episode.

Uncertain episode identity should remain separate, with a relation unresolved, not grouped first and
qualified afterward.

### 5. Bundled A action not surfaced as A_ACTION_GAP

A019 has target `EEG and MRI`.

B1 uses it in the EEG episode rather than flagging that A violated the one-action-identity rule.

B1 must emit A_ACTION_GAP for an A span that bundles distinct action targets and must not use that bundled
span as evidence for one selected child action.

## Bounded patch

A:
- split mixed polarity/certainty/attribution/role clauses;
- clarify certainty semantics.

B1:
- governing plan context supports planned only, not execution;
- bare shorthand does not entail state;
- state evidence phrase should be the minimal phrase carrying the state;
- source labels are not actors;
- ambiguous preference cannot become recommendation/agreement;
- unresolved episode identity means do not group;
- bundled A action => A_ACTION_GAP, no selective child use.

No new stage, validator, or architecture change.

## Advancement rule

After one rerun of the same A -> B1 integration:
- if these hidden meaning-changing defects are gone, proceed to B2 even if minor reviewable imperfections remain;
- do not optimize further for cosmetic variance.

No C/render changes.
