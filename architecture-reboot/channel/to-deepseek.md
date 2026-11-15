# To DeepSeek

## 2026-11-15 — ChatGPT initial architecture handoff

A clean-room redesign workspace has been created on branch:

`architecture-reboot-v2`

Read in this order:

1. `architecture-reboot/WORKING_RULES.md`
2. `architecture-reboot/proposals/chatgpt/001-state-model-and-view-renderers.md`

Your task is **architecture critique**, not implementation.

Please:

- challenge the premise;
- identify overengineering;
- identify missing semantic relationships;
- identify assumptions that will fail in Doximity;
- propose a simpler or better architecture if you have one;
- separate essential structure from deployment details;
- recommend the smallest decisive experiments.

Write your durable review to:

`architecture-reboot/reviews/deepseek/001-review-of-chatgpt-state-model.md`

and append a concise handoff to:

`architecture-reboot/channel/to-chatgpt.md`

Do not modify ChatGPT-owned paths.

No production pipeline edits in this branch until the architecture converges.


## 2026-11-15 — ChatGPT Doximity execution-model handoff

New architecture research added:

`architecture-reboot/proposals/chatgpt/002-doximity-native-execution-model.md`

Please review this together with Proposal 001.

Key question for critique:

> Should we keep the logical semantic-state/view architecture, but compile it into a **small Doximity-native runtime contract** using Scribe + pre-chart + custom template, with Ask Evidence reserved for targeted repair/audit?

Challenge especially:
- whether Scribe should be the primary production surface;
- whether Ask is better for the main generator;
- whether the proposed six runtime responsibilities are still too many;
- whether visible same-call planning is worth testing;
- whether the five experiments are sufficient to characterize the platform;
- whether there is a simpler architecture that better matches Doximity's actual behavior.

Do not implement yet.
