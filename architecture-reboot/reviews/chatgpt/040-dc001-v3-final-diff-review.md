# ChatGPT review 040 — DC-001 v3 final exact-diff review

## Verdict

**REVISE ONCE MORE. Do not apply DC-001 v3 yet.**

The architecture remains converged. DC-001 v3 fixes the major integration defects from v1/v2, but three local statements still violate the agreed authority boundaries or downstream-open scope.

This is a patch review, not a reopening of Review 4.

---

# Resolved

v3 correctly fixes:

- §2 diagram now acknowledges A/P-required vs body-optional problem association;
- body association is optional rather than forbidden;
- S4 explicitly consumes S3's rendered-problem set and selected representation;
- exact `NO_APPROVED_REPRESENTATION` token is withdrawn;
- S2 representations may be built from source-grounded objects/relations, not only pre-phrased claims;
- interface chain and distinctiveness table match the repaired structure;
- consensus numbering and decision 29 are aligned;
- no Phase 0 change is attempted.

Three blockers remain.

---

# Blocker 1 — D6 still accidentally freezes body uniqueness

D6 says:

> within one section and, for A/P units, one problem, the same object may participate in at most one render unit;
> uniqueness for body units is governed by the section contract, not by this rule;

The first sentence still applies to body units.

For a body unit, the parenthetical condition "and, for A/P units, one problem" drops out, leaving:

> within one section, the same object may participate in at most one render unit.

That is exactly the body-section uniqueness policy the second sentence says is downstream.

So the two bullets contradict one another.

## Required revision

Scope the first rule explicitly to A/P only, e.g.:

> within one A/P section + owning problem, the same object may participate in at most one render unit unless an explicit reuse contract permits otherwise;

Then separately:

> body-section duplicate/use constraints are governed by the applicable section contract and are not fixed here.

Also scope any existing "cross-problem reuse within the same section" checker language to problem-owning/A/P contexts so body units do not acquire hidden problem ownership.

---

# Blocker 2 — D9's "multiple approved representations" rule still mixes semantic approval with ordering

D9 says:

> Where S2 approves more than one representation for a problem, those representations must be interchangeable — equivalent, or explicitly ordered by S2 with the basis recorded.

There are two problems.

## A. "interchangeable" and "explicitly ordered" are not the same condition

Two semantically non-equivalent representations can be ordered, but S3 choosing among them can still change clinical meaning.

Example:
- "Bell's palsy favored"
- "Bell's palsy favored; stroke not excluded"

An S2 preference/order does not automatically make both safe editorial alternatives.

## B. "basis recorded" risks reintroducing an unspecified rationale field

The architecture requires structured support/adjudication references, not a mandatory free-text basis.

## Required revision

Freeze only the safety condition:

> S2 may expose multiple approved representations to S3 only when choosing among them requires no further semantic adjudication under the governing selection contract.

If multiple semantically non-equivalent alternatives remain and selection would change clinical meaning, S2 has not completed its contract.

Any support for the approval/selection relation should use the already-agreed structured source/adjudication references; exact fields remain downstream.

This preserves:
- S2 = semantic choice space;
- S3 = editorial selection within a semantically safe choice space.

---

# Blocker 3 — "no candidate is defensible" and "required problem" remain ambiguous

D9 says:

> where no candidate is defensible, an explicit state that S3 can act on

But the same block correctly says approved representations may be built from source-grounded objects/relations and need not start as source text already phrased as a claim.

Therefore "no candidate is defensible" can be misread as:
> no S1 candidate claim formulation is defensible

even though a symptom/question representation may still be supportable from other source-grounded objects.

## Required revision to S2

Say:

> where no claim representation can be semantically approved for that problem candidate, emit an explicit unresolved/no-approved-representation state; exact form downstream.

D10 then says:

> if S2's approved set for a required problem is empty, inclusion is blocked...

"Required problem" remains undefined and risks implying a pre-S3 inclusion decision.

## Required revision to S3

Say:

> S3 may not include/render an A/P problem that lacks an S2-approved claim representation. If a separate governing requirement says that candidate must render, the S2→S3 seam fails/flags rather than inventing a claim.

This keeps:
- S2 = semantic adequacy;
- S3 = inclusion;
- governing requirements may constrain S3 without S2 deciding inclusion.

---

# Minor cleanup — CONSENSUS 29

Current v3:

> S3 selects the rendered-problem set and one approved representation per problem

Prefer:

> ...one approved representation per rendered **A/P** problem

because body units may have optional associations but do not instantiate owned A/P problems.

This is not independently blocking if the canonical surrounding text makes the scope unmistakable, but it is cheap to make exact.

---

# Approval condition

I would approve DC-001 for canonical application once a **v4** proposal changes only:

1. D6 A/P checker scoping;
2. D9 multiple-representation safety wording;
3. D9/D10 no-approved-representation and S3 inclusion wording;
4. optional one-word A/P scope cleanup in CONSENSUS 29.

No other architecture content needs reopening.

Do not apply canonical files yet.
Do not touch Phase 0.
