# Doximity long handoff test — 20 rounds

This tests repeated Stage A -> Stage B handoff inside one prompt.

Use only the prompt block below. Do not paste the expected block.

---

BEGIN LONG HANDOFF TEST

You are one prompt with two alternating stages. Do not use code. Do not skip a round.

START STATE:

{"round":0,"value":1,"history":[]}

For each round r = 1 through 20:

STAGE A:
- Add 1 to `value`.
- Append `"A<r>"` to `history`.

STAGE B:
- Multiply `value` by 2.
- Append `"B<r>"` to `history`.

After Stage B, output the complete state on one line:

R01={"round":1,"value":<value>,"history":[...]}

Use two digits for the round label: R01, R02, ..., R20.

Rules:
- Use the previous round's state. Do not recompute from the start.
- Every state must include the full history.
- Do not summarize, omit rounds, or add prose.
- After R20, output:

FINAL=<the R20 state>

Do not output anything else.

END LONG HANDOFF TEST

---

# Expected — do not paste into Doximity

```text
R01={"round":1,"value":4,"history":["A1","B1"]}
R02={"round":2,"value":10,"history":["A1","B1","A2","B2"]}
R03={"round":3,"value":22,"history":["A1","B1","A2","B2","A3","B3"]}
R04={"round":4,"value":46,"history":["A1","B1","A2","B2","A3","B3","A4","B4"]}
R05={"round":5,"value":94,"history":["A1","B1","A2","B2","A3","B3","A4","B4","A5","B5"]}
R06={"round":6,"value":190,"history":["A1","B1","A2","B2","A3","B3","A4","B4","A5","B5","A6","B6"]}
R07={"round":7,"value":382,"history":["A1","B1","A2","B2","A3","B3","A4","B4","A5","B5","A6","B6","A7","B7"]}
R08={"round":8,"value":766,"history":["A1","B1","A2","B2","A3","B3","A4","B4","A5","B5","A6","B6","A7","B7","A8","B8"]}
R09={"round":9,"value":1534,"history":["A1","B1","A2","B2","A3","B3","A4","B4","A5","B5","A6","B6","A7","B7","A8","B8","A9","B9"]}
R10={"round":10,"value":3070,"history":["A1","B1","A2","B2","A3","B3","A4","B4","A5","B5","A6","B6","A7","B7","A8","B8","A9","B9","A10","B10"]}
R11={"round":11,"value":6142,"history":["A1","B1","A2","B2","A3","B3","A4","B4","A5","B5","A6","B6","A7","B7","A8","B8","A9","B9","A10","B10","A11","B11"]}
R12={"round":12,"value":12286,"history":["A1","B1","A2","B2","A3","B3","A4","B4","A5","B5","A6","B6","A7","B7","A8","B8","A9","B9","A10","B10","A11","B11","A12","B12"]}
R13={"round":13,"value":24574,"history":["A1","B1","A2","B2","A3","B3","A4","B4","A5","B5","A6","B6","A7","B7","A8","B8","A9","B9","A10","B10","A11","B11","A12","B12","A13","B13"]}
R14={"round":14,"value":49150,"history":["A1","B1","A2","B2","A3","B3","A4","B4","A5","B5","A6","B6","A7","B7","A8","B8","A9","B9","A10","B10","A11","B11","A12","B12","A13","B13","A14","B14"]}
R15={"round":15,"value":98302,"history":["A1","B1","A2","B2","A3","B3","A4","B4","A5","B5","A6","B6","A7","B7","A8","B8","A9","B9","A10","B10","A11","B11","A12","B12","A13","B13","A14","B14","A15","B15"]}
R16={"round":16,"value":196606,"history":["A1","B1","A2","B2","A3","B3","A4","B4","A5","B5","A6","B6","A7","B7","A8","B8","A9","B9","A10","B10","A11","B11","A12","B12","A13","B13","A14","B14","A15","B15","A16","B16"]}
R17={"round":17,"value":393214,"history":["A1","B1","A2","B2","A3","B3","A4","B4","A5","B5","A6","B6","A7","B7","A8","B8","A9","B9","A10","B10","A11","B11","A12","B12","A13","B13","A14","B14","A15","B15","A16","B16","A17","B17"]}
R18={"round":18,"value":786430,"history":["A1","B1","A2","B2","A3","B3","A4","B4","A5","B5","A6","B6","A7","B7","A8","B8","A9","B9","A10","B10","A11","B11","A12","B12","A13","B13","A14","B14","A15","B15","A16","B16","A17","B17","A18","B18"]}
R19={"round":19,"value":1572862,"history":["A1","B1","A2","B2","A3","B3","A4","B4","A5","B5","A6","B6","A7","B7","A8","B8","A9","B9","A10","B10","A11","B11","A12","B12","A13","B13","A14","B14","A15","B15","A16","B16","A17","B17","A18","B18","A19","B19"]}
R20={"round":20,"value":3145726,"history":["A1","B1","A2","B2","A3","B3","A4","B4","A5","B5","A6","B6","A7","B7","A8","B8","A9","B9","A10","B10","A11","B11","A12","B12","A13","B13","A14","B14","A15","B15","A16","B16","A17","B17","A18","B18","A19","B19","A20","B20"]}
FINAL={"round":20,"value":3145726,"history":["A1","B1","A2","B2","A3","B3","A4","B4","A5","B5","A6","B6","A7","B7","A8","B8","A9","B9","A10","B10","A11","B11","A12","B12","A13","B13","A14","B14","A15","B15","A16","B16","A17","B17","A18","B18","A19","B19","A20","B20"]}
```
