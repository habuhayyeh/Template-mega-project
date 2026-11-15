# ChatGPT proposal 008 — two-LLM implementation workflow

## Purpose

Define how ChatGPT, DeepSeek, and the signer move from the frozen architecture into concrete implementation files without recreating the old project's failure modes.

This document is about **engineering process**, not runtime architecture.

No implementation files should be authored until this workflow is agreed.

---

# 1. Roles

## Signer / user — product owner and runtime authority

Owns:
- final clinical/style/product decisions;
- resolving genuine ChatGPT↔DeepSeek disagreements when evidence does not decide;
- running the actual Doximity experiments;
- supplying raw Doximity outputs as acceptance evidence.

Does not need to:
- manually reconcile schemas;
- carry intermediate runtime artifacts;
- decide implementation details already settled by evidence.

Only actual signer-run Doximity results count as Doximity acceptance evidence.

---

## DeepSeek — primary implementation engineer

Primary responsibility:
> turn frozen specifications into concrete modular implementation files.

Owns:
- first draft of runtime implementation files;
- exact prompt prose;
- pseudocode/DSL encoding;
- field-level schema implementation;
- operator definitions;
- build/package implementation;
- revisions after accepted review findings.

Must not:
- silently alter frozen interfaces/functions;
- add new semantic authority to a submodule;
- patch one fixture with a case-specific rule without proposing the general rule;
- mark its own implementation accepted.

If implementation exposes a defect in the frozen design, DeepSeek files a **CHANGE REQUEST** rather than silently redesigning the module.

---

## ChatGPT — architecture custodian and independent reviewer

Primary responsibility:
> preserve the frozen design, define acceptance obligations, and adversarially review implementation against historical failures.

Owns:
- pre-authoring implementation/acceptance brief for each artifact;
- review of DeepSeek implementation;
- failure-mode coverage;
- contract-boundary review;
- regression review;
- recommendation to ACCEPT / REVISE / REOPEN DESIGN.

Must not:
- silently rewrite DeepSeek-owned implementation files;
- relax a frozen requirement merely to make implementation easier;
- treat mechanical validity as semantic correctness;
- accept a file solely because one fixture passes.

ChatGPT may propose exact replacement text or pseudocode in review, but DeepSeek remains the implementation-file author unless ownership is explicitly reassigned.

---

# 2. One writer per implementation path

To preserve provenance and avoid simultaneous competing edits:

- DeepSeek owns implementation/runtime source files.
- ChatGPT owns review/acceptance artifacts.
- Consensus documents are updated only after explicit agreement.
- Raw Doximity run artifacts are immutable evidence once added.

Neither LLM should edit the other's owned review/proposal path.

---

# 3. The implementation unit: one artifact at a time

Do not ask DeepSeek to write the entire system in one pass.

Each implementation artifact moves through a fixed lifecycle:

```text
FROZEN DESIGN
    |
    v
A. ACCEPTANCE BRIEF
    |
    v
B. IMPLEMENTATION DRAFT
    |
    v
C. INDEPENDENT REVIEW
    |
    v
D. REVISION
    |
    v
E. STATIC / FIXTURE VALIDATION
    |
    v
F. DOXIMITY TEST WHEN APPLICABLE
    |
    v
G. FREEZE ARTIFACT
```

Only then should a dependent artifact treat it as stable.

---

# 4. Step A — ChatGPT writes the acceptance brief before implementation

For each file/module, ChatGPT first produces a short acceptance artifact containing:

1. **PURPOSE**
2. **INPUT**
3. **OUTPUT**
4. **DO**
5. **AVOID**
6. **DETECT**
7. **FAILURE BEHAVIOR**
8. **CONTROL MODE**
9. **VALIDATION MODE**
10. **HISTORICAL REGRESSIONS THIS FILE MUST PREVENT**
11. **DEPENDENCIES**
12. **ACCEPTANCE FIXTURES / TEST OBLIGATIONS**

This brief must derive from frozen consensus, not invent new architecture.

DeepSeek reviews the brief before writing implementation.

If DeepSeek believes the brief contradicts the frozen design, it challenges the brief now rather than compensating in implementation.

---

# 5. Step B — DeepSeek writes the implementation artifact

DeepSeek converts the accepted brief into the concrete file.

Implementation should prefer:

- natural-language prose where semantic judgment is intended;
- typed DSL/pseudocode where structure/accounting must be explicit;
- canonical operators where wording/reproducibility requires it;
- fail-closed states where the submodule cannot satisfy its contract.

Every implementation file should identify:
- version;
- dependencies;
- frozen contract/brief it implements.

It should not copy entire upstream/downstream specs unless required; avoid duplicate authority.

---

# 6. Step C — ChatGPT reviews independently

ChatGPT reviews the implementation against:

1. frozen interface;
2. frozen function;
3. acceptance brief;
4. known historical failures;
5. scope/authority boundaries;
6. contradiction with other files;
7. unnecessary prompt complexity;
8. whether prose should instead be typed structure;
9. whether typed rules are pretending to mechanize semantic judgment.

Review outcome must be one of:

- **ACCEPT**
- **REVISE**
- **REOPEN DESIGN**

No ambiguous "looks good."

---

# 7. Step D — DeepSeek revises; ChatGPT verifies

For **REVISE**:
- DeepSeek changes only the implementation file it owns;
- responds point-by-point to the review;
- identifies any recommendation it rejects and why.

ChatGPT then verifies the revised artifact.

Repeat until ACCEPT or genuine design disagreement.

For **REOPEN DESIGN**:
- implementation stops;
- disputed point returns to architecture review;
- user is involved if evidence does not decide.

Do not patch around an architectural disagreement.

---

# 8. Step E — static and fixture validation

Before Doximity testing, run every available non-Doximity validation:

- schema/type checks;
- accounting checks;
- conflict lint;
- source-coverage fixtures;
- known failure fixtures;
- operator stress fixtures;
- regression fixtures from old failures.

A file that fails local/static validation does not proceed to Doximity.

Passing static validation proves only the predicates tested.

---

# 9. Step F — Doximity acceptance

Only artifacts whose behavior depends on the Doximity model need signer-run Doximity acceptance.

For each Doximity experiment:

1. Freeze exact package/version before the run.
2. Use fixed synthetic fixture(s).
3. Run in multiple fresh conversations under the same condition.
4. Save raw outputs unchanged.
5. Compare the relevant intermediate artifact, not only the final note.
6. Record both:
   - mechanical validator results;
   - semantic review results.

Do not edit the prompt between repeated runs of one experiment.

---

# 10. Independent scoring of Doximity results

To avoid consensus bias:

1. Raw run outputs are committed first.
2. ChatGPT reviews the raw runs against the frozen acceptance brief.
3. DeepSeek reviews the same raw runs against the same brief.
4. Each writes its own review before reconciliation where feasible.
5. Then compare disagreements.

The acceptance question is not:
> "Did one run look good?"

It is:
> "Did the artifact satisfy the frozen contract reproducibly, and where did failures localize?"

---

# 11. Step G — artifact freeze

An implementation artifact is frozen only when:

- DeepSeek implementation is complete;
- ChatGPT review = ACCEPT;
- static/fixture tests pass;
- required Doximity acceptance passes;
- no unresolved contradiction with existing frozen files.

Freeze means:
- dependent files may rely on it;
- future edits require regression testing;
- semantic/interface changes require a formal change request.

---

# 12. Change-control rule

Every later edit is classified as one of:

## PATCH
No semantic contract change.
Examples:
- typo;
- exact schema bug;
- non-semantic formatting error.

## IMPLEMENTATION CHANGE
Same frozen function, different prompt/DSL/operator implementation.

Requires:
- targeted tests;
- whole-suite regression where non-local sensitivity is plausible.

## DESIGN CHANGE
Changes:
- goal;
- input/output;
- decision ownership;
- function;
- semantic authority.

Requires:
- architecture review;
- DeepSeek + ChatGPT agreement;
- user decision if unresolved.

This classification prevents implementation patches from silently changing architecture.

---

# 13. Proposed file-authoring order

Do not write I1 through R3 immediately.

The dependency order should be:

## Phase 0 — engineering control files
1. implementation manifest/status ledger;
2. acceptance-brief template;
3. change-request template;
4. regression/test fixture registry.

## Phase 1 — shared contracts
5. source/paste contract;
6. identifiers and common enums;
7. failure-state vocabulary;
8. normalization/source-fidelity contract;
9. Case IR schema skeleton;
10. centralized ordering contract skeleton;
11. standing-item contract skeleton;
12. style/voice contract skeleton.

These shared contracts must have one authority each.

## Phase 2 — INGEST
13. I1 Source Map;
14. I2 Span Registry;
15. I3 Object Extraction;
16. I4 Source Annotation.

Then run ingest-focused reproducibility/coverage fixtures before STRUCTURE depends on them.

## Phase 3 — STRUCTURE
17. S1 Problem Model;
18. S2 Semantic Adjudication;
19. S3 Content Selection & Problem Use;
20. S4 Note Blueprint / Unit Compilation.

Then run E1 Case-IR reproducibility.

## Phase 4 — RENDER
21. operator registry;
22. R1 Unit Realization;
23. R2 Section Composition;
24. R3 Note Assembly.

Then run E2 render/output reproducibility.

## Phase 5 — engineering support
25. CHECK;
26. AUDIT protocol/oracle tooling;
27. BUILD/compiler/conflict lint;
28. deployment package/manifest.

Some support validators may be prototyped earlier when needed by a phase, but their final forms belong to the engineering-support layer.

---

# 14. Important refinement: tests are written before implementation where possible

For each artifact, the acceptance brief should define failure fixtures before DeepSeek writes the implementation.

This is the process equivalent of the architecture's fail-closed principle.

Historical examples must become fixtures, including:
- O51 rule-conflict regression;
- duplicate CT/infarct/family concern;
- apixaban hold/resume split;
- prior plan promoted to current;
- first-person A/P;
- "The MRI to show.";
- missing seizure precautions;
- malformed REUSE/schema;
- silent section/block truncation;
- non-local regression after rule edit.

We should not depend on remembering these failures during later testing.

---

# 15. Division of labor summary

| Task | ChatGPT | DeepSeek | User |
|---|---|---|---|
| Frozen architecture custody | Primary | Challenge | Final authority |
| Acceptance brief | **Author** | Review | Decide if needed |
| Runtime implementation file | Review | **Author** | — |
| Static tests/fixtures | Specify required behavior; review | Implement | — |
| Semantic oracle/acceptance criteria | **Primary** | Review/challenge | Clinical arbiter |
| Doximity run | Analyze | Analyze | **Runs / supplies raw output** |
| Regression interpretation | **Independent reviewer** | **Independent reviewer** | Resolve if needed |
| Consensus update | Draft | Confirm | Final authority |
| Implementation freeze | Recommend | Confirm implementation complete | Final authority when needed |

---

# 16. Process invariant

> **No artifact is both authored and finally accepted by the same LLM.**

And:

> **No implementation file is written before its acceptance obligations and historical failure fixtures are known.**

Those two rules are intended to prevent the engineering process from reproducing the runtime failure mode of a model silently validating its own assumptions.
