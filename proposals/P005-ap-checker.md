# P005 — fail-only checker for the A/P stage

**Status:** draft, awaiting review. Not implemented.
**Affects:** a new `tools/check_ap.py`, `tests/validator-fixtures/`, `runs/`.
**Does not affect:** any pipeline stage, the substrate, either oracle, the six kinds.

---

## 1. Why this exists

The `05` contract names four invariants it cannot enforce:

1. a line status must come from `COURSE`;
2. a triggered `STANDING_ITEMS` entry must appear;
3. a fact excluded by a permanent decision must not appear;
4. a plan item must stay in the block whose input carried it.

Run1 of the Doximity set walked past the first one and wrote `postictal confusion resolved`. No amount of prose in `05` makes that impossible, because prose is read by the same model that is being checked. The check has to happen after the output exists and be mechanical.

## 2. Shape

`tools/check_ap.py handoff.txt ap.txt [--standing STANDING_ITEMS.md] [--ledger ledger.txt]`

Exit 0 clean, 1 breach, 2 usage. **Fail-only.** It never rewrites, never suggests, never repairs. A note that fails is reviewed and re-run; a checker that silently fixes would be a decision-maker, which is not its job.

## 3. Checks that are genuinely mechanical

| # | Check | How |
|---|---|---|
| C1 | **Unsupported line status** | Extract the final comma-segment of each `//` line. If it matches a status vocabulary — `resolved`, `improved`, `unchanged`, `worse`, `returned to baseline` — require the same phrase in a `COURSE` entry of that block. Otherwise breach. |
| C2 | **Required standing item** | For each entry in `STANDING_ITEMS.md`, test its trigger against the block's `PRIMARY_CLAIM` using the trigger's literal terms. If satisfied, require a line in `Plan:` whose words come from that item. |
| C3 | **Block ownership of plan items** | Every plan line must trace to a `MANAGEMENT` entry in the same block, or to a standing item. A line whose words appear only in another block's `MANAGEMENT` is a breach. |
| C4 | **Forbidden IDs** | Given a ledger, a fact whose text appears in a `DISCARD` entry but in no retained entry must not appear in the output. Catches the O54 case without `05` ever knowing D-014. |
| C5 | **Exact duplicate plan items** | Two plan lines identical after casefold, punctuation and whitespace normalisation. |
| C6 | **Deterministic repeated proposition** | Two bullets in one block whose normalised token sets are equal, or where one is a prefix of the other with the same head noun. Exact and near-exact only; semantic duplication is out of scope. |
| C7 | **Management in a bullet** | A bullet whose words trace to a `MANAGEMENT` entry and not to an `EVIDENCE` entry. |

## 4. What it deliberately does not check

- Whether a bullet "materially supports" the claim. That is judgement, and a checker that guesses it would produce false failures that train us to ignore it.
- Whether two reasoning propositions are distinct.
- Whether a status is clinically correct — only whether the Handoff contains it.
- Spelling, style, ordering.

A checker that over-reaches gets switched off. Every check above is decidable from the files without interpreting medicine.

## 5. Fixtures

Each check needs a known-bad file that must fail with a specific message, and the accepted run that must pass. Without fixtures the checker proves nothing — the same rule that applies to `check_sections.py`.

Minimum fixtures:

- a line status absent from `COURSE` (the run1 fabrication, reduced to two lines);
- a satisfied trigger with the item missing;
- a plan line borrowed from the other block;
- a bullet quoting a discarded object;
- a duplicated plan line.

## 6. What it changes about acceptance

The three-run protocol keeps its invariants, but a run that passes the checker and still differs from its siblings is a stability failure, not a contract breach. The two failures need different fixes, and today they look the same.

## 7. Order of work

1. Regenerate the baseline Handoff from a ledger that already excludes O54, so C4 has nothing to catch on the accepted case.
2. Build the checker with fixtures.
3. Re-run the package: `05`, `AP_ANCHOR`, `STANDING_ITEMS`, Handoff, one dispatcher, three times.

The checker is not a substitute for the input fix in step 1. It catches what the input cannot express; it does not license leaving contradictions in the input.

## Out of scope

Any change to `05`, the anchor, the substrate, the oracles, `06`, `07`, and any semantic scoring.
