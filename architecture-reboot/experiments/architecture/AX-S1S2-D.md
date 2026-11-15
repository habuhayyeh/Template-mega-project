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
10. candidate mentioned but explicitly deferred / not independently assessed.

## Frozen inputs

For each case:
- source package;
- signer-approved target note;
- annotated ingest substrate when testing STRUCTURE in isolation;
- exact DC-001 interface contract.

## Artifact under test

Preferred artifact-level output:
- S1 candidates + anchors + salience inputs;
- S2 adoption/relations + approved claim representations;
- S3 rendered-problem set + selected representation;
- S4 final ordered blueprint.

Avoid full final-note generation unless needed for a paired end-to-end check.

## Assertions

### S1
- candidate exists only when subject requires its own current assessment question/status;
- candidacy is source-grounded;
- no adoption verdict appears in S1;
- no final claim selection appears in S1;
- body-only context does not become a fake A/P problem.

### S2
- source temporality is consumed, not re-owned;
- current adoption is adjudicated correctly;
- competing/nested/complementary/contradictory relations are preserved when present;
- approved representation(s) are source-grounded;
- S2 does not expose a choice set requiring further semantic adjudication by S3.

### S3
- only S2-approved representations are selected;
- no new claim is synthesized;
- rendered A/P problem inclusion is correct;
- no A/P problem renders without an approved representation;
- body-only content remains usable without problem promotion.

### S4
- consumes S3 rendered-problem state;
- does not re-decide inclusion or claim;
- final problem order follows centralized ordering contract and S1 salience inputs.

## Run design

- small artifact batch first;
- full batch if schema/output is stable;
- exact same-order batch repeated in 3 fresh conversations;
- diagnostic trace only for failed cases.

## Failure interpretation

- S1 adoption/final-claim leakage -> interface implementation failure; if unavoidable across realistic cases, reopen S1/S2 design.
- S2 cannot provide safe representations without forcing S3 semantic choice -> reopen S2/S3 boundary.
- S4 changes which problems exist or which claims are selected -> authority leak.
- correct, stable boundary behavior -> supports DC-001 STRUCTURE architecture.

## What this experiment cannot prove

It does not test:
- raw-source leakage into RENDER;
- S4 concentration under fixed substrate independently;
- I3 proposition stability;
- test-mode observer effect;
- scale;
- R2 prose expressivity;
- shared-action rendering.
