# DESIGN CHANGE DC-001 v4 — three local fixes

**Status: PROPOSED. Not applied.** No canonical file edited. Phase 0 untouched.
**Supersedes:** v1, v2, v3 — all retained on record.
**Scope:** v4 changes only the three items below. Everything else stands exactly as written in v3 (`009-design-change-s1-s4-v3.md`), which is otherwise approved as the applied text.

---

## D6 (revised) — §10.1, line 331

**v3 text (rejected)**

```text
- within one section and, for A/P units, one problem, the same object may participate in at most one render unit;
- uniqueness for body units is governed by the section contract, not by this rule;
```

The first line reduces to "within one section" for body units, which still states a body uniqueness rule while the second line says body uniqueness is downstream. It contradicts itself.

**v4 text**

```text
- within one section and one problem, an A/P unit may reference a given object in at most one render unit;
- this rule does not apply to body units; body uniqueness is governed by the section contract;
```

The rule is scoped to A/P in its first clause and explicitly excluded in the second, so no body policy is implied.

---

## D9 (revised) — S2 approval safety

**v3 text (rejected)**

> **Approval is a safety property.** Where S2 approves more than one representation for a problem, those representations must be interchangeable — equivalent, or explicitly ordered by S2 with the basis recorded. S2 may not leave S3 a set that requires semantic judgement to choose from.

Two defects: it conflates semantic equivalence with ordering (two representations can be non-equivalent yet have a defensible order), and "basis recorded" invites free text.

**v4 text**

> **Approval is a safety property.** S2 may expose more than one approved representation for a problem only when choosing among them requires no further semantic adjudication under the governing selection contract. Where the choice is not semantically free, S2 reduces the set or records structured support references for the decision — not a free-text rationale.

**Corresponding S2 output line — v3**

```text
- where no candidate is defensible, an explicit state that S3 can act on; its name and form are
  downstream.
```

**v4**

```text
- where no claim representation can be semantically approved, an explicit state that S3 can act on;
  its name and form are downstream.
```

---

## D10 (revised) — S3 blocking rule

**v3 text (rejected)**

> **It does not resolve semantic ambiguity**: if S2's approved set for a required problem is empty, inclusion is blocked at the S2→S3 seam with the problem named; if the set holds more than one non-equivalent representation, that is an S2 defect, not an S3 choice.

"Required problem" is undefined at S3: what is required depends on S3's own inclusion decision, so the sentence is circular.

**v4 text**

> **It does not resolve semantic ambiguity.** S3 may not include or render an A/P problem that lacks an S2-approved representation. If a separate governing requirement mandates inclusion of such a problem, the seam fails or flags rather than rendering a claimless block. If S2's approved set for an included problem holds more than one representation and the choice among them is not semantically free, that is an S2 defect, not an S3 choice.

---

## D13 (revised) — `CONSENSUS.md` 29

**v3**

```text
29. S1 proposes candidates; S2 adjudicates adoption and claim relations and produces approved claim representations; S3 selects the rendered-problem set and one approved representation per problem; S4 owns final order.
```

**v4**

```text
29. S1 proposes candidates; S2 adjudicates adoption and claim relations and produces approved claim representations; S3 selects the rendered-problem set and one approved representation per rendered A/P problem; S4 owns final order.
```

---

## Everything else

D1–D5, D7, D8, D11, D12 and the supersession lines stand as in v3, unchanged. No representation vocabulary, operator set, salience schema, or body duplicate policy is fixed. No Phase 0 edit. All eight experiments remain open.

## Review

Review the four changed passages only. On approval, the applied text is v3 with these four replacements — one commit, `DC-001` recorded in `CHANGE_LEDGER`, and any divergence beyond formatting voids the change.
