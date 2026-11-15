# DeepSeek response 022 — the predicate-kind leak

Accepted, no redefinition.

`predicate_kind` belongs to the predicate record owned by `ACCEPTANCE_MODEL`. `FIXTURE_INDEX` does not gain a column for it.

That was the same conflation as Review 1's "fixtures do not own which assertions exist" — I fixed the sentence that created the ownership and then reintroduced it in a data model, which is how it would have survived. A column is an ownership claim.

Corrected consequences:

- **F-06** stays a historical fixture; its referenced predicate is a `BUILD_GATE`.
- **F-15** stays a historical fixture; its referenced predicate is a `PROCESS_GATE`.
- A fixture row carries: case id, observation, evidence, boundary, referenced predicate/assertion-set ids, fixture status. Nothing about predicate kind.

Review 2 is closed from my side.
