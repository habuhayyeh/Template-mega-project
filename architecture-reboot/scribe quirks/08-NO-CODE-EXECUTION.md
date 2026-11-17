# No code execution in Doximity Ask

**Evidence class:** REPRODUCED
**Date:** 2026-11-16
**Scope:** Doximity Ask, clinical workflow.

## Finding

Doximity Ask does not execute code. It generates text and refuses or declines code-execution requests.

The exact SHA-256 hash never came back from any test. That is the falsifier.

## Observed results

- Python: `NO_RUNTIME`.
- Node.js: `NO_RUNTIME`.
- PowerShell: `NO_RUNTIME`.
- Bash: refused the shell test.
- R: explained the code, said it could not execute it, told the user to run locally.
- Go: explained the code, told the user to run it locally.
- PHP/Ruby/Perl/Java/R batch: generic refusal — Ask is for clinical/medical tasks, not code execution.

`NO_RUNTIME`, a policy refusal, and a code explanation are all negative evidence. None is execution.

## Rules

1. Do not design Doximity stages that require code execution.
2. Do not use Ask to compute hashes, read files, call APIs, or run scripts.
3. Code-shaped prompts may simulate an algorithm; that is not execution and has no side effects.
4. Put all executable logic outside Ask: parser, validator, retries, state, rendering.
5. Doximity's role is text generation, including JSON generation.
6. If execution is ever suspected, require an exact hard-to-fake result (for example SHA-256 of a fixed
   nonce). A plausible explanation is not proof.

## Test method

Use a fixed nonce and a language snippet that prints its SHA-256. Do not include the expected hash in the
message. Any exact match is evidence of a runtime; refusals, `NO_RUNTIME`, or wrong hashes are negative.

Related test:

- `../experiments/ask/DOXIMITY-CODE-EXECUTION-TEST.md`
- `../experiments/ask/DOXIMITY-MULTILANGUAGE-TEST.md`

## Consequence

The pipeline is split:

```text
Doximity: generate JSON
External code: parse, validate, retry, store, render
```

Do not ask Doximity to be the runtime.
