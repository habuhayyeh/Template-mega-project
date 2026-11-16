# Review 150 — Post-D053 architecture review

## Verdict

**D-053 is directionally correct, but the architecture is not ready to run C yet.**

Retiring B1/action-state enums was the right move. The clean-packet A->B run is the strongest execution result so
far. However, three architectural gaps remain before the compiler/render boundary is trustworthy:

1. A may now be redundant or over-semantic for the cleaner Scribe packet.
2. B owns reconciliation but does not emit enough reconciled event structure for C to compile HPI without
   re-deciding it.
3. Current C does not implement the typed-group + canonical-operator boundary that prior Doximity experiments
   already showed to be the most stable rendering architecture.

These are architecture issues, not reasons to reopen action-state enums.

---

## 1. Re-test whether A is still necessary

### Why this is architectural

The cleaner `SCRIBE_EVIDENCE_V2_2` packet is already:
- source-separated;
- record-ID-stable;
- concise;
- one or a few clinically coherent assertions per record;
- explicit about speaker/provenance;
- sufficiently structured for the target note.

A then expands that packet into another long semantic/action corpus.

In the latest clean run, A introduced or has previously introduced:
- pointer drift;
- mixed-polarity errors;
- ambiguous result polarity;
- action-coverage risk.

This creates a serious no-human-intermediate-review problem:

> B is forbidden to discover an action absent from A, but A is a generative stage that can omit actions.

An A omission therefore becomes an irreversible **omission sink**.

### Recommendation

Do not delete A yet.

Run one controlled architecture experiment:

**Arm 1 — current**
`Scribe -> A -> B`

**Arm 2 — direct**
`Scribe -> B-direct`

B-direct should cite exact Scribe record IDs/selectors itself and preserve the same constraints:
- no invented facts/actions;
- source-qualified wording;
- problem architecture;
- diagnostic stance;
- action ownership;
- unresolved rather than guessing.

Compare:
- clinical coverage;
- attribution/provenance fidelity;
- action preservation;
- problem architecture;
- final B concision;
- hidden semantic errors;
- output size.

If direct-B matches or improves the current result, A is unnecessary for the clean Scribe contract.

### If A remains

A should be minimized.

The most questionable A fields are `polarity` and `certainty` as authoritative intermediate metadata.
The exact selector already contains “no,” “suspected,” “not clearly,” etc. The current model can misassign the
metadata while preserving the source text correctly.

If A remains, prefer:
- exact source record;
- exact selector;
- assertion kind/material role;
- explicit source/provenance/time;
- source-local action split and wording.

Consider making polarity/certainty non-authoritative or removing them where they do not add information beyond the
selector.

---

## 2. B -> C has a reconciliation-output hole

### Ownership conflict

Current B owns:
- same/distinct episode decisions;
- evolution;
- corroboration/conflict;
- baseline-vs-current relationships;
- problem architecture.

Current C owns:
- HPI chronology;
- current-vs-baseline placement;
- minimum-sufficient event selection.

But B currently emits only:
- `PROBLEM`;
- `ACTION_VIEW`;
- optional unresolved items.

It does **not** emit the reconciled event/clinical units that represent the episode decisions it owns.

Therefore C cannot compile HPI without re-reading A/source material and reconstructing:
- which records refer to the same event;
- event chronology;
- which details belong to Wednesday vs Thursday cluster;
- baseline staring vs current episodes;
- which duplicate collateral descriptions are covered/corroborative.

That violates the stated ownership boundary.

### Recommendation

B needs a compact **reconciled clinical-unit output**.

This does not require a new stage or mandatory global episode model.

Example:

```text
CLINICAL_UNIT U001
  kind=current_event
  label=initial Wednesday event
  evidence=<A/Scribe refs>
  chronology=1
  relation_to_problem=P001

CLINICAL_UNIT U002
  kind=current_event
  label=Thursday recurrent cluster
  evidence=<...>
  chronology=2
  relation_to_problem=P001

CLINICAL_UNIT U003
  kind=baseline_comparator
  label=longstanding interruptible staring spells
  evidence=<...>
  relation_to_problem=P001
```

The exact schema is a proposal question.

The invariant is:

> C should receive the result of B's reconciliation, not be forced to redo it.

This also solves the current P002 over-problematization cleanly: baseline staring can be a comparison unit under
P001 without becoming a separate A/P problem.

---

## 3. Current C ignores the strongest prior render evidence

This is the largest architecture gap.

Current `C-NOTE-COMPILER-V2` emits open-ended fields such as:

```text
content=<A/B handles + cited wording>
function=<...>
preserve=<...>
```

and A/P fields such as:

```text
claim=
support=
counter=
actions=
preserve=
```

That is **not** a decision-complete rendering contract.

The renderer still has to decide:
- merge/split behavior;
- rhetorical class;
- head vs modifier;
- condition attachment;
- duplicate coverage;
- exact order;
- plan composition;
- how much prose to generate.

### This conflicts with prior empirical evidence

Existing repository evidence already showed:

#### B+ canonical-operator experiment
- 24/24 operator executions stable across 3 fresh conversations.
- typed groups + canonical operators removed the remaining structural/wording drift.

#### Operator stress suite
- 63/63 valid renders correct;
- 45/45 malformed inputs rejected;
- 108/108 valid/invalid boundary correct;
- malformed structures were not silently repaired into plausible prose.

The proven production boundary was:

```text
semantic objects
  -> typed groups
  -> canonical render operator
  -> bounded Doximity rendering
```

with roles such as:
- HEAD;
- MODIFIER;
- CONDITION;
- COVERED;
- rhetorical class;
- explicit order;
- OPERATOR.

### Recommendation

Do not run current C as written.

C should be revised to emit **typed render groups with canonical operators**, incorporating the P006/B+/stress-suite
evidence.

Conceptually:

```text
RENDER_GROUP G001
  section=HPI
  class=FACT
  operator=FACT_TIMING_PROVENANCE
  head=<clinical unit / evidence handle>
  modifier=<optional>
  covered=<optional duplicate/corroborative handles>
  order=1

RENDER_GROUP G002
  section=AP:P001
  class=PLAN
  operator=PLAN_CONDITIONAL
  action=<B ACTION_VIEW>
  condition=<supported condition handle>
  order=...
```

Exact operator vocabulary should reuse/adapt the tested P006 families rather than inventing a new open-ended prose
schema.

Malformed/underspecified groups should **fail closed**, not invite renderer repair.

---

## 4. C should have less raw-source freedom

Current C receives:
- A;
- B;
- the full canonical Scribe packet.

If B emits the reconciled clinical units it owns, C should normally be able to compile from:
- A exact source-local evidence;
- B reconciled units/problems/actions.

Full Scribe access at C creates an escape hatch for reinterpretation.

Recommendation:
- remove full-packet semantic freedom from C;
- allow only mechanical dereference of already-cited A/B source references when exact text is needed.

The compiler should not discover new clinical content.

---

## 5. P002 is a B contract defect, not an architecture failure

The latest B run incorrectly promoted longstanding interruptible staring to a separate BACKGROUND problem.

That should be corrected in B's problem threshold:

> A chronic/baseline symptom or phenomenologically distinct spell does not become a separate BACKGROUND problem solely
> because it is chronic or different from the primary event. Without independent disease identity or separate current
> assessment/management, preserve it as baseline/comparison evidence within the relevant primary problem.

Do not create a new stage for this.

---

## 6. Preserve what is working

Do **not** reopen:

- B1/action-state enums;
- same-model semantic validators;
- multi-pass micro-staging;
- final-writer clinical reasoning;
- manual intermediate physician review.

Preserve:

- source-qualified management wording;
- one production Ask invocation with logical internal phases;
- B as the clinical synthesis/problem-architecture owner;
- final renderer as a bounded lexicalizer;
- signer review of the final clinical note.

---

## Recommended sequence

### Architecture decision 1 — A necessity

Run one direct-B comparator on the clean Scribe packet before investing further in A-specific corrections.

### Architecture decision 2 — B output completeness

Whichever ingestion path survives, B must emit compact reconciled clinical units sufficient for C to consume B's
episode/baseline decisions without reconstructing them.

### Architecture decision 3 — C contract

Replace the current open-ended NOTE_BLUEPRINT with typed groups + canonical render operators, reusing P006/B+/stress
evidence.

### Then

Run:
1. surviving ingestion -> B;
2. revised B -> revised C;
3. renderer;
4. final-note comparison against the signer’s target.

No further synthetic operator suite is needed before the canonical case.

## Overall assessment

The project is now much closer to a small coherent architecture than it was earlier.

The likely durable shape is either:

```text
Scribe -> A(minimal) -> B(synthesis + reconciled units) -> C(typed groups/operators) -> render
```

or, if the direct-B comparator wins:

```text
Scribe -> B(synthesis + reconciled units) -> C(typed groups/operators) -> render
```

The next architecture work should decide **whether A earns its existence**, then make B->C decision-complete.
