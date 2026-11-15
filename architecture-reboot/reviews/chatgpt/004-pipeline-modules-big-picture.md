# ChatGPT review 004 — pipeline modules at big-picture level

## Verdict

**ACCEPT the three-module runtime architecture, with one naming/boundary clarification.**

DeepSeek's proposal correctly separates:

### Runtime / patient-case pipeline
1. **INGEST**
2. **PLAN / STRUCTURE**
3. **RENDER**

from:

### Engineering support systems
4. **CHECK**
5. **AUDIT**
6. **BUILD**

This distinction should be explicit because the signer asked for the overall pipeline shape, not every engineering instrument.

The production note-generation pipeline therefore has **three logical steps inside one Ask call**.

CHECK, AUDIT, and BUILD are not additional per-patient runtime stages.

---

## 1. Runtime Step 1 — INGEST

### Question
> What did the supplied material say, and where did it come from?

### Owns
- source-family recognition;
- source boundaries / spans;
- atomic clinical objects;
- provenance / speaker;
- source temporality;
- explicit source-level attributes;
- high-recall capture.

### Must not own
- final note relevance;
- problem organization;
- duplicate collapse for rendering;
- section placement;
- render-unit composition;
- final wording.

### Output
A source-faithful object substrate.

This is essentially:
> **source -> stable semantic objects**

---

## 2. Runtime Step 2 — STRUCTURE

I prefer the user-facing architectural name **STRUCTURE** (or NOTE PLAN) rather than just `PLAN`, because `PLAN` is overloaded clinically and may be confused with the Plan portion of the A/P.

### Question
> What does the note mean, what belongs where, and how should the stable objects be used?

### Owns
All encounter-level semantic adjudication needed before prose:
- neurologic problems;
- reasoning roles;
- current adoption when it requires encounter-level interpretation;
- relevance / disposition;
- section use;
- cross-problem reuse;
- duplicate coverage;
- modifiers / conditions;
- render units;
- operator selection;
- ordering.

### Must not own
- prose writing;
- alteration of source object content;
- invention of facts.

### Output
The completed **Case IR**:
- stable objects from INGEST;
- problem structure;
- explicit render units/operators.

This is the single hard semantic planning module.

---

## 3. Runtime Step 3 — RENDER

### Question
> Given a complete Case IR, how should each unit be expressed as the final note?

### Owns
- canonical operator execution;
- local grammar;
- punctuation/capitalization;
- approved abbreviations;
- approved folding;
- section-specific style/voice.

### Must not own
- relevance;
- object selection;
- problem membership;
- duplicate decisions;
- operator choice;
- reordering;
- semantic repair.

### Output
The final note.

This is:
> **Case IR -> note**

The Doximity operator experiments provide direct evidence that this boundary can be highly reliable when the Case IR is already explicit.

---

# 4. External engineering systems

These should not be presented as patient-case pipeline steps.

## CHECK
Mechanical:
> Does the final note obey the emitted Case IR?

Used in test/engineering workflows when the IR is available.

## AUDIT
Semantic:
> Does the Case IR faithfully represent the source?

Human/oracle/model-assisted engineering review.

## BUILD
Deployment:
> Are the modular source contracts internally consistent, and can they compile into the small Doximity package?

Includes conflict lint.

These three support the runtime architecture but do not add cognitive stages to the Doximity note-generation call.

---

# 5. One boundary clarification: INGEST vs STRUCTURE

DeepSeek's outline puts `adoption` entirely in M2, while the ingestion handoff allows INGEST to preserve current adoption **when explicit**.

I think the clean boundary is:

### INGEST
May capture **explicit source statements** without inference.

Example:
> current clinician: "I agree this is vascular dementia."

INGEST can preserve that explicit adoption signal as source content.

### STRUCTURE
Owns the **final encounter-level adoption decision** used by the note.

That distinction prevents M1 from becoming clinically interpretive while still preserving explicit source meaning.

The same principle applies generally:

> INGEST preserves what the source explicitly says.  
> STRUCTURE decides how the current note uses it.

---

# 6. Should INGEST and STRUCTURE collapse into one module?

**No at the architectural level.**

They may be executed by the same Doximity model in one call, but they should remain separate logical modules because their failure modes differ:

- INGEST failure = source loss / bad decomposition / bad provenance.
- STRUCTURE failure = wrong relevance / ownership / grouping / operator selection.

E1 needs to measure these separately.

So the runtime architecture should remain:

```text
INGEST -> STRUCTURE -> RENDER
```

inside one Ask call.

Not because Doximity literally performs three prompts, but because these are three distinct responsibilities with separate acceptance criteria.

---

# 7. No additional runtime modules yet

I agree with DeepSeek that we should **not** currently add:

- ALLOCATE;
- ORGANIZE;
- ASSEMBLE;
- separate A/P pipeline;
- separate body pipeline;
- per-section semantic planners;
- self-audit stage inside the model.

Those are not justified by current evidence and risk recreating the old pipeline.

If future experiments demonstrate a specific independent failure mode that cannot be isolated inside one of the three modules, then a new module can earn its existence.

---

# 8. Proposed big-picture structure for signer review

```text
                    ONE DOXIMITY ASK CALL

RAW CHART + TRANSCRIPT
          |
          v
+---------------------+
| 1. INGEST           |
| source -> objects   |
+---------------------+
          |
          v
+---------------------+
| 2. STRUCTURE        |
| objects -> Case IR  |
+---------------------+
          |
          v
+---------------------+
| 3. RENDER           |
| Case IR -> note     |
+---------------------+
          |
          v
      FINAL NOTE
```

Engineering around it:

```text
SOURCE -> IR      : AUDIT
IR -> NOTE        : CHECK
MODULES -> PACKAGE: BUILD
```

My recommendation is to freeze **this level** before discussing detailed schemas or operator lists.

The next design discussion should ask only:
- Are three runtime logical modules the correct granularity?
- Is STRUCTURE the correct responsibility boundary?
- Do we need any fourth runtime responsibility based on demonstrated evidence?

No implementation yet.
