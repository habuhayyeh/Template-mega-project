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

- **Execution package:** rebuilt, source-first, but the source contract is **not accepted** by review.
- **Scorer:** not built. **Gate 0:** unrun. **Doximity:** unrun. **Phase 0:** untouched and stale.

## 5. Exact position

HEAD at handoff: see `git log -1`. Last substantive commit: generator constructs `S4_INPUT_VIEW`.

`python architecture-reboot/tools/make_seeds.py` builds the package:
4 layer-specific parents → 27 seeds → `MANIFEST.json`. **A second run must produce zero diff**; that is
a build failure condition, not a warning.

Current counts: 4 clean parents · 27 seeds · 16 active predicates · campaign `GATE0-C1` ·
registry `PILOT-2` · active set `ACTIVE-PILOT-2` · schema `SCHEMA-2` · oracle `ORACLE-2.0`.

## 6. The four open blockers (review 078)

1. **Exact nested source→destination path map** for `S4_INPUT_VIEW`. Group-level only today; the
   reviewer wants per-field provenance, e.g. `from_s2.members[i] ← S2.representations[0].members[i]`.
2. **Gate 0 procedure still says "unrelated family"** in body/pass-criteria while the header says
   `FULL_SILENCE-WITHIN-LAYER`. Align every occurrence.
3. **S3 reason registry missing**: no `reason` vocabulary, no reason→basis requirement map, no valid
   basis target type. Schema example and generator use different labels. Needs a clean `NOT_RENDERED`
   parent so equality / reason / basis seeds stop overlapping.
4. **Parent identity tracking**: adding a second S3 parent means more than four parents across four
   types; track parent identity separately from parent type.

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

## 8. Your task

Close blockers 1–4 as source edits, regenerate twice with zero diff, and hand off in
`channel/to-chatgpt.md` with: commit hash, changed-file list, parent count by type, active predicate
count, seed count per predicate, pending predicates, identities, governing hashes, and explicit
confirmation that no scorer exists.

Then stop. The reviewer inspects the source contract before any scorer is written.
