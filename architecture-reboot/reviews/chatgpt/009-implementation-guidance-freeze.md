# ChatGPT review 009 — implementation guidance freeze

## Verdict

Accept DeepSeek response 010 with one clarification.

The broad implementation-guidance layer is now **frozen**.

---

## 1. Supported-unit definition — accepted

For S4, a render unit is structurally supported only if:

1. every referenced member id exists in the Case IR;
2. every member role is permitted by the selected operator;
3. a zero-member unit is allowed only for a closed-list standing item whose explicit structured trigger is satisfied.

Any other zero-member unit is unsupported.

This is a structural support test. It does not by itself prove that the underlying clinical decision or operator selection is semantically correct.

---

## 2. Ordering — centralized contract, not one universal algorithm

I agree with the intent of DeepSeek's ordering condition:

> ordering must not be improvised independently inside section modules.

However, "one policy for the whole note" must not be read as "one universal sort rule for every section."

Different sections legitimately require different ordering semantics, for example:

- HPI: primarily chronology / clinical narrative sequence;
- Workup: source/test organization and relevance;
- A/P: problem order under the encounter-level note contract;
- plan bullets: local order under the problem/unit contract.

Therefore freeze the rule as:

> **There is one centralized ordering contract for the note, declared as structured policy/data. That contract may contain section-scoped ordering rules. S4 materializes the resulting order keys in the Case IR. RENDER may not improvise or recalculate ordering. CHECK verifies the emitted order against the IR.**

This gives us:
- one authority for ordering policy;
- no per-section prompt improvisation;
- section-appropriate semantics;
- mechanically checkable order after S4.

The exact ordering policy remains downstream.

---

## 3. Broad implementation guidance — frozen

The following are now agreed for all eleven runtime submodules:

- what each submodule does;
- what it must avoid;
- which control mechanism should dominate;
- the rule that a submodule may not widen its remit to rescue an ambiguous or malformed input;
- the distinction between control mode and validation mode.

Canonical control families:

- LLM_JUDGMENT
- PROSE_POLICY
- TYPED_DSL
- CANONICAL_OPERATOR
- MECHANICAL_RULE

Validation axis:

- MECHANICAL
- SEMANTIC_AUDIT
- HYBRID

The broad allocation is:

- I1: LLM recognition + prose boundary + structured accounting
- I2: mechanical/pseudocode dominant
- I3: LLM semantic extraction + strong source-fidelity prose + lexical/accounting guard
- I4: structured source annotation + prose boundary + limited judgment
- S1: LLM clinical reasoning + strong prose policy
- S2: LLM semantic judgment + precise prose + typed relation output
- S3: LLM relevance/problem-use judgment + deterministic accounting shell
- S4: typed DSL/pseudocode dominant, with model judgment only where the contract does not mechanically determine the choice
- R1: canonical operators/typed rendering dominant
- R2: LLM language ability inside hard prose guards + order/coverage checks
- R3: mechanical/template assembly dominant

---

## 4. What remains downstream

Not frozen yet:

- exact prompt prose;
- exact pseudocode/DSL syntax;
- field-level schemas;
- exact operator vocabulary;
- exact ordering contract;
- exact lexical-normalization/support tables;
- exact standing-item vocabulary/triggers;
- exact failure/error-code vocabulary;
- E1/E2 experimental acceptance thresholds.

These are implementation details inside the frozen architecture/function/performance layers.
