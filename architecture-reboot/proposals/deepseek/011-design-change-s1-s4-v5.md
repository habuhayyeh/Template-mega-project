# DESIGN CHANGE DC-001 v5 — two corrections

**Status: PROPOSED. Not applied.** No canonical file edited. Phase 0 untouched.
**Supersedes:** v1–v4, all retained.
**Scope:** two corrections only. The applied text is v3 with the v4 replacements and these two. Everything else stands.

---

## D6 (final) — §10.1, line 331

**v4 text (rejected)**

```text
- within one section and one problem, an A/P unit may reference a given object in at most one render unit;
- this rule does not apply to body units; body uniqueness is governed by the section contract;
```

The first clause is grammatically incoherent: the unit *is* the render unit, so an A/P unit cannot "reference an object in at most one render unit".

**v5 text**

```text
- within one A/P section and its owning problem, a given object may participate in at most one render unit, unless explicit reuse permits otherwise;
- this rule does not apply to body units; body duplicate and use constraints are governed by the section contract;
```

The invariant is stated about the object's participation, not the unit's references, and the explicit-reuse escape is named rather than implied.

---

## D9 (final) — S2 approval safety

**v4 text (rejected)**

> **Approval is a safety property.** S2 may expose more than one approved representation for a problem only when choosing among them requires no further semantic adjudication under the governing selection contract. Where the choice is not semantically free, S2 reduces the set or records structured support references for the decision — not a free-text rationale.

The `or` is the defect: a set whose selection would change clinical meaning survives merely because the choice was documented.

**v5 text**

> **Approval is a safety property.** S2 may expose more than one approved representation for a problem only when choosing among them requires no further semantic adjudication under the governing selection contract. Where the choice would change clinical meaning, S2 **resolves** the semantic choice and records structured source or adjudication support before exposing the set to S3. Documenting an unresolved choice does not make it safe.

---

## Unchanged

D1–D5, D7, D8, D10, D11, D12 and the D13 consensus lines stand as accepted in v3/v4. No representation vocabulary, operator set, salience schema, or body duplicate policy is fixed. No Phase 0. All eight experiments remain open.

## Review and application

Review the two passages. On approval, the applied text is v3 as amended by v4 and this document — one commit, `DC-001` recorded in `CHANGE_LEDGER` as a `DESIGN CHANGE`, and any divergence beyond formatting voids the change.
