# PROJECT

## What this is

A neurology note-generation system for Doximity: encounter material in — recording, dictation, prior records — one source-faithful note out. A working semantic substrate is built once, then consumed by two independent branches: a concise Assessment & Plan, and the note body.

## Goal

Every line of the output is traceable to something the encounter contains. The clinician's own reasoning survives organization; it is not replaced by downstream inference. Nothing is added.

## Shape

```text
encounter sources
  → 01 decompose → 01V validate → frozen O# substrate
        ├── A/P branch:  02 → 03 → 04 → 05
        └── body branch: 06 → 07 → sections
```

The two branches never consume each other's intermediate output. Both read the same frozen substrate.

## Non-goals

- A comprehensive clinical database.
- A provenance ledger or per-item metadata schema beyond what a defect forced.
- Grading rubrics, severity classes, or scoring apparatus built before a real defect exists.
- Any content the encounter does not contain: norms, negatives, reassurance, attestation.
