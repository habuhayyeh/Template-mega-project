# V3 extraction experiments

Home for the targeted Doximity tests on `third-version`.

**Current state:** workspace created; packets, method prompts, and reference answers have not been authored. No runs have been performed.

[Approved strategy](../../reviews/V3_TARGETED_TESTING_PLAN.md) · [Initial run matrix](MATRIX.md) · [Failure log](FAILURES.md)

## Materials

| Location | Contents | Sent to Doximity? |
|---|---|---|
| [packets/](packets/README.md) | Complete synthetic encounter packets: transcript, chart material, and current clinician assessment/exam/plan. | One packet per run. |
| [prompts/](prompts/README.md) | Three complete method prompts: A source-first, B meaning-first, C assessment-guided. | One prompt per run. |
| [shared/](shared/README.md) | Common source-fidelity and output requirements included identically in all method prompts. | Through the complete prompt. |
| [references/](references/README.md) | Reviewed semantic expectations for each packet, including expected changes and invariants. | No. |
| [runs/](runs/README.md) | Exact submitted inputs, raw outputs, runtime details, and evaluations. | Only the recorded input is submitted. |

## Initial pilot

One baseline and three variants, tested with A/B/C and two fresh repetitions per combination: **24 planned outputs**. See [the matrix](MATRIX.md). This is an initial screen, not proof of reliability or production acceptance.

Prompt versions change the extraction method. Packet variants change the clinical input or its expression. All methods receive the same packet version and share the same expected meaning.

## Next work

1. Create the baseline packet and its semantic reference answer.
2. Obtain clinician review of the expected handling before evaluating model output.
3. Derive the causal-target, mixed-statement, and management variants, each with its own reviewed expectations.
4. Write the three comparable method prompts using the same shared requirements.
5. Freeze one input revision for the comparison, then run the matrix in Doximity and retain every output.

Packet and prompt filenames listed in the folder guides are reserved names, not existing completed artifacts. A folder guide is not a runnable prompt or a reference answer.

## Record keeping

Pin the git commit containing each prompt, packet, shared requirement, and reference version in the run record. Keep raw output unchanged; put evaluation and corrections in separate files. Preserve failed runs. A revised prompt or packet requires a new comparison batch rather than overwriting an earlier run.

Keep the six-section worksheet fixed during this comparison. Original source material controls the expected meaning; prior model extractions do not. Clinical fidelity is reviewed separately from mechanical formatting.

Initial packets will be explicitly labeled synthetic. Repository data rules in [AGENTS.md](../../AGENTS.md) and D-010 apply to every future upload.
