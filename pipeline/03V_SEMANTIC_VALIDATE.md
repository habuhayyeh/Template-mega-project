# MODULE 03V — SEMANTIC VALIDATE

## PURPOSE

Adjudicate the routing produced by `03`. This is a review of assignments, not a new analysis.

It receives the immutable object table and the raw `03` ledger, checks the four semantic invariants below, and re-emits the ledger with the minimum number of destination changes needed to satisfy them.

It does not decompose, allocate, select, order, compress, or write. `04` assembles; `05` writes.

---

## INPUT CONTRACT

Two parts, both supplied:

1. **Object table** — every object with its ID, its immutable bucket, its text, and its provenance marker.
2. **Raw `03` ledger** — one assignment line per object, any `REUSE` lines, and the three validation lines.

The object table is authoritative. The ledger is a candidate.

---

## WHAT IT MAY AND MAY NOT DO

May change: a destination role, a block number, a discard reason within the closed set.

May not:

- rewrite, retype, shorten, or normalise object text
- invent an ID or a fact
- alter a provenance marker
- move an object to a bucket other than its own, except the roles already allowed by `03`
- merge two objects, compress, or summarise
- write note prose or explain the decision

Change only what an invariant requires. Where the ledger already complies, leave it alone. When in doubt, leave it.

---

## INVARIANTS

**1. Primary claim.** Where a problem has a current-encounter diagnostic formulation, that formulation is `PRIMARY_CLAIM`. A description of the presenting event, the chief complaint, or the triggering circumstance outranks nothing: it may be a qualifier or evidence, never the primary claim, while a formulation is available in the same block.

**2. Problem label.** A `PROBLEM_LABEL` names the problem. A preference, concern, counseling statement, incidental remark, or normal finding is not a label. Where a proposition that names the problem exists in the block, prefer it — with one exception. A prior clinician's diagnostic formulation does not become the label merely because it names a diagnosis more specifically. Unless the current encounter explicitly adopts it, it stays attributed historical evidence. Prefer the problem or symptom proposition, which may itself be historical, over an unadopted diagnostic formulation.

**3. Block coherence.** Every retained object must support, contextualize, describe the course of, or manage the block it sits in. Historical provenance does not disqualify a relevant object; recency does not qualify an irrelevant one. Do not force unrelated material into the nearest block. An object that belongs to no block is discarded, not relocated to a plausible one.

**4. Uncertainty.** Diagnostic hedges, stated alternatives, and unresolved states are preserved wherever they appear. No destination change may increase certainty, drop an alternative, or convert a conditional into a statement.

---

## PROCEDURE

1. Read the object table; treat bucket and provenance as fixed.
2. For each problem, test the four invariants against the assigned objects.
3. Note every violating line, and the single destination change that fixes it.
4. Apply those changes. Touch nothing else.
5. Re-emit the full ledger, unchanged where compliant.

---

## OUTPUT CONTRACT

- The corrected ledger, one line per input object, in input ID order.
- `REUSE` lines only where the declared function still holds.
- The three validation lines, recomputed from the corrected ledger.
- Nothing else. No diff, no explanation, no commentary, no note prose.

If nothing violates an invariant, re-emit the ledger exactly as received.
