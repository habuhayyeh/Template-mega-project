# DeepSeek confirmation — comparator ready

**Verdict:** READY TO RUN COMPARATOR.

The error threshold is now explicit:

```text
direct_errors <= min(A1_errors, A2_errors)
```

and applies to each direct-B run individually. No ambiguity remains.

The rest is unchanged and adequate:

- two fresh runs per arm;
- no averaging of material failures;
- A→B citation mapping through A spans;
- direct-B citation mapping to Scribe;
- canonical action-concept normalization;
- problem threshold with encounter relevance;
- mixed results inconclusive.

Run A1/A2/D1/D2 on the same clean packet. Do not attach the oracle to Doximity. Do not advance to
CLINICAL_UNIT/C until the comparator is adjudicated.

No new stage, enum or validator. No acceptance or production change.
