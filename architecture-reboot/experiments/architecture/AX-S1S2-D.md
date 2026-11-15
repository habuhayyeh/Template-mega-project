# AX-S1S2-D — STRUCTURE authority and claim-representation flow

**Status:** DESIGN ONLY / UNRUN

## Question

Can the repaired S1 -> S2 -> S3 -> S4 architecture produce correct problem candidacy, adoption, claim representations, note selection, and final ordering **without authority leakage across seams**?

## Architecture claims under test

- S1 owns candidacy/subject identity, not adoption or final claim.
- S2 owns semantic adjudication/adoption and approved claim representations.
- S3 owns rendered A/P problem inclusion and selection only within an S2-safe representation space.
- S4 owns blueprint and final order, not problem inclusion or semantic claim choice.
- A/P problems require approved claim representations.
- body content may remain valid without becoming an A/P problem.

## Required fixture families

At minimum include:
1. prior diagnosis, not referenced/adopted today;
2. historical diagnosis explicitly re-adopted today;
3. historical diagnosis disputed today;
4. current symptom/question with no final diagnosis;
5. explicit differential with two viable alternatives;
6. nested/more-specific claim relationship;
7. body-only historical neurologic fact;
8. historical condition used only as etiology/evidence for another problem;
9. rebuilt K2: explicit current linkage of a continued historical problem to management, so no medication->diagnosis inference is needed;
10. candidate mentioned but explicitly deferred / not independently assessed;
11. explicit contradictory-source case: two source families make incompatible assertions that must remain attributed/adjudicated rather than silently collapsed.

## Frozen inputs

For each case:
- source package;
- signer-approved target note;
- annotated ingest substrate when testing STRUCTURE in isolation;
- exact DC-001 interface contract.

If STRUCTURE is isolated, the ingest substrate must be hand-frozen or come from a separately scored ingest artifact; do not let an unscored same-session ingest error masquerade as a STRUCTURE failure.

## Artifact under test

Preferred artifact-level output:
- S1 candidates + anchors + salience inputs;
- S2 adoption/relations + approved claim representations;
- S3 rendered-problem set + selected representation;
- S4 final ordered blueprint.

Avoid full final-note generation unless needed for a paired end-to-end check.

## Score families

### A. Structural/interface assertions

#### S1
- no adoption verdict appears in S1;
- no final claim selection appears in S1;
- no final render order appears in S1.

#### S2
- source temporality is consumed, not re-owned;
- approved representation(s) are source-grounded;
- S2 does not expose a choice set requiring further semantic adjudication by S3.

#### S3
- only S2-approved representations are selected;
- no new claim is synthesized;
- no A/P problem renders without an approved representation.

#### S4
- consumes S3 rendered-problem state and selected representation;
- does not re-decide inclusion or claim;
- final problem order is owned by S4, using S1 salience inputs rather than an upstream final order.

### B. Semantic correctness assertions

- the right neurologic subjects become S1 candidates;
- body-only context does not become a fake A/P problem;
- current adoption is clinically correct;
- competing/nested/complementary/contradictory relations are faithfully preserved/adjudicated;
- contradictory-source adjudication preserves the non-selected assertion in the IR with its source attribution intact; S2's selected resolution is recorded as a semantic decision rather than implemented by deleting the conflicting source assertion;
- rendered A/P problem inclusion is clinically correct;
- body-only content remains usable without problem promotion;
- final order satisfies the governing clinical/order contract.

Report structural/interface and semantic results separately.

## Run design

- Gate 0 scorer calibration first;
- small artifact batch first;
- executable manifest freezes exact case IDs/count/order/package/scorer versions;
- full batch only if schema/output is stable;
- exact same-order batch repeated in 3 fresh conversations;
- diagnostic trace only for failed cases.

## Architecture-reopen logic

Do **not** use an arbitrary percentage threshold.

A controlled logical counterexample can falsify a universal authority invariant if satisfying the correct clinical/structural requirement requires violating the canonical responsibility boundary.

Before reopening architecture, exclude:
- malformed fixture;
- scorer defect;
- implementation noncompliance;
- missing downstream schema/contract detail.

Ordinary semantic mistakes are implementation/contract/schema defects first.
A reproducible semantic failure becomes architectural when the interface cannot carry the information needed to make the correct decision without authority violation.

## What this experiment cannot prove

It does not test:
- raw-source leakage into RENDER;
- S4 concentration under fixed substrate independently;
- I3 proposition stability;
- test-mode observer effect;
- scale;
- R2 prose expressivity;
- shared-action rendering.
