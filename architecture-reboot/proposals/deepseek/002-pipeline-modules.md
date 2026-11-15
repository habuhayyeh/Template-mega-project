# DeepSeek proposal 002 — the pipeline modules, in outline

Big-picture structure only. Not schemas, not operator lists.

**Three generative responsibilities, two external instruments, one build step.** The three run inside a single Ask call; only their contract boundaries are real.

---

## 1. The shape

```text
                    one Ask call
  ┌───────────────────────────────────────────────┐
  │  M1 INGEST → M2 PLAN → M3 RENDER               │
  └───────────────────────────────────────────────┘
        │            │            │
        │            │            └── note
        │            └── Case IR (test mode)
        └── spans

  after the call, outside Doximity:
  M4 CHECK   IR → note          mechanical
  M5 AUDIT   source → IR        semantic, human/oracle

  before deployment:
  M6 BUILD   modules → package  + conflict lint
```

Five runtime responsibilities, three of them generative, and every one has a single question it answers.

| Module | The one question | Input | Output |
|---|---|---|---|
| **M1 INGEST** | What did the source say, and where? | pasted source | spans + objects |
| **M2 PLAN** | What is the note about, and how is each fact to be rendered? | objects + spans | problems + units/operators |
| **M3 RENDER** | How does a unit read as a line? | units + style | note text |
| **M4 CHECK** | Does the note match the IR? | IR + note | pass/fail, disagreements |
| **M5 AUDIT** | Does the IR match the source? | spans + IR | defects, coverage gaps |
| **M6 BUILD** | Does the package contain contradictory rules? | source modules | deployment artifact |

## 2. What each is allowed and forbidden

**M1 INGEST.** Allowed: split into spans, create objects, assign kind, provenance, status, speaker, span pointer. Forbidden: deciding note sections, ordering, duplication, rendering, or what matters clinically. High recall — it may over-produce objects; it may not drop a span.

**M2 PLAN.** Allowed: group objects into problems, choose the claim, choose units, assign operators, decide duplicates, modifiers, conditions, order, bucket, adoption. Forbidden: writing note prose, inventing facts, changing object text, dropping a used object without a disposition. This is where every semantic decision lives, and it is the only module that makes them.

**M3 RENDER.** Allowed: capitalisation, punctuation, approved abbreviations, number/unit and time display, section-scoped voice, folding exactly what the unit names. Forbidden: selecting, merging, omitting, reordering, choosing an operator, adding a word outside the operator's fixed text.

**M4 CHECK.** Mechanical only: IR→note conformance, per-section-per-problem uniqueness, coverage, voice, order, operator validity. Forbidden: judging whether the IR is right, and repairing anything.

**M5 AUDIT.** Semantic: source→IR fidelity, coverage gaps, operator selection. Forbidden: repairing anything, and acting as a gate inside production. It is a review instrument.

**M6 BUILD.** Mechanical: compile modules, lint for contradictory rules, duplicate authority over one decision, out-of-scope rules, untested rules. Forbidden: adding behaviour.

## 3. Why six and not more

Each of the six answers a question the others cannot:

- M1 cannot decide relevance without becoming M2.
- M2 cannot render without becoming M3.
- M3 cannot be trusted to check itself — hence M4.
- M4 cannot see the source — hence M5.
- M6 exists because the last system failed through accumulated contradictory clauses in one compiled file, not through module count.

There is no separate allocation module, no separate organisation module, no per-section pipeline, no "assemble" stage. Those existed because meaning was being re-derived at each step; with units in the IR there is nothing left for them to decide.

## 4. What this deliberately does not do

- **No stage numbering that implies a runtime sequence.** M1–M3 are one call. The numbering is a contract order, not three prompts.
- **No per-section modules.** Section differences are a style table and an operator set, not four pipelines. If a section later needs different semantics, that is evidence for a module, and we do not have it.
- **No "validation layer" inside the model.** M3 may not self-check as a substitute for M4.
- **No second model pass in production.** Two-pass is a manual option, not the architecture.

## 5. The open question this leaves

Where the boundary between M1 and M2 falls when a single model performs both. Ingest can plausibly produce a unit-bearing IR directly, which would collapse M1 and M2 into one responsibility with two named halves.

That is not a defect; it is a sizing question. My position: keep them named separately even if one call executes both, because the audit checks them separately — span coverage belongs to M1, unit correctness to M2 — and a boundary you cannot audit separately is a boundary you do not have.
