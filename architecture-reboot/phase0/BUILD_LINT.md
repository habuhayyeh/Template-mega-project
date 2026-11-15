# BUILD_LINT — what the compiler refuses

The deployment package is assembled from many files. The lint runs on every build and fails the build on any violation below. It is the only instrument that can see contradiction between contract statements.

## 1. What the lint governs

The lint does not scan files for prose. Every normative statement is a **rule record** with explicit fields, and the lint operates on records.

```yaml
rule: R-014
decision: AP_ORDER_REASONING             # the decision this rule governs
owner_contract: AP_RENDER_CONTRACT       # the contract that owns the decision — not the file
scope: RENDER                            # INGEST | STRUCTURE | RENDER | CHECK | AUDIT | BUILD | SHARED
normative:
  modality: MUST_FIRST                   # MUST_FIRST | MUST_AFTER | MUST | MUST_NOT | ALLOWED
  subject: reasoning
  object: facts
fixture: F-02
check: C-AP-ORDER
```

Required: `rule`, `decision`, `owner_contract`, `scope`, `normative`. Optional: `fixture`, `check`, `note`.

The record above is illustrative. The syntax is not frozen; what is frozen is that these fields exist and are machine-readable.

## 2. Violations

### L1 — Contradictory rules

Two rules with the same `decision` whose `normative` fields are comparable and differ.

Comparable means they describe the same subject and object in a way where both cannot hold — for example `MUST_FIRST reasoning / facts` against `MUST_AFTER reasoning / facts`.

Different wording of the same requirement is not a contradiction and is not reported.

### L1c — Unresolved authority

Two rules share a `decision` but their normative fields are not comparable, so a machine cannot tell whether they agree.

This fails the build. If a machine cannot decide whether two statements conflict, a reader cannot either, and the runtime will pick one arbitrarily — which is the mechanism that produced the original contradiction.

### L2 — Duplicate authority

Two contracts claim `owner_contract` for the same `decision`.

Authority belongs to a **decision id**, and a decision id has exactly one owning contract. Files are carriers, not owners: splitting one contract across three files does not create three owners; putting two contracts in one file creates two.

### L2b — Orphan decision

A decision that appears in rules but has no owning contract, or whose owning contract no longer exists.

### L3 — Out-of-scope rule

A rule whose statement governs behaviour outside its declared `scope`.

Examples: a `RENDER` rule that selects content; an `INGEST` rule that assigns sections.

`scope: SHARED` may define vocabulary used everywhere but may not issue per-module instructions.

### L4 — Untested rule

A rule with neither `fixture` nor `check`.

### L5 — Dangling reference

A `fixture`, `check`, `decision` or `owner_contract` reference that does not exist or is marked withdrawn.

### L6 — Unresolved conflict marker

Unmerged text in a compiled file.

## 3. Severity

Every violation fails the build. There are no warnings.

| Violation | Result |
|---|---|
| L1 contradictory | fail |
| L1c unresolved authority | fail |
| L2 duplicate authority | fail |
| L2b orphan decision | fail |
| L3 out of scope | fail |
| L4 untested | fail |
| L5 dangling reference | fail |
| L6 conflict marker | fail |

## 4. Output

```text
BUILD_LINT
  files: 14   rules: 96   decisions: 71   contracts: 9
  L1  contradictory ............ 0
  L1c unresolved authority ..... 0
  L2  duplicate authority ...... 0
  L2b orphan decision .......... 1   ← R-041 / AP_ORDER_2 has no owning contract
  L3  out of scope ............. 0
  L4  untested ................. 0
  L5  dangling reference ....... 0
  L6  conflict marker .......... 0
  RESULT: FAIL
```

The report names rule ids, the decision, the contracts, and the file each rule was compiled from. It localises; it does not explain.

## 5. What the lint does not do

- It does not decide whether a rule is clinically right.
- It does not repair, suggest, or downgrade.
- It does not scan prose. A statement not written as a rule record is documentation, and documentation is not compiled.

## 6. When it runs

Every commit touching a contract file, every packaging run, and as a precondition of acceptance. A package that fails lint is not a valid artifact, regardless of its output.
