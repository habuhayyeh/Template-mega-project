# BUILD_LINT — what the compiler refuses

The deployment package is assembled from many small files. The lint runs on every build and fails the build on any of the violations below. It is the only instrument that can see contradiction between files; no runtime module can.

## 1. Violations

### L1 — Contradictory rules (class C11)

Two rules govern the same decision and prescribe outcomes that cannot both hold.

How it is detected — deliberately narrow, because the lint does not judge prose:

1. each rule's normative content is reduced to a tuple `(modality, order, threshold)` — for example `MUST_FIRST`, `MUST_AFTER`, `COUNT>=2`;
2. two rules with the same `DECISION_ID` whose tuples are **comparable and differ** are a contradiction (L1);
3. two rules with the same `DECISION_ID` whose tuples are **not comparable** are reported as **L1b ambiguous authority** — not an automatic failure, but they must be merged into one rule or given distinct ids.

Two rules saying the same thing in different words are not a contradiction. A lint that treated differing prose as disagreement would flag every rephrasing and would stop being used.

Example that motivated it: one section of the old writer said reasoning precedes facts, another said it follows them. Both were in the package. The writer obeyed a different one per run.

### L2 — Duplicate authority

More than one file claims to own the final say on a decision.

How it is detected: `decision → owning file` must be one-to-one. A second file may reference the decision, never redefine it.

### L3 — Out-of-scope rule

A rule that governs behaviour outside its module's declared scope.

Examples: a renderer rule that selects content; an ingest rule that assigns note sections.

How it is detected: each file declares a scope (`INGEST`, `STRUCTURE`, `RENDER`, `CHECK`, `AUDIT`). A rule may reference another scope's identifiers but may not issue instructions to it.

### L4 — Untested rule

A rule with no fixture and no check reference.

How it is detected: every rule carries either `fixture:` or `check:` pointing to something that exists.

A rule nobody can test is a preference, and preferences accumulate.

### L5 — Dangling reference

A rule cites a contract, fixture, operator or check id that does not exist, or cites an id marked withdrawn.

### L6 — Unresolved conflict marker

Any conflict marker or unmerged text in a compiled file.

## 2. Rule declaration format

Every normative line carries a machine-readable tag on the preceding line:

```text
<!-- rule DECISION_ID=AP_ORDER_1 scope=RENDER class=L1 -->
Facts render before reasoning within a problem block.
```

Required attributes: `DECISION_ID`, `scope`. Optional: `fixture`, `check`, `note`.

Rules without a tag are prose, not contract, and are compiled into a `NOTES` section that the runtime does not read.

## 3. Output

The lint emits a report:

```text
BUILD_LINT
  files: 14   rules: 96   decisions: 71
  L1 contradictory ............ 0
  L1b ambiguous authority ..... 0
  L2 duplicate authority ...... 0
  L3 out of scope ............. 0
  L4 untested ................. 3   ← fail
  L5 dangling reference ....... 1   ← fail
  L6 conflict marker .......... 0
  RESULT: FAIL
```

Failures list the file, the line, the rule ids involved, and the decision id. No prose explanation; the report is read by whoever wrote the rule.

## 4. What the lint does not do

- It does not judge whether a rule is clinically right.
- It does not repair anything.
- It does not weaken to a warning. A violation fails the build; a build that only warned is how the old package accumulated contradictions.

## 5. When it runs

- on every commit that touches a contract file;
- on every packaging run;
- as part of acceptance. A package that fails lint is not a valid artifact, regardless of how its output looks.
