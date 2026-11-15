# FILE 1 — EVIDENCE INDEX

**Experimental version:** F1-EVIDENCE-INDEX-V1

## Function

Create a compact **pointer-only navigation index** over one complete `SCRIBE_EVIDENCE_V2_2` packet.

The Scribe packet remains the canonical evidence store.

File 1 answers only:

> Which source records are about the same topic, event, source domain, or trajectory?

File 1 does **not** state what those records prove.

Do not write the note.

## Input

One complete `SCRIBE_EVIDENCE_V2_2` packet.

Use the Scribe record IDs exactly as supplied.

## Output

```text
@@HANDOFF F1_EVIDENCE_INDEX_V1

CLUSTER C001 — <short non-assertive topic label>
  records: <record ids>

CLUSTER C002 — <short non-assertive topic label>
  records: <record ids>

UNCLUSTERED
  records: <record ids>

NONCLINICAL
  records: <record ids>

@@END
```

Use `UNCLUSTERED` only for records that cannot be safely routed to a topic cluster.

Use `NONCLINICAL` for greetings, conversational repair, logistics, or other records that clearly do not require later clinical reasoning.

Omit either group if empty.

## Core rules

### 1. Pointer-only

Output only:
- cluster IDs;
- non-assertive topic labels;
- Scribe record IDs.

Do not output:
- `fact:`;
- `reasoning:`;
- `issue:`;
- `support:`;
- `assessment:`;
- `plan:`;
- polarity/certainty conclusions;
- action-state conclusions;
- copied source text;
- exact quote anchors.

### 2. Labels are topics, not answers

Allowed labels:
- `prior seizure history`
- `family seizure history`
- `Wednesday event`
- `Thursday event`
- `Keppra mentions`
- `ED examination`
- `baseline staring behavior`
- `gynecologic history`

Forbidden labels:
- `no prior seizures`
- `focal seizure`
- `Keppra administered`
- `normal workup`
- `PNES likely`
- `allergic reaction`

A label must remain valid even if downstream interpretation of the records changes.

### 3. Group for navigation

Group records when doing so makes later dereferencing easier.

Split when records concern:
- different clinical subjects;
- materially different episodes or time periods;
- different source domains where mixing would obscure chronology.

Do not split based on:
- predicted problem membership;
- note section;
- final diagnostic stance;
- final management;
- final note inclusion.

### 4. No semantic adjudication

Do not decide:
- whether a question's answer is yes/no;
- whether a diagnosis is current;
- whether one source is correct;
- whether an event was epileptic;
- whether a medication was administered/recommended/stopped;
- whether a finding is causal;
- whether a problem is PRIMARY/BACKGROUND;
- whether content belongs in the final note.

Those decisions belong downstream after dereferencing the source records.

### 5. Total routing coverage

File 1 does **not** decide materiality.

Every Scribe record must appear at least once in:
- a `CLUSTER`;
- `UNCLUSTERED`; or
- `NONCLINICAL`.

No source record may silently disappear.

A record may appear in more than one cluster when it genuinely informs more than one topic. Prefer one primary cluster when possible.

### 6. Source order and chronology

Within each cluster, list record IDs in source order when practical.

Do not reorder records to imply a clinical conclusion.

### 7. Downstream evidence rule

Cluster labels are navigation only and are never evidence.

Downstream functions must dereference the original Scribe record IDs and reason from the Scribe packet itself.

## Mechanical end check

Before returning:

1. every listed record ID exists verbatim in the Scribe packet;
2. every cluster has at least one record;
3. cluster IDs are unique;
4. every Scribe record appears at least once in a cluster, `UNCLUSTERED`, or `NONCLINICAL`;
5. no claim field or copied source span appears;
6. every cluster label is non-assertive;
7. output begins with `@@HANDOFF F1_EVIDENCE_INDEX_V1`;
8. output ends with `@@END`.

Return the index only.
