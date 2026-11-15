# DeepSeek review — File B problem architecture contract

**Reviewed:** `02-PROBLEM-ARCHITECTURE.md`.
**Status:** architecture review; no implementation.

## Verdict

**Accept with two boundary fixes.** The contract owns the right decisions and stays out of C. The tiny
packet exposes two gaps that need fixing before the test.

## Fix 1 — add an architecture-unresolved lane

The contract says sparse evidence should produce a sparse map, but the output format has no way to say:

> the packet is insufficient to establish a problem, a role, or a relationship.

Per-problem `unresolved` only works after a problem exists. On the three-record packet, B may be forced to
invent a problem just to have somewhere to put uncertainty.

Add:

```text
ARCHITECTURE_UNRESOLVED
  topic=<...>
  evidence=<record IDs + selectors>
  issue=<what cannot be decided>
```

Use it when:

- no problem threshold is met;
- encounter role cannot be decided;
- problem identity is plausible but not established;
- a relationship is suspected but unsupported.

Do not turn it into a differential or a note section.

## Fix 2 — B may not repair A

The contract says B may resolve an A `UNRESOLVED` if the packet supplies evidence A failed to carry. That
is a loophole: B can silently rewrite A's semantic layer.

Change to:

- B may reread the canonical packet to evaluate problem identity, containment, role and relations.
- B may not change A's polarity, time, attribution, certainty, event identity or action state.
- If B finds that A omitted material evidence, B must add an `ARCHITECTURE_UNRESOLVED` item and flag it
  back to A; it must not repair A inside the problem map.

## Fix 3 — clarify `adoption` vs `encounter_role`

These fields overlap. State the combinations explicitly:

- `historical` + `BACKGROUND` is valid;
- `current_adopted` + `PRIMARY` is valid;
- `reported` + `unresolved` is valid;
- `historical` + `PRIMARY` requires current independent evaluation/management evidence.

Do not let `adoption` silently become the role.

## What is right

- candidate-problem threshold;
- disease-centered vs syndrome-centered;
- containment;
- distinct downstream disorder;
- multifactorial syndrome;
- PRIMARY/BACKGROUND separate from severity;
- role evidence required;
- source-supported causality only;
- action ownership without changing action state;
- nonproblem evidence preserved for C;
- no section/prose/final-plan decisions;
- no forced problem count.

## Test after fixes

Use the existing three-record A output. Expected:

- no forced problem if the packet does not establish a current assessment question;
- historical stroke may be `BACKGROUND` or `ARCHITECTURE_UNRESOLVED`, but not current/PRIMARY;
- falls must not be automatically linked to stroke or declared the consult reason;
- no residual deficit, action, section or prose;
- any uncertainty goes in `ARCHITECTURE_UNRESOLVED`, not a fake problem.

No C, renderer, validator or note. No Gate-0 acceptance. No Doximity production change. No Phase 0.
