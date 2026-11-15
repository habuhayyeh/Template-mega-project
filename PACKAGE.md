# PACKAGE — the canonical Doximity run

A stage can only be judged against the package it was given. Two of the three P003 Doximity runs were untestable for standing items because `STANDING_ITEMS.md` was never supplied, and one had no dispatcher at all. This file fixes the package so a run set is actually a set.

## Files

| File | Role |
|---|---|
| `pipeline/05_WRITE_AP.md` | governing instructions |
| `pipeline/AP_ANCHOR.md` | format authority |
| `pipeline/STANDING_ITEMS.md` | closed list of plan items that need no source sentence |
| the frozen Handoff for the run | the only source of clinical content |

All four are attached. Nothing else.

The Handoff must come from a ledger that already excludes what a decision excludes. A decision recorded in `DECISIONS.md` is not visible to `05` and must not be reconstructed there.

## Dispatcher — verbatim, identical for every run in a set

```text
Read 05_WRITE_AP.md and follow it as the governing instructions.
Read AP_ANCHOR.md as the formatting standard.
Read STANDING_ITEMS.md as the closed list of plan items that may appear without a source sentence.
Apply them to the Handoff.
Use only the Handoff for clinical content. The other three files govern form and the permitted plan items; take no facts from them.
Return only the final Assessment and Plan. No explanation, preamble, commentary, or analysis.
```

## What makes a run set a set

- Same four files, byte-identical, for every run.
- Same dispatcher text, verbatim.
- Fresh conversation each time.
- No edits between runs.
- All runs kept raw, including the bad ones, and each scored against the same invariant list.

A run with a different dispatcher is a different experiment. It may be kept as a control — the under-specified call that invented `postictal confusion resolved` is worth keeping for exactly that reason — but it is not a repetition.

## What a run set decides

- **Stability:** do the runs agree on facts, reasoning, plan decisions and placement?
- **Contract:** does each run pass `tools/check_ap.py`?

A run can pass the contract and still differ from its siblings; that is instability, not a breach, and the two need different fixes. A run can match its siblings and still breach the contract; that is a rule that is not being applied, which is what the checker exists to catch.
