# DeepSeek review — A vs direct-B comparator

**Verdict:** BLOCKED by two experimental-design issues. The architecture question is right.

## 1. One run per arm is not enough

The comparator says one fresh session per arm. Prior A2 runs showed material run-to-run variance on
coverage and splitting. A single run per arm can decide the architecture by noise.

Minimum fix:

- run each arm **twice**, fresh sessions, same packet;
- score each run independently;
- direct-B wins only if both runs pass every blocking dimension and are no worse than both A→B runs;
- if the pattern is mixed, do not average; run one targeted follow-up or declare inconclusive.

This is still small: two runs per arm, not a new stage.

## 2. Citation shapes are not directly comparable

Arm A returns A + B. B cites A span IDs, and A cites Scribe records.

Arm B-Direct cites Scribe records/selectors directly.

The comparator says “check every source citation/selector,” but does not define how to audit A→B B
citations through A. Without that mapping, pointer/action scores are not comparable.

Add an audit rule:

- Arm A: B evidence/action refs -> A span IDs -> A source_record/selector -> Scribe.
- Arm B: direct refs -> Scribe.
- For action coverage, normalize both to the same action concept set before scoring.
- Do not penalize A for having an intermediate ID layer; penalize only broken source linkage.

## What is fair

- Same clean packet.
- Same B responsibilities.
- Same problem threshold.
- Same action coverage list.
- Same no-enum rule.
- Separate fresh sessions.
- No C/oracle attached.
- Direct-B must cite exact Scribe records/selectors.
- Decision rule favors fidelity over concision.

## What is right

The comparator focuses on the real question: does A earn its place on a clean packet?

The scoring dimensions are appropriate. The problem threshold rule is now correct. The direct-B arm is
not obviously stronger by prompt asymmetry; it carries both ingestion and synthesis, which is the cost
being tested.

## Required patch

1. two runs per arm;
2. citation/action normalization rule for A→B;
3. predeclare how mixed results are handled.

Then READY TO RUN.

No C, no CLINICAL_UNIT, no production change. No acceptance or Phase 0.
