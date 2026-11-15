# Proposal 133 — Pointer-only File 1 evidence index

**Status:** CANDIDATE — not active runtime yet

## Purpose

Replace synthesized F1 clinical claims with a compact routing index over the immutable Scribe V2.2 packet.

## Core rule

> F1 groups source record IDs. F1 does not state what those records prove.

The Scribe packet remains the evidence store.

## Output

```text
@@HANDOFF F1_EVIDENCE_INDEX_V1

CLUSTER C001 — <non-assertive topic label>
  records: <Scribe record ids>

CLUSTER C002 — <non-assertive topic label>
  records: <Scribe record ids>

UNCLUSTERED_MATERIAL
  records: <material ids that cannot be safely grouped>

@@END
```

Omit `UNCLUSTERED_MATERIAL` when empty.

## Allowed work

F1 may:
- group records about the same clinical subject/event/trajectory;
- separate major episode/time domains;
- assign a short topic label solely for navigation;
- omit obvious conversational repair/filler;
- leave difficult material unclustered rather than interpret it.

## Forbidden work

F1 may not:
- synthesize a clinical fact;
- assign polarity/certainty;
- decide whether a diagnosis is current;
- determine action state;
- infer causality;
- decide problem identity/containment;
- assign PRIMARY/BACKGROUND;
- decide note inclusion/section/order;
- copy large source-text spans;
- create exact-quote proof obligations.

## Topic-label rule

Labels describe **what the records are about**, not what is true.

Allowed:
- `prior seizure history`
- `family seizure history`
- `Wednesday event`
- `Thursday event`
- `Keppra mentions`
- `ED examination`
- `baseline staring behavior`

Forbidden:
- `no prior seizures`
- `focal seizure`
- `Keppra administered`
- `normal workup`
- `PNES likely`

## Grouping rule

Group records only when doing so makes downstream dereferencing easier.

Split when:
- they concern different clinical subjects;
- they concern materially different episodes/time periods;
- mixing them would obscure source chronology.

Do not split because of:
- predicted problem membership;
- future note section;
- final management;
- final diagnostic stance.

## Duplicate record policy

A source record may appear in more than one cluster only when it materially informs more than one distinct
topic and downstream reuse is genuinely useful.

Prefer one primary cluster when possible.

## Coverage

Route all records that may materially affect:
- neurologic history;
- current episode characterization;
- examination/workup interpretation;
- medication/action interpretation;
- safety/functional context;
- later neurologic assessment or management.

The original packet remains available to downstream modules. F1 omission is not evidence deletion.

## Mechanical checks

A non-semantic checker may verify:
- every listed record id exists in the supplied packet;
- cluster IDs are unique;
- every cluster contains at least one record;
- output begins/ends correctly.

No semantic PASS/FAIL validator is part of this candidate.

## Downstream contract

F2 receives:
1. the original Scribe V2.2 packet;
2. this F1 evidence index.

F2 must dereference the original record text when making semantic decisions.

## Experiment

Run this candidate once on the same frozen Scribe V2.2 packet.

Evaluate:
- completion;
- output size;
- whether clusters are navigable;
- whether clinically material source records are routed;
- whether labels remain non-assertive;
- whether GPT-4o avoids claim synthesis despite source content;
- whether downstream semantic work can use the index without needing a copied fact layer.
