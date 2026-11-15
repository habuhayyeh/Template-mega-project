# Review 135 — File A three-record contract test

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
  certainty=reported
  relation=same_state
  disposition=carry_forward
  unresolved=SPK2 real-world role is not established; whether T001 and P1.001 derive from the same reporter is not established

UNIT U002
  concept=left MCA stroke
  evidence=P1.002[selector=Prior left MCA stroke in 2022; role=support]
  kind=diagnosis
  attribution=P1.002: PMH documentation
  time=2022; scope=historical
  polarity=affirmed
  certainty=documented
  relation=none
  disposition=carry_forward

UNRESOLVED_REGISTER

UNRESOLVED X001
  topic=falls source attribution
  evidence=T001[selector=SPK2; role=provenance], P1.001[selector=VIA=EMS report; role=provenance]
  issue=SPK2 role is unmapped and the sources do not establish whether the transcript statement and EMS-mediated patient report came from the same reporter

@@END
```

## Boundary result

**PASS.**

The output preserves the architect's required distinctions:

- one falls unit references T001 and P1.001;
- one historical left MCA stroke unit references P1.002;
- SPK2 remains unmapped;
- the repeated count of three is not summed or converted into a new total;
- no stroke-falls causal relation is inferred;
- no residual deficit is invented;
- historical stroke is not promoted to a current stroke problem;
- no consult reason is invented;
- no action, test, result, problem role, containment, note section, plan ownership, or prose is created.

## Narrow implementation observation

The File A contract uses `disposition=carry_forward` rather than the earlier sample enum value
`problem candidate`.

This is intentional and necessary to satisfy the architect's explicit ownership rule that candidate-problem
eligibility belongs to B, not A.

No architecture change is proposed here.
