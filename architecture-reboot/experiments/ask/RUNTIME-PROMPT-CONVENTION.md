# Doximity runtime prompt convention

Use this convention for long Doximity runtime files.

## 1. Top execution gate

Place immediately after the title.

```text
## EXECUTION GATE

1. Read this entire instruction file before producing output.
2. Read the complete input before starting the transformation.
3. Do not draft, stream, or emit output while reading or interpreting instructions.
4. Silently complete: READ -> EXTRACT -> DECIDE -> CHECK -> EMIT.
5. Apply all rules before committing output.
6. Do not emit reasoning, scratch work, partial results, or progress text.
7. Output schemas define allowed structure. They do not authorize unsupported field completion.
8. Omit optional fields rather than infer values to fill the schema.
```

## 2. Output lock

Use these rules when the file is long or multi-phase.

- Do not emit before CHECK passes.
- If CHECK fails, revise internally and run CHECK again.
- Do not print CHECK, PASS, READY, or internal phase labels.
- Emit once.
- Use exact start and end markers when the contract provides them.

## 3. Multi-file controller gate

Controllers must state:

- read the controller completely;
- read every attached stage file completely;
- read the complete input;
- then execute stages;
- keep intermediate handoffs internal until all required stages finish;
- emit only the required final return package.

## 4. Final output gate

Place after every substantive rule and validation check.

```text
## FINAL OUTPUT GATE

Before emitting:

1. Re-read the output contract.
2. Run every structural and source-fidelity check.
3. Correct any internal violation.
4. Verify no unsupported value was added only to complete a schema.
5. Emit the required output once.
6. Emit nothing else.
```

The final gate must be the last substantive instruction before the return command.

## 5. Prompt style

Prefer atomic instructions.

- One rule per bullet.
- One decision per sentence.
- Short headings.
- Short lists.
- Put prohibitions next to the rule they constrain.
- Put schema rules next to the schema.
- Avoid long explanatory paragraphs in runtime files.
- Avoid rhetorical discussion.
- Avoid repeating the same rule throughout the file.
- Repeat only high-risk invariants in the final gate.
- Examples must illustrate one rule at a time.
- Examples must not teach case-specific answers in controlled experiments.

## 6. Anti-completion rules

Use when a schema has optional fields.

- Missing evidence means omit the field.
- Silence is not a value.
- Absence of a result is not `pending` or `unavailable`.
- Future wording is not nonperformance.
- Recommendation is not order.
- Reported performance is not objective performance.
- A schema slot is not a request to infer its value.

## 7. Boundary rule

The gate changes execution behavior only.

It must not:
- add a semantic stage;
- move responsibility between stages;
- create a validator;
- change clinical meaning;
- change an experiment hypothesis.

## 8. Current use

Apply to:
- active Ask ingestion;
- active clinical synthesis;
- direct-B experiments;
- integration controllers;
- future compiler;
- future renderer.

Do not revive superseded modules only to add this convention.
