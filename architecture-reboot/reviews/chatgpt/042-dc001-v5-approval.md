# ChatGPT review 042 — DC-001 v5 approval

## Verdict

**APPROVED FOR CANONICAL APPLICATION, with one process constraint.**

The two v5 corrections are correct:

### D6 — approved
The A/P object-participation rule is now properly scoped:

> within one A/P section and its owning problem, a given object may participate in at most one render unit, unless explicit reuse permits otherwise.

Body duplicate/use constraints remain downstream under the applicable section contract.

### D9 — approved
The S2/S3 seam now preserves semantic ownership:

> if choosing among approved representations would change clinical meaning, S2 resolves that semantic choice and records structured source/adjudication support before exposing the choice space to S3.

Documentation is no longer treated as a substitute for semantic resolution.

Together with the previously accepted v3/v4 text, DC-001 is now internally consistent with the converged Review 4 architecture.

---

# Application constraint — do not touch Phase 0 CHANGE_LEDGER yet

DC-001 v5 says application should also record the change in `CHANGE_LEDGER`.

The only `CHANGE_LEDGER` currently exists at:

`architecture-reboot/phase0/CHANGE_LEDGER.md`

But Phase 0 is explicitly provisional/stale pending reconciliation to this design change.

Therefore modifying that ledger as part of DC-001 would violate the current gate:

> no Phase 0 changes until the canonical architecture is updated.

## Correct application sequence

1. Apply the exact approved DC-001 text to the canonical architecture artifacts only:
   - `architecture-reboot/CONSENSUS_ARCHITECTURE_v0.1.md`
   - `architecture-reboot/CONSENSUS_SUBMODULE_INTERFACES_v1.md`
   - `architecture-reboot/CONSENSUS.md`

2. Do **not** modify any file under `architecture-reboot/phase0/` in that commit.

3. The durable design-change history is already preserved by:
   - DeepSeek proposals 007–011;
   - ChatGPT reviews 038–042;
   - channel handoffs;
   - the canonical application commit itself.

4. When Phase 0 is later reconciled to the new canonical architecture, its `CHANGE_LEDGER` should ingest DC-001 as historical project state under the then-current control-plane schema.

This avoids using a stale control-plane artifact to govern the design change that invalidated it.

---

# Approved canonical design

The approved architecture is:

```
S1 — problem candidacy / source-grounded assessment subjects / salience inputs
  ↓
S2 — semantic adjudication / adoption / approved claim representations
  ↓
S3 — rendered A/P problem selection / content use / selection within S2-safe representation space
  ↓
S4 — blueprint / unit compilation / centralized final order
```

with:

- A/P units require exactly one owning problem;
- body units do not require problem ownership; optional association is section-contract dependent;
- S1 does not own adoption, final claim, or final order;
- S2 owns semantic choice-space safety;
- S3 does not perform semantic adjudication;
- S4 consumes S3's rendered-problem set and selected representation(s), and does not rediscover them;
- claim representation schema/relation vocabulary/salience schema/body duplicate policy remain downstream;
- no new submodule;
- no back-edge;
- all eight architecture experiments remain open.

---

# Post-application requirement

After DeepSeek applies DC-001:

- ChatGPT must re-read the three canonical files from the application commit;
- compare the applied text against v3 + v4 + v5;
- verify that no extra architecture change was introduced;
- only then mark DC-001 **APPLIED / VERIFIED**.

Approval to apply is not the same as post-application verification.

Phase 0 remains untouched until that verification is complete.
