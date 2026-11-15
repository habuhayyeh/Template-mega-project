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

Every DeepSeek turn uploads its `NEXT` to `channel/to-chatgpt.md`; that handoff is addressed to the
reviewer, not the signer. The user-facing reply reports the state and the upload, not a task for the
signer. Surface a signer decision directly only when `channel/to-deepseek.md` or a review asks the
signer to decide.

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

- **Execution package:** source contract rebuilt under D-023/D-024 as `SCHEMA-3`; review 081/082
  remain the architecture and scorer-input boundary. The package is source-first and regenerable.
- **Scorer/harness/preflight:** implemented and **CLOSED under D-019** after independent review.
  `python architecture-reboot/tools/preflight.py` passes with 7/7 checks and 46 tests.
  **Gate 0:** unrun; the signer reference + two blinded evaluator judgments have not been executed.
  **Doximity:** unrun. **Phase 0:** untouched and stale.

## 5. Exact position

HEAD at handoff: see `git log -1`. Last substantive commit: CASE-01 SCHEMA-3 rebuild under D-023/D-024.

`python architecture-reboot/tools/make_seeds.py` builds:
5 clean parents across 4 parent types → 28 seeds → `MANIFEST.json`. **A second run must produce zero
diff**; that is a build failure condition, not a warning. The build also checks every seed is a real
non-noop mutation and differs from its parent at exactly one declared path; 28/28 are checked, with 0
no-op and 0 multi-diff seeds. The manifest records the checked before/after values and the
dependency-context map.

`python architecture-reboot/tools/preflight.py` is the single mechanical entry point. It checks frozen
architecture/Phase-0 drift, source/generated freshness and determinism, governing hashes and
identities, active registry, dependency-context integrity, seed mutation integrity, stale source
markers and the scorer/unit tests. Current result: **PASS**, 7 checks, 46 tests.

Current counts: 5 clean calibration parents · 4 parent types · 28 seeds · 16 active predicates ·
campaign `GATE0-C2` · registry `PILOT-2` · active set `ACTIVE-PILOT-2` · schema `SCHEMA-3` · oracle
`ORACLE-3.0` · reason registry `REASON-1` · operator set `PILOT-OPERATORS-1`.

Parent identities: `S1_CASE01_CLEAN`, `S2_CASE01_CLEAN`, `S3_CASE01_RENDERED_CLEAN`,
`S3_CASE01_NOT_RENDERED_CLEAN`, `S4_CASE01_CLEAN`.

CASE-01: two rendered problems — falls and a retained inactive infarct; the S1-CAND seed is now a
medication-only candidate. Scorer: 13 mechanical predicates + 3 semantic signer-reference predicates; 46 synthetic tests; no Gate 0 acceptance
run. Packet preparation: 33 records, 16 semantic packets, 0 references/0 evaluators. These packets are
**blocked for evidence collection** by review 089 answer-key leakage; see proposal 014. Index at
`architecture-reboot/runs/gate0-packets-c2/INDEX.md`.

## 6. Review 084 closure: scorer/harness/preflight

**Review 084 closes the implementation layer under D-019.** No implementation blocker remains. Do not
reopen it without a failing test, counterexample, implementation result or genuine contradiction.

**Option F policy (signer-approved D-021).** Semantic Gate 0 uses one signer/clinician reference
judgment followed by two blinded LLM evaluator judgments. The signer reference is the accepted verdict;
both evaluators must match it and within-layer specificity. Mismatch is FAIL; missing, duplicate or UNDECIDABLE evidence is INCOMPLETE. References are reusable while packet/policy/oracle/context identity is
unchanged; evaluator evidence is reusable only for the same model family/version. Project-context agents
are ineligible. The harness records `REFERENCE` and `EVALUATOR` roles separately. All pre-D-023
references from `gate0-packets-c1` are invalid after the SCHEMA-3 rebuild.

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

**Gate 0 remains unrun.** 46 synthetic tests pass. No `acceptance` harness run was executed, no
judgments were fabricated, and the signer reference + two blinded evaluator judgments have not been executed.

No Doximity, no Phase 0.

## 7. Working rules that matter

**Sync shorthand.** `.` / `sync` means refresh live state and continue already-authorized work; it
does not itself approve a pending proposal. Option F is separately and explicitly signer-approved.

**Signer-review presentation.** Semantic signer packets are presented in clinician-readable form:
(1) short case summary using only packet-visible facts; (2) the exact rule in plain language; (3)
the question **“Is there a violation?”**; (4) a brief example of what would count as a violation when
helpful. The signer answers `Yes / No / Cannot determine`; the harness mapping is
`Yes -> FIRED`, `No -> SILENT`, `Cannot determine -> UNDECIDABLE`. The presentation must not
reveal seed/clean status, expected verdict, mutation metadata, or answer-key fields.

**No status-only updates.** Every sync, review, closure, handoff, and user-facing project update must
end with a concrete `NEXT`: the next task/decision, responsible actor when relevant, and—if blocked—
the exact unblock action. Even when no new work landed, state the next authorized action. Closing one
layer must immediately identify the next dependency. If signer input is required, ask the narrow
decision and give a recommendation; otherwise proceed with the next authorized task.

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

Gate 0 acceptance requires one signer/clinician reference and two blinded LLM evaluator judgments under Option F.
Safe mechanical preparation, including blinded packet generation, may proceed if authorized, but no
acceptance verdict may be claimed without the required reference and evaluator evidence.

No Doximity or Phase 0 work is authorized by this closure.

## Signer-discovered CASE-01 contract correction

D-023: a major established primary neurologic diagnosis may retain its own A/P problem even when
inactive and without current management; inactivity changes rendering depth to shorter/condensed rather
than causing automatic omission. This partially supersedes D-015.

Blinded Gate-0 signer Packet 7 exposed a CASE-01 oracle defect: the current oracle/seed incorrectly
treats prior left MCA infarct candidacy as a violation. Gate-0 acceptance is paused pending a controlled
CASE-01 source-contract rebuild. Architecture remains closed unless that rebuild proves the
adoption-vs-retention distinction impossible.

**NEXT:** DeepSeek rebuilds CASE-01 clean parents/seeds under D-023, regenerates, runs preflight and
packets mode only, and returns the diff for ChatGPT review.

## Review 090 governance correction + packet-blinding status

D-026 is void. Verified interaction history shows no explicit SCHEMA-3 approval; the signer sent only
`.`, which D-022 defines as sync only. SCHEMA-3 therefore remains **provisional**, despite the existing
implementation and reported 46-test/preflight PASS.

Proposal 014 is technically accepted by ChatGPT in principle, but still requires explicit signer
approval before implementation. The current semantic packet set remains blocked because it exposes
answer-key fields.

The remaining blockers are explicit signer approval of SCHEMA-3 and Proposal 014. S1-CAND packets expose
`candidate_concepts_must_exclude`, and S2-ADOPT packets expose `expected.adoption`. These are
answer-key fields and violate Option F. `proposals/deepseek/014-semantic-packet-blinding.md` proposes
the smallest governed correction, including `REVIEW-POLICY-F-2`.

**NEXT:** ChatGPT routes proposal 014 to the signer; after approval, DeepSeek removes semantic
`oracle.expected`, regenerates packets and restarts reference collection. No references or Gate-0
acceptance from the current packet set.

## Governance dispute resolved

Review 091 rechecked the prior interaction history specifically for the SCHEMA-3 approval request.
The signer sent only `.`; no explicit SCHEMA-3 approval exists. D-027 stands and D-026 is not carried
forward. SCHEMA-3 remains technically implemented but provisional.

The action-channel rule in commit `cfcbbf2` is accepted: DeepSeek sends `NEXT` to ChatGPT, and ChatGPT
decides whether signer interruption is necessary.

Proposal 014 remains reviewer-approved in principle but not signer-approved.

**NEXT:** ChatGPT owns the signer escalation for the two pending contract decisions; DeepSeek takes no
further contract action until an explicit decision is recorded.
