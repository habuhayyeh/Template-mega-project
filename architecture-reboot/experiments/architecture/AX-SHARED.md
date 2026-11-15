# AX-SHARED — shared diagnostic/management action across problems

**Status:** DESIGN ONLY / UNRUN

## Question

Can the architecture represent one underlying clinical action that serves multiple neurologic problems while preserving one-owner semantics and all clinically material cross-problem relevance/rationale?

## Architecture claim under test

A/P units can retain exactly one owning problem while preserving clinically meaningful secondary cross-problem relevance through a downstream schema that does not create a second action identity.

## Core fixture design

Each case should contain:
- at least two neurologic problem candidates;
- one shared diagnostic or management action;
- one problem-specific action for each problem;
- explicit source-grounded linkage of the shared action to both problems.

At least one core fixture must give the shared action **different explicit rationales for the two problems**, not one rationale that merely applies twice.

Example shape:
- seizure evaluation;
- possible new stroke;
- one MRI serving both;
- rationale A: evaluate structural epileptogenic/new lesion concern;
- rationale B: evaluate acute ischemic/vascular lesion concern;
- EEG specific to seizure;
- vascular workup/secondary-prevention action specific to stroke.

Do not use a case where the second linkage is inferred only from drug class or convention.

## Optional robustness fixture

A shared action that is referenced in both a body section and A/P may be tested separately.

This mixes cross-problem sharing with cross-section reuse, so it is robustness evidence rather than part of the minimum core shared-action claim.

## What stays open

Do not pre-freeze:
- `also_serves`;
- `secondary_problem_refs`;
- cross-problem rationale field names;
- exact render syntax.

Those are schema candidates to compare.

## Preservation scope

Both distinct problem-specific rationales must remain recoverable in the structured IR.

Final-note prose is governed by the signer-approved target and section contract:
- any rationale designated clinically material to communicate must remain represented in the final note;
- the note needs no second action identity and need not separately restate both rationales when one concise combined realization or permitted cross-reference preserves the required meaning;
- concision is not permission to erase a clinically material secondary rationale.

## Required output behavior

- the shared action has one identity and one owner;
- one A/P owning problem is explicit;
- both distinct rationales remain recoverable in the IR;
- all signer/section-contract-required rationale content is preserved in the final note without unnecessary duplication;
- problem-specific actions remain under their own problems;
- no duplicated action identity;
- no clinically material rationale is silently dropped;
- no fake second ownership is created.

## Experimental arms

Compare candidate representations, for example:
- one owner + secondary problem references;
- one owner + cross-problem rationale object/relation;
- other minimal schema that preserves both rationales.

The experiment should determine the minimal sufficient representation; it should not assume one schema in advance.

## Scoring

- action identity count (one), not textual occurrence;
- owner correctness;
- IR preservation of both rationales;
- final-note preservation of all rationale content required by the signer-approved target/section contract;
- problem-specific action placement;
- no duplicate action identity;
- no semantic loss;
- reproducibility across fresh runs.

## Run design

- Gate 0 scorer calibration first;
- freeze exact fixtures, candidate schema arm, package/scorer versions;
- repeat frozen arms under the standard same-order fresh-run gate before robustness permutations.

## Architecture consequence

If a minimal downstream schema preserves one action identity, one owner and both rationales reproducibly:
> keep one-owner A/P architecture.

If all reasonable one-owner representations either create a second action identity or lose clinically necessary linkage:
> reopen the one-owner assumption for shared actions.

This is a focused schema/architecture boundary test, not a general multi-problem test.

## Pending product decision

Whether a shared action renders once, or once under its primary problem with a terse reference from the second, is a **product decision, PENDING_SIGNER**.

One-owner A/P semantics entail one *owner*, not one *mention*. This experiment must not freeze either policy as required behaviour; it measures which representations are constructible and what each preserves, and the signer chooses among them.

## Occurrence count is unscored

How many times the action appears in the final note is **UNSCORED** until signer policy is frozen. The
scored invariants are: one action identity, one owning problem, both clinically material rationales
preserved, and no second action identity. Textual occurrence is a product decision and must not appear as
an architecture invariant anywhere in this spec.
