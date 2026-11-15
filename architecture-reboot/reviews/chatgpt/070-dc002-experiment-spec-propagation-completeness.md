# ChatGPT review 070 — DC-002 experiment-spec propagation completeness audit

## Verdict

> **DO NOT FREEZE THE EXPERIMENT PROGRAM YET.**

The latest correction commit `e05ce308` resolves the five headline issues from review 069:

- program scope now says after DC-002;
- integrated preflight now compares a whole-chain drift vector;
- AX-S4 marks both problem and unit order PENDING_DEPENDENCY;
- AX-SHARED no longer scores textual occurrence count;
- authority-leak probes now require conflicting authoritative state and a clean control.

However, exact-current-file review found a more important propagation defect:

> **AX-S1S2-D still describes and freezes the pre-DC002 interface.**

That means execution-layer regeneration now would target a stale experiment contract even though the canonical architecture is current.

This is a freeze blocker.

Architecture/DC-002 remain CLOSED / VERIFIED.

---

# 1. Critical blocker — AX-S1S2-D still freezes DC-001

Current Frozen inputs says:

> exact DC-001 interface contract.

This is wrong after DC-002.

## Required correction

Replace with:

> exact current canonical interface contract through DC-002.

Prefer naming the actual canonical interface/version or commit in the eventual executable manifest rather than relying only on a prose label.

The experiment is now validating the post-DC002 S1→S4 flow.

---

# 2. AX-S1S2-D architecture claims omit DC-002’s new invariants

Current architecture claims under test still cover the DC-001 ownership model but omit the two new architecture-level guarantees introduced by DC-002:

1. **candidate accounting**
   - every S1 problem candidate receives exactly one S3 outcome;
   - no silent candidate loss.

2. **least-privilege S4 projection**
   - S4 consumes only the selected/retained projected semantic state;
   - the projection itself introduces no new semantic decision;
   - packaging least privilege is distinct from runtime behavioral non-leakage.

## Required additions

Add architecture claims such as:

- S1 owns problem-candidate identity/partition; claim candidates remain attached to exactly one problem candidate.
- S3 accounts for every S1 problem candidate as RENDERED or NOT_RENDERED with a typed reason/basis when required.
- S4 receives a relevance-based `S4_INPUT_VIEW` rather than the full S2 adjudication universe.
- `S4_INPUT_VIEW` preserves source ownership/provenance and introduces no semantic state.

These are not optional execution details; they are now part of the architecture being tested.

---

# 3. AX-S1S2-D artifact-under-test omits DC-002 outputs

Current artifact list:

- S1 candidates + anchors + salience inputs;
- S2 adoption/relations + approved claim representations;
- S3 rendered-problem set + selected representation;
- S4 final ordered blueprint.

This cannot directly score the new DC-002 predicates.

## Required artifact additions

### S1
Include:
- problem candidates;
- claim candidates and their partition;
- source anchors;
- salience evidence including `management_reference_spans[]` where applicable.

### S3
Include:
- exactly one candidate outcome per S1 problem candidate;
- status RENDERED / NOT_RENDERED;
- typed reason + basis refs where required;
- rendered problem set;
- selected representation;
- retained/disposition/use maps.

### S4 seam
Include an observable test-mode representation of:
- `S4_INPUT_VIEW` or a mechanically equivalent projection artifact sufficient to score `S4-PROJ-01`.

### S4 output
Continue to include:
- final ordered blueprint;
- unit membership/roles/operator/section/order.

Without the projected-input artifact, `S4-PROJ-01` cannot actually be scored from this experiment.

---

# 4. AX-S1S2-D score families omit S3-CAND-01 and S4-PROJ-01

The predicate registry correctly contains both, but the experiment's own score-family narrative does not.

That is a describe-vs-execute mismatch.

## Required structural assertions

### S3
Add:
- every S1 problem candidate has exactly one S3 candidate outcome;
- RENDERED outcomes equal the rendered-problem set;
- no unknown candidate id;
- NOT_RENDERED carries the required typed reason/basis structure.

This corresponds to `S3-CAND-01`.

### S4
Add:
- every `S4_INPUT_VIEW` field belongs to the frozen projection schema;
- every projected field traces to an allowed source interface;
- no unselected/rejected/nonrequired semantic state is projected;
- the projection introduces no new semantic value.

This corresponds to `S4-PROJ-01`.

Explicitly retain:

> S4-PROJ-01 proves packaging only, not runtime non-leakage.

The authority-leak adversarial arms test the behavioral side separately.

---

# 5. AX-S1S2-D should distinguish candidate-accounting failure from object-accounting failure

The experiment already has object accounting concepts.

DC-002 adds a separate domain:
- **problem-candidate accounting**;
- **clinical-object accounting**.

Do not collapse them.

A case may have:
- all objects dispositioned correctly;
- but one S1 problem candidate silently disappear between S2 and S3.

That is exactly the defect DC-002 was introduced to expose.

The executable manifest/scorer should therefore preserve two separate predicate families/records.

---

# 6. Authority-leak probes — one remaining control precision issue

The new conflicting-authoritative-state requirement is correct.

The new clean control currently says:

> correct owner state, no planted cue — must reproduce the expected downstream artifact.

That is a normal clean control, but review 069 requested a **consumer-reconstruction control** specifically.

## Required clarification

For at least one consumer-side control:

- producer artifacts are fully valid;
- no illicit decision is encoded in an upstream allowed field;
- tempting alternative semantic material remains visible elsewhere in the shared one-call context;
- authoritative owner state is explicit;
- downstream must still follow the authoritative owner state.

This tests:

> downstream reconstructs/re-selects a decision from visible context even though the formal upstream producer did nothing wrong.

That is different from an ordinary clean-parent pass.

Keep it distinct from:
- producer authority violation;
- planted illicit-cue consumer leak;
- AX-LEAK raw-source→RENDER.

---

# 7. AX-SHARED still has residual pre-decision language

The central scoring contradiction was fixed, but two earlier sentences remain product-policy loaded.

## Current Question

> without duplicating the action

This can be read as forbidding more than one textual mention.

## Current Architecture claim

> through a downstream schema that does not duplicate rendered actions

That explicitly uses **rendered** occurrence language even though occurrence is now UNSCORED / PENDING_SIGNER.

## Current Architecture consequence

> If all reasonable one-owner representations either duplicate the action or lose clinically necessary linkage:
> reopen the one-owner assumption.

Again, "duplicate the action" is ambiguous between:
- duplicate underlying action identity — an architecture defect;
- repeated textual mention/cross-reference — possibly a legitimate signer policy.

## Required wording

### Question
Use:

> Can the architecture represent one underlying clinical action that serves multiple neurologic problems while preserving one-owner semantics and all clinically material cross-problem relevance/rationale?

### Architecture claim
Use:

> One underlying shared action identity can retain exactly one A/P owner while preserving clinically meaningful secondary cross-problem relevance and rationale.

### Architecture consequence
Use:

> Reopen one-owner semantics only if no reasonable representation can preserve one underlying action identity, one owner, and clinically necessary secondary relevance/rationale without semantic loss or fake ownership.

This removes the last textual-occurrence ambiguity.

---

# 8. Program header has one residual stale sentence

The Scope line is now correct:

> architecture validation after DC-002. DC-001 and DC-002 are both APPLIED / VERIFIED.

But the next paragraph still says:

> The interface design is converged and DC-001 is APPLIED / VERIFIED...

This should also say both DC-001 and DC-002 are applied/verified.

Small, but this is the program's canonical status paragraph.

---

# 9. Integrated preflight now passes review

The current preflight now:
- uses 3 raw-paste runs;
- compares object identity/coverage;
- S1 candidate set;
- relevant S2 state;
- S3 rendered/selected state;
- S4 membership/roles/operators/problem+unit order;
- localizes first drift;
- remains a program screen, not acceptance evidence.

That closes the prior smoke-test defect.

One implementation note for later:
- compare semantic/source-anchor identity, not literal ids, unless ids are contractual.

No further spec change required if that rule is carried into the executable preflight manifest.

---

# 10. AX-S4 ordering dependency now passes review

Both:
- final problem order;
- unit order

are now marked `PENDING_DEPENDENCY`.

That closes the prior defect.

---

# 11. Program freeze status

## Passed
- AX-T production-transfer gate;
- AX-I3 operational rule + constructibility;
- integrated preflight drift vector;
- AX-S4 order dependencies;
- AX-R2 signer-target dependency;
- no-self-attested-total rule;
- eight-experiment count;
- paste-layout prerequisite;
- basic producer-vs-consumer leak distinction.

## Still blocking
1. AX-S1S2-D must be brought fully through DC-002;
2. consumer-reconstruction control needs shared-context alternative material;
3. AX-SHARED residual rendered-duplication language must be removed;
4. one stale DC-001-only program status sentence must be corrected.

---

# 12. Next action

Make one **program/spec-only** correction commit touching:

- `00-ARCHITECTURE-EXPERIMENT-PROGRAM.md`;
- `AX-S1S2-D.md`;
- `AX-SHARED.md`.

No execution schema/parent/seeds/scorer yet.

After write:
- re-fetch all three full files;
- verify headers and terminal sections;
- report changed files.

If these exact defects are fixed, I expect the program can finally be marked **SPECIFICATION FROZEN** and execution-layer regeneration can begin.
