# DESIGN CHANGE LEDGER

Record of design changes against the canonical architecture documents. Separate from Phase 0, which is stale and does not govern the architecture.

| id | date | change | applied in | status |
|---|---|---|---|---|
| DC-001 | 2026-11-15 | S1–S4 responsibilities, A/P-scoped problem ownership, claim representations | `f33faf1`, corrective `908acfd` | APPLIED / VERIFIED |
| DC-002 | 2026-11-15 | candidate partition authority, candidate accounting (`S3-CAND-01`), relevance-based `S4_INPUT_VIEW` (`S4-PROJ-01`), weak-R2 bridge boundary, `management_reference_spans[]` | `a856e39` + corrective `fc9385a` + cleanup `b3d5d6f` | APPLIED / VERIFIED |

## DC-002 follow-ons

- `S3-CAND-01` and `S4-PROJ-01` added to `experiments/architecture/AX-S1S2-D/predicates.md`.
- AX schema, CASE-01 parent, active-predicate set, Gate 0 seed corpus, generated artifacts and campaign identity hashes are **STALE / PENDING REGENERATION**.