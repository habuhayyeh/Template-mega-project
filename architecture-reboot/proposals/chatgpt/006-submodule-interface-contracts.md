# ChatGPT proposal 006 — submodule interface contracts

## Scope

This document defines only:

- submodule name;
- goal;
- input;
- output.

It does **not** define internal function, algorithms, rules, schemas, or prompt wording.

The purpose is to freeze the architecture interfaces before discussing how each submodule performs its work.

---

# Runtime architecture

```text
INGEST
  I1 Source Map
  I2 Span Registry
  I3 Object Extraction
  I4 Source Annotation

STRUCTURE
  S1 Problem Model
  S2 Semantic Adjudication
  S3 Content Selection & Problem Use
  S4 Note Blueprint / Render-Unit Compilation

RENDER
  R1 Unit Realization
  R2 Section Composition
  R3 Note Assembly
```

All are logical responsibilities inside one Doximity Ask call, not separate prompts.

---

# 1. INGEST

## I1 — Source Map

**Goal**

Identify and preserve the distinct source families and their boundaries.

**Input**

- raw pasted chart material;
- current encounter transcript.

**Output**

- ordered source registry;
- bounded source blocks;
- available source-level provenance such as source type, date, service/author, and transcript speaker labels.

---

## I2 — Span Registry

**Goal**

Create complete mechanically bounded coverage of each recognized source without semantic summarization.

**Input**

- ordered source registry;
- bounded source blocks from I1.

**Output**

- ordered span registry;
- each span linked to exactly one source;
- every received source fragment represented by a span boundary.

---

## I3 — Object Extraction

**Goal**

Convert source spans into stable, independently useful clinical propositions while preserving high recall.

**Input**

- source registry;
- span registry;
- span text.

**Output**

- stable semantic object set;
- each object linked to its source span;
- span-to-object accounting, including spans that yield no clinical object but remain explicitly accounted for.

---

## I4 — Source Annotation

**Goal**

Attach source-grounded attributes to the stable objects without deciding how the final note will use them.

**Input**

- source registry;
- span registry;
- stable object set from I3.

**Output**

- annotated object substrate, including source-grounded provenance/attribution/temporality and other agreed source-level metadata;
- explicit source statements about clinician stance/adoption preserved as source evidence, not yet converted into final encounter-level adoption.

---

## INGEST final output

> **Source-faithful substrate = source registry + span registry + annotated stable objects + source coverage accounting.**

This becomes the sole semantic input to STRUCTURE.

---

# 2. STRUCTURE

## S1 — Problem Model

**Goal**

Define what the current neurologic encounter is clinically about.

**Input**

- INGEST source-faithful substrate.

**Output**

- ordered neurologic problem registry;
- current problem-level claims/formulations;
- any necessary problem hierarchy/relationship needed for note organization.

---

## S2 — Semantic Adjudication

**Goal**

Resolve the semantic relationships and encounter-level status of the source objects without yet deciding the final note layout.

**Input**

- annotated stable objects;
- problem model from S1.

**Output**

- semantically adjudicated objects/relationships, including the agreed encounter-level interpretation needed downstream;
- resolved duplicate/coverage, modifier, condition, reasoning-role, temporality/adoption, and similar semantic relationships;
- no section assignment and no render operator yet.

---

## S3 — Content Selection & Problem Use

**Goal**

Decide which adjudicated objects are used in this note and for which problem(s), while preserving explicit reuse.

**Input**

- problem model;
- semantically adjudicated object set from S2.

**Output**

- retained object-use set;
- explicit omissions/dispositions for unused clinical objects;
- problem use/reuse map for each retained object;
- complete accounting of every clinical object as used or dispositioned.

This submodule does **not** choose the final note section or rendering operator.

---

## S4 — Note Blueprint / Render-Unit Compilation

**Goal**

Convert the retained problem-linked object uses into the complete executable blueprint of the final note.

**Input**

- ordered problem model;
- retained object-use set and problem-use map from S3;
- adjudicated semantic relationships from S2;
- section/style/operator contracts.

**Output**

- completed Case IR containing:
  - ordered section list;
  - explicit section assignment;
  - render units;
  - unit membership/member roles;
  - rhetorical class;
  - canonical operator;
  - order;
  - required reuse accounting;
  - completeness status.

The output must be complete enough that RENDER makes no semantic selection decisions.

---

## STRUCTURE final output

> **Completed Case IR = what must appear, where it appears, which problem it serves, how objects combine, which operator renders it, and in what order.**

---

# 3. RENDER

## R1 — Unit Realization

**Goal**

Convert each valid render unit into its canonical clinical-language realization without changing the unit's semantics.

**Input**

- one render unit at a time;
- referenced object payload;
- selected operator definition;
- section-scoped style rules.

**Output**

- rendered unit text corresponding to that unit.

---

## R2 — Section Composition

**Goal**

Turn the already-rendered, already-ordered units of one section into coherent section text without changing their semantic content or order.

**Input**

- ordered rendered unit texts for one section;
- section composition/style contract.

**Output**

- completed text for that section.

---

## R3 — Note Assembly

**Goal**

Assemble the already-completed sections into the final note artifact exactly according to the STRUCTURE-supplied section blueprint.

**Input**

- ordered section list from the Case IR;
- completed section texts from R2;
- final formatting contract.

**Output**

- final clinical note.

---

## RENDER final output

> **Final note = faithful surface realization of the completed Case IR.**

---

# Interface summary

| Submodule | Goal in one phrase | Input | Output |
|---|---|---|---|
| I1 Source Map | identify sources | raw paste | source registry |
| I2 Span Registry | account for source boundaries | source registry + source text | span registry |
| I3 Object Extraction | extract stable propositions | spans | stable objects |
| I4 Source Annotation | attach source-grounded metadata | sources + spans + objects | annotated object substrate |
| S1 Problem Model | define encounter problems | annotated substrate | problem registry |
| S2 Semantic Adjudication | resolve object meaning/relationships | objects + problems | adjudicated object set |
| S3 Content Selection & Problem Use | decide use and problem reuse | adjudicated objects + problems | retained use map + dispositions |
| S4 Note Blueprint / Unit Compilation | define complete executable note plan | use map + adjudication + contracts | completed Case IR |
| R1 Unit Realization | render one unit | unit + objects + operator/style | unit text |
| R2 Section Composition | compose one section | ordered unit text | section text |
| R3 Note Assembly | assemble note | ordered sections | final note |

---

# Why this differs from the earlier 4/4/3 wording

The earlier labels created overlap:

- Object Adjudication included problem use/relevance.
- View Projection included section use.
- Render-Unit Compilation also needed section/operator decisions.

This revision gives each STRUCTURE submodule one distinct output:

1. **S1:** problems;
2. **S2:** semantic adjudication;
3. **S3:** retained content + problem use;
4. **S4:** note blueprint / Case IR.

That makes the authority boundaries much easier to audit.

---

# Requested DeepSeek decision

Review **only** the names, goals, inputs, and outputs.

For every submodule, respond with one of:

- ACCEPT;
- MERGE WITH <submodule>;
- SPLIT;
- REVISE INPUT;
- REVISE OUTPUT;
- REVISE GOAL.

Do not define internal functions yet.

The immediate objective is to freeze the submodule interface contracts before discussing how any submodule performs its work.
