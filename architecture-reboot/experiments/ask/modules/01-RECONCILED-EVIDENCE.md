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

Return only:

```text
@@HANDOFF F1_RECONCILE_V1
STATUS=VALID

FACT F001
  refs: <comma-separated Scribe record ids>
  fact: <compact source-supported representation>
  time: <CURRENT_EPISODE | ONGOING | HISTORICAL | CURRENT | UNKNOWN>
  support: <AGREES | EVOLUTION | SINGLE_SOURCE | CONFLICT>
  conflict: <none or short unresolved conflict>

FACT F002
  ...

SOURCE_REASONING R001
  refs: <record ids>
  statement: <reasoning explicitly stated by a source>
  stance: <source-qualified wording>

UNRESOLVED U001
  refs: <record ids>
  issue: <what cannot safely be reconciled>

@@END
```

Use only sections that contain entries.

## Goal

Produce the **smallest source-faithful fact map that preserves distinctions needed for later neurologic reasoning**.

Prefer references over copied prose.

The output should be materially smaller than the Scribe packet.

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
FACT F010
  refs: T084,T089,T099
  fact: Returned near baseline after first event, then developed recurrent symptoms the following evening.
  time: CURRENT_EPISODE
  support: EVOLUTION
  conflict: none
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

If sources materially disagree and the disagreement cannot be safely resolved from the supplied evidence:

```text
support: CONFLICT
conflict: <brief description>
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

### 7. Questions

Do not create a FACT from a question alone.

A question may be omitted from the handoff if a clear answer is captured elsewhere and no material
uncertainty is lost.

If an unanswered question itself represents an important unresolved issue, place it in `UNRESOLVED`
with the source record ID.

### 8. Actions

Do not perform full action-state adjudication here.

You may preserve an action mention only when needed to understand factual chronology.

File 2 owns source-level action-state reconciliation.

### 9. Lazy splitting

A Scribe record may contain several propositions.

Do **not** automatically split all of them.

Split/restate only when separate handling is required to preserve:
- different fact times;
- different polarity/certainty;
- a true conflict;
- materially different downstream meaning.

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
6. output is a compact index/representation, not a second copy of the packet.

Return the handoff only.
