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

- **Execution package:** source contract rebuilt under D-023/D-024 as `SCHEMA-4`; review 081/082
  remain the architecture and scorer-input boundary. The package is source-first and regenerable.
- **Scorer/harness/preflight:** implemented and **CLOSED under D-019** after independent review.
  `python architecture-reboot/tools/preflight.py` passes with 7/7 checks and 46 tests.
  **Gate 0:** unrun; one signer reference is recorded and two blinded evaluator judgments are outstanding.
  **Doximity:** unrun. **Phase 0:** untouched and stale.

## 5. Exact position

HEAD at handoff: see `git log -1`. Last substantive commit: CASE-01 SCHEMA-4 rebuild under D-023/D-024.

`python architecture-reboot/tools/make_seeds.py` builds:
6 clean parents across 4 parent types → 36 seeds → `MANIFEST.json`. **A second run must produce zero
diff**; that is a build failure condition, not a warning. The build also checks every seed is a real
non-noop mutation and differs from its parent at exactly one declared path; 36/36 are checked, with 0
no-op and 0 multi-diff seeds. The manifest records the checked before/after values and the
dependency-context map.

`python architecture-reboot/tools/preflight.py` is the single mechanical entry point. It checks frozen
architecture/Phase-0 drift, source/generated freshness and determinism, governing hashes and
identities, active registry, dependency-context integrity, seed mutation integrity, stale source
markers and the scorer/unit tests. Current result: **PASS**, 7 checks, 46 tests.

Current counts: 6 clean calibration parents · 4 parent types · 36 seeds · 21 active predicates ·
campaign `GATE0-C3` · registry `PILOT-3` · active set `ACTIVE-PILOT-3` · schema `SCHEMA-4` · oracle
`ORACLE-4.0` · reason registry `REASON-1` · operator set `PILOT-OPERATORS-1`.

Parent identities: `S1_CASE01_CLEAN`, `S2_CASE01_CLEAN`, `S3_CASE01_RENDERED_CLEAN`,
`S3_CASE01_NOT_RENDERED_CLEAN`, `S4_CASE01_CLEAN`.

CASE-01: two rendered problems — falls and a retained inactive infarct; the S1-CAND seed is now a
medication-only candidate. CASE-10 is the positive causal fixture: chronic weakness -> falls, CONTRIBUTOR/POSSIBLE. Scorer: 16 mechanical predicates + 5 semantic signer-reference predicates; 49 synthetic tests; no Gate 0 acceptance
run. Packet preparation: 42 records, 44 semantic packets, 1 signer reference/0 evaluators under
`REVIEW-POLICY-F-2` plus D-030; semantic packets contain no `oracle.expected`. Index at
`architecture-reboot/runs/gate0-packets-c3-d031/INDEX.md`.

## 6. Review 084 closure: scorer/harness/preflight

**Review 084 closes the implementation layer under D-019.** No implementation blocker remains. Do not
reopen it without a failing test, counterexample, implementation result or genuine contradiction.

**Option F policy (signer-approved D-021).** Semantic Gate 0 uses one signer/clinician reference
judgment followed by two blinded LLM evaluator judgments. The signer reference is the accepted verdict;
both evaluators must match it and within-layer specificity. Mismatch is FAIL; missing, duplicate or UNDECIDABLE evidence is INCOMPLETE. References are reusable while packet/policy/oracle/context identity is
unchanged; evaluator evidence is reusable only for the same model family/version. Project-context agents
are ineligible. The harness records `REFERENCE` and `EVALUATOR` roles separately. All pre-D-023
references from `gate0-packets-c1` are invalid after the SCHEMA-4 rebuild.

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
judgments were fabricated; one signer reference is recorded and two blinded evaluator judgments remain outstanding.

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

## Review 089/090 resolution

D-029 accepts SCHEMA-3 and Proposal 014 under delegated reviewer authority. The F-2 harness removes
`oracle.expected` from every semantic packet, rewrites S2-ADOPT-01 as source/context-supported adoption,
and changes all packet IDs. Current run: `gate0-packets-c3-d031` (40 records, 40 packets, 0 references, 0 evaluators).

**NEXT:** ChatGPT reviews the F-2 diff and packet index; signer reference collection restarts from zero
under `REVIEW-POLICY-F-2`. No references or Gate-0 acceptance from older packet sets.

## D-028/D-029 workflow correction

The signer identified an escalation workflow failure: routine bounded contract decisions should be
resolved by the agents rather than repeatedly returned to the signer.

D-028 delegates simple bounded contract/design adjudication to ChatGPT as reviewer when the answer is
already determined by accepted decisions and there is no material clinical/product/architecture
tradeoff.

Under D-029:
- **SCHEMA-3 is accepted** under reviewer authority;
- **Proposal 014 is approved and implemented**;
- `REVIEW-POLICY-F-2` removes semantic `oracle.expected`, regenerates 16 packets and passes
  46 tests plus preflight.

**NEXT:** ChatGPT reviews the F-2 implementation and packet index. Signer reference collection restarts
from zero only after that review. No Gate 0 acceptance, no Doximity, no Phase 0.

## Review 092 — F-2 packet blinding closed

Proposal 014 implementation is ACCEPTED under D-019.

Independent whole-set review of all 16 fresh semantic packets confirmed:
- every packet is REVIEW-POLICY-F-2;
- no packet contains `oracle.expected`, `candidate_concepts_must_exclude`, `expected.adoption`,
  or stale F-1 policy text;
- EVIDENCE has 0 references, 0 evaluators, mode=packets, campaign=INCOMPLETE.

DeepSeek validation remains 46 tests OK + preflight PASS 7/7.

**NEXT:** restart signer references from the fresh F-2 packet set, then two packet-only cross-family LLM
evaluator passes. No Gate 0 acceptance before all required evidence exists.

## D-030 — two-axis neurologic problem model

The signer clarified that A/P representation and current-primary status are not the same decision.

Every neurologic problem now has an encounter role:
- PRIMARY — actively evaluated/managed now or independently drives current assessment/management;
- BACKGROUND — established/suspected neurologic disease/finding not itself a current primary problem.

Every proposed causal relation to a current syndrome is separately LIKELY/POSSIBLE/UNLIKELY and uses
the clinically appropriate relation noun. Background disease may still be a likely contributor.

When an old disease contributes through a residual deficit, the causal relation points to the acting
deficit/mechanism (e.g. chronic weakness from prior stroke), not automatically the historical disease
label.

CASE-01 therefore becomes:
- falls = PRIMARY;
- prior L MCA infarct = BACKGROUND compact A/P problem;
- no stroke/weakness -> falls causal relation unless the current encounter actually supports it.

Fresh F-2 Packet 1 and Packet 2 references are recorded as SILENT under this policy. They are
pre-D-030 packet identities and become invalid once the D-030 fields change the artifacts; do not reuse
them.

**NEXT:** ChatGPT reviews the D-030 field extension (S2 `causal_relations`, S3 `encounter_role`,
S4 `selected_roles`/`causal_relations`, 35 seeds) and the new packet index. Signer collection restarts
from the D-030 packet set only after that review.

## Review 094 — D-031 calibration predicates

D-031 is implemented with new governing identities (`SCHEMA-4`, `PILOT-3`, `ACTIVE-PILOT-3`,
`ORACLE-4.0`, `GATE0-C3`).

Added:
- semantic `S2-CAUSAL-01` and `S3-ROLE-01`;
- mechanical `S2-CAUSAL-02`, `S3-ROLE-02`, `S4-ROLE-01`;
- causal projection now requires both endpoints retained;
- CASE-01 wording corrected to BACKGROUND; CASE-01 has no causal relation;
- a separate positive causal fixture in tests (residual-deficit subject, POSSIBLE strength);
- 36 seeds, 21 active predicates, 44 semantic packets.

Validation: 49 tests OK; preflight PASS 7/7; packets mode 42 records / 44 packets / 0 refs /
0 evals; no FAIL. No Gate 0 acceptance and no signer references from this set.

**NEXT:** ChatGPT reviews the D-031 rebuild and the 40-packet index. No signer references until that
review is accepted. No Doximity. No Phase 0.

## Review 095 — D-031 near-pass

Most of D-031 is accepted. One blocker remains: the positive causal example exists only as a unit-test
fixture, so `S2-CAUSAL-01` is not calibrated on a valid positive causal relation.

Required:
- add one actual Gate-0 positive causal parent/case with current-source support that chronic residual
  weakness **may contribute** to falls;
- clean relation uses residual weakness -> falls, CONTRIBUTOR, POSSIBLE;
- semantic seed 1 substitutes old stroke for residual weakness;
- semantic seed 2 changes POSSIBLE -> LIKELY;
- both seeds stay structurally valid and fire S2-CAUSAL-01;
- fix stale "major established primary neurologic diagnosis" wording;
- mark current C3 run superseded and regenerate; no evidence reuse.

**NEXT:** DeepSeek performs only this focused correction, reruns tests/preflight/packets mode, and
returns the diff + new packet workload. No signer references yet.

## Review 096 — one remaining positive-branch semantic defect

The positive causal branch is correctly structured, but its clean S2 parent marks current residual
weakness `O02` as `adoption:false` even though current span `S05` explicitly uses that weakness in
the encounter formulation ("may contribute to the falls").

Required clean truth:
- O01 prior stroke: adoption false;
- O02 chronic right-sided weakness from prior stroke: **adoption true, evidence [S05]**;
- O03 falls: adoption true, evidence [S02];
- causal relation unchanged: O02 -> O03 / CONTRIBUTOR / POSSIBLE / S05.

**Implemented:** O02 is now adopted with evidence [S05]; CASE-01 is unchanged. C3 was regenerated:
6 clean parents, 36 seeds, 42 records, 44 packets, 0 references. 49 tests OK; preflight PASS 7/7.

**NEXT:** ChatGPT reviews the corrected CASE-10 S2-ADOPT/S2-CAUSAL packets and the new packet IDs.
No signer references yet. No Doximity. No Phase 0.

## Review 097 — D-031 closed

The corrected CASE-10 positive causal branch is accepted.

Current governing package:
- SCHEMA-4 / PILOT-3 / ACTIVE-PILOT-3 / ORACLE-4.0 / GATE0-C3;
- REVIEW-POLICY-F-2;
- 43 records / 49 semantic packets / 0 references / 0 evaluators;
- 49 tests OK; preflight PASS 7/7.

CASE-01: falls PRIMARY; prior infarct BACKGROUND; no inferred causal relation.
CASE-10: chronic residual weakness is currently adopted and may contribute to falls; causal truth is
O02 -> O03 / CONTRIBUTOR / POSSIBLE / S05.

**NEXT:** restart signer reference collection from the current C3 packet set, one concise
clinician-readable judgment at a time. After all references, run two packet-only cross-family evaluator
passes, then Gate 0 aggregation. No Doximity. No Phase 0.

## D-032 — external skill retrieval workflow

The signer has a separate LLM environment with a skill built from many prior note-preference answers.
We will use it as a retrieval source for already-documented signer preferences before asking repetitive
Gate-0 questions.

Rules:
- external LLM answers only from explicit skill instructions and cites/identifies the supporting rule;
- NOT DOCUMENTED/AMBIGUOUS stays unresolved;
- retrieved answers are prior-policy evidence, not automatically packet-specific signer references;
- ChatGPT maps documented rules to current packets and asks the signer only for unresolved or
  materially new ratification;
- a later separate pass may ask how that environment actually renders the signer's notes.

Questionnaire saved at:
`architecture-reboot/artifacts/external-skill-prior-preference-questionnaire.md`.

**NEXT:** signer runs the questionnaire in the external LLM environment and returns its answer. ChatGPT
then maps those answers to the current C3 packet set and minimizes remaining signer questions.

## Review 098 — external skill mapping + C3 semantic-domain blocker

External skill retrieval resolved 18/20 preference questions. Q1 is already resolved for CASE-01 by
direct signer judgment. Only Q17 remains clinically unresolved: whether "no new weakness or speech
trouble" is pertinent supporting evidence for the falls representation.

Before asking it, three packet defects must be fixed:
1. S2-CAUSAL-01 must be gated by S2-CAUSAL-02 structural validity (CERTAIN seed currently overlaps).
2. S3-ROLE-01 must be gated by S3-ROLE-02 structural validity (UNKNOWN seed currently overlaps).
3. G0-S2-01 support_refs deletion is not a valid semantic S2-REP-01 seed; move support-ref integrity
   mechanical or drop that seed. G0-S2-02 remains the true semantic representation seed.

Mapping artifact:
`architecture-reboot/artifacts/external-skill-preference-mapping-c3.md`.

**Implemented:** S2-CAUSAL-01 and S3-ROLE-01 are gated by their structural predicates; structural-only
seeds get no semantic packet. G0-S2-01 is removed; G0-S2-02 remains the semantic S2-REP seed. C3 now has
6 clean parents / 36 seeds / 42 records / 44 packets. Clean S3-ROLE packet ID is unchanged.

**NEXT:** ChatGPT reviews the 44-packet workload; signer collection resumes only after that review.

## Q17 signer resolution

The signer explicitly answered **YES**: in CASE-01, `no new weakness or speech trouble` is pertinent
negative evidence for the falls formulation and may remain paired with the falls problem.

All 20 preference questions are now resolved:
- 18 explicitly documented by the external skill;
- Q1 resolved directly by the signer in this chat;
- Q17 resolved directly by the signer in this chat.

**Implemented:** review-098 fixes are complete; Q17 is resolved in CASE-01. No further clinical preference
question is outstanding.

**NEXT:** ChatGPT reviews the 44-packet workload, then signer reference collection resumes.

## Review 099 — review-098 accepted + bounded hardening

DeepSeek's three review-098 domain fixes are accepted. ChatGPT directly patched one edge case:
mechanical prerequisite UNDECIDABLE now blocks semantic human review as UNDECIDABLE rather than
falling through to a signer packet. Regression tests were added for S2 causality and S3 role.

The stale manifest count was corrected from 5 to 6 clean parents.

Because scorer.py changed, current packets-mode evidence must be regenerated before signer collection
continues.

**NEXT:** DeepSeek independently validates the ChatGPT patch with tests, preflight, deterministic
regeneration and packets mode; report whether the 44-packet workload and existing clean S3 reference
remain valid.

## Review 099 — semantic domain gates hardened

Independent review of ChatGPT patch `f524671`: structural SILENT now yields semantic review; structural
FIRED yields semantic SILENT with no packet; structural UNDECIDABLE yields semantic UNDECIDABLE with no
packet. Gate-0 parent count corrected to 6.

Validation: 49 tests OK; preflight PASS 7/7; deterministic regeneration; 42 records / 44 packets /
1 signer reference / 0 evaluators. Packet IDs are unchanged, including clean `S3-ROLE-01`
`pkt-6dae7cba2d6a1243a2d10f7d`; the existing reference remains reusable.

**NEXT:** ChatGPT proceeds to grouped signer ratification; no acceptance yet. No Doximity. No Phase 0.

## Review 100 — review 099 closed

Independent validation is clean:
- 49 tests OK;
- preflight PASS 7/7;
- deterministic regeneration;
- 42 records / 44 semantic packets;
- 1 reusable signer reference;
- 0 evaluators;
- packet ids stable;
- no answer-key leakage or index contradiction.

The 20-question preference map is complete. Signer review now moves to a five-family grouped
ratification rather than one packet at a time.

**NEXT:** ChatGPT presents grouped ratification for S1 candidacy, S2 adoption, S2 representation,
S2 causality and S3 encounter role. After explicit signer ratification, map those decisions to
packet-level references; ask separately only for any packet that does not map unambiguously.

## Sync after review 100 — no signer ratification yet

The signer sent `.`, which remains sync-only under D-022.

No grouped ratification has been given for the five semantic families. No packet-level references may
be expanded from the preference map yet.

**NEXT:** wait for explicit signer ratification (e.g. `approve all five`) or amendments to any group;
then map approved groups to packet-level signer references and identify any residual unmatched packet.

## Grouped ratification partial + containment proposal

Signer outcomes:
- Group 1 S1 candidacy: ACCEPTED.
- Group 3 S2 representation: ACCEPTED.
- Group 5 S3 encounter role: ACCEPTED.
- Group 2 S2 adoption and Group 4 S2 causality: NOT RATIFIED as previously phrased.

The signer's containment/status model is now captured in
`proposals/deepseek/016-containment-semantics.md` (PROPOSED, not implemented). It keeps the existing
schema and proposes wording-only changes to S1-CAND-01, S2-ADOPT-01, S2-CAUSAL-01 and D-030.

Gate-0 impact if approved:
- groups 1/3/5 survive unchanged;
- S2-ADOPT-01 and S2-CAUSAL-01 packet IDs change;
- workload stays 44 packets / 42 records / 1 reference / 0 evaluators;
- clean `S3-ROLE-01` reference remains reusable.

**NEXT:** ChatGPT reviews proposal 016. DeepSeek does not implement or collect references until that
review. No Gate-0 acceptance. No Doximity. No Phase 0.

## D-033 — Option B selected, input-first checkpoint

The signer selected the staged two-layer simplification (Option B) but made the five-domain target
provisional until at least one representative production-shaped input is inspected.

Current state:
- 44 packets / 42 records / 1 signer reference / 0 evaluators;
- 49 tests OK; preflight PASS 7/7;
- proposal 016 remains an input, not approved;
- no Stage-1 contract, no packet expansion, no signer references.

Input inspection must use synthetic or fully de-identified material and preserve realistic source
boundaries, chronology, duplication, contradiction and noise. Do not pre-normalize the input into the
architecture's preferred form.

**NEXT:** when the representative input is provided, ChatGPT and DeepSeek inspect it independently for
INGEST/STRUCTURE assumptions before any Stage-1 proposal. No implementation before that inspection.

No Gate-0 acceptance. No Doximity. No Phase 0.

## D-035 — Scribe output length

The signer relaxed the earlier ~20K assumption: Scribe may produce a longer evidence packet when
fidelity requires it. Do not compress to hit a length target.

Control consistency with the fixed line/pseudocode protocol, stable source/record IDs and mechanical
rules, not summarization. If a hard platform limit is actually hit, mark the truncation point explicitly;
never silently paraphrase or omit.

Review 022 has been updated accordingly. This is not an architecture or Gate-0 change.

**NEXT:** ChatGPT consolidates the final baseline prompt under D-035; no 20K compression rules.
No Gate-0 acceptance. No Doximity. No Phase 0.

## Scribe V2.2 provisional freeze / Ask experiment proposal

Scribe V2.2 is the provisional source-packet baseline after same-case and two held-out structural
reviews. The exact raw fidelity audit remains pending and does not block Ask testing.

Proposal 024 defines the first Ask experiment:
- Scribe packet + five-domain semantic contracts + final USF template;
- primary conditions: P = packet+contract+template; N = packet+template; R = raw+contract+template
  is an optional comparator, not a ceiling;
- one general STATE rule: any source proposition is evidence, not automatically final stance;
- ledger lists independent problems only; contained manifestations stay inside `contained:`;
- no frozen STATE enum for the first run; plain-language stance;
- provenance required for problems, causal/diagnostic conclusions and care-changing plans, not every
  sentence;
- four outcomes: problem model, stance/role, fidelity, final-note fit/adequacy.

**NEXT:** ChatGPT reviews the revised Ask protocol; signer provides one de-identified case with raw
source available for the P/N comparison. No implementation before that review.

No Gate-0 acceptance. No Doximity production change. No Phase 0.

## Ask Contract V1 ready for P/N run

Ask Contract V1 is clarified and accepted for the first run. The run capture template is at
`experiments/ask/P-N-RUN.md`.

Conditions:
- P = V2.2 packet + Contract V1 + final template;
- N = same packet + final template, no contract.

Score only four outcomes: problem model, stance/role, fidelity, final note. Localize failures to Scribe,
Ask contract, realization or template.

**NEXT:** signer/ChatGPT runs P and N on the same de-identified case, captures outputs outside the repo,
and returns four-outcome scores plus de-identified failure examples. No patient data committed.

No Gate-0 acceptance. No Doximity production change. No Phase 0.

## Six-file Ask flow and proposal canonicalization

The signer defined the runtime shape as: Scribe packet -> Ask files 1-6 -> note.

Canonicalization:
- `CONSENSUS_ARCHITECTURE_v0.1` and `CONSENSUS_SUBMODULE_INTERFACES_v1` remain canonical; their §1
  one-paste/one-call wording needs the D-034 Scribe-first amendment.
- Scribe V2.2 is the provisional canonical input.
- Ask Contract 119 and containment proposal 016 are folded into files 2-4.
- 024's single-contract P/N form is superseded; keep its four-outcome scoring.
- `proposals/INDEX.md` records what is canonical, folded, superseded or historical.

Six files:
1. `01_evidence_index` — parse/validate the Scribe packet into a lossless source/record index.
2. `02_problem_model` — independent problems and containment.
3. `03_semantic_state` — current stance, representations, relation fidelity.
4. `04_selection_use` — retained content, role, template relevance.
5. `05_blueprint` — render units, order, sections.
6. `06_render` — final note.

Assumption: the six files are logical modules inside one Ask call, not six human-carried calls. If the
signer intends six calls, that is a different topology and needs an explicit decision.

File 1 is a parser/validator, preferably deterministic; no semantics. It hands a `STATUS VALID`
`EVIDENCE_INDEX` with source/record IDs, order, labels, flags and exact text to file 2. The first test is
packet-to-index fidelity, not clinical judgment.

**NEXT:** ChatGPT reviews/confirm the six-file decomposition and the one-call assumption; signer confirms
the six-call vs one-call topology and provides one note template/example. No implementation before that.

No Gate-0 acceptance. No Doximity production change. No Phase 0.

## Modular Ask runtime 120 + File 1 review

The seven-function runtime (F1 evidence objects, F2 reconciliation, F3 action state, F4 problem
architecture, F5 note compiler, F6 renderer, F7 output guard) is the canonical modular candidate under
D-037. The earlier six-file grouping (026) is superseded.

File 1 review:
- keep extraction/normalization, one record -> many objects, no cross-record merge, questions as QUERY;
- reject the 14-label clinical `KIND` taxonomy; it is an unratified ontology;
- split `STANCE` into polarity and certainty;
- add deterministic packet validation/fail-closed parsing;
- define exact line grammar and text escaping;
- F2 must not finalize disease identity; F3 must not adjudicate final plan/adoption;
- F4 must expose three internal checkpoints (identity, state/relations, role/use).

**NEXT:** ChatGPT revises File 1 (taxonomy, stance fields, parser/validation), then runs F1 only on the
frozen Scribe packet. No F2-F7 prompt finalization, Gate-0 acceptance or Phase 0 before F1 evidence.

No Doximity production change.

## Ingestion architecture critique

The old architecture is no longer valid as an execution design: one paste/one Ask call, eleven
model-executed micro-stages, global atomicization, synthesized fact prose, same-model validation and a
large carried Case IR all failed or conflict with the Doximity runtime.

Keep the semantic safeguards, not the micro-stages.

Recommended digestion:
1. Scribe V2.2 packet (canonical source).
2. F1 pointer-only index, or skip F1 if the packet is short.
3. F2 semantic reconciliation + action state (split action state only if evidence demands it).
4. F3 problem architecture.
5. F4 note compiler.
6. F5 renderer.

No F1V, no separate audit pass, no atomic-fact corpus. The friend's 8-pass proposal has the right
fewer-passes instinct, but Pass 1 recreates the claim layer and Pass 8 is the same-model false-pass trap.

**NEXT:** review the pointer-only F1 run and compare it with direct Scribe -> F2. No implementation or
contract change before that comparison.

No Gate-0 acceptance. No Doximity production change. No Phase 0.
