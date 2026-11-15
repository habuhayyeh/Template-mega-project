# DeepSeek response 017 — to 021 (line-by-line) and 022 (blind-spot audit)

## 0. Position up front

**The verdict is correct and I am not defending the current Phase 0.** The control plane as written describes enforcement that does not exist, and it omits the registries, lifecycle states, versions and evidence packets that its own rules depend on.

Three structural concessions, which resolve most rows before they are argued individually:

1. **Every document is SPEC, not ACTIVE.** No lint, no checker, no packet. The state must be visible on each file. Until an instrument exists, its gate is a **manual checklist** (M0) performed and signed by a reviewer.
2. **There are three authorities Phase 0 never created**: a decision registry, a contract registry, and an implementation manifest. Without them, L2/L2b/L4 and half the fixture assertions are unimplementable. They must be added.
3. **The evidence packet is the unit of acceptance**, not the artifact. `run id + brief version + assertion set version + baseline version + required evidence + check report`. Anything less cannot be scored reproducibly.

I will restructure Phase 0 rather than patch it. Below: concessions, the rows I contest, and answers to the "must answer" lists.

---

## 1. BUILD_LINT (021a)

**Accepted without argument:** lines 1, 3, 7, 10, 11, 12, 13, 14–17, 18, 19, 22, 24, 30–34, 36, 38, 40, 42–46, 48–50, 52–56, 58, 60–62, 64–70, 72–85, 89–101, 103, 107–108, 111–113.

That is most of the file. Specific concessions:

- **L1 as written is false.** Different values are not incompatibility. Replace with: contradiction requires *same atomic decision* + *overlapping applicability* + *modes marked exclusive by a declared compatibility relation*. Where the relation is undefined, the result is **L1c block**, not a contradiction claim.
- **L3 is not mechanically decidable** from prose. It becomes a registry check: a rule's declared scope must fall inside the decision's allowed scopes.
- **L4 does not prove coverage.** Replace the pointer check with `RULE → ASSERTION_ID → check/audit → fixture`, and require the assertion to be ACTIVE.
- **Lifecycle**: draft rules may exist; only compiled rules fail the gate.
- **Sample output** must be labelled illustrative — it currently reads like a report.

**Contested:**

- **Line 109 / PROSE_POLICY (line 7, 51).** PARTIAL REJECT. The lint does not judge prose — true — but that does not delete prose policy. A rule record carries `payload_ref` to authoritative prose, and the compiler **embeds that payload verbatim** into the package. Prose stays normative; the lint checks structure, ownership, scope, pointer integrity and payload hash, never meaning. What line 109 bans is *unreferenced* prose in a compiled artifact, which is the actual failure mode: prose that no rule owns and no check covers.
- **Line 3 "only instrument" (line 17).** ACCEPT the correction: BUILD is the only *mechanical* package-level detector of contradiction. A semantic reviewer sees what metadata cannot; I withdraw "only".
- **Line 30–34 "why a machine knows two rules cannot both hold".** PARTIAL. It does not know. It knows three things: same atomic decision, overlapping applicability, and a declared exclusivity relation between modal pairs. Outside those conditions it blocks as unresolved rather than asserts contradiction. That is weaker than the file claimed and stronger than "a human must read everything".

**Must answer:**
- *How does PROSE_POLICY survive line 109?* Payload reference, embedded verbatim, hashed, owned by a rule.
- *How does L1 know incompatibility?* Declared compatibility table over (decision, applicability, modality). No inference.
- *Conditions?* `applies_when` clause list over typed predicates; overlap computed, not guessed.
- *Identity/ownership independent of self-declaration?* Decision registry; rules reference ids, the registry supplies owner and allowed scopes.
- *L3 mechanical?* Registry scope containment only.
- *L4 coverage?* Assertion-level traceability, ACTIVE status required.
- *What enforces it pre-Phase 1?* Nothing today. M0 manual gate, explicitly labelled as manual.

## 2. AUDIT_PROTOCOL (021b)

**Accepted:** 11, 13–21, 25, 31, 35, 39, 43, 47–54, 60–62, 64, 72–74, 78.

- **Line 41 (auditor may add assertions) — ACCEPT the criticism, it is post-hoc drift.** New findings are recorded as `DISCOVERY`, unscored, and require an acceptance change plus rerun before they can score.
- **Line 78 (any reviewer who did not write) — ACCEPT, too weak.** Primary acceptance reviewer must be independent of the implementation author; the author may be a secondary challenger.
- **Line 17 (properties only, never expected prose) — ACCEPT, too absolute.** Bounded expected prose is a legitimate property where wording is contractual.
- **Line 13–21 (Mode A framing) — ACCEPT.** Mode is determined by assertion prerequisites, not by volume.
- **Last line: `UNDECIDABLE` for a required assertion blocks; it does not merely lower information.**

**Contested:**
- **Line 68 (escalate to signer) — PARTIAL.** Engineering ambiguity goes first to the frozen contract and an independent review; the signer arbitrates clinical, style or product calls. Escalating everything wastes the signer's judgement.

**Must answer:**
- *Line 41 is not goalpost movement because* DISCOVERY is unscored and cannot be applied retroactively; it must pass through ACCEPTANCE CHANGE and a rerun.
- *Implementer cannot be primary auditor because* independence is about authorship of the implementation, not authorship of the text; the author knows too much to be the primary judge.
- *Expected prose is allowed where* the contract states wording as the property; the ban is on speculative prose, not contractual prose.
- *Sufficient packet:* run id, package version, mode, brief version, assertion set version, baseline version, required evidence, check report.

## 3. ACCEPTANCE_BRIEF (021c)

**Accepted:** 11, 13, 14 (real defect — my `§1 L1–L6` mislabelled), 16, 19, 21, 22, 23, 26, 27, 31, 32, 33, 34, 35, 36, 37, 38, 39.

- **Line 37 (unit names exactly one problem) — ACCEPT, not frozen.** Body units may not be problem-bound. Examples must not encode unratified design. Replace with neutral placeholders.
- **Line 47–52 (checks not traceable to P1–P4) — ACCEPT.** Real mapping defect.
- **Line 62 (F2 → reject unit pair) — ACCEPT.** That was hidden runtime policy. Failure behaviour must reference an assertion, not restate a rule.
- **Line 72 (exactly five fields) — ACCEPT with manifest.** Fields stay five only if the manifest and assertion packet own id, version, severity, prerequisites.

**Contested:**
- **Line 86 (one page) — REJECT as a rule, ACCEPT as guidance.** I wrote "target", not a criterion. Making length a decomposition criterion would be wrong for the reason given: coverage grows with case richness. I will mark it explicitly as advice.

**Must answer:**
- *Is "one problem per unit" frozen?* No. Withdrawn from examples.
- *Severity* lives in the assertion packet.
- *Version pinning* via manifest-controlled contract version, not path.
- *Line 62 is not policy because* it will be an assertion reference.
- *Page count* is not a criterion; it is a hint.

## 4. CHANGE_CONTROL (021d)

**Accepted:** 3 (soften), 9, 11, 15, 17, 19, 24, 28, 31–34, 40, 50, 54–61, 63, 69, 75.

- **Line 7 (whitespace is safe) — ACCEPT, it is unsafe.** Classify by verified effect, not edit type.
- **Line 19 / 40 (checker code vs check spec) — ACCEPT and this is the important one.** Fixing a validator to implement an unchanged check is an IMPLEMENTATION CHANGE; altering the check definition is an ACCEPTANCE CHANGE.
- **Line 36 (all prior acceptance invalidated) — ACCEPT, overbroad.** Dependency-based invalidation.
- **Line 49 (all acceptance changes in the fixture register) — ACCEPT, wrong authority.** A change ledger owns them; the register owns only fixture/assertion history.
- **Line 72 (stale example) — ACCEPT.** F-09 in my example was wrong; it must be F-06 or a neutral placeholder.
- **Line 65 — ACCEPT:** the informed/approved states must be defined explicitly, not left to a table that does not contain them.
- **Line 24 — ACCEPT:** Doximity changes need non-local sentinel runs, not just module regression.

**Contested:** none material.

**Must answer:**
- *Whitespace is not safe because* YAML and prompt serialisation are whitespace-sensitive.
- *Checker bugfix is implementation because* the definition of success is unchanged; only the code implementing it was wrong.
- *Not all acceptance is invalidated because* invalidation follows the dependency graph.
- *Register is not the change ledger.*
- *Reboot change history* lives in `architecture-reboot/CHANGELOG.md`, not the root file.

## 5. FIXTURE_REGISTER (021e)

**Accepted:** 11–21 (the seven-way split — observation, evidence, boundary, assertions, prerequisites, severity, status), 25, 26, 30, 31, 33, 34, 35, 38–40, 42, 46, 48, 49, 51, 52, 53, 55, 56, 58, 60–65, 67–72, 74–76.

- **Title** is wrong — it is not "failures that reached output"; packaging and process items are in it. Rename.
- **F1–F4 definitions are too literal/broad** — accepted as written in the review.
- **A-01a token containment** is OVERSTRICT as a proof of fidelity and does not detect a fabricated *relation*; it is one guard among several. Marked PENDING_DEPENDENCY (normalisation table unfrozen).
- **F-11 ownership (line 73)** — ACCEPT: S2 decides adoption; S3 decides current-plan use; S4 builds the unit. My single S2 assertion conflated them.
- **Line 98 `MEASURED`** — ACCEPT: not in the frozen vocabulary. Diff generation is mechanical; acceptance of the diff is semantic. A-C02a is removed as an assertion and recorded as a process metric.
- **Missing apixaban composition fixture** — ACCEPT, added, evidenced by `set3/validation.txt`.
- **Missing F5 instability fixture** — ACCEPT, added as a within-set identical-condition comparison.

**Contested:**
- **A-02a vs consensus #23 (line 43).** PARTIAL REJECT. #23 permits explicit reuse of one object by multiple units; it does not license *unapproved duplicate rendering of the same proposition within one section and problem*, which is the measured failure. The invariant stands, restated as "unapproved duplicate": approved reuse is explicit and recorded, so it is not "unapproved". What was wrong was my wording, not the rule.
- **C-02 "O51 unrelated" (line 94).** REJECT the label, ACCEPT the consequence. O51 is a prior MMSE; the added clause governed prior-record results, so the move was a **direct** effect. That makes C-02 poor evidence for C14, and I withdraw it as the C14 exemplar. C14 needs an object that no clause could plausibly govern. Until then C14 has no mandatory fixture — which is the honest position.
- **C12 needs no semantic assertion (line 107/128).** PARTIAL: it does need one, and the B+ defect is precisely operator underspecification. Add S4 SEMANTIC_AUDIT for operator adequacy, keeping the mechanical role check.

**Must answer:**
- *A-02a* defended above.
- *A-02b scope*: within the adjudicated duplicate relationship, not globally.
- *F-11 ownership*: split S2/S3/S4.
- *MEASURED*: removed.
- *C12*: semantic assertion added.
- *Apixaban, F5*: added.
- *Severity/prerequisites*: assertion packet, not the register file.

## 6. README (021f)

**Accepted:** 3 (no manifest — a real omission, to be added), 13, 14, 15, 17, 18, 19, 20, 21, 22, 23.

- **Line 5 provenance claim** — ACCEPT: I will cite or drop it. The drafts exist under review; that is the defensible statement.
- **Line 15 pipeline description** — ACCEPT: it conflicts with the frozen workflow (engineer reviews brief first; CHECK built as schemas appear; static validation precedes Doximity).
- **Line 12 (change control prevents C14)** — ACCEPT: wrong mapping. Regression protocol detects C14; change control governs edits.
- **Line 17 (nothing changes during Phase 1)** — ACCEPT: false.

**Must answer:** the manifest was omitted because I treated Phase 0 as five documents and did not derive the control plane from the frozen workflow. That is the error. The README will point to the manifest, the lifecycle document, the change-history authority and the enforcement status, rather than restating a simplified lifecycle.

---

## 7. Blind-spot audit (022) — classification

| # | Blind spot | Class |
|---|---|---|
| 1 | test-mode vs production equivalence | PHASE 0 GAP — record as standing obligation |
| 2 | module-boundary behaviour inside one LLM context | PHASE 0 GAP — seam matrix, needed before integration |
| 3 | failure propagation / containment | PHASE 0 GAP — one failure must not cascade |
| 4 | one-call package/resource budget | DOWNSTREAM — owner: package manifest |
| 5 | source→compiled-package fidelity | PHASE 0 GAP — payload hash |
| 6 | package-order sensitivity | DOWNSTREAM — experiment protocol |
| 7 | environment fingerprints | DOWNSTREAM — experiment manifest |
| 8 | cross-run ID matching | PHASE 0 GAP — case namespace |
| 9 | case namespace isolation | PHASE 0 GAP — with 8 |
| 10 | paste-layout / source-order bias | DOWNSTREAM — fixtures |
| 11 | contradictory-source fixtures | PHASE 0 GAP — corpus class missing |
| 12 | full source→output coverage chain | PHASE 0 GAP — chain assertion |
| 13 | seam matrices | PHASE 0 GAP — with 2 |
| 14 | component→integrated evidence hierarchy | PHASE 0 GAP — evidence levels |
| 15 | corpus coverage | DOWNSTREAM — 10-note corpus |
| 16 | scorer calibration | PHASE 0 GAP — known-bad control exists in protocol, not in Phase 0 |
| 17 | control-plane meta-tests | PHASE 0 GAP — who tests the tests |
| 18 | control-plane self-change governance | PHASE 0 GAP — version the control plane |
| 19 | raw-evidence integrity | PHASE 0 GAP — immutable, hashed |
| 20 | baseline versioning | PHASE 0 GAP — with packet |
| 21 | typed absence / unresolved semantics | PHASE 0 GAP — `UNDECIDABLE` and `DISCOVERY` exist, absence types do not |
| 22 | local-artifact vs system readiness | PHASE 0 GAP — readiness states |

Most are Phase 0 gaps, which means Phase 0 is not one control plane but two: the documents I wrote, and the **obligation ledger** that records what is owned downstream so it cannot vanish. I did not build the ledger.

---

## 8. What I propose instead of patching

1. **Rebuild Phase 0 around three registries** — decision, contract, manifest — and an **obligation ledger**.
2. **Add lifecycle state to every document**: SPEC / M0-manual / ACTIVE, with the enforcing instrument named.
3. **Add the acceptance packet** and the **change ledger** as first-class artifacts.
4. **Rebuild the fixture register** as an index over per-case packets, with the seven-part split.
5. **Answer 022 with an obligation per item**: owner, prerequisite, future acceptance test.

I will not defend the current text further. The next artifact will be the rebuilt control plane, not a revision of this one.
