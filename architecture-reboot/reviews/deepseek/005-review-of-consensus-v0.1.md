# DeepSeek review 005 — Consensus Architecture v0.1

**Verdict: ACCEPT WITH ONE MATERIAL FIX.** The structure is sound; one invariant is missing and it is the invariant we paid for three times.

---

## 1. What holds

Checked against the six points you asked about:

- **No semantic decision leaked into the renderer.** §9's forbidden list covers duplicate identity, ownership, membership, operator choice, class movement and silent repair. Nothing in the allowed list can change what the note says.
- **The IR references clinical truth rather than duplicating it.** Units carry ids and roles; there is no rewritten prose anywhere in the IR. Good.
- **The mechanical/semantic split is coherent.** §10.1 is IR-local and note-local; §10.2 is explicitly a review instrument and does not pretend to be a predicate. That is the split I argued for and it is stated correctly.
- **Reuse does not open an accounting hole.** "Every object is either used by ≥1 unit or explicitly dispositioned" closes the one-object/multi-unit case I raised.
- **Span coverage is checkable** under the stated mechanical span boundary, with the caveat in §4 below.
- **The open items do not require reopening.** Operator vocabulary, kind taxonomy and span representation are correctly left to E1.

## 2. The missing invariant — material

§10.1 contains no rule limiting how many times one object may be rendered *within one section*.

As written, an object may belong to two units in the same section, and every mechanical check passes: each unit references a valid id; each maps to output; the object is used by ≥1 unit; no forbidden transform appears. The note renders the same fact twice and the checker is satisfied.

That is not hypothetical. It is the failure we measured repeatedly: the infarct rendered twice in one A/P, the CT rendered twice, the family concern rendered twice. It is the most expensive defect in our history, and v0.1 does not exclude it.

**Required addition to §10.1:**

> **Per-section object uniqueness.** Within one section, an object may appear in at most one unit, as any member role. Cross-section reuse is allowed and expected.

Two consequences worth stating in the architecture:

- an object rendered in HPI and again in A/P is correct; the same object in two A/P units is a contract violation;
- if a fact genuinely needs two lines in one section, that is two objects with one span, which the source allows and the span record already permits.

## 3. A clarification, not a defect

§11 allows production to suppress the Case IR. That is reasonable for the clinician's view, but it has a consequence the document should state plainly:

> Production output is not mechanically checked. Auditability is a test-time property; the acceptance claim rests on test-mode evidence, not on a guarantee about what Doximity emits in production.

Without that sentence, a reader will assume the checker runs on real notes. It does not and cannot, since there is no code inside the Ask call.

## 4. Span coverage, under one assumption

§3 works if the pasted source preserves line and speaker boundaries. If the signer's paste collapses whitespace or merges turns, span coverage becomes uncheckable and the ingest boundary needs a different mechanical anchor.

This is the dependency you already flagged. I am recording it as an assumption the architecture rests on, not as a defect: it is testable in one paste, and it is the next thing to obtain.

## 5. Conclusion

Accept on one condition: add the per-section uniqueness invariant. I have written the wording above; it is one line in §10.1 and one paragraph in §7 or §9.

When that is in, I will confirm **ACCEPT Consensus Architecture v0.1** without qualification. Nothing else in the document needs to change for me.
