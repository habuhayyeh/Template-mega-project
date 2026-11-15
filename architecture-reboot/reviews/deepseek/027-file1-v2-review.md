# DeepSeek review — File 1 F1-EVIDENCE-V2

**Reviewed:** `experiments/ask/modules/01-EVIDENCE-OBJECTS.md` (F1-EVIDENCE-V2)
**Status:** review only; no implementation.

## Verdict

V2 fixes the ontology and stance problems. **One parser blocker remains**; do not run it as written.

## BLOCKER — the separator count is wrong

The output schema has eight fields:

```text
E0001 :: SRC=... :: ACT=... :: POL=... :: CERT=... :: TIME=... :: ATTR=... :: TEXT=...
```

That is **seven** structural ` :: ` separators after the evidence id, not six. The parsing rule says
"only the first six literal ` :: ` separators after the evidence id are structural." A compliant parser
would consume the sixth separator before `ATTR`, leaving `ATTR=... :: TEXT=...` inside the text field, or
would parse `TEXT` as `ATTR`.

Fix to **seven** separators, or better define the fields positionally:

```text
id
SRC
ACT
POL
CERT
TIME
ATTR
TEXT (remainder)
```

The count should match the schema exactly.

## BLOCKER — Step 0 rejects valid prechart records

Step 0 says every record is:

```text
<record id> :: <source/speaker label> :: <text>
```

But V2.2 prechart records can be:

```text
P1.001 :: SEC=HPI :: VIA=EMS report :: text
```

Step 0 would treat that as malformed or as three fields. Define the input forms explicitly:

```text
T record:  T... :: SPK... :: text
P record:  P... :: [SEC=...] :: [VIA=...] :: text
```

The `TEXT` is everything after the last structural source field.

## Minor — ATTR containing ` :: `

`ATTR=VIA:prior neurology note` is fine, but an attribution containing ` :: ` would break positional
parsing. Either forbid ` :: ` in ATTR/SRC/ACT/POL/CERT/TIME or define escaping. Do not let free text
silently shift columns.

## Minor — Step 0 says “source/speaker label” only

Prechart records do not have a speaker. Use `label/source fields` or list the two forms above.

## Accept

- removal of the 14-label clinical kind ontology;
- `ACT` limited to STATEMENT / QUESTION / ACTION_MENTION / REASONING;
- POL and CERT separated;
- `[UNCLEAR]`/`[VERBATIM]` preserved in TEXT;
- time categories defined;
- questions as `ACT=QUESTION`, `POL=NA`, `CERT=NA`;
- one record -> many objects; no cross-record merge;
- action mentions unadjudicated; reasoning preserved;
- fail-closed invalid output;
- no problem/role/use/note decisions.

## Run readiness

After the two parser fixes, F1 V2 is ready for the first empirical run. Until then, an F1 output could be
misparsed even when the model follows the prompt.

No Gate-0 acceptance. No Doximity production change. No Phase 0.
