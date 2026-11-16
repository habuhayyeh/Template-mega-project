# Synthesis keyed-field test — one problem, one unit, one action

Use this in a fresh Ask turn. It tests whether keyed fields survive better than positional `;;` fields.

---

BEGIN TEST INSTRUCTIONS

This is a schema test, not a full note. Read the packet and frozen coverage below.

Output exactly three records, using keyed fields in the order shown. Fill every field. Use `NONE` when a
field is empty. Do not output a fourth record. Do not write a note.

BEGIN TEST OUTPUT

@@PROBLEM;;id=P001;;role=PRIMARY;;label=<short problem label>;;evidence=<comma IDs from coverage>;;counter=NONE;;contains=<baseline comparator or NONE>;;separate=NONE;;order=1
@@UNIT;;id=CU001;;type=current_event;;label=<short event label>;;sources=<comma IDs from coverage>;;chronology=<short chronology or NONE>;;problem=P001
@@ACTION;;id=AV001;;sources=<comma IDs from coverage>;;target=<source-local target>;;wording=<source-qualified wording>;;owner=P001;;unresolved=NONE
@@END

END TEST OUTPUT

Do not synthesize beyond these three records. Do not output COV records.

END TEST INSTRUCTIONS

BEGIN SCRIBE PACKET

<paste the complete Scribe packet here>

END SCRIBE PACKET

BEGIN FROZEN COVERAGE

<paste the accepted coverage census here>

END FROZEN COVERAGE
