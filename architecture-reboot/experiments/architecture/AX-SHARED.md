# AX-SHARED — shared diagnostic/management action across problems

**Status:** DESIGN ONLY / UNRUN

## Question

Can the architecture represent one real clinical action that serves multiple neurologic problems without duplicating the action, losing a rationale, or violating one-owner A/P semantics?

## Architecture claim under test

A/P units can retain exactly one owning problem while preserving clinically meaningful secondary cross-problem relevance through a downstream schema that does not duplicate rendered actions.

## Fixture design

Each case should contain:
- at least two neurologic problem candidates;
- one shared diagnostic or management action;
- one problem-specific action for each problem;
- explicit source-grounded rationale linking the shared action to both problems.

Example shape:
- seizure evaluation;
- possible new stroke;
- one MRI serving both;
- EEG specific to seizure;
- vascular workup/secondary-prevention action specific to stroke.

Do not use a case where the second linkage is inferred only from drug class or convention.

## What stays open

Do not pre-freeze:
- `also_serves`;
- `secondary_problem_refs`;
- cross-problem rationale field names;
- exact render syntax.

Those are schema candidates to compare.

## Required output behavior

- shared action renders exactly once;
- one A/P owning problem is explicit;
- both clinically important rationales remain recoverable/preserved;
- problem-specific actions remain under their own problems;
- no duplicated order/action;
- no rationale is silently dropped;
- no fake second ownership is created.

## Experimental arms

Compare candidate representations, for example:
- one owner + secondary problem references;
- one owner + cross-problem rationale object/relation;
- other minimal schema that preserves both rationales.

The experiment should determine the minimal sufficient representation; it should not assume one schema in advance.

## Scoring

- action cardinality;
- owner correctness;
- preservation of both rationales;
- problem-specific action placement;
- no duplicate render;
- no semantic loss;
- reproducibility across fresh runs.

## Architecture consequence

If a minimal downstream schema solves the case reproducibly:
> keep one-owner A/P architecture.

If all reasonable one-owner representations either duplicate the action or lose clinically necessary linkage:
> reopen the one-owner assumption for shared actions.

This is a focused schema/architecture boundary test, not a general multi-problem test.
