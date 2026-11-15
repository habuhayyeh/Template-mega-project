# Review 121 — File 1 atomicization execution failure

## Evidence

A real Doximity Ask/GPT-4o run was performed with the earlier File 1 atomic-evidence design.

Observed output:
- output header was F1_EVIDENCE_V1 (older schema);
- 175 evidence objects were emitted;
- output terminated mid-record;
- no closing handoff marker was produced;
- the run did not finish the source packet;
- the output was approximately 26.5 KB while the input Scribe packet was approximately 34.7 KB.

The run therefore expanded a large fraction of the packet before reaching the later source material.

## Interpretation

This is not primarily a KIND/STANCE-schema defect.

The material failure is **global atomicization cardinality**:

> one Scribe packet record -> one or many rewritten evidence objects across the entire packet

creates a second near-full copy of the encounter before any clinically useful reconciliation occurs.

F1-EVIDENCE-V2 would reduce ontology ambiguity but would preserve the same one-to-many global expansion.
It is therefore not worth rerunning as the immediate next experiment.

## Architecture consequence

The Scribe V2.2 packet should remain the immutable source/evidence store.

Ask modules should prefer:
- compact references to Scribe record IDs;
- reconciliation decisions;
- retained conflicts/evolution;
- problem/use decisions;

rather than repeatedly copying source content into successive intermediate representations.

This restores an important original reboot principle: stable source-linked evidence should be referenced
rather than repeatedly rewritten.

## Design correction

Remove global atomicization as a standalone Ask function.

Treat Scribe as having already completed enough high-recall extraction for the production surface.

The first Ask semantic function should instead perform **source reconciliation/compression by reference**:
- collapse obvious duplicate/source-overlapping statements;
- preserve longitudinal evolution;
- preserve true conflict;
- retain source IDs;
- produce a compact reconciled fact set;
- do not decide final neurologic problem identity, encounter role, or final plan.

Only split a Scribe record locally when a material semantic distinction requires separate handling.

This is **lazy decomposition**, not global atomic decomposition.

## Runtime implication

Candidate chain becomes:

1. F1 Reconciled Evidence
2. F2 Action State
3. F3 Problem Architecture (internal S1 -> S2 -> S3 checkpoints)
4. F4 Note Compiler (S4)
5. F5 Renderer
6. F6 Output Guard

The number of files is empirical, not sacred.

## Phase-0 implication

The old AX-I3 assumption that a global proposition object set should be produced before later structure
must be reconsidered after this evidence.

Future acceptance should test whether clinically meaningful distinctions survive into downstream
decisions, not require a globally materialized atomic object for every source proposition unless that
materialization proves necessary.

No Phase-0 edit is made in this review.

## Next experiment

Run the new compact F1 reconciliation function on the same frozen Scribe packet.

Success is:
- complete output;
- materially smaller than the source packet;
- source references preserved;
- duplicate/evolution/conflict handling useful;
- no final problem/role/note decisions.
