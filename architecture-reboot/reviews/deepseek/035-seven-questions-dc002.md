# DeepSeek response 035 — 058 point-by-point, seven questions, smallest DC-002

I agree the interface layer is not fully closed. Four of the red-team findings are real; the rest are program corrections. I propose DC-002 as three edits, not a redesign.

---

## The seven questions

**1. "Candidate" in consensus 28 means a claim candidate, while item 27 means a problem candidate.** The word is overloaded across two adjacent items, which is why the cross-candidate question could not be answered: nobody could tell what was being related to what.

- item 27: problem candidate — a subject that needs its own assessment question;
- item 28: claim candidate — a formulation that may become, or contribute to, a claim representation.

DC-002 renames them everywhere. Every downstream question about "missing cross-candidate relations" is unanswerable until this is fixed, so it goes first.

**2. Candidate disposition is necessary, and cannot be proven from current artifacts.** S3 accounts for *objects* (`S3-ACCT-01`), not for *problem candidates*. A candidate that S1 proposed and nobody rendered leaves no trace, so a silent-loss hole exists exactly as reported. It is closed by one record and one predicate, not a new stage.

**3. Minimum S2 relation projection for S4** is a closed field list:

```text
per rendered problem: problem_id, selected_representation_id, members[], order_inputs[]
per unit: operator, section, order
```

Nothing else. No candidate-to-candidate relations, no adjudication history, no adoption verdicts — adoption is settled at S3 before a problem renders, and S4 has no use for the reasoning that produced it. S4 receiving the whole adjudication record is privilege it does not need, and in a one-call context unnecessary privilege becomes leak surface.

**4. The R2 boundary can be made testable by reversibility, without moving discourse upstream.** A join is legitimate if splitting the output at sentence and punctuation boundaries recovers each unit's text as a contiguous span. A merge that cannot be undone is a semantic edit and should be rejected. That test is mechanical, and it gives R2 a criterion instead of a prohibition.

**5. Yes — AX-T must gate production-transfer.** If instrumentation perturbs output, then every test-mode result carries an unmeasured artifact, and a production claim inherits it silently. Other experiments may run first as diagnostics; no result transfers until AX-T passes.

**6. Yes — "renders exactly once" needs signer approval.** One-owner A/P semantics entail one *owner*, not one *mention*. The candidate default (full statement under the primary problem, terse cross-reference where the second rationale is clinically material) is a clinical and stylistic choice and belongs to the signer. I would not freeze it in an experiment spec.

**7. The preflight is not redundant.** Every isolated arm freezes its input, so none tests raw paste → Case IR end to end. The preflight is the only screen that exercises ingest and its boundaries together. It stays a **program-level screen**, explicitly not an acceptance experiment and never counted as a ninth.

---

## Smallest DC-002

Three edits. No new module, no new stage, no reordering.

**D1 — terminology.** `problem candidate` and `claim candidate` defined distinctly in the interface document; consensus items 27–28 reworded to use them.

**D2 — candidate accounting.** S3 records for every S1 problem candidate one of `RENDERED` or `NOT_RENDERED` with a reason. New predicate `S3-CAND-01` (mechanical): every candidate id appears in `rendered[]` or in candidate dispositions. This is the silent-loss hole closed at its cause.

**D3 — S4 least privilege.** S4 consumes an S2→S4 **projection** with the closed field list in Q3, not the adjudication record. New predicate `S4-PROJ-01` (mechanical): every field S4 reads is in the projection list; any adjudication field present in S4's input is a leak.

**Not in DC-002, and why:** the AX-LEAK extension for semantic authority leaks and the AX-T gate are experiment-program changes; the S4 ordering contract and AX-R2 targets are prerequisites to freeze, not interface edits. Mixing them in would make DC-002 a second design change wearing a cleanup's name.

---

## What I accept without qualification

- Operator evidence supports canonical realisation and auditability, **not** upstream semantic reproducibility. Every claim I make about stability must be scoped to the mechanical subset and measured, not implied.
- The demonstration so far does not show reproducibility of grouping; it shows that decisions *can* be made explicit and audited. Those are different claims and only the second is supported.
- The pilot's three frozen cases are all single-problem, so it cannot observe the S1/S2 boundary failing. That is a real limitation of the pilot, not a closed issue.
