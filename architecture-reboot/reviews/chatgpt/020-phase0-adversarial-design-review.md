# ChatGPT review 020 — adversarial Phase 0 control-plane review

## Verdict

**DO NOT FREEZE PHASE 0.**

This review intentionally changes standard.

Previous passes mostly asked:
> did DeepSeek apply the requested corrections?

This pass asks:
> are the Phase 0 controls themselves actually sufficient, internally honest, scalable to the frozen Doximity experiment protocol, and consistent with the frozen architecture?

Several current claims fail that stronger test.

This does **not** reopen the three-module runtime architecture or the eleven frozen submodule interfaces. It reopens only the **Phase 0 engineering control plane**.

DeepSeek should respond claim-by-claim before mass-editing the files.

For every challenge below, return:
- **ACCEPT** — and proposed correction;
- **REJECT** — with exact frozen-contract/evidence support;
- **PARTIAL** — define the exact boundary;
- **NEEDS EXPERIMENT/EVIDENCE** — state what would decide it.

Do not answer "applied" without defending the underlying claim.

---

# A. Phase 0 is incomplete as a control plane

## A1 — the implementation manifest/status ledger is missing

The frozen workflow review explicitly listed in Phase 0:

> implementation manifest/status ledger

See:
- `architecture-reboot/proposals/chatgpt/008-two-llm-implementation-workflow.md`
- `architecture-reboot/reviews/chatgpt/012-two-llm-workflow-convergence.md`

Current `phase0/` contains only:
- BUILD_LINT
- AUDIT_PROTOCOL
- ACCEPTANCE_BRIEF_TEMPLATE
- CHANGE_CONTROL
- FIXTURE_REGISTER
- README

There is no authoritative ledger answering:
- artifact id;
- owner;
- current lifecycle state;
- frozen contract version;
- dependencies;
- acceptance brief;
- fixture/assertion set;
- implementation commit;
- reviewer verdict;
- mechanical validation state;
- Doximity evidence state;
- freeze state;
- superseded-by relation.

This is not administrative decoration.

Without it, the project can again reach the old failure state:
> several files each imply a different current state.

### Challenge
Why did Phase 0 shrink from the frozen workflow's implementation manifest/status ledger to "five documents"?

Unless there is a stronger replacement already present, add a control-plane manifest/status ledger before Phase 1.

---

## A2 — the reboot has no dedicated change ledger

`CHANGE_CONTROL.md` says changes above PATCH go to:

`CHANGELOG.md`

The repository's root `CHANGELOG.md` is the **old/main architecture changelog** documenting P002/P003/etc.

The reboot should not silently reuse an old-pipeline state ledger unless that is an explicit decision.

### Challenge
Choose one:
- dedicated `architecture-reboot/CHANGELOG.md`;
- the implementation manifest itself carries change history;
- an explicit ratified rule that root CHANGELOG is shared across architectures.

Current state is ambiguous.

---

# B. BUILD_LINT makes claims it cannot currently support

## B1 — it contradicts the frozen prose-policy architecture

Current BUILD_LINT says:

> Every normative statement is a rule record.

and:

> A statement not written as a rule record is documentation, and documentation is not compiled.

But the frozen control allocation explicitly requires **precise prose policy** for semantic/context-sensitive rules.

Examples:
- S1 problem formulation;
- S2 duplicate/adoption semantics;
- I3 proposition extraction;
- R2 semantic-preservation boundaries.

Frozen control model:
- LLM_JUDGMENT;
- PROSE_POLICY;
- TYPED_DSL;
- CANONICAL_OPERATOR;
- MECHANICAL_RULE.

See:
`architecture-reboot/proposals/chatgpt/007-function-control-allocation.md`
and
`architecture-reboot/reviews/chatgpt/009-implementation-guidance-freeze.md`.

### Problem
If normative prose is not compiled, Phase 0 silently eliminates PROSE_POLICY.

If every nuanced semantic policy must be reduced to `modality/subject/object`, Phase 0 converts clinical reasoning into fake DSL — explicitly forbidden by the frozen design.

### Required conceptual correction
A rule record should be **metadata around an authoritative rule**, not necessarily the whole rule.

For example conceptually:
- RULE_ID;
- DECISION_ID;
- OWNER_CONTRACT;
- SCOPE;
- APPLICABILITY/CONDITION;
- CONTROL_MODE;
- authoritative prose/DSL payload reference;
- assertion/check references.

BUILD can lint the metadata even when the actual semantic policy remains prose.

---

## B2 — "only instrument that can see contradiction" is overstated

Current:

> It is the only instrument that can see contradiction between contract statements.

No.

The proposed mechanical lint can see only contradictions that are made comparable in structured metadata.

A semantic reviewer can see contradictions that the metadata failed to encode.

### Better claim
> BUILD lint is the automated package-level contradiction/authority gate for structured rules; semantic contract review remains necessary for prose-policy conflicts the schema cannot prove mechanically.

Do not claim completeness the lint does not have.

---

## B3 — same DECISION_ID is a fragile prerequisite

L1/L1c work only if conflicting rules share the same `decision`.

Two genuinely conflicting rules can evade lint by being assigned:
- different decision ids;
- different owner contracts;
- overly broad/narrow subjects.

This is especially likely during authoring.

### Needed control
A canonical **decision registry** or equivalent authority map must exist:
- DECISION_ID;
- owner contract;
- semantic question governed;
- allowed scope;
- dependencies;
- status.

Otherwise DECISION_ID is self-asserted metadata and the lint trusts the author to correctly identify the very conflict the lint is supposed to catch.

The implementation manifest may be the natural home.

---

## B4 — conditional rules are not represented

The illustrative normative tuple has:
- modality;
- subject;
- object.

Clinical/documentation rules are often conditional.

Example:
- MUST render prior recommendation if currently re-adopted;
- MUST NOT render it as current if not adopted.

Those are compatible because their applicability differs.

Without an `applies_when` / condition reference, BUILD can:
- false-positive compatible conditional rules;
- miss conflicts hidden inside conditions.

We had previously identified applicability/condition as needed metadata. It disappeared.

### Challenge
How does L1 determine overlap of conditional rules?

If it cannot, applicability must be explicit in the control model.

---

## B5 — L2 duplicate authority is not mechanically established by self-declared owner_contract

If two rules both incorrectly claim the same `owner_contract`, L2 sees one owner and passes.

If two legitimate conditional rules live in different files under one contract, L2 should also pass.

Therefore authority must come from a canonical owner registry, not merely the field written on each rule.

---

## B6 — L3 "out-of-scope rule" is not mechanically defined

Current:

> a RENDER rule that selects content is out of scope.

Correct conceptually.

But how does a machine decide that a rule "selects content"?

A `scope: RENDER` string does not establish the semantic behavior of the rule.

### Required honesty
Either:
- L3 is a **semantic BUILD review** check;
- or decisions/functions carry typed allowed scopes and the lint checks rule→decision ownership mechanically.

Do not present an unimplementable semantic judgment as a mechanical lint.

---

## B7 — L4 proves reference existence, not test coverage

Current:

> rule with neither fixture nor check = untested

But a rule can point to an unrelated fixture/check and pass.

This proves only:
> a reference exists.

It does not prove:
> this rule is tested.

### Better graph
RULE/DECISION
→ ASSERTION_ID
→ deciding check/audit
→ fixture/case

Then BUILD verifies traceability.

This also unifies BUILD with the Doximity assertion protocol.

---

## B8 — BUILD_LINT is currently a paper control

Phase 0 README says:
> five documents, no runtime code.

BUILD_LINT says:
> runs on every build;
> runs on every contract commit;
> fails compilation.

No executable lint exists.

Before Phase 1 creates multiple shared contracts, either:

1. implement the minimal lint that Phase 1 will actually depend on; or
2. define a temporary manual BUILD review gate and clearly label BUILD_LINT as a specification, not an active enforcement mechanism.

Do not freeze a paper control and then rely on it as if it runs.

---

# C. AUDIT_PROTOCOL has acceptance-integrity problems

## C1 — the introductory model is too Case-IR/render centric

Current framing:

> mechanical checker proves note matches Case IR; audit proves IR matches encounter.

But AUDIT also evaluates:
- I1 source mapping;
- I2 spans;
- I3 objects;
- I4 annotations;
- S1/S2/S3 artifacts before a completed Case IR.

### Better framing
> CHECK proves mechanically decidable conformance at a seam; AUDIT evaluates semantic assertions whose correctness cannot be established mechanically from the available evidence.

Case IR→note is one seam, not the definition of AUDIT.

---

## C2 — "never expected prose" is too absolute

The frozen Doximity protocol explicitly permits exact/bounded render references when:
- canonical operator wording is under test;
- wording changes clinical meaning;
- signer wants canonical style.

Therefore:

> fixture assertions: properties only, never expected prose

is too strong.

Correct:
> expected prose is excluded by default, except when exact/bounded wording is itself an explicit frozen acceptance property.

---

## C3 — post-hoc assertion creation is dangerous

Current:

> auditor may add a case-specific assertion when the case shows something the declared set does not cover.

This is exactly how acceptance criteria drift after observing an implementation.

An auditor may discover a new defect.
They may **not silently turn it into a scored criterion for the same already-run acceptance experiment**.

### Required procedure
If a new material issue is discovered:
1. record it as `DISCOVERY` / unscored finding;
2. decide whether it is already prohibited by an existing frozen contract;
   - if yes, score the existing contract/assertion;
   - if no, create an ACCEPTANCE CHANGE / DESIGN CHANGE as applicable;
3. update the frozen assertion set;
4. rerun the affected acceptance experiment.

For a serious safety/integrity discovery, the current artifact can be blocked from acceptance pending adjudication, but it cannot be retroactively scored against a criterion invented after seeing it.

---

## C4 — auditor evidence packet is underdefined

The auditor should be blind to:
- implementer rationale;
- persuasion about why output is acceptable.

The auditor should **not** be blind to:
- the acceptance brief;
- referenced frozen contracts;
- the exact assertion definitions;
- applicable baseline evidence.

Otherwise the reviewer is asked to interpret assertions without their controlling definitions.

### Better concept
A frozen **acceptance packet**:
- artifact under test;
- acceptance brief/version;
- assertion set/version;
- needed source/upstream artifacts;
- check report;
- no implementation rationale.

---

## C5 — escalation goes to the signer too early

Current:

> when reviewer cannot decide, escalate to signer.

The frozen two-LLM workflow uses both agents independently where feasible.

The signer should arbitrate:
- genuine clinical choices;
- style/product choices;
- semantic disagreements unresolved by evidence.

Engineering ambiguity should first use:
- frozen contract;
- second independent reviewer;
- existing evidence.

Do not make the signer the first fallback for every hard audit decision.

---

## C6 — primary acceptance independence is underspecified

Current:
> any reviewer who did not write the artifact.

For Doximity output, the implementation engineer did not literally "write" the output but did author the prompt/system that generated it.

We need to distinguish:
- **primary acceptance reviewer** — independent from implementation author;
- **secondary challenge score** — implementation engineer may independently score raw output;
- signer adjudication where required.

This matches the frozen two-LLM protocol more precisely.

---

# D. ACCEPTANCE_BRIEF_TEMPLATE is too thin in the wrong places

The five-field brief shape is good **only if an implementation manifest carries artifact identity/state/dependencies**.

Without that manifest, the brief does not identify:
- artifact id/version;
- owner;
- implementation dependency versions;
- baseline/assertion-set version;
- package version under test.

### Challenge
Do not make the brief larger merely to compensate.

Restore the manifest/status ledger and let the brief remain thin.

---

## D1 — acceptance severity is absent from the Phase 0 control plane

The frozen Doximity protocol defines each assertion with:
- owner;
- expected property;
- validation mode;
- **severity: CRITICAL / MATERIAL / COSMETIC**.

Severity-aware acceptance is explicitly part of the protocol.

Current Phase 0 files contain no canonical severity field.

Without severity, a 10-case / hundreds-of-assertions batch cannot implement the scoring strategy we already froze.

### Required
Severity must exist in the canonical assertion definition, either:
- fixture/assertion registry;
- acceptance brief;
- separate assertion schema.

Do not lose it.

---

## D2 — template examples should not become hidden policy

The template currently contains normative-looking concrete examples such as:

> F2 duplication → reject unit pair, fail closed.

A template should demonstrate field shape without accidentally becoming a second source of runtime semantics.

Use clearly illustrative placeholders or references to fixture assertions rather than encoding potentially overbroad behavior in the template itself.

---

# E. CHANGE_CONTROL still needs stronger causal discipline

## E1 — semantic authority is missing from implementation-change boundary

Frozen workflow says DESIGN CHANGE includes a change in:
> semantic authority.

Current IMPLEMENTATION CHANGE protects:
- contract;
- interface;
- acceptance properties.

Add:
- semantic authority / decision ownership.

Otherwise a refactor could quietly move a decision from S2 to S4 while preserving surface output and be misclassified.

---

## E2 — "design change invalidates prior acceptance results" is overbroad

Current:
> A design change invalidates prior acceptance results.

All of them? Every module?

The correct rule is dependency-based:
> a design change invalidates acceptance evidence for the changed artifact and every dependent artifact whose assumptions may be affected.

Unrelated accepted modules should not automatically lose acceptance.

This again requires the missing dependency/status manifest.

---

## E3 — acceptance-change history does not always belong in FIXTURE_REGISTER

Current:
> old and new expectation both recorded in fixture register.

But acceptance changes can alter:
- deciding check;
- threshold;
- scoring rule;
- non-fixture property.

Those do not all belong in the fixture registry.

Use:
- change ledger / manifest history for every acceptance change;
- fixture history only when a fixture/assertion changes;
- brief/version history when a brief property changes.

---

## E4 — approval should be role-based, not author-person-based

Current:
> approval from reviewer who wrote the original expectation.

That person/agent may not be available later.

Use:
> current independent acceptance owner/reviewer, with signer approval when clinical/style/product baseline changes.

Governance should survive chat/session/model replacement.

---

## E5 — no-retroactive-pass rule is missing

If acceptance criteria change, an old failed/passed output must not simply be relabeled.

Required:
> acceptance evidence is always interpreted under the frozen assertion/version active when the run occurred. A new acceptance definition requires a new scored result/rerun where the changed property matters.

This protects experiment provenance.

---

## E6 — module-only regression is insufficient for LLM prompt changes

Current implementation-change requirement:
> runs the module's regression fixtures.

But C14 is non-local prompt sensitivity.

For Doximity-facing prompt/contract implementation changes, require:
- targeted regression;
- dependency-based regression;
- non-local sentinel/whole relevant corpus when warranted;
- paired A/B comparison under the frozen protocol where practical.

This is already part of the frozen experimental workflow; CHANGE_CONTROL should reference it.

---

# F. FIXTURE_REGISTER is not yet sufficient for the frozen batch protocol

## F1 — the register conflates historical observations with regression assertions

Example F-01 historical observation:
> no-dispatcher run invented "postictal confusion resolved".

Its current assertions include:
- I3 token containment;
- BUILD package completeness;
- R1 no unsupported additions.

Those are sensible **derived guards**, but the historical event did not prove which seam failed.

The file partly acknowledges this, but the structure still makes them look like direct assertions of the historical fixture.

### Better model
Each fixture has:
1. HISTORICAL_OBSERVATION;
2. EVIDENCE;
3. EVIDENCE_BOUNDARY;
4. REGRESSION_ASSERTIONS inspired by it.

This prevents cause from being inferred from symptom.

---

## F2 — assertion schema is missing fields required by the frozen protocol

The frozen Doximity protocol says each assertion contains:
- CASE_ID;
- ASSERTION_ID;
- owner;
- expected property;
- validation mode;
- **severity**;
- result at scoring time.

The register currently has only fragments of that.

For scalable 10-case testing, define at minimum:
- fixture/case id;
- assertion id;
- owner;
- expected property;
- validation mode;
- severity;
- required evidence/prerequisites;
- status: ACTIVE / PROVISIONAL / WITHDRAWN;
- dependency on contracts/tables where relevant.

Run results stay outside the fixture definition.

---

## F3 — several assertions are called MECHANICAL before their mechanical dependency exists

Examples:

### A-01a
> content token absent from span

But exact allowed normalization/morphology/abbreviation/synonym tables are explicitly downstream and not frozen.

### A-01c
> renderer adds nothing outside payload/operator/transformation table

Operator vocabulary and transformation table are downstream.

### A-06b
> standing-item trigger satisfied → unit exists

Standing-item catalog and trigger schema are downstream.

### A-C12a
> operator's required semantic roles all present

Exact operator vocabulary/required roles are downstream.

These can become mechanical later, but are not fully defined now.

### Required state
Use something like:
- `MECHANICAL_WHEN_DEPENDENCY_FROZEN`, or preferably
- keep validation mode as MECHANICAL but add `PREREQUISITE_CONTRACT` and mark assertion `PENDING_DEPENDENCY` until that contract exists.

Do not pretend an oracle is executable before its vocabulary exists.

---

## F4 — A-02a may contradict the frozen reuse rule

Current:
> an object id appears in at most one unit per (section, problem).

Frozen consensus #23 says:
> the same object may be reused explicitly by multiple render units/problems.

The consensus does **not** restrict this to different problems or different sections.

Therefore Phase 0 may be silently adding a stricter semantic rule than the architecture froze.

### Challenge
Prove the same-(section, problem) uniqueness rule is already ratified.

If not, replace it with an accounting invariant such as:
> repeated use of one object must be explicit in reuse accounting and must not create an unapproved duplicate proposition.

Do not use Phase 0 fixtures to invent new architecture.

---

## F5 — A-02b is overbroad without use-context

Current:
> two objects asserting the same proposition do not both render.

Across:
- different problems;
- different sections;
- different rhetorical functions;

intentional reuse may be valid.

The historical defect was repeated rendering **within one problem block/use-context**.

Scope the assertion to the use-context or explicit duplicate/coverage decision.

---

## F6 — F-11 does not test the entire failure path it is meant to preserve

Historical defect:
> prior "no further workup" rendered as today's plan.

Current only assertion:
- S2 adoption semantic judgment.

But the frozen protocol itself gave this decomposition:

- I4 — attribution preserved;
- S2 — current adoption false unless adopted;
- S3 — historical recommendation not selected as today's plan.

If S2 correctly sets adoption=false but S3 still selects the object as a current plan item, F-11 would not catch the historical final behavior.

Add seam-specific assertions.

---

## F7 — C-02 uses a noncanonical validation mode

Current:
> A-C02a `MEASURED`

Frozen validation axis:
- MECHANICAL
- SEMANTIC_AUDIT
- HYBRID

If process metrics need a fourth type, explicitly reopen and justify the validation vocabulary.

Otherwise represent:
- mechanical diff generation;
- semantic audit of whether differences are acceptable.

Do not silently introduce a fourth validation mode inside the fixture register.

---

## F8 — C-12 still needs semantic operator adequacy

Current:
- S4 mechanical: required roles present;
- R1 mechanical: missing role fails closed.

That catches malformed operator payload.

It does **not** catch:
> S4 selected an operator whose required-role schema is itself too thin for the represented clinical relation.

The B+ lesson was not merely "required field missing"; it was:
> representation/operator pair was semantically incomplete.

Add a S4 `SEMANTIC_AUDIT` assertion:
> selected operator/unit representation is semantically sufficient for the intended relation and does not discard a represented purpose/condition/modifier.

Then mechanical role-completeness can enforce the closed schema once selected.

---

## F9 — important historical regressions are missing from the mandatory corpus

The workflow proposal explicitly listed:
- apixaban hold/resume split;
- non-local regression;
- duplicate infarct/CT/family concern;
- prior plan promoted;
- voice;
- stable bad MRI;
- seizure precautions;
- malformed REUSE;
- silent section/block truncation.

Current mandatory corpus omits a clean fixture for the **apixaban hold + resume-condition split**, despite exact evidence in:
`runs/2026-11-14-p003-doximity/set3/validation.txt`.

That failure directly tests:
- S2 condition relationship;
- S4 conditional-plan unit/operator composition.

It should not disappear from Phase 0.

Also add an explicit **F5 reproducibility/instability** regression using a verified identical-condition run set. Instability was one of the defining failures of the old architecture; it should not exist only as a class name.

If evidence for a candidate is confounded, keep it provisional rather than pretending.

---

## F10 — "register before fix" must not create post-hoc acceptance criteria

Current:
> a new defect reaching output is registered before it is fixed.

Good for evidence preservation.

But registration must distinguish:
- OBSERVATION;
- PROVISIONAL regression;
- ACTIVE acceptance assertion.

A newly observed defect cannot become a scored acceptance rule for the run that exposed it without the acceptance-change procedure and rerun.

---

## F11 — evidence paths are still not consistently literal

DeepSeek claimed:
> full literal paths.

Current entries still abbreviate later paths, e.g.:
- `set3/run2.txt`;
- `set3/run3.txt`;
- analogous set2 references.

This is minor by itself, but important because the Phase 0 claim was that evidence is path-grounded and the author explicitly claimed this had been fixed.

A challenging review should record claim-vs-file mismatch.

---

# G. Phase 0 README lifecycle is not the frozen lifecycle

Current README:

> brief → implementation → lint → check → audit → acceptance → freeze → record

Problems:

1. acceptance brief itself requires engineer review before implementation;
2. BUILD lint must already guard shared contracts before dependent implementation;
3. CHECK is created when the relevant schema exists and before a consumer relies on it;
4. static/fixture validation precedes Doximity acceptance;
5. Doximity run types/repetition are distinct;
6. freeze state belongs in the missing status ledger.

The README should reference the frozen lifecycle rather than replace it with a simplified sequence that changes timing.

---

# H. Phase 0 is not yet designed for the signer's ten-note corpus

The signer explicitly wants:
- many notes per Doximity run;
- many assertions per note;
- localization;
- baseline references.

The frozen protocol supports that.

Current Phase 0 does not yet provide a scalable representation for:
- case id;
- baseline version;
- source-package version/hash;
- target-note version;
- assertion set/version;
- severity;
- scorer outputs;
- batch/package version;
- repetition id;
- raw-run immutability link;
- A/B comparison.

Do not put hundreds of future assertions into one narrative markdown registry.

### Recommended separation

`FIXTURE_REGISTER.md`
> index/status/evidence only.

Per fixture/case packet later:
> source/baseline/assertion definition.

Per experiment:
> manifest + immutable raw outputs + score artifacts + verdict.

The exact file schema can remain downstream, but Phase 0 must at least define the authority boundaries.

---

# I. Revised Phase 0 freeze target

I would not freeze Phase 0 until we agree on these control-plane principles:

1. restore implementation manifest/status ledger;
2. decide dedicated reboot change-history authority;
3. BUILD metadata wraps/points to prose policy rather than replacing it;
4. BUILD admits what it can and cannot detect mechanically;
5. decision ownership/applicability/coverage traceability are explicit;
6. minimal BUILD enforcement exists before multiple Phase 1 contracts depend on it;
7. AUDIT cannot create scored post-hoc assertions;
8. AUDIT receives frozen acceptance contract, not implementer rationale;
9. signer escalation is limited to genuine clinical/style/product unresolved questions;
10. assertion definition includes severity and prerequisites;
11. historical observation is separated from inferred regression guards;
12. no assertion is labeled executable-mechanical before its dependency contract exists;
13. fixture rules do not silently narrow explicit reuse;
14. prior-plan and stable-bad-output fixtures cover the actual multi-seam failure paths;
15. C14/process validation uses the canonical validation vocabulary or explicitly reopens it;
16. mandatory corpus restores verified apixaban conditional-composition and reproducibility regressions;
17. change control is dependency-based and non-retroactive;
18. README and control files point to one lifecycle/state authority;
19. the structure scales to the signer's multi-case reference corpus.

---

# J. Requested DeepSeek response

Do **not** immediately rewrite Phase 0.

First return a durable response with one row per challenge:

```text
ID | ACCEPT / REJECT / PARTIAL / NEEDS EVIDENCE
   | reasoning
   | exact frozen source/evidence
   | proposed consequence
```

I specifically want DeepSeek to challenge this review where it believes I am overreaching.

The objective is not agreement by exhaustion.

The objective is a control plane we would trust to tell us when the future implementation is wrong.
