# Doximity reproducibility gradient experiment — 2026-11-15

## Purpose

Determine whether Doximity reproducibility improves as semantic and wording freedom are progressively removed from the final note-writing stage.

This was a synthetic test. No real patient data.

The same synthetic seizure case was tested under three increasingly constrained contracts:

- **Arm A — ordinary prose contract**
- **Arm B — structured DSL with explicit semantic roles**
- **Arm C — fully precomputed render plan**

Each arm was run in **3 fresh Doximity conversations** under the same intended experimental condition for that arm.

The experiment was designed to distinguish:

1. variability caused by open-ended prose instructions;
2. variability caused by residual surface-realization freedom after semantic structure is fixed;
3. variability that persists even when the final text is completely specified.

---

# 1. Experimental gradient

## Arm A — ordinary prose contract

Doximity received clinical objects plus prose instructions such as:

- combine overlapping CT information;
- combine timing with the relevant fact;
- preserve provenance;
- treat apixaban hold/resume as one management decision;
- preserve reasoning and plan order.

The model still had to decide **how** those instructions mapped onto final bullets.

### Observed result

The three runs were clinically similar, but they were not structurally/textually identical.

Meaningful variation included:

- whether old left MCA encephalomalacia remained a separate bullet or was merged into the CT bullet;
- CT wording:
  - `with no hemorrhage and no acute abnormality`
  - `showed no hemorrhage and no acute abnormality`
  - `old left MCA encephalomalacia with no hemorrhage or acute abnormality`;
- provenance rendering:
  - `documented by prior neurology 2024-02`
  - `also documented by prior neurology 2024-02`
  - parenthetical provenance;
- `two years ago` versus `2 years ago`;
- apixaban composition:
  - `held with resumption after MRI excludes hemorrhage`
  - `held; resume after MRI excludes hemorrhage`;
- capitalization and punctuation.

### Key failure

In one run the model merged:

- old left MCA encephalomalacia

with:

- CT head no hemorrhage / no acute abnormality

into one CT bullet, while other runs kept them separate.

That is clinically meaningful **merge/split drift**.

### Interpretation

Ordinary prose rules do not fully determine the semantic grouping of output.

**Arm A verdict: clinically similar, but not structurally deterministic.**

---

## Arm B — structured DSL

Doximity received explicit fields such as:

- `GROUP`
- `CLASS`
- `HEAD`
- `MODIFIER`
- `PROVENANCE`
- `COVERED`
- `CONDITION`
- `ORDER`

The model no longer had to decide whether the seizure and duration belonged together, whether a duplicate CT object should get its own line, or whether hold/resume represented one management decision.

### Observed result

Across all three runs, the clinically meaningful structure remained stable:

- one seizure + duration bullet;
- one postictal + duration bullet;
- one infarct + provenance bullet;
- one encephalomalacia bullet;
- one CT bullet;
- one substrate-reasoning bullet;
- one MRI-reasoning bullet;
- exactly five plan items;
- apixaban hold/resume remained one management line;
- ordering remained stable.

However, surface wording still varied.

Examples:

- `Witnessed bilateral tonic-clonic seizure, ~2 mins`
  versus
  `Witnessed bilateral tonic-clonic seizure lasting ~2 mins`;

- provenance after an em dash versus parentheses;

- `resume apixaban` versus `resume`;

- `old left MCA encephalomalacia` versus `old left MCA encephalomalacia on CT`;

- CT punctuation and conjunction differences.

### Interpretation

Explicit semantic roles removed the major merge/split instability, but the final writer still had freedom to choose sentence architecture and wording.

**Arm B verdict: semantically/structurally stable, but not textually deterministic.**

---

## Arm C — fully precomputed render plan

Doximity was told to return an already specified final Assessment & Plan exactly.

### Observed result

All 3 runs were **textually identical**.

The repeated output preserved exactly:

- capitalization;
- punctuation;
- abbreviations;
- bullet count;
- order;
- merge/split structure;
- provenance rendering;
- plan composition.

### Interpretation

This demonstrates that Doximity is capable of highly reproducible output when essentially all semantic and surface decisions are removed.

It argues against the hypothesis that Doximity itself is so stochastic that deterministic-looking output is impossible.

**Arm C verdict: textually deterministic in this test.**

---

# 2. Gradient result

The experiment produced a clean reproducibility gradient:

```
Arm A — ordinary prose
    many semantic + wording choices remain
    -> clinical meaning similar, but merge/split and wording drift

Arm B — structured DSL
    semantic relationships fixed
    -> structure stable, wording still drifts

Arm C — precomputed render plan
    semantic relationships + wording fixed
    -> identical output across 3 fresh runs
```

## Main conclusion

The dominant problem is not decomposition itself and is not proven to be unavoidable Doximity randomness.

The dominant failure mode is:

> the final writer is asked to rediscover semantic relationships and sentence architecture that could instead be specified upstream.

The experiment supports moving clinically meaningful decisions out of free-form generation.

---

# 3. What this experiment does and does not prove

## It supports

- retaining the atomic-object/decomposition architecture;
- moving merge/split decisions upstream;
- making duplicate coverage explicit;
- making timing/modifier relationships explicit;
- making conditional management composition explicit;
- fixing output order upstream;
- reducing the final writer to a narrower rendering task.

## It does not prove

- that every production case will be reproducible;
- that all Doximity modes behave identically;
- that 3 runs establish mathematical determinism;
- that a fully precomputed note is the preferred production design;
- that all semantic classification can safely be made mechanical.

The result is engineering evidence about the **location of variability**, not a guarantee about all future cases.

---

# 4. How to use this result effectively

Use the gradient as a design diagnostic.

When a future Doximity run varies, ask:

### If the variation is merge/split, duplication, problem ownership, or management composition
Move that decision **upstream into explicit structured metadata**.

Do not add another prose instruction to the final writer.

### If the structure is stable but wording varies
Consider whether the wording difference matters.

- If clinically irrelevant, it may remain generative.
- If reproducibility matters, define a canonical render operator.

### If a fully specified output still varies
That is stronger evidence of platform/runtime noncompliance rather than contract ambiguity.

### Do not use this experiment to justify
- exploding the workflow into many files;
- abandoning decomposition;
- adding dozens of special-case prose rules;
- treating all model variability as a platform defect.

The useful abstraction is **decision completeness**, not file count.

---

# 5. Relationship to the B+ experiment

The gradient identified the gap between Arm B and Arm C:

- Arm B had correct semantic structure but residual wording freedom.
- Arm C was reproducible but prewrote the note.

The follow-up **B+ canonical-render-operator experiment** tested the middle ground:

> typed semantic groups + small canonical render operators

That experiment is documented separately in:

`artifacts/doximity_bplus_operator_experiment_2026-11-15.md`

The B+ result is the practical architectural follow-up to this gradient.
