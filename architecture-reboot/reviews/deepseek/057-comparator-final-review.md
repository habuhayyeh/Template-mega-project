# DeepSeek final review — A vs direct-B comparator

**Verdict:** BLOCKED by one decision-rule ambiguity. Everything else is ready.

## What is fixed

- Two runs per arm, fresh sessions.
- No averaging of material failures.
- A→B citation mapping through A span/action to Scribe.
- Direct-B citation mapping to Scribe.
- Canonical action-concept normalization.
- Problem threshold now requires encounter relevance.
- Direct-B not penalized for intermediate IDs.
- Mixed results are inconclusive, not averaged.

## Remaining ambiguity

The decision rule says direct-B must have:

> no more hidden semantic errors than **either** A→B run

“Either” is ambiguous:

- no more than at least one A run;
- no more than both A runs;
- no more than the better A run;
- no more than the worse A run.

This is the main tie-breaker. Define it explicitly.

Recommended conservative rule:

```text
direct_errors <= min(A1_errors, A2_errors)
```

Direct-B must be no worse than the **better** A→B run on hidden semantic errors. If A has 1 and 3 errors,
direct-B needs ≤1. If A has 2 and 2, direct-B needs ≤2.

If you prefer a less strict rule, use `<= max(A1,A2)`, but state it. Do not leave “either.”

## Other dimensions

- Action/provenance coverage: “equal or better than both” is clear.
- Problem architecture/stance: “equivalent or better than both” is clear.
- Representation burden: nonblocking unless fidelity equal.
- A single excellent direct-B run remains insufficient.

## Fairness

Direct-B carries ingestion + synthesis in one pass; A→B splits them. That is the cost being tested, not an
unfair prompt asymmetry.

## After the fix

State the error comparison explicitly, then run four fresh sessions:

- A1, A2;
- D1, D2.

No C/CLINICAL_UNIT until the comparator is adjudicated.

No new stage, enum or validator. No acceptance or production change.
