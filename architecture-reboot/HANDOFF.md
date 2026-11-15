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

- **You (DeepSeek)** — primary engineer / co-engineer: propose architecture first by default, implement substantial work, run builds/validators, report with counts and hashes, and independently review bounded ChatGPT implementation patches.
- **ChatGPT** — architect/reviewer of record + bounded implementation maintainer: challenges design and diffs, writes its own reviews, and may directly patch localized implementation defects when the accepted contract/tests make the correction unambiguous.
- **Signer (the user)** — final authority on clinical, stylistic, product, architectural, and governance decisions.

| path | owner |
|---|---|
| `architecture-reboot/proposals/deepseek/`, `reviews/deepseek/` | you |
| `architecture-reboot/channel/to-chatgpt.md` | you (append your handoff) |
| `architecture-reboot/proposals/chatgpt/`, `reviews/chatgpt/`, `channel/to-deepseek.md` | ChatGPT |

**Everything durable goes in the repo.** Chat is not state. Every turn that changes files ends with a
channel handoff naming the commit, the changed files, the counts, and what is still open.

**Implementation exception:** coordination/review paths remain single-writer, but implementation is no
longer DeepSeek-only. When ChatGPT finds a bounded implementation defect whose correction is already
determined by the accepted contract, it may patch the code directly, add/adjust tests, commit, and send
you the exact commit for independent review. Treat that patch as reviewable code, not as self-validating.
Broader/new implementation remains DeepSeek's default responsibility. Neither agent silently changes
architecture, frozen interfaces, predicate semantics, experiment hypotheses, oracle semantics, or
clinical/style/product policy through an implementation patch.

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

- **Execution package:** source contract accepted after review 081; review 082 corrected only the
  scorer-input boundary. The package is source-first and regenerable.
- **Scorer/harness/preflight:** implemented and **CLOSED under D-019** after independent review.
  `python architecture-reboot/tools/preflight.py` passes with 7/7 checks and 42 tests.
  **Gate 0:** unrun; the three-independent-human-review prerequisite is outstanding.
  **Doximity:** unrun. **Phase 0:** untouched and stale.

## 5. Exact position

HEAD at handoff: see `git log -1`. Last substantive commit: review-083 fixes plus the D-019 preflight.

`python architecture-reboot/tools/make_seeds.py` builds:
5 clean parents across 4 parent types → 28 seeds → `MANIFEST.json`. **A second run must produce zero
diff**; that is a build failure condition, not a warning. The build also checks every seed is a real
non-noop mutation and differs from its parent at exactly one declared path; 28/28 are checked, with 0
no-op and 0 multi-diff seeds. The manifest records the checked before/after values and the
dependency-context map.

`python architecture-reboot/tools/preflight.py` is the single mechanical entry point. It checks frozen
architecture/Phase-0 drift, source/generated freshness and determinism, governing hashes and
identities, active registry, dependency-context integrity, seed mutation integrity, stale source
markers and the scorer/unit tests. Current result: **PASS**, 7 checks, 42 tests.

Current counts: 5 clean calibration parents · 4 parent types · 28 seeds · 16 active predicates ·
campaign `GATE0-C1` · registry `PILOT-2` · active set `ACTIVE-PILOT-2` · schema `SCHEMA-2` · oracle
`ORACLE-2.0` · reason registry `REASON-1` · operator set `PILOT-OPERATORS-1`.

Parent identities: `S1_CASE01_CLEAN`, `S2_CASE01_CLEAN`, `S3_CASE01_RENDERED_CLEAN`,
`S3_CASE01_NOT_RENDERED_CLEAN`, `S4_CASE01_CLEAN`.

Scorer: 13 mechanical predicates + 3 human-review predicates; 42 synthetic tests; no Gate 0 acceptance
run.

## 6. Review 083 fixes and D-019 preflight

**Input boundary.** Scorer input is target artifact + read-only dependency context + oracle + frozen
predicate/contract rules. `00-GATE0-MANIFEST.md` fixes the dependency matrix; the manifest hash-pins the
clean, seed-independent context. The scorer evaluates only the target `parent_type`.

**Review-083 fixes.** The harness now recomputes every governing hash, checks the frozen campaign
identities and the scorer registry's active set before packets/acceptance, and rejects a stale manifest.
Generator and scorer share one pure `projection_contract.py`. Clean-parent verdicts distinguish
`FAIL`/`INCOMPLETE`/`PASS`. Judgments are bound to packet + predicate; stale or mismatched records fail.
Evidence records the dependency hashes actually supplied and the implementation fingerprints. Parent-type
and campaign verdicts are written to `EVIDENCE.json`.

**Scorer/harness.** `architecture-reboot/scorer/` contains the pure scorer, predicate registry and
projection adapter. `architecture-reboot/tools/gate0_harness.py` owns the answer key, packet generation,
specificity, human-judgment aggregation and immutable evidence. The scorer does not open files or read
the manifest; a test patches `builtins.open` to prove it.

**D-019 preflight.** `architecture-reboot/tools/preflight.py` consolidates the recurring mechanical
checks without adding acceptance criteria: frozen zones, regeneration/freshness/determinism, governing
hashes/identities/registry, dependency context, seed mutation integrity, stale markers and unit tests.
It exits non-zero on any failure and does not run Gate 0.

**Gate 0 remains unrun.** 42 synthetic tests pass. No `acceptance` harness run was executed, no
judgments were fabricated, and the three-independent-human-review prerequisite is outstanding.

No Doximity, no Phase 0.

## 7. Working rules that matter

**Efficiency protocol:** classify findings as ARCHITECTURE / CONTRACT / IMPLEMENTATION / NONBLOCKING;
review the changed diff plus its dependency cone rather than re-auditing the whole project; stop a layer
once its contract is satisfied, validators pass and evidence is reproducible; reopen only on new evidence.
Implementation handoffs use `COMMIT / TYPE / CHANGED / INVARIANTS / VALIDATION / BLOCKERS / NEXT`.
Prefer asymmetric work: DeepSeek handles substantial/new implementation and local execution; ChatGPT
handles adversarial review, invariant/test design and bounded direct fixes; the non-author reviews the
actual diff. Consolidate recurring mechanical checks behind one preflight entry point before broad review
or acceptance. Human/semantic prerequisites block semantic acceptance, not safe mechanical preparation.

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

The scorer/harness/preflight implementation layer is closed. Do **not** reopen it without new evidence
(a failing test, counterexample, implementation result, or genuine contradiction).

Gate 0 acceptance remains blocked by the requirement for three independent blinded human judgments.
Safe mechanical preparation, including blinded packet generation, may proceed if authorized, but no
acceptance verdict may be claimed without the required human judgments.

No Doximity or Phase 0 work is authorized by this closure.
