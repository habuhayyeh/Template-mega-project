# Input visibility test

Use this first. It checks whether Doximity is actually passing the packet into the turn.

Run in a fresh Ask conversation, with the packet pasted between the packet markers.

---

BEGIN INPUT TEST

Read the packet below.

Output exactly:

@@CHECK;;first_record=<first record ID in the packet>;;last_record=<last record ID in the packet>;;t_count=<number of T records>;;p1_count=<number of P1 records>
@@END

Do not synthesize. Do not explain. Do not output any other record.

END INPUT TEST

BEGIN SCRIBE PACKET

<paste the complete Scribe packet here>

END SCRIBE PACKET
