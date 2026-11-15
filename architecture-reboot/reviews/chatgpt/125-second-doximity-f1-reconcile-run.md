# Review 125 — second Doximity F1 reconciliation run

## Verdict

**PASS for the architectural purpose of File 1, with contract simplification before moving on.**

The revised run corrected the main Review-124 defect:
- heterogeneous omnibus facts were largely split into coherent subjects/trajectories;
- output remained compact and complete;
- reference-backed evidence remained visible;
- event semiology, timeline, baseline behavior, exam/workup, history and unresolved conflicts were separable enough for downstream use.

No further same-case File-1 optimization is justified before testing downstream modules.

## What still failed

### 1. Runtime schema drift

The model did not obey the literal wrapper/grammar exactly:
- it added an explanatory preamble;
- used `@@FACT F01 | ...` headings instead of the specified FACT block grammar;
- omitted the exact `@@HANDOFF ... STATUS=VALID` wrapper.

Because production is GPT-4o inside one Ask context rather than a deterministic parser, this is not itself
a clinical failure. It is evidence that strict parser-like syntax is an unnecessary burden unless a later
mechanical consumer actually requires it.

### 2. `support:` is ambiguous and low-value

The run used `AGREES`, `SINGLE_SOURCE`, `EVOLUTION`, and `CONFLICT`, but some labels mix:
- missing documentation vs true contradiction;
- uncertain detail vs conflict;
- multi-record same-source support vs independent corroboration.

The source refs plus explicit UNRESOLVED entries already carry the useful information.

**Decision:** remove `support:` from F1.

### 3. UNRESOLVED leaked downstream actions

The model invented `next_step:` recommendations such as:
- obtain video/timing strips;
- repeat screening;
- retrieve reports;
- reconcile MAR.

These are action/planning decisions and belong downstream, not in evidence reconciliation.

**Decision:** F1 UNRESOLVED carries only `issue` + `refs`. No recommendation, plan, next step, or requested test.

### 4. Some action content still appears inside FACTs

Executed interventions may remain as factual chronology when they materially affect the episode (e.g.,
a medication was actually given).

Prospective/recommended/planned actions should not be reconciled in F1 except as explicit source reasoning
or when needed to preserve chronology. F2 owns source-level action-state reconciliation.

## Freeze level

F1 is now **provisionally frozen at the behavioral boundary**, not at exact surface syntax.

Required behavior:
- compact source-ID-backed evidence reconciliation;
- one subject/event/state/trajectory per fact;
- local reference completeness;
- explicit source reasoning kept separate;
- unresolved conflicts retained without resolving them;
- no problem identity/role/use;
- no final action/plan decisions.

Exact punctuation, heading style and item count are not frozen.

## Architecture consequence

Do not rerun the same case merely to force exact F1 formatting.

Proceed to F2 Action State using:
- the immutable Scribe packet as evidence store;
- F1 reconciled evidence as context/index;
- source IDs for dereferencing.

Later integrated runs will reveal whether F1 granularity is actually sufficient.
