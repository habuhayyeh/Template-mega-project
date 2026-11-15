# AX-T — test-mode observer effect

**Status:** DESIGN ONLY / UNRUN

## Question

Does requesting observable Case IR materially change final-note behavior compared with production-shaped final-note-only output?

## Architecture claim under test

Test-mode evidence is representative enough of production behavior to support predeployment validation claims under the tested condition.

## Paired arms

For the exact same:
- source package;
- implementation package;
- case order;
- Doximity mode/settings;
- all instructions except the additional standard test-mode output request;

run:

### Arm A — production-shaped
Final note only.

### Arm B — standard test mode
Same final note plus the standard observable Case IR / execution artifact.

Do not use a rich diagnostic trace as Arm B; diagnostic traces are a different run type and are never acceptance evidence.

The measured observer effect explicitly includes the effect of the instruction that requests the additional artifact. Do not pretend instrumentation can be separated from that request.

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

- Gate 0 scorer calibration first;
- use a representative multi-case batch;
- freeze exact case IDs/count/order/package/scorer versions;
- repeat A and B in separate fresh conversations, same frozen order, default 3 repetitions per arm.

## Interpretation

### No material difference
Supports transfer of test-mode validation to production-shaped behavior under tested conditions.

### Test mode materially improves behavior
Observed test-mode success may overestimate production reliability.

### Test mode materially worsens behavior
Instrumentation imposes a burden and may invalidate direct transfer of acceptance evidence.

## Architecture consequence

If observer effect is material:
- production acceptance needs a dedicated final-note-only evidence layer;
- test IR remains useful for diagnosis but cannot be treated as behaviorally neutral;
- consider reducing emitted telemetry.

This experiment does not test diagnostic-trace equivalence; traces remain diagnostic-only by rule.
