# How to judge whether File A does its job

**Purpose:** decide whether the ingestion/reconciliation layer is correct enough to build on, and when it
actually needs another field, rule or pass.

File A is not judged by final note quality. It is judged by whether it preserves the distinctions B/C
need, without inventing meaning.

## The one question

> Given the original Scribe packet, can a competent downstream function make the correct problem and
> note decisions from File A's ledger plus the records File A cites?

If yes, A did its job. If B has to reread the whole packet to recover a distinction A dropped, A failed
at that distinction. If B fails because it made a bad problem decision, that is B, not A.

## Five things to measure

### 1. Structural validity

Mechanical:

- every unit parses;
- every cited record exists;
- every selector resolves to the cited record;
- required fields are present;
- no forbidden decisions (problem, role, section, plan, prose);
- action fields are legal;
- output ends correctly.

A single structural failure means the handoff is not usable. Fix before judging content.

### 2. Fatal fidelity

These are hard failures. One is enough to fail the run:

- invented patient fact;
- wrong speaker/source attribution;
- historical promoted to current;
- negation flipped;
- certainty strengthened;
- question treated as answer;
- action upgraded (`recommended` -> `ordered` -> `performed` -> `resulted`);
- two distinct events merged in a way that changes meaning;
- counterevidence lost;
- outside-service diagnosis turned into Neurology adoption.

### 3. Coverage

Did A preserve every **material distinction**?

Not every sentence. Every distinction that could change:

- problem identity;
- current state;
- causal reasoning;
- action state;
- exam/workup interpretation;
- functional/safety context;
- final management.

Each source record should be either represented by a unit, cited by a unit, or explicitly excluded as
nonassertion. Silent omission is the failure.

### 4. Reconciliation correctness

For records that overlap, did A choose correctly among:

- duplicate/corroboration;
- same state but different source;
- possible overlap with unresolved identity;
- evolution over time;
- true conflict;
- independent material.

False merge and false split are both errors. A must be allowed to say `possible_overlap` or `unresolved`
rather than force a decision.

### 5. Downstream recoverability

Give B only:

- A's ledger;
- the exact records A cites;
- no full packet.

Can B produce the correct problem map? This tests whether A preserved enough meaning and pointers. If B
needs uncited records, A missed a material distinction or a selector.

## Test set: small probes, not one long note

Use 10–15 synthetic packets of 3–10 records. Each isolates one distinction. Small probes let you
attribute the failure.

Minimum probes:

1. **Baseline sparse packet** — falls + historical stroke, no consult context.
2. **Duplicate/corroboration** — same event in transcript and note.
3. **Two similar events** — same symptom, different times; must not merge.
4. **Evolution** — baseline, worsening, recovery; one trajectory.
5. **True conflict** — same field, same time, incompatible values.
6. **Question vs answer** — clinician asks, patient answers, collateral answers.
7. **Patient vs collateral vs objective** — same symptom, three sources.
8. **Historical disease + new symptom** — no automatic linkage.
9. **Residual deficit vs new worsening** — contained vs current change.
10. **Action states** — recommended, ordered, performed, result pending/final.
11. **Medication list vs adherence** — listed is not taken.
12. **Nonproblem content** — exam, meds, workup, history survive without becoming problems.
13. **Multi-assertion record** — selector required; whole-record citation is insufficient.
14. **Sparse/insufficient packet** — A must not invent a problem or consult reason.
15. **Outside-service diagnosis** — attributed formulation, not Neurology adoption.

Each probe has:

- required units;
- forbidden claims;
- expected relations;
- expected action fields;
- expected unresolved;
- expected nonproblem preservation.

## Scoring

Score per probe, not one aggregate impression.

| dimension | target |
|---|---|
| structural validity | 100% |
| fatal fidelity | 0 fatal errors |
| material coverage | ≥95% of expert-marked distinctions |
| reconciliation | ≥90% correct on probes; 0 false merges of distinct events |
| action state | 100% on action probes |
| nonproblem preservation | ≥95% |
| downstream recoverability | B succeeds on ≥90% probes from A + cited records |
| stability | 3 runs; no fatal variance; grouping consistent |

Thresholds are calibration aids, not natural law. A single fatal error overrides a high average.

## How to run it

1. Create synthetic/de-identified probes; keep patient content out of the repo.
2. Run A on the exact Scribe packet.
3. Score structural validity first.
4. Score fatal fidelity.
5. Score coverage and reconciliation.
6. Run B on A + cited records only.
7. Log each failure by category.
8. Re-run the full probe set after any A change.

Do not tune A against one long real packet. Use the long packet for realism, the probes for diagnosis.

## When A needs something new

Add only for a repeated, specific failure:

- **A new field** — a distinction is repeatedly lost and cannot be recovered from the cited record.
- **A new selector rule** — multi-assertion records keep producing wrong support.
- **A new unit type** — a whole class of material has no representation (e.g., nonproblem exam).
- **A split pass** — A is structurally valid but one category (action state) repeatedly fails and cannot
  be stabilized inside the lane.
- **A new rule** — the same fatal error appears across different probes.

Do not add:

- a field B never uses;
- a pass because a category exists conceptually;
- an audit/validator stage to catch errors A should not make;
- more prose rules when the failure is missing structure.

## Decision rule

A is good enough to build B when:

1. structural validity is 100%;
2. fatal fidelity is 0 on the probe set;
3. material coverage and nonproblem preservation meet target;
4. B can make correct problem decisions from A + cited records on the probe set;
5. three runs are stable.

If A passes, build B. If A fails one category repeatedly, fix that category. If A fails everywhere,
the unit schema is wrong, not the prompt.

No Gate-0 acceptance. No Doximity production change. No Phase 0.
