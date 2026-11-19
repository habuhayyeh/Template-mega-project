# Encounter packets

Status: not yet authored. All initial cases will be synthetic test material.

Each file will be a complete packet ready to pair with any method prompt. Include these three labeled input groups:
1. Encounter transcript with identifiable speakers.
2. Chart material with document/service labels, source dates, and relevant results.
3. Current clinician examination, personal assessment/reasoning, and management decisions.

Use stable source labels so reference answers and reviewers can identify supporting passages. Preserve facts, uncertainty, negation, timing, attribution, and action modifiers in realistic source language.

## Reserved packet names

| ID | Planned filename | Controlled comparison |
|---|---|---|
| P00 | `P00_baseline.md` | Straightforward complete encounter. |
| P01 | `P01_causal_target.md` | Change the target of one stated causal relationship. |
| P02 | `P02_mixed_statement.md` | Express the same finding, interpretation, and action together; preserve their meaning. |
| P03 | `P03_management.md` | Change one action qualifier while preserving all other management details. |

Derive each variant from P00, not from the preceding variant. Preserve unrelated content. If one semantic change requires coordinated source edits to maintain coherence, document all affected passages in the corresponding reference answer.

P01 and P03 change meaning; their keys specify the precise expected change and all invariants. P02 changes expression; its clinical meaning should remain invariant.

Keep expected answers, test explanations, variant differences, and scoring instructions outside submitted packets, in `references/`. Every submitted packet must contain enough source material to support the expected handling without requiring new clinical reasoning.
