# B+ Render Rules and Bugs

## Status

**REPRODUCED synthetic Doximity evidence**

Historical evidence:

- gradient experiment;
- B+ canonical-operator experiment;
- operator stress suite;
- P006 typed-group proposal.

These rules remain useful even though the surrounding architecture has changed.

---

# 1. Reproducibility gradient

Observed across three fresh conversations per arm:

```text
ordinary prose
    -> semantic merge/split drift + wording drift

structured DSL
    -> semantic structure stable
    -> wording still drifts

typed groups + canonical operators
    -> stable in the B+ repeated-run test

fully precomputed output
    -> identical in the gradient test
```

## Rule

When output variation changes clinical structure, do not add more prose instructions to the final writer.

Move that decision upstream into explicit structure.

---

# 2. Typed groups

The useful group types were:

- FACT_GROUP
- REASON_GROUP
- COMPOSE_GROUP

Each group belongs to one rhetorical class.

A group must never span:

- different problems;
- different rhetorical classes.

---

# 3. Group roles

Validated roles:

### HEAD

The primary semantic payload rendered by the operator.

Exactly one HEAD per group.

### MODIFIER

Adds bounded information such as:

- duration;
- timing;
- quantity;
- tempo;
- trend.

### CONDITION

Provides the conditional portion of one decision.

### COVERED

Represents another source/object carrying the same proposition.

COVERED does not receive its own output line.

## Rule

The renderer does not decide these roles.

They must already be assigned.

---

# 4. One object, one group

An object may appear in at most one render group.

Do not reuse one semantic object across PLAN and REASONING or across multiple groups.

Object reuse produced malformed contracts and ambiguous error classification.

---

# 5. Grouping is an upstream semantic decision

The renderer must not decide:

- whether two facts are equivalent;
- whether one is a modifier of another;
- whether a condition belongs to an action;
- whether duplicate evidence should be suppressed;
- which object is the HEAD.

Those decisions must already be complete.

---

# 6. Explicit operator

B+ added a canonical operator to the group.

Examples tested successfully:

- FACT_DURATION
- FACT_TIMING_PROVENANCE
- FACT_COVERED
- REASONING_IMPERSONAL
- CONDITIONAL_PLAN
- SIMPLE_PLAN
- exact ordered multi-group rendering

Potential generic families:

- PROBLEM_LINE
- FACT_SIMPLE
- FACT_DURATION
- FACT_TIMING
- FACT_TIMING_PROVENANCE
- FACT_COVERED
- REASONING_SIMPLE
- REASONING_TEST_PURPOSE
- PLAN_SIMPLE
- PLAN_CONDITIONAL
- PLAN_TEST

The vocabulary should remain small.

Do not create case-specific operators for every clinical sentence.

---

# 7. Operator input must be proposition-complete

## Historical bug: stable but wrong

B+ repeatedly rendered:

```text
The MRI to show.
```

The output was identical across fresh runs.

The problem was not randomness.

The input/operator received an incomplete proposition.

Bad semantic payload:

```text
we'll see what the MRI shows
```

Better:

```text
TEST=MRI
PURPOSE=determine whether there is a new lesion
```

Then:

```text
OPERATOR=REASONING_TEST_PURPOSE
```

can render a complete sentence.

## Rule

> A renderer must not manufacture the missing object of a clinical relation.

Stable bad output means fix the upstream payload/operator.

Do not loosen the prose prompt.

---

# 8. Order must be explicit

Group order and plan order should be assigned before rendering.

The renderer should not decide:

- centrality;
- priority;
- rhetorical sequence;
- which plan item comes first.

The structured-DSL and B+ tests showed stable ordering when order was explicit.

---

# 9. Payload accounting

Every retained semantic object must have one explicit disposition:

- HEAD;
- MODIFIER;
- CONDITION;
- COVERED;
- separately rendered;
- intentionally omitted with authorized reason.

Do not allow silent leakage or silent duplicate rendering.

---

# 10. Fail closed

The stress suite showed a strong boundary:

- valid groups rendered;
- malformed groups were rejected;
- malformed groups were not silently repaired into plausible clinical prose.

Preserve that behavior.

## Renderer rule

If required payload is missing or structurally invalid:

```text
CONTRACT_ERROR
```

or another small deterministic failure form.

Do not repair.

Do not infer.

Do not "make it work."

---

# 11. Error taxonomy should be small

Stress testing exposed overlapping labels:

- CONTRADICTORY_PAYLOAD vs INVALID_COVERAGE;
- CLASS_MISMATCH vs INVALID_COMPOSITION;
- unsupported transformation vs missing required field.

The valid/invalid decision was stable even when the precise label varied.

## Rule

Do not make production correctness depend on a nuanced free-form error ontology.

Preferred:

1. deterministic structural check when possible;
2. small mutually exclusive error set;
3. explicit precedence if multiple errors can apply;
4. otherwise generic CONTRACT_ERROR.

---

# 12. Rendering should not reopen clinical decisions

The final writer should receive:

- problem ownership;
- rhetorical class;
- group membership;
- group roles;
- canonical operator;
- order;
- failure behavior.

It should not receive a partially decided clinical bundle and be asked to "write naturally."

---

# 13. Surface variability is different from semantic variability

If:

- structure is stable;
- wording differs;
- meaning is unchanged;

then decide whether the wording difference matters.

If exact reproducibility matters, use a canonical operator.

If not, bounded surface variation may be acceptable.

Do not overconstrain clinically irrelevant wording.

---

# 14. B+ bug catalog

## BUG BPLUS-01 — incomplete proposition

Symptom:

```text
The MRI to show.
```

Cause:

Missing semantic object in operator payload.

Fix:

Make relation proposition-complete upstream.

---

## BUG BPLUS-02 — overlapping error taxonomy

Symptom:

Same malformed structure receives different plausible error labels.

Cause:

Error categories are not mutually exclusive.

Fix:

Simplify taxonomy or define precedence.

---

## BUG BPLUS-03 — object reuse

Symptom:

Same object appears in more than one group/class.

Cause:

Missing accounting invariant.

Fix:

One object -> at most one group.

---

## BUG BPLUS-04 — renderer repair temptation

Risk:

Malformed input is converted into plausible prose.

Required behavior:

Fail closed.

The stress suite showed that explicit typed contracts can enforce this boundary.

---

# 15. Preserved production principle

> The closer the renderer is to a lexicalizer, the more reproducible Doximity becomes.

Do not confuse this with prewriting the whole note.

The target is:

```text
clinical decisions
-> explicit typed groups
-> complete operator payload
-> canonical operator
-> bounded rendering
```
