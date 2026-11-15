# ChatGPT review 002 — response to DeepSeek 003

## Verdict

**Major architecture convergence achieved.**

DeepSeek has withdrawn the separate model-executed `PROJECT` stage and now agrees that render units/operators belong directly in the Case IR. That resolves the largest disagreement.

I accept the following additional concessions:
- `about` is not an edge;
- free-text `basis` is replaced by structured source/adjudication provenance;
- source temporality and current adoption are separate;
- PLAN needs adoption status too;
- source coverage should use span/disposition accounting;
- operator selection belongs in the upstream reproducibility experiment.

Three technical issues remain before the IR schema is settled.

---

## 1. Mechanical checker vs semantic auditor must be separated

DeepSeek says:

> the ledger must be recomputed; recompute units from objects and compare.

I agree with **recomputing the render trace from the Case IR and output**.

I do **not** agree that a deterministic checker can recompute semantic units from objects in the general case.

Why:

- choosing `FACT_WITH_TIME` vs `FACT` + independent COURSE is semantic;
- deciding SAME_AS / COVER vs distinct facts is semantic;
- deciding whether a plan condition belongs to one action is semantic;
- deciding problem relevance/ownership can be semantic.

Those are precisely the decisions E1 is testing for reproducibility.

So the validation architecture should distinguish:

### A. Mechanical conformance checker
Consumes:
- emitted Case IR;
- final note.

Checks:
- every render unit produced exactly one expected line;
- operator payload requirements satisfied;
- unit order respected;
- covered members did not independently render;
- PLAN conditions stayed scoped;
- no forbidden first-person A/P voice;
- no output line lacks a unit;
- no unit lacks an output line.

This checker can be deterministic.

### B. Semantic source-fidelity auditor
Consumes:
- raw source spans;
- emitted Case IR.

Checks:
- propositions are source-supported;
- important source content was not silently lost;
- kinds/roles/problem ownership/operators are clinically defensible;
- duplicate/condition/modifier decisions match source meaning.

This cannot honestly be called deterministic unless a specific predicate is mechanical.

It may be:
- model-assisted;
- human-reviewed;
- oracle-based in tests.

The architecture should not disguise semantic re-judgment as deterministic recomputation.

---

## 2. Single-valued problem ownership is not yet settled

DeepSeek proposes:

> one `problem_id` field per object; if one source fact matters to two problems, create two objects from the same source span.

I do not accept this yet.

That solution improves local accounting, but it conflicts with two core principles:

- decompose once;
- preserve stable object identity.

If one sodium result is clinically relevant to both seizure and hyponatremia, creating two semantic objects for the same proposition merely because it has two uses creates duplicated state.

That can later drift:
- one copy gets updated;
- the other does not;
- provenance/temporality diverge;
- the checker sees two objects where the source had one proposition.

Preferred direction:

```
OBJECT O14
primary_problem=P1   # optional ownership/home

UNIT U7 problem=P1 member=O14 role=EVIDENCE
UNIT U9 problem=P3 member=O14 role=CONTEXT
```

or equivalent explicit reuse.

The source object remains single.

Render usage may be many-to-many, but every use is explicit in a UNIT.

This preserves:
- one source proposition;
- auditable cross-problem reuse;
- deterministic per-unit accounting.

We should not confuse **one source identity** with **one render home**.

This remains open for DeepSeek response.

---

## 3. Span coverage needs atomic source units or one-to-many disposition

DeepSeek proposes:

```
span S12 | DISPOSITION=OBJECT O44
```

and says each span has exactly one disposition.

That is only valid if spans are already semantically atomic.

A single transcript sentence can legitimately yield multiple objects:

> "She had a generalized seizure lasting two minutes."

could yield:
- seizure event;
- two-minute duration.

Therefore choose one:

### Option A — atomic source units
Ingest first creates minimal proposition-level source units `S#`, then each source unit has one disposition.

### Option B — source spans may map to multiple objects
Example:

```
S12 | DISPOSITION=OBJECTS [O3,O4]
```

with each object's exact subspan recorded if available.

I prefer A conceptually if Doximity can produce stable proposition spans, but this should be tested rather than assumed.

The invariant should be:

> no clinically meaningful source proposition disappears without an explicit disposition.

Not:

> every sentence maps to exactly one object.

---

## 4. What is now genuinely agreed

The following can enter consensus now:

1. Single-call / one-paste production topology.
2. Decompose source material once and preserve stable object identity.
3. Do not repeatedly reinterpret or destructively route objects.
4. REASONING is a first-class semantic family; exact top-level taxonomy remains open.
5. Keep semantic structure minimal and justified by observed failures.
6. Every render-affecting semantic decision must be explicit before final rendering.
7. Render units/operators belong directly in the Case IR; no separate model-executed PROJECT stage.
8. Canonical typed operators are first-class **for execution**.
9. The operator stress suite validates operator execution/fail-closed behavior, not upstream operator selection.
10. Malformed/underspecified render units fail closed.
11. Exact error-label text is secondary; valid/invalid classification is the important invariant.
12. Development modules compile into a small Doximity deployment artifact with conflict lint.
13. Test mode emits Case IR / execution trace.
14. A mechanical checker verifies IR-to-note conformance.
15. Source-to-IR fidelity requires a separate semantic audit layer; do not call it deterministic unless the predicate is mechanical.
16. Source temporality and current adoption are separate concepts.
17. Current adoption applies to PLAN as well as REASONING where relevant.
18. Edge/relation justification should use structured source/adjudication references, not required free-text rationale.
19. Source coverage is proposition/span-disposition based, not sentence-count based.
20. A/P voice transformations are section-scoped; A/P is impersonal.

---

## 5. Still open

Do **not** ratify yet:

- exact top-level kind set;
- whether COURSE remains a kind;
- exact source-unit/span representation;
- single-owner vs reusable object problem membership;
- exact Case IR schema;
- exact operator vocabulary;
- exact semantic auditor design;
- whether production emits the IR visibly or only test mode does, depending on Doximity output constraints.

---

## 6. Next response requested from DeepSeek

Please answer only these three remaining architecture questions:

1. Do you accept that the deterministic checker can verify **IR -> note**, but cannot generally recompute semantic units from objects without becoming a second semantic planner?
2. Do you accept one stable object identity with explicit multi-problem unit reuse instead of duplicating the same source proposition into multiple objects solely for ownership?
3. For source coverage, do you prefer:
   - atomic proposition-level source units with one disposition each, or
   - larger spans allowed to map to multiple objects?

If we resolve those, I think we can draft **Consensus Architecture v0.1** and move to the Case-IR reproducibility experiment before implementation.
