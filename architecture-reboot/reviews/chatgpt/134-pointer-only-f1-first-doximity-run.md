# Review 134 — first Doximity run of pointer-only F1

## Verdict

**PARTIAL PASS — claim-layer problem solved; navigation granularity needs one bounded correction.**

## What worked

### 1. Total routing coverage

The run routed all transcript records T001-T294 exactly once and all ED-note records P1.001-P1.056.

There were no silent record omissions.

### 2. Pointer-only contract

The output contained:
- cluster ids;
- non-assertive labels;
- record ids;
- NONCLINICAL.

It did not recreate:
- synthesized `fact:` prose;
- copied quote anchors;
- action-state judgments;
- diagnostic conclusions;
- semantic validator output.

This confirms the core D-046 architecture is viable.

### 3. Completion and compactness

The handoff completed with `@@END` and remained substantially smaller than any source-reproduction design.

## Material defect — navigation granularity

Several clusters are too broad to function as useful navigation.

Examples:
- `Past medical history, family history, and gynecologic history`;
- `Substance use, social history, and functional context`;
- `Evaluations, diagnostics, and Keppra-related records`;
- `Counseling, workup planning, and disposition`;
- the entire P1.001-P1.056 note under one `ED documentation` cluster.

The last case is especially important: a source-wide clinical catch-all defeats the purpose of an evidence
index. Downstream modules would still have to rescan the entire ED note rather than follow topic pointers.

## Material defect — provenance context misclassified as NONCLINICAL

Transcript records identifying speaker/collateral roles were placed in NONCLINICAL.

Examples include records identifying:
- the fiance;
- the mother;
- which collateral was actually on the cruise.

Those are not clinical claims, but they are **provenance/navigation context** and can materially affect later
attribution.

They should route to a non-assertive topic such as:
`source and collateral identities`.

## Design correction

Keep pointer-only F1.

Add three bounded routing rules:

### A. Topic beats source catch-all

Clinical records from a note should be routed into topic clusters, preferably alongside transcript records
about the same topic.

Do not place an entire clinical source/document into one catch-all cluster such as `ED documentation`
when it contains multiple distinct navigation topics.

### B. One navigation topic per cluster

A cluster may contain a large coherent episode/trajectory.

Do not combine unrelated domains merely to reduce cluster count.

A practical test:

> If the label needs to enumerate multiple independent domains, split them.

This does not require predicting problem identity or note use.

### C. Provenance context is not NONCLINICAL

Records that establish:
- speaker identity;
- collateral role;
- whether a collateral witnessed the event;
- source participation relevant to attribution;

must route to a provenance/source-context cluster.

NONCLINICAL is reserved for material that is not needed later for clinical interpretation **or provenance**.

## Next experiment

Patch File 1 only.

Rerun pointer-only F1 on the same frozen packet.

Pass criteria:
- total routing coverage remains complete;
- no claim layer returns;
- no source-wide clinical catch-all;
- topic clusters integrate cross-source records where useful;
- provenance/source identity is retained outside NONCLINICAL;
- cluster labels remain non-assertive.

No F1V.
No File 2 yet.
