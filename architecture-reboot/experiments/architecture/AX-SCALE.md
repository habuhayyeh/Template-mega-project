# AX-SCALE — one-call attention and IR scaling

**Status:** DESIGN ONLY / UNRUN

## Question

Does explicit source accounting + Case IR machinery remain usable at realistic consult size, or does auditability itself degrade model accuracy through attention/resource load?

## Architecture claim under test

The one-call architecture can carry enough explicit structure for real neurology cases without unacceptable degradation before realistic source volume is reached.

## Core design

Hold the decisive clinical core constant.

Create a controlled ladder that progressively adds:
- irrelevant chart context;
- relevant-but-nondecisive historical context;
- additional source documents;
- longer transcript context;
- more source spans/objects;
- more accounting records.

Do not change the correct final clinical conclusion.

## Levels

Do not freeze an arbitrary byte/token threshold.
Use empirically defined levels such as:
- small;
- moderate;
- realistic-large;
- stress.

Record actual input/output size for each run.

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

Use same core case across scale levels.
Where practical, include more than one clinical core to avoid overfitting to one case shape.
Repeat each frozen level in fresh conversations.

## Interpretation

If failure rises sharply before realistic source volume:
- compress IR representation;
- derive some bookkeeping mechanically;
- reduce emitted telemetry;
- use sparse refs instead of verbose repeated payloads.

Only reopen module topology if representation/schema compression cannot make realistic cases tractable.
