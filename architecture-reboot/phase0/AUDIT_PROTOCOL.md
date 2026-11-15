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

Used for: the first run of a new case, any run offered as acceptance evidence, any run under dispute.

**The implementer's rationale is never an input in either mode.** It makes the reviewer agree with the author.

## 3. What the auditor does

The order below is the default. It is a sequence of questions, not a fixed rubric: the reviewer answers the ones that apply, adds case-specific questions where warranted, and records which were not answerable and why.

1. **Coverage** — does every source span have a disposition, and every object a span?
2. **Fidelity** — is every object's content supported by its span?
3. **Problem model** — does every problem have a claim, and are any two problems the same thing?
4. **Duplicate identity** — does any fact render twice within one section and problem?
5. **Adoption** — is any prior recommendation presented as current, or a current one buried?
6. **Placement** — is each object used under the problem it explains?
7. **Operator fit** — does the chosen operator render the payload it was given?
8. **Completeness** — does every required line exist?
9. **Voice and format** — section-scoped style?
10. **Note as a whole** — sections in order, nothing invented between them?

Do not stop at the first failure. Record every question answerable and every failure found; a batch that returns one failure per run wastes the run.

Stop early only when a failure makes later questions uninterpretable, and state why: coverage wrong → fidelity unanswerable; IR malformed → operator fit unanswerable; source incomplete → nothing downstream trustworthy.

## 4. What is recorded

```text
CHECK 4  duplicate identity
RESULT   FAIL
EVIDENCE O7 and O44 share a proposition; U3 and U9 both render it
SPAN     S12
OWNER    STRUCTURE / S2
MODE     B
```

Five fields plus the mode. The owner is a submodule, not a person.

## 5. Sign-off

`ACCEPT` — every answerable question passed.
`REJECT` — at least one failed, with the full list of independent failures.
`BLOCKED` — the audit could not proceed, with the stopping reason.

A Mode A audit may reject or report, but may not sign an acceptance decision. Acceptance requires Mode B.

## 6. When the reviewer cannot decide

Escalate to the signer. Do not average, hedge, or accept with reservations. An unresolved question recorded as "probably fine" becomes a fixture and then a standard.

## 7. What this protocol must not contain

- expected clinical content for any case — that is a fixture;
- a scoring formula — that is the batch protocol;
- criteria invented after seeing the implementation — that is drift.

## 8. Who audits

Any reviewer who did not write the artifact. An agent auditing its own output is not an audit.
