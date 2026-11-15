# PACKET — acceptance packet and change ledger

---

# §1 Acceptance packet

The unit of acceptance is the packet, not the note. A note without a packet is an observation.

```yaml
packet:
  run_id: 2026-11-16-case03-run2
  case_id: CASE-03
  mode: PRODUCTION            # PRODUCTION | TEST
  model: doximity-ask
  package_version: pkg-7
  contract_versions: { STRUCTURE_CONTRACT: 2, RENDER_CONTRACT: 2 }
  brief_version: B-03-v1
  assertion_set_version: AS-03-v1
  baseline_version: BASE-03-v1
  required_evidence: [source_package, case_ir, note]
  evidence_hashes: { source_package: sha256:…, case_ir: sha256:…, note: sha256:… }
  check_report: CHECK-03-v1
  audit: { mode: B, result: REJECT, findings: [F-0412] }
  verdict: REJECT
```

Rules:

1. A run scored without a packet is not acceptance evidence.
2. `assertion_set_version` must match the version frozen for this case; a mismatch invalidates the score.
3. `verdict` may be `ACCEPT`, `REJECT`, `BLOCKED`, or `DISCOVERY` (a finding not covered by any frozen assertion).
4. A `DISCOVERY` is not scored. It becomes an acceptance change and a rerun, or it does not enter the record.
5. Changing any version in the packet means a new packet, not an edited one.

---

# §2 Change ledger

Every governed change, one line. This is the authority for change history; the root `CHANGELOG.md` belongs to the old pipeline and is not used here.

```text
2026-11-16 | IMPLEMENTATION CHANGE | RENDER  | v0→v1  | no contract change; regression F-02/F-12 pass | approved: reviewer
2026-11-16 | ACCEPTANCE CHANGE     | AS-03-v1 | added A-03-07 (voice, second person) | reason: style contract already prohibited it; assertion was missing | approved: reviewer
2026-11-16 | DESIGN CHANGE         | STRUCTURE | moved CURRENT_ADOPTION from S3 to S2 | dependency: S2, S3, S4 | signer: n/a
```

Fields: date, category, artifact or assertion set, what changed, reason, approval.

Categories, from `CHANGE_CONTROL.md`: `PATCH`, `IMPLEMENTATION CHANGE`, `DESIGN CHANGE`, `ACCEPTANCE CHANGE`.

---

# §3 No retroactive rescoring

A run is interpreted under the assertion version frozen when it ran. If the criteria change afterwards:

- the old score stays as recorded, marked `superseded`;
- the case is re-run and re-scored under the new version;
- the old packet is never edited.

This rule exists because the cheapest way to make a failing system pass is to rewrite what counted as passing, and it is nearly invisible when done gradually.

---

# §4 Discovery

```text
DISCOVERY D-0041
case: CASE-03
finding: a medication reconciliation line renders under the wrong problem
covered by frozen assertion: no
action: proposed acceptance change AC-07 → if accepted, rerun
```

A discovery does not lower the score of the run that found it. It does not improve it either. It is a finding, and findings enter the record only by being converted.
