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
Identify the neurologic subjects this encounter is actually about, and partition them.

**Role**
Propose problem candidates, attach claim candidates to them, and own the partition. It decides no
claim and no adoption verdict.

**Input**
- complete INGEST source-faithful substrate.

**Output**
- problem candidates with stable ids and source anchors;
- for each problem candidate, its claim candidates — the source formulations that could become, or
  contribute to, a claim representation;
- the partition: which claim candidate maps to which problem candidate; each claim candidate maps to
  exactly one problem candidate;
- structured salience inputs, including `management_reference_spans[]` — the spans containing a
  management statement referencing the problem candidate's subject. Salience evidence only: it
  records that a statement exists, never that the subject is a problem, adopted, or current;
- candidate-level relationships the substrate states explicitly.

**Distinctive boundary**
S1 answers **"which neurologic subjects need their own assessment question, and what belongs to what?"**
Partition authority is exclusive: downstream modules may not merge, split, or re-parent problem
candidates or their claim candidates. S1 does not decide which candidate is the current claim, whether
a prior formulation is adopted, or what order problems render in.

---

## S2 — Semantic Adjudication

**Goal**
Resolve what the source objects mean for this encounter, including whether prior material is current.

**Role**
Adjudicate relations among objects and among claim candidates, decide encounter-level adoption,
assign reasoning roles, and produce approved claim representations.

**Input**
- annotated stable objects, including the source temporality recorded during annotation;
- problem candidates, their claim candidates, and the partition between them, from S1.

**Output**
- adjudicated object relations: duplicates, modifiers, conditions, reasoning roles;
- encounter-level adoption decisions per object, stated against source evidence;
- for each problem candidate, the relation among its claim candidates — for example COMPETING,
  COMPLEMENTARY, NESTED, or UNRESOLVED; the vocabulary is defined downstream;
- zero or more approved claim representations per problem candidate, which may be assembled from
  source-grounded objects and relations and are not limited to sources already phrased as claims;
- where no claim representation can be semantically approved, an explicit state that S3 can act on.

**Distinctive boundary**
S2 may adjudicate source-grounded cross-problem and cross-object relations. It may **not** use such a
relation to merge, split, or re-parent the S1 partition; claim candidates whose relation forms one
representation stay within one problem candidate. **Source temporality is not S2's** — it is recorded
during annotation and only consumed here.

**Approval is a safety property.** S2 may expose more than one approved representation for a problem
only when choosing among them requires no further semantic adjudication. Where the choice would change
clinical meaning, S2 resolves it and records structured support before exposing the set to S3.


S2 answers **"what do these objects mean here, and which claim formulations are defensible?"**
It does not select content, choose sections, or order. Documenting an unresolved semantic choice does
not make it safe.
---

## S3 — Content Selection & Problem Use

**Goal**
Decide what the note uses, under which problem, and which approved representation each rendered A/P
problem carries.

**Role**
Turn the adjudicated substrate into the rendered-problem set and retained content, and account for
every candidate and every object.

**Input**
- problem candidates from S1;
- adjudicated objects, adoption decisions and approved claim representations from S2.

**Output**
- the set of problems that render;
- exactly one outcome for every S1 problem candidate: RENDERED, or NOT_RENDERED with a typed reason
  and, where the reason family depends on upstream state, basis references to that state;
- retained object-use set;
- explicit dispositions for unused clinical objects;
- problem use/reuse map for each retained object;
- for each rendered A/P problem, one representation taken from S2's approved set;
- complete accounting of every clinical object as used or dispositioned.

**Distinctive boundary**
S3 answers **"what content are we using, for which problem, and which approved claim does it carry?"**
It may not synthesise a representation, promote an unresolved relation to a single claim, or merge
representations. S3 may not include or render an A/P problem that lacks an approved representation. It
accounts for candidates as well as objects: a candidate that renders nothing leaves a record, not a
silence.


**It does not resolve semantic ambiguity.** S3 may not include or render an A/P problem that lacks an
S2-approved representation. If a separate governing requirement mandates inclusion, the seam fails or
flags rather than rendering a claimless problem. If S2's approved set for an included problem holds more
than one representation and the choice among them is not semantically free, that is an S2 defect, not
an S3 choice.
---

## S4 — Note Blueprint / Render-Unit Compilation

**Goal**
Convert the retained, problem-linked content into the complete executable blueprint of the final note.

**Role**
Freeze every render-affecting decision so RENDER has nothing semantic left to choose, and own the final
problem and unit order.

**Input**
`S4_INPUT_VIEW` — a mechanical projection assembled at the seam. Each field keeps its source owner; the
projection decides nothing.

- from S1: problem-candidate identity and structured salience/order inputs, projected only for the ids
  S3 marked RENDERED;
- from S3: the rendered set, the selected representation id per problem, retained use, problem-use/reuse;
- from S2: the selected representation's member ids, the semantic relations those members carry, the
  selected representation's own claim relation where it has one, and the duplicate/equivalence grouping
  needed to assign COVERED;
- from I3/I4: retained object payload, provenance, temporality;
- from the frozen contracts: section, style, operator definitions, and the ordering contract.

Excluded: unselected alternatives, their relations, and the adjudication trail. The exclusion is
relevance-based, not type-based: an adoption verdict is projected only where a frozen S4 function needs
it for selected or retained content.

**Output**
A completed Case IR containing: ordered section list; explicit section assignment; render units; unit
membership and **member roles (HEAD, MODIFIER, CONDITION, COVERED)**; rhetorical class; canonical
operator; order; reuse accounting; completeness status.

**Distinctive boundary**
The explicit `S4_INPUT_VIEW` does not contain the adjudication record. That is a packaging statement,
not a behavioural one: this is one shared model context, and least-privilege packaging is not
non-leakage at runtime.

S2 supplies the relations; S4 supplies the member roles. Neither may do the other's part. S4 owns the
final problem and unit order; S1's salience inputs feed that ordering and are not an order.


**Standing-item exception.** A render unit may have zero source-object members only for a closed-list
standing item whose explicit trigger conditions are satisfied by the structured Case IR. Such units
participate in the same completeness accounting as any other.

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


**Weak-R2 contract.** R2 may add whitespace, capitalisation and contract-permitted punctuation. Punctuation is a surface transform, not a lexical bridge. The lexical bridge allowlist is empty by default: R2 adds no lexical bridge tokens at all, and no relation-bearing word (`therefore`, `then`, `because`, `despite`, `but`, `however`) may ever be admitted. A bridge is licensed only by an upstream relation plus the frozen contract.

Two guards: **mechanical preservation** — after frozen normalisation of permitted capitalisation, whitespace and punctuation, each unit's text appears as a contiguous span in unit order; and a **semantic no-new-relation audit** — no causal, temporal, contrastive, conditional, attributive, certainty, negation or scope relation appears unless a unit contains it.
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
   -> problem candidates + claim candidates + salience inputs
   |
   v
S2 SEMANTIC ADJUDICATION
   -> adjudicated objects + adoption + approved claim representations
   |
   v
S3 CONTENT SELECTION & PROBLEM USE
   -> rendered-problem set + retained use map + dispositions + selected representations
   |
   v
S4 NOTE BLUEPRINT / UNIT COMPILATION  (owns final problem and unit order)
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
| S1 | Which neurologic subjects need their own assessment question? |
| S2 | What do the objects mean, and which claim formulations are defensible? |
| S3 | Which content is used, for which problem, with which approved claim? |
| S4 | Exactly what must render, where, how, and in what order? |
| R1 | How does one specified unit read? |
| R2 | How do specified prose units read together without semantic change? |
| R3 | How are completed sections assembled into the final note? |

---

# Freeze statement

ChatGPT and DeepSeek agree on all eleven submodules at the interface level, including their goals, inputs, outputs, and responsibility boundaries, with the two clarifications above for S4 standing-item units and R2 prose-only bounded composition.

The next design layer may define **function** inside each submodule, but must not change these interfaces without explicitly reopening the architecture.
