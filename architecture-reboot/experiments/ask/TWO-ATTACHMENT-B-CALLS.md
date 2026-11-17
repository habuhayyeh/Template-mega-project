# FILE B — CALL SCRIPT

EXECUTE ONLY THESE CALLS IN ORDER.

Do not execute the illustrations in File A. Do not call F_UNUSED.

START STATE:

{"value": 1, "history": [], "wrapped": null}

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

END CALL SCRIPT
