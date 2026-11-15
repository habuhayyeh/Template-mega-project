# P002 — A/P assembly and rendering corrections

**Status:** proposed. Awaiting architectural review.
**Affects:** `pipeline/04_ASSEMBLE.md`, `pipeline/05_WRITE_AP.md`.
**Does not affect:** the substrate, either oracle, `01`, `02`, `03`, `06`, `07`, or the six kinds.

## Problem

The last full run (`runs/2026-11-14-04-05/`) produced an A/P that is better attributed than the previous one and still wrong in five specific ways, all inside `04` and `05`.

## Evidence

| # | Observed | Cause |
|---|---|---|
| 1 | O32 `family's concern about her memory` was deleted as a subset of O34 `… is not today's issue`; the A/P now names a concern it never states | `04` §2 treats a subset as a duplicate |
| 2 | O16 `fluid restriction` was deleted as a subset of O46 `fluid restriction started`; the plan kept the completion statement and lost the order | same |
| 3 | both problem lines begin lowercase (`//post-…`) | `05` has no capitalisation rule |
| 4 | one piece of reasoning rendered as three bullets, two of them saying the MRI will tell us | `05` renders `CLAIM_QUALIFIER` entries one per bullet |
| 5 | `not driving until six months` and `not driving for six months — not negotiable` appear as two plan bullets | no plan-deduplication rule |
| 6 | `no further workup (prior neurology, 2025-06)` sits in today's plan | prior-record management rendered as a current plan item |

## Proposed change

**`04` §2 — duplicate means the same assertion, not a contained one.** Delete an entry only when it asserts the same fact as another retained entry. A subset that adds a distinct proposition (`fluid restriction` versus `fluid restriction started`; a concern versus a statement about that concern) is retained.

**`05` — four rendering rules:**

1. Capitalise the first word of each problem line after `//`.
2. `CLAIM_QUALIFIER` entries that overlap are merged into one reasoning bullet, placed last before `Plan:`. Distinct qualifiers stay separate.
3. One plan bullet per fact. Where two entries state the same decision, keep the fuller and drop the other.
4. A management entry dated to a prior record is not a current plan item. It is not rendered at all unless it is a standing instruction still in force.

## Validation plan

1. `python tools/check_sections.py substrate/acceptance_v2.txt oracles/section_ledger_v2.txt` — unchanged, must stay PASS.
2. Rerun `04` → `05` on `tests/acceptance/seizure_case/ap_handoff_input.txt` with the corrected ledger; record both outputs under `runs/`.
3. Score the A/P against `pipeline/AP_ANCHOR.md`: lowercase gone, one reasoning bullet, no duplicated plan fact, no prior-record plan item, O32 and O16 present.

## Risk

Merging qualifiers can lose a distinct proposition. Mitigation: merge only entries that assert the same thing; the rule is overlap, not co-location. The rerun is scored against the anchor, and any lost proposition is recorded rather than accepted.

## Out of scope

The 14-bullet problem is already fixed by the `03` evidence rule imported in `import/v2`. This proposal does not revisit it.
