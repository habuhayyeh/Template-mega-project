# TWO-ATTACHMENT TEMPLATE — function library + call script

Paste this as the prompt. Attach both files.

---

BEGIN TWO-ATTACHMENT TEST

You have two attachments.

Attachment 1 is the **function library**. It defines functions only. It contains illustrations, not calls.
Attachment 2 is the **call script**. It contains the only calls you may execute.

READ GATE

1. Read both attachments completely before producing output.
2. Do not execute anything while reading.
3. Identify the files by their content markers, not by attachment order:
   - `FILE A — FUNCTION LIBRARY`
   - `FILE B — CALL SCRIPT`
4. Do not execute the illustration lines in File A.
5. Do not call any function that File B does not call.

If either attachment is missing or unreadable, return only:

{"error":"ATTACHMENT_NOT_READ"}

EXECUTION

Simulate the File B calls in order. Do not use code. Do not invent functions.

Return exactly one JSON object:

{
  "read": {
    "file_a": "FUNCTION LIBRARY",
    "file_b": "CALL SCRIPT",
    "functions": 5,
    "calls": 5
  },
  "trace": [
    {"call": "C1", "value": 0, "history": []},
    {"call": "C2", "value": 0, "history": []},
    {"call": "C3", "value": 0, "history": []},
    {"call": "C4", "value": 0, "history": []},
    {"call": "C5", "value": 0, "history": []}
  ],
  "wrapped": "<done>"
}

No prose. No code fence. No extra calls. No `F_UNUSED`.

END TWO-ATTACHMENT TEST

---

# Expected — do not paste into Doximity

```json
{
  "read": {
    "file_a": "FUNCTION LIBRARY",
    "file_b": "CALL SCRIPT",
    "functions": 5,
    "calls": 5
  },
  "trace": [
    {"call": "C1", "value": 2, "history": ["A1"]},
    {"call": "C2", "value": 4, "history": ["A1", "B1"]},
    {"call": "C3", "value": 5, "history": ["A1", "B1", "A2"]},
    {"call": "C4", "value": 10, "history": ["A1", "B1", "A2", "B2"]},
    {"call": "C5", "value": 10, "history": ["A1", "B1", "A2", "B2"]}
  ],
  "wrapped": "<done>"
}
```

Run three times. Any extra call, missing function, illustration execution, or wrong value fails.
