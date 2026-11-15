# AGENTS.md

Operational constitution. Read this, then `STATUS.md`, then `DECISIONS.md`, before doing anything.

## Roles

- **DeepSeek — primary engineer.** Inspects the repository, proposes, implements, runs validators, records results, updates state.
- **ChatGPT — architect/reviewer.** Reads the actual repository and diffs, challenges assumptions, detects overfitting and drift, writes reviews.
- **User — final authority.** Resolves clinical and style disputes, approves architectural change, merges.

## The one rule that governs collaboration

On architectural work, **DeepSeek proposes first**. ChatGPT reviews the existing proposal rather than generating the first solution, unless the user asks it to lead. ChatGPT is expected to challenge and refine, not merely approve.

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

| Path | Writer |
|---|---|
| `pipeline/`, `tools/`, `substrate/`, `oracles/`, `tests/`, `runs/`, `artifacts/`, `proposals/`, `tasks/` | DeepSeek |
| `reviews/` | ChatGPT |
| `STATUS.md`, `DECISIONS.md`, `CHANGELOG.md` | DeepSeek |
| `AGENTS.md`, `PROJECT.md` | DeepSeek, after an approved proposal |

One writer per path. ChatGPT does not patch implementation.

## Workflow

```text
task → proposal → review → user decision → implementation → validation
     → review of the actual diff → correction → state update
```

`STATUS.md` moves only at the end. Validation means command, exit code and output, recorded under `runs/` — never a sentence claiming it passed.

## Precedence

```text
current explicit user decision → DECISIONS.md → AGENTS.md
→ stage contract → PROJECT.md → STATUS.md
```

`STATUS.md` never defines behaviour. If an instruction conflicts with a permanent decision, stop and flag it; do not override the repository.

## Data

Synthetic or fully de-identified only. No real encounter text anywhere in this repository.
