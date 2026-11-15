# ChatGPT review 011 — synthesis of independent failure maps

## Context

This review was written after an independent pre-sync failure analysis in:

`architecture-reboot/reviews/chatgpt/010-pre-sync-failure-analysis.md`

and then compared against DeepSeek:

`architecture-reboot/reviews/deepseek/011-failure-mode-map.md`

The two maps converge strongly. I accept DeepSeek's ten defect classes and its conclusion that S4 is the densest risk concentration without that implying it should be split.

---

# 1. Main agreement

DeepSeek's map correctly captures the major demonstrated runtime failures:

- fabrication;
- duplication;
- silent omission;
- contract/schema break;
- run-to-run instability;
- cross-problem leakage;
- provenance misuse;
- prior-to-current promotion;
- voice violation;
- truncation.

I also agree with:

- silent omission having multiple entry points;
- instability being a cross-run property rather than a single-module defect;
- S4 being high-risk because it concentrates decisions, not because its boundary is wrong;
- RENDER being far safer than old 05 once semantic choices are removed.

---

# 2. Four additional failure classes should remain explicit

## F11 — Contract contradiction / duplicate authority

Historical example:
- the added prior-record/EVIDENCE_MODE rule conflicted with the existing WORKUP rule and moved O51 from the correct section.

This is not merely F5 instability. The model was given contradictory authority.

Primary owner:
- BUILD / contract compilation, not a runtime submodule.

Runtime manifestation:
- I1/S4/R1 may behave inconsistently while each locally follows one valid rule.

Defense:
- one decision owner;
- centralized contracts;
- build-time conflict/authority lint;
- regression fixtures after every rule change.

---

## F12 — Stable bad output from representation incompleteness

Historical example:
- `The MRI to show.` repeated identically across B+ runs.

This is not stochasticity, fabrication, or malformed syntax.
The system was stable but semantically under-specified.

Primary owners:
- S2/S4 representation completeness;
- R1 must refuse to infer the missing relation.

Defense:
- semantic payload completeness requirements;
- operator-specific required semantic fields;
- production-shaped fixtures, not only typechecks.

Important:
A Case IR can be mechanically valid yet clinically/linguistically insufficient.

---

## F13 — Over-inclusion / wrong note use

Examples:
- background antihypertensive/statin/fluid restriction appearing in neurologic A/P without sufficient neurologic relevance;
- preference/driving/chronic concern routed into inappropriate sections.

This differs from F6 cross-problem leakage:
- F6 = right content attached to wrong problem;
- F13 = content should not have been retained for that note use at all, or is placed in the wrong note view.

Primary owners:
- S3 relevance/use;
- S4 section assignment.

Defense:
- neurologic-claim-centered selection policy;
- explicit omission/use accounting;
- section-use semantic audit.

---

## F14 — Non-local regression after rule change

Historical example:
- a rule added for one failure changed unrelated object placement.

This is related to F5 but operationally distinct:
- F5 measures repeated-run variance with fixed instructions;
- F14 measures regression caused by changing the contract.

Primary owner:
- engineering regression system / BUILD.

Defense:
- no prompt patch accepted on one target example alone;
- run whole regression suite after every contract change;
- diff Case IR by object/unit/operator, not only final prose.

---

# 3. One qualification to DeepSeek's renderer conclusion

DeepSeek says RENDER is forbidden from making decisions that could produce F2/F3/F5.

Directionally correct, but not absolute:

- R1 could still violate output cardinality and duplicate/omit a unit if not mechanically checked;
- R2 can drop a unit during prose composition, as DeepSeek itself maps under F3;
- R3 can truncate/omit a section;
- R2 can introduce wording-level instability even when the Case IR is stable.

The improved statement is:

> RENDER no longer has **legitimate semantic authority** to create duplication, omission, or structural variance. If those occur in RENDER, they are contract violations rather than discretionary semantic choices and should be mechanically detectable where feasible.

That distinction is stronger.

---

# 4. Failure contract should become part of every concrete submodule spec

The old system often had:

1. what to do;
2. what not to do.

The concrete implementation should require four blocks:

## DO
The intended operation.

## AVOID
Forbidden decisions/transformations.

## DETECT
How failure becomes observable:
- mechanical predicate;
- semantic audit criterion;
- cross-run reproducibility comparison.

## FAILURE BEHAVIOR
What happens when the submodule cannot satisfy the contract:
- preserve as UNKNOWN/UNRESOLVED;
- emit typed error;
- fallback to faithful representation;
- fail closed.

Most importantly:

> failure in one submodule must not be silently converted into a plausible success by the next one.

---

# 5. Per-module highest-risk failure focus

| Submodule | Highest-risk failure |
|---|---|
| I1 Source Map | provenance/source-family misclassification |
| I2 Span Registry | silent source loss / semantic segmentation |
| I3 Object Extraction | fabrication or proposition omission |
| I4 Source Annotation | provenance/time/adoption conflation |
| S1 Problem Model | wrong problem/claim granularity |
| S2 Semantic Adjudication | false duplicate/condition/adoption relation |
| S3 Selection & Problem Use | silent omission or inappropriate inclusion/problem use |
| S4 Blueprint | wrong grouping/section/operator/order or missing required unit |
| R1 Realization | semantic repair / unsupported wording / voice |
| R2 Composition | deletion/reorder/new relation during prose joining |
| R3 Assembly | missing/extra/reordered section or wrapper |

Cross-cutting:
- BUILD: contract contradiction and regression;
- AUDIT: semantic source->IR correctness;
- CHECK: IR->note conformance;
- E1/E2: reproducibility across fresh runs.

---

# 6. Proposed next step

Before writing exact prompt/DSL syntax, turn the frozen performance guidance into a **failure-aware implementation specification** for each submodule:

```text
SUBMODULE
GOAL
INPUT
OUTPUT

DO
AVOID
DETECT
FAILURE BEHAVIOR

CONTROL MODE
VALIDATION MODE
```

Then derive prose/pseudocode/operator text from that specification.

This preserves the failure lessons from main in the concrete implementation rather than relegating them to a retrospective document.
