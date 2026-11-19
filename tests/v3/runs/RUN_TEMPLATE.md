# Run record template — not a performed run

Copy into an actual run folder. Complete fields from the real run; mark unavailable runtime information explicitly.

| Field | Value |
|---|---|
| Run ID / batch | To record |
| Packet ID, path, and git commit | To record |
| Method ID, prompt path, and git commit | To record |
| Shared-instruction path and git commit | To record |
| Reference path, git commit, and review status | To record |
| Runtime: Doximity or local/mock | To record |
| Date/time and timezone | To record |
| Exposed model/version and settings | To record, or unavailable |
| Fresh conversation / prior context | To record |
| Exact submitted input and attachments | To record |
| Raw output file | To record |
| Capture limitations or deviations | To record, or none |
| Evaluation file and reviewer | To record |
| Evaluation status | Not evaluated |

## Evaluation contents

In the separate evaluation file, record each reference expectation and its result with the relevant output passage. Record omissions, invented assertions, changed causal relationships, temporal/attribution errors, altered management details, and formatting failures separately.

Report concision and review burden separately from clinical fidelity. Do not use an overall score to conceal consequential errors. Preserve the raw output when adding corrections or reevaluating against a corrected key.
