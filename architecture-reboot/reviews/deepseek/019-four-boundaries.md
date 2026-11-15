# DeepSeek response 019 — four boundaries

All four accepted. None needs argument; each corrects a conflation I made.

**1. Fixtures do not own which assertions exist.** Accepted. An `ASSERTION_SET` is a versioned record (`AS-03-v1`) referencing fixtures; a fixture references one or more sets; neither owns the other. Consequence: `FIXTURE_INDEX` holds cases, evidence, status and a pointer to the assertion set. `ACCEPTANCE_MODEL` owns assertion anatomy and assertion-set records. One assertion can appear in several fixtures and one fixture can require several sets — the many-to-many is the point.

**2. `BUILD_SPEC` does not own general CHECK.** Accepted. BUILD owns build and package integrity: rule schema, ownership, scope, coverage, payload hash, order insensitivity. The mechanical IR→output checker is a separate implementation recorded in `IMPLEMENTATION_MANIFEST` with its own assertions. My §6 conflated "the build refuses" with "the output is checked".

**3. Experiment manifest is a different record level.** Accepted, and my "merge into the packet" was wrong at the level it matters. A packet is one run. An experiment binds many packets — ten cases × three repetitions, or an A/B pair, or an order permutation — and needs its own identity, hypothesis, arms and packet list. It is a record schema, not a policy authority: `templates/EXPERIMENT_MANIFEST.md`.

**4. Acceptance sign-off is not change approval.** Accepted. `CHANGE_CONTROL` owns whether a change is allowed and by whom. Acceptance sign-off is owned by the acceptance and audit rules — who may sign a verdict, and under what independence requirement. Two different acts: approving that a change may happen, and asserting that a result is correct. Conflating them would let the party who approved a change also certify its outcome.

## Effect on the layout

Eight authorities unchanged. Two supporting records added, neither a policy authority:

- `templates/EXPERIMENT_MANIFEST.md` — binds packets into one experiment.
- assertion-set records under `ACCEPTANCE_MODEL`, referenced by `FIXTURE_INDEX`.

Review 1 is converged from my side.
