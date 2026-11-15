# ChatGPT review 039 — DC-001 v2 exact-diff review

## Verdict

**REVISE AGAIN. Do not apply DC-001 v2 yet.**

DC-001 v2 correctly fixes most of the defects from review 038, and the underlying architecture remains converged. The remaining findings are patch-integration and authority-preservation defects.

This does **not** reopen Review 4.

---

# Resolved from review 038

DC-001 v2 correctly fixes:

1. S1 no longer owns final claim/adoption/order.
2. S2 source temporality is explicitly distinguished from encounter-level adoption.
3. S2 relation examples are labeled illustrative/downstream.
4. The interface chain is updated.
5. The Distinctiveness table is updated.
6. CONSENSUS numbering moves to 26–29.
7. S2 no longer decides whether a problem is "required" before S3 inclusion.
8. S1 salience inputs are described as structured/inspectable with exact schema downstream.
9. The candidacy examples are explicitly non-exhaustive.

The remaining issues follow.

---

# Blocker 1 — architecture §2 high-level Case IR diagram is still unchanged

Review 038 explicitly required an update to the high-level Case IR diagram because it currently says:

```
|-- explicit render units
|     |-- problem
|     |-- rhetorical class
...
```

DC-001 v2 contains no edit to architecture §2.

Therefore v2 still visually encodes a universal `problem` field despite the new rule:

- A/P: owning problem required;
- body: no owner required; optional association by section contract.

This was review-038 blocker 9 and remains unresolved.

## Required revision

Update the diagram so the unit field is conceptually:

> problem owner/association as required by section contract — A/P owner required, body association optional

Exact compact wording is flexible.

---

# Blocker 2 — D4 contradicts D1 on body problem association

D1 says:

> A body unit requires no problem. It may carry an optional problem association where the section contract asks for one.

D4 changes both examples to:

```
problem=P1   # required for A/P units; omitted for body units
```

"omitted for body units" forbids the optional association D1 explicitly permits.

## Required revision

Use wording such as:

```
problem=P1   # owning problem required for A/P; body association optional per section contract
```

Do not turn "not required" into "forbidden."

---

# Blocker 3 — D5 invents a body duplicate policy

D5 proposes:

> within one section and, for A/P units, one problem, the same object may participate in at most one render unit;
> body units are keyed by section alone;

The second sentence freezes a new policy:

> one object may appear in at most one body render unit per section.

That was **not** agreed in Review 4.

Review 038 specifically said:

> body-section duplicate/use constraints are governed by the body section contract / unit-accounting rule; do not invent the exact body duplicate policy here if it is downstream.

"Body units are keyed by section alone" does exactly that.

## Required revision

Scope the existing mechanical uniqueness rule to A/P:

> within one A/P section + owning problem, the same object may participate in at most one render unit unless an explicit reuse contract permits otherwise.

For body sections, state only:

> duplicate/use constraints are section-contract dependent and remain downstream.

Do not freeze a section-only key.

Also scope the existing "cross-problem reuse within the same section" bullet to contexts with problem ownership, preferably A/P, so it does not imply hidden ownership for body units.

---

# Blocker 4 — S4 still does not explicitly consume S3's final rendered-problem state

D10 replaces:

> ordered problem model

with:

> problem candidates and S1's salience inputs (S4 owns final order)

But after the repaired architecture, S3 owns:

- whether an S1 candidate becomes a rendered A/P problem;
- the selected approved claim representation for that rendered problem.

If S4 receives only generic "problem candidates" plus the old:
- retained object-use set/problem-use map;
- S2 relationships;

then the interface does not explicitly require S4 to consume:

- S3's rendered-problem inclusion decision;
- S3's selected claim representation.

That leaves room for S4 to rediscover or infer them.

## Required revision

S4 Input should explicitly include conceptually:

- rendered/selected A/P problem set from S3;
- selected approved claim representation for each rendered A/P problem;
- retained object-use/problem-use map from S3;
- S2 adjudicated relations;
- S1 structured salience inputs;
- section/style/operator/ordering contracts.

S4 may retain access to candidate IDs/metadata as references, but **rendered problem inclusion and selected claim representation must be supplied by S3, not inferred by S4.**

---

# Blocker 5 — exact `NO_APPROVED_REPRESENTATION` freezes downstream schema

D8 adds:

> an explicit `NO_APPROVED_REPRESENTATION` state

The architecture agreement was about behavior/ownership, not an exact Case-IR enum or error label.

The canonical documents still leave:
- exact field-level Case IR schema;
- exact failure/disposition vocabulary;
- exact error taxonomy

downstream.

Backticks and uppercase make `NO_APPROVED_REPRESENTATION` look normative.

## Required revision

Freeze the concept, not the token:

> an explicit state indicating that no claim representation is semantically approved for that candidate

and state that the exact field/value is downstream.

The production fail-closed invariant remains unchanged.

---

# Blocker 6 — S3 can still silently choose among semantically non-equivalent approved representations

D9 says:

> If several approved representations exist, it selects one and records the choice; it does not resolve the ambiguity itself.

Those two clauses can conflict.

If several approved representations are semantically non-equivalent, selecting one **is** resolving a clinically meaningful ambiguity unless S2 has already established that selection among them is editorially interchangeable/allowed.

Review 035 already closed this boundary:

> S3 may select among S2-approved representations only where S2 has made the semantic choice space safe; unresolved non-equivalent alternatives remain an S2 semantic issue.

## Required revision

State conceptually:

> S3 selects only among representations whose interchangeability/allowed-choice status has already been established by S2 or the governing selection contract. If multiple semantically non-equivalent representations remain without an approved selection relation, S3 must not choose among them.

No exact relation field is required at architecture level.

---

# Blocker 7 — approved claim representations must not be restricted to explicit source "claim formulations"

D7 says S1 outputs:

> for each candidate, the candidate claim formulations present in the source

That is fine as a source-grounded input.

But D8's Role/Output is phrased mainly around:

> relations among candidate claims;
> mark which claim formulations are defensible.

This can be read as requiring an explicit source claim formulation before S2 can produce an approved representation.

That would recreate Candidate C's restriction.

A valid problem can be symptom/question-level even when the source provides observations rather than one canonical claim sentence.

Review 036 already froze the broader concept:

> a claim representation may be built from one or more source-grounded objects and their S2-adjudicated relations.

## Required revision

Make explicit in S2:

> approved claim representations may be grounded in source claim formulations **or other source-grounded objects/relations sufficient to support the assessment question**.

S2 may not invent unsupported content, but it is not limited to verbatim/existing claim phrases.

---

# Blocker 8 — CONSENSUS decision 29 should name approved representations, not only defensible formulations

D12 proposes:

> S2 adjudicates adoption and claim relations and marks defensible formulations; S3 selects among approved representations...

This leaves an unexplained step between:
- "marks defensible formulations"
and
- "approved representations."

The canonical structural decision should reflect the actual interface:

> S2 adjudicates adoption and claim relations and produces/approves semantically valid claim representation(s); S3 selects among those approved representations...

Exact wording can remain concise.

---

# Non-blocking — "problem" vs "problem candidate" terminology

D1 uses:

> A problem candidate exists...

D7 retains the submodule title:

> S1 — Problem Model

This is acceptable; no rename is required.

However, all summary text should consistently distinguish:
- candidate subject/problem from S1;
- rendered A/P problem after S3 selection.

Do not casually call every S1 candidate a final "problem" in diagrams or checker rules.

---

# Approval state

DC-001 v2 is **not approved for application yet**.

The architecture itself remains accepted:

```
S1 candidacy
 -> S2 semantic adjudication + approved representations
 -> S3 note/problem selection
 -> S4 blueprint + central order
```

with:
- A/P problem owner mandatory;
- body problem association optional by section contract;
- no back-edge;
- no new submodule;
- exact representation/failure/relation schemas downstream.

---

# Required next proposal

Issue **DC-001 v3** as a proposal only.

It should revise only these eight items:

1. architecture §2 Case IR diagram;
2. §7 example comment;
3. §10.1 checker scope without inventing body duplicate policy;
4. S4 Input to explicitly consume S3 rendered-problem set + selected representations;
5. replace exact `NO_APPROVED_REPRESENTATION` token with conceptual state;
6. constrain S3 selection among multiple approved representations;
7. make S2 approved representations explicitly able to derive from source-grounded objects/relations, not only explicit claim formulations;
8. align CONSENSUS decision 29 with approved-representation ownership.

Do not apply canonical files yet.
Do not touch Phase 0.
