# DeepSeek response 024 — four final Review 3 corrections

All four accepted. None needs argument.

**1. H2 threshold withdrawn.** "≥2 independent evidence sources per CRITICAL class" was mine, not the architecture's. No upstream contract authorises a number, and inventing one is the same error as the predicates I just spent a review withdrawing. Removed.

**2. Corpus completeness is multidimensional.** Failure class is one axis, not the definition. The rewrite records coverage as a matrix over axes that already exist upstream — failure class, artifact, seam, mode, source family — with cells marked covered or not. No aggregate score, no threshold; the matrix is read, not summed.

**3. F3 restated behaviourally.** Test/production equivalence cannot be defined on IR fields that production is allowed to suppress. The obligation becomes: for the properties production actually carries, a test-mode run and a production-mode run on the same case agree. If production suppresses a property, that property is simply outside the comparison, and the omission is recorded rather than assumed harmless.

**4. B1 scoped.** CHECK proves the **declared mechanically decidable** predicates, not all IR→note conformance. Anything not declared is unaudited, and the rewrite says so instead of letting "CHECK passed" imply more than it earned.

## Pattern

Three of these four are the same mistake in different places: I asserted a guarantee (a threshold, a coverage claim, an equivalence, a scope of proof) that the frozen contracts did not grant. The rewrite will carry a single rule to stop it — **every claim names the contract that grants it, or it is marked as a design proposal**.

Review 3 closed from my side.
