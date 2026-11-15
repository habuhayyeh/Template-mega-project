# ACCEPTANCE_BRIEF — template

One page. Written before implementation. References contracts; never restates them.

---

```yaml
brief: B-04
artifact: S4
version: 1
control_plane: 2

contracts:                       # version-pinned references, not summaries
  - CON-STRUCTURE @2
  - CON-OPERATOR_REGISTRY @1
  - CTL-BUILD_SPEC §2

cases:                           # every relevant case, by id
  - CASE-02
  - CASE-05

predicates:                      # ids only; definitions live in ACCEPTANCE_MODEL
  - PRD-010  REQUIRED
  - PRD-020  REQUIRED
  - PRD-030  PENDING_DEPENDENCY (CON-OPERATOR_REGISTRY unfrozen)

failure_behaviour:
  - predicate: PRD-010
    behaviour: reject the duplicate unit; do not merge silently
```

---

## Fields

1. **Contracts** — version-pinned ids. If the brief has to explain a contract, the contract is unclear.
2. **Cases** — every relevant case. Historical cases are preferred; a derived case must name the invariant it exists for and the historical class beside it.
3. **Predicates** — ids, each marked `REQUIRED` or `PENDING_DEPENDENCY`. A predicate that cannot run yet is listed with its blocking contract, not quietly dropped.
4. **Failure behaviour** — per predicate. "Reject, do not repair" is a behaviour; the predicate id is what makes it auditable later.

## Rules

1. A predicate id must exist and be `ACTIVE` or explicitly `PENDING_DEPENDENCY`.
2. No code, no prompt text. Bounded expected wording is allowed only where a contract fixes the wording.
3. The brief is versioned and frozen before implementation. Changing it is an `ACCEPTANCE CHANGE`.
4. The engineer may reject a brief that is untestable or contradicts a contract, and must record why.
5. Length is not a criterion. A long brief over a coherent artifact is fine.
