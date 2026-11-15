# Architecture experiment program

**Status:** DESIGN ONLY / UNRUN  
**Scope:** architecture validation after DC-001  
**Phase 0:** not required to define these experiments; Phase 0 remains out of scope until this program is reviewed.

The interface design is converged, but the architecture is not empirically validated.

The eight architecture experiments are:

1. `AX-S1S2-D` — STRUCTURE authority and claim-representation flow
2. `AX-LEAK` — forbidden-context leakage across logical seams
3. `AX-S4` — S4 decision-concentration reproducibility
4. `AX-I3` — proposition-boundary / object-extraction stability
5. `AX-T` — test-mode observer effect
6. `AX-SCALE` — one-call attention / IR scaling
7. `AX-R2` — R2 expressivity and representation burden
8. `AX-SHARED` — shared diagnostic/management action across problems

The rebuilt K2 case is a fixture inside AX-S1S2-D, not a ninth experiment.

## Common protocol

Use the frozen Doximity protocol:
- artifact-level batches rather than full traces by default;
- exact same frozen batch/order repeated in fresh conversations;
- default reproducibility gate = 3 fresh repetitions;
- diagnostic trace runs are localization-only and never acceptance evidence;
- no Doximity self-scoring;
- external CHECK/AUDIT scoring;
- every assertion has one earliest owning submodule;
- source package + signer-approved target note are the realistic-case baseline;
- raw outputs are immutable;
- order/position robustness is tested only after same-order variance is characterized.

Each experiment must preserve:
- frozen input fixture(s);
- frozen package/instructions;
- predefined assertions;
- raw outputs;
- scorer outputs;
- first-divergence notes;
- final verdict.

A pass means only:
> passed under the tested frozen condition.

No experiment may be used to claim a broader property than it actually tests.
