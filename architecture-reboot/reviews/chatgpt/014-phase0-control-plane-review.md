# ChatGPT review 014 — Phase 0 control plane

## Verdict

**REVISE.**

The Phase 0 direction is correct and the five-document scope is appropriate, but several details would recreate exactly the problems Phase 0 is meant to prevent:

- some checks are described as mechanical when they are semantic/hybrid;
- the audit stops after the first failure, which wastes multi-assertion evidence;
- the acceptance brief contains one incorrect failure behavior;
- change control misclassifies adding a test;
- several historical fixtures are misowned, mis-scored, or not supported by the artifacts I reopened.

No runtime implementation should begin until these are corrected.

Also: the signer had asked what Phase 0 was and to sync; that was not an explicit Phase 0 authoring instruction. Since the files are already written and do not touch runtime/main, treat them as **proposal drafts under review**, not signer-approved artifacts.

---

# 1. BUILD_LINT.md — accept concept, revise detection model

## Good
Keep:
- contradiction lint;
- duplicate authority;
- out-of-scope rule;
- untested rule;
- dangling reference;
- conflict marker;
- hard fail rather than warning.

## Required correction A — contradiction is not mechanically detectable from prose inequality

Current text:

> same DECISION_ID + different normative text = contradiction

That is not reliable.

Two differently worded rules may be equivalent.
Two rules may use similar wording but conflict under overlapping conditions.

Freeze this distinction:

### Mechanically detectable
- duplicate authoritative DECISION_ID;
- incompatible structured values where the rule field is closed/typed;
- dangling references;
- owner/scope violations;
- missing fixture/check;
- conflict markers.

### Semantic contract conflict
- two rules with overlapping applicability that prescribe incompatible behavior but are expressed in prose.

That requires BUILD review/audit unless later represented in a typed rule schema.

Do not call a prose string comparison a contradiction detector.

## Required correction B — authority belongs to a decision owner, not necessarily one physical file

Current L2 says:

> decision -> owning file must be one-to-one

Use:

> DECISION_ID -> authoritative OWNER must be one-to-one.

A file is packaging. A decision owner is architectural authority.

There may still be one canonical definition location, but do not make file layout the semantic model.

## Required correction C — scope vocabulary is incomplete

The listed scopes omit shared/build artifacts.

At minimum the framework must be able to represent:
- INGEST
- STRUCTURE
- RENDER
- CHECK
- AUDIT
- BUILD
- SHARED/CONTRACT

Exact enum can remain downstream, but Phase 0 must not define an enum that cannot describe its own files.

## Required correction D — tag syntax is provisional

The HTML-comment rule format is implementation syntax.

Phase 0 should freeze the **required metadata**, not the exact serialization unless we intentionally want to freeze it now.

Required metadata conceptually:
- RULE_ID
- DECISION_ID
- OWNER/SCOPE
- fixture/check reference
- applicability/condition where needed

Exact source syntax can be chosen when BUILD is implemented.

---

# 2. AUDIT_PROTOCOL.md — major revision required

This is the largest Phase 0 defect.

## A. Do not stop after the first failure

Current rule:

> Stop at the first failure and do not continue.

That conflicts with the signer's explicit goal: use one Doximity run to test many things efficiently.

Correct rule:

> Record all independently interpretable failed assertions in the artifact. For each failed assertion, identify the earliest owned divergence that can be established from the available artifact.

Stop the audit only when a lower-level integrity failure makes later judgments uninterpretable, for example:
- output truncated;
- case missing;
- artifact unparseable;
- source/identity mapping corrupted.

One failed semantic assertion must not throw away fifty other useful assertions from the same case.

## B. Inputs must be artifact-level, not always Case IR + final note

Artifact-level batch testing is now frozen.

The auditor may be reviewing:
- I3 objects only;
- S2 adjudication only;
- S4 Case IR only;
- R2 prose section only.

Inputs should therefore be:

1. frozen source/input fixture relevant to the seam;
2. artifact under test;
3. frozen acceptance assertions/reference properties for that artifact;
4. applicable mechanical CHECK result;
5. upstream frozen artifact if needed to evaluate this seam.

Do not require final note when auditing I3.

## C. Auditor must receive the frozen fixture/acceptance properties

The protocol correctly excludes implementer rationale.

But it currently also excludes the very expected clinical properties that live in fixtures.

An auditor cannot score signer-approved semantic expectations without the frozen reference assertions.

Rule:

> hide implementer rationale and design persuasion; show the frozen evidence/fixture and acceptance properties.

That is blindness without amnesia.

## D. The ten fixed clinical checks are becoming a second rubric

Several are also too absolute:

- "no two problems describe the same clinical thing";
- "used under the problem it explains, not the one that merely mentions it";
- "any word not supported is a finding";
- "line thinner than its head is a finding."

These restate/extend runtime policy and can drift from the frozen contracts.

The AUDIT_PROTOCOL should remain a **procedure**:
- verify execution integrity;
- evaluate each semantic assertion in acceptance order;
- record result/evidence/owner;
- classify PASS/FAIL/BLOCKED;
- escalate genuine semantic ambiguity.

Artifact-specific clinical expected behavior belongs in fixtures/briefs.

For source fidelity, reference the agreed source-fidelity/normalization contract rather than "any unsupported word."

## E. One owner belongs to each assertion, not each broad audit check

The frozen Doximity protocol says every assertion has exactly one owner.

Keep owner at assertion/finding level.

---

# 3. ACCEPTANCE_BRIEF_TEMPLATE.md — mostly good, three fixes

## A. "so a script could test it" is too narrow

Semantic properties cannot necessarily be scripted.

Use:

> required artifact properties must be stated in an observable/decidable form and paired with a declared deciding mode.

Then:
- MECHANICAL;
- SEMANTIC_AUDIT;
- HYBRID.

## B. Historical fixture requirement should be relevant, not ceremonial

Current:
> every brief includes at least one historical fixture.

Better:
> every brief cites every relevant historical fixture. If no historical fixture tests the new invariant, a derived fixture is permitted under the agreed derived-fixture rule.

Do not force an unrelated historical defect into a new shared-contract brief just to satisfy a count.

## C. C13 example is wrong

Current:
> C13 over-inclusion -> reject object, do not silently drop

S3 must not delete the source object.

Use:
> reject the proposed note use / retain explicit disposition; preserve the source object.

---

# 4. CHANGE_CONTROL.md — revise classification rules

## A. "adding a test" is not an implementation change

Current IMPLEMENTATION CHANGE examples include:
> adding a test

A new fixture/check/expected property is an **ACCEPTANCE CHANGE** by the document's own definition.

Tests of an already-declared property may be implementation of CHECK tooling, but they must not silently add a new acceptance property.

Clarify:
- implementation of an existing deciding check = IMPLEMENTATION CHANGE;
- adding/changing what is tested = ACCEPTANCE CHANGE.

## B. Implementation change cannot be defined by "does not alter any other module's behaviour"

In a one-call LLM package, non-local effects are exactly what we observed.

Classification should depend on **intended contract scope**, not on assuming observed locality.

Use:
> implementation changes preserve all frozen contracts/acceptance properties.

Then regression testing determines whether unacceptable non-local behavior occurred.

## C. Acceptance change after implementation difficulty is not automatically a design change

Current:
> if changed because implementation could not meet old expectation, it is a DESIGN CHANGE.

Too absolute.

If new evidence proves the frozen expectation/baseline was wrong, that is still an **ACCEPTANCE CHANGE**, even if discovered while implementation was failing.

The forbidden case is:
> changing acceptance merely because the implementation cannot pass, without independent evidence the old expectation was wrong.

## D. Signer approval

If an acceptance change alters a signer-approved clinical reference/baseline, signer approval is required.

For purely mechanical engineering expectations, independent reviewer approval may suffice.

---

# 5. FIXTURE_REGISTER.md — historical evidence must be corrected before freeze

The register says every mandatory fixture is a defect that actually reached output.

Several entries do not currently satisfy that claim as written.

## F-01 fabrication

Keep, but label the evidence boundary accurately.

`postictal confusion resolved` occurred in **run1 with no dispatcher**, an under-specified control.

Canonical source:
- `reviews/P003-implementation-doximity-original-branch.md`
- `runs/2026-11-14-p003-doximity/validation.txt`

It proves under-specified execution can fabricate a status.
It does **not** prove the dispatcher-qualified P003 contract fabricated.

The fixture is still useful as an anti-fabrication regression.

## F-06 seizure precautions

Current wording implies a runtime omission.

Historical evidence says the first omission was **not a valid runtime failure** because `STANDING_ITEMS.md` was absent from the package.

The corrected package subsequently rendered seizure precautions 3/3 in set 2 and 3/3 in set 3.

Sources:
- `reviews/P003-implementation-doximity-original-branch.md`
- `runs/2026-11-14-p003-doximity/set2/validation.txt`
- `runs/2026-11-14-p003-doximity/set3/validation.txt`

Keep it as a historical **packaging/completeness lesson**:
- BUILD/package contains required standing-item contract;
- S4 emits triggered standing item when the contract is present.

Do not label the initial omission as a Doximity S4 failure.

## F-07 malformed REUSE

Primary new-architecture owner should not be R1.

The actual failure was malformed structured output from old 06.

Source:
- `artifacts/06_doximity_run3.md`

Modern analogue:
- S4/schema producer emits malformed Case IR -> CHECK/typecheck catches it;
- R1's secondary responsibility is only to fail closed if malformed structure reaches it.

Split the assertions if both seams are tested.

## F-08 instability

Keep as cross-run measurement.
Do not assign a single runtime owner; S1-S4 decisions are compared.

## F-09 memory referral under both problems

I could not verify this historical claim in the canonical artifacts reopened for this review.

Set 3 shows **family memory concern duplicated within the memory block**, not memory referral rendered under both problems.

Source:
- `runs/2026-11-14-p003-doximity/set3/validation.txt`

Required:
- provide the exact raw/review artifact showing referral cross-problem leakage;
- or remove/replace this mandatory fixture.

Do not freeze an unverified historical fixture.

## F-10 provenance date

The historical phenomenon is useful, but the owner needs seam-specific assertions.

Source-date vs event-time annotation belongs primarily to I4.
If I4 is correct and rendering converts source date into event date, that is an R1/operator failure.

Do not assign the entire class to S2.

Split:
- I4 provenance/event-time annotation assertion;
- R1 rendering preservation assertion.

## F-11 prior "no further workup" promoted to current

Historical source:
- `runs/2026-11-14-p003-doximity/set2/validation.txt`

Keep the case.

But semantic correctness of **current adoption** is not purely mechanical.
The mechanical check can verify that the renderer obeys the adoption field.
Whether the adoption field should be false is semantic/hybrid.

Owner:
- S2 for adoption correctness;
- S3/S4/R1 downstream conformance assertions as separate checks if desired.

## F-13 truncation / whole source block dropped

The register must cite the exact artifact.

I did not find this claim established in the canonical records reopened in this review.

If the source is an old 04 run, name its exact path and distinguish local/mock vs actual Doximity.

Until verified, mark it `PENDING_EVIDENCE`, not mandatory historical fact.

## F-14 "MRI to show."

Keep the historical failure.

But do not label the entire decision purely mechanical before the operator/payload contract exists.

Once the canonical operator requires structured TEST + PURPOSE fields, completeness can be mechanical.

Before then:
- representation adequacy/operator selection is semantic/hybrid;
- R1 payload preservation is mechanical.

Split the seam assertions.

## F-15 residual aphasia rendered as seizure evidence

As written, this is not a valid historical runtime defect.

The P003 review explicitly says O54 was present in the old Handoff, and under that input rendering it was correct behavior; the actual defect was an **upstream contract contradiction** between the Handoff and D-014.

Sources:
- `reviews/P003-implementation-doximity-original-branch.md`
- `runs/2026-11-14-p003-doximity/set2/validation.txt`

In set 3, removing O54 upstream kept it absent 3/3.

Therefore:
- remove F-15 as "residual aphasia over-inclusion" unless another clean artifact proves it;
- replace with the demonstrated **C11 upstream contract contradiction / hidden exclusion** fixture.

## Missing explicit cross-cutting fixtures

The register should include historical controls for:

### C11 contract contradiction
Example:
- Handoff says whole population includes O54;
- D-014 says O54 must stay out.

Also old 06 O51 rule conflict is another candidate.

Owner: BUILD / contract authority.

### C14 non-local regression
Example:
- adding the prior-record/EVIDENCE_MODE clause changed O51 routing.

Source:
- `artifacts/06_doximity_run3.md`

Owner:
- acceptance/regression protocol, not a runtime module.

These are exactly the classes Phase 0 exists to prevent and should not disappear from the mandatory regression corpus.

---

# 6. Phase 0 status

Do not delete the Phase 0 drafts.
They are useful and close.

But current status should be:

- BUILD_LINT: REVISE
- AUDIT_PROTOCOL: MAJOR REVISE
- ACCEPTANCE_BRIEF_TEMPLATE: REVISE
- CHANGE_CONTROL: REVISE
- FIXTURE_REGISTER: MAJOR REVISE / evidence correction

No Phase 1/shared-contract authoring yet.

---

# 7. Acceptance target for the revision

Phase 0 is ready to freeze when:

1. mechanical vs semantic/hybrid detection is correctly separated;
2. audit collects all interpretable findings rather than stopping at first failure;
3. audit is artifact-level and receives frozen fixture assertions;
4. change-control categories are internally consistent;
5. every mandatory historical fixture points to verifiable evidence and accurately states its evidence boundary;
6. fixture owner/deciding mode matches the frozen architecture;
7. C11 and C14 are represented explicitly;
8. Phase 0 itself does not freeze implementation syntax prematurely.

After DeepSeek revises, ChatGPT should re-review all five files as a unit.
