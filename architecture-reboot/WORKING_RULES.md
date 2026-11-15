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

## Design phase only

Do **not** modify the production pipeline from this branch while the structural design is unsettled.

No implementation should begin until the agents agree on a structural design or the user explicitly chooses between unresolved alternatives.

## Review loop

The intended cycle is:

1. ChatGPT writes a structural proposal.
2. DeepSeek reviews it critically:
   - identify unnecessary complexity;
   - identify missing relationships;
   - identify Doximity/runtime assumptions;
   - propose a better alternative where appropriate.
3. ChatGPT reviews DeepSeek's critique and revision.
4. Repeat until the agents agree.
5. Escalate to the user whenever:
   - the agents disagree and repository evidence does not settle it;
   - the choice is subjective, clinical, stylistic, or product-related;
   - a platform assumption cannot be verified;
   - proceeding would require guessing.

## One writer per path

### ChatGPT owns
- `architecture-reboot/proposals/chatgpt/`
- `architecture-reboot/reviews/chatgpt/`
- `architecture-reboot/channel/to-deepseek.md`

### DeepSeek owns
- `architecture-reboot/proposals/deepseek/`
- `architecture-reboot/reviews/deepseek/`
- `architecture-reboot/channel/to-chatgpt.md`

### Consensus
- `architecture-reboot/CONSENSUS.md` is written only after both agents explicitly agree on a design point.
- ChatGPT may draft the consensus text; DeepSeek must explicitly confirm it in its channel before it is treated as agreed.
- The user remains final authority.

## Evaluation criteria

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
