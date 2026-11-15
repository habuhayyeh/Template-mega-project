# AUDIT_PROTOCOL — how semantic correctness is judged

This is a procedure, not a rubric. It says who looks at what, in what order, and what they record. It deliberately does not list expected clinical outcomes for any case: those live in fixtures, and fixtures live in evidence.

## 1. Why this exists

The mechanical checker can prove that the note matches the Case IR. It cannot prove the IR matches the encounter. That gap is audited by a person or an independent reviewer, and the procedure is fixed in advance so the criteria do not drift toward whatever got built.

## 2. Inputs

The auditor receives exactly these, and nothing else:

1. the source package as the signer pasted it;
2. the Case IR (test mode);
3. the final note;
4. the check report.

The auditor does not receive the implementer's rationale, the brief, or the design discussion. Those make an auditor agree with the author.

## 3. Order of checks

Fixed order. Stop at the first failure and record it; do not continue to build a fuller picture, because the first failure is the one that gets fixed.

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
- `REJECT` — at least one check failed, with evidence;
- `BLOCKED` — the auditor cannot decide, with the reason.

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
