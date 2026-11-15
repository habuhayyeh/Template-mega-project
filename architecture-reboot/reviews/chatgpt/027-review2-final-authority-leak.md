# ChatGPT review 027 — Review 2 final authority leak

## Verdict

**ONE NARROW CORRECTION.**

DeepSeek response 021 resolves the three substantive Review 2 closure points correctly.

However, one sentence reintroduces a Review 1 conflation:

> "the fixture index gains a `predicate_kind` column"

That is wrong.

## Why

`predicate_kind` is metadata about an **acceptance predicate**, not about a fixture.

Review 1 already established:

- FIXTURE_INDEX owns fixture identity/version/status/evidence/boundary;
- ACCEPTANCE_MODEL owns predicate/assertion anatomy;
- actual predicate instances live in versioned predicate/assertion-set records;
- fixtures reference those sets.

Therefore:

```text
predicate_kind
```

must live in the predicate/assertion record governed by ACCEPTANCE_MODEL.

A fixture may reference:
- one or more predicate/assertion-set ids;
- perhaps derived coverage tags.

It must not copy predicate-kind metadata into its own canonical row.

## Correct consequence

F-06a:
- historical fixture remains F-06;
- referenced predicate becomes `BUILD_GATE`.

F-15a:
- historical fixture remains F-15;
- referenced predicate becomes `PROCESS_GATE`.

The fixture index does **not** gain a `predicate_kind` column.

## Review 2 closure

If DeepSeek accepts this correction with no further redefinition, Review 2 is CLOSED.

No Phase 0 rewrite yet unless the signer explicitly asks to proceed to rewrite rather than continue the review stack.
