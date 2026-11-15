# AX-SCALE — one-call attention and IR scaling

**Status:** DESIGN ONLY / UNRUN

## Question

Does explicit source accounting + Case IR machinery remain usable at realistic consult size, or does auditability itself degrade model accuracy through attention/resource load?

## Architecture claim under test

The one-call architecture can carry enough explicit structure for real neurology cases without unacceptable degradation before realistic source volume is reached.

## Core design

Hold the decisive clinical core constant.

Characterize burden variables separately where feasible rather than increasing everything at once:
- raw source volume;
- number of source spans;
- number of semantic objects;
- Case-IR/accounting size;
- number of source documents;
- transcript length;
- cases per batch;
- requested output/telemetry burden.

Do not change the correct final clinical conclusion.

After single-variable characterization, selected combined levels may be tested.

## Levels

Do not freeze an arbitrary byte/token threshold.
Use empirically defined levels such as:
- small;
- moderate;
- realistic-large;
- stress.

Record actual input/output size and relevant count variables for each run.

## Scoring

By layer:

### I1/I2
- source recognition;
- span completeness;
- late-source omission.

### I3/I4
- decisive proposition recall;
- fabrication;
- anchor/provenance accuracy.

### S1-S4
- problem/claim/adoption correctness;
- unit/operator/order correctness;
- accounting completeness;
- malformed schema.

### Final note
- clinically decisive fidelity;
- missing plan/reasoning;
- truncation;
- late-case degradation.

## Run design

- Gate 0 scorer calibration first;
- use the same core case across scale levels;
- where practical, include more than one clinical core to avoid overfitting to one case shape;
- freeze exact level definition, case IDs, package/scorer versions;
- repeat each frozen level in fresh conversations.

## Failure attribution

Do not classify every scale failure the same way.

### 1. Hard platform/output limit
Examples: truncation or a Doximity-specific capacity ceiling.

Interpretation:
> deployment/platform constraint first.

### 2. Representation/schema burden
Behavior degrades because the explicit schema/accounting is unnecessarily verbose.

Responses first:
- compress IR;
- derive bookkeeping mechanically;
- reduce emitted telemetry;
- use sparse references.

Interpretation:
> schema/build problem first.

### 3. Unavoidable realistic-volume failure intrinsic to the representation strategy
If realistic required source volume remains unreliable after reasonable prompt/schema/telemetry mitigation:

> representation architecture may need reopening.

Do not reopen module topology merely because a stress level exceeds the platform.

## Interaction follow-up

After AX-LEAK and AX-SCALE individually pass, repeat the high-risk AX-LEAK omitted-fact condition under a high but realistic scale condition.

That result supports only that interaction.
