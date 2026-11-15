# DeepSeek response 028 — refined D, five questions

**1. A/P-scoped ownership — accepted.**

A/P units require exactly one owning problem. Body units do not require an owner and may carry an optional association where the section contract asks for it.

This fixes K7 properly. Under universal ownership, a migraine history either becomes a fake A/P problem or has nowhere to live; under A/P-scoped ownership it simply never needed to be a problem. The uniqueness rule that catches duplication still holds where it matters — the A/P — and stops being stretched over sections that are not organised by problem.

**2. K2 — my example was invalid, and the correction is right.**

"Continue aspirin" cannot adopt a prior stroke. That is medication→diagnosis inference, which we banned earlier for a separate reason (atrial fibrillation being promoted to infarct etiology). I used K2 to argue against Candidate C, and the argument does not survive: under the frozen rules the aspirin line has no problem under *any* arrangement unless the source links them.

That matters for the experiment as well. The K2 case must be rebuilt with explicit linkage — "continue aspirin for secondary prevention of the known left MCA infarct" — before it can discriminate anything. As I wrote it, it would have tested a rule the architecture already forbids, and a passing result would have proven nothing.

**3. Eligibility in S2, selection in S3 — accepted, with one constraint.**

- S2 decides which candidate formulations are **semantically eligible**: adopted, current, not contradicted by the encounter.
- S3 selects the rendered claim **from that eligible set only**. It may not reclassify, merge, or synthesise a claim.

The constraint: eligibility is a set, so S3 can still face two eligible candidates. Rule needed — S3 prefers the candidate asserted in the current encounter; on a genuine tie it fails closed rather than choosing. Otherwise S3 quietly becomes a semantic adjudicator through its tie-breaking.

**4. S4 owns order; S1 supplies salience — accepted.**

S1 offers features: acuity, risk, whether managed today, source recency. S4 materialises the order. That matches the frozen rule that S4 centralises final problem and unit order, and it removes the S1 "ordered problem registry" that contradicted it.

One consequence: problem order becomes reproducible only if S4's ordering inputs are explicit. If S4 sorts on prose judgement, order drifts exactly as it did in the old writer. The salience features should be declared values, not adjectives.

**5. No new submodule and no back-edge — confirmed.**

S1 → S2 → S3 → S4 is acyclic. S1 loses claim authority, S2 gains eligibility, S3 gains final selection, S4 keeps order. No module is added, none is merged, and nothing points backwards.

**This is a `DESIGN CHANGE`** against the frozen S1/S2 interface: S1's output is no longer "current problem-level claims", and S2 gains a responsibility it did not have. It should be recorded as one, with the interface document revised — not treated as a clarification, which is the mistake I made with the back-edge.
