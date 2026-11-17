# In-prompt handoff — strict contract

**Evidence class:** REPRODUCED
**Date:** 2026-11-16
**Scope:** Passing D-S output into D-T inside one Doximity prompt.

## Finding

A strict handoff works when Stage A carries the full payload plus a sentinel, and Stage B is forbidden from
reading the original facts.

Three runs produced identical Stage A JSON and identical Stage B lines. The `[A]` sentinel appeared in every
Stage B line.

## First test was inconclusive

The first handoff prompt allowed Stage B to use `FACTS`. Stage A lost IDs in some runs, yet Stage B still
produced correct labels and IDs. That proved Stage B reread `FACTS`, not that the handoff failed.

It also had no exact Stage A schema, so array-of-sections and array-of-objects could both be called valid.

## Strict contract

1. Define the exact Stage A schema. Do not say “sections JSON.”
2. Stage A carries every field Stage B needs: `id`, `section`, `order`, `kind`, label/chronology/target/topic.
3. Stage A adds a sentinel value, e.g. `sentinel: "[A]"`.
4. Stage B may use **only** Stage A. It may not read `FACTS`.
5. If a value is missing, Stage B returns `HANDOFF_ERROR`; it does not fill from memory.
6. Stage B order follows Stage A `order`, not section grouping.
7. The test’s expected output must follow the same rule.

## What was proven

For the fixed fixture:

- Stage A exact JSON, three runs;
- Stage B six lines, three runs;
- every line carried `[A]`;
- order followed `P001`, `CU001`, `CU002`, `CU003`, `AV001`, `X001`.

This proves the prompt can pass data from Stage A to Stage B without rereading facts.

## Limits

- Small fixed fixture, not the real packet.
- Labels were stable because they were fixed in `FACTS`.
- This does not prove synthesis determinism.
- A missing sentinel is the failure signal; a correct-looking line without `[A]` means Stage B cheated.

## Test file

`../experiments/ask/DOXIMITY-HANDOFF-TEST-V2.md`
