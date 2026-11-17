# Negative results log

**Purpose:** keep failed runs and invalid tests visible. Do not let the handbook read as a wall of passes.

Some failures are model behavior; some are test defects. Both matter.

---

## 1. Coverage omitted whole categories

Repeated attempts at an eight-category coverage census dropped categories:

- `current_event_records` missing;
- `action_bearing_records` missing;
- `investigation_records` missing;
- only 6 of 8 categories returned.

The output sometimes started at `baseline_comparator_records`, skipping the first category.

Related:

- `../reviews/deepseek/067-semicolon-output-review.md`
- `../reviews/deepseek/069-output-review-3.md`
- `../experiments/ask/COVERAGE-ONE-CATEGORY-TEST.md`

## 2. `@@` output records collapsed or truncated

- A custom `@@CHECK` input test returned only `@@END`.
- `@@PROBLEM` stopped after four fields.
- `@@UNIT` stopped after the label.
- Some runs emitted only `@@END`.

The packet was visible; a plain-text test returned `first_record=T001; t_count=25`, and a JSON test
returned `{"first_record":"T001","t_count":25}`.

Related:

- `06-SERIALIZATION-AND-SENTINELS.md`
- `../experiments/ask/DOXIMITY-CODE-EXECUTION-TEST.md`

## 3. YAML lost nesting

YAML coverage output returned:

```yaml
coverage:
current_event_records: [...]
background_records: [...]
```

The bucket keys were not indented under `coverage`, so `coverage` was empty. Invalid for the expected shape.

Related: `07-STRUCTURED-FORMATS.md`.

## 4. CSV was valid but semantically wrong

CSV coverage returned all eight buckets and parsed cleanly, but `baseline_comparator_records` included
`T002` and `P1.002`. Those are prior-history records, not baseline comparisons.

Related: `07-STRUCTURED-FORMATS.md`.

## 5. Free synthesis drifted

Same packet, same coverage, same free-synthesis prompt:

| Run | Units | Actions | Unresolved |
|---|---:|---:|---:|
| 1 | 12 | 5 | 0 |
| 2 | 14 | 6 | 5 |
| 3 | 12 | 6 | 3 |

All were valid JSON. Content varied:

- `P002` longstanding staring became a separate BACKGROUND problem in all three;
- `contains` and `separate_from` used unit IDs, labels and problem IDs interchangeably;
- `counterevidence` contained diagnostic uncertainty (`T018/T019`);
- `T008` action was missing in some runs;
- unresolved entries ranged from 0 to 5;
- global `order` changed.

Related:

- `../reviews/deepseek/072-synthesis-json-test-review.md`
- `../experiments/ask/SYNTHESIS-JSON-PROMPT.md`

## 6. First handoff test was inconclusive

Stage A sometimes returned objects, sometimes only section names. Stage B still produced correct labels and
IDs, proving it reread `FACTS`. The prompt allowed that fallback and did not define a Stage A schema.

This was a test defect, not a handoff pass.

Related: `../experiments/ask/DOXIMITY-HANDOFF-TEST.md`.

## 7. Handoff V2 expected output was wrong

The prompt required Stage B in Stage A order. Stage A started with `P001` / Assessment, but the expected
Stage B block started with HPI. The model followed the rule; the test expectation was wrong.

Fixed in the test file.

Related: `../experiments/ask/DOXIMITY-HANDOFF-TEST-V2.md`.

## 8. Code execution never succeeded

- Python: `NO_RUNTIME`.
- Node.js: `NO_RUNTIME`.
- PowerShell: `NO_RUNTIME`.
- Bash: refused.
- R and Go: explained code, said run locally.
- PHP/Ruby/Perl/Java/R batch: generic “Ask is for clinical tasks” refusal.

No run returned the expected SHA-256 hash.

Related: `08-NO-CODE-EXECUTION.md`.

## 9. Test-design lessons

- A free semantic synthesis test cannot be scored by exact labels without a gold output.
- A handoff test must forbid Stage B from rereading the source facts.
- A test’s expected output must follow its own ordering rule.
- Format validity does not imply semantic correctness.
- One passing run is not determinism.
