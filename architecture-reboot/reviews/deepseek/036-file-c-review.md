# DeepSeek review — File C note compiler contract

**Reviewed:** `03-NOTE-COMPILER.md`.
**Status:** architecture review; no implementation.

## Verdict

**Accept with one output-schema fix.** C owns the right decisions and does not reopen A/B.

## Fix — add `BLUEPRINT_UNRESOLVED`

The contract says C may preserve an unresolved A/P role "in an unresolved A/P blueprint area," but the
output schema has no such area. It also receives `ARCHITECTURE_UNRESOLVED` from B but has nowhere to carry
it.

Add:

```text
BLUEPRINT_UNRESOLVED
  ITEM=<problem/unit/section handle>
  issue=<why placement or inclusion cannot be decided>
  evidence=<handles/record IDs + selectors>
```

Use it for:

- `encounter_role=unresolved`;
- no established RFC;
- upstream `ARCHITECTURE_UNRESOLVED` that affects placement;
- a section whose inclusion depends on an unresolved architecture decision.

C must carry B's unresolved items forward. It may not drop them because the template has no obvious slot.

## What is right

- explicit blueprint before prose;
- RFC not inferred from first symptom or severity;
- HPI clinical chronology, not source order;
- disease-centered neuro history;
- meds at presentation, not encounter rewrites;
- current exam only;
- workup ordered/performed/result states separated;
- A/P only from existing B problems;
- unresolved role not converted to PRIMARY/BACKGROUND;
- shared actions one primary home;
- nonproblem evidence survives;
- no prose.

## Test after the fix

Use the existing three-record A/B output. Expected:

- no invented RFC;
- historical stroke may appear in NEURO_HX, but no A/P role is forced;
- falls are not forced into HPI or a problem;
- no MEDS/EXAM/WORKUP entries without source units;
- unresolved role carried in `BLUEPRINT_UNRESOLVED`;
- no prose.

No renderer, validator or full note. No Gate-0 acceptance. No production change.
