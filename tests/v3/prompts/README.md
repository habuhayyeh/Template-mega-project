# Method prompts

Status: not yet authored. Folder documentation is not a runnable prompt.

## Reserved prompt names

| Method | Planned filename | Initial organizing approach |
|---|---|---|
| A | `A_source_first.md` | Extract within each source, then reconcile and associate the statements. |
| B | `B_meaning_first.md` | Organize complete source-linked statements by observations/history, interpretations/relationships, and management. |
| C | `C_assessment_guided.md` | Use the clinician's assessment as a provisional guide, then independently scan for unmatched and contradictory material. |

Each future file will contain a complete copyable prompt. Include the same [shared requirements](../shared/README.md) verbatim in each. Vary the organizing method while holding source-fidelity, reconciliation, architecture, and output requirements constant.

Use all three prompts against every packet. Do not insert packet-specific answers or clinical examples taken from the answer keys.

Keep one current version per method; git retains history. Record the exact prompt commit in each run. Check shared text equality before freezing a comparison. Any revision after testing starts belongs to a new batch and must be evaluated against earlier cases as well as its targeted failure.
