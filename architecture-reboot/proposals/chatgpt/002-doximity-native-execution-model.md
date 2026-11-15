# ChatGPT Proposal 002 — Doximity-Native Execution Model and Module Boundaries

**Status:** research-informed architecture proposal for critique. Not implementation.
**Date:** 2026-11-15
**Purpose:** adapt the clean-room architecture to the actual Doximity product surfaces and to the runtime failures already observed in this repository.

---

# 1. Core conclusion

We should not design "for Doximity" as though Doximity were one generic prompt box.

Public Doximity documentation describes three materially different AI surfaces:

1. **Scribe** — transcript-to-note generation using a selected/custom note template and optional pre-chart note.
2. **Ask** — general HIPAA-compliant assistant with uploaded documents, saved prompts, and conversational interaction.
3. **Ask Evidence / Refine With Ask inside Scribe** — post-generation copilot that can see both the generated note and the full session transcript and can make targeted edits.

These surfaces should have different jobs.

The architecture should exploit what each surface natively exposes instead of forcing a long simulated pipeline through one generative call.

---

# 2. Verified public behavior

## Scribe

Doximity publicly states that:

- Scribe converts encounter audio/transcript into H&P, progress, consult, or custom-template notes.
- A **pre-chart note** can be supplied before the visit.
- **Custom note templates** can be created and reused.
- Scribe uses **GPT-4o** for note summarization.
- A Scribe session can run up to **140 minutes**.
- The generated transcript and note are retained for 29 days; audio is destroyed after transcription.
- Scribe is intentionally a summarizer: it filters ordinary chatter and selects clinically important material.

Official references:
- https://support.doximity.com/hc/en-us/articles/55409797170451-How-To-Use-Doximity-Scribe
- https://support.doximity.com/hc/en-us/articles/55385851431187-Getting-Started-with-Doximity-Scribe
- https://support.doximity.com/hc/en-us/articles/55386093900435-Troubleshooting-Privacy

## Ask

Doximity publicly states that:

- Ask accepts uploaded documents as context.
- prompts can be saved;
- Ask is conversational;
- Doximity warns that some **multi-turn or nuanced questions may not be handled perfectly**.

Official reference:
- https://support.doximity.com/hc/en-us/articles/55381817186195-Doximity-Ask-FAQs

## Ask Evidence / Scribe Ask

Doximity publicly states that:

- it can access the **generated note and original/full transcript**;
- it can retrieve information discussed in the visit even when omitted from the original note;
- it can perform targeted edits;
- Doximity explicitly recommends **specific, targeted instructions rather than broad rewrites**;
- edits are previewed and accepted/rejected by the clinician.

Official references:
- https://support.doximity.com/hc/en-us/articles/55386058959891-Ask-Evidence
- https://support.doximity.com/hc/en-us/articles/55409733477523-How-to-Use-Doximity-Ask-With-Scribe-Notes

---

# 3. What is NOT publicly exposed

I found no public Doximity documentation exposing:

- a deterministic seed;
- temperature or sampling controls;
- token/context limits for Scribe templates or Ask attachments;
- a stage-by-stage internal execution trace;
- tool-call traces;
- hidden chain-of-thought;
- an API for inserting a persistent intermediate semantic state between Scribe generation steps;
- guarantees that multiple uploaded instruction files are read in a deterministic priority order.

Therefore we should not design any safety-critical behavior around those assumptions.

A Doximity-generated "diagnostic explanation" can describe observable behavior, but it should not be treated as a causal trace of the model's hidden computation.

---

# 4. What our own Doximity runs add

The repository demonstrates several platform-relevant behaviors.

## Strong findings

### 4.1 Explicit absence is strong

When O54 was removed upstream from the Handoff, it stayed absent in all clean set-3 outputs.

This is stronger than telling the final writer to remember an exclusion.

### 4.2 Closed, explicit inputs can be stable

Once STANDING_ITEMS was actually included in the package, the required seizure precaution appeared consistently.

### 4.3 Semantic equivalence is not stable enough to rediscover at render time

Clean set 3 varied on:

- two infarct descriptions -> one vs two lines;
- two CT descriptions -> one vs two lines;
- two MRI adjudication phrases -> one vs two;
- apixaban hold + conditional resume -> split vs composed.

### 4.4 Output schema is not absolute

The 06 runs show that a schema can be followed twice and then broken on another identical run.

### 4.5 Prompt edits are non-local

Changing a rule for one object changed treatment of a different object in later 06 testing.

## Design implication

Doximity can follow substantial global instructions, but it is a poor place to repeatedly perform **boundary-sensitive semantic adjudication** whose answer must remain identical across runs.

---

# 5. Revised mental model of the platform

I propose that we model Doximity as:

> **A strong holistic summarizer and local editor, but a weak deterministic workflow engine.**

That means:

### Good jobs for Doximity

- interpret natural clinical conversation;
- capture encounter facts from transcript;
- produce fluent HPI/history prose;
- render already-decided problem structures;
- perform local grammar/style transformations;
- use a custom note template;
- retrieve omitted transcript details after generation;
- perform narrow, targeted corrections.

### Poor jobs for Doximity when reproducibility matters

- repeatedly canonicalize semantically overlapping source facts;
- decide current-vs-historical management late;
- infer management target from medication knowledge;
- choose problem ownership in several different stages;
- enforce large schemas with many conditional branches;
- act as a hidden multi-module orchestrator;
- explain its own hidden runtime causally;
- make the same semantic decision independently in several note sections.

---

# 6. Important architecture change: development modules are not runtime stages

The clean-room proposal should distinguish:

## A. Source modules in GitHub

Human-readable, independently reviewable components:

```
modules/
  00-source-policy.md
  10-case-model.md
  20-problem-model.md
  30-hpi-view.md
  31-history-view.md
  32-workup-view.md
  40-ap-view.md
  50-style.md
  60-safety.md
  70-diagnostics.md
```

These are **design/source-code modules**.

## B. Doximity deployment artifacts

These should be deliberately few.

Likely target:

```
DIST/
  SCRIBE_TEMPLATE.txt
  PRECHART_CONTRACT.txt
  ASK_AUDIT_PROMPT.txt
```

or, if the user is operating in Ask rather than Scribe:

```
DIST/
  ENGINE.md
  STYLE.md
  CASE_INPUT.*
```

The build should compile source modules into the fewest useful runtime artifacts.

**More files in Doximity are not automatically more modular.**

The module boundary that matters is semantic responsibility, not attachment count.

---

# 7. Doximity-native execution topology

I now prefer this as the primary production topology:

```
                  PRIOR RECORD / PRE-CHART
                           |
                           v
LIVE ENCOUNTER ---> DOXIMITY SCRIBE
                           |
               Custom Neurology Template
                           |
                           v
                    INITIAL NOTE
                           |
                           v
                   HUMAN REVIEW
                           |
             +-------------+-------------+
             |                           |
          accept                     targeted issue
                                         |
                                         v
                                  ASK EVIDENCE
                           (note + full transcript)
                                         |
                                         v
                                  TARGETED PATCH
```

This fits the product rather than pretending Scribe is a programmable pipeline.

---

# 8. What happens to the Persistent Case State idea?

The semantic-state idea remains useful, but we should distinguish **conceptual architecture** from **deployable artifact**.

There are three possible versions.

## Version 1 — external persistent state

A real structured state exists outside Doximity and is fed to renderers.

This is strongest technically but requires an external controller/workflow that may not be available in the user's clinical environment.

## Version 2 — visible same-call render plan

Doximity first emits a compact semantic/view plan and then renders the note in the same response.

Because generated earlier text is available to later generation in the same completion, this creates an observable intermediate artifact.

Advantages:
- auditable;
- may reduce repeated semantic choice.

Disadvantages:
- pollutes production output;
- still model-generated and stochastic;
- Scribe's normal note UI may not support clean separation of plan from note.

## Version 3 — implicit single-pass case model

The custom template contains modular semantic rules, but the state is conceptual and not separately emitted.

Advantages:
- simplest production workflow;
- fits Scribe natively.

Disadvantages:
- less observable;
- harder to localize semantic planner errors.

### Current recommendation

Use **Version 3 for production** and **Version 2 in test mode**.

Do not require an unavailable external state engine unless experiments prove the Scribe-native design is insufficient.

---

# 9. Module plan optimized for Doximity

I would reduce the runtime design to six responsibilities.

## Module 1 — Source / provenance policy

Purpose:
- define what information may enter the note;
- distinguish transcript, clinician statements, patient/family report, and prior-record/pre-chart content;
- forbid invention;
- establish source priority where sources conflict.

This module should be short and global.

### Why

Doximity already has the transcript. We should not waste prompt budget recreating a source ingestion engine unless needed.

---

## Module 2 — Case normalization policy

Purpose:
- interpret facts once for the current generation;
- distinguish:
  - current encounter vs historical;
  - clinical event time vs documentation date;
  - fact vs clinician reasoning vs management;
  - same proposition vs distinct proposition;
  - condition/modifier relationships.

This is the most important semantic module.

### Key constraint

It should define a **small relation vocabulary**, not dozens of object types.

The old six-kind ontology should be re-justified rather than inherited.

---

## Module 3 — Neurologic problem model

Purpose:
- create active neurologic problem/claim nodes;
- attach relevant evidence, reasoning, course, and management;
- permit non-neurologic material only when it changes/supports/refutes/contextualizes neurologic care.

This encodes the user's real clinical mental model.

The problem model should be formed once and reused by HPI/history/A&P views rather than independently rediscovered.

---

## Module 4 — Section view rules

Purpose:
- specify what each note section wants from the case model.

Examples:

### HPI
- presentation chronology;
- symptoms/triggers/risk factors/important negatives;
- no diagnostic synthesis ending.

### Neuro history
- neurologically relevant prior conditions and baseline deficits.

### Workup
- results only, not planned tests.

### A/P
- problem-centered claim -> decisive evidence -> clinician reasoning/uncertainty -> plan;
- impersonal clinical voice;
- explicit current management only;
- no late semantic deduplication.

One semantic state, multiple views.

---

## Module 5 — Surface/style renderer

Purpose:
- abbreviations;
- sentence/bullet style;
- temporal phrasing;
- impersonal A/P voice;
- local grammar.

This module must not make clinical decisions.

---

## Module 6 — Audit / test mode

Purpose:
produce an observable contract-action ledger.

Example:

```
P1 seizure
F1 <- transcript seizure + ED seizure | SAME_FACT | rendered A/P fact 1
F2 <- CT no hemorrhage + CT no acute abnormality | CANONICALIZED | rendered workup 2
M1 <- apixaban held + resume if MRI... | COMPOSED | plan 3
```

The ledger should describe **declared transformations and source mappings**, not hidden reasoning.

Production mode omits it.

---

# 10. How to use each Doximity surface

## Scribe = primary generator

Use for:
- transcript intake;
- pre-chart context;
- one holistic note generation;
- custom note structure.

Do not ask Scribe to execute a visible 7-stage pipeline.

## Ask = architecture/development sandbox or document-based processor

Use for:
- testing instruction modules with uploaded synthetic cases;
- comparing alternative module designs;
- generating structured semantic ledgers from controlled inputs;
- saved prompts for repeatable experiments.

Do not assume attachment order alone creates deterministic precedence.

## Ask Evidence = targeted post-generation repair/audit

Use for:
- "add the medication side effect discussed in the visit";
- "move X to the A/P";
- "check whether this bullet is supported by the transcript";
- "identify transcript details omitted from the HPI";
- one narrow correction at a time.

This matches Doximity's own recommendation for targeted instructions.

Avoid using Ask Evidence for repeated broad whole-note rewrites, because every broad rewrite creates another opportunity for semantic drift.

---

# 11. Diagnostics: what we can and cannot learn

## We cannot obtain a true hidden execution trace

Doximity does not expose one publicly.

## We can create useful observable diagnostics

### A. Pre/post semantic ledger in test mode

Ask the system to report:
- source IDs/spans used;
- same-fact groups;
- problem assignment;
- current/historical status;
- action-condition pairs;
- rendered section/line.

### B. Independent transcript audit with Ask Evidence

Because Ask Evidence has the full transcript, test prompts such as:

- "For every A/P bullet, identify the transcript or pre-chart support."
- "List transcript facts clinically relevant to P1 that are absent from the note."
- "List note statements that cannot be matched to the transcript/pre-chart."

This is not proof of how the note was generated. It is a useful **post-hoc retrieval audit**.

### C. Repeat-run comparison

Three or more fresh identical runs remain necessary for decisions where semantic stability matters.

---

# 12. The most important deployment experiments

Before hardening the module architecture, run small experiments against the actual product.

## Experiment 1 — file count / packaging

Same synthetic task, same total text:

- A: one compiled ENGINE file;
- B: three files (ENGINE, STYLE, CASE);
- C: many small modules.

Measure:
- contract compliance;
- semantic reproducibility;
- omissions;
- latency.

This tells us whether attachment fragmentation itself hurts performance.

## Experiment 2 — Scribe native vs Ask attachment workflow

Same synthetic encounter content:

- A: custom Scribe template + pre-chart note;
- B: Doximity Ask with uploaded engine + synthetic transcript.

Measure:
- section fidelity;
- clinical omissions;
- duplicate handling;
- reproducibility.

This tells us whether we should optimize primarily for Scribe or Ask.

## Experiment 3 — hidden vs visible plan

Same input:

- A: final note only;
- B: output compact semantic ledger first, then final note.

Measure whether visible planning improves:
- duplicate collapse;
- action-condition composition;
- stable problem ownership.

If not, discard visible planning.

## Experiment 4 — broad rewrite vs targeted Ask Evidence

Generate one flawed note, then:

- A: "rewrite note to fix all issues";
- B: four narrow edits, one defect at a time.

Compare collateral changes.

Prediction: targeted edits will be more stable, consistent with Doximity's documented guidance.

## Experiment 5 — native pre-chart provenance

Put prior-record facts in the pre-chart note with clear source/date labels.

Test whether Scribe reliably distinguishes:
- event date;
- documentation date;
- current vs historical management.

This directly tests whether a separate provenance ontology is necessary.

---

# 13. Architecture implications for the clean-room proposal

I would modify Proposal 001 in one important way.

Originally:

> persistent semantic case model -> view plans -> renderers

I now think the **logical** architecture is correct, but the **Doximity deployment** should not necessarily instantiate each box as a separate call or file.

The better abstraction is:

```
SOURCE MODULES (GitHub)
        |
        v
COMPILE
        |
        v
DOXIMITY-OPTIMIZED RUNTIME CONTRACT
        |
        +--> semantic normalization policy
        +--> problem model
        +--> section views
        +--> style
        |
        v
SINGLE HOLISTIC SCRIBE GENERATION
        |
        v
TARGETED ASK-EVIDENCE REPAIR IF NEEDED
```

Thus:

> **modular source, compiled runtime, single semantic adjudication point, thin render views.**

That may be the best compromise between sound architecture and the actual platform.

---

# 14. Current recommendation

Do not break the Doximity deployment into more and more files.

Instead:

1. make GitHub highly modular;
2. compile modules into one/few runtime artifacts;
3. use Scribe's native transcript + pre-chart + custom template as the production context;
4. make one semantic normalization/problem-model decision per generation;
5. let section renderers be views, not independent reinterpreters;
6. reserve Ask Evidence for narrow post-generation corrections and transcript audits;
7. use visible ledgers only in test mode;
8. empirically test file count, visible planning, and Scribe-vs-Ask topology before finalizing the architecture.

The key optimization target is not "more modular Doximity prompts."

It is:

> **fewer independent semantic decisions inside Doximity, while keeping the source architecture modular outside it.**
