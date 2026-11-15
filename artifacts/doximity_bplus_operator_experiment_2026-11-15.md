# Doximity B+ canonical-render-operator experiment — 2026-11-15

## Purpose

Test whether Doximity becomes reproducible when semantic grouping decisions are fixed upstream and the final writer receives a small canonical render operator rather than open-ended prose instructions.

This is synthetic test evidence. No real patient data.

## Prior challenge context

Three earlier arms used the same synthetic seizure content:

- Arm A — ordinary prose contract: clinically similar but merge/split and surface drift occurred.
- Arm B — structured DSL with explicit GROUP/CLASS/HEAD/MODIFIER/COVERED/CONDITION/ORDER: semantic structure stabilized, but wording still varied.
- Arm C — fully precomputed output: three runs were textually identical.

The B+ challenge tested the middle ground: explicit semantic groups plus a canonical render operator, without prewriting the entire note.

## B+ design

One batch contained 8 isolated rendering trials. The same batch was run in 3 fresh Doximity conversations.

Therefore:

- 8 operator executions per fresh conversation
- 3 fresh conversations
- 24 operator executions total

The 8 trials inside one response are contract-fidelity tests, not independent model sessions; the three fresh conversations are the true repeated-run axis.

Canonical operator families tested:

- FACT_DURATION
- FACT_TIMING_PROVENANCE
- FACT_COVERED
- REASONING_IMPERSONAL
- CONDITIONAL_PLAN
- SIMPLE_PLAN
- exact ordered multi-group rendering

## Observed result

All three fresh conversations returned the same T1-T8 outputs.

**Observed reproducibility: 24/24 operator executions matched across the three fresh runs.**

No run-to-run variation was observed in:

- duration folding;
- timing + provenance rendering;
- COVERED suppression;
- plan composition;
- plan order;
- group order;
- simple fact rendering;
- multi-group rendering.

### Repeated output pattern

T1
- Witnessed bilateral tonic-clonic seizure, ~2 mins.
- Postictal confusion, ~1 hr.

T2
- Known left MCA infarct two years prior to presentation (also documented by prior neurology, 2024-02).

T3
- CT head showed no hemorrhage or acute abnormality.

T4
- The MRI to show.
- EEG to determine whether there is epileptiform activity.

T5
- Hold apixaban; resume after MRI excludes hemorrhage.
- EEG.
- Seizure precautions.

T6
- Generalized weakness, ~1 hr.
- Productive cough.
- Chest radiograph showed no acute abnormality.

T7
- Prior right cavernous ICA aneurysm two years prior to presentation (also documented by prior radiology, 2024-03).
- Repeat vascular imaging.
- Outpatient vascular neurology follow-up.

T8
- Witnessed bilateral tonic-clonic seizure, ~2 mins.
- Known left MCA infarct two years prior to presentation (also documented by prior neurology, 2024-02).
- CT head showed no hemorrhage or acute abnormality.
- MRI to determine whether there is a new lesion.
- EEG.
- Hold apixaban; resume after MRI excludes hemorrhage.
- Seizure precautions.

The complete T1-T8 output above was repeated identically in all three fresh conversations.

## Important defect exposed

T4 rendered:

> The MRI to show.

This is poor prose, but it was reproduced identically in all three runs.

Interpretation:

- this is not stochastic drift;
- it is a deterministic operator/input defect;
- the render operator lacked a complete proposition.

T8 shows the correct representation pattern:

> MRI to determine whether there is a new lesion.

Therefore the renderer should not receive an incomplete conversational proposition such as:

`we'll see what the MRI shows`

and be expected to infer the missing semantic payload.

Instead the upstream representation should expose the complete relation, conceptually:

`TEST=MRI | PURPOSE=determine whether there is a new lesion`

and a canonical operator should render that relation.

## Architectural conclusion

The experimental progression is:

```
ordinary prose
    -> semantic + structural drift

explicit DSL groups
    -> semantic structure stable, wording still drifts

typed groups + canonical render operators (B+)
    -> textually stable across 3 fresh runs / 24 operator executions

fully precomputed output
    -> textually stable
```

This supports a production boundary between Arm B and Arm C:

> semantic objects -> explicit typed groups -> canonical render operator -> Doximity surface rendering

The evidence does **not** justify abandoning decomposition.

It supports removing semantic merge/split/compose decisions from the final writer.

## Implication for P006

P006 already contains the correct semantic roles:

- HEAD
- MODIFIER
- CONDITION
- COVERED
- rhetorical class
- order

The B+ evidence suggests adding one more explicit field:

- OPERATOR

Illustrative form:

```
FACT_GROUP G1
OPERATOR=FACT_DURATION
HEAD=O3
DURATION=O4
```

or:

```
COMPOSE_GROUP G2
OPERATOR=CONDITIONAL_PLAN
ACTION=O12
CONDITION_ACTION=O25
```

The operator vocabulary should remain small and generic rather than become a long set of case-specific rules.

Likely initial families to consider:

- PROBLEM_LINE
- FACT_SIMPLE
- FACT_DURATION
- FACT_TIMING
- FACT_TIMING_PROVENANCE
- FACT_COVERED
- REASONING_SIMPLE
- REASONING_TEST_PURPOSE
- PLAN_SIMPLE
- PLAN_CONDITIONAL
- PLAN_TEST

Exact names and schemas remain a proposal question.

## Next experiment

Do **not** run another synthetic architecture challenge first.

Revise P006 to incorporate the operator layer, then test the actual canonical seizure case in Doximity under the same package/mode across three fresh conversations.

The next test should answer whether the B+ result generalizes to the production-shaped P006 input.


---

# How to use this result effectively

This experiment should be used as a **render-boundary design guide**.

## When the operator output is correct and stable

Promote that operator pattern into the reusable render vocabulary.

Examples from this experiment:

- duration folding;
- timing + documentation provenance;
- covered-duplicate suppression;
- conditional plan composition;
- fixed ordering.

## When the operator output is stable but wrong

Treat that as an **operator or input-schema defect**, not as model randomness.

The key example is:

> `The MRI to show.`

It appeared identically in all three fresh runs.

The problem is that the operator received an incomplete conversational proposition:

`we'll see what the MRI shows`

The renderer was then expected to manufacture an impersonal sentence without being given the semantic object of `show`.

Do not add a looser prose instruction such as “make this sound natural.”

Instead expose the complete relation upstream:

```
TEST=MRI
PURPOSE=determine whether there is a new lesion
```

and render it with a bounded operator:

```
OPERATOR=REASONING_TEST_PURPOSE
TEST=MRI
PURPOSE=determine whether there is a new lesion
```

Expected surface:

`MRI to determine whether there is a new lesion.`

## When an operator varies across runs

First decide whether the variation is:

- semantic/structural;
- or merely stylistic.

If semantic/structural, the operator is not decision-complete enough and should be redesigned upstream.

If merely stylistic and clinically irrelevant, the variation may be acceptable.

## What not to do

Do not use this result to:

- add large prose exception lists;
- make the renderer infer missing clinical relations;
- infer management targets from medication identity;
- collapse the whole architecture into prewritten prose;
- claim absolute Doximity determinism from three runs.

The practical lesson is narrower:

> a small canonical operator layer can remove the residual variability that remained after semantic groups were already fixed.

# Relationship to the gradient experiment

The preceding gradient experiment is documented in:

`artifacts/doximity_gradient_experiment_2026-11-15.md`

Together, the two experiments show:

```
ordinary prose
    -> semantic + structural drift

structured DSL
    -> structure stable, wording drift

typed groups + canonical operators (B+)
    -> identical in this 3-run / 24-execution test

fully precomputed output
    -> identical
```

This is why the current target architecture is **between Arm B and Arm C**, not either extreme.
