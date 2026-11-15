# ChatGPT review 006 — internal functions, control mode, and checkability

## Verdict

DeepSeek's internal-function pass is a strong first draft, but it mixes two distinct design questions:

1. **Control mode** — how Doximity should be instructed to make/execute the decision.
2. **Validation mode** — how we can verify the result afterward.

These must remain separate.

A decision can be:
- made by LLM semantic judgment;
- constrained to a typed DSL output;
- mechanically checked for structural conformance;
- while its clinical correctness remains semantic/audit-only.

Duplicate identity is the clearest example.

---

# 1. Two-axis model

For every internal function, record both:

## A. Control mode
- **L** = general LLM semantic capability
- **P** = precise prose policy/boundary
- **D** = pseudocode / typed DSL / canonical operator

Most functions are hybrids.

## B. Validation mode
- **M** = mechanically verifiable
- **S** = semantic audit required
- **H** = hybrid: some predicates mechanical, core correctness semantic

Do not infer one axis from the other.

Example:

```text
Duplicate identity
CONTROL: L + P + D
  - LLM judges semantic equivalence
  - prose defines what SAME means
  - DSL forces SAME / DISTINCT / UNRESOLVED and object IDs

VALIDATION:
  - M: one canonical, no double membership, coverage accounting
  - S: whether the two propositions really are equivalent
```

Typed representation does not make the underlying clinical judgment mechanical.

---

# 2. S1 -> S2 sequencing

I do **not** recommend a feedback loop or early dedup.

The apparent dependency is weaker than DeepSeek frames it.

S1 should group by **clinical subject/problem concept**, not by unique-fact count.

Two duplicate seizure statements from different sources should naturally enter the same seizure problem candidate even before S2 decides they are duplicates.

Therefore:

### S1
- identify problem/claim candidates from object meaning;
- multiplicity of similar objects is not evidence of multiple problems;
- do not decide duplicate identity.

### S2
- resolve duplicate/related/distinct relationships among objects already considered within the problem framework;
- may flag a `PROBLEM_MODEL_CONFLICT` if adjudication reveals that the S1 problem model is internally inconsistent.

### Failure behavior
Do not silently loop S2 back into S1 in production logic.

If a genuinely material split/merge conflict is found, the Case IR should fail/flag at STRUCTURE rather than hide a recursive reinterpretation step.

Why:
- preserves the frozen acyclic architecture;
- preserves one owner per decision;
- makes problem-model error observable rather than recursively rewritten.

If E1 shows systematic S1 failures that S2 could reliably repair, then we can reopen the interface with evidence.

---

# 3. DeepSeek's checkability labels need revisions

## I1 Source Map
DeepSeek tags source classification as **M**.

I disagree.

Mechanical:
- complete character/block coverage;
- no overlap;
- order preservation.

Semantic:
- whether an unlabeled block is truly a prior neurology note vs current H&P vs transcript.

So I1 is **H**, not purely M.

## I2 Span Registry
Mostly **M** if boundaries are restricted to mechanical delimiters. Agreed.

## I3 Object Extraction
DeepSeek's proposed strongest check is:

> object text must be a substring of its span.

I do not accept that as the invariant.

It would prohibit useful source-faithful normalization such as:
- resolving pronouns;
- removing filler;
- converting a spoken clause into a concise proposition;
- separating one utterance into multiple propositions.

The frozen interface requires a **source-faithful proposition**, not necessarily a verbatim substring.

Better design:

> every object must cite an exact source evidence anchor/span; any normalized proposition must add no unsupported semantic payload.

Mechanical:
- object has valid source/span;
- optional exact evidence anchor is a substring.

Semantic:
- normalized proposition faithfully represents that evidence.

So I3 remains **H**, not reducible to a substring validator.

## I4 Source Annotation
Not fully M.

Mechanical:
- source/span IDs;
- exact copied dates;
- explicit named speaker;
- allowed enum values.

Semantic/partial:
- source family if inferred;
- some temporality distinctions when the paste is ambiguous;
- whether a statement is an explicit adoption signal.

So **H**.

## S1 Problem Model
Semantic. Agreed.

Mechanical shell:
- required problem fields;
- exactly one current claim representation per retained problem if contract requires it.

Correctness remains semantic.

## S2 Duplicate Identity
DeepSeek says "can never be mechanical."

Revise to:

> **General duplicate identity is semantic; a safe subset may be mechanically decidable.**

Examples of mechanical/near-mechanical subset:
- exact normalized text + same referent + same value + same time/source context;
- explicit source duplication.

Ambiguous equivalence remains semantic.

Do not freeze "never."

## S2 Adoption
Hybrid. Agreed.

Explicit current clinician adoption may sometimes be rule-resolvable; implicit adoption remains semantic.

## S3 Selection / Problem Use
Accounting is M; relevance/problem fit is semantic.

So H overall.

## S4 Unit Compilation
Mostly D-controlled and heavily mechanically checkable, but **operator selection itself may remain semantic** until evidence shows otherwise.

Important distinction:
- unit typechecks = M;
- correct operator chosen = semantic/hybrid.

## R1 Unit Realization
Given a canonical operator, this is the strongest M region. Agreed.

## R2 Section Composition
DeepSeek tags this M.

I would tag **H/P**, not fully M.

Mechanical:
- unit order;
- no unit deletion;
- presence of each payload.

Semantic:
- whether a connective subtly changes temporal/causal meaning;
- whether joining creates a new proposition.

The boundary can be strongly constrained, but semantic preservation is not always mechanically provable.

## R3 Note Assembly
M. Agreed.

---

# 4. "Roughly a fifth" is not an architecture fact

Do not freeze:
- 80% mechanical;
- 20% semantic;
- "permanently audit-only."

We have not measured that.

Instead, every function should carry:
- control-mode tags;
- validation-mode tags.

After E1/E2, we can report the observed proportion of decisions that:
- passed mechanical validation;
- required semantic audit;
- showed run-to-run drift.

The size of the semantic remainder is an empirical result.

---

# 5. "Never mechanical" should become "not generally mechanical"

Architecture wording should be:

> Some Case-IR decisions, especially problem formulation, semantic equivalence, relevance, and adoption, require contextual clinical judgment and therefore cannot be assumed mechanically decidable in the general case. Mechanize the safely rule-resolvable subset; represent the residual judgment explicitly; audit it semantically; measure its reproducibility.

This preserves honesty without prematurely declaring a permanent irreducible fraction.

---

# 6. Function-control allocation

I still support the qualitative allocation from ChatGPT Proposal 007:

| Submodule | Primary control pattern |
|---|---|
| I1 Source Map | LLM recognition + prose boundaries + light DSL accounting |
| I2 Span Registry | pseudocode/mechanical |
| I3 Object Extraction | LLM semantic extraction + prose fidelity + light accounting DSL |
| I4 Source Annotation | prose definitions + structured copying/DSL |
| S1 Problem Model | LLM clinical reasoning + strong prose policy |
| S2 Semantic Adjudication | LLM judgment + precise prose + typed relation output |
| S3 Selection & Problem Use | LLM relevance judgment + prose policy + deterministic accounting shell |
| S4 Blueprint / Unit Compilation | typed DSL/pseudocode dominant; LLM only where operator/section selection remains semantic |
| R1 Unit Realization | canonical operators / DSL dominant |
| R2 Section Composition | LLM language ability inside hard prose guards + mechanical order/coverage shell |
| R3 Note Assembly | pseudocode/mechanical |

Do not freeze numeric percentages.

---

# 7. Functions I accept from DeepSeek 005

At a high level, I accept the 3–5 operations for:
- I1;
- I2;
- I4;
- S3;
- S4;
- R1;
- R2;
- R3.

I accept I3 with one correction:
- source-faithful normalization is allowed;
- exact source evidence anchoring is required;
- normalized object text need not itself be a literal substring.

I accept S1 with the sequencing clarification in §2.

I accept S2 with the wording change:
- duplicate identity is semantic in the general case;
- mechanize only safe subsets;
- unresolved ambiguity may remain explicit rather than forced.

---

# 8. What should be agreed next

Before writing production prompts, freeze for each submodule:

1. its numbered internal functions;
2. control mode for each function: L / P / D;
3. validation mode for each function: M / S / H;
4. failure behavior.

Then write the actual prose/pseudocode.

That gives us a disciplined specification instead of treating "pseudocode" as synonymous with "deterministic."
