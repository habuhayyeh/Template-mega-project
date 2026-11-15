# Review 132 — DeepSeek 028: accept root cause, challenge quote-anchored fix

## Verdict

**Accept the root-cause diagnosis. Do not yet accept the proposed quote-anchored F1 implementation.**

DeepSeek is right on the central architecture point:

> F1V is not an independent validator because F1 creates synthesized clinical claims and F1V asks the same
> model to validate those claims.

The observed failures support that diagnosis:
- topic-neighbor refs passed as support;
- question records passed as answers;
- action-state upgrades passed;
- a complete VERIFY ledger still false-passed.

The problem is not mainly missing validator rules.

## What I accept from DeepSeek

1. **Remove the synthesized `fact:` claim layer from F1.**
2. **Do not make fresh-session F1V the production architecture.**
3. **Do not keep expanding F1V.**
4. **Keep the Scribe V2.2 packet as the canonical evidence store.**
5. **Move semantic reconciliation/action interpretation downstream.**
6. **Use mechanical validation only for genuinely mechanical invariants.**
7. **Keep the runtime small.**

## What I challenge

### 1. Quote-anchored F1 can recreate the duplication problem

The reason D-039 introduced lazy decomposition was that copying/re-expressing source content downstream
expanded the packet and caused truncation.

A quote-anchored index risks creating another near-copy:

```text
CLUSTER
  record ids
  exact source text repeated again as anchors
```

If downstream already has the immutable Scribe packet, copying exact source text into F1 is unnecessary
for most clusters.

The strongest way to eliminate F1 support obligations is not:

> synthesized fact -> exact quote

It is:

> synthesized fact -> **no claim at all; pointers only**

### 2. DeepSeek's example demonstrates the danger

The proposed example says:

```text
T153: "Any previous seizures?"
T154: "No."
P1.010: "No prior seizure history."
```

Those are not the actual Scribe V2.2 record texts/assignments in the frozen packet.

Actual relevant records include:
- T153: clinician asks whether she ever had seizures before;
- T154: clinician asks about family members with seizures;
- T155: response says not on father's or mother's side;
- P1.010: no previous history of seizure activity.

So even while recommending "exact anchors," the review itself produced non-exact/misassigned anchors.

That does not invalidate the architecture diagnosis. It argues against making GPT-4o copy source text as a
new runtime artifact.

### 3. Exact quote existence is not the needed invariant

If F1 contains no clinical assertion, there is no need for a quote to "prove" the cluster.

The Scribe record itself remains directly available downstream.

A cluster label such as:

```text
CLUSTER C003 — prior seizure history
  records: P1.010,T153
```

does not assert that prior seizures were absent. It only groups records about that subject.

Downstream semantic work can dereference P1.010 and T153 and determine:
- P1.010 is a denial;
- T153 is a question.

This directly avoids the exact failure that F1V could not catch.

## Counterproposal — pointer-only F1 index

### Function

F1 should perform only **semantic routing/grouping of source records**.

It should answer:

> Which Scribe records belong together as evidence about the same clinical subject/event/trajectory?

It should not answer:

> What clinical fact do those records prove?

### Candidate output

```text
@@HANDOFF F1_EVIDENCE_INDEX_V1

CLUSTER C001 — patient identity
  records: P1.011

CLUSTER C002 — prior seizure history
  records: P1.010,T153

CLUSTER C003 — family seizure history
  records: T154,T155

CLUSTER C004 — Wednesday event
  records: T038,T040,T042,T046,T048,T050,T052,T054,T059,T061,T063,T066,P1.016

CLUSTER C005 — Thursday event
  records: ...

CLUSTER C006 — Keppra mentions
  records: P1.009,P1.014,P1.053,P1.054,P1.055,T135

UNCLUSTERED_MATERIAL
  records: <only if material records cannot be safely grouped>

@@END
```

No:
- `fact:`;
- `reasoning:`;
- `issue:`;
- exact quote duplication;
- final polarity/certainty;
- action state;
- causal interpretation;
- problem identity;
- section/use decision.

### Cluster label rule

The label must be **topic-only and non-assertive**.

Allowed:
- prior seizure history;
- family seizure history;
- Thursday event;
- Keppra mentions;
- ED examination;
- baseline staring behavior.

Forbidden:
- no prior seizures;
- epileptic seizure;
- Keppra administered;
- normal testing;
- PNES likely.

### Splitting rule

Split only on objective routing differences:
- different clinical subject/event;
- materially different time episode;
- different source domain when mixing would make downstream dereferencing harder.

Do not split based on predicted problem membership, note section, or final plan.

### Coverage

F1 should aim to route every **material** Scribe record needed for later neurologic reasoning.

It need not reproduce:
- conversational repair;
- greetings;
- duplicated filler;
- low-value questions whose answered content is already represented elsewhere.

The original packet remains available downstream, so omission from F1 is not deletion from the evidence
store.

## Validator consequence

If F1 becomes pointer-only:

- there is no claim-support validator to run;
- F1V should be removed from the production path;
- only mechanical checks remain useful:
  - cited record id exists;
  - cluster id is unique;
  - no duplicate record placement if exclusivity is required;
  - every cluster has at least one record;
  - output closes correctly.

These do not require an LLM validator.

## Runtime consequence

Candidate minimal runtime:

```text
Scribe V2.2
  -> F1 Evidence Index (pointer-only clusters)
  -> F2 Semantic Reconciliation + Action State
  -> F3 Problem Architecture
  -> F4 Note Compiler
  -> F5 Renderer
```

Whether reconciliation and action state truly belong together in F2 remains empirical.

## Recommendation

Do **not** run fresh-session F1V yet.

First settle the more fundamental question:

> quote-anchored index vs pointer-only index.

My preference is pointer-only because it:
- eliminates the claim layer;
- avoids source-text duplication;
- preserves D-039 lazy decomposition;
- makes source dereferencing explicit;
- minimizes token/cardinality load;
- removes the need for a semantic F1 validator.

If DeepSeek agrees, build the pointer-only F1 candidate and run one Doximity test.
