# SUPERSEDED — DO NOT RUN

Active File 1 is now `01-EVIDENCE-INDEX.md` (pointer-only). Semantic F1V has been removed from the active runtime after false-PASS evidence and DeepSeek architecture review 029.

# FILE 1 — RECONCILED EVIDENCE

**Experimental version:** F1-RECONCILE-V1

## Function

Transform one Scribe V2.2 packet into a **compact reconciled evidence map** for the next Ask function.

The Scribe packet remains the canonical evidence store and remains available to downstream functions. The handoff is an index/reconciliation layer, not a replacement evidence corpus.

Downstream functions may dereference any cited Scribe record ID when finer detail is needed.

Do not copy every Scribe record into the output.
Do not create one output object per source proposition.
Do not write the note.

## Input

One complete `SCRIBE_EVIDENCE_V2_2` packet.

Use its record IDs as stable evidence references.

## Output

Return a compact handoff with three optional record families:

```text
@@HANDOFF F1_RECONCILE_V1

FACT F001 — <short subject label>
  fact: <compact source-supported representation>
  refs: <Scribe record ids>

SOURCE_REASONING R001 — <short subject label>
  reasoning: <reasoning explicitly stated by a source>
  refs: <Scribe record ids>

UNRESOLVED U001 — <short subject label>
  issue: <material conflict/uncertainty that cannot be safely reconciled>
  refs: <Scribe record ids>

@@END
```

Use only record families that contain entries.

The exact punctuation/heading style is not clinically important. The semantic fields are.

Do **not** add extra fields such as:
- `support:`;
- `next_step:`;
- `recommendation:`;
- `plan:`;
- `action:`.

F1 is an evidence-reconciliation handoff, not a planning module.

## Goal

Produce a **compact source-faithful fact map that preserves distinctions needed for later neurologic reasoning and note construction**.

Prefer references over copied prose.

Do not minimize FACT count at the expense of downstream separability. A somewhat larger complete handoff is better than a smaller handoff that bundles unrelated clinical subjects.

The output should remain materially smaller than the Scribe packet.

## Reconciliation-unit invariant

Each `FACT` must describe **one clinical subject/event/state or one coherent longitudinal trajectory**.

Multiple records may be combined only when they are:
- duplicate/corroborating statements about that same subject;
- different observations of the same event;
- or a meaningful evolution of that same subject over time.

Do not create omnibus FACTs that combine unrelated domains merely because they belong to the same patient or
the same note section.

Examples of content that normally stays separate unless one directly modifies the other:
- current neurologic presentation vs past medical history;
- family history vs unrelated gynecologic history;
- medication/supplement regimen vs employment/residence;
- examination findings vs allergy/PCP/admin state.

### Downstream-separability test

Before merging two propositions, ask:

> Could a later function reasonably need to give these different problem membership, temporal stance,
> section placement, inclusion/disposition, or action handling?

If yes, keep them as separate FACTs.

### Reference validity

Every `refs:` id must appear **verbatim as a record id in the supplied Scribe packet**.

Do not:
- invent a record id;
- transpose `T###` into `P1.###` or vice versa;
- cite a nearby record because it discusses the same topic;
- cite a question-only record as evidence that its answer is true;
- cite a record that does not support the clause merely because it is in the same conversation/topic.

A question-only record may support only the fact that the question was asked or that an issue remained unresolved. It cannot support the answer unless the answer is contained in that same record.

### Local reference completeness

Every independently meaningful clause in a `fact:` line must be supported by at least one record id listed
in that same FACT's `refs:`.

Do not include a clause because it exists somewhere else in the packet unless its supporting record id is
also listed here.

A FACT is invalid if its wording cannot be audited from its own `refs:`.

Each cited ref must support at least one clause in that item. Remove unrelated/question-only refs rather than padding the citation list.

## Reconciliation rules

### 1. Duplicate / overlapping source statements

When multiple records state the same clinically meaningful proposition, create one FACT and list all
supporting record IDs.

Do not preserve duplicate wording merely because it came from multiple sources.

### 2. Longitudinal evolution

When records describe change over time, preserve the trajectory in one FACT when this can be done without
losing a material distinction.

Example:

```text
FACT F010 — episode trajectory
  fact: Returned near baseline after first event, then developed recurrent symptoms the following evening.
  refs: T084,T089,T099
```

Do not call temporal evolution a contradiction.

### 3. Different evidence modalities

Patient report, collateral report, examination, and test result may refer to the same clinical issue but
are not interchangeable.

Do not collapse:
- patient-reported weakness;
- objective weakness on exam;

into one objective fact unless the exam actually supports it.

A FACT may cite both only if its wording preserves the distinction.

### 4. True conflict

If sources materially disagree and the disagreement cannot be safely resolved from the supplied evidence, preserve the disagreement as an `UNRESOLVED` item:

```text
UNRESOLVED U010 — episode duration
  issue: Witness and document estimates materially disagree.
  refs: T066,T125,P1.016
```

Do not choose a winner merely because one source is more polished or already written as a note.

### 5. Historical status

A historical disease/event identity may persist.

A historical **status** does not automatically persist.

Do not turn:
`historical seizure-free`
into
`currently seizure-free`
without current support.

### 6. Explicit source reasoning

Keep source reasoning separate from reconciled facts.

Examples:
- source clinician says seizure is possible;
- prior neurologist favored a diagnosis;
- patient/collateral suspected an allergic trigger.

Do not convert source reasoning into final encounter truth here.

Do not create a new negative conclusion from silence. Absence of a documented causal link, diagnosis, trigger, or relationship does not itself justify a FACT saying that no such link exists. If the unresolved relationship is clinically material, preserve it as `UNRESOLVED` without deciding it.

### Attribution caution

For transcript records, preserve what the record actually establishes.

Do not infer a stable real-world identity for `SPK0`, `SPK1`, etc. across the transcript unless the packet itself explicitly establishes that identity in the relevant record/context.

When speaker identity is uncertain, prefer source-neutral wording such as:
- "transcript reports...";
- "collateral report...";
- "one speaker reports...";

rather than inventing "patient", "mother", "fiance", or another role.

### 7. Questions

Do not create a FACT from a question alone.

A question may be omitted from the handoff if a clear answer is captured elsewhere and no material
uncertainty is lost.

If an unanswered question itself represents an important unresolved issue, place it in `UNRESOLVED`
with the source record ID.

`UNRESOLVED` should describe source-level uncertainty/conflict. Do not invent a new diagnostic-classification problem unless a source explicitly states that uncertainty.

### 8. Actions

Executed interventions may appear inside a FACT only when the source explicitly establishes that they occurred and they are needed to preserve the chronology or clinical state of that subject/event.

Do not reconcile prospective/recommended/planned/ordered/discontinued actions in F1 unless the action state itself is the clinical fact needed for chronology. Never collapse a sequence of action states into a statement that treatment was administered.

Do not generate recommendations, next steps, tests to obtain, records to retrieve, or management suggestions.

File 2 owns source-level action-state reconciliation. Final encounter plan/adoption remains downstream.

### 9. Lazy splitting

A Scribe record may contain several propositions.

Do **not** automatically split all of them.

Split/restate when separate handling is required to preserve:
- different clinical subjects/events;
- different fact times;
- different polarity/certainty;
- a true conflict;
- different likely problem membership;
- different likely note-section/use decisions;
- materially different downstream meaning.

Do not keep propositions together solely to reduce output length.

Otherwise keep them together in one compact reconciled fact.

## Forbidden decisions

Do not decide:
- what is an independent neurologic problem;
- what is contained under another problem;
- the final current encounter diagnosis/stance;
- PRIMARY vs BACKGROUND;
- causal/contributory relations unless merely preserving explicit source reasoning;
- which content renders;
- section assignment;
- problem order;
- final plan;
- note prose.

## Completeness rule

Do not aim to reproduce every conversational detail.

Preserve every **clinically meaningful distinction** that could change:
- neurologic problem identity;
- current state/certainty;
- causal reasoning;
- action state;
- examination interpretation;
- workup interpretation;
- functional/safety context;
- final neurologic management.

Low-value conversational repair, repeated questioning, and redundant restatement need not appear in the
handoff when the underlying evidence is preserved by reference.

Compression must preserve enough source IDs that downstream functions can recover omitted detail from the original packet without relying on the reconciled wording alone.

## End check

Before returning:
1. output is complete and ends with `@@END`;
2. every FACT/REASONING/UNRESOLVED item cites Scribe record IDs;
3. no source conflict was silently resolved;
4. no historical status became current;
5. no final problem/role/note decision was made;
6. every independently meaningful clause is supported by one of that item's own refs;
7. no FACT combines unrelated downstream decision units merely to reduce item count;
8. every ref exists verbatim in the input packet;
9. no question-only record is used as evidence for an answer;
10. no administered/performed action is inferred from recommendation/order/discontinuation alone;
11. transcript speaker identity is not invented from SPK labels;
12. no recommendation/next-step/plan field was invented;
13. no `support:` label was added;
14. output is a compact index/representation, not a second copy of the packet.

Return the handoff only.
