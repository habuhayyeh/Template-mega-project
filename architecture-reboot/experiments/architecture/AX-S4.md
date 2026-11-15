# AX-S4 — S4 decision-concentration reproducibility

**Status:** DESIGN ONLY / UNRUN

## Question

Is S4 too semantically dense to execute reproducibly even when S1/S2/S3 outputs are fixed and correct?

## Architecture claim under test

S4 can remain one top-level submodule while internally freezing:
- section assignment;
- render-unit grouping;
- member roles;
- rhetorical class;
- operator;
- final problem/unit order;
- reuse;
- completeness.

## Frozen inputs

Hold identical:
- S1 candidates + salience inputs;
- S2 adjudicated relations/adoption + approved claim representations;
- S3 rendered-problem set + exactly one selected representation per rendered A/P problem + retained-use map;
- section/style/operator contracts.

No raw-source ambiguity should be needed to make the tested S4 decisions.

This is an S4 ceiling test under fixed upstream substrate, not a claim about production end-to-end behavior.

## Fixture families

Include cases stressing:
1. simple single-problem A/P;
2. multiple evidence objects;
3. duplicate/covered objects;
4. conditional plan;
5. multiple problems;
6. body + A/P placement;
7. explicit reuse;
8. standing item;
9. differential claim representation;
10. S2 had multiple semantically selection-safe representations, S3 selected exactly one, and S4 must honor that exact selected representation without revisiting alternatives;
11. shared-action case may be excluded here and tested separately in AX-SHARED unless its representation is already frozen.

A fixture that hands S4 two unselected representations is malformed upstream structure, not a valid ambiguity stress case.

## Scored dimensions

Score independently:
- section assignment;
- unit grouping;
- member roles;
- rhetorical class;
- operator selection;
- final problem order;
- unit order;
- reuse accounting;
- completeness/accounting validity;
- fidelity to S3's selected claim representation.

Do not collapse into one S4 pass percentage.

## Run design

- Gate 0 scorer calibration first;
- artifact-level S4 batch only;
- freeze exact case IDs/count/order/package/scorer versions;
- repeat exact same frozen batch/order in 3 fresh conversations;
- if any family is unstable, use a diagnostic single-case trace and then a targeted S4-only confirmation.

## Interpretation

### Stable and correct
Supports keeping S4 as one architectural submodule under the tested fixed-substrate condition.

### Stable and wrong
Contract/schema/representation defect, not stochasticity.

### Drift localized to one S4 decision family
Prefer internal ordered functions inside S4 before adding a new top-level submodule.

### Independent recurrent drift across several S4 families
Reconsider whether S4 needs a separately auditable internal seam or architectural split.

## Reopen criterion

Do not split S4 merely because it has many responsibilities.
Split only if evidence shows:
- a distinct decision family is independently unstable;
- it has a separable input/output contract;
- and isolating it would improve auditability without duplicating authority.
