# Architect

Architecture-only workspace for this project.

This directory is for recommendations, maps, contracts and design decisions. It is not runtime code, not
a Gate-0 artifact, and not an implementation branch.

## Rules

1. Only this `architect/` directory is committed by the architect role.
2. Do not edit `architecture-reboot/`, `scorer/`, `experiments/`, `proposals/`, `channel/`, `runs/` or
   `DECISIONS.md` from here.
3. Architecture recommendations are advisory until the signer or the authorized reviewer adopts them.
4. No patient data. No generated notes. No acceptance evidence.
5. A recommendation that changes runtime behavior must be handed off explicitly; this directory does not
   implement it.

## Current documents

- `CURRENT-MAP.md` — adopted three-layer architecture map.
- `recommendations/001-ingestion-evidence-ledger.md` — ingestion boundary and Evidence Ledger contract.
- `recommendations/002-a-contract-repair.md` — repair A; source registry, assertion domain, evidence
  state and action lane.
- `recommendations/003-next-structural-step.md` — earlier decision; superseded on A polarity.
- `recommendations/004-revised-next-step.md` — patch B threshold, quarantine A polarity, gate C.
- `recommendations/005-b-relationship-contract.md` — patch B relationships before C; no C run yet.

## Status

No Gate-0 acceptance. No Doximity production change. No Phase 0.
