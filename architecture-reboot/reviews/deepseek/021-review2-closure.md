# DeepSeek response 021 — Review 2 closure points

All three accepted. Two are better than what I proposed.

**1. Decision-registry inclusion criterion.** Accepted. My wording was vague enough to justify anything. The criterion is:

> A decision is registered when it is normative **and** externally consequential — interface-visible, cross-referenced by another contract, multiply governed, directly referenced by an acceptance predicate or a coverage obligation, or such that changing its owner or value semantics would require a `DESIGN CHANGE` or `ACCEPTANCE CHANGE`.

Anything else stays local and unregistered. That is a test another person can apply, which mine was not.

**2. One assertion model, not a dichotomy.** Accepted, and it replaces my `INVARIANT` / `ASSERTION` split. A predicate carries an explicit `applies_to` clause; a case-bound assertion has a narrow applicability, a reusable invariant has a broad one, and both are the same kind of record. Two record types would have produced two evaluators that drift.

**3. No protocol amendment.** Accepted, and it is the better answer. My proposal widened the rule to accommodate packaging assertions; this instead distinguishes predicate kinds and leaves the frozen runtime rule intact:

| Predicate kind | Owner domain | Rule preserved |
|---|---|---|
| case assertion | runtime submodule (I1–R3) | one owning submodule, used for first-divergence localisation |
| `BUILD_GATE` | BUILD | package/completeness predicates |
| `PROCESS_GATE` | PROCESS | repetition agreement, regression diffs |
| `SCORER_CONTROL` | SCORER | negatives, calibration |

Universal rule: **every acceptance predicate has exactly one registered owner; the owner domain is determined by predicate kind.**

Consequences: F-06a becomes a `BUILD_GATE`, F-15a a `PROCESS_GATE`, A-C02a a `PROCESS_GATE` (or is dropped), and the fixture index gains a `predicate_kind` column. No amendment, no orphan.

**4. Experiment manifest.** Accepted: shared condition fields belong to `EXPERIMENT_MANIFEST`; a packet references `EXP-id` and `arm`, and may repeat a shared field only as a checked snapshot with a hash. A packet that invents its own shared condition is invalid.

Review 2 is closed from my side.
