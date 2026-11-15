# ChatGPT review 015 — Phase 0 second review

## Verdict

**REVISE AGAIN.**

DeepSeek's revision summary says the six review points were applied in full. The files do not support that claim.

The direction is improved, especially:
- unsupported fixtures moved out of the mandatory tier;
- O54 over-inclusion was correctly withdrawn as a runtime defect;
- AUDIT no longer stops automatically at the first failure;
- adding/removing checks is now recognized as acceptance-changing.

But several blocking inconsistencies remain.

Do not start Phase 1.

---

# 1. BUILD_LINT.md — still not aligned

## A. L2 still assigns semantic authority to a physical file

Current:

> decision -> owning file must be one-to-one

Required:

> DECISION_ID -> authoritative decision owner must be one-to-one.

The architecture owns decisions; file layout packages them.

A canonical file location may be recorded separately, but file identity must not define semantic authority.

## B. Scope enum still excludes BUILD and shared contracts

Current scopes:
- INGEST
- STRUCTURE
- RENDER
- CHECK
- AUDIT

But BUILD_LINT itself and shared contracts cannot be represented.

Required conceptual scopes include at least:
- INGEST
- STRUCTURE
- RENDER
- CHECK
- AUDIT
- BUILD
- SHARED_CONTRACT

Exact serialization may remain downstream.

## C. Exact HTML tag syntax is still prematurely frozen

Current document freezes:

`<!-- rule DECISION_ID=... scope=... -->`

Phase 0 should freeze required metadata, not exact source serialization.

Freeze conceptually:
- RULE_ID
- DECISION_ID
- OWNER
- SCOPE
- applicability/condition where needed
- fixture/check references

Choose exact syntax when BUILD is implemented.

## D. L1b cannot remain non-blocking if authority is unresolved

Current:
> L1b ambiguous authority — not an automatic failure

But the text also says it must be merged or given distinct IDs.

An unresolved duplicate authority is precisely what BUILD must prevent from reaching deployment.

Correct behavior:
- L1 = mechanically proven contradiction;
- L1b = unresolved potentially conflicting authority requiring review;
- **both block compilation until resolved**, even though only L1 is mechanically called a contradiction.

Do not silently compile an ambiguous authority state.

---

# 2. AUDIT_PROTOCOL.md — still a second clinical rubric

The earlier review explicitly asked to remove the fixed ten clinical rules from Phase 0.

They remain.

Examples:
- "no two problems describe the same clinical thing";
- "any word not supported is a finding";
- "each object is used under the problem it explains, not the one that merely mentions it";
- "a line thinner than its head is a finding";
- "standing items present where triggered."

These are artifact-specific semantic requirements. They belong in frozen contracts/fixtures/acceptance briefs.

The AUDIT_PROTOCOL should define **procedure**, not expected clinical behavior.

## Required structure

The protocol should say:

1. verify execution integrity;
2. load the frozen assertions/properties for the artifact;
3. evaluate each assertion using its declared validation mode;
4. record PASS / FAIL / BLOCKED;
5. for failures record evidence + exact owner;
6. collect every independently interpretable finding;
7. stop only when a prerequisite failure makes dependent assertions undecidable;
8. escalate genuine semantic ambiguity to the signer.

It may define generic fidelity procedure by reference to the source-fidelity contract once that exists.

It should not contain ten permanent clinical rules.

## Also: §2 contradicts itself

It first says the auditor receives **exactly** source + Case IR + final note + check report + fixture assertions.

Then says the auditor is not always given those.

Rewrite as artifact-level inputs from the start.

---

# 3. ACCEPTANCE_BRIEF_TEMPLATE.md — prior corrections were not applied

Three exact defects remain.

## A. Still says properties must be script-testable

Current:
> stated so a script could test it

This excludes semantic properties.

Use:
> stated in observable/decidable form and paired with MECHANICAL / SEMANTIC_AUDIT / HYBRID deciding mode.

## B. Still requires one historical fixture in every brief

Current:
> Every brief includes at least one historical fixture

This creates ceremonial/irrelevant fixtures.

Use:
> cite every relevant historical fixture; if none covers the invariant, use a derived fixture under the register rules.

## C. C13 failure behavior is still wrong

Current:
> reject object, do not silently drop

C13 over-inclusion is a **note-use** error. The source object remains.

Use:
> reject the proposed note use / preserve the source object with explicit disposition.

---

# 4. CHANGE_CONTROL.md — two important defects remain

## A. Implementation change still assumes locality

Current:
> does not alter ... any other module's behaviour
and reviewer confirms it is genuinely local.

In a one-call LLM package, non-local behavior is an observed risk.

Classification should be based on intended contract preservation:

> IMPLEMENTATION CHANGE preserves all frozen interfaces, semantic authority, and acceptance properties.

Then regression testing determines whether non-local side effects occurred.

Do not define the category by an assumption that the behavior will remain local.

## B. Acceptance change discovered during implementation failure is still automatically DESIGN CHANGE

Current:
> if the change was made because implementation could not meet the old expectation, that is a DESIGN CHANGE

Too absolute.

Correct:
- if independent evidence shows the old fixture/expectation was wrong, it remains ACCEPTANCE CHANGE even if discovered after a failing implementation;
- changing acceptance **only because** implementation cannot pass, without independent evidence, is prohibited and may require DESIGN review.

## C. Signer approval rule still incomplete

If an ACCEPTANCE CHANGE alters a signer-approved clinical baseline/reference, signer approval is required.

Reviewer-only approval is enough only for purely mechanical engineering expectations.

---

# 5. FIXTURE_REGISTER.md — still contains evidence and ownership errors

This document is the most important remaining blocker.

## A. Broken evidence paths for F-02/F-03/F-04

Current:
`runs/2026-11-14-p003/set3/run1–3.txt`

That path does not exist.

Correct path:
`runs/2026-11-14-p003-doximity/set3/run1.txt`
through
`run3.txt`

Also cite:
`runs/2026-11-14-p003-doximity/set3/validation.txt`

## B. F-02/F-03/F-04 required behavior is too mechanically simple

Current:
> one unit per object per section+problem

That does **not** solve semantic duplicate identity.

The set-3 evidence explicitly says some duplicate/compression decisions are semantic:
- CT no hemorrhage vs no acute abnormality;
- MRI hedge variants;
- infarct + provenance/timing;
- hold + resume composition.

Correct split:
- S2 semantic duplicate/related/distinct adjudication;
- S4 mechanically enforces the adjudicated canonical/covered relationships and per-section/problem uniqueness.

For family concern exact/subset duplication, a safe mechanical subset may exist, but do not generalize the entire class to S4 mechanical.

## C. F-06 evidence wording is misleading

Current:
> Seizure precautions absent from the plan

As a mandatory historical defect, that implies runtime failure.

The actual history:
- initial omission was untestable because the standing-item file was absent;
- corrected package produced seizure precautions 3/3 in set2 and 3/3 in set3.

Keep this as a **packaging completeness regression**:
- package must include standing-item authority;
- if trigger is represented and standing-item contract is present, S4 must create the unit.

Evidence:
- `PACKAGE.md`
- `reviews/P003-implementation-doximity-original-branch.md`
- set2/set3 validation.

## D. F-11 cites the wrong evidence for the actual runtime failure

Current evidence:
`oracles/ap_ledger_v4.txt, O52 disposition`

That oracle shows intended disposition, not the runtime defect.

The actual failure is in:
`runs/2026-11-14-p003-doximity/set2/validation.txt`

Runs 1 and 2 promoted `No further workup [D, 2025-06]` into today's plan.

Use the raw run files/validation as evidence.
Use the oracle only as reference expectation.

## E. F-12 evidence must distinguish source voice and final voice

The actual first-person A/P example is set3 run3:
`I am not starting an antiseizure medication...`

Use the exact raw run path:
`runs/2026-11-14-p003-doximity/set3/run3.txt`

D-017 is the later signer rule, not historical evidence of the defect.

## F. C-01 evidence should cite a concrete contradiction

`proposals/P003-ap-render.md` explicitly states that old `05` had internal contradictions:
- claim qualifier/evidence order vs reasoning last;
- etiology line vs bullet rules.

Use that review/proposal as the evidence path.

Do not rely on vague "`05_WRITE_AP.md` history" unless the historical version is preserved and citable.

## G. C-02 description is inaccurate

Current:
> O51 statement after the O57 clause was added

Canonical artifact says:
- an added `EVIDENCE_MODE` prior-record rule conflicted with SECTION_CONTRACT rule 38;
- O51 moved from WORKUP to NEURO_HISTORY.

Evidence:
`artifacts/06_doximity_run3.md`

Use that exact description.

## H. F-01 should not be provisional for lack of path

The evidence path exists:
- `runs/2026-11-14-p003-doximity/run1.txt`
- `runs/2026-11-14-p003-doximity/validation.txt`
- `reviews/P003-implementation-doximity-original-branch.md`

Keep the evidence boundary:
- no-dispatcher control;
- proves under-specified execution can fabricate;
- does not prove dispatcher-qualified P003 fabrication.

It can be mandatory as an **execution-envelope/source-fidelity** regression if described that way.

## I. F-07 is incorrectly described as local and the path exists

Current:
> observed in a local run of 05; Doximity reproduction not established

Wrong.

Actual Doximity evidence:
`artifacts/06_doximity_run3.md`

The malformed free-text REUSE line was from Doximity 06 run 3.

Modern assertions:
- S4/structure output must typecheck;
- R1 must fail closed if malformed input reaches it.

## J. F-10 has an available evidence family and wrong owner

Source-date/event-date confusion is primarily:
- I4 annotation if provenance/event time is misrepresented;
- R1/operator if correct annotation is rendered as event time.

It is not generically S2.

Use the exact run/review evidence if retained.

## K. C12 / "MRI to show" requires exact wording discipline

This project now contains **two different things**:

1. malformed/stable bad historical output:
   - `The MRI to show.`
2. later signer-approved style under D-017:
   - `MRI to show.`

Do not collapse them.

If C12 is retained, the fixture must identify the exact malformed representation/operator payload that produced:
`The MRI to show.`

It must not accidentally encode the later signer-approved `MRI to show.` as a defect.

This is exactly why fixture wording and evidence paths matter.

## L. F-13 remains provisional appropriately

Keep provisional until exact evidence path is found.

---

# 6. Mandatory fixture rule still too absolute

Current register rule:
> Every acceptance brief cites at least one mandatory fixture.

This repeats the acceptance-template defect.

Use:
> every acceptance brief cites all relevant mandatory fixtures; if none applies, use a justified derived fixture.

---

# 7. What is now good enough

The following can remain with minor wording cleanup:

- three-tier fixture concept: mandatory / provisional / withdrawn;
- evidence path required for mandatory status;
- new defects registered before fixes;
- withdrawn fixtures preserved rather than deleted;
- derived fixture must name adjacent historical class/invariant;
- independent reviewer owns acceptance change;
- audit no longer automatically stops after one finding.

---

# 8. Phase 0 status after second review

Still:

- BUILD_LINT: REVISE
- AUDIT_PROTOCOL: MAJOR REVISE
- ACCEPTANCE_BRIEF_TEMPLATE: REVISE
- CHANGE_CONTROL: REVISE
- FIXTURE_REGISTER: MAJOR REVISE

This is not architecture churn. These are control-plane correctness defects.

Phase 1 should remain blocked until the five documents agree with each other and with the historical evidence.

---

# 9. Next response requested from DeepSeek

Please do not summarize "applied in full."

Instead return:
1. the five revised files;
2. a point-by-point disposition table for every item in this review:
   - ACCEPTED + exact file/section changed;
   - REJECTED + reason;
   - NEEDS EVIDENCE.

Then I will perform one final unit review of Phase 0.
