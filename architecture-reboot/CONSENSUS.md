# Architecture Reboot V2 — Consensus

## Ratified structural decisions

These points have been explicitly proposed and accepted by both ChatGPT and DeepSeek, or settled by the user.

1. **Production topology is one call / one paste.**
   Chart material and transcription are supplied together; no human carries intermediate artifacts between model calls.

2. **Decompose once and preserve stable source-object identity.**
   Later note construction references objects rather than repeatedly recreating their clinical meaning.

3. **Do not repeatedly reinterpret or destructively route objects.**
   Semantic decisions that affect rendering should not be rediscovered at the final writer.

4. **REASONING is a first-class semantic family.**
   Claim, etiology, qualifier, uncertainty, and adjudication are reasoning roles rather than generic evidence. The exact full top-level kind taxonomy is still open.

5. **Keep semantic structure minimal and evidence-driven.**
   Do not add ontology, relations, stages, or fields without a demonstrated need.

6. **Every render-affecting semantic decision must be explicit before final rendering.**

7. **Render units/operators belong directly in the Case IR.**
   There is no separate model-executed PROJECT stage in the one-call architecture.

8. **Canonical typed operators are first-class for execution.**
   The Doximity B+/operator stress evidence supports explicit operators as the final render boundary.

9. **The operator stress suite validates execution, not selection.**
   Stable 108/108 valid-vs-invalid behavior does not establish that the upstream planner will choose the correct operator/group from raw source material.

10. **Malformed or underspecified render units fail closed.**
    The renderer must not silently repair malformed semantic structure into plausible clinical prose.

11. **Exact diagnostic error labels are secondary.**
    The production invariant is correct valid/invalid classification and fail-closed behavior, not exact error-code wording.

12. **Development modularity and deployment packaging are separate.**
    Source modules may be small and responsibility-specific; deployment should compile to a small Doximity-compatible package.

13. **The deployment build requires conflict linting.**
    It should fail on contradictory rules, duplicate authority over one decision, out-of-scope rules, and untested rules.

14. **Test mode emits an observable Case IR / execution trace.**
    The trace is an auditable artifact, not hidden chain-of-thought and not proof of correctness by itself.

15. **Mechanical validation and semantic fidelity are different jobs.**
    A deterministic checker may verify Case-IR-to-note conformance. Source-to-IR semantic correctness requires a separate semantic audit unless a predicate is genuinely mechanical.

16. **Source temporality and current adoption are separate concepts.**

17. **Current adoption applies to PLAN as well as REASONING when relevant.**
    Historical provenance does not by itself determine whether a recommendation is currently adopted.

18. **Relationship justification uses structured evidence references.**
    Prefer source-span/adjudication references over mandatory free-text rationale.

19. **Source coverage is proposition/span-disposition based, not sentence-count based.**
    The invariant is that clinically meaningful source content does not silently disappear.

20. **Style rules are section-scoped.**
    In particular, final A/P prose uses an impersonal clinical voice; body sections may follow different voice rules.

## Explicitly superseded

- "Each render unit owns exactly one problem" — superseded by A/P-scoped ownership (DC-001 D2).
- S1 output "current problem-level claims" — superseded by candidate proposals plus S2 adjudication (DC-001 D8, D9).

- A separate model-executed `PROJECT` stage after Case State is withdrawn.
- A required free-text `basis` field for semantic relations is withdrawn.
- The earlier large relation wish-list is not adopted.
- The Scribe-primary execution topology in ChatGPT Proposal 002 is void under the user's actual Ask-based one-call workflow.

21. **Mechanical checking is Case-IR-to-note only.**
    A deterministic checker verifies unit references, operator validity, unit↔line mapping, allowed transformations, voice, ordering, and accounting. It does not reconstruct semantic units from objects.

22. **Source-to-Case-IR correctness is a separate semantic audit.**
    Kind, role, problem use, operator selection, duplicate/condition/modifier judgments, and other clinical-semantic choices require semantic review unless a specific predicate is genuinely mechanical.

23. **One source proposition keeps one stable object identity.**
    The same object may be reused explicitly by multiple render units/problems. Do not clone a proposition solely to give it multiple problem homes. An optional primary problem may exist for accounting only.

24. **Object accounting is usage/disposition based.**
    Every object must appear in at least one render unit or carry an explicit disposition. Coverage is not defined as assignment to exactly one problem.

25. **Source spans are mechanically bounded, not semantically atomized.**

    A span is a line, utterance, speaker turn, or equivalent boundary preserved by the paste format. One span may yield multiple objects. Every span has at least one disposition, and every object points back to its source span.

26. **Problem ownership is A/P-scoped.** Body units require no problem; optional association by section contract.
27. **A problem candidate exists only where the subject needs its own current assessment question**, and is source-grounded. S1 owns the candidate partition: each claim candidate maps to exactly one problem candidate.
28. **A claim is a representation** that may carry several claim candidates **belonging to that problem candidate**, together with their relation; the kind vocabulary is downstream.
29. **S1 proposes candidates; S2 adjudicates adoption and claim relations and produces approved claim representations; S3 selects the rendered-problem set and one approved representation per rendered A/P problem; S4 owns final order.**

## Still open

The following are not yet consensus:

- exact top-level kind taxonomy;
- whether `COURSE` remains a separate kind;
- exact canonical operator vocabulary;
- exact field-level Case IR schema;
- exact semantic-audit instrument/test protocol;
- whether Case IR is visible only in test mode or can be hidden/suppressed in production;
- the concrete paste-layout/provenance contract, which depends on an actual example of how chart material + transcript are pasted into Doximity Ask.

## Next decisive experiment

After the remaining schema questions are resolved, test **Case IR reproducibility** from identical raw source material across fresh Doximity runs.

Compare separately:
- object coverage/identity;
- kind/role;
- problem membership/use;
- render-unit membership;
- operator selection;
- member roles;
- order;
- source-span disposition.

Operator/render-unit agreement is a primary metric because prior failures occurred despite stable discovery of the underlying facts.


## Runtime module count — ratified

The production note-generation pipeline has **three logical runtime modules**, all executed within the same single Doximity Ask call:

1. **INGEST** — source material -> stable source-linked semantic objects.
2. **STRUCTURE** — objects -> completed Case IR, including problems, render units, operators, reuse, ordering, and other render-affecting semantic decisions.
3. **RENDER** — completed Case IR -> final note prose.

There is **no fourth runtime module** at present.

A new runtime module should be added only if a distinct responsibility and a separately auditable seam are demonstrated by evidence. Otherwise it belongs inside one of the existing three modules.

The following are **not runtime pipeline steps**:
- **CHECK** — external mechanical IR -> note conformance.
- **AUDIT** — external semantic source -> IR fidelity review.
- **BUILD** — development/deployment compilation and conflict linting.

This distinction is deliberate: three runtime modules, three engineering support systems.


## Submodule interface layer — frozen

The eleven runtime submodules are now agreed at the **interface level**: name, goal, role, input, output, and responsibility boundary.

Canonical artifact:

`architecture-reboot/CONSENSUS_SUBMODULE_INTERFACES_v1.md`

Runtime tree:

1. **INGEST**
   - I1 Source Map
   - I2 Span Registry
   - I3 Object Extraction
   - I4 Source Annotation

2. **STRUCTURE**
   - S1 Problem Model
   - S2 Semantic Adjudication
   - S3 Content Selection & Problem Use
   - S4 Note Blueprint / Render-Unit Compilation

3. **RENDER**
   - R1 Unit Realization
   - R2 Section Composition
   - R3 Note Assembly

Two interface clarifications are included:
- R2 applies only to prose-composed sections and is bounded to non-semantic joining; A/P bypasses R2.
- S4 may emit a zero-member unit only for a closed-list standing item whose explicit trigger conditions are satisfied by structured Case IR/problem state.

The next design layer is **submodule function**. Interface changes require reopening architecture consensus.


## Broad implementation guidance — frozen

ChatGPT and DeepSeek agree on the broad performance/implementation model for all eleven runtime submodules.

Canonical review:
`architecture-reboot/reviews/chatgpt/009-implementation-guidance-freeze.md`

The implementation principle is:

- semantic/contextual decisions -> **LLM_JUDGMENT** under **PROSE_POLICY**;
- closed structural/accounting decisions -> **TYPED_DSL / MECHANICAL_RULE**;
- reproducibility-critical surface realization -> **CANONICAL_OPERATOR**;
- control mode and validation mode are separate dimensions.

Each submodule has an agreed **DO / AVOID / dominant-control** contract.

Additional frozen rules:
- a function that cannot satisfy its own contract fails/flags; it does not widen its remit to perform a neighboring function;
- S4 supports a unit only when all member ids exist and roles are valid for the operator, or when a zero-member unit is an explicitly triggered closed-list standing item;
- ordering is governed by one centralized structured ordering contract, which may contain section-scoped rules; S4 writes the resulting order into the Case IR, and RENDER may not recalculate it.

Exact prompts, DSL syntax, schemas, operator vocabulary, ordering policy details, normalization tables, standing-item catalog, and error taxonomy remain downstream.


## Two-LLM engineering workflow — frozen

The implementation process is now agreed.

Roles:
- **DeepSeek** = primary implementation engineer and author of runtime implementation artifacts.
- **ChatGPT** = architecture custodian, thin acceptance-brief author, regression-obligation owner, and independent implementation reviewer.
- **Signer** = clinical/product authority and actual Doximity runtime operator.

Core process invariants:
- no implementation artifact is finally accepted by the same LLM that authored it;
- no implementation begins before its acceptance obligations are defined;
- BUILD conflict lint begins in Phase 0;
- CHECK is created as soon as the schema/contract it validates exists, before downstream consumers rely on it;
- semantic AUDIT procedure exists from Phase 0, while artifact-specific audit fixtures/oracles mature alongside implementation;
- fixtures/checks/expected properties are controlled artifacts and changes to them are classified as **ACCEPTANCE CHANGE**;
- historical regressions are mandatory baseline fixtures; derived fixtures are allowed only for new invariants and must name the invariant and related historical failure class;
- a minimal vertical slice is tested after shared contracts and before full runtime expansion.

Canonical workflow review:
`architecture-reboot/reviews/chatgpt/012-two-llm-workflow-convergence.md`

DeepSeek confirmation:
`architecture-reboot/reviews/deepseek/014-workflow-freeze.md`


## Doximity experimental protocol — frozen

Doximity testing uses distinct experiment types rather than one universal test format.

### Artifact-level batch
Many independent cases test the same artifact/seam in one fresh conversation. The optimization target is:
> maximize predefined assertions per returned artifact, not checkpoints per case.

### Replicated batch
The exact same frozen batch, same order, is repeated in fresh conversations. Three fresh runs are the default **gate**, not an estimate of a population stability rate. Claims are scoped as "passed 3/3 under this frozen condition."

### Diagnostic single-case trace
A failed/ambiguous case may be rerun with richer checkpoint visibility to localize a candidate first divergence. Because trace output changes the requested task, **trace runs are diagnostic only and can never satisfy an acceptance criterion.**

### Robustness/batching test
After same-order variance is characterized, test:
- fixed order permutations;
- selected single-case controls;
- early/middle/late position effects.

Additional frozen rules:
- Doximity does not self-grade with PASS/CORRECT; external CHECK/AUDIT scores outputs;
- if runtime failure output is needed, use a single generic `CONTRACT_ERROR` rather than a nuanced model-generated taxonomy;
- every scored assertion has exactly one owning submodule; if a property spans modules, split it into separate assertions;
- realistic reference cases consist of source package + signer-approved target note; structured assertions are derived by the agents and only ambiguous semantic points are escalated to the signer;
- scorer negative controls are offline mutated artifacts; runtime invalid probes are separate Doximity tests of fail-closed behavior;
- batch-size/output limits are empirical, not fixed by an arbitrary byte threshold;
- raw Doximity outputs are immutable evidence.

Canonical protocol:
`architecture-reboot/proposals/chatgpt/009-doximity-experimental-protocol.md`

Convergence review:
`architecture-reboot/reviews/chatgpt/013-doximity-protocol-convergence.md`

DeepSeek confirmation:
`architecture-reboot/reviews/deepseek/016-protocol-freeze.md`
