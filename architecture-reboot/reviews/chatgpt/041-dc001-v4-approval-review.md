# ChatGPT review 041 — DC-001 v4 approval review

## Verdict

**REVISE LOCALLY. Do not apply DC-001 v4 yet.**

The architecture remains converged. Of the four v4 passages:

- D10 is accepted.
- D13 is accepted.
- D6 is conceptually accepted but should be grammatically corrected before canonical insertion.
- D9 contains one remaining logical authority defect.

This is not a reopening of architecture.

---

# D6 — concept accepted; canonical wording needs correction

v4 says:

> within one section and one problem, an A/P unit may reference a given object in at most one render unit;

The subject is malformed:
- an A/P unit is itself a render unit;
- therefore saying "an A/P unit may reference ... in at most one render unit" is structurally confused.

The intended invariant is clear.

## Required wording

Use conceptually:

> within one A/P section + owning problem, a given object may participate in at most one render unit unless an explicit reuse contract permits otherwise;

and:

> this rule does not apply to body units; body duplicate/use constraints are governed by the applicable section contract.

This keeps the rule scoped to A/P and does not invent a body policy.

---

# D9 — one remaining logical defect

v4 says:

> Where the choice is not semantically free, S2 reduces the set **or records structured support references for the decision** — not a free-text rationale.

The `or` is wrong.

Recording structured support references does not resolve the semantic choice.

If S2 leaves multiple semantically non-equivalent representations in the approved set, S3 still faces a semantic decision even if S2 documents why those representations exist.

That violates the frozen seam:

> S2 = semantic adjudication / safe approved choice space  
> S3 = editorial selection within that safe choice space

## Required rule

When the choice is not semantically free:

1. S2 must complete the semantic adjudication so the set exposed to S3 no longer requires semantic judgment; and
2. S2 records structured source/adjudication references supporting that adjudication.

Support references accompany the semantic resolution; they are not an alternative to it.

Conceptually:

> **Approval is a safety property.** S2 may expose more than one approved representation for a problem only when choosing among them requires no further semantic adjudication under the governing selection contract. If the alternatives are not semantically interchangeable/selection-safe, S2 must resolve the semantic choice before handoff and record structured source/adjudication references supporting that resolution. It may not leave S3 a set whose selection would change clinical meaning.

Exact relation vocabulary and support fields remain downstream.

---

# D10 — accepted

v4 correctly states:

> S3 may not include or render an A/P problem that lacks an S2-approved representation.

and:

> if a separate governing requirement mandates inclusion, the seam fails/flags rather than rendering claimless.

It also correctly returns a semantically unsafe multi-representation set to S2 ownership.

No further change required.

---

# D13 — accepted

The addition of:

> per rendered A/P problem

correctly scopes S3 claim-representation selection to problem-owned A/P rather than body associations.

No further change required.

---

# Approval condition

Issue **DC-001 v5** changing only:

1. D6 canonical grammar/scoping;
2. D9 replace the unsafe `reduce OR document` rule with `resolve AND document structured support`.

Everything else from v3+v4 stands.

If v5 makes only those two corrections, I expect DC-001 to be ready for application review.

Do not apply canonical files yet.
Do not touch Phase 0.
