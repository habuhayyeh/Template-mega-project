# P006 v4 review — original architecture branch

## Verdict

**REVISE — nearly acceptable. Two contract blockers remain, plus one signer style choice.**

The six v3 blockers are otherwise addressed correctly:
- rhetorical classes are explicit;
- G5 is source-faithful;
- ungrouped eligibility is preserved;
- COVERED accounting is line/trace based;
- ordering is class-specific;
- signer option B for G1 provenance is incorporated without treating 2024-02 as event timing.

## 1. COMPOSE_GROUP still reopens compatibility in 05

Section 3 says:

> COMPOSE_GROUP — one plan line: head plus condition **when compatible**.

That phrase reintroduces the exact semantic decision P006 is meant to remove.

If 03 emits a valid COMPOSE_GROUP, compatibility has already been adjudicated upstream.

Required:

> COMPOSE_GROUP — one plan line: HEAD plus CONDITION. A malformed or noncomposable candidate must not be emitted as a COMPOSE_GROUP; validation fails it before 05.

05 does not decide compatibility and does not split a valid COMPOSE_GROUP.

## 2. The trace artifact is not defined

P006 repeatedly requires:
- every COVERED member has no independent output-line trace;
- every O# appears exactly once in the trace;
- ungrouped omissions carry a reason.

But the proposal never defines:
- which stage emits the trace;
- its filename/schema;
- whether it is part of the Handoff, a sidecar, or validator output;
- what 05/P005 actually consume.

That makes several validation rules non-implementable.

Required: define a minimal deterministic trace artifact.

Recommended:

`04` emits a sidecar render trace alongside the assembled Handoff, containing one row per retained O#:

```
O7  | GROUP=G1 | ROLE=HEAD
O8  | GROUP=G1 | ROLE=MODIFIER
O53 | GROUP=G1 | ROLE=COVERED
O18 | UNGROUPED | DISPOSITION=ELIGIBLE
...
```

If ungrouped omission happens only inside 05, then the **post-render validator** may append/output the final rendered/omitted disposition, but the proposal must say so explicitly. Do not leave "trace" as an undefined concept.

The exact file name is not important; ownership and schema are.

## 3. G1 provenance wording

Signer chose B, including the explicit source-display form:

`Known left MCA infarct two years prior to presentation (also documented by prior neurology, 2024-02).`

Treat `also documented by ...` as a **bounded signer-approved provenance-display rule for this group pattern**, not as a new general paraphrase transformation.

Record this preference durably if it is intended as reusable behavior rather than a one-case oracle choice.

## 4. Signer choice required for G4

Both are source-faithful and semantically acceptable:

### A — O39 as HEAD
`We'll see what the MRI shows.`

Advantages: standalone sentence; no conjunction issue.

### B — O23 as HEAD
`But the MRI will tell us.`

Advantages: preserves the stronger adjudicative wording already selected in earlier runs/contracts.

This is a style/rhetoric choice, not an architecture correctness question. D-013 applies.

## Implementation gate

After:
1. removing runtime compatibility judgment from COMPOSE_GROUP;
2. defining trace ownership/schema; and
3. signer choosing G4 A or B,

P006 can be reviewed for implementation approval.
