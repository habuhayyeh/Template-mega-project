# Consensus Architecture v0.1

**Status:** structural consensus draft.  
**Branch:** `architecture-reboot-v2`  
**Implementation:** not authorized yet.

This document consolidates the architecture points accepted by both ChatGPT and DeepSeek after review of the original pipeline failures, the Doximity reproducibility gradient, B+ operator experiment, and operator stress suite.

---

## 1. Production constraint

The production workflow is:

> **one paste -> one Doximity Ask call -> one final note**

The paste contains chart material plus the encounter transcription.

No human carries intermediate artifacts between model calls in the production workflow.

Therefore every semantic planning decision and final rendering step must occur inside one Doximity call, even though the design is described in logical modules.

Logical modules are **responsibility boundaries**, not runtime passes.

---

## 2. High-level architecture

```text
RAW PASTE
   |
   v
SOURCE SPAN ACCOUNTING
   |
   v
SEMANTIC INGEST / ADJUDICATION
   |
   v
CASE IR
   |-- source-linked objects
   |-- problems
   |-- current/historical/adoption metadata
   |-- explicit render units
   |     |-- problem  (required for A/P units; optional for body units)
   |     |-- rhetorical class
   |     |-- canonical operator
   |     |-- object member roles
   |     |-- order
   |     '-- section
   |
   v
CANONICAL OPERATOR RENDERING
   |
   v
FINAL NOTE

TEST MODE additionally emits:
   CASE IR / execution trace

External engineering validation:
   A. mechanical IR -> note checker
   B. separate semantic source -> IR audit
```

There is **no separate model-executed PROJECT stage** between Case IR and rendering.

---

## 3. Source spans

The raw paste is first represented using mechanically preserved source boundaries.

A span is not a semantic proposition.

Preferred examples:
- pasted line;
- transcript speaker turn;
- utterance;
- clearly delimited chart block line.

Example:

```text
S12 | source=Transcript | speaker=Daughter | text="Her memory has been getting worse for about a year..."
```

One source span may produce multiple semantic objects.

Every source span must receive at least one disposition, for example:

```text
OBJECTS=[O36,O37]
NOT_CLINICAL
NOT_USED_BY_THIS_NOTE
MERGED_SOURCE
UNRESOLVED
```

The exact closed disposition vocabulary remains to be finalized.

The invariant is:

> no clinically meaningful source content silently disappears.

This design depends on the actual Doximity paste layout preserving usable boundaries. That must be tested with a real synthetic paste example.

---

## 4. Semantic objects

Each independently useful clinical proposition receives one stable object identity.

Objects are source-linked and non-destructive.

Conceptually:

```text
OBJECT O36
kind=FACT
text="memory worsening over a year"
source_span=S12
provenance=...
speaker=Daughter
source_temporality=CURRENT_SOURCE
current_adoption=NOT_APPLICABLE
```

The same object may participate in multiple render units.

Do not clone an object merely because the same proposition contributes to more than one problem or note section.

### Kind taxonomy

The leading candidate is:

```text
IDENTIFIER
FACT
COURSE
REASONING
PLAN
```

but this is **not ratified**.

What is ratified:

- REASONING is first-class;
- claim / qualifier / etiology / uncertainty / adjudication belong as reasoning roles rather than generic evidence;
- the exact fate of COURSE should be determined by reproducibility evidence, not preference.

---

## 5. Temporality and adoption

Source history and current clinical adoption are separate dimensions.

Conceptually:

```text
source_temporality = CURRENT_SOURCE | HISTORICAL_SOURCE
current_adoption   = ADOPTED | NOT_ADOPTED | NOT_APPLICABLE
```

A historical diagnosis/recommendation can therefore be:
- historical and currently adopted;
- historical and not adopted.

This rule applies to both REASONING and PLAN when relevant.

No drug-class or diagnosis heuristic may infer adoption.

---

## 6. Problems

Problems are explicit clinical organizational nodes.

Each **A/P** render unit owns exactly one problem.

A body unit requires no problem. It may carry an optional problem association where the section contract asks for one, and that association is not an ownership claim.

A problem candidate exists only when the neurologic subject requires its own current assessment question or status in this encounter.

A subject that supports, refutes, or contextualises another problem remains evidence or context unless it is independently assessed. These are examples, not an exhaustive list.

Every candidate must be source-grounded: a subject the model infers but the encounter never addresses cannot become a problem.

A problem's claim is a **representation**, not a single object reference. A representation may carry more than one candidate together with the relation among them. The kinds of representation and their fields are defined downstream.

A source object may be reused by units belonging to different problems when that reuse is clinically justified.

Optional `primary_problem` on an object may be used for accounting/navigation, but it does not restrict reuse.

Problem organization remains neurologically centered.

---

## 7. Render units

A render unit is the executable semantic decision that converts one or more source objects into one note line or bounded output unit.

It contains no rewritten clinical summary prose.

Conceptually:

```text
UNIT U7
section=AP
problem=P1            # required for A/P units; optional for body units
class=FACT
operator=FACT_WITH_TIME_AND_PROVENANCE
members:
  O7  role=HEAD
  O8  role=MODIFIER
  O53 role=COVERED
order=20
```

or:

```text
UNIT U11
section=AP
problem=P1            # required for A/P units; optional for body units
class=PLAN
operator=PLAN_CONDITIONAL
members:
  O12 role=HEAD
  O25 role=CONDITION
order=60
```

Render units encode every semantic decision that materially affects:
- merge/split;
- problem placement;
- rhetorical class;
- condition scope;
- canonical member;
- modifier attachment;
- ordering;
- operator choice.

These decisions are fixed **before final rendering**.

The operator stress suite supports this as the stable execution boundary.

Important limitation:

> The stress suite proves operator execution fidelity, not upstream operator selection fidelity.

Operator selection is therefore part of the Case-IR reproducibility experiment.

---

## 8. Canonical operators

Operators come from a closed vocabulary.

The exact list is not yet ratified.

Examples under consideration include families such as:
- direct fact;
- fact + time;
- fact + provenance;
- direct reasoning;
- reasoning test-purpose;
- direct plan;
- conditional plan.

Each operator defines:
- required member roles;
- allowed optional roles;
- fixed wording elements;
- allowed transformations;
- output cardinality;
- failure conditions.

Malformed or under-specified units fail closed.

Production may use a generic:

```text
CONTRACT_ERROR
```

rather than a complex overlapping diagnostic taxonomy.

---

## 9. Rendering boundary

The renderer is deliberately weak.

Allowed:
- capitalization;
- punctuation;
- approved abbreviations;
- operator-fixed wording;
- approved number/time normalization;
- explicit modifier/condition folding;
- section-scoped voice transforms;
- approved provenance display.

Forbidden:
- deciding duplicate identity;
- inventing missing semantic payload;
- deciding problem ownership;
- changing unit membership;
- selecting a different operator;
- moving content across rhetorical classes;
- silently dropping a unit;
- silently repairing malformed structure.

A/P uses impersonal clinical voice.

Body sections may use different voice rules.

---

## 10. Validation architecture

### 10.1 Mechanical conformance checker

Consumes:
- emitted Case IR;
- final note.

Checks only mechanical predicates, such as:
- every unit references valid object IDs;
- every operator exists and typechecks;
- every required role is present;
- every unit maps to the expected note output;
- every note output maps to a unit;
- order is respected;
- covered members do not independently render when forbidden;
- condition scope is preserved;
- only allowed operator/transform text is introduced;
- A/P voice rule is obeyed;
- every object is either used by >=1 unit or explicitly dispositioned;
- within one A/P section and its owning problem, a given object may participate in at most one render unit, unless explicit reuse permits otherwise;
- this rule does not apply to body units; body duplicate and use constraints are governed by the section contract;
- cross-section reuse is allowed;
- explicit cross-problem reuse within the same section is allowed.

This checker does **not** reconstruct semantic units from objects.

### 10.2 Semantic source-fidelity audit

Consumes:
- raw source spans;
- Case IR.

Evaluates:
- source support;
- semantic completeness;
- object decomposition;
- kind/role correctness;
- problem use;
- duplicate coverage;
- modifier/condition linkage;
- current adoption;
- operator selection.

This is a semantic review instrument, not a deterministic checker unless a specific predicate is mechanical.

For engineering it may use:
- reviewed oracles;
- independent model review;
- human review;
- targeted deterministic predicates where available.

---

## 11. Test-mode ledger

Test mode should emit the Case IR / execution trace.

The trace is not hidden reasoning and is not trusted as proof.

It exists so an independent checker/auditor can answer:

- what source spans became objects;
- what objects were used;
- which unit used them;
- what operator was chosen;
- where the unit rendered;
- what was explicitly omitted/dispositioned.

Production may suppress this artifact if Doximity supports a clean way to do so.

If production suppresses the Case IR/trace, independent external checking is therefore a **test/predeployment property**, not a claim that every live production note is mechanically verified. Production reliability claims must rest on validated test-mode behavior and regression evidence unless a practical runtime checking surface is later available.

---

## 12. Development modularity vs deployment

GitHub source should remain modular by responsibility.

Possible modules:

```text
ingest-contract
object-schema
reasoning-roles
render-unit-schema
operators
section-style
standing-items
validation
diagnostics
```

These are **source modules**, not Doximity runtime stages.

A build step compiles them into a small deployment artifact, likely one or a few Markdown/text files.

The build must fail on:
- contradictory rules;
- two rules with authority over the same decision;
- out-of-scope rules;
- rules without tests;
- duplicate or shadowed operator definitions.

File count itself is not the target.

---

## 13. What has been explicitly rejected

The reboot rejects:

- repeated prose reinterpretation across `01 -> 02 -> 03 -> 04 -> 05` style stages;
- destructive object routing;
- duplicate resolution at final rendering;
- a model-executed semantic PROJECT stage;
- prose-like Handoff artifacts requiring reinterpretation;
- large speculative relation ontologies;
- mandatory free-text rationale for semantic relations;
- treating a self-reported ledger as proof;
- treating exact error-label wording as the production invariant;
- cloning one proposition solely to give it multiple problem homes;
- assuming every sentence is one semantic proposition;
- assuming Doximity can provide hidden internal reasoning traces.

---

## 14. Remaining design questions

These are now narrow and experimentally resolvable:

1. Exact top-level object kinds.
2. Whether COURSE remains separate or folds into FACT/time metadata.
3. Exact canonical operator vocabulary.
4. Final field-level Case IR schema.
5. Exact span disposition vocabulary.
6. Exact semantic-audit procedure.
7. Whether test-mode IR can be cleanly suppressed in production.
8. The optimized Doximity paste-layout/provenance contract. The ingestion handoff is sufficient for architecture; exact delimiters/headings are now an E1 fixture/optimization question rather than a structural blocker.

These are not reasons to reopen the overall architecture.

---

## 15. Next decisive experiment

### E1 — Case IR reproducibility

Use one fixed synthetic source paste in the exact intended Doximity Ask layout.

Run it in fresh conversations with the same model/mode.

Ask for **Case IR only**, not the final note.

Compare separately:

- source-span dispositions;
- object coverage and identity;
- object kind;
- reasoning role;
- source temporality;
- current adoption;
- problem use;
- render-unit membership;
- operator selection;
- HEAD/MODIFIER/CONDITION/COVERED roles;
- unit order.

The primary metric is **render-unit/operator agreement**, not a single aggregate similarity score.

A clinically important disagreement is a failure even if global Jaccard similarity remains high.

### Interpretation

If objects drift:
> ingest/decomposition remains unstable.

If objects are stable but units/operators drift:
> semantic adjudication/planning remains unstable.

If Case IR is stable but rendered notes drift:
> operator/render contract is incomplete.

This experiment localizes the remaining problem before implementation.

---

## 16. E1 input-fixture requirement

The ingestion-layer handoff now provides enough architectural structure to proceed.

E1 should use a representative **synthetic** Ask paste containing:
- transcript;
- most recent neurology note;
- current encounter notes;
- prior notes;
- imaging/studies;
- recent and relevant historical labs.

Exact delimiters, headings, source order, and how much labeling Doximity needs are test variables to optimize. The clinician should not be required to manually author internal SRC/SPAN/IR syntax in routine production use.
