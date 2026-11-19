# Raw runs and evaluations

Status: no runs performed. [The matrix](../MATRIX.md) lists planned slots.

Use one folder per actual run, for example `screen01/P00-A-r1/`. Reserved names and planned matrix cells do not establish that a run occurred.

Each completed run folder contains:
- `record.md` — filled from [RUN_TEMPLATE.md](RUN_TEMPLATE.md).
- `input.md` — exact submitted prompt/text, plus exact versioned attachment references or copies if attachments were used.
- `output.txt` — untouched raw output, including any extra introductory or closing text.
- `evaluation.md` — results against the reviewed reference, unsupported additions, and reviewer corrections.

Record the actual runtime. Local/model simulations are labeled local/mock and cannot be counted as Doximity acceptance. Do not fabricate unavailable model identifiers or settings.

Use fresh conversations where available and identical settings for the comparison. Retain both repetitions, including failures. If an output was manually edited before preservation, do not label it raw; record the limitation.

Update the matching matrix cell with a link to the run record after capture and with evaluation status after review. Log actionable failures in [FAILURES.md](../FAILURES.md).

Run IDs use `packet-method-repetition`; `screen01` identifies the first frozen comparison batch. Change the batch identifier when test inputs change, so earlier results remain reproducible.
