# Consensus Submodule Interfaces v1

**Status:** FROZEN at interface level  
**Scope:** names, goals, roles, inputs, outputs, and responsibility boundaries only.  
**Not yet defined:** internal function, schema details, operator vocabulary, prompt wording, implementation.

The production runtime remains one Doximity Ask call with three logical modules:

```text
INGEST -> STRUCTURE -> RENDER
```

The eleven submodules below are responsibility boundaries inside that single call, not separate prompts.

---

# 1. INGEST

## Parent goal

Create a high-recall, source-faithful substrate describing **what was supplied, what it said, and where it came from**, without deciding how the final note should use it.

Final output:

> source registry + span registry + stable annotated objects + source coverage accounting

---

## I1 — Source Map

**Goal**  
Identify and preserve the distinct source families and their boundaries.

**Role**  
Establish the provenance frame for everything downstream.

**Input**  
- raw pasted chart material;
- current encounter transcript.

**Output**  
- ordered source registry;
- bounded source blocks;
- available source-level metadata such as source type, date, service/author, transcript speaker labels.

**Distinctive boundary**  
I1 answers **"which source is this?"**  
It does not split source text into semantic objects and does not decide relevance.

---

## I2 — Span Registry

**Goal**  
Create complete mechanically bounded coverage of every recognized source.

**Role**  
Make source coverage observable so no supplied fragment silently disappears.

**Input**  
- source registry;
- bounded source blocks from I1.

**Output**  
- ordered span registry;
- each span linked to exactly one source;
- every supplied source fragment represented by a mechanically defined span.

**Distinctive boundary**  
I2 answers **"what source fragments were received?"**  
It does not decide what those fragments mean clinically.

---

## I3 — Object Extraction

**Goal**  
Convert source spans into stable, independently useful clinical propositions while preserving high recall.

**Role**  
Create the durable semantic objects that all later note uses reference.

**Input**  
- source registry;
- span registry;
- span text.

**Output**  
- stable semantic object set;
- each object linked to its source span;
- span-to-object accounting, including spans that yield no clinical object but remain accounted for.

**Distinctive boundary**  
I3 answers **"what clinical propositions are present?"**  
It does not decide what the note will do with them.

---

## I4 — Source Annotation

**Goal**  
Attach source-grounded attributes to stable objects without deciding their final encounter-level use.

**Role**  
Preserve provenance, attribution, temporality, and explicit source stance.

**Input**  
- source registry;
- span registry;
- stable object set from I3.

**Output**  
- annotated object substrate;
- source-grounded provenance/attribution/temporality and other agreed source metadata;
- explicit source statements about clinician stance/adoption preserved as evidence, not yet converted into final encounter-level adoption.

**Distinctive boundary**  
I4 answers **"what source-grounded attributes belong to this object?"**  
It does not decide whether today's note adopts, emphasizes, or renders the object.

---

# 2. STRUCTURE

## Parent goal

Transform the source-faithful object substrate into a complete executable Case IR describing **what the encounter is about, what will be used, where it belongs, and how it must render**.

Final output:

> completed Case IR

All render-affecting semantic decisions must be complete before RENDER begins.

---

## S1 — Problem Model

**Goal**  
Define what the current neurologic encounter is clinically about.

**Role**  
Create the encounter-level neurologic problem/claim framework that organizes later decisions.

**Input**  
- complete INGEST source-faithful substrate.

**Output**  
- ordered neurologic problem registry;
- current problem-level claims/formulations;
- any required problem hierarchy or relationships needed for note organization.

**Distinctive boundary**  
S1 answers **"what are the problems/claims?"**  
It does not yet decide every object's use, section, or render form.

---

## S2 — Semantic Adjudication

**Goal**  
Resolve the encounter-level semantic meaning and relationships of the source objects.

**Role**  
Determine how objects relate to one another and to the current encounter before note-layout decisions.

**Input**  
- annotated stable objects;
- problem model from S1.

**Output**  
- semantically adjudicated object set/relationships;
- resolved duplicate/coverage, modifier, condition, reasoning-role, temporality/adoption, and similar semantic relationships;
- no section assignment and no render operator yet.

**Distinctive boundary**  
S2 answers **"what does this object mean here, and how does it relate to other objects?"**  
It does not decide whether the object is selected for the note or how it renders.

---

## S3 — Content Selection & Problem Use

**Goal**  
Decide which adjudicated objects are used in the note and for which problem(s), while preserving explicit reuse.

**Role**  
Turn the complete semantic substrate into the retained note-content set.

**Input**  
- ordered problem model;
- semantically adjudicated objects from S2.

**Output**  
- retained object-use set;
- explicit dispositions for unused clinical objects;
- problem use/reuse map for each retained object;
- complete accounting of every clinical object as used or dispositioned.

**Distinctive boundary**  
S3 answers **"what content are we using, and for which problem?"**  
It does not choose the final section, operator, wording, or unit shape.

---

## S4 — Note Blueprint / Render-Unit Compilation

**Goal**  
Convert the retained problem-linked content into the complete executable blueprint of the final note.

**Role**  
Freeze every render-affecting decision so RENDER has nothing semantic left to choose.

**Input**  
- ordered problem model;
- retained object-use set and problem-use map from S3;
- adjudicated semantic relationships from S2;
- section/style/operator contracts.

**Output**  
A completed Case IR containing:
- ordered section list;
- explicit section assignment;
- render units;
- unit membership/member roles;
- rhetorical class;
- canonical operator;
- order;
- reuse accounting;
- completeness status.

**Standing-item exception**  
A render unit may have zero source-object members only for a closed-list standing item whose explicit trigger conditions are satisfied by the structured Case IR/problem state. Such units participate in the same completeness accounting as other units.

**Distinctive boundary**  
S4 answers **"exactly what must render, where, in what unit, with which operator, and in what order?"**  
It does not write prose.

---

# 3. RENDER

## Parent goal

Convert the completed Case IR into the final clinical note **without changing any semantic decision**.

Final output:

> final note

---

## R1 — Unit Realization

**Goal**  
Convert each valid render unit into its canonical clinical-language realization.

**Role**  
Perform the smallest allowed language-generation step.

**Input**  
- one render unit;
- referenced object payload;
- selected operator definition;
- section-scoped style rules.

**Output**  
- rendered unit text corresponding to that unit.

**Distinctive boundary**  
R1 answers **"how does this one already-decided unit read?"**  
It cannot choose content, section, order, problem, operator, or membership.

---

## R2 — Section Composition

**Goal**  
Turn already-rendered, already-ordered units into coherent prose-section text without altering their semantics.

**Role**  
Provide local prose continuity for sections such as HPI/history that are not naturally one-unit-per-bullet.

**Input**  
- ordered rendered unit texts for one prose-composed section;
- section composition/style contract.

**Output**  
- completed prose text for that section.

**Hard boundary**  
R2 may:
- join adjacent units in unit order;
- add punctuation and whitespace permitted by the section contract.

R2 may not:
- delete;
- reorder;
- create new semantic content;
- merge two units into a new proposition;
- add a temporal or causal connective not represented by the units.

**A/P exception**  
A/P is rendered as its specified bullet/unit structure and bypasses R2 unless a future explicitly approved section contract states otherwise.

**Distinctive boundary**  
R2 answers **"how do already-rendered units read together as prose?"**  
It does not perform semantic synthesis.

---

## R3 — Note Assembly

**Goal**  
Assemble completed sections into the final note exactly according to the STRUCTURE-supplied blueprint.

**Role**  
Produce the final note artifact and formatting shell.

**Input**  
- ordered section list from the Case IR;
- completed section texts from R2 where applicable;
- direct rendered unit/bullet output for sections that bypass R2;
- final formatting contract.

**Output**  
- final clinical note.

**Distinctive boundary**  
R3 answers **"how are the already-approved sections packaged into the final note?"**  
It cannot add, omit, reorder, or semantically rewrite sections.

---

# Interface chain

```text
RAW PASTE
   |
   v
I1 SOURCE MAP
   -> source registry
   |
   v
I2 SPAN REGISTRY
   -> span registry
   |
   v
I3 OBJECT EXTRACTION
   -> stable objects
   |
   v
I4 SOURCE ANNOTATION
   -> annotated object substrate
   |
   v
S1 PROBLEM MODEL
   -> problem registry
   |
   v
S2 SEMANTIC ADJUDICATION
   -> adjudicated object set
   |
   v
S3 CONTENT SELECTION & PROBLEM USE
   -> retained use map + dispositions
   |
   v
S4 NOTE BLUEPRINT / UNIT COMPILATION
   -> completed Case IR
   |
   v
R1 UNIT REALIZATION
   -> rendered units
   |
   +--> R2 SECTION COMPOSITION where section contract requires prose
   |       -> completed prose sections
   |
   v
R3 NOTE ASSEMBLY
   -> FINAL NOTE
```

This diagram is a **logical dependency graph** inside one model call, not a claim that Doximity executes eleven separate prompts.

---

# Distinctiveness rule

The frozen architectural rule is:

> **One decision has one owner. Data may pass through multiple submodules; decision authority may not be duplicated.**

Each submodule therefore owns one primary question:

| Submodule | Unique question |
|---|---|
| I1 | Which source is this? |
| I2 | What source fragments were received? |
| I3 | What clinical propositions are present? |
| I4 | What source-grounded attributes belong to them? |
| S1 | What are the encounter's neurologic problems/claims? |
| S2 | What do the objects mean here and how do they relate? |
| S3 | Which content is used, and for which problem? |
| S4 | Exactly what must render, where, how, and in what order? |
| R1 | How does one specified unit read? |
| R2 | How do specified prose units read together without semantic change? |
| R3 | How are completed sections assembled into the final note? |

---

# Freeze statement

ChatGPT and DeepSeek agree on all eleven submodules at the interface level, including their goals, inputs, outputs, and responsibility boundaries, with the two clarifications above for S4 standing-item units and R2 prose-only bounded composition.

The next design layer may define **function** inside each submodule, but must not change these interfaces without explicitly reopening the architecture.
