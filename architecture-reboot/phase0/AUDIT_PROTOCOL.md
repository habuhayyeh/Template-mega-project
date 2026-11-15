# AUDIT_PROTOCOL — how semantic correctness is judged

This is a procedure. It says who looks at what, in what order they look, and what they record. It does not contain clinical expectations for any case: those live in fixtures, and fixtures live in evidence.

## 1. Why this exists

The mechanical checker can prove the note matches the Case IR. It cannot prove the IR matches the encounter. That gap is audited by a reviewer, and the procedure is fixed in advance so the criteria do not drift toward whatever got built.

## 2. Two audit modes

The auditor is not always given everything. Which inputs exist determines which questions are answerable.

### Mode A — artifact audit

The reviewer has the returned artifact and the frozen assertions for the case.

Inputs: the artifact; the fixture assertions (**properties only, never expected prose**).

Answerable: consistency, placement, completeness, voice.

Not answerable: whether the IR is faithful to a source the reviewer cannot see.

Used for: batch volume.

### Mode B — full audit

Inputs: artifact; Case IR; source package; check report; fixture assertions.

Answerable: everything, including fidelity and coverage.

Used for: the first run of a new case, any run whose assertions need source visibility to decide, any run under dispute.

**The implementer's rationale is never an input in either mode.** It makes the reviewer agree with the author.

## 3. What the auditor does

The audit is driven by the fixture's **declared assertions**, not by a fixed checklist.

Each assertion belongs to one seam (coverage, fidelity, problem model, duplicate identity, adoption, placement, operator fit, completeness, voice, whole-note). The auditor takes the assertions declared for this case, groups them by seam, and answers each one.

If an assertion cannot be decided from the evidence available in this mode, it is recorded as `UNDECIDABLE` with the reason. It is not answered from expectation.

The auditor may add a case-specific assertion when the case shows something the declared set does not cover; the addition is recorded and, if it proves general, promoted through `ACCEPTANCE CHANGE`.

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

`ACCEPT` — every answerable question passed.
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

Any reviewer who did not write the artifact. An agent auditing its own output is not an audit.
