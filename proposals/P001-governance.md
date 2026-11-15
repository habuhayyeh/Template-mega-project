# P001 — Governance and workspace

**Status:** approved with execution amendment, 2026-11-14.
**Outcome:** repository layout, ownership, proposal threshold, workflow, precedence, data rule, and migration are recorded in `AGENTS.md`, `PROJECT.md`, `DECISIONS.md`, and the directory structure.

## Amendment carried into execution

The working tree descends from `habuhayyeh/Template-mega-project` `main` at `d4363f0`. No second root history was created. The import is a commit on that history.

## Transport limitation, recorded

This session can read the remote over `https` with `http.sslBackend=openssl` but has no push credentials. Implementation is committed locally and pushed by the user; the reviewer reads the pushed branch. This is a transport constraint, not a governance exception.

## Rejected in v1 and why

`SHA256SUMS` — git already content-addresses; the failure mode was competing canon, not silent bytes. Replaced by the canonical pointer block in `STATUS.md`.

`archive/` on `main` — superseded material belongs in history or a legacy branch, never beside canonical files.
