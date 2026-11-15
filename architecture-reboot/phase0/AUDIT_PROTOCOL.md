# AUDIT_PROTOCOL — how semantic correctness is judged

This is a procedure. It says who looks at what, in what order they look, and what they record. It does not contain clinical expectations for any case: those live in fixtures, and fixtures live in evidence.

## 1. Why this exists

The mechanical checker proves the **declared mechanically decidable** predicates on IR→note conformance. It does not prove all conformance, and it cannot prove the IR matches the encounter. Both gaps are this protocol's job. That gap is audited by a reviewer, and the procedure is fixed in advance so the criteria do not drift toward whatever got built.

## 2. Two audit modes

The auditor is not always given everything. Which inputs exist determines which questions are answerable.

### Mode A — artifact audit

The reviewer has the returned artifact and the frozen assertions for the case.

Inputs: the artifact; the fixture assertions (**properties only, never expected prose**).

Answerability here is per assertion, not per mode: an assertion is answerable if the available evidence settles it. Nothing is answerable merely because of the mode, and nothing is barred merely because of it.

Used for: batch volume, where the source is large and most assertions concern the artifact itself.

### Mode B — full audit

Inputs: the artifact; the fixture assertions; and whichever of source package, Case IR or check report the assertions under review require. The Case IR is included only where an assertion concerns it.

Answerability is again per assertion: source-dependent assertions become decidable here, and the rest are decided as in Mode A.

Used for: the first run of a new case, any run whose assertions need source visibility, any run under dispute.

**The implementer's rationale is never an input in either mode.** It makes the reviewer agree with the author.

## 3. What the auditor does

The audit is driven by the fixture's **declared assertions**, not by a fixed checklist.

Each assertion belongs to one seam (coverage, fidelity, problem model, duplicate identity, adoption, placement, operator fit, completeness, voice, whole-note). The auditor takes the assertions declared for this case, groups them by seam, and answers each one.

If an assertion cannot be decided from the evidence available in this mode, it is recorded as `UNDECIDABLE` with the reason. It is not answered from expectation.

A finding not covered by any frozen assertion is recorded as **`DISCOVERY`, not an assertion**. It does not score, cannot be applied retroactively, and enters the record only by becoming an `ACCEPTANCE CHANGE` followed by a rerun.

This replaces an earlier allowance that an auditor could add assertions after seeing the output — that allowance was post-hoc goalpost movement with a procedural name.

Do not stop at the first failure. Record every assertion answerable and every failure found; a batch returning one failure per run wastes the run. Stop early only when a failure makes later assertions uninterpretable, and state why.

## 4. What is recorded

```text
CHECK 4  duplicate identity
RESULT   FAIL
EVIDENCE O7 and O44 share a proposition; U3 and U9 both render it
SPAN     S12
OWNER    S2
MODE     B
```

Five fields plus the mode. The owner is a submodule, not a person.

## 5. Sign-off

`ACCEPT` — every **required** assertion was decidable and passed. An undecidable required assertion blocks acceptance; it does not lower information.
`REJECT` — at least one failed, with the full list of independent failures.
`BLOCKED` — the audit could not proceed, with the stopping reason.

Either mode may sign acceptance **if every declared assertion for that case is decidable from the evidence available in it**. If any is `UNDECIDABLE`, the audit cannot accept, whatever the mode.

## 6. When the reviewer cannot decide

Escalate to the signer. Do not average, hedge, or accept with reservations. An unresolved question recorded as "probably fine" becomes a fixture and then a standard.

## 7. What this protocol must not contain

- expected clinical content for any case — that is a fixture;
- a scoring formula — that is the batch protocol;
- criteria invented after seeing the implementation — that is drift.

## 8. Who audits

The primary acceptance reviewer must be **independent of the implementation author**. The author may act as a secondary challenger or scorer, never as the primary judge.

Independence is about authorship of the implementation, not of the text: an agent that did not type the note but did design the module is not independent.
