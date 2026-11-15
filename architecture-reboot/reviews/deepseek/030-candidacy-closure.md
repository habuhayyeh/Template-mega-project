# DeepSeek response 030 — four closure points

**1. Candidacy rule — accepted.** 

> A separate problem candidate exists only when the neurologic subject requires its own current assessment question or status in this encounter.

It answers the question my own review left open, and it does so at the right level: not a list of problem types, but a test about *this encounter*.

Three cases it settles, which is why I believe it:

- **Infarct as etiology.** The infarct supports the seizure claim; it has no assessment question of its own today. It stays evidence, not a problem — which is the O10 case (atrial fibrillation not promoted to an infarct etiology) generalised into a rule.
- **Family memory concern explicitly deferred.** No assessment question today, so no candidate; it belongs in the history, not the A/P. That is K4 solved without a special case.
- **A separately managed situation with no new question** — the anticoagulation covering two indications — remains a candidate, because the clinician makes a management decision about it.

**What the rule implies and does not say:** every candidate must be source-grounded. A subject the model infers but the encounter never touches cannot become a problem. That should be stated, because it is the boundary between an assessment and an invention.

**What it cannot be:** mechanical. "Requires its own assessment question" is a clinical judgement, applied by S1 and audited afterwards. I would not try to make it a predicate; I would give it the cases above as the audit fixtures.

**2. Claim representation — enums and fields are downstream.** Accepted. My `SINGLE / NESTED / DIFFERENTIAL / UNRESOLVED` and the fields I sketched are illustrative, not frozen. What survives as architecture is only this: a claim is a representation that may carry more than one candidate and a relation, and S3 selects among approved representations rather than among raw candidates.

**3. No mandatory free-text rationale.** Accepted, and it is the right instinct — a prose justification is a generative surface with no check, which is exactly the defect we removed from edge `basis` earlier. The representation carries structured support instead: source span refs and object ids, plus an adjudication record when the relation came from judgement rather than text. Free text may be recorded, never required.

**4. Fail at the S2/S3 seam, not at S4.** Accepted.

If a required A/P problem has no approved claim representation, that is a failure *there*, with the problem named and the reason recorded. Rendering a claimless problem and hoping a later completeness check catches it moves the failure two modules away from its cause and makes attribution guesswork — the same mistake as letting the renderer repair malformed units.

S4's completeness check stays, but as defence in depth, not as the primary detector.

---

## Status

Interface design closes for me: S1 candidacy, S2 relations and eligibility, S3 selection among representations, S4 order and completeness, each with one question, acyclic, and no back-edge.

The architecture experiments remain open and unrun: AX-2 (seam leakage, corrected), AX-T (observer effect), AX-SCALE, AX-I3, and the rebuilt K2 with explicit linkage.

The candidacy rule is a `DESIGN CHANGE` against S1's interface — its output is now candidate subjects with assessment questions, not problems.
