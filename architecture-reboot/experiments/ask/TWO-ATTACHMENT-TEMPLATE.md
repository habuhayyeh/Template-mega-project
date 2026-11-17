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
5. Do not call F_UNUSED or F_UNUSED2.
6. Execute exactly C1 through C12, once each, in order.

If either attachment is missing or unreadable, return only:

{"error":"ATTACHMENT_NOT_READ"}

EXECUTION

Simulate the File B calls. Do not use code. Do not invent functions.

Return exactly one JSON object with this shape:

{
  "read": {
    "file_a": "FUNCTION LIBRARY",
    "file_b": "CALL SCRIPT",
    "functions": 12,
    "calls": 12
  },
  "trace": [
    {
      "call": "C1",
      "value": 0,
      "history": [],
      "wrapped": null,
      "joined": null,
      "length": null,
      "pair": null
    },
    {
      "call": "C2",
      "value": 0,
      "history": [],
      "wrapped": null,
      "joined": null,
      "length": null,
      "pair": null
    },
    {
      "call": "C3",
      "value": 0,
      "history": [],
      "wrapped": null,
      "joined": null,
      "length": null,
      "pair": null
    },
    {
      "call": "C4",
      "value": 0,
      "history": [],
      "wrapped": null,
      "joined": null,
      "length": null,
      "pair": null
    },
    {
      "call": "C5",
      "value": 0,
      "history": [],
      "wrapped": null,
      "joined": null,
      "length": null,
      "pair": null
    },
    {
      "call": "C6",
      "value": 0,
      "history": [],
      "wrapped": null,
      "joined": null,
      "length": null,
      "pair": null
    },
    {
      "call": "C7",
      "value": 0,
      "history": [],
      "wrapped": null,
      "joined": null,
      "length": null,
      "pair": null
    },
    {
      "call": "C8",
      "value": 0,
      "history": [],
      "wrapped": null,
      "joined": null,
      "length": null,
      "pair": null
    },
    {
      "call": "C9",
      "value": 0,
      "history": [],
      "wrapped": null,
      "joined": null,
      "length": null,
      "pair": null
    },
    {
      "call": "C10",
      "value": 0,
      "history": [],
      "wrapped": null,
      "joined": null,
      "length": null,
      "pair": null
    },
    {
      "call": "C11",
      "value": 0,
      "history": [],
      "wrapped": null,
      "joined": null,
      "length": null,
      "pair": null
    },
    {
      "call": "C12",
      "value": 0,
      "history": [],
      "wrapped": null,
      "joined": null,
      "length": null,
      "pair": null
    }
  ],
  "final": {
    "value": 0,
    "history": [],
    "wrapped": null,
    "joined": null,
    "length": null,
    "pair": null
  }
}

Replace the values. Keep exactly 12 trace entries and one final object.

No prose. No code fence. No extra calls.

END TWO-ATTACHMENT TEST

---

# Expected — do not paste into Doximity

```json
{
  "read": {
    "file_a": "FUNCTION LIBRARY",
    "file_b": "CALL SCRIPT",
    "functions": 12,
    "calls": 12
  },
  "trace": [
    {
      "call": "C1",
      "value": 2,
      "history": [
        "A1"
      ],
      "wrapped": null,
      "joined": null,
      "length": null,
      "pair": null
    },
    {
      "call": "C2",
      "value": 4,
      "history": [
        "A1",
        "B1"
      ],
      "wrapped": null,
      "joined": null,
      "length": null,
      "pair": null
    },
    {
      "call": "C3",
      "value": 5,
      "history": [
        "A1",
        "B1",
        "A2"
      ],
      "wrapped": null,
      "joined": null,
      "length": null,
      "pair": null
    },
    {
      "call": "C4",
      "value": 10,
      "history": [
        "A1",
        "B1",
        "A2",
        "B2"
      ],
      "wrapped": null,
      "joined": null,
      "length": null,
      "pair": null
    },
    {
      "call": "C5",
      "value": 10,
      "history": [
        "A1",
        "B1",
        "A2",
        "B2"
      ],
      "wrapped": "<done>",
      "joined": null,
      "length": null,
      "pair": null
    },
    {
      "call": "C6",
      "value": 7,
      "history": [
        "A1",
        "B1",
        "A2",
        "B2",
        "C1"
      ],
      "wrapped": "<done>",
      "joined": null,
      "length": null,
      "pair": null
    },
    {
      "call": "C7",
      "value": 8,
      "history": [
        "A1",
        "B1",
        "A2",
        "B2",
        "C1",
        "C2"
      ],
      "wrapped": "<done>",
      "joined": null,
      "length": null,
      "pair": null
    },
    {
      "call": "C8",
      "value": 10,
      "history": [
        "A1",
        "B1",
        "A2",
        "B2",
        "C1",
        "C2",
        "C3"
      ],
      "wrapped": "<done>",
      "joined": null,
      "length": null,
      "pair": null
    },
    {
      "call": "C9",
      "value": 10,
      "history": [
        "A1",
        "B1",
        "A2",
        "B2",
        "C1",
        "C2",
        "C3"
      ],
      "wrapped": "<done>",
      "joined": "A1|B1|A2|B2|C1|C2|C3",
      "length": null,
      "pair": null
    },
    {
      "call": "C10",
      "value": 10,
      "history": [
        "A1",
        "B1",
        "A2",
        "B2",
        "C1",
        "C2",
        "C3"
      ],
      "wrapped": "<done>",
      "joined": "A1|B1|A2|B2|C1|C2|C3",
      "length": 7,
      "pair": null
    },
    {
      "call": "C11",
      "value": 10,
      "history": [
        "A1",
        "B1",
        "A2",
        "B2",
        "C1",
        "C2",
        "C3"
      ],
      "wrapped": "<done>",
      "joined": "A1|B1|A2|B2|C1|C2|C3",
      "length": 7,
      "pair": [
        7,
        10
      ]
    },
    {
      "call": "C12",
      "value": 11,
      "history": [
        "A1",
        "B1",
        "A2",
        "B2",
        "C1",
        "C2",
        "C3",
        "C4"
      ],
      "wrapped": "<done>",
      "joined": "A1|B1|A2|B2|C1|C2|C3",
      "length": 7,
      "pair": [
        7,
        10
      ]
    }
  ],
  "final": {
    "value": 11,
    "history": [
      "A1",
      "B1",
      "A2",
      "B2",
      "C1",
      "C2",
      "C3",
      "C4"
    ],
    "wrapped": "<done>",
    "joined": "A1|B1|A2|B2|C1|C2|C3",
    "length": 7,
    "pair": [
      7,
      10
    ]
  }
}
```

Run three times. Any extra call, missing function, illustration execution, or wrong value fails.
