# CHANGE_LEDGER — the record of governed changes

Canonical for: **what changed, when, why, and who approved it.**

One line per change. If a change is not here, it is not a governed change — it may still have happened in git, but it is not valid for acceptance.

The root `CHANGELOG.md` belongs to the old pipeline and is not used here.

---

## Format

```text
CHG-id | date | category | target | change | reason | approval
```

Categories come from `CHANGE_CONTROL.md`: `PATCH`, `IMPLEMENTATION`, `DESIGN`, `ACCEPTANCE`, plus two record kinds with no approval path — `SUPERSESSION` and `CLOSURE`.

---

## Entries

```text
CHG-0001 | 2026-11-15 | IMPLEMENTATION | phase0/BUILD_LINT → BUILD_SPEC | renamed; scope narrowed to build integrity | name implied ownership of CHECK | reviewer
CHG-0002 | 2026-11-15 | DESIGN | phase0/REGISTRIES → AUTHORITY_REGISTRY + IMPLEMENTATION_MANIFEST | split by mutation class | registries changed at different rates for different reasons | reviewer
CHG-0003 | 2026-11-15 | DESIGN | phase0/PACKET → ACCEPTANCE_MODEL + CHANGE_LEDGER | split run-level from project-level | a packet is evidence; a ledger is governance | reviewer
CHG-0004 | 2026-11-15 | DESIGN | OBLIGATIONS → COVERAGE_LEDGER | obligations plus corpus coverage | one file, two questions about sufficiency | reviewer
CHG-0005 | 2026-11-15 | ACCEPTANCE | predicate kinds | BUILD_GATE / PROCESS_GATE / SCORER_CONTROL recognised | frozen "one owning submodule" applies to runtime case assertions only | reviewer
CHG-0006 | 2026-11-15 | ACCEPTANCE | FIXTURE_INDEX | predicates moved out of fixtures; rows reference ids | a fixture owning a predicate is an authority leak | reviewer
CHG-0007 | 2026-11-15 | ACCEPTANCE | CASE-07 | historical-source objects may render in plan when adopted | temporality is not adoption | reviewer
CHG-0008 | 2026-11-15 | ACCEPTANCE | CASE-11 | `O51` withdrawn as non-local exemplar | the move was a direct effect of the clause | reviewer
CHG-0009 | 2026-11-15 | ACCEPTANCE | OBL-06, OBL-10 | invariance claims replaced by characterisation | no contract requires package- or paste-order invariance | reviewer
CHG-0010 | 2026-11-15 | ACCEPTANCE | OBL-21 | reproducibility limit removed as a definition | limit is measured by experiment, not assumed | reviewer
```

---

## Rules

1. No entry without an approval where the category requires one.
2. No retroactive editing of an entry. A correction is a new entry referencing the old.
3. An `ACCEPTANCE CHANGE` entry names the old and new expectation, and the evidence that the old one was wrong.
4. A `SUPERSESSION` entry names both packets and never replaces the old verdict.
