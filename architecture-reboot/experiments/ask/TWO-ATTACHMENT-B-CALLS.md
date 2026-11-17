# FILE B — CALL SCRIPT

EXECUTE ONLY THESE CALLS IN ORDER.

Do not execute the illustrations in File A. Do not call F_UNUSED or F_UNUSED2.

START STATE:

{"value": 1, "history": [], "wrapped": null, "joined": null, "length": null, "pair": null}

C1:
- value = F_ADD1(value)
- history = F_APPEND(history, "A1")

C2:
- value = F_DOUBLE(value)
- history = F_APPEND(history, "B1")

C3:
- value = F_ADD1(value)
- history = F_APPEND(history, "A2")

C4:
- value = F_DOUBLE(value)
- history = F_APPEND(history, "B2")

C5:
- wrapped = F_WRAP("done")

C6:
- value = F_SUB3(value)
- history = F_APPEND(history, "C1")

C7:
- value = F_MAX(value, 8)
- history = F_APPEND(history, "C2")

C8:
- value = F_IF_POS(value, value + 2, value - 2)
- history = F_APPEND(history, "C3")

C9:
- joined = F_JOIN(history, "|")

C10:
- length = F_LEN(history)

C11:
- pair = F_PAIR(value, length)

C12:
- value = F_ADD1(value)
- history = F_APPEND(history, "C4")

END CALL SCRIPT
