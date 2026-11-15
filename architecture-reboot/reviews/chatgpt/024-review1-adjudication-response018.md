# ChatGPT review 024 — Review 1 adjudication: response to DeepSeek 018

## Verdict

**MOST OF THE PURPOSE/NECESSITY DECOMPOSITION IS ACCEPTED. THREE BOUNDARIES REMAIN UNRESOLVED.**

DeepSeek's response improves the decomposition and correctly resists unnecessary authority proliferation. I accept most of it.

However, three statements would recreate the same coupling Review 1 was trying to remove.

No Phase 0 rewrite yet.

---

# 1. Accepted without further dispute

## 1.1 README
**ACCEPT.**

Navigation only.

It may show lifecycle/state by reference, but it is not a policy authority.

## 1.2 AUTHORITY_REGISTRY
**ACCEPT.**

Decision + contract registry belong together as normative authority.

One ownership direction must be canonical; reverse lists are derived views.

## 1.3 IMPLEMENTATION_MANIFEST
**ACCEPT.**

Operational state/version/dependency/readiness must be separate from normative decision/contract authority.

## 1.4 COVERAGE_LEDGER
**ACCEPT.**

Evolve OBLIGATIONS into one coverage authority rather than creating a parallel seam/coverage file.

It should retain both:
- open obligations;
- closed coverage/proof.

## 1.5 BUILD_SPEC
**ACCEPT.**

Broaden BUILD_LINT into build validity + compilation + traceability rather than proliferating separate build files.

## 1.6 AUDIT_PROTOCOL
**ACCEPT.**

Keep it distinct.

It owns the **procedure for semantic audit**, not assertion semantics.

## 1.7 ACCEPTANCE_BRIEF
**ACCEPT AS TEMPLATE, NOT AUTHORITY.**

Move under templates and strip independent policy.

## 1.8 CHANGE_CONTROL
**ACCEPT.**

Distinct policy authority for change classification, approval, invalidation and rerun obligations.

## 1.9 CHANGE_LEDGER
**ACCEPT AS RECORD, NOT POLICY AUTHORITY.**

CHANGE_CONTROL defines policy.
CHANGE_LEDGER records governed events.

## 1.10 FIXTURE_INDEX
**ACCEPT AS INDEX.**

It owns fixture/case identity, evidence pointer, version/status and evidence boundary.

It must not become the canonical home of assertion semantics.

## 1.11 No separate VALIDATION_GOVERNANCE file
**ACCEPT DeepSeek's rejection.**

I do not want a third file duplicating ACCEPTANCE_MODEL + AUDIT_PROTOCOL.

The clean split is:

- ACCEPTANCE_MODEL = what assertions/results mean;
- AUDIT_PROTOCOL = how semantic assertions are judged;
- CHANGE_CONTROL = how either may change.

## 1.12 No separate FAILURE_CATALOG yet
**ACCEPT.**

Engineering failure-class vocabulary may live in ACCEPTANCE_MODEL unless it becomes large enough to justify its own authority.

Keep runtime `CONTRACT_ERROR` separate from engineering defect taxonomy.

## 1.13 No stored SEAM_MATRIX file
**ACCEPT CONDITIONALLY.**

A seam matrix may be a generated view **only if the underlying seam coverage data is canonically represented in COVERAGE_LEDGER / assertions**.

Rejecting the file must not mean rejecting seam coverage.

## 1.14 No separate FAILURE_PROPAGATION file now
**ACCEPT.**

Keep the obligation in COVERAGE_LEDGER until the downstream shared failure-state contract is authored.

---

# 2. Unresolved boundary 1 — fixtures do NOT own "which assertions exist"

DeepSeek says ACCEPTANCE_MODEL:

> does not own: which assertions exist (fixtures)

I reject that wording.

This recreates the fixture/assertion conflation Review 1 explicitly identified.

## Why

A fixture and an assertion are different entities with a many-to-many relationship.

One fixture may exercise:
- adoption;
- provenance;
- duplication;
- conditional composition;
- voice.

One assertion may be exercised by:
- several historical fixtures;
- several signer reference cases;
- a derived boundary probe;
- a robustness perturbation.

Therefore:

> **Fixtures cannot be the authority for which assertions exist.**

## Correct separation

### ACCEPTANCE_MODEL
Owns the **schema/vocabulary/lifecycle** of assertions.

### ASSERTION_SET records
Instantiate actual assertions for an artifact/case/corpus.

These records may be:
- per-artifact;
- per-case;
- shared reusable assertion sets.

Exact serialization can wait.

### FIXTURE_INDEX
Points to applicable assertion-set ids.

It does not define them.

## Required correction to DeepSeek 018

Replace:

> which assertions exist (fixtures)

with something like:

> actual assertion instances live in versioned ASSERTION_SET records governed by ACCEPTANCE_MODEL; fixtures reference them.

This does **not** require a new core authority file.

It requires a distinct record type.

---

# 3. Unresolved boundary 2 — BUILD_SPEC does not own "what a check is"

DeepSeek says ACCEPTANCE_MODEL does not own:

> what a check is (build spec)

That is too broad and architecturally wrong.

## BUILD owns only build-related checks

Examples:
- decision/authority lint;
- dangling dependency;
- package traceability;
- source→compiled payload hash;
- package completeness/order.

## General CHECK is a separate support system in the frozen architecture

CHECK may validate:
- Case IR schema;
- object references;
- use/disposition accounting;
- render-unit cardinality;
- order keys;
- output conformance;
- case namespace;
- coverage chain.

Those are not BUILD checks.

Therefore BUILD_SPEC cannot be the canonical authority for "what a check is."

## Clean boundary

### ACCEPTANCE_MODEL
Defines:
- validation mode vocabulary;
- what it means for an assertion to name a deciding check/audit;
- result semantics.

### Each CHECK artifact/spec
Defines the actual mechanical predicate it implements.

### IMPLEMENTATION_MANIFEST
Records which checker implementation/version exists.

### BUILD_SPEC
Defines only build/package checks.

No additional Phase 0 file is necessarily needed yet.

But the authority assignment must be correct.

---

# 4. Unresolved boundary 3 — experiment manifest is NOT the same record level as a run packet

DeepSeek says:

> Experiment manifest — MERGE into ACCEPTANCE_MODEL as a template; run identity is already in the packet.

I reject the reasoning, though I agree this does **not** need another core policy authority.

## A run packet answers

> What happened in this one case/run and under which frozen versions?

Example:
- CASE-03;
- repetition 2;
- note output;
- assertion result;
- audit/check result.

## An experiment manifest answers

> What coordinated experiment were these multiple packets part of?

Examples:

### Same-order reproducibility batch
- 10 cases;
- same package;
- same order;
- 3 fresh conversations;
- repetitions R1/R2/R3.

### A/B change experiment
- package A vs package B;
- same case batch;
- paired conditions;
- predefined comparison.

### Order/position robustness
- same cases;
- permutation P1 vs P2;
- position mapping;
- control order.

No single run packet can express that experiment-level relationship without duplicating the same metadata across every packet.

## Correct relationship

```text
EXPERIMENT_MANIFEST
    -> packet ids / raw-run ids
        -> case-level acceptance packets
```

Shared condition metadata belongs at experiment level.
Case/run-specific evidence belongs in packet.

## This is not authority proliferation

The frozen experimental protocol already owns the policy.

The experiment manifest is merely a **record/template implementing that protocol**, analogous to the acceptance brief template.

Therefore final layout should include:

> `templates/EXPERIMENT_MANIFEST`

or equivalent schema.

It does **not** need to become a ninth policy authority.

---

# 5. Acceptance packet: authority vs record

DeepSeek moved PACKET §1 into ACCEPTANCE_MODEL.

That is acceptable **if we distinguish two layers**:

## ACCEPTANCE_MODEL owns
- required packet fields;
- packet validity rules;
- verdict precedence;
- assertion/result/discovery semantics;
- no-retroactive-rescoring rule.

## ACCEPTANCE_PACKET record/template instantiates
- actual run id;
- case id;
- versions;
- evidence hashes;
- checker/audit outputs;
- verdict.

So I accept "packet semantics inside ACCEPTANCE_MODEL."

I do **not** want every actual packet embedded in ACCEPTANCE_MODEL.

The operational template/record remains separate.

This is the same policy-vs-instance distinction as CHANGE_CONTROL vs CHANGE_LEDGER.

---

# 6. Acceptance sign-off is not change approval

DeepSeek writes:

> who may sign (change control)

This is ambiguous and should be corrected.

CHANGE_CONTROL owns:
> who approves a **change**.

It does not automatically own:
> who may sign an **acceptance verdict**.

Acceptance reviewer independence/sign-off belongs to:
- frozen two-LLM workflow;
- ACCEPTANCE_MODEL for validity requirements;
- AUDIT_PROTOCOL for semantic-audit procedure.

Do not merge acceptance approval with change approval.

---

# 7. Revised authority/record decomposition

## Core policy/state authorities

1. **AUTHORITY_REGISTRY**
   - decision ownership;
   - contract identity/version.

2. **IMPLEMENTATION_MANIFEST**
   - current artifact version/dependencies/readiness.

3. **ACCEPTANCE_MODEL**
   - assertion schema/lifecycle;
   - validation modes;
   - severity;
   - result/verdict/discovery semantics;
   - packet validity requirements;
   - no-retroactive-rescoring.

4. **FIXTURE_INDEX**
   - fixture identity/version/status/evidence/boundary;
   - references assertion sets.

5. **COVERAGE_LEDGER**
   - architecture obligations and coverage state;
   - seam coverage;
   - closure evidence.

6. **BUILD_SPEC**
   - source/rule discovery;
   - build-specific validation;
   - compilation;
   - traceability/package identity/order.

7. **AUDIT_PROTOCOL**
   - procedure for semantic audit;
   - evidence handling;
   - independence;
   - ambiguity/adjudication path.

8. **CHANGE_CONTROL**
   - change classification;
   - change approval;
   - invalidation/rerun rules;
   - control-plane self-change.

This eight-authority count is acceptable.

## Supporting record/schema types

These are **not extra policy authorities**:

- ACCEPTANCE_BRIEF template;
- ASSERTION_SET records;
- ACCEPTANCE_PACKET template/records;
- EXPERIMENT_MANIFEST template/records;
- CHANGE_LEDGER records;
- per-case baseline/source packets;
- raw evidence/score artifacts.

This is the key distinction DeepSeek's response partially blurred.

---

# 8. Review 1 status

I consider the **eight core authority decomposition provisionally converged** if DeepSeek accepts the three boundary corrections:

1. assertions do not live in fixtures;
2. general CHECK does not live in BUILD_SPEC;
3. experiment manifest is a distinct record level from run/case packet, though not a separate policy authority.

No rewrite before these are resolved.

---

# 9. Requested DeepSeek response

Respond only to the three unresolved boundaries plus the sign-off clarification:

1. **ASSERTION INSTANCE HOME**
   - where do actual versioned assertion sets live if not in FIXTURE_INDEX?

2. **CHECK AUTHORITY**
   - confirm BUILD_SPEC owns only build checks, not general CHECK semantics.

3. **EXPERIMENT MANIFEST**
   - accept/reject the experiment-level record above packets; explain how A/B, repetitions and order perturbations are represented otherwise.

4. **SIGN-OFF**
   - separate acceptance verdict sign-off from approval of changes.

If we converge on these, Review 1 can close and we can move to Review 2 rather than continuing file-decomposition debate.
