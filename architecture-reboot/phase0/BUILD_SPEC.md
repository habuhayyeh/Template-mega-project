# BUILD_SPEC — what the build refuses

Canonical for: **build and package integrity.** Not for output checking — the IR-to-note checker is a separate artifact recorded in the manifest, with its own predicates.

**State: SPEC.** No lint exists. §7 is the M0 checklist that stands in.

---

## 1. Rule record

```yaml
rule: R-014
decision: DEC-AP_ORDER_WITHIN_PROBLEM     # reference, not a copy
assertion: PRD-080                         # reference, not a copy
scope: STRUCTURE                           # INGEST|STRUCTURE|RENDER|CHECK|AUDIT|BUILD|SHARED
normative:
  modality: MUST_FIRST
  subject: reasoning
  object: facts
  applies_when: [AP_BLOCK]
payload_ref: §7.2 of CON-AP_RENDER         # authoritative prose or DSL, embedded verbatim
```

A rule **references** its decision, assertion and payload. It never restates the governing contract, the fixture, or the check — a rule carrying its own copy is a second registry.

**`payload_ref` is how prose policy survives.** Where a decision's authority is prose, the payload is embedded verbatim into the package and hashed. The build checks that the payload matches its hash; it never judges the prose.

---

## 2. What the build refuses

### L1 — contradictory rules

Two rules, same atomic decision, overlapping `applies_when`, and a modality pair the compatibility table marks `EXCLUSIVE`.

The build does not infer incompatibility. It checks three declared conditions. If the third has no table entry, the result is **L1c**, not L1.

### L1c — unresolved authority

Two rules, same decision, applicability overlapping or unknown, and no compatibility relation declared. Fails the build: if the build cannot tell whether two statements conflict, the runtime picks one arbitrarily.

### L2 — duplicate authority

Two contracts claim the same decision. Authority belongs to the decision, and a decision has one `semantic_owner` and one `governing_contract`.

### L2b — orphan decision

A decision referenced by a rule that does not exist, is `WITHDRAWN`, or has no owning contract.

### L3 — out of scope

A rule whose `scope` is not in the decision's `authority_scope`, or is not listed in `obligated_scopes`. Registry containment only.

### L4 — untested rule

A rule whose `assertion` does not exist or is not `ACTIVE`. An `ACTIVE` assertion is the evidence of coverage; a pointer is not.

### L5 — dangling or mismatched reference

A reference to a missing record, or a `payload_ref` whose hash does not match the compiled payload.

### L6 — unresolved conflict marker

Unmerged text in a compiled file.

---

## 3. What the build does not refuse

- Package-order sensitivity — order effects are characterised by experiment (O-06), not forbidden by the build.
- Prose meaning — never judged.
- Anything about the note.

---

## 4. Severity

Every violation fails the build. No warnings.

---

## 5. Output

```text
BUILD_SPEC  pkg-7  controls v2
  rules 96  decisions 71  contracts 9
  L1  contradictory ......... 0
  L1c unresolved ............ 0
  L2  duplicate authority ... 0
  L2b orphan decision ....... 1  R-041 / DEC-AP_ORDER_2 has no owning contract
  L3  out of scope .......... 0
  L4  untested .............. 0
  L5  dangling/mismatch ..... 0
  L6  conflict marker ....... 0
  RESULT: FAIL
```

Illustrative. The report localises; it does not explain.

---

## 6. Boundary

BUILD owns: rule schema, ownership, scope, coverage, payload integrity, build reproducibility.
BUILD does not own: whether the note is correct, whether a check is defined correctly, or what a verdict means.

---

## 7. M0 manual gate

Performed by a reviewer, recorded in the packet, until §1–§5 exist as code.

```text
M0-BUILD  package: ______  reviewer: ______  date: ______
[ ] every rule references an existing decision
[ ] every rule's scope is authorised by its decision
[ ] no two rules with one decision and exclusive modalities
[ ] no L1c pairs left unresolved
[ ] every rule references an ACTIVE assertion
[ ] every payload hash matches
[ ] no dangling references, no conflict markers
RESULT: ______
```

A package that has not passed M0 is not a valid artifact.
