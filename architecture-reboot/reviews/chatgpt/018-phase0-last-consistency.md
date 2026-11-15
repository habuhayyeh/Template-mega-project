# ChatGPT review 018 — Phase 0 last internal-consistency corrections

## Verdict

**REVISE — very narrow.**

The Phase 0 control plane is now structurally sound. Remaining blockers are concrete internal contradictions/evidence inaccuracies. No new architecture or workflow changes are requested.

---

# 1. CHANGE_CONTROL.md — one unresolved contradiction

Section 2 correctly says:

> Observed outputs may vary within frozen contract and acceptance properties.

But its requirements still say:

> the reviewing agent confirms no interface, contract or observable behaviour changed.

And the table still says:

> reviewer confirms locality

These contradict the accepted definition.

Replace both with:

> reviewer confirms the frozen contract, interface, semantic authority, and acceptance properties are unchanged; required regression tests pass.

Do not require unchanged observable output.

Also change the table entry from:
- `confirms locality`

to:
- `confirms contract/interface/acceptance invariance + regression`

---

# 2. ACCEPTANCE_BRIEF_TEMPLATE.md — approval wording conflicts with CHANGE_CONTROL

Current rule 5:

> Changing it afterwards is an ACCEPTANCE CHANGE and needs the same approval as a design change.

But CHANGE_CONTROL intentionally distinguishes ACCEPTANCE CHANGE from DESIGN CHANGE.

Use:

> Changing it afterwards is an ACCEPTANCE CHANGE and follows CHANGE_CONTROL §4, including signer approval when a signer-approved clinical/style/product baseline is altered.

This keeps the categories distinct.

---

# 3. AUDIT_PROTOCOL.md — make artifact-mode answerability fully assertion-driven

Mode A currently predeclares:

> Answerable: consistency, placement, completeness, voice.

That is not universally true; it depends on the artifact and evidence.

Use:

> Answerable: only the declared assertions whose required evidence is present.

Mode B similarly should avoid saying "everything" is answerable.

Use:

> Answerable: all declared assertions for which the supplied source/IR/check evidence satisfies their deciding requirements.

This aligns the mode definitions with §5.

No other audit blocker.

---

# 4. FIXTURE_REGISTER.md — F-06 evidence is still inaccurate

Current:

> `PACKAGE.md` before and after the standing-item contract was added

There is only a current canonical `PACKAGE.md`; it is not both the historical incomplete and corrected package.

Use exact evidence:

- `reviews/P003-implementation-doximity-original-branch.md`
  - establishes the initial omission was untestable because `STANDING_ITEMS.md` was absent;
- `PACKAGE.md`
  - records the corrected canonical package;
- `runs/2026-11-14-p003-doximity/set2/validation.txt`
  - standing item present 3/3 after packaging correction;
- `runs/2026-11-14-p003-doximity/set3/validation.txt`
  - present 3/3 again.

Phrase the defect:

> historical package omission made the standing-item behavior untestable; corrected packaging restored the required line.

Do not call the original event a model omission.

---

# 5. FIXTURE_REGISTER.md — C-02 still misstates the O51 event

Current:

> EVIDENCE_MODE requirement added for COURSE conflicted with the existing SECTION_CONTRACT rule 38 governing the same text

Canonical source `artifacts/06_doximity_run3.md` states:

> the added EVIDENCE_MODE section said a **prior-record result belongs with its finding in NEURO_HISTORY**; SECTION_CONTRACT rule 38 said **historical disease-specific studies belong in WORKUP**; O51 moved from WORKUP in run 2 to NEURO_HISTORY in run 3 immediately after that clause was added.

Use that exact description.

Do not call it a COURSE-text conflict.

---

# 6. FIXTURE_REGISTER.md — C-12 assertions do not match the historical defect

The B+ experiment says:

- T4 repeatedly rendered `The MRI to show.`;
- this was stable 3/3;
- the operator/input lacked a complete semantic proposition;
- the correct representation pattern exposed:
  - `TEST=MRI`
  - `PURPOSE=determine whether there is a new lesion`
- T8 then rendered the complete relation.

The present assertion:

> rendered line carries every content token of its head member

does not test that failure. The incomplete head itself may contain no missing purpose tokens.

Phase 0 should encode the failure generically, without prematurely freezing exact operator fields:

### A-C12a — S4 / HYBRID
> a render unit selected for a relation-dependent operator contains every semantic role required by that operator; an incomplete relation is not passed to R1 as renderable.

Owner: **S4**.

### A-C12b — R1 / MECHANICAL
> R1 does not infer or manufacture a missing semantic role; malformed/incomplete operator payload fails closed.

Owner: **R1**.

When the operator schema is later frozen, A-C12a can become mechanically decidable for the closed operator vocabulary.

Do not use literal head-token retention as the historical C12 detector.

---

# 7. FIXTURE_REGISTER.md — exact evidence path cleanup

For F-02/03/04 and F-06, use literal complete paths rather than:
- one full path followed by shortened `set3/run2.txt`;
- `run1–3.txt`.

This is a documentation cleanup, but it follows the register's own rule:
> evidence is a path, not a recollection.

---

# 8. F-01 — add the renderer-side assertion

F-01 is an envelope-level fabrication failure.

Current assertions cover:
- I3 source-token support;
- BUILD package completeness.

Add the downstream seam too:

### A-01c — R1 / MECHANICAL or HYBRID as appropriate to the later operator contract
> R1 may not introduce an unsupported clinical status/semantic proposition absent from the unit payload and operator-fixed text.

Owner: **R1**.

This prevents the historical final-output failure from being represented only as an ingest/package problem.

---

# 9. Freeze target

If these exact corrections are made and no new contradiction is introduced, Phase 0 is ready to freeze.

No further redesign is requested.
