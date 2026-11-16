# Serialization and sentinel failures

**Evidence class:** REPRODUCED
**Date:** 2026-11-16
**Scope:** Doximity Ask output serialization for coverage and synthesis handoffs.

## Finding

Custom `@@` output records are not reliable in Doximity Ask.

A simple plain-text input check worked:

```text
first_record=T001; t_count=25
```

The same check expressed with a custom `@@CHECK` record returned only:

```text
@@END
```

A JSON version of the same check worked:

```json
{"first_record":"T001","t_count":25}
```

Synthesis attempts using `@@PROBLEM`, `@@UNIT` and `@@ACTION` repeatedly produced truncated records:

- `@@PROBLEM` stopped after four fields;
- `@@UNIT` stopped after the label;
- action wording became generic and lost source content;
- some runs emitted only `@@END`.

This happened after the packet was confirmed visible and readable. It is not an input-visibility failure.

## What this means

The model can read the packet and answer in plain text or JSON. It does not reliably reproduce a custom
`@@` record protocol as output.

`@@` appears to be treated as control framing rather than content. Unknown or complex `@@` records can be
dropped, collapsed, or truncated.

Pipe-delimited records are also unsafe: Doximity rendered them as Markdown tables, adding empty fields and
breaking the parser.

`;;` fields worked for simple three-field coverage records, but complex seven- and nine-field records still
truncated. Delimiter choice alone does not fix schema pressure.

## Durable rules

1. Use **JSON** for model-authored structured handoffs.
2. Return one JSON object. No prose, no Markdown, no code fence.
3. Do not use `|` as a field or record delimiter.
4. Do not use custom `@@COV`, `@@PROBLEM`, `@@UNIT`, `@@ACTION`, `@@CHECK` or `@@UNRESOLVED` output records.
5. `@@PACKET`, `@@SOURCE` and `@@END` in the **Scribe input packet** are input framing, not a model-output
   format. Do not copy that style into downstream model outputs.
6. Do not mix JSON and `@@` records in one response.
7. Validate JSON keys and array types mechanically. Fail closed on extra prose or missing keys.
8. If a JSON handoff fails, first test input visibility with a plain-text question, not another sentinel
   format.

## Why JSON works better here

- JSON is whitespace-insensitive; collapsed line breaks do not destroy structure.
- It does not trigger Markdown tables.
- It does not require the model to reproduce custom control markers.
- It avoids positional field counts.
- It is familiar enough that the model produces it reliably in this environment.

JSON does **not** fix semantic classification. Coverage buckets can still be wrong or over-inclusive. It
only fixes serialization.

## Recommended handoff shapes

Coverage:

```json
{
  "coverage": {
    "current_event_records": [],
    "background_records": [],
    "medication_records": [],
    "exam_records": [],
    "workup_records": [],
    "reasoning_records": [],
    "action_records": [],
    "baseline_comparator_records": []
  }
}
```

Synthesis:

```json
{
  "problems": [],
  "units": [],
  "actions": [],
  "unresolved": []
}
```

## Do not conclude

Do not conclude that the model cannot follow structure. The plain-text and JSON checks worked. The failure
is specific to the custom `@@` output protocol and, separately, pipe-delimited table syntax.

Do not add more prose warnings around `@@`. Replace the serialization.
