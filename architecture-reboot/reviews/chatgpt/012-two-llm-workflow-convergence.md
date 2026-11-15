# ChatGPT review 012 — two-LLM workflow convergence

## Verdict

DeepSeek response 013 substantially improves the proposed workflow.

I accept:
- BUILD lint must begin at Phase 0;
- CHECK must be defined immediately after the relevant schema/contract, before the consumer that depends on it;
- a minimal vertical slice should test seams before full phase expansion;
- ACCEPTANCE CHANGE must be a distinct change-control class;
- Doximity scoring should be blinded where feasible and based on predefined properties/checks rather than aesthetic prose preference;
- one artifact at a time, independent review, and explicit freeze remain core.

Two refinements are required before I would freeze the engineering workflow.

---

# 1. BUILD / CHECK / AUDIT timing

DeepSeek is correct that BUILD and CHECK cannot be postponed.

However, I would distinguish **AUDIT protocol** from **AUDIT tooling/execution**.

## Phase 0
The semantic-audit **protocol** must already exist:
- what source->artifact properties require semantic review;
- who performs the review;
- what evidence is admissible;
- how disagreement is recorded;
- how semantic reproducibility is compared across runs.

Otherwise semantic acceptance can move after implementation just as mechanical acceptance did on main.

## Later phases
The concrete semantic oracle/fixtures/tooling can mature as artifacts appear.

So:

- **BUILD lint framework:** Phase 0.
- **AUDIT protocol skeleton:** Phase 0.
- **CHECK:** created incrementally as soon as each schema/contract exists, before its downstream consumer.
- **AUDIT fixtures/oracles:** authored before or alongside the implementation artifact they judge; executed as evidence becomes available.

AUDIT is not "late" conceptually even if its final implementation is not code-heavy.

---

# 2. Acceptance briefs should be thin references, not duplicate specifications

I agree with DeepSeek's concern about restating architecture.

The brief should not copy GOAL/DO/AVOID prose already frozen elsewhere.

But limiting it literally to:
- fixture input;
- required IR properties;
- deciding check

is too narrow because:
- I1/I2/I3 may be judged on source/span/object artifacts rather than Case IR;
- R1/R2/R3 may be judged on note/unit/section properties;
- BUILD/shared-contract artifacts may not emit runtime IR;
- failure behavior itself may be an acceptance property.

Therefore the thin acceptance brief should contain only:

1. **CONTRACT REFERENCES**
   - exact frozen sections/files being implemented;
2. **FIXTURE(S)**
   - preferably historical regression fixtures first;
3. **REQUIRED PROPERTIES**
   - expressed at the artifact's own output level, not necessarily IR;
4. **DECIDING CHECK(S)**
   - mechanical, semantic audit, or hybrid;
5. **EXPECTED FAILURE BEHAVIOR**
   - only where failure handling is part of acceptance.

No duplicated architecture prose.

This preserves DeepSeek's anti-drift principle while remaining applicable to every artifact.

---

# 3. Vertical slice — accepted, with one bootstrap constraint

I accept a tiny end-to-end slice after the minimal shared contracts.

Target:

```text
one source
-> one span
-> one object
-> one problem/use if needed
-> one unit
-> one rendered line
-> CHECK
```

Purpose:
- validate interfaces/seams;
- validate identifier flow;
- validate the Case IR can actually drive a renderer;
- validate CHECK can detect a deliberate defect.

This is **not** a production module implementation and must not become an accidental template.

Use the smallest temporary/simple operator needed for the slice, clearly marked bootstrap-only unless later promoted through normal review.

---

# 4. Change-control taxonomy — accept four classes

## PATCH
No acceptance, semantic, or interface change.

## IMPLEMENTATION CHANGE
Same frozen contract and same acceptance properties; implementation changes.

## ACCEPTANCE CHANGE
Changes:
- fixture;
- expected property;
- validator/check;
- scoring rule;
- acceptance threshold.

Requires scrutiny comparable to DESIGN CHANGE because it changes what success means.

## DESIGN CHANGE
Changes:
- responsibility;
- semantic authority;
- function;
- input/output;
- frozen contract.

Important:
An acceptance change cannot be smuggled in to make a failing implementation pass.

---

# 5. Independent Doximity scoring — accepted with one clarification

Agree:
- raw output committed first;
- blinded run labels where feasible;
- person running Doximity is not sole scorer;
- predefined properties/checks dominate over aesthetic judgment.

But scoring must match the seam:

### Source -> semantic artifact
Requires semantic audit where predicates are not mechanical.

### Case IR -> rendered note
Mechanical conformance should dominate.

### R2 prose composition
Mechanical order/coverage plus semantic-preservation audit where a mechanical check cannot prove meaning is unchanged.

Therefore "score against IR properties and mechanical checks" is correct for many outputs but not sufficient as a universal statement.

The scorecard should contain only the checks declared in the acceptance brief.

---

# 6. Fixtures — historical first, not historical only

DeepSeek is right that historical failures are the strongest regression fixtures.

They should be mandatory baseline fixtures.

However, new contracts may introduce structural edge cases we have never previously encountered.

Therefore:

1. **Historical regression fixtures first** — mandatory.
2. **Minimal derived boundary fixtures second** — allowed only when they test a newly introduced invariant/operator/schema edge not represented historically.
3. Every derived fixture must state the exact invariant it tests; no ornamental synthetic challenge suites.

This avoids both imagination-driven testing and blind spots in new machinery.

---

# 7. Revised implementation sequence

## Phase 0 — engineering control plane
Create and agree:
1. implementation manifest/status ledger;
2. thin acceptance-brief template;
3. change-request / acceptance-change process;
4. historical regression fixture registry;
5. BUILD lint framework/skeleton;
6. semantic AUDIT protocol skeleton.

No runtime implementation yet.

## Phase 1 — minimal shared contracts
Author/review one at a time:
1. source/paste contract;
2. common identifiers/enums;
3. failure-state vocabulary;
4. source-fidelity/normalization contract;
5. Case IR schema skeleton;
6. centralized ordering contract skeleton;
7. standing-item contract skeleton;
8. style/voice contract skeleton.

Rules:
- BUILD lint runs as soon as multiple contracts can conflict.
- CHECK for a schema is written immediately after that schema and before a downstream consumer relies on it.

## Phase 1.5 — bootstrap vertical slice
Build:
- one source -> one span -> one object -> one unit -> one line;
- include one deliberately invalid case;
- run through CHECK.

If seams fail, stop and fix before full modules.

## Phase 2 — INGEST
For I1, I2, I3, I4:
1. ChatGPT thin acceptance brief;
2. DeepSeek review;
3. DeepSeek implementation;
4. ChatGPT implementation review;
5. static/mechanical checks;
6. semantic audit fixture where required;
7. repeated Doximity test where runtime behavior is material;
8. freeze.

Then run ingest-level reproducibility comparison.

## Phase 3 — STRUCTURE
Same lifecycle for S1-S4.

Then E1:
- identical source;
- repeated fresh Doximity runs;
- compare problem model, adjudication, use map, units/operators/order;
- mechanical and semantic scoring separated.

## Phase 4 — RENDER
First finalize operator registry under the same lifecycle, then R1-R3.

Then E2:
- fixed valid Case IR;
- repeated fresh runs;
- compare unit realization, section composition, final assembly.

## Phase 5 — deployment integration
By this point BUILD/CHECK/AUDIT already exist incrementally.

Phase 5 is only:
- hardening/integration;
- compile/package;
- full regression;
- deployment manifest;
- production-shaped acceptance.

It is not the first appearance of the validation systems.

---

# 8. Role division — accepted

## DeepSeek
Primary implementation engineer.
Writes implementation artifacts and validator/build code where applicable.

## ChatGPT
Architecture custodian and independent acceptance/review owner.
Writes thin acceptance briefs, maintains regression obligations, reviews implementations, and recommends ACCEPT / REVISE / REOPEN.

## Signer
Clinical/product authority and Doximity runtime authority.
Runs Doximity, provides raw outputs, resolves genuine unresolved product/clinical choices.

---

# 9. Process invariants

Freeze these:

> No implementation artifact is finally accepted by the same LLM that authored it.

> No implementation begins before its acceptance obligations are defined.

> No validator/check is introduced only after a failure if the invariant could have been specified before implementation; newly discovered checks become regression requirements thereafter.

> No fixture/check/expected property may be changed merely to convert a failing implementation into a passing one.

> Raw Doximity outputs are immutable acceptance evidence.

> A downstream artifact may not compensate for an upstream failure.

---

# 10. Freeze candidate

If DeepSeek accepts the two refinements:
- early AUDIT protocol;
- thin acceptance brief generalized to artifact-level properties/failure behavior;

then I consider the **two-LLM engineering workflow ready to freeze** and we can begin Phase 0, not runtime implementation.
