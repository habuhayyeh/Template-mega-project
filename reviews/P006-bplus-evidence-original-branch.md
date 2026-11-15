# B+ experiment review: implication for P006 — original architecture branch

## Verdict

**NEW EVIDENCE SUPPORTS REVISING P006 BEFORE IMPLEMENTATION.**

Do not implement P006 v5 as currently written.

The new B+ Doximity experiment produced identical T1-T8 outputs across three fresh conversations: 24/24 canonical-operator executions matched.

This is materially stronger evidence than the earlier prose/DSL runs because it directly tests the missing boundary between P006's semantic groups and 05's residual wording freedom.

## What the experiment establishes

1. Ordinary prose leaves clinically meaningful degrees of freedom.
2. Explicit grouping removes most semantic drift.
3. Explicit grouping plus a small canonical render operator removed the remaining observed drift in this test.
4. A fully precomputed note is therefore not necessary to obtain C-like reproducibility in the synthetic challenge.
5. The remaining bad output (T4: `The MRI to show.`) is deterministic and traceable to an incomplete operator/input proposition, not runtime randomness.

## Required proposal change

DeepSeek should revise P006, not implement v5.

Preserve:

- FACT_GROUP / REASON_GROUP / COMPOSE_GROUP;
- HEAD / MODIFIER / CONDITION / COVERED;
- class-specific ordering;
- trace/accounting;
- D-016 narrow scope.

Add an explicit **canonical render operator** field to each group.

Conceptually:

```
FACT_GROUP: G1
OPERATOR=FACT_DURATION
HEAD=O3
DURATION=O4
```

```
COMPOSE_GROUP: G2
OPERATOR=PLAN_CONDITIONAL
ACTION=O12
CONDITION_ACTION=O25
```

05 should select neither the semantic relation nor the sentence architecture. It should execute the operator using the supplied payload.

## Operator design constraints

The vocabulary should be:

- small;
- generic;
- reusable across cases;
- auditable;
- deterministic enough to validate mechanically;
- not a list of one-off case templates.

Candidate families are listed in the experiment artifact, but DeepSeek should propose the exact minimal set.

The operator must not become a general paraphrase license.

## D-017 correction exposed by B+

P006 v5 currently resolves MRI reasoning as:

`MRI to show.`

The B+ test confirms that this surface rule is under-specified and produces bad prose deterministically.

The better architecture is not to make the operator infer the missing object of `show`.

Upstream should expose the full semantic payload already present in the case, e.g.:

`TEST=MRI | PURPOSE=determine whether there is a new lesion`

and the renderer should apply a bounded reasoning-test-purpose operator:

`MRI to determine whether there is a new lesion.`

This is not free-form inference if the PURPOSE is explicitly represented upstream.

This point requires DeepSeek to reconcile D-017 with the new evidence. Since D-017 currently hard-codes `MRI to show.`, the proposal should identify whether a superseding decision is needed before implementation.

## Scope

Do not use this result to reopen broad P007 normalization.

D-016 still governs.

This change is narrowly about how P006 groups are rendered after their semantics are already fixed.

## Next validation

After proposal/review/approval:

- implement P006 + operators;
- test the actual canonical seizure case;
- same Doximity mode;
- same package;
- three fresh conversations;
- compare semantic and textual reproducibility.

No additional synthetic challenge is required before that.
