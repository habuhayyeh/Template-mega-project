# ChatGPT review 005 — module definitions and submodules

## Scope

Big-picture internal decomposition only. No field schemas, operator vocabulary, prompt wording, or implementation.

## Recommended tree

RUNTIME — one Doximity Ask call

1. INGEST
   1.1 Source Map
   1.2 Span Accounting
   1.3 Object Extraction
   1.4 Object Source-Annotation

2. STRUCTURE
   2.1 Clinical / Problem Model
   2.2 Object Adjudication
   2.3 View Projection
   2.4 Render-Unit Compilation

3. RENDER
   3.1 Unit Realization
   3.2 Section Composition
   3.3 Note Assembly

These are logical responsibility blocks, not separate prompts or model calls.

---

# 1. INGEST

## Parent outcome

Produce a high-recall, source-faithful substrate of stable semantic objects with enough source metadata for downstream STRUCTURE to work without reopening or re-summarizing the raw paste.

Governing question:

What was supplied, what did it say, and where did it come from?

## I1 — Source Map

Owns:
- recognizing source families;
- distinguishing transcript, current notes, prior notes, imaging, labs, etc.;
- preserving source order;
- source labels, date, service when available;
- transcript speaker labels when available.

Produces:
- source registry / source map.

Must not:
- synthesize sources;
- rank authority globally;
- decide note relevance;
- promote old diagnoses/plans into current ones.

## I2 — Span Accounting

Owns:
- mechanically bounded lines / utterances / speaker turns / pasted fragments;
- span IDs;
- source linkage;
- accounting for all received spans.

Produces:
- complete span map.

Boundary correction:
INGEST may call text nonclinical, unresolved, or object-bearing. It should not decide final NOT_RELEVANT_TO_NOTE or final omission. Relevance belongs in STRUCTURE after the encounter/problem model exists.

## I3 — Object Extraction

Owns:
- decomposition into independently useful clinical propositions;
- one stable object ID per proposition;
- source-faithful object text;
- coarse semantic family/kind if that taxonomy proves reliable.

Produces:
- stable object set.

Must not:
- create HPI/A-P copies of one fact;
- choose final problem or section;
- collapse near-duplicates for rendering;
- choose operators.

## I4 — Object Source-Annotation

Owns:
- source/span linkage;
- speaker/attribution;
- source date;
- source temporality;
- purely source-grounded attributes.

Adoption boundary:
INGEST may preserve an explicit current-clinician adoption statement as source content/evidence. STRUCTURE owns the final current-adoption decision used by the note.

In short:
INGEST records what was said.
STRUCTURE decides what the note adopts.

---

# 2. STRUCTURE

## Parent outcome

Convert the stable object substrate into the complete source-linked blueprint of the note: what the encounter is about, what each object is doing, where it is used, and exactly how it will be rendered.

Governing question:

What does this encounter mean, what belongs in the note, and how should the stable objects be used?

## S1 — Clinical / Problem Model

Owns:
- retained neurologic problems;
- current claim/formulation for each problem;
- problem hierarchy/order when needed;
- encounter-level adoption of historical diagnoses/reasoning/plans;
- whether non-neurologic issues materially belong because they affect neurologic care.

Produces:
- encounter problem model.

Must not:
- write problem-line prose;
- alter source objects;
- invent adoption.

## S2 — Object Adjudication

Owns:
- used vs explicitly omitted/dispositioned;
- problem use/reuse;
- reasoning role;
- duplicate/covered decisions;
- modifier relationships;
- condition relationships;
- final adoption decisions;
- standing-item trigger decisions when source criteria are met;
- explicit cross-problem reuse.

Produces:
- fully adjudicated object-use map.

Must not:
- write prose;
- clone a proposition solely for another use;
- infer relationships from medication/diagnosis heuristics.

## S3 — View Projection

Owns:
- Reason for consult;
- HPI;
- ROS;
- neurologic history;
- other PMH;
- medications;
- exam;
- workup;
- A/P;
- explicit cross-section reuse;
- section-specific use/omission.

Produces:
- note-view map using stable object IDs.

Must not:
- create new clinical content;
- destructively route an object;
- create separate per-section semantic ontologies.

This replaces the old destructive section-routing concept.

## S4 — Render-Unit Compilation

Owns:
- render-unit membership;
- rhetorical class;
- HEAD / MODIFIER / CONDITION / COVERED or equivalent roles;
- operator selection;
- unit order;
- section/problem ownership;
- fail-closed completeness of required payload.

Produces:
- completed Case IR / render specification.

Must not:
- write final prose;
- silently repair missing payload;
- add semantic claims.

This is the boundary supported by the B+ and stress-suite evidence.

---

# 3. RENDER

## Parent outcome

Express the completed Case IR as a readable clinical note without changing its semantic decisions.

Governing question:

How should the already-decided units be expressed?

## R1 — Unit Realization

Owns:
- canonical operator execution;
- local grammar;
- punctuation/capitalization;
- approved abbreviations;
- approved provenance display;
- approved number/time normalization;
- modifier/condition folding exactly as specified.

Produces:
- rendered unit text.

Must not:
- select/omit objects;
- decide equivalence;
- change operators;
- move content;
- invent missing payload.

## R2 — Section Composition

Owns:
- joining already-rendered, already-ordered units into readable section output;
- HPI/history sentence and paragraph assembly;
- section-specific voice;
- local pronouns/transitions where meaning is unchanged;
- bullet vs paragraph presentation.

Constraint:
This is not a semantic polish pass.

It may not:
- omit a unit;
- reorder units;
- create new causal/temporal relationships;
- reinterpret uncertainty;
- semantically merge two units.

Why needed:
A/P may map closely to one unit per bullet, but HPI/history need coherent narrative assembly. If this responsibility is not explicit, it will still occur invisibly inside the writer.

## R3 — Note Assembly

Owns:
- section headings/order;
- spacing/bullets;
- suppressing sections already marked empty by the IR;
- final note formatting.

Must not:
- decide relevance;
- move content across sections;
- perform a global rewrite/polish pass.

---

# 4. Do not create separate runtime submodules for

- allocation;
- deduplication;
- generic organize;
- A/P assembly;
- body-note assembly;
- reasoning extraction;
- problem-line writing;
- medication logic;
- standing items;
- final polish;
- self-audit.

These are either responsibilities already owned above, configuration/rule tables, or external engineering functions.

---

# 5. External engineering systems

CHECK:
- IR/schema/type conformance;
- unit-output alignment;
- uniqueness/reuse accounting;
- order/voice/allowed-transform checks;
- fail-only reporting.

AUDIT:
- source-span coverage;
- object/decomposition fidelity;
- problem/adoption/role correctness;
- render-unit/operator semantic appropriateness;
- no repair.

BUILD:
- module compilation;
- conflict/authority/scope lint;
- test-coverage lint;
- package versioning/manifest.

These are not patient-case runtime stages.

---

# 6. Two boundary changes relative to the current ingestion handoff

A. Final note relevance moves out of INGEST.
INGEST remains high-recall. Clinical material should not be labeled not relevant to the note before STRUCTURE knows the encounter/problem model.

B. Adoption evidence is distinct from the final adoption decision.
INGEST preserves explicit adoption language; STRUCTURE decides the final current-adoption state used by the note.

---

# 7. Questions for DeepSeek

Review at this same level only:

1. Do you agree with the 4 / 4 / 3 submodule tree?
2. Which submodule, if any, is unnecessary or combines cleanly with another?
3. Is View Projection genuinely separate from Object Adjudication, or should they be one responsibility?
4. Is Section Composition necessary inside RENDER to support HPI/history without becoming a semantic-polish stage?
5. Do you agree final relevance belongs in STRUCTURE, not INGEST?
6. Do you agree explicit adoption evidence may be preserved in INGEST but final adoption belongs to STRUCTURE?
7. Is any demonstrated failure still unowned by this tree?

No schema design or implementation yet.
