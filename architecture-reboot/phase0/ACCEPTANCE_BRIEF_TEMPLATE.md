# ACCEPTANCE_BRIEF_TEMPLATE

A brief is written before implementation and says what correct means. It is thin on purpose: it references the frozen architecture and never restates it.

## 1. The five fields

### A. Contract references

Exact section references into the frozen documents. Not summaries, not paraphrases — pointers.

```text
CONTRACT
  CONSENSUS_ARCHITECTURE_v0.1 §7 render units
  CONSENSUS_SUBMODULE_INTERFACES_v1 S4
  phase0/BUILD_LINT §1 L1–L6
```

If the brief needs to explain the contract, the contract is unclear and should be fixed first.

### B. Fixtures

The cases the artifact must handle, by id from `FIXTURE_REGISTER.md`. A brief cites **all relevant historical fixtures** for the artifact, plus any derived fixture, which must justify why no historical case covers its invariant.

```text
FIXTURES
  F-02 duplication, infarct block
  F-06 missing required line, seizure precautions
  D-01 (derived) zero-member unit — adjacent to F-06
```

### C. Required artifact properties

What the output must contain, stated so that the named check can decide it. Properties, not examples. A property answerable only semantically is legitimate — it just has to say so.

```text
PROPERTIES
  every unit names exactly one problem
  every unit's operator is in the closed vocabulary
  the section list is ordered and contains no duplicate section
```

### D. Deciding checks

For each property, the check that decides it, and which mode answers it — `MECHANICAL`, `SEMANTIC_AUDIT` or `HYBRID`.

```text
CHECKS
  P1  MECHANICAL      unit.problem is single-valued
  P2  MECHANICAL      operator ∈ vocabulary
  P3  MECHANICAL      section list has no duplicates
  P4  SEMANTIC_AUDIT  operator renders the payload
```

A property with no deciding check is not a property. It is a hope.

### E. Expected failure behaviour

Named by failure class, not described as bad output.

```text
FAILURE BEHAVIOUR
  class F2 duplication      → reject unit pair, fail closed
  class C13 over-inclusion  → object is dispositioned NOT_USED with a reason;
                              placement is checked by audit, not rejected at runtime
  class C11 contradiction   → build fails, no artifact produced
```

"Reject, do not repair" is a behaviour. `F2` is what makes it auditable six months later.

## 2. Rules for writing a brief

1. Five fields, no more. Extra sections become a second specification.
2. No code, no prompt text. If the brief contains the solution, it is no longer a test.
3. Every property has a check; every check names its mode.
4. Every fixture id must exist in the register.
5. The brief is frozen before implementation starts. Changing it afterwards is an `ACCEPTANCE CHANGE` and needs the same approval as a design change.

## 3. Review of a brief

The engineer reviews the brief before implementing. The engineer may reject a brief that is untestable, self-contradictory, or that asserts something the contract does not authorize. Rejections are recorded with the reason; the reviewer revises.

An engineer who implements against a brief they believe is wrong is worse than an engineer who stops.

## 4. Size

Target one page. If a brief needs three, the artifact is doing too much and should be split.
