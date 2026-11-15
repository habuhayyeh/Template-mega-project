# Proposal 020 — simplification report and staged repair plan

**Status:** PROPOSED — no code/contract change. This synthesizes the two independent audits, the two
cross-reviews, proposal 016, and the current GATE0-C3 state.

## 1. Executive summary

The three-stage runtime architecture is sound. The problem is accumulated **exception rules** and an
overbuilt **measurement layer** around them.

Current state:

- 21 active predicates, of which 5 are semantic questions and 16 are mechanical;
- 36 seeds, 42 records, 44 semantic packets, 1 signer reference, 0 evaluators;
- 49 tests pass; preflight passes;
- groups 1/3/5 (S1 candidacy, S2 representation, S3 role) are signer-accepted;
- groups 2/4 (S2 adoption, S2 causality) are not ratified as phrased;
- proposal 016 (containment wording) is pending and unimplemented.

The system is not failing because the architecture is wrong. It is failing because every clinical
clarification creates a new contract version, a new predicate pair, new seeds, new packets and a new
reference reset. The cost of changing a rule is now larger than the cost of the rule itself.

## 2. What is actually sound and should stay

1. `INGEST -> STRUCTURE -> RENDER` as three logical responsibilities.
2. Stable source-linked objects with provenance and temporality.
3. One semantic decision has one owner.
4. S1 problem identity, S2 semantic meaning, S3 note-use, S4 compilation are separate.
5. Weak final rendering relative to upstream semantics.
6. Encounter role separate from causal certainty.
7. Option F: one signer reference, two blinded packet-only evaluators.
8. D-028: reviewer adjudicates routine bounded contract changes; signer only for genuine
   clinical/product/architecture choices.
9. Immutable packet evidence and reproducible generation.

## 3. Why it needs fixing

### 3.1 Clinical rules are an exception chain

D-015, D-023 and D-030 accumulated as corrections:

- chronic problems generally require current management;
- major inactive neurologic diagnoses may still render;
- PRIMARY/BACKGROUND becomes independent of retention;
- residual deficits and causal subjects get additional special wording;
- containment now adds another layer of interpretation.

The result is hard to reason about and hard to test. The same clinical question appears in DECISIONS,
predicates, registry assertions, packet instructions, schema notes and review text.

### 3.2 The measurement layer is overbuilt

Concrete evidence:

- **44 packets for 5 clinical questions**;
- **21 predicates**, including shape and meaning both scored for the same field
  (`S2-CAUSAL-01/02`, `S3-ROLE-01/02`);
- **gating special cases** in `score()` to stop structural seeds overlapping semantic predicates;
- **full-silence across every semantic family**, so one seed needs references for the whole family;
- **one seed per predicate**, producing plumbing seeds such as the removed `G0-S2-01` and the
  projection-only `G0-S4-12/13`;
- **clean-parent overload**: layer-local fixtures `S3_CASE01_NOT_RENDERED_CLEAN` and
  `S2_CASE10_CAUSAL` required `case_oracle` and per-parent dependency exceptions.

### 3.3 Identity and hash coupling

`SCHEMA-4`, `PILOT-3`, `ACTIVE-PILOT-3`, `ORACLE-4.0` and `GATE0-C3` changed together while most changes
were wording or fixture changes. Prose edits inside `schema.md`/`predicates.md` change governing hashes
and force regeneration. That is why packet IDs and references keep resetting.

### 3.4 Governance cost

D-024 through D-029 are five decisions to settle one approval. The system spends more time on
attestation and correction than on the clinical model. D-028 fixed the escalation rule, but the
decision log still lacks a clean active/superseded/void index.

### 3.5 The current work is blocked on the unresolved model

Groups 2 and 4 cannot be ratified until adoption and causal-subject semantics are clarified. Proposal
016 is the smallest wording fix, but the broader D-015/D-023/D-030 chain remains. Building more packet
machinery before that model is settled risks optimizing around rules we may delete.

## 4. Target model

### 4.1 Semantic model

Use five **semantic questions**, not five predicates per field:

1. **Problem identity/containment** — does this item have independent problem identity, or is it a
   contained manifestation?
2. **Current-encounter stance** — what does the current source endorse, reject, leave historical, or
   leave unresolved at proposition/object level?
3. **Representation support** — is the approved representation semantically supported by its members
   and relations?
4. **Relation fidelity** — is the causal relation the most specific relation explicitly supported by
   the source, with correct noun, strength and direction?
5. **Encounter role** — is the problem PRIMARY or BACKGROUND for this encounter?

These map to the existing owners; no new module is needed.

### 4.2 Validation model

For each field/axis:

- one **validator** — deterministic shape, vocabulary, id, support and closure check;
- one **semantic question** — judged only if the validator passes;
- validator failure blocks semantic review; it does not create a parallel semantic packet;
- validators are tested in unit/property fixtures and preflight, not as Gate-0 semantic targets.

This removes the gating special cases and the shape/semantic overlap.

### 4.3 Test model

- **Scenario/case** — coherent multi-layer clinical truth (CASE-01, CASE-10).
- **Fixture** — deliberately layer-local artifact with explicit oracle/dependencies; not a fake clean
  parent.
- **Seed** — one meaningful clinical failure mode, not one registry entry.
- Default specificity: all mechanical validators in the layer must pass; semantic calibration covers the
  intended impact set plus a cheap collateral check (combined packet or clean-parent comparison).

### 4.4 Packet model

- one packet per artifact/layer, carrying several independent semantic questions with separate verdict
  slots;
- per-question context slices, so S2 and S3 questions do not leak context into each other;
- expected answers remain blinded;
- packet reuse keyed to the question/packet hash, not the whole campaign name.

### 4.5 Identity model

At minimum:

- **shape id** — fields/ownership/interfaces;
- **semantic policy id** — predicate meaning/wording;
- **source/oracle id** — clinical truth;
- **packet id** — concrete bytes.

Invalidate only the smallest dependency that changed. A wording clarification should not rename the
campaign or force a schema bump.

### 4.6 Normative source

One machine-readable **semantics registry**:

- predicate id;
- current assertion;
- plain-language review question;
- prerequisite validators;
- decision/provenance reference.

Generate operational copies where possible. Keep `DECISIONS.md` as provenance history, plus a current
index with `active/superseded/void` state.

## 5. Options

| option | scope | pros | cons |
|---|---|---|---|
| **A. Minimal** | Approve 016 wording + calibration cleanups only | Fast; unblocks groups 2/4; low risk; keeps current model | Leaves D-015/D-023/D-030 exception chain; measurement still tied to rules likely to change |
| **B. Staged two-layer** | Semantic model first, then measurement redesign | Fixes root causes; avoids optimizing harness around deleted rules; incremental | Longer; requires re-ratification of groups 2/4; packet reset |
| **C. Big-bang rewrite** | All semantic and measurement changes at once | Maximum simplification | High risk; loses evidence; hard to attribute failures; violates incremental governance |

**Recommendation: B, with A's proposal 016 as the immediate first contract patch.**

## 6. Recommended sequence

### Phase 0 — reconcile

- ChatGPT produces the reconciliation matrix from audits 017/101/102/018/019.
- Signer/reviewer chooses scope: A, B, or C.
- No implementation before that choice.

### Phase 1 — immediate semantics (small)

- Approve/amend proposal 016 wording only:
  - S1 independent problem identity;
  - S2 adoption as current-source proposition endorsement;
  - S2 causal relation as most-specific source-supported entity;
  - D-030 subject paragraph replaced.
- No schema field; no seed change; S2-ADOPT/S2-CAUSAL packet IDs change.
- Groups 1/3/5 survive; groups 2/4 re-ratify.

### Phase 2 — semantic architecture consolidation

- Merge problem identity/containment, encounter role and render depth into one current rule.
- Retire D-015/D-023 special-case wording where D-030 now governs.
- Decide whether resolved formulation should be the default for S2/S3; if yes, experiment first.
- Clarify S1 salience only after S4 ordering dependency is frozen.
- Keep coverage, R2 bridges, shared-action ownership as separate experiments.

### Phase 3 — measurement redesign

- Validators vs semantic questions.
- One packet per artifact/layer; per-question slots.
- Seeds only for meaningful clinical failure modes.
- Scenario vs fixture separation; remove `case_oracle`/per-parent dependency hacks.
- Semantics registry; identity axes; active/superseded/void decision index.
- Re-collect references under the new packet set; one-time reset.

### Phase 4 — infrastructure

- Generic decision-closure/accounting validator.
- Projection/hash cleanup: hash normative blocks, not prose; exact paths for semantic fields, additive
  non-semantic fields allowed.
- R2 bridge, coverage, shared-action experiments only after the above.

## 7. Success criteria

- one semantic question per field; no scored shape predicate;
- no gating special cases in `score()`;
- one packet per artifact/layer, not per predicate;
- seeds only for clinical distinctions; no one-seed-per-predicate rule;
- prose edits do not change packet IDs unless the question/packet content changes;
- one normative source for predicate wording/instructions;
- Gate-0 coverage preserved, with fewer packets and fewer signer questions;
- all accepted clinical groups still traceable to a current decision.

## 8. Risks and mitigations

- **Over-generalization loses source fidelity** — keep source-linked objects and explicit provenance;
  no free-form salience or relation graph.
- **Harness rewrite becomes a new bookkeeping system** — implement incrementally; validators are
  tested mechanically, not by signer packets.
- **One-time packet/reference reset** — acceptable now: only one reference exists; preserve clean
  S3-ROLE while packets are unchanged, accept reset when combined packets land.
- **Clinical policy ambiguity** — signer ratifies the semantic model, not every implementation detail.
- **Scope creep** — Phase 1 is wording only; Phases 2–4 require separate review.

## 9. Decision requested

Choose:

- **A** — minimal wording + calibration cleanup now; defer semantic consolidation.
- **B (recommended)** — 016 wording now, then semantic consolidation, then measurement redesign.
- **C** — full rewrite; not recommended.

No implementation until the choice and the reconciliation matrix are recorded.

No Gate-0 acceptance. No Doximity. No Phase 0.
