# Two-attachment function and call handoff

**Evidence class:** OBSERVED / REPRODUCED
**Date:** 2026-11-16
**Scope:** One attachment as a function library, one as a call script, plus a template with a read gate.

## Test shape

- Attachment A: `FILE A — FUNCTION LIBRARY`, 12 function definitions, 2 unused functions, 3 illustrations.
- Attachment B: `FILE B — CALL SCRIPT`, 12 ordered calls.
- Template: read both attachments, identify by content markers, do not execute illustrations, do not call
  unused functions, simulate calls, return JSON.

Files:

- `../experiments/ask/TWO-ATTACHMENT-A-FUNCTIONS.md`
- `../experiments/ask/TWO-ATTACHMENT-B-CALLS.md`
- `../experiments/ask/TWO-ATTACHMENT-TEMPLATE.md`

## What worked

- The model identified A as functions and B as calls.
- It reported 12 functions and 12 calls.
- It executed C1–C12 in order.
- It did not call `F_UNUSED` or `F_UNUSED2`.
- It did not execute the illustration lines.
- Four runs produced the same semantic JSON: value `11`, 8-item history, joined string, length `7`,
  pair `[7,10]`.

This is simulation, not real code execution.

## What failed

### Angle brackets were stripped

`F_WRAP(text) => "<" + text + ">"` produced:

```json
"wrapped": ""
```

Three of three runs. The angle-bracket value was stripped, consistent with HTML-tag handling.

### Bracket form was not perfectly stable

`F_WRAP(text) => "[" + text + "]"` produced:

- first batch: 2/3 correct, one run with `"wrapped": ""`;
- later batch: 4/4 correct with `"[done]"`.

Bracket form is safer than angle brackets, but not proven byte-stable.

### JSON whitespace varies

Some runs returned compact JSON; others inserted spaces after `:` and `,`. Parsed values were identical.
Raw text was not byte-identical.

## Rules

1. Identify attachments by content markers, not attachment order.
2. One attachment defines functions; the other contains calls. Do not mix roles.
3. Put a read-all gate before execution.
4. Forbid illustrations and unused functions explicitly.
5. Avoid `<...>` in model output. It can be stripped as HTML.
6. Treat `[...]` as risky too; prefer plain tokens such as `WRAP_done`.
7. Compare JSON semantically, not by whitespace. Byte-level determinism is not established.
8. This tests file-role separation and function simulation, not code execution.

## Limit

Successful simulation does not mean Doximity can execute code. The model follows definitions; it does not run
them.
