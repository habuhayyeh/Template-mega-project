# Architecture Reboot V2 — Working Rules

## Purpose

This branch is a **clean-room architecture workspace** for redesigning the neurology note-generation system from first principles.

It is intentionally separate from the current implementation work on `main`.

The existing pipeline, decisions, tests, and failures may be used as **evidence about what worked or failed**, but they are **not inherited as architectural requirements** unless this workspace independently adopts them.

## Goal

Design the smallest architecture that can reliably turn source material — especially the encounter recording/transcript plus relevant prior records — into a neurologically centered clinical note that is:

- source-faithful;
- clinically useful;
- reproducible in clinically meaningful content;
- auditable;
- resistant to fabricated facts or silent loss;
- practical to deploy in Doximity's attachment-based environment.

## Design and implementation boundary

The structural architecture is frozen unless a new counterexample requires reopening it. Do **not** silently change architecture, module ownership, interfaces, predicate meaning, experiment hypotheses, oracle semantics, or product/clinical policy during implementation.

Once a contract is accepted, bounded implementation defects may be fixed directly. DeepSeek remains the default primary engineer for substantial implementation. ChatGPT may directly patch localized defects when the accepted contract and tests determine the correction, then must commit the change and hand it to DeepSeek for independent review.

## Review loop

For architecture/contract work, the intended cycle is:

1. DeepSeek proposes first by default, unless the user asks ChatGPT to lead.
2. ChatGPT reviews it critically:
   - identify unnecessary complexity;
   - identify missing relationships;
   - identify Doximity/runtime assumptions;
   - challenge unsupported assumptions and drift.
3. DeepSeek revises; ChatGPT reviews the actual change.
4. Repeat until the agents agree or the user adjudicates.

For bounded implementation defects after the contract is accepted:

1. whichever agent finds the defect may patch it directly if the correction is unambiguous from the accepted contract;
2. add/adjust tests or validators;
3. commit the patch;
4. the other agent independently reviews the actual diff and validation evidence;
5. correct if needed, then update state.

Escalate to the user whenever:
   - the agents disagree and repository evidence does not settle it;
   - the choice is subjective, clinical, stylistic, or product-related;
   - a platform assumption cannot be verified;
   - proceeding would require guessing.

## Path ownership and implementation exception

### ChatGPT owns
- `architecture-reboot/proposals/chatgpt/`
- `architecture-reboot/reviews/chatgpt/`
- `architecture-reboot/channel/to-deepseek.md`

### DeepSeek owns
- `architecture-reboot/proposals/deepseek/`
- `architecture-reboot/reviews/deepseek/`
- `architecture-reboot/channel/to-chatgpt.md`

### Implementation
- DeepSeek is the default primary implementer for substantial/new implementation work.
- ChatGPT may directly edit implementation paths for bounded, contract-preserving fixes it discovers during review.
- A ChatGPT implementation patch must include or update tests/validation where applicable, be committed, and be handed to DeepSeek for independent review.
- This exception does not permit ChatGPT to silently alter frozen architecture, interfaces, predicate semantics, experiment definitions, oracle semantics, or product/clinical/style policy.

### Consensus
- `architecture-reboot/CONSENSUS.md` is written only after both agents explicitly agree on a design point.
- ChatGPT may draft the consensus text; DeepSeek must explicitly confirm it in its channel before it is treated as agreed.
- The user remains final authority.

## Efficiency protocol

### Classify before acting

Every substantive finding is one of:

- **ARCHITECTURE** — accepted design cannot satisfy the requirement; reopen deliberately.
- **CONTRACT** — required behavior is underspecified or contradictory; fix the governing contract.
- **IMPLEMENTATION** — accepted contract determines the answer; patch directly, test, commit, independent review.
- **NONBLOCKING** — editorial/low-impact cleanup that cannot invalidate evidence; record without blocking progress.

### Review the dependency cone, not the whole project

Every implementation handoff declares:

```text
COMMIT:
TYPE:
CHANGED:
INVARIANTS:
VALIDATION:
BLOCKERS:
NEXT:
```

Review starts with the declared diff, affected invariants, generated outputs, and direct dependencies. Widen only when a failed check, hash, generated artifact, or explicit dependency requires it.

### Stop when the layer is proven enough

Do not reopen a layer merely because another review pass might find something. Stop when:
- the governing contract is satisfied;
- required validators/tests pass;
- evidence is reproducible;
- no remaining defect can invalidate or materially mislead the result.

Reopen only for new evidence: a failing test, counterexample, implementation result, or genuine contradiction.

### Prefer asymmetric work

- DeepSeek: substantial/new implementation, local execution, repository maintenance, first-pass engineering.
- ChatGPT: architecture/contract adjudication, adversarial review, invariant/test design, bounded direct fixes.
- The non-authoring agent reviews the actual diff and evidence.

### Preflight first

Consolidate recurring mechanical checks behind one architecture-reboot preflight entry point. It should cover, where applicable:
- source/generated freshness;
- governing-source hashes and campaign identities;
- deterministic regeneration / second-run zero diff;
- seed mutation integrity;
- active-predicate/registry consistency;
- dependency-context integrity;
- scorer/unit tests;
- stale-marker detection;
- forbidden architecture or Phase-0 drift.

Once available, preflight precedes broad implementation review or acceptance work. A missing human/semantic prerequisite blocks semantic acceptance, not safe mechanical build/test/packet preparation.


Every proposed architecture should be judged against:

1. **Source fidelity** — no invented clinical facts; provenance remains recoverable.
2. **Semantic stability** — important clinical relationships are decided once, not rediscovered repeatedly.
3. **Reproducibility** — identical clinically meaningful input should yield the same clinically meaningful note structure/content.
4. **Auditability** — failures can be localized to a named decision/module.
5. **Minimality** — avoid proliferating rules, stages, or schemas without demonstrated value.
6. **Doximity feasibility** — deployment must fit the actual file/prompt/runtime constraints.
7. **Clinician usability** — the resulting note should reflect the neurologist's reasoning and preferred style without requiring cumbersome manual orchestration.
8. **Extensibility** — the architecture should support HPI, history, workup, A/P, and future specialty-specific behavior without duplicating semantic logic.

## Clean-room constraint

Do not argue that something must exist merely because the old pipeline had it.

For each component ask:

> If we were starting today, knowing what the experiments taught us, would we deliberately design this component?

If not, remove or replace it.
