# ChatGPT review 029 — Review 3 final conformance leaks

## Verdict

DeepSeek 023 accepts the substance of Review 3, but **Review 3 is not closed yet**.

Three rewrite consequences reintroduce unauthorized requirements while ostensibly fixing the old ones.

This is exactly the pattern DeepSeek correctly identified:

> a predicate that answers an open design question becomes an unpublished decision.

---

# 1. H2 — invented threshold: ">=2 independent evidence sources per CRITICAL class"

DeepSeek rewrites H2 as:

> coverage requires >=2 independent evidence sources per CRITICAL class.

This is **not authorized upstream**.

The frozen Doximity protocol explicitly rejects arbitrary fixed thresholds where empirical characterization is required.

Review 3 said:

> failure class is one axis, not the whole oracle.

It did **not** authorize:
- two sources;
- two fixtures;
- two cases;
- any fixed minimum per severity class.

## Correct rewrite consequence

Coverage must be represented as a multidimensional coverage ledger across the required dimensions, such as:
- architecture invariant;
- submodule/seam;
- failure class;
- semantic primitive;
- source type;
- operator family;
- high-risk historical regression;
- long-context/position stress where applicable.

Coverage sufficiency is a governed acceptance question.

If a future rule requires a numeric minimum for some dimension, that threshold must be justified and frozen through the proper acceptance/design path.

**Do not invent `>=2` now.**

---

# 2. H1/H2 — failure class cannot become the primary corpus-completeness axis

DeepSeek says:

> count is not fixed; coverage is measured per class.

That is still too narrow.

The frozen experimental protocol says:

> coverage matrix, not random notes.

And Review 3 explicitly states failure class is **one axis**, not the whole oracle.

A corpus can cover every F1-F10/C11-C14 class and still omit:
- S1 problem-model ambiguity;
- conditional adoption;
- source contradiction;
- specific source-family combinations;
- R2 prose composition;
- standing-item triggers;
- multi-problem reuse;
- operator-family coverage;
- long-context/position effects.

## Correct consequence

Do not define corpus completeness as "per failure class."

Define it as:
> coverage across the frozen architecture/acceptance dimensions recorded in COVERAGE_LEDGER.

Failure class is one tag/dimension.

---

# 3. F3 — test/production equivalence must not require IR fields that production may not expose

DeepSeek rewrites O-01 as:

> equivalence at note + declared IR fields, not byte equality.

Better than byte equality, but still overcommits.

Frozen architecture explicitly leaves open whether Case IR is:
- visible only in test mode;
- hidden/suppressed in production.

Therefore production-mode equivalence cannot require comparison of IR fields that do not exist externally in production.

## Correct consequence

The obligation should be phrased behaviorally:

> test instrumentation must not materially change the production-relevant decisions/output properties that are externally observable or otherwise validly comparable under the paired experiment.

Where both modes expose a comparable field, compare it.
Where production suppresses the field, do not invent observability.

The exact paired equivalence predicates remain downstream acceptance design.

---

# 4. B1 — CHECK wording still needs the mechanical qualifier

DeepSeek says:

> CHECK proves IR->note conformance only; semantic adequacy is AUDIT's.

This is directionally correct but still too broad if read as **all** IR→note conformance.

Frozen consensus #21 is specific:
- unit references;
- operator validity;
- unit↔line mapping;
- allowed transformations;
- voice;
- ordering;
- accounting.

R2 semantic-preservation can remain non-mechanical.

## Correct wording

> CHECK proves the **declared mechanically decidable IR→note conformance predicates**. It does not prove semantic adequacy or any non-mechanical preservation predicate.

This avoids recreating the original overclaim in shorter language.

---

# Review 3 closure condition

DeepSeek should answer only these four corrections.

If accepted without adding another threshold or hidden semantic rule, Review 3 is CLOSED.

No Phase 0 rewrite yet.
