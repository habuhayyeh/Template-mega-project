# ChatGPT proposal 007 — function-control allocation by submodule

## Status

Proposal for the next design layer.

The submodule interfaces are frozen. This document asks how each submodule should perform its agreed function using three control modes:

1. **LLM semantic capability** — interpretation, clinical judgment, decomposition, fluent language.
2. **Specific prose contract** — purpose, boundaries, clinical policy, allowed/forbidden decisions.
3. **Pseudocode / typed DSL / canonical operators** — explicit accounting, branching, schemas, unit composition, order, fail-closed behavior.

This is not a choice of one mode per submodule. Most submodules need a hybrid.

---

# 1. Core design principle

Use the **least rigid control that reliably fixes the decision**.

### LLM capability is best for
- semantic interpretation;
- recognizing clinical propositions;
- clinical problem formulation;
- context-sensitive relevance;
- determining meaning when the answer cannot be reduced to a closed rule;
- natural prose composition within a fixed semantic envelope.

### Specific prose instructions are best for
- defining the goal of a submodule;
- specifying clinical/documentation policy;
- ownership boundaries;
- source-fidelity rules;
- telling the model what it may and may not infer;
- describing nuanced judgment that cannot be represented cleanly as pseudocode.

### Pseudocode / typed DSL is best for
- complete accounting;
- iteration over all objects/spans/units;
- explicit roles;
- closed vocabularies;
- ordering;
- composition rules;
- completeness checks;
- fail-closed behavior;
- canonical operator execution.

The Doximity gradient supports this division:
- ordinary prose left semantic/structural drift;
- explicit DSL stabilized semantic structure;
- typed groups + canonical operators produced stable text in the B+ and stress tests.

Therefore pseudocode should be concentrated where the model would otherwise rediscover **merge/split, grouping, order, conditional scope, coverage, or wording architecture**.

---

# 2. Prompt architecture for every submodule

Each submodule should be written in three layers when needed:

## Layer A — semantic objective
Short natural-language statement of what the model is trying to accomplish.

## Layer B — prose contract
Precise clinical/documentation rules and forbidden decisions.

## Layer C — execution contract
Pseudocode / DSL only for parts that are:
- enumerable;
- testable;
- reproducibility-critical.

Do not encode open-ended clinical reasoning as fake pseudocode.

---

# 3. Recommended allocation by submodule

Scale:
- **HIGH** = central control mechanism;
- **MEDIUM** = important supporting role;
- **LOW** = minimal use;
- **NONE** = should not be relied on.

| Submodule | LLM semantic capability | Specific prose | Pseudocode / DSL |
|---|---:|---:|---:|
| I1 Source Map | MEDIUM | HIGH | MEDIUM |
| I2 Span Registry | LOW | MEDIUM | HIGH |
| I3 Object Extraction | HIGH | HIGH | LOW-MEDIUM |
| I4 Source Annotation | MEDIUM | MEDIUM | HIGH |
| S1 Problem Model | VERY HIGH | HIGH | LOW |
| S2 Semantic Adjudication | HIGH | VERY HIGH | MEDIUM |
| S3 Content Selection & Problem Use | HIGH | HIGH | HIGH |
| S4 Note Blueprint / Unit Compilation | MEDIUM | MEDIUM | VERY HIGH |
| R1 Unit Realization | LOW | MEDIUM | VERY HIGH |
| R2 Section Composition | HIGH language ability | VERY HIGH boundary contract | MEDIUM |
| R3 Note Assembly | LOW | LOW-MEDIUM | VERY HIGH |

These are architectural proportions, not literal token percentages.

---

# 4. INGEST functions

## I1 — Source Map

### Semantic capability
Use the model to recognize source families from natural pasted material:
- transcript;
- neurology note;
- ED/H&P;
- imaging;
- labs;
- medication list.

### Prose
Strong instructions:
- preserve source boundaries;
- do not synthesize sources;
- preserve internal order;
- do not infer authority globally.

### Pseudocode
Use a small accounting shell:

```text
FOR each bounded source block:
    assign SOURCE_ID
    classify SOURCE_TYPE from closed list if possible
    copy available date/service/speaker metadata
    preserve original order
IF source type cannot be determined:
    SOURCE_TYPE=UNKNOWN
DO NOT merge source blocks
```

Why not more pseudocode:
source recognition from messy human text is semantic.

---

## I2 — Span Registry

This should be one of the most pseudocode-heavy ingest submodules.

```text
FOR each SOURCE in source order:
    segment only on approved mechanical boundaries
    FOR each fragment:
        create exactly one SPAN_ID
        link SPAN -> SOURCE
CHECK:
    no received source text is outside a span
```

LLM interpretation should be minimal. It should not semantically split one sentence into propositions here.

---

## I3 — Object Extraction

This should remain LLM-heavy.

The task is semantic decomposition, and over-formal pseudocode risks distorting the source.

### Prose core
- extract independently useful propositions;
- preserve attribution/certainty/negation;
- do not summarize several propositions into one;
- do not create note-specific copies;
- high recall.

### Light pseudocode shell
Useful only for coverage:

```text
FOR each SPAN:
    identify 0..N independently useful clinical propositions
    create one OBJECT per proposition
    link every OBJECT to the SPAN
    if no clinical proposition:
        record non-object span disposition
```

Do not pseudocode rules for deciding what counts as an independently useful proposition beyond examples and prose criteria.

---

## I4 — Source Annotation

Mixed but relatively structured.

Use prose to define:
- source temporality vs event time;
- attribution;
- explicit adoption statement vs final adoption.

Use pseudocode for exact copying/accounting:

```text
FOR each OBJECT:
    source_id := linked source
    span_id := linked span
    speaker := explicit speaker else UNKNOWN
    source_date := exact available date else UNKNOWN
    source_temporality := derived from source class only
DO NOT infer current_adoption
```

---

# 5. STRUCTURE functions

## S1 — Problem Model

This is the most LLM-semantic submodule.

Do **not** attempt to turn neurologic problem formulation into detailed pseudocode.

### LLM
Use clinical reasoning to identify:
- neurologically meaningful problems/claims;
- appropriate granularity;
- whether uncertainty itself is the claim;
- whether a chronic neurologic issue deserves a separate problem.

### Prose
Very important:
- neurologic claims are the organizing unit;
- non-neurologic data become separate problems only when materially relevant;
- prior diagnoses remain attributed unless adopted;
- no invented problem from medication class.

### Pseudocode
Only an accounting skeleton:

```text
produce ordered PROBLEM set
each retained neurologic claim -> exactly one problem node
do not create problem solely from a medication or isolated historical label
```

The clinical judgment stays generative.

---

## S2 — Semantic Adjudication

Hybrid.

The model must reason semantically about:
- duplicate vs related;
- modifier vs independent fact;
- condition;
- claim/etiology/uncertainty/adjudication role;
- current adoption.

Prose defines those concepts and clinical boundaries.

Pseudocode should enforce a **closed relationship vocabulary and accounting**, not decide the relationship:

```text
FOR each candidate semantic relation:
    choose only from approved relation/role set
    cite object ids/source evidence
    do not silently rewrite object text
IF relation cannot be justified:
    leave unresolved rather than infer
```

This is where fake determinism would be dangerous.

---

## S3 — Content Selection & Problem Use

Semantic selection is LLM-heavy, but accounting must be pseudocode-heavy.

### LLM/prose
Decide:
- whether an object is useful in the note;
- which problem(s) it serves;
- whether reuse is warranted;
- whether omission is clinically appropriate.

### Pseudocode shell
Critical:

```text
FOR every clinical OBJECT:
    assign >=1 PROBLEM_USE
    OR assign explicit DISPOSITION

FOR each PROBLEM_USE:
    preserve same OBJECT_ID

DO NOT clone object solely for reuse
DO NOT leave object unaccounted
```

This is a good example of **semantic decision inside deterministic accounting**.

---

## S4 — Note Blueprint / Render-Unit Compilation

This should be the most pseudocode/DSL-heavy semantic submodule.

The hard semantic choices have already been made upstream.

### Prose
Only enough to define:
- section contracts;
- operator-selection intent;
- standing-item policy;
- section-specific expectations.

### Pseudocode / typed DSL
Very strong:

```text
FOR each retained OBJECT_USE:
    assign SECTION
    assign UNIT
    assign ROLE within unit
    assign RHETORICAL_CLASS
    assign OPERATOR from closed vocabulary
    assign ORDER

VALIDATE unit required fields
VALIDATE section/problem/object uniqueness
VALIDATE current plan item -> plan unit
VALIDATE surviving reasoning -> reasoning unit
VALIDATE every required problem claim -> claim unit
FAIL CLOSED on malformed unit
```

This is where the Doximity B+/stress evidence applies most directly.

---

# 6. RENDER functions

## R1 — Unit Realization

Very little open-ended prompting.

Use canonical operator definitions.

Example:

```text
OPERATOR=PLAN_CONDITIONAL
REQUIRE:
    ACTION
    CONDITION
OUTPUT:
    <ACTION>; <CONDITION>.
IF missing required field:
    CONTRACT_ERROR
```

The LLM supplies grammar only within the operator's fixed surface envelope.

This is the strongest pseudocode/DSL region because it produced 108/108 correct valid-vs-invalid behavior in the stress suite.

---

## R2 — Section Composition

This is the exception: natural language capability is useful again.

HPI/history need fluency.

### LLM
Use general language ability to make ordered unit text read naturally.

### Prose boundary
Must be extremely explicit:
- prose sections only;
- preserve unit order;
- no deletion;
- no semantic merging;
- no new causal/temporal connectives;
- no new uncertainty interpretation;
- A/P bypasses R2.

### Pseudocode
Only guardrails:

```text
FOR adjacent units in section order:
    preserve every unit payload
    join only where section contract permits
    preserve semantic boundaries
```

Do not canonicalize every HPI sentence unless experiments show clinically meaningful drift.

---

## R3 — Note Assembly

Almost entirely mechanical/pseudocode.

```text
FOR SECTION in CaseIR.section_order:
    emit section heading
    emit completed section payload
DO NOT add/omit/reorder sections
AP uses direct bullet-unit output
prose sections use R2 output
```

No reason to spend model intelligence here.

---

# 7. General rule for deciding prose vs pseudocode

When writing each function, ask:

## Question A
Is the decision primarily **semantic/clinical** and context-dependent?

If yes:
> use LLM capability + prose contract.

Examples:
- what is the neurologic problem?
- is this prior diagnosis currently adopted?
- are these two objects clinically the same proposition?
- is this fact relevant to this problem?

## Question B
Is the decision primarily **accounting/structural** and has a closed correct form?

If yes:
> use pseudocode / DSL.

Examples:
- every object must be used or dispositioned;
- a condition attaches to one action;
- unit order;
- section order;
- required fields;
- standing-item trigger schema;
- fail closed.

## Question C
Is the task **surface language** after semantics are fixed?

If wording variation is acceptable:
> use general LLM capability within prose boundaries.

If wording stability matters:
> use canonical operator pseudocode.

This rule is more important than the exact percentages.

---

# 8. Proposed system-wide proportion

At the architecture level, I would roughly target:

### INGEST
- semantic LLM: **~50%**
- prose policy: **~30%**
- pseudocode/accounting: **~20%**

### STRUCTURE
- semantic LLM: **~45%**
- prose policy: **~30%**
- pseudocode/accounting: **~25%**

But internally this is uneven:
- S1 is mostly LLM;
- S4 is mostly DSL/pseudocode.

### RENDER
- semantic LLM: **~20%**
- prose/style contract: **~25%**
- pseudocode/operators: **~55%**

These percentages are only design intuition. They should **not** be frozen until E1/E2 tests measure where Doximity actually drifts.

The stronger invariant is the qualitative allocation table in §3.

---

# 9. What not to do

Do not:
- write pseudocode that pretends to mechanize clinical judgment;
- rely on broad prose for merge/split/accounting/order decisions already known to drift;
- write huge exception lists;
- let RENDER infer missing semantic relations;
- use canonical operators for every sentence merely to chase textual identity;
- force the clinician to manually author the internal DSL.

The DSL is an internal model contract.

---

# 10. Recommended next design sequence

1. Freeze the **function** of each submodule in plain language.
2. For each function, mark each decision as:
   - SEMANTIC;
   - POLICY;
   - MECHANICAL.
3. Map:
   - SEMANTIC -> LLM + prose;
   - POLICY -> precise prose;
   - MECHANICAL -> pseudocode/DSL.
4. Only then write the actual module instructions.
5. Test E1 before expanding operator/pseudocode coverage.

This prevents us from choosing syntax before we know which decisions actually require it.
