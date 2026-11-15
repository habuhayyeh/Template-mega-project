# Review 136 — File A three-record test after DeepSeek field corrections

## Test packet

```text
T001 :: SPK2 :: Three falls since June.
P1.001 :: SEC=HPI :: VIA=EMS report :: Patient reports three falls.
P1.002 :: SEC=PMH :: Prior left MCA stroke in 2022.
```

## Exact File A output

```text
@@HANDOFF A_INTERPRET_RECONCILE_V1

DECISION_LEDGER

UNIT U001
  concept=falls
  evidence=T001[selector=Three falls since June; role=support], P1.001[selector=Patient reports three falls; role=support]
  kind=statement
  attribution=T001: SPK2 role unmapped; P1.001: ED HPI via EMS report of patient report
  time=since June where stated; scope=longitudinal
  polarity=affirmed
  certainty=unstated
  relation=possible_overlap
  disposition=carry_forward
  unresolved=SPK2 real-world role is not established; whether T001 and P1.001 describe the same reporter/event is not established

UNIT U002
  concept=left MCA stroke
  evidence=P1.002[selector=Prior left MCA stroke in 2022; role=support]
  kind=diagnosis
  attribution=P1.002: PMH documentation
  time=2022; scope=historical
  polarity=affirmed
  certainty=unstated
  relation=none
  disposition=carry_forward

UNRESOLVED_REGISTER

UNRESOLVED X001
  topic=falls source attribution/event overlap
  evidence=T001[selector=SPK2; role=provenance], P1.001[selector=VIA=EMS report; role=provenance]
  issue=SPK2 role is unmapped and the packet does not establish whether the transcript statement and EMS-mediated patient report describe the same reporter/event

@@END
```

## Result

**PASS.**

DeepSeek Step-2 corrections are satisfied:

- U001 `certainty=unstated`;
- U001 `relation=possible_overlap`;
- U002 `certainty=unstated`;
- same evidence records preserved;
- same provenance uncertainty preserved;
- no new unit or downstream problem decision introduced.

No B, C, renderer, validator, full note, Phase 0, or production change was created.
