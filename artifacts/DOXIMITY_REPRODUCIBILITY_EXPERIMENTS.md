# Doximity reproducibility experiments — index and use guide

## Why these artifacts exist

These experiments were created to identify where reproducibility failures arise in the Doximity note-generation workflow.

They should be treated as **architecture evidence**, not as clinical-note templates and not as proof of absolute determinism.

## Read in this order

### 1. Gradient experiment

`artifacts/doximity_gradient_experiment_2026-11-15.md`

Question:

> What happens as semantic and wording freedom are progressively removed?

Result:

- ordinary prose -> structural/wording drift;
- structured DSL -> structure stable, wording still varies;
- precomputed render plan -> identical across three fresh runs.

Use this artifact to understand **where the variability lives**.

### 2. B+ canonical-render-operator experiment

`artifacts/doximity_bplus_operator_experiment_2026-11-15.md`

Question:

> Can we recover Arm-C-like reproducibility without prewriting the entire note?

Result:

- 8 isolated operator trials;
- 3 fresh Doximity conversations;
- 24/24 operator executions reproduced identically across the three runs.

Use this artifact to justify the current target boundary:

> semantic objects -> typed groups -> canonical render operator -> Doximity rendering

## Important bug

B+ deliberately exposed a bad deterministic render:

> `The MRI to show.`

This appeared identically in all three runs.

That bug is important because it distinguishes:

- **stochastic drift** from
- **deterministic contract/input defects**.

The operator was given an incomplete proposition. The renderer should not be expected to infer the missing semantic object.

Correct architecture:

```
TEST=MRI
PURPOSE=determine whether there is a new lesion
```

then:

`REASONING_TEST_PURPOSE -> MRI to determine whether there is a new lesion.`

Do not fix this class of problem with more free-form prose at the rendering stage.

## Engineering rules derived from both experiments

1. **Keep decomposition.**
   Atomic source-faithful objects remain useful.

2. **Do not repeatedly rediscover relationships.**
   Grouping, coverage, modifiers, conditions, and order should be explicit upstream.

3. **Use canonical render operators for wording that must be stable.**
   Operators should be small, generic, reusable, and auditable.

4. **Do not prewrite the whole note unless required.**
   Arm C proves exact reproduction is possible, but B+ suggests it may not be necessary.

5. **Treat stable bad output as a contract bug.**
   If the same wrong phrase appears every run, fix the representation/operator.

6. **Treat unstable semantic structure as an upstream decision gap.**
   Do not solve merge/split drift with more stylistic prompting.

7. **Use production-shaped validation next.**
   Synthetic challenges have served their purpose. The next meaningful test is the canonical seizure case under revised P006.

## Current architectural implication

These experiments support revising P006 to add an explicit `OPERATOR` to its existing typed groups while preserving D-016's narrow scope.

They do **not** independently authorize broader P007 normalization.
