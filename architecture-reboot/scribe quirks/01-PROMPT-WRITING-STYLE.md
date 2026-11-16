# Prompt Writing Style for Doximity

## Status

**REPRODUCED / ACTIVE STYLE**

This style is based on the current Scribe prompt behavior plus the runtime-gating experiments.

The central idea is:

> Treat the prompt as a sequence of small executable functions with explicit boundaries, not as an essay describing desired behavior.

---

# 1. Start with a hard execution gate

Put the gate before substantive instructions.

Preferred form:

```text
Read this entire instruction set before emitting any output.

Do not begin output while still reading or interpreting the instructions.

Before writing the output, silently perform the required passes.
```

For multi-stage prompts:

```text
Read the entire controller.
Read every attached stage file.
Read the complete input.
Do not emit an intermediate handoff while still reading later-stage instructions.
Complete all required internal phases before emission.
```

## Why

Observed behavior improved when Doximity was explicitly prevented from early commitment.

Without the gate, the model can begin solving the task while later instructions have not yet constrained the solution.

## Rule

**READING and EMISSION are separate phases.**

---

# 2. Use a fixed internal execution sequence

Preferred:

```text
READ
EXTRACT
DECIDE
CHECK
EMIT
```

Each phase should have one responsibility.

### READ

Understand all instructions and the complete input.

### EXTRACT

Identify only material the current stage is authorized to use.

### DECIDE

Make only the semantic decisions owned by this stage.

### CHECK

Apply structural and semantic boundary checks.

### EMIT

Return only the required artifact.

## Do not expose these phases in output

They are execution control, not content.

---

# 3. Write functions as atomic imperatives

Good:

```text
Process transcript turns in original order.

Do not merge adjacent turns.

Keep a question only when an elliptical answer cannot be interpreted without it.

Split one clinician turn when it contains two independently recoverable management targets.

Preserve "planned" as planned.

Do not convert "planned" to "ordered".
```

Bad:

```text
Be careful to preserve provenance and try not to infer too much while maintaining clinically meaningful distinctions and ensuring that management decisions are appropriately represented.
```

The second form contains multiple hidden functions and no explicit failure boundary.

## Atomic-function rule

One instruction should preferably answer one of these:

- **what to inspect;**
- **what to preserve;**
- **what to split;**
- **what to omit;**
- **what decision may be made;**
- **what decision is forbidden;**
- **what must be checked;**
- **what must be emitted.**

---

# 4. Give every function an explicit boundary

Preferred structure:

```text
FUNCTION

Do:
- X
- Y
- Z

Do not:
- A
- B
- C
```

Example:

```text
SOURCE-LOCAL EXTRACTION

Process one raw turn at a time.

Keep clinical evidence.
Keep clinician interpretation.
Keep management.

Do not merge turns.
Do not reconcile speakers.
Do not infer a missing answer.
```

This is more reliable than a paragraph containing both permissions and prohibitions.

---

# 5. Separate local functions from whole-packet functions

Do not burden every source record with decisions that only make sense after the packet exists.

## Local functions

Execute while reading one raw source unit:

- source boundary;
- KEEP / OMIT;
- source-local splitting;
- source-local state preservation;
- nested provenance;
- unclear/verbatim preservation.

## Whole-packet functions

Execute after candidate records exist:

- coverage census;
- action census;
- completeness audit;
- final deletion sweep;
- serialization check.

This reduces competing objectives during extraction.

---

# 6. Prefer closed vocabularies only when the model can classify them safely

Closed vocabularies are useful for:

- rhetorical class;
- render operator;
- broad coverage bucket;
- action category;
- valid structural roles.

They are risky when they invite unsupported semantic completion.

Repeated failure example:

```text
decision=
execution=
response=
result=
```

Even when optional, Doximity repeatedly filled unsupported dimensions.

## Rule

A closed schema is safe only when:

1. every field has a clearly observable source basis;
2. omission is natural;
3. the model is not pressured to complete a conceptual state table;
4. repeated tests show it does not invent values.

Otherwise preserve source-qualified wording instead of normalizing.

---

# 7. Anti-completion must be explicit

Use:

```text
Output schemas define allowed structure.

They do not authorize unsupported field completion.

Omit optional fields rather than infer values to fill the schema.
```

This helps, but note:

> Repeating anti-completion prose does not rescue a representation that structurally invites completion.

That was demonstrated by the action-state experiments.

---

# 8. Put the output contract late

The model should first know:

1. the function;
2. the boundaries;
3. the checks;
4. then the serialization.

Avoid leading with a large schema before the engine understands the semantic contract.

A schema shown too early can become a completion target.

---

# 9. Put the final emission gate last

The last substantive instruction should be an output lock.

Preferred:

```text
FINAL OUTPUT GATE

Before emitting:

1. Re-read the output contract.
2. Run every structural check.
3. Correct any internal violation.
4. Verify no unsupported field was added only to complete the schema.
5. Emit the complete artifact once.
6. Emit nothing else.
```

For Scribe, the final gate may also include:

- deletion sweep;
- record grammar verification;
- complex-turn split check;
- template/scaffold deletion check.

---

# 10. Use examples to define boundaries, not to teach clinical reasoning

Useful examples:

```text
"We need an EEG."

Allowed:
Stated EEG is needed.

Not allowed:
EEG ordered.
```

Useful:

```text
"CT was done but I have not reviewed it."

Allowed:
CT completed; not yet reviewed.

Not allowed:
CT pending.
Not allowed:
CT normal.
```

The example demonstrates a transformation boundary.

Avoid examples that encourage the model to infer a case-specific clinical conclusion.

---

# 11. State invalid transformations explicitly

Doximity often makes plausible completion errors.

Explicitly forbid:

- question -> answer;
- silence -> negative;
- recommendation -> order;
- plan -> performance;
- completed test -> available result;
- not reviewed -> pending;
- temporal sequence -> causation;
- witness diagnosis -> established diagnosis;
- service label -> actor identity;
- chronic symptom -> separate problem;
- same target -> same action episode.

These are recurring failure classes, not hypothetical warnings.

---

# 12. Prefer source-local language over normalized semantic labels when the label is brittle

If the source says:

```text
will keep Keppra for now
```

preserve:

```text
continue levetiracetam for now
```

Do not force:

```text
decision=continue
execution=not_started
result=unavailable
```

The source-qualified wording retained the clinically important distinction more reliably than the normalized slots.

---

# 13. Do not make the model copy exact source substrings during synthesis unless required

Repeated experiments showed neighboring-record drift and nonliteral selectors.

When the Scribe packet already has coherent record boundaries:

- prefer stable record IDs for provenance;
- mechanically dereference exact source text later if needed;
- do not require the synthesizer to reproduce exact quote fragments while reasoning.

If exact sub-record selection is truly necessary, treat that as a source-boundary problem first.

---

# 14. Do not combine generation and semantic self-validation

Same-context validators visibly executed full checklists and still false-passed obvious defects.

Do not rely on:

```text
Generate semantic claim
-> same model validates claim
-> PASS means safe
```

Mechanical checks are different.

Good mechanical checks:

- required marker exists;
- ID exists;
- duplicate ID;
- enum membership;
- group has one HEAD;
- object appears at most once;
- referenced source record exists.

Semantic correctness should be resolved by better ownership and representation, not a same-model PASS label.

---

# 15. Treat functions as contracts, not file count

A function can be:

- a local pass;
- a packet-level pass;
- an internal phase;
- a separate module;
- a render operator.

Do not create a separate file or model call merely because a new function exists.

Split execution only when evidence shows the model cannot reliably perform the functions together.

---

# 16. Preferred Doximity prompt grammar

Use:

- short headings;
- short imperative lines;
- one rule per line;
- explicit DO / DO NOT boundaries;
- small closed lists;
- literal output markers;
- examples only where they clarify a known failure mode;
- final gate at the end.

Avoid:

- long explanatory paragraphs;
- architecture history inside runtime prompts;
- multiple synonyms for the same rule;
- aspirational language;
- vague "use judgment";
- hidden compound functions;
- large semantic state tables unless empirically validated;
- decorative prose.

---

# 17. Function definition template

Use this when adding a new function:

```text
==================================================
FUNCTION NAME
==================================================

PURPOSE

<one sentence>

INPUT

<what this function may inspect>

DO

<atomic rule>
<atomic rule>
<atomic rule>

DO NOT

<forbidden decision>
<forbidden decision>

IF UNCERTAIN

<fail/omit/unresolved behavior>

OUTPUT

<exact allowed shape>

CHECK

<observable invariants>
```

Not every runtime block needs every heading, but the semantic structure should be this clear.

---

# 18. Highest-confidence writing principle

> If a rule matters, express it as an executable atomic boundary.

Do not rely on the model to infer the intended boundary from explanatory prose.
