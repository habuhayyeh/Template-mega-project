# Architecture experiment program

**Status:** DESIGN ONLY / UNRUN  
**Scope:** architecture validation after DC-001  
**Phase 0:** remains out of scope until this experiment program is reviewed/frozen.

The interface design is converged and DC-001 is APPLIED / VERIFIED, but the architecture is not empirically validated.

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

## Gate 0 — scorer calibration

Before any scored architecture experiment produces acceptance evidence, the relevant CHECK/AUDIT scorer must pass a known-bad seeded-defect calibration for the predicates it will score.

- scorer calibration is offline unless the runtime contract itself is under test;
- runtime invalid probes are separate;
- one calibration may serve a campaign while scorer logic and predicate definitions are unchanged;
- a materially changed scorer or predicate family requires recalibration.

Gate 0 is a prerequisite, not a ninth architecture experiment.

## Common protocol

Use the frozen Doximity protocol:
- artifact-level batches rather than full traces by default;
- exact same frozen batch/order repeated in fresh conversations;
- default reproducibility gate = 3 fresh repetitions;
- claims are scoped as "passed/agreed under this frozen condition", not population stability estimates;
- diagnostic trace runs are localization-only and never acceptance evidence;
- no Doximity self-scoring;
- external CHECK/AUDIT scoring;
- every assertion has one earliest owning submodule;
- source package + signer-approved target note are the realistic-case baseline;
- raw outputs are immutable;
- order/position robustness is tested only after same-order variance is characterized.

Each executable experiment manifest must freeze:
- case IDs and case count;
- exact fixture content;
- case order;
- package/instruction version;
- control-plane version when one governs the scorer/run;
- predefined assertions;
- scorer/version;
- run type.

Batch size is empirical, not globally fixed:
- start small for a new artifact shape;
- escalate only if output completeness/schema stability remain intact;
- realistic signer cases and purpose-built micro-fixtures may both be used where appropriate.

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

## Program-level interaction check

Eight independent passes do not prove that all eight properties compose.

After the relevant component experiments pass, run targeted crossed conditions for high-risk interactions. At minimum:
- repeat the high-risk AX-LEAK omitted-fact condition under a high but realistic AX-SCALE condition.

Any crossed condition supports only that interaction.

A later integrated end-to-end campaign is still required before claiming whole-system composition.

## Paste-layout prerequisite

AX-I3 intentionally begins from fixed source spans and therefore does not test whether the production paste is parsed into those boundaries correctly.

Before production-shaped claims depend on I1/I2 source boundaries, run a separate ingestion/deployment paste-layout characterization covering the production layouts actually contemplated:
- transcript;
- last neurology note;
- other current notes;
- imaging;
- recent labs;
- relevant historical labs;
- source ordering/layout variations.

This is a prerequisite/characterization obligation, not currently a ninth architecture experiment.

## Integrated preflight screen (not a ninth experiment)

A single 3-run screen over the **raw paste → Case IR** path, as a program-level gate rather than an
acceptance experiment.

It is not redundant: every isolated experiment freezes its input, so none exercises ingest and its
boundaries together. The preflight is the only screen that sees the whole path.

It never counts as an experiment, never replaces one, and a pass states only that the pipeline runs end
to end under the tested condition.

## Program dependencies before scoring

- **S4 ordering.** No ordering predicate may be scored until the ordering contract and its salience
  values are frozen. Until then `S4-ORD-01` and its seed stay `PENDING_DEPENDENCY`.
- **AX-R2 targets.** AX-R2 cannot start without signer-quality HPI/history prose targets. Synthetic
  specimens are not a substitute: the experiment measures representation burden against real targets.
- **AX-SHARED occurrence policy.** Once versus once-plus-reference is a product decision and stays
  `PENDING_SIGNER`.

## No self-attested totals

Artifacts must not carry aggregate counts they are also asserting. Where a count matters, CHECK derives
it; a self-declared total is a claim the scorer cannot verify and will eventually contradict.
