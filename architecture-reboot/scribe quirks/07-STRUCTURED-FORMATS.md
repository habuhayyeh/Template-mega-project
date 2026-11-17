# Structured format comparison — JSON, CSV, YAML

**Evidence class:** OBSERVED / REPRODUCED
**Date:** 2026-11-16
**Scope:** Doximity Ask handoffs for coverage and synthesis.

## Finding

JSON is the safest structured handoff.

CSV works for the flat coverage census, but not as the canonical format for nested synthesis.

YAML failed the nested coverage shape: the model returned the bucket keys without indentation under
`coverage`, so `coverage` was empty and the buckets sat at the root.

## Observed results

### JSON

- Returned one valid object with the eight coverage arrays.
- Nested objects and arrays survive.
- No Markdown table, no field-count problem.
- One run had a semantic error (`T015` in `current_event_records` and `workup_records`), but the format was
  valid. Format success is not semantic correctness.

### CSV

- Returned a valid `bucket,record_id` table.
- All eight buckets appeared.
- Easy to parse and inspect.
- Works only because coverage is flat. Synthesis would need separate `problems.csv`, `units.csv`,
  `actions.csv`, `unresolved.csv` and manual joins.
- One run duplicated baseline rows (`T002`, `P1.002`), a semantic error, not a CSV error.

### YAML

- Returned the eight keys, but not nested under `coverage`.
- Indentation did not survive.
- Invalid for the expected `coverage` object.
- Not recommended for nested records.

## Rules

1. **JSON is canonical** for coverage and synthesis handoffs.
2. **CSV is allowed** for the flat coverage census and for human review/export.
3. **Do not use CSV as the canonical synthesis format.** Nested problems/units/actions would require
   multiple tables and joins.
4. **Do not use YAML for nested handoffs.** If YAML is used at all, keep it flat and validate indentation.
5. **Do not maintain two sources of truth.** JSON is authoritative; CSV is an export/view.
6. **Format does not fix semantics.** A valid JSON or CSV object can still over-tag or omit records.

## Integration pattern

```text
Doximity -> JSON handoff -> external parser/validator
                              |
                              +-> CSV export for review
```

Do not feed the CSV export back as the primary input unless the importer reconstructs the same schema.

## Related experiments

- `../experiments/ask/COVERAGE-JSON-PROMPT.md`
- `../experiments/ask/COVERAGE-CSV-PROMPT.md`
- `../experiments/ask/COVERAGE-YAML-PROMPT.md`
