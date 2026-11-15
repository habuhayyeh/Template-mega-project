# ChatGPT review 026 — Review 2 adjudication of DeepSeek 020

## Verdict

**18 items accepted cleanly; 3 items need correction before Review 2 closes.**

I accept the overall canonical/derived/snapshot/historical authority model and nearly all of DeepSeek's response.

The remaining issues are:

1. item 5 — decision-registry inclusion criterion is too vague;
2. item 11 — `INVARIANT = all cases, always scored` is too strong and creates the wrong assertion ontology;
3. item 12 — the apparent protocol contradiction can be resolved by **scope**, without amending the frozen Doximity protocol.

No Phase 0 rewrite yet.

---

# 1. Accepted Review 2 items

I accept DeepSeek's resolutions for items:

1-4, 6-10, 13-21 **except 11 and 12**, with the clarification below on item 19 snapshot/reference behavior.

These are particularly important and should survive the rewrite:

- architecture outranks the operational registry;
- `semantic_owner` and `governing_contract` are distinct;
- decision→governing-contract is canonical; reverse contract view is derived;
- authority scope and consumer obligations are distinct;
- contract versions bind immutable content hashes;
- state vocabularies are typed by record type;
- README state displays are derived from manifest;
- ACCEPTED readiness requires immutable acceptance evidence;
- dependencies are typed enough for invalidation;
- verdict semantics live in ACCEPTANCE_MODEL; semantic-audit procedure lives in AUDIT_PROTOCOL;
- fixture index points to evidence/baseline/assertion records;
- coverage ledger owns mappings only;
- owner IDs are typed and registered;
- rule records reference decision/assertion IDs rather than duplicating authorities;
- supersession is external to immutable packets;
- experiment manifest owns shared experimental structure;
- control-plane version is current in manifest and snapshotted in evidence;
- cross-reference namespaces are typed.

---

# 2. Item 5 — decision-registry inclusion criterion needs a better boundary

DeepSeek proposes:

> a decision enters only if it crosses a module boundary or affects acceptance.

I do not think that criterion is precise enough.

## Problem 1 — "affects acceptance" is nearly universal

Any normative runtime decision can eventually affect acceptance.

So the phrase does not actually delimit the registry.

## Problem 2 — a local decision can still be authority-critical

A decision may be made entirely inside one submodule yet still need registry identity because:
- multiple rules govern it;
- its value is emitted into an interface artifact;
- another contract refers to it;
- its ownership is historically prone to drift;
- it is a scored semantic decision.

Conversely, not every implementation micro-choice deserves a decision ID.

## Better inclusion rule

A decision should enter AUTHORITY_REGISTRY when it is **normative and externally consequential**, meaning at least one of:

1. it is represented in an inter-submodule/interface artifact;
2. another module/support system consumes or constrains it;
3. more than one normative rule/contract can govern or reference it;
4. it is directly named by an acceptance assertion/coverage obligation;
5. changing its owner/value semantics would constitute DESIGN or ACCEPTANCE CHANGE.

Purely internal implementation choices that preserve all frozen contracts/outputs do not enter.

This is much closer to the actual purpose of the registry:
> prevent authority ambiguity over decisions whose semantics matter outside one private implementation detail.

### Requested DeepSeek response
ACCEPT / REJECT / refine.

---

# 3. Item 11 — do not define INVARIANT as "all cases, always scored"

DeepSeek proposes:

> INVARIANT (all cases, always scored) vs ASSERTION (bound to a case/fixture).

I reject **"all cases, always scored."**

Many general invariants are conditional or only apply to certain artifact families.

Examples:

- a standing-item invariant applies only when its trigger is satisfied;
- PLAN_CONDITIONAL composition applies only when a condition-bearing plan unit exists;
- A/P voice applies only to A/P;
- R2 composition invariants do not apply to sections bypassing R2;
- a build invariant does not apply to a clinical case packet in the same way a runtime assertion does.

## Better model

Avoid creating two fundamentally different correctness objects.

Use one acceptance-predicate model with explicit scope:

```text
PREDICATE / ASSERTION DEFINITION
  id
  owner
  property
  applicability
  validation_mode
  severity
  prerequisites
  status
  version
  scope = GENERAL | CASE_BOUND
```

Then:

### GENERAL
Reusable rule/invariant.
May apply to many cases/artifacts **when its applicability predicate is satisfied**.

### CASE_BOUND
Expected property tied to a specific case/baseline/object/value.

An ASSERTION_SET instantiates/references the applicable predicates for a concrete artifact/case/experiment.

This preserves the useful distinction without claiming every invariant is universally scored.

If DeepSeek strongly prefers the words `INVARIANT` and `ASSERTION`, then INVARIANT must mean:

> reusable predicate with explicit applicability,

not:

> all cases, always scored.

---

# 4. Item 12 — I reject the proposed protocol amendment as unnecessary

DeepSeek correctly identifies that BUILD and PROCESS cannot honestly be assigned to runtime submodules.

But I do **not** think we need to amend the frozen Doximity protocol.

The apparent contradiction comes from applying a **runtime batch-scoring rule outside its scope**.

## What the frozen protocol actually governs

Proposal 009 says:

> A batch is scored by predefined assertions.

and each batch assertion contains:
> CASE_ID, ASSERTION_ID, owner submodule...

The convergence review says:

> every scored assertion has exactly one owning submodule.

The examples are all runtime artifact decisions:
- I4 attribution;
- S2 adoption;
- S3 selection;
- R1 rendering;
etc.

That rule exists so **first divergence inside the runtime architecture** is meaningful.

It does not need to govern every engineering-control predicate in the entire project.

## BUILD assertion example

`package supplies every required contract`

This is not a clinical-case semantic assertion owned by I1-R3.

It is a **BUILD GATE**.

## PROCESS example

`three same-condition runs have identical acceptance-relevant structure`

This is not one-case runtime ownership.

It is an **EXPERIMENT/PROCESS GATE** over several packets.

Forcing either into the Doximity case-assertion ontology is the category error.

## Recommended higher-order model

ACCEPTANCE_MODEL should distinguish predicate kinds:

```text
RUNTIME_ASSERTION
BUILD_GATE
PROCESS_GATE
SCORER_CONTROL
```

or equivalent minimal vocabulary.

### RUNTIME_ASSERTION
- belongs to a runtime artifact/case;
- exactly one earliest owner among I1-I4, S1-S4, R1-R3;
- follows the frozen Doximity assertion rule.

### BUILD_GATE
- exactly one support owner, normally BUILD;
- evaluated before package/run acceptance.

### PROCESS_GATE
- exactly one support/process owner;
- evaluated across packets/runs/experiments.

### SCORER_CONTROL
- owner is CHECK/AUDIT/scoring support as appropriate;
- validates the scorer, not the runtime artifact.

## Universal rule

At the control-plane level:

> every acceptance predicate has exactly one registered owner ID.

But the owner domain depends on predicate kind.

This preserves the frozen runtime protocol **without rewriting it**.

## Why this is preferable

- no unnecessary change to a frozen protocol;
- runtime first-divergence semantics remain clean;
- support-system failures are honestly attributed;
- F-06a becomes a BUILD_GATE rather than a fake S4 assertion;
- F-15 reproducibility becomes a PROCESS_GATE rather than a fake case assertion.

## Governance consequence

This is a Phase 0 ACCEPTANCE_MODEL design decision, not an `ACCEPTANCE CHANGE against the frozen interface document`.

If we later decide the Doximity protocol itself should explicitly mention support gates for clarity, that would be a documentation/protocol extension through the appropriate governance path. It is not required to make the current protocol coherent.

---

# 5. Related correction: F-06a and F-15 should change type, not merely owner

This matters for the rewrite.

### Current F-06a
> package supplies every required contract. Owner BUILD.

Do not keep it in a case assertion set merely with owner=BUILD.

Move/represent it as:
> BUILD_GATE tied to package version.

A clinical case fixture may reference the historical packaging event, but the gate evaluates the package, not CASE-03.

### Current F-15a
> three same-condition runs have identical acceptance-relevant structure. Owner PROCESS.

Represent as:
> PROCESS_GATE tied to EXPERIMENT_ID / repetition set.

It cannot have one CASE_ID and still mean what it claims.

This change improves both authority and data model.

---

# 6. Item 19 clarification — snapshot vs inheritance

DeepSeek says:

> shared experiment fields may not be re-declared in a packet.

Accept the anti-duplication intent, with one precision:

A packet may contain:
- `experiment_id`;
- `arm_id` / condition reference where needed;
- immutable per-run/case evidence.

Shared condition metadata should be resolved from the immutable EXPERIMENT_MANIFEST.

If a field is duplicated for portability, it must be explicitly labeled a **snapshot** and mechanically checked against the experiment manifest, never independently editable.

Prefer reference over duplication.

---

# 7. Review 2 closure condition

Review 2 can close if DeepSeek accepts or convincingly refines these three points:

1. decision-registry inclusion = normative + externally consequential, not merely "crosses a boundary or affects acceptance";
2. reusable invariants require explicit applicability; they are not "all cases, always scored";
3. runtime assertions and engineering/process gates are different predicate kinds, preserving the frozen one-submodule rule for runtime assertions without broadening its domain.

If those converge, I consider the authority graph sufficiently precise to permit the Phase 0 rewrite later.

Do not rewrite yet.
