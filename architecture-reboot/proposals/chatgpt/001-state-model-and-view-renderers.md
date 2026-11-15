# ChatGPT Proposal 001 — State Model + View Renderers, Not a Prose Pipeline

## Thesis

The central problem is not that the current system lacks enough modules. It is that the same clinical meaning is repeatedly **reinterpreted** at several stages.

The redesign should therefore stop moving prose through a long chain of transformations.

Instead:

> **Decompose source material once into persistent semantic objects, attach explicit relationships to those objects, then generate multiple note views from the same state.**

The architecture should behave more like a **small compiler / blackboard system / DAG** than a prose pipeline.

Modularity should live in **responsibility boundaries and data contracts**, not primarily in the number of uploaded files.

---

# 1. What I would keep

## 1.1 Atomic decomposition

I would keep decomposition.

A source sentence can contain multiple independently useful propositions. Those propositions need independent provenance, routing, and reuse.

Example:

> "Her left MCA stroke was two years ago and she has mild residual aphasia."

should be representable as at least two atomic propositions:

- prior left MCA stroke, two years prior;
- residual mild aphasia.

Decomposition protects fidelity and allows the same source to support different note sections.

### Important change

Decomposition should happen **once**.

Objects should not be destroyed, rewritten into new identities, or copied into new representations as they travel through the system.

---

# 2. What I would stop doing

## 2.1 Stop repeated reallocation

The current architectural smell is:

`decompose -> classify -> allocate -> organize -> assemble -> reinterpret -> render`

where later stages repeatedly decide what earlier objects "really mean."

Instead of reallocating objects, keep one persistent object and attach metadata/relations.

An object should not move from one conceptual table to another. Different views should **reference the same object ID**.

## 2.2 Stop asking the final writer to rediscover semantics

The renderer should not decide:

- whether two facts are duplicates;
- which duplicate is canonical;
- whether a COURSE item is a modifier or independent fact;
- whether two management statements are one conditional decision;
- which problem a management action belongs to;
- whether a historical statement is a current plan;
- whether two reasoning statements are equivalent.

Those are semantic planning decisions.

If reproducibility matters, they should be settled once before surface generation.

---

# 3. Proposed architecture

```
                     SOURCE MATERIAL
                           |
                           v
                  SEMANTIC INGESTION
                           |
                           v
                 PERSISTENT CASE STATE
                  /        |        \
                 /         |         \
                v          v          v
        HPI VIEW PLAN  HISTORY PLAN  A/P VIEW PLAN
                |          |          |
                v          v          v
           HPI RENDER   HISTORY     A/P RENDER
                 \         |         /
                  \        |        /
                   v       v       v
                       VALIDATION
```

The important architectural object is the **Persistent Case State**.

Everything else is a view.

---

# 4. Persistent Case State

The case state has two layers:

## 4.1 Immutable source objects

Each atomic object stores what the source actually supplied.

Minimum conceptual fields:

```text
id
source_text
normalized_proposition
semantic_kind
provenance
speaker / attribution
source_time
clinical_event_time if explicitly known
current-vs-historical source status
```

The exact schema is open for debate.

The key rule is:

> Source payload and provenance are immutable after ingestion.

Corrections create an explicit revision/adjudication record rather than silently rewriting history.

## 4.2 Relations / annotations

Clinical meaning often lives between objects, not inside one object.

Examples:

```text
DUPLICATE_OF / SAME_PROPOSITION
MODIFIES
CONDITION_OF
SUPPORTS
REFUTES
EXPLAINS
ETIOLOGY_OF
MANAGEMENT_TARGET
PROBLEM_MEMBERSHIP
CURRENTLY_ADOPTED
HISTORICAL_ONLY
SECTION_RELEVANCE
TIME_RELATION
```

I do **not** propose adopting this exact list now.

The point is structural:

> Relationships should be represented explicitly rather than rediscovered by every renderer.

This is where our old pipeline was weakest.

---

# 5. Problem model

A neurologic note is organized around neurologic problems/claims.

I would therefore treat a problem as a first-class node, not merely a heading generated late.

Conceptually:

```text
P1: seizure after prior left MCA stroke

claims:
  ...
evidence:
  ...
reasoning:
  ...
course:
  ...
management:
  ...
```

Objects reference problems; the problem does not own copied versions of the objects.

An object may support more than one view and, where clinically justified, more than one problem relation.

This prevents destructive "allocation."

---

# 6. View Plans

Before prose generation, each note section gets a **view plan**.

A view plan is not another clinical summary. It is a render specification referencing persistent IDs.

Example A/P plan:

```text
PROBLEM P1

LINE A
class: FACT
head: O7
modifier: O8
covered: O53

LINE B
class: FACT
head: O17
covered: O44

LINE C
class: REASONING
head: O39
covered: O23

PLAN LINE D
head: O12
condition: O25
bucket: anticoagulation
```

The important difference from the current Handoff is:

> The plan tells the renderer what semantic decisions are already settled.

The renderer is not asked to rediscover equivalence, ownership, or composition.

### Other views

The HPI view can reference the same underlying objects but specify:

- chronological ordering;
- presentation-specific history;
- relevant negatives;
- triggers/risk factors;
- no diagnostic synthesis at the end.

The Workup view can reference the same result objects without copying them into a second ontology.

---

# 7. Renderer responsibilities

The renderer should have a deliberately small freedom envelope.

Allowed:

- punctuation;
- capitalization;
- local grammar;
- approved abbreviations;
- bounded tense/voice normalization;
- approved temporal surface transformations;
- folding explicitly designated modifiers/conditions;
- the user's preferred A/P voice, e.g. impersonal rather than conversational first person.

Not allowed:

- duplicate detection;
- problem assignment;
- current-vs-historical adoption;
- clinical relevance selection;
- etiologic inference;
- reasoning reconstruction;
- management-target inference;
- deciding whether two management entries compose.

This is the boundary I think will matter most for reproducibility.

---

# 8. Diagnostics should be architectural, not retrospective explanations

We should stop asking the model:

> "Why did you do that?"

as though this were a software debugger.

Instead, during development, require an **execution ledger** with fixed observable decisions.

Example:

```text
G1 | FACT | HEAD=O7 | MODIFIER=O8 | COVERED=O53 | OUTPUT=L3
G2 | PLAN | HEAD=O12 | CONDITION=O25 | OUTPUT=L10
O18 | UNGROUPED | ELIGIBLE | OUTPUT=L4
O19 | UNGROUPED | OMITTED | REASON=NOT_SELECTED
```

This is not chain-of-thought.

It is a contract-action ledger.

Then diagnostics can distinguish:

- semantic planner drift;
- renderer contract violation;
- simple wording drift;
- validator failure.

Production can hide the ledger; test mode preserves it.

---

# 9. Validation

Validation should be independent of generation whenever possible.

Three layers:

## 9.1 State validation
Before rendering:

- every relation references real IDs;
- no impossible group composition;
- provenance exists;
- current/historical status is explicit where required;
- problem relationships are valid.

## 9.2 Render-plan validation

- every required HEAD exists;
- every COVERED member is accounted for;
- no object is accidentally rendered twice when the plan says once;
- plan conditions remain attached to the correct action;
- ordering constraints are explicit.

## 9.3 Output validation

- no unsupported clinical payload;
- all required plan units rendered;
- forbidden first-person A/P voice absent if that is the style contract;
- no prohibited duplication;
- section boundaries respected.

The validator reports failure. It does not silently rewrite the note.

---

# 10. Modularity vs Doximity packaging

This is where I would separate **development modularity** from **deployment packaging**.

## Development

In GitHub, make the system highly modular:

```
modules/
  semantic-model.md
  planner.md
  ap-renderer.md
  hpi-renderer.md
  history-renderer.md
  style.md
  validation.md
  diagnostics.md
```

Small modules are easier for humans and agents to reason about.

## Deployment

Do **not** upload 20 files to Doximity.

Compile the modules deterministically into a small deployment package, for example:

```
DIST/
  ENGINE.md
  STYLE.md
  TEST_MODE.md
```

or even one `ENGINE.md` if Doximity behaves better with fewer attachments.

The inability to upload a ZIP is therefore not an architectural blocker.

The repo can be modular while Doximity receives a compiled artifact.

This is analogous to source files versus a built executable.

---

# 11. Platform boundary

The architecture should be platform-agnostic.

Doximity is a deployment target with constraints, not the ontology.

We should explicitly distinguish:

### Architecture
What decisions must exist and where they belong.

### Execution topology
Whether those decisions are produced in:
- one Doximity call;
- two manual Doximity passes;
- Doximity + an external controller;
- another model/tool.

We should not distort the semantic model merely because today's UI accepts only certain attachment patterns.

At the same time, if Doximity cannot reliably perform a required multi-pass operation, that is a real deployment constraint and must be tested.

---

# 12. The major unresolved question

The hardest remaining architectural question is:

> **Who creates the Persistent Case State and View Plans?**

Possible answers:

### Model A — single generative planner
One model reads all source material and emits the state/relations/view plans.

Pros:
- simplest operationally.

Cons:
- semantic planning itself may drift.

### Model B — staged semantic planning
One pass extracts atomic objects; another adjudicates relationships/view plans.

Pros:
- easier to audit.

Cons:
- more calls and orchestration.

### Model C — deterministic + model hybrid
Deterministic code handles what can be mechanical; the model handles semantic relations only.

Pros:
- likely strongest reproducibility.

Cons:
- may be impossible inside Doximity alone.

### Model D — single-call hidden planning + output ledger
Doximity creates state and note in one run but emits an observable ledger in test mode.

Pros:
- operationally compatible with one-call environments.

Cons:
- the ledger may describe the result rather than function as a truly independent intermediate artifact.

I do **not** think we should choose among these yet without DeepSeek's critique.

---

# 13. What I would explicitly reconsider from the old architecture

Starting clean, I would challenge these assumptions:

1. **Do we need six semantic kinds at all?**
   Maybe yes, but they should earn their place.

2. **Do we need 01/02/03/04/05 as separate stages?**
   Probably not in their current form.

3. **Do we need an A/P Handoff as prose-like intermediate state?**
   Possibly not. A typed view plan may replace it.

4. **Should body and A/P branches be truly independent after ingestion?**
   Probably yes, but both should query the same state rather than consume duplicated representations.

5. **Should routing be exclusive?**
   Probably not at the object level. One object may legitimately feed HPI, history, workup, and A/P.

6. **Should duplicate resolution happen at render time?**
   No.

7. **Should management-to-problem targeting be inferred from medications?**
   No. It should be source-grounded or explicitly adjudicated.

8. **Should Doximity be expected to behave like a deterministic compiler?**
   Only for decisions we have already made explicit. Its generative role should be narrow.

---

# 14. My current preferred abstraction

If I had to name the system now:

> **Source-faithful semantic case model + note view compiler**

rather than:

> note-generation pipeline.

That framing better matches what we are trying to build.

---

# 15. Questions for DeepSeek

Please challenge this proposal rather than merely refine it.

Specifically:

1. Is a persistent semantic state/graph actually simpler than the current pipeline, or are we replacing one complexity with another?
2. What is the **minimal** relation set needed to solve the failure modes we have actually observed?
3. Which of our current semantic kinds are necessary, redundant, or wrongly defined?
4. Should problem membership be one-to-one, one-to-many, or view-specific?
5. Is a separate View Plan necessary, or can relations on the case state directly drive renderers?
6. Where should semantic duplicate resolution happen?
7. What is the cleanest representation for current-vs-historical management?
8. How should clinician reasoning be preserved without converting it into generic evidence?
9. Can Doximity realistically generate the state and note in one call, or must we accept multi-pass/manual/external orchestration?
10. What diagnostic ledger can Doximity plausibly emit that is actually useful without pretending to expose hidden reasoning?
11. Is "compile many repo modules into one/few Doximity files" the right deployment strategy?
12. Which parts of this proposal are overengineered?
13. Propose a materially different architecture if you believe one is better.
14. Identify the smallest experiment that would distinguish your preferred architecture from mine.

The next step should be architectural critique, not implementation.
