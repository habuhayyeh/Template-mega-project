# Review 129 — stale F1V V1 execution after V2 was active

## Verdict

**INVALID AS A TEST OF F1V V2.**

The returned validation block explicitly identified itself as:

```text
@@VALIDATION F1V_RECONCILE_V1
STATUS=REPAIRED
```

and did not emit the mandatory per-item VERIFY ledger required by F1V V2.

Therefore this run cannot be used to judge whether the V2 validator architecture works.

## Additional observation

The validator claimed that minor repairs were applied, but the corrected handoff still retained the same
structural content in several previously problematic areas. Because the wrong validator version ran,
that is not evidence against V2.

## Action

Do not change F1 or F1V based on this run.

Repeat only the validator stage using the current canonical:
`01V-RECONCILED-EVIDENCE-VALIDATOR.md`

Expected first line:
```text
@@VALIDATION F1V_RECONCILE_V2
```

Expected body:
- one VERIFY line for every FACT;
- one VERIFY line for every SOURCE_REASONING item;
- one VERIFY line for every UNRESOLVED item.

Any validator output lacking that ledger is not a valid V2 run.
