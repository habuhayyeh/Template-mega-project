# AUDIT_PROTOCOL — how semantic correctness is judged

This is a procedure, not a rubric. It says who looks at what, in what order, and what they record. It deliberately does not list expected clinical outcomes for any case: those live in fixtures, and fixtures live in evidence.

## 1. Why this exists

The mechanical checker can prove that the note matches the Case IR. It cannot prove the IR matches the encounter. That gap is audited by a person or an independent reviewer, and the procedure is fixed in advance so the criteria do not drift toward whatever got built.

## 2. Inputs

The auditor receives exactly these, and nothing else:

1. the source package as the signer pasted it;
2. the Case IR (test mode);
3. the final note;
4. the check report;
5. the frozen fixture assertions for this case — **properties only, never expected prose**.

The auditor is not always given source, IR and note. For artifact-level batches the audit works from the returned artifact plus the frozen assertions. What is never given is the implementer's rationale.

The auditor does not receive the implementer's rationale, the brief, or the design discussion. Those make an auditor agree with the author.

## 3. Order of checks

Fixed order, but **do not stop at the first failure**. Record every check that fails and can still be interpreted independently.

The batch is expensive and its value is the failure picture; an audit that returns one failure per run wastes the run. Order matters for attribution, not for stopping: the earliest failed check names the owning submodule.

Stop early only when a failure makes later checks uninterpretable, and state the reason:

- coverage wrong → fidelity cannot be assessed;
- IR malformed → operator fit is meaningless;
- source package incomplete → nothing downstream is trustworthy.

1. **Coverage** — every source span has a disposition; every object traces to a span.
2. **Fidelity** — every object's content is supported by its span. Any word not supported is a finding, regardless of plausibility.
3. **Problem model** — every problem has a claim; no two problems describe the same clinical thing.
4. **Duplicate identity** — no fact is rendered twice within a section and problem; every duplicate group has one canonical.
5. **Adoption** — no prior recommendation is presented as current without a statement; no current one is buried as historical.
6. **Placement** — each object is used under the problem it explains, not the one that merely mentions it.
7. **Operator fit** — the chosen operator renders the payload it was given. A line thinner than its head is a finding.
8. **Completeness** — every required line exists; standing items present where triggered.
9. **Voice and format** — section-scoped style; A/P impersonal.
10. **Note as a whole** — sections in order, nothing invented between them, nothing missing.

## 4. What the auditor records for each check

```text
CHECK 4  duplicate identity
RESULT   FAIL
EVIDENCE object O7 and O44 share the same proposition; units U3 and U9 both render it
SPAN     S12
OWNER    STRUCTURE / S2
```

Five fields: check, result, evidence, span, owner. The owner is the submodule, not a person.

## 5. Sign-off

A case is audited when every check has a result and every failure has an owner and evidence. "Signed" means the auditor states one of:

- `ACCEPT` — every check passed;
- `REJECT` — at least one check failed, with the full list of independent failures;
- `BLOCKED` — the audit could not proceed, with the stopping reason.

A `REJECT` lists every independent failure, not the first one.

## 6. When the auditor cannot decide

The auditor escalates to the signer. They do not average, hedge, or accept with reservations. An unresolved semantic question recorded as "probably fine" is how a wrong claim enters the corpus and becomes a fixture.

## 7. What this protocol must not contain

- expected clinical content for any case (that is a fixture);
- a scoring formula (that is the batch protocol);
- criteria invented after seeing an implementation (that is drift).

## 8. Who audits

Any reviewer who did not write the artifact. For signer-facing cases, the signer decides; for engineering cases, the reviewing agent decides. An agent auditing its own output is not an audit.

## 9. Cost

Ten checks per case. Most pass in seconds. The expensive ones are 3 and 4, and they are the ones worth the time — they are the failures that reached output most often.
