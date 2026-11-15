# Architecture Reboot V2

This directory is the design arena for a clean-sheet redesign of the neurology note-generation system.

## Why this exists

The current implementation taught us a great deal about:

- reproducibility failures;
- semantic duplication;
- historical vs current management;
- provenance;
- clinician reasoning;
- Doximity packaging;
- the limits of asking a final writer to make too many semantic decisions.

Rather than continue patching the existing architecture indefinitely, this branch starts from first principles.

## Current phase

**Architecture only. No production implementation.**

## Start here

1. `WORKING_RULES.md`
2. `proposals/chatgpt/001-state-model-and-view-renderers.md`
3. DeepSeek should write its critique under `reviews/deepseek/` and append a handoff to `channel/to-chatgpt.md`.

## Branch

`architecture-reboot-v2`

The existing `main` branch remains the current implementation/history and should not be modified as part of this clean-room design discussion.
