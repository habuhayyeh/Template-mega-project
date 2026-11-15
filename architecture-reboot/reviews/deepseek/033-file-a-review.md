# DeepSeek review — File A interpret/reconcile

**Reviewed:** `01-INTERPRET-RECONCILE.md`, review 135.
**Status:** architecture review; no implementation.

## Verdict

**Accept the contract with two field corrections.** The boundary test passes: one falls unit, one
historical stroke unit, unmapped `SPK2`, no count, no causality, no problem/role/section/action/prose.

The two defects are field semantics, not architecture.

## Defect 1 — `certainty` is carrying attribution

The contract defines `certainty` as the source-supported qualifier (possible, likely, suspected,
uncertain, unstated). The test output uses:

```text
certainty=reported
certainty=documented
```

`reported` and `documented` are source/attribution status, not certainty. They belong in `attribution`
or `kind`, not `certainty`.

Correct:

```text
U001 certainty=unstated
U002 certainty=unstated
```

If the source says “possible,” “likely,” “suspected,” or “unlikely,” use that. Otherwise use `unstated`.
Do not encode “patient-reported” as lower certainty; that is attribution.

## Defect 2 — `relation=same_state` asserts more than the source

T001 and P1.001 both describe falls, but the packet does not establish that they came from the same
reporter or the same event. The output already records that uncertainty in `UNRESOLVED`.

Use:

```text
relation=possible_overlap
```

for the falls unit. Keep both refs and the unresolved attribution issue. Do not use `same_state` unless
the source establishes the same state/reporter.

## What is right

- sparse units, not a fact corpus;
- record ID + selector + role;
- no candidate-problem decision;
- no problem/role/section/plan/prose;
- historical stroke stays historical;
- unmapped speaker stays unmapped;
- no count aggregation;
- no causality;
- action lane absent when no action exists;
- unresolved provenance preserved.

## Next step

Fix only the two fields above, re-run the same three-record test, and stop. Expected:

- `U001 certainty=unstated`, `relation=possible_overlap`;
- `U002 certainty=unstated`;
- same refs, same unresolved note, no new unit.

Do not build B or C yet. Do not add new fields.

No Gate-0 acceptance. No Doximity production change. No Phase 0.
