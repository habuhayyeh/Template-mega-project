# AGENTS.md

Operational constitution. Read this, then `STATUS.md`, then `DECISIONS.md`, before doing anything.

## Roles

- **DeepSeek — primary engineer / co-engineer.** Inspects the repository, proposes architecture first by default, implements substantial work, runs validators, records results, updates state, and independently reviews bounded implementation patches made by ChatGPT.
- **ChatGPT — architect/reviewer + bounded implementation maintainer.** Reads the actual repository and diffs, challenges assumptions, detects overfitting and drift, writes reviews, and may directly patch localized implementation defects when the accepted contract already determines the correct behavior.
- **User — final authority.** Resolves clinical, style, product, governance, and architectural disputes and may change the agent division of labor.

## The rules that govern collaboration

On architectural or contract work, **DeepSeek proposes first**. ChatGPT reviews the existing proposal rather than generating the first solution, unless the user asks it to lead. ChatGPT is expected to challenge and refine, not merely approve.

On implementation work, either agent may fix a bounded defect when the accepted contract and tests make the correction unambiguous. When ChatGPT discovers such a defect during review, it should normally patch it directly, add or adjust tests, commit the change, and hand the exact commit to DeepSeek for independent review. This direct-patch rule does **not** authorize silent changes to architecture, module ownership, frozen interfaces, predicate meaning, experiment hypotheses, oracle semantics, clinical/style/product policy, or other accepted design contracts.

## When to stop and ask the user

Either agent escalates, at any point, when:

- the two agents disagree on a design point and neither can settle it with repository evidence;
- the contract is genuinely ambiguous, not merely terse;
- the choice is clinical, stylistic, or product, and cannot be derived from a decision or a contract;
- the consequence changes what the note says to a reader;
- the alternative is guessing.

Do not escalate mechanical choices, formatting, or tooling details that a decision or contract already answers. An escalation that could have been resolved from the repository is noise.

Form: one short message — the question, the options, a recommendation. No document.

The answer is recorded as a `D-###` decision. Until it is there, it is not settled.

## When a proposal is required

A `P###` proposal is required when a change alters:

- what a stage accepts or emits;
- a module contract;
- the substrate schema;
- oracle semantics;
- the six kinds or the metadata schema;
- **which stage is responsible for a decision**.

Fixing behaviour that was already agreed is a `T###` task with a recorded validator run, not a proposal.

## Ownership

Coordination/review paths remain single-writer. Implementation paths have a bounded exception under D-018.

| Path | Writer |
|---|---|
| legacy implementation paths such as `pipeline/`, `tools/`, `substrate/`, `oracles/`, `tests/`, `runs/`, `artifacts/`, `tasks/` | DeepSeek by default; ChatGPT may patch bounded implementation defects under D-018 |
| `architecture-reboot/scorer/`, `architecture-reboot/tools/`, `architecture-reboot/tests/`, and other implementation artifacts under the reboot | DeepSeek by default; ChatGPT may patch bounded implementation defects under D-018 |
| `architecture-reboot/reviews/chatgpt/`, `architecture-reboot/proposals/chatgpt/`, `architecture-reboot/channel/to-deepseek.md` | ChatGPT |
| `architecture-reboot/reviews/deepseek/`, `architecture-reboot/proposals/deepseek/`, `architecture-reboot/channel/to-chatgpt.md` | DeepSeek |
| `STATUS.md`, `CHANGELOG.md` | DeepSeek by default |
| `DECISIONS.md`, `AGENTS.md`, `PROJECT.md` | either agent only after an explicit user-approved governance/design decision |

A ChatGPT direct implementation patch must preserve accepted design semantics, include or update validation/tests where applicable, be committed to GitHub, and be handed to DeepSeek for independent review. DeepSeek must not treat a ChatGPT patch as self-validating merely because ChatGPT authored it.

## Workflow

Design/contract changes:

```text
task → proposal → review → user decision → implementation → validation
     → review of the actual diff → correction → state update
```

Bounded implementation defects after the contract is accepted:

```text
review finds defect → discovering agent patches + tests → commit
                    → other agent independently reviews actual diff
                    → correction if needed → state update
```

`STATUS.md` moves only at the end. Validation means command, exit code and output, recorded under the appropriate evidence/run path — never a sentence claiming it passed.

## Precedence

```text
current explicit user decision → DECISIONS.md → AGENTS.md
→ stage contract → PROJECT.md → STATUS.md
```

`STATUS.md` never defines behaviour. If an instruction conflicts with a permanent decision, stop and flag it; do not override the repository.

## Data

Synthetic or fully de-identified only. No real encounter text anywhere in this repository.
