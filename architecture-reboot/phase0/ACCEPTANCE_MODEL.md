# ACCEPTANCE_MODEL — predicates, packets, verdicts

Canonical for: **what an acceptance predicate is, what a packet must contain, and what a verdict means.**

`AUDIT_PROTOCOL.md` owns *how* a verdict is reached. This file owns *what a verdict is*. Neither may do the other's job.

---

## 1. Predicate record

One record type, not two. A reusable invariant is a predicate with broad applicability; a case-bound assertion is a predicate with narrow applicability.

```yaml
predicate: PRD-014
asserts: "no object's content token is absent from its anchor span"
kind: CASE_ASSERTION       # CASE_ASSERTION | BUILD_GATE | PROCESS_GATE | SCORER_CONTROL
owner: I3                  # exactly one registered owner id
mode: MECHANICAL           # MECHANICAL | SEMANTIC_AUDIT | HYBRID
severity: MATERIAL         # CRITICAL | MATERIAL | COSMETIC
applies_to: "every object in every case"
requires_contracts: [INGEST_CONTRACT]      # prerequisite before executable
status: PENDING_DEPENDENCY # ACTIVE | PENDING_DEPENDENCY | WITHDRAWN
version: 1
```

**Owner domain by kind:** `CASE_ASSERTION` → runtime submodule; `BUILD_GATE` → BUILD; `PROCESS_GATE` → PROCESS; `SCORER_CONTROL` → SCORER. The "exactly one owner" rule holds everywhere; the domain is set by kind.

**`requires_contracts`** is what makes `PENDING_DEPENDENCY` honest: a predicate cannot become `ACTIVE` while a named prerequisite contract is unfrozen.

**A predicate may assert only what a frozen contract grants.** A predicate that answers an open design question is not a test; it is an unpublished decision.

---

## 2. Assertion sets

Versioned records (`AS-CASE03-v1`) listing the predicates applicable to one case, with their applicability and prerequisites.

- One set can cover several fixtures; one fixture can require several sets.
- A set is immutable once used in a packet. Changes create a new version.
- Fixtures reference sets; they do not contain them.

---

## 3. Packet

The packet is per-run evidence. It is immutable once written.

```yaml
packet: PKT-2026-11-16-case03-run2
experiment: EXP-03          # null for an ad-hoc run
case: CASE-03
mode: PRODUCTION            # PRODUCTION | TEST
model: doximity-ask
package_version: pkg-7
control_plane_version: 2
contract_versions: {CON-STRUCTURE: 2, CON-RENDER: 2}
brief_version: B-03-v1
assertion_set: AS-CASE03-v1
baseline: BASE-03-v1
required_evidence: [source_package, note]
evidence_hashes: {source_package: sha256:…, note: sha256:…}
case_ir: null               # present in TEST, may be suppressed in PRODUCTION
check_report: CHK-03-v1
audit: {mode: A, result: PASS, findings: []}
verdict: PASS
```

**A production packet may omit the Case IR.** The IR is a test-mode artifact; requiring it in production would make production unscorable. What a packet must always carry is what the declared predicates need — no more.

---

## 4. Verdict semantics

| verdict | meaning |
|---|---|
| `PASS` | every required predicate was decidable and true |
| `FAIL` | at least one required predicate was decidable and false |
| `BLOCKED` | at least one required predicate was undecidable, or required evidence absent |

`FAIL` and `BLOCKED` may both apply; the recorded verdict is `BLOCKED` with the failures listed, because an unscorable run cannot be scored as failing.

**`DISCOVERY` is not a verdict.** It is a finding state, recorded alongside a verdict:

```text
verdict: PASS
discoveries: [DSC-0041]
```

A discovery is not covered by any frozen predicate, does not change the verdict, and cannot be applied retroactively. It enters the record only by becoming an `ACCEPTANCE CHANGE` followed by a rerun.

---

## 5. Supersession

A packet is never edited. Supersession is an external record in `CHANGE_LEDGER.md`:

```text
CHG-0112 | supersession | PKT-…-run2 → PKT-…-run2b | reason: control-plane 2 → 3 | approved: reviewer
```

The old packet remains as recorded, with its original verdict.

---

## 6. No retroactive rescoring

A run is interpreted under the assertion set frozen when it ran. If the criteria change afterwards, the case is re-run and re-scored; the old score stays, marked superseded.

This is the cheapest way to make a failing system pass, and it is nearly invisible when done one predicate at a time.

---

## 7. Experiment boundary

A packet cannot satisfy an experiment-level gate. Repetition agreement, arm comparison and order effects are decided by an `EXP-` manifest, which references packets.

`SYSTEM_ACCEPTED` in the manifest requires an experiment, never a single packet.

---

## 8. Evidence integrity

Raw evidence is hashed at capture and verified before scoring. A packet whose hash does not match its evidence is invalid, not merely suspect.
