# DeepSeek response 014 — accepted, with one caveat on the audit protocol

**Answer: yes to both refinements.** The caveat is about what the Phase 0 audit protocol is allowed to contain.

---

## 1. AUDIT protocol at Phase 0 — accepted, with a distinction

Agreed that the protocol must exist before implementation, or the semantic criteria get written to fit whatever got built.

But a protocol written at Phase 0 has a hazard: if it lists expected outcomes, it becomes a second specification written before the artifact exists, and it will be wrong in the place that matters — the case nobody imagined.

So the Phase 0 artifact should be a **procedure, not a rubric**:

- what the auditor receives (source spans, the IR, the note);
- what they must check, in order (coverage, adoption, duplicate identity, operator fit);
- what evidence they record for each check;
- who signs, and what "signed" means;
- what happens when the auditor cannot decide — escalate, do not average.

What it must not contain at Phase 0: a list of expected clinical outcomes for a case. Those belong to fixtures, and fixtures belong to evidence.

## 2. Brief shape — accepted

`CONTRACT REFERENCES + FIXTURES + REQUIRED ARTIFACT PROPERTIES + DECIDING CHECKS + EXPECTED FAILURE BEHAVIOR` is better than my "IR properties" and I withdraw that narrower version.

One note on the last field: expected failure behaviour should name the **failure class** from the ten-plus-four list, not just describe the bad output. "Reject, do not repair" is a behaviour; `C13 over-inclusion` is what makes it auditable later.

## 3. Fixtures — accepted, with one tightening

Historical failures mandatory; derived boundary fixtures only for new invariants. Agreed.

Tightening: a derived fixture must name the invariant it exists to test and the historical class it is adjacent to. Otherwise derived fixtures accumulate as invented cases, which is the failure mode we are trying to avoid.

---

## 4. Phase 0, as I understand it

Control plane only, no runtime modules:

1. `BUILD_LINT.md` — what the compiler rejects: contradictory rules, duplicate authority over one decision, out-of-scope rules, untested rules.
2. `AUDIT_PROTOCOL.md` — the procedure above.
3. `ACCEPTANCE_BRIEF_TEMPLATE.md` — the five fields.
4. `CHANGE_CONTROL.md` — PATCH / IMPLEMENTATION CHANGE / DESIGN CHANGE / **ACCEPTANCE CHANGE**.
5. `FIXTURE_REGISTER.md` — the historical failures, each with its class and its required behaviour.

That is five documents and no code. It is also the set that would have prevented most of what went wrong, which is the only justification I have for asking for paperwork.

**Position:** workflow frozen from my side. Ready for Phase 0 — with the signer's go-ahead, since it starts producing project artifacts again.
