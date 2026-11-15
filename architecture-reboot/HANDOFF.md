# Handoff — start here in a new chat

You are the **primary implementation engineer** on a neurology note-generation system. This file is
self-contained; do not assume any prior conversation.

---

## 1. The project

Turn an encounter (recording/transcript, dictation, prior records) into one source-faithful clinical
note. The architecture was rebuilt from scratch; the old pipeline on `main` is evidence, not a
requirement.

**Repository:** `github.com/habuhayyeh/Template-mega-project`
**Branch:** `architecture-reboot-v2` (work here; `main` is history)
**Local clone:** `C:\Users\hussa\OneDrive\Documents\deepseek new\Template-mega-project`

## 2. Roles and channels

- **You** — engineer: write the artifacts, run the build, report with counts and hashes.
- **ChatGPT** — reviewer/architect of record. You do not edit its paths.
- **Signer (the user)** — final authority on anything clinical, stylistic or product.

| path | owner |
|---|---|
| `architecture-reboot/proposals/deepseek/`, `reviews/deepseek/` | you |
| `architecture-reboot/channel/to-chatgpt.md` | you (append your handoff) |
| `architecture-reboot/proposals/chatgpt/`, `reviews/chatgpt/`, `channel/to-deepseek.md` | ChatGPT |

**Everything durable goes in the repo.** Chat is not state. Every turn that changes files ends with a
channel handoff naming the commit, the changed files, the counts, and what is still open.

Git: `git add -A && git commit -m "…" && git pull --rebase && git push origin architecture-reboot-v2`

## 3. What is frozen

- **Architecture** — `CONSENSUS_ARCHITECTURE_v0.1.md`, `CONSENSUS_SUBMODULE_INTERFACES_v1.md`, `CONSENSUS.md`.
- **DC-001** and **DC-002** — both APPLIED / VERIFIED. See `DESIGN_CHANGE_LEDGER.md`.
  Do not reopen without a new counterexample.
- **Experiment program** — `experiments/architecture/00-ARCHITECTURE-EXPERIMENT-PROGRAM.md`.
  Status **SPECIFICATION FROZEN / UNRUN**. Eight experiments, all unrun.

Pipeline shape: `INGEST (I1–I4) → STRUCTURE (S1–S4) → RENDER (R1–R3)`, all inside one Doximity Ask call.
S1 proposes problem candidates and owns the partition; S2 adjudicates adoption and claim relations and
approves claim representations; S3 selects and accounts; S4 compiles the blueprint and owns order.

## 4. What is stale / unbuilt

- **Execution package:** source-first rebuild now carries an executable projection map, a frozen
  experiment-local reason registry, and a clean NOT_RENDERED S3 parent. The source contract is
  **pending independent review**; do not call it accepted.
- **Scorer:** not built. **Gate 0:** unrun. **Doximity:** unrun. **Phase 0:** untouched and stale.

## 5. Exact position

HEAD at handoff: see `git log -1`. Last substantive commit: review-078 four-blocker source pass.

`python architecture-reboot/tools/make_seeds.py` builds:
5 clean parents across 4 parent types → 27 seeds → `MANIFEST.json`. **A second run must produce zero
diff**; that is a build failure condition, not a warning. The build also checks every seed is a real
non-noop mutation and differs from its parent at exactly one declared path; 27/27 are checked, with 0
no-op and 0 multi-diff seeds. The manifest records the checked before/after values.

Current counts: 5 clean calibration parents · 4 parent types · 27 seeds · 16 active predicates ·
campaign `GATE0-C1` · registry `PILOT-2` · active set `ACTIVE-PILOT-2` · schema `SCHEMA-2` · oracle
`ORACLE-2.0` · reason registry `REASON-1` · operator set `PILOT-OPERATORS-1`.

Parent identities: `S1_CASE01_CLEAN`, `S2_CASE01_CLEAN`, `S3_CASE01_RENDERED_CLEAN`,
`S3_CASE01_NOT_RENDERED_CLEAN`, `S4_CASE01_CLEAN`.

## 6. Review 078 four-blocker pass — addressed, pending review

**Review 079 regression is closed.** The mutation function now runs for every parent type; the build
rejects a no-op copy and any seed whose actual diff does not match exactly one declared path. The
manifest mutation record is derived from the checked diff.

1. **Exact S4 source map.** `schema.md::PROJECTION_MAP` freezes destination, owner, source path,
   selector, requirement and transform for all 14 mapped rules. `make_seeds.py` reads the block and
   constructs `S4_INPUT_VIEW`; `S4_PARENT.json` carries no projection.
2. **Gate 0 specificity.** `00-GATE0-MANIFEST.md` now uses `FULL_SILENCE-WITHIN-LAYER` in the model,
   seed requirement, procedure and pass criteria.
3. **S3 reason registry.** `schema.md::REASON_REGISTRY` freezes `REASON-1`, the reason→basis map, the
   `object` basis target type, non-empty and reference-existence rules. `S3_CASE01_NOT_RENDERED_CLEAN`
   is the valid reference; equality/reason/basis seeds derive from it.
4. **Parent identity.** Every parent carries `parent_id`; the manifest keys `clean_parents` by identity
   and counts types separately from parents.

No scorer, no Gate 0 run, no Doximity, no Phase 0.

## 7. Working rules that matter

- **Never claim a fix is applied without reading the file back.** A dedupe guard whose marker was an
  empty string silently skipped every append once; a file-truncating bug turned a 75-line file into 5
  because `open(w).write(open(r).read())` evaluates the write first. Read → transform in memory →
  write → re-read → verify counts and headings.
- **Source vs generated.** `parents/*.json`, `oracle.json`, `schema.md`, `predicates.md`,
  `G0-SEEDS.md`, `make_seeds.py` are **source**. `seeds/generated/*` is **generated** and never
  hand-edited; if it is wrong, fix the generator and rerun.
- **One mutation per seed, one owning predicate**, silence measured within a layer.
- **Evidence is a path**, not a recollection. Fixtures without a citable path stay provisional.
- **No self-attested totals**; the manifest derives counts.
- Hashes: SHA-256 over file bytes for governing source, over canonical JSON for artifacts.
- Do not edit `phase0/CHANGE_LEDGER.md` — Phase 0 is a stale control plane and does not govern the
  architecture. Design changes go in `DESIGN_CHANGE_LEDGER.md`.

## 8. Next

The reviewer inspects the source contract before any scorer is written. Do not build the scorer, run
Gate 0, or touch Doximity/Phase 0 in this pass.
