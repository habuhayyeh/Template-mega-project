# Scribe Quirks

## Purpose

This folder is the working handbook for writing prompts and execution contracts for the Doximity GPT-4o engine used in this project.

It records **observed engine behavior**, not general LLM folklore.

Use it when designing or revising:

- Scribe ingestion prompts;
- Ask semantic modules;
- compiler/blueprint contracts;
- render operators;
- internal logical phases within one Ask invocation;
- Doximity experiments.

Do not treat every rule here as a universal model law. Each rule is tagged by the evidence that produced it.

## Core operating model

The strongest evidence supports this division:

```text
SOURCE-LOCAL FUNCTIONS
  preserve boundaries
  de-noise
  split source-local complexity
  preserve source-supported state
        |
        v
WHOLE-PACKET FUNCTIONS
  coverage census
  action census
  completeness audit
        |
        v
CLINICAL SYNTHESIS
  reconcile sources
  build problems
  decide diagnostic stance
  reconcile actions
        |
        v
COMPILER
  choose typed groups
  assign rhetorical class
  assign roles
  assign canonical operator
  assign order
        |
        v
RENDERER
  execute operator
  fail closed on malformed input
```

The engine performs best when each layer receives a **decision-complete input for the function it owns**.

## Highest-confidence engine rules

1. Put a hard **read-all / no-emission gate** at the beginning of long prompts.
2. Write functions as **short atomic imperatives**, not long explanatory prose.
3. Separate **READ -> EXTRACT -> DECIDE -> CHECK -> EMIT**.
4. Do not let the model draft while still reading instructions.
5. Make later semantic decisions explicit upstream rather than asking a later writer to rediscover them.
6. Avoid schemas that invite the model to fill unsupported slots.
7. Exact copied selectors are unreliable during simultaneous synthesis; prefer stable source record IDs where possible.
8. Same-context LLM validation can execute visibly and still false-pass obvious semantic errors.
9. Do not use the same model to generate a semantic claim and then trust it to independently validate that claim in the same context.
10. Typed groups + canonical render operators can be highly reproducible when the semantic payload is complete.
11. Stable bad output is usually a **contract/input defect**, not stochasticity.
12. Malformed render structures should fail closed; the renderer should not repair them.
13. Error-label taxonomy matters less than preserving the valid/invalid boundary.
14. Coverage enumeration and synthesis compete. If synthesis repeatedly omits material evidence, perform a dedicated coverage census before synthesis.
15. The useful unit of modularity is a **function boundary**, not necessarily a separate file or separate model call.
16. Use **JSON** for model-authored structured handoffs. Do not use custom `@@` output records.
17. Do not use `|` as a delimiter. Doximity renders pipe-delimited records as Markdown tables.
18. `@@PACKET` / `@@SOURCE` / `@@END` in the Scribe input packet are input framing, not an output format to copy downstream.
19. JSON is canonical for structured handoffs. CSV is acceptable for the flat coverage census or review export, not as the synthesis source of truth. YAML is not recommended for nested handoffs.
20. Doximity Ask does not execute code. Put all executable logic outside the model.
21. Clinical reference checks run after synthesis, not during coverage. They are not packet evidence and cannot add patient facts.
22. Free semantic synthesis is not deterministic. Test fixed invariants or a frozen JSON, not exact labels.
23. D-S/D-T are deterministic only on a frozen facts JSON with explicit `order` and fixed templates.
24. A baseline/prior pattern is never a separate problem; it is a `baseline_comparator` unit under the problem it informs.
25. `contains` and `separate_from` are problem handles only and stay empty when no separate problem exists.
26. Attach the Scribe packet for attachment tests; Doximity can read it.
27. In-prompt handoff requires a fixed Stage A schema, full payload, a sentinel, and a Stage B ban on rereading source facts.
28. Keep a negative-results log. A handbook of passes alone overstates reliability.
29. Every test entry must reference the exact prompt file and state the run count. If either is missing, mark it unverified.
30. With two attachments, identify each by content marker, not attachment order. One file defines functions; the other contains calls.
31. Avoid `<...>` in model output; it can be stripped as HTML. Treat `[...]` as risky too.
32. JSON determinism is semantic, not byte-level. Whitespace varies between runs.
33. Diagnose a spec defect before a model failure: exact shape, gold, field count, fallback rule, sentinel, order and run count.

## Files

- [01-PROMPT-WRITING-STYLE.md](01-PROMPT-WRITING-STYLE.md)  
  Canonical prompt-writing style for Doximity.

- [02-BPLUS-RENDER-RULES.md](02-BPLUS-RENDER-RULES.md)  
  Preserved B+ typed-group/operator rules and the important bugs they exposed.

- [03-EXPERIMENT-TO-RULE-LEDGER.md](03-EXPERIMENT-TO-RULE-LEDGER.md)  
  Test-by-test evidence ledger and the rule derived from each experiment.

- [04-FUNCTION-PLACEMENT.md](04-FUNCTION-PLACEMENT.md)  
  Which functions must be source-local, which belong to a whole-packet pass, and which must remain downstream.

- [05-DOXIMITY-CONTRACT-CHECKLIST.md](05-DOXIMITY-CONTRACT-CHECKLIST.md)  
  Compact checklist for writing or reviewing a new Doximity module.

- [06-SERIALIZATION-AND-SENTINELS.md](06-SERIALIZATION-AND-SENTINELS.md)  
  Reproduced finding: custom `@@` output records collapse/truncate; JSON handoffs work; pipes become tables.

- [07-STRUCTURED-FORMATS.md](07-STRUCTURED-FORMATS.md)  
  JSON vs CSV vs YAML for coverage and synthesis handoffs.

- [08-NO-CODE-EXECUTION.md](08-NO-CODE-EXECUTION.md)  
  Reproduced finding: Ask does not run code; executable logic stays outside.

- [09-CLINICAL-REFERENCE-CHECK.md](09-CLINICAL-REFERENCE-CHECK.md)  
  Post-synthesis drug monograph and literature checks, with example prompts.

- [10-SYNTHESIS-AND-DSDT.md](10-SYNTHESIS-AND-DSDT.md)  
  Why free synthesis drifts; constrained invariants; D-S/D-T determinism; attachment results.

- [11-IN-PROMPT-HANDOFF.md](11-IN-PROMPT-HANDOFF.md)  
  Strict Stage A -> Stage B handoff with sentinel and no source fallback.

- [12-NEGATIVE-RESULTS.md](12-NEGATIVE-RESULTS.md)  
  Failed runs, invalid tests and test-design bugs kept alongside the passes.

- [13-TEST-PROMPT-TRACEABILITY.md](13-TEST-PROMPT-TRACEABILITY.md)  
  Test-to-prompt map with run counts, observed results and unverified items.

- [14-TWO-ATTACHMENT-HANDOFF.md](14-TWO-ATTACHMENT-HANDOFF.md)  
  Function-library and call-script attachments: what worked, bracket stripping and JSON whitespace.

- [15-FAILURE-MODES.md](15-FAILURE-MODES.md)  
  Eight recurring failure modes: how they happened, why, diagnosis and prevention.

## Evidence classes

### REPRODUCED

Observed in repeated fresh Doximity conversations or across multiple independent experiments.

### OBSERVED

Observed in at least one valid Doximity execution.

### DESIGN CONSEQUENCE

An architecture choice supported by observed behavior but not itself directly tested.

### REJECTED PATTERN

A pattern that produced repeated material failures.

## Scope rule

Only promote a quirk into a durable rule when:

- it was directly observed;
- or multiple experiments converge on the same mechanism;
- or a controlled comparison isolates the behavior.

Do not turn one malformed run, stale prompt execution, or invalid control condition into an engine rule.
