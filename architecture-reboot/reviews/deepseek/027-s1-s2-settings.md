# DeepSeek 027 — challenging the architecture across S1/S2 settings

Not a defence of Candidate A. Four arrangements, run against cases from our own record, to find where each breaks.

---

## 1. The settings

| | S1 Problem Model | S2 Adjudication | Claim decided by |
|---|---|---|---|
| **A** | candidates + evidence | adoption, relations, **finalises claim binding** | S2 |
| **C** | final problems, current-asserted claims only | adoption, relations | S1, by restriction |
| **D** | candidates + evidence | adoption, relations (no claim) | **S3**, with selection |
| **M** | merged with S2 | — | one module |

B is excluded already: it is the back-edge we withdrew.

---

## 2. Cases from the record

### K1 — the seizure claim

> "Post-stroke seizure from the old left MCA scar rather than a new lesion."

Asserted today. **All four work.** No discrimination.

### K2 — continued problem, procedural adoption only

Prior neurology documents a left MCA infarct. Today: "continue aspirin, no new deficits." The infarct is never restated.

- **A** — S1 offers the historical infarct as candidate; S2 reads the continuation as adoption; claim binds. Works.
- **C** — no current assertion of the infarct, so it is not a current problem. The aspirin line then has **no problem to belong to**. Breaks, unless plans may exist without problems.
- **D** — S2 marks the historical claim adopted; S3 binds it because it is used. Works.
- **M** — works, with no audit seam.

C's failure here is the F-11 shape in reverse: not a prior leaking into today, but a today-plan orphaned from its problem.

### K3 — prior recommendation, never adopted

A 2025-06 note says "no further workup". Today is silent.

- **A / D** — nothing adopted, no plan line. Correct.
- **C** — same result by a different route. Correct.

This is the case we actually shipped wrong, and every setting handles it once the object carries its provenance.

### K4 — family concern, explicitly not today's issue

- **A / C / D** — claim is "not today's issue", which is a *negative* claim. The risk is not adoption but **problem creation**: something that should be one HPI line becomes an A/P block.
- **M** — same risk, worse attribution.

No setting fixes this. It is a rule about when a problem may exist at all: a problem requires either a management action or a reasoned claim. That rule is missing from all four.

### K5 — sources contradict

Prior note: seizure in 2024. Transcript: "first seizure last month".

- **A** — one problem, two candidate claims, S2 reconciles and binds. This is precisely the work A puts in the finalisation step.
- **C** — the transcript wins by construction. Simple, and usually right — but it silently discards the prior without recording a conflict.
- **D** — S2 records the contradiction as a relation; S3 binds the current claim and the conflict stays visible in the IR.
- **M** — no seam to attribute the reconciliation to.

D keeps the disagreement as data; C resolves it by policy. For a note that will be read by the clinician who wrote the prior, keeping the disagreement is worth more than the simplicity.

### K6 — management with no stated diagnosis

"Continue the current regimen" — nothing names the problem.

- **All four break.** There is no candidate claim, and a plan unit with no problem has no home.
- The only fixes are: fail closed, or define an explicit unclassified-management block. That is a missing rule in every setting, not a property of the arrangement.

### K7 — historical fact that belongs in the body, not the A/P

"History of migraine", mentioned once, addressed never.

- **A** — S1 may create a problem; S2 declines adoption; the fact still needs to appear in the body. Works only if body sections do not depend on problems.
- **C** — no problem is created and the fact flows to the body directly. **Simplest.**
- **D** — as A.

C's advantage is real here, and it points at something worth saying: **problems exist for the A/P.** If the body is built from objects, not problems, then most of C's restrictiveness is harmless and its simplicity is free.

---

## 3. What the comparison actually shows

**The A-vs-C question is not about cycles. It is about whether a plan unit may exist without a problem.**

- If every plan unit needs a problem, C cannot stand — K2 orphans the plan — and A or D is required.
- If a plan unit may stand alone, C is viable, much simpler, and K7 favours it strongly.

That decision is not in the frozen architecture. It should be settled before choosing an arrangement, because it determines the answer.

**A concentrates badly.** Under A, S2 owns duplicates, modifiers, conditions, roles, adoption **and** claim finalisation. That is the same overload the review already flagged at S4, moved one module left.

**D distributes better.** S3 already decides what is used and under which problem. Deciding which used object is the claim is the same kind of editorial judgement, and putting it there means S2 stays a relation-resolver. D also keeps K5's contradiction visible instead of resolving it by policy.

---

## 4. Recommendation

**D, with the plan-without-problem question settled first.**

If the answer is "plans require problems", D and A both work and D distributes authority better. If the answer is "plans may stand alone", C becomes the cheapest architecture and should be tested alongside D rather than dismissed.

**Two rules missing from every setting, and worth fixing regardless:**

1. a problem exists only if there is a management action or a reasoned claim (K4);
2. a plan unit with no problem fails closed, or lands in an explicit unclassified block (K6).

---

## 5. The experiment that discriminates

**One case, K2 shape** — a continued problem with only procedural adoption language, plus one plan line.

- Under C, the plan line has no problem; the run either fails or produces an orphan.
- Under D, the line lands under the adopted problem.
- Run it five times; the question is not whether it succeeds but whether the *failure mode* is the one we can live with.

That is one case and five runs, and it separates the arrangements far better than the seam-leakage probe, which tests something all four share.
