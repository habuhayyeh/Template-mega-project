# Brief for an expert note writer — map the ingestion-to-note architecture

Use this prompt with a senior neurology note writer who does not know Doximity or our repository. Attach
2–3 de-identified Scribe packets, the final note template, and 2–3 examples of notes you consider good.

---

You are a senior neurology note writer and clinical information architect. You do not need to know
Doximity. I need you to help design the **map from a source packet to a final note**, not write prompt
text.

## Context

Production is:

```text
Doximity Scribe -> source-faithful evidence packet -> Doximity Ask (GPT-4o, no code execution) -> note
```

The Scribe packet is canonical. It keeps source blocks, stable record IDs, speaker/source labels,
source order, dates and provenance. Example:

```text
@@PACKET SCRIBE_EVIDENCE_V2_2
@@SOURCE T TRANSCRIPT CURRENT
T001 :: SPK2 :: Three falls since June.
T002 :: SPK1 :: She also had a spell on Wednesday.
@@SOURCE P1 ED NOTE 2026-11-14
P1.001 :: SEC=HPI :: VIA=EMS report :: Patient reports three falls.
P1.002 :: SEC=PMH :: Prior left MCA stroke in 2022.
@@END
```

Downstream functions may dereference any `T###` or `P1.###` record. They must not invent source content.

## What we tried and why it failed

1. **Global atomic facts.** One record became many fact objects. The output expanded to ~175 objects and
   truncated before the packet was complete.
2. **Compact synthesized facts + semantic validator.** F1 wrote short `fact:` prose; F1V checked it with
   the same model. F1V emitted a full verification ledger and still passed question-only references,
   wrong local support and action-state upgrades. It was a second editor, not an independent validator.
3. **Pointer-only topic index.** It removed the claim layer, but GPT-4o produced coarse source-wide
   buckets. It did not reduce the reading the next semantic pass had to do.

Conclusion: do not create a second fact corpus, do not copy source text into intermediate stages, and do
not use a same-model audit as proof.

## Current candidate

```text
Scribe packet
  -> A. semantic reconciliation + action state
  -> B. problem architecture
  -> C. note compiler
  -> D. renderer
```

Possibly split action state into its own pass. No separate fact-extraction pass. No topic index. No
validator pass. No prose until C/D.

We want your clinical judgment on whether this is the right map, and what the handoffs should contain.

## Your task

### 1. Critique the candidate

- Is the order right?
- Is a pass missing?
- Is a pass unnecessary?
- Should action state be separate?
- Should reconciliation and problem architecture be one pass or two?
- Where would a good note writer naturally make each decision?

### 2. Produce the map

Give a one-page dependency map of the clinical decisions and handoffs, not a software diagram.

For each pass, state:

- purpose;
- input;
- output;
- what it owns;
- what it must not decide;
- the main failure modes;
- what the next pass must be able to recover.

### 3. Define the handoff schemas

Use plain text that GPT-4o can follow and a human can audit. Prefer pointers to source record IDs over
copied text. For each handoff, show:

- required fields;
- optional fields;
- stable IDs;
- how to cite source records;
- how to represent uncertainty, negation, conflict and action state;
- what must never appear in that handoff.

Do not design a new ontology unless a clinical distinction cannot be represented otherwise.

### 4. Map the note

Using the attached template/examples, show where each kind of content goes:

- reason for consult;
- HPI timeline;
- neurologic history;
- other PMH;
- medications;
- exam;
- workup;
- A/P per problem;
- anything else the template requires.

For each section, state what the compiler needs from the problem model and what the renderer may add
without inventing clinical content.

### 5. Give test cases

List 10–15 high-value cases or edge cases that the map must handle. Include:

- historical disease with a current new symptom;
- residual deficit vs new worsening;
- two events close in time;
- patient report vs collateral report vs objective finding;
- a provisional A/P label in a current note;
- conflicting sources;
- recommended vs ordered vs administered vs completed action;
- test performed vs result available;
- an independent disorder vs a contained manifestation;
- a multifactorial syndrome;
- an important negative or counterevidence;
- a medication change with unclear adherence;
- a patient with multiple neurologic and non-neurologic problems.

For each, state what must not be lost.

### 6. Challenge the constraints

Tell us where these rules are clinically wrong or too rigid:

- no atomic fact corpus;
- no copied source text in handoffs;
- no same-model audit;
- no prose until the structure is stable;
- source record IDs as the only evidence pointers;
- one Ask call with several logical passes.

### 7. Recommend the final map

End with:

- the minimum pass set;
- what each pass owns in one sentence;
- the handoff artifact for each pass;
- what you would delete or merge;
- the three highest-risk failure points;
- the first test you would run.

## Constraints

- Preserve source fidelity and provenance.
- Preserve current vs historical, disease identity vs current status, patient report vs objective
  finding, diagnosis vs evidence, problem vs manifestation, contained manifestation vs distinct
  disorder, PRIMARY vs BACKGROUND, certainty, action decision vs execution, test performed vs result
  available, attribution and counterevidence.
- Do not write the final note prompts yet. Design the map first.
- Do not assume the model can execute code or reliably validate itself.
- Do not invent patient content. Use the attached packets and exact record IDs.

## Deliverable

Return:

1. one-page map;
2. pass table;
3. handoff schemas with examples;
4. note-section map;
5. test cases;
6. critique and risks;
7. recommended final map.

Keep it concrete. We need a map we can build from, not a general essay.
