# Gate 0 signer review index — BLINDED

**Campaign:** GATE0-C1  
**Policy:** REVIEW-POLICY-F-1  
**Packets:** 16

This index is for the signer/clinician reference pass.

It intentionally omits:
- seed/clean status;
- artifact filename;
- expected verdict;
- expected predicate/mutation;
- specificity answer key;
- scorer status/detail.

Review only the packet file named on each row. Record one of `FIRED`, `SILENT`, or `UNDECIDABLE`
plus a short rationale. Do not use `INDEX.md` or `INDEX.json` during blinded review because those are
operator artifacts containing answer-key information.

| # | predicate | packet id | packet file |
|---:|---|---|---|
| 1 | `S1-CAND-01` | `pkt-16ced7dee2e14aec98b74e97` | `architecture-reboot/runs/gate0-packets-c1/packets/pkt-16ced7dee2e14aec98b74e97.json` |
| 2 | `S2-ADOPT-01` | `pkt-876bdd66fa7db9f55b3b388b` | `architecture-reboot/runs/gate0-packets-c1/packets/pkt-876bdd66fa7db9f55b3b388b.json` |
| 3 | `S2-REP-01` | `pkt-6e8fc6ddcd12ae7f2f7eb917` | `architecture-reboot/runs/gate0-packets-c1/packets/pkt-6e8fc6ddcd12ae7f2f7eb917.json` |
| 4 | `S1-CAND-01` | `pkt-9ccb3e56876196e560fb2d48` | `architecture-reboot/runs/gate0-packets-c1/packets/pkt-9ccb3e56876196e560fb2d48.json` |
| 5 | `S1-CAND-01` | `pkt-e7dbed42337dc547369d4057` | `architecture-reboot/runs/gate0-packets-c1/packets/pkt-e7dbed42337dc547369d4057.json` |
| 6 | `S1-CAND-01` | `pkt-995d0079ed67a340d3fe26a9` | `architecture-reboot/runs/gate0-packets-c1/packets/pkt-995d0079ed67a340d3fe26a9.json` |
| 7 | `S1-CAND-01` | `pkt-c7ff8beb7be31a3c477b782b` | `architecture-reboot/runs/gate0-packets-c1/packets/pkt-c7ff8beb7be31a3c477b782b.json` |
| 8 | `S1-CAND-01` | `pkt-2ce5dbd0a6aa1898354b8b82` | `architecture-reboot/runs/gate0-packets-c1/packets/pkt-2ce5dbd0a6aa1898354b8b82.json` |
| 9 | `S2-ADOPT-01` | `pkt-e503c5ad04f05e6145605ae5` | `architecture-reboot/runs/gate0-packets-c1/packets/pkt-e503c5ad04f05e6145605ae5.json` |
| 10 | `S2-REP-01` | `pkt-a80d28edaad348d933f7709d` | `architecture-reboot/runs/gate0-packets-c1/packets/pkt-a80d28edaad348d933f7709d.json` |
| 11 | `S2-ADOPT-01` | `pkt-b55c0a355406bee7b8e660a7` | `architecture-reboot/runs/gate0-packets-c1/packets/pkt-b55c0a355406bee7b8e660a7.json` |
| 12 | `S2-REP-01` | `pkt-a3a9ad7506d9ea1c7605c899` | `architecture-reboot/runs/gate0-packets-c1/packets/pkt-a3a9ad7506d9ea1c7605c899.json` |
| 13 | `S2-ADOPT-01` | `pkt-36c35eb264b6140753c7d5a0` | `architecture-reboot/runs/gate0-packets-c1/packets/pkt-36c35eb264b6140753c7d5a0.json` |
| 14 | `S2-REP-01` | `pkt-054b2f788f871e0e635153fa` | `architecture-reboot/runs/gate0-packets-c1/packets/pkt-054b2f788f871e0e635153fa.json` |
| 15 | `S2-ADOPT-01` | `pkt-cc7b359b2179e787734bdbaa` | `architecture-reboot/runs/gate0-packets-c1/packets/pkt-cc7b359b2179e787734bdbaa.json` |
| 16 | `S2-REP-01` | `pkt-02282d97e541275e53f0202f` | `architecture-reboot/runs/gate0-packets-c1/packets/pkt-02282d97e541275e53f0202f.json` |

## Reference record shape

```json
{
  "packet_id": "<packet id>",
  "predicate_id": "<predicate id>",
  "judge_id": "signer",
  "judge_type": "HUMAN",
  "role": "REFERENCE",
  "authority": "SIGNER_CLINICIAN",
  "verdict": "FIRED | SILENT | UNDECIDABLE",
  "rationale": "<brief reason>",
  "policy_version": "REVIEW-POLICY-F-1"
}
```

Do not inspect answer-key/operator artifacts until all signer reference verdicts are recorded.
