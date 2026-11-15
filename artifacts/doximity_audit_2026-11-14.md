# Doximity audit, 2026-11-14 — provenance check before use

An external audit was run on "the same dispatcher and same four inputs: `05`, `AP_ANCHOR`, `STANDING_ITEMS`, `handoff_v2.txt`", scoring `ap_run1.txt`, `ap_run2.txt`, `ap_run3.txt`.

**The files it scored are not those inputs.** They are the local P003 mock runs, `runs/2026-11-14-p003/ap_run1..3.txt`, which used `handoff.txt` (v3, containing O54) and no `STANDING_ITEMS.md`.

Verification, from the stored files:

| Marker in the audit | mocks | set 1 | set 2 | set 3 |
|---|---|---|---|---|
| all three omit `Seizure precautions` | yes | yes | no | no |
| run1 contains `residual mild expressive aphasia` | yes | no | yes | no |
| run3 says `about two minutes` | yes | no | no | no |

Only the mock set matches all three. The audit's own file names match the mock naming.

## What that invalidates

- **D5, "hallucinated aphasia".** Not a hallucination. O54 was present in `handoff.txt`, which those runs used. The mock set was scored, not the v4 Handoff.
- **D6, "standing items omitted in all three".** The package had no `STANDING_ITEMS.md`. Already recorded as a packaging defect, and already fixed: set 2 and set 3 both carry `Seizure precautions` in all three runs.
- Any statement about `handoff_v2.txt` or the four-file package is about a run set that was not scored.

## What survives

The audit's structural findings do not depend on which set it read. They match ours and go further:

- **D1 surface normalisation** is a real violation in the mock set (`about two minutes` in run3) and a real risk in any set. Mechanically enforceable.
- **D2 evidence identity, D3 COURSE typing, D4 reasoning identity, D7 management canonicalisation** are semantic decisions the writer is being asked to make fresh each run. That is the same failure set 3 showed as grouping instability.

## Where it goes further than P006

P006 handles rendering groups. The audit proposes moving four more decisions upstream:

1. evidence merged to one canonical row per fact, with combined source tags;
2. `COURSE` delivered pre-typed — `STATUS`, `MODIFIER(target)`, `INDEPENDENT`, `IRRELEVANT`;
3. `CLAIM_QUALIFIER` de-duplicated to distinct propositions upstream;
4. `MANAGEMENT` collapsed to one entry per decision, conditional state preserved;
5. triggered standing items injected as explicit management rows with a `Standing` source.

If that is right, P006 as written is too narrow: it addresses the rendering of groups but leaves the writer still classifying `COURSE` and still choosing between management duplicates.

## Recommendation

Do not act on the audit's premises, but take its boundary. Either widen P006 into a single pre-`05` normalisation pass that produces typed `COURSE`, merged evidence, canonical management, injected standing items and the render groups, or split it: P006 for groups, P007 for the rest. That is a reviewer call, and it is the next decision I need.
