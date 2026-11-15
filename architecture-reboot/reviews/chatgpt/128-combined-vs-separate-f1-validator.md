# Review 128 — combined vs separate File 1 validator execution

## Compared conditions

A. **Combined file:** F1 and F1V merged into one file.
B. **Separate files:** F1 followed by F1V as separate files in one Ask run.

## Result

**Separate-file execution is the better shape, but F1V V1 falsely passed.**

### Combined file

The combined condition produced a plausible F1 handoff but did not expose a distinct validator audit/result.
That makes it impossible to tell whether validation actually occurred or whether the model simply generated
one answer under a larger prompt.

The combined handoff still contained bounded fidelity errors, including:
- unrelated/question-only refs;
- unsupported negative history expansion;
- action-state interpretation;
- diagnostic possibilities introduced in UNRESOLVED.

Conclusion: merging validator instructions into F1 reduces observability and does not provide reliable
adversarial checking.

### Separate files

The separate condition explicitly emitted:

```text
@@VALIDATION F1V_RECONCILE_V1
STATUS=PASS
```

but the handoff still contained violations that F1V was supposed to catch.

Examples:
- question-only refs remained in FACT citation lists;
- some refs were irrelevant to the clause they supposedly supported;
- prospective ED workup remained embedded in FACT;
- source reasoning remained mixed into some FACTs;
- some negative medication/social statements exceeded the captured answers.

Therefore the validator **ran**, but it rubber-stamped the output.

## Interpretation

The problem is not that validators are useless.

The problem is that F1V V1 allowed a global PASS without forcing source-by-source adversarial inspection.

The next validator version should require an observable item-level verification ledger before PASS.

## Decision

Keep F1 and F1V as separate files.

Do not merge them for the active experiment.

F1V V2 must emit one compact VERIFY line for every F1 item across:
- reference existence;
- local support;
- question-as-answer;
- action fidelity;
- attribution;
- semantic boundary;
- downstream separability.

PASS is forbidden if any item is omitted or any applicable check fails.

## Escalation rule

Run F1V V2 against the already-produced F1 output; do not rerun F1.

If F1V V2 still falsely passes obvious defects, the next test should be **validator in a fresh Ask session**
rather than adding more validator prose in the same context.
