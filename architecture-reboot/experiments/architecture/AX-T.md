# AX-T — test-mode observer effect

**Status:** DESIGN ONLY / UNRUN

## Question

Does requesting observable Case IR / trace materially change the final note behavior compared with production-shaped final-note-only output?

## Architecture claim under test

Test-mode evidence is representative enough of production behavior to support predeployment validation claims.

## Paired arms

For the exact same:
- source package;
- implementation package;
- case order;
- Doximity mode/settings;

run:

### Arm A — production-shaped
Final note only.

### Arm B — standard test mode
Same final note plus the standard observable Case IR / execution artifact.

Do not use a rich diagnostic trace as Arm B; diagnostic traces are a different run type and are never acceptance evidence.

## Primary comparison

Score the **final note** in A vs B using the same frozen production-relevant assertions.

Do not require hidden/internal equivalence for properties production never emits.

## Metrics

- semantic fidelity;
- problem inclusion;
- plan inclusion;
- section correctness;
- operator/payload-visible conformance where inferable;
- omission/fabrication;
- structural completeness;
- reproducibility within each arm.

## Run design

Use a representative multi-case batch.
Repeat A and B in separate fresh conversations, same frozen order, default 3 repetitions per arm.

## Interpretation

### No material difference
Supports transfer of test-mode validation to production-shaped behavior under tested conditions.

### Test mode materially improves behavior
Observed test-mode success may overestimate production reliability.

### Test mode materially worsens behavior
Instrumentation imposes a burden and may invalidate acceptance runs.

## Architecture consequence

If observer effect is material:
- production acceptance needs a dedicated final-note-only evidence layer;
- test IR remains useful for diagnosis but cannot be treated as behaviorally neutral;
- consider reducing emitted telemetry.

This experiment does not test diagnostic-trace equivalence; traces remain diagnostic-only by rule.
