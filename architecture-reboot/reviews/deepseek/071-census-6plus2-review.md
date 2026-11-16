# DeepSeek review — six primary buckets + two flags

**Verdict:** ACCEPT the structure, with one correction: allow **action-only** records.

## What is right

- Six content families are a coherent partition.
- `action_records` and `baseline_comparator_records` are properties, not content families.
- One primary bucket by default is the right rule.
- Flags may overlap any primary bucket.
- Actions keep their target domain.
- `reasoning_records` is a real content family.
- `background_records` is positively defined, not “everything else.”
- The census is retained for inventory, not clinical interpretation.
- The fixture plan is strong.

## The gap: action-only records

The design says every record has one primary bucket, with flags as modifiers. Some records have no
content-family payload at all:

- `T023` — discussed inpatient vs outpatient, favored inpatient;
- `T024` — counseling on safety precautions and driving restriction;
- pure referral/follow-up or level-of-care actions;
- pure “no further action” decisions.

These are management actions, not background, medication, investigation, exam, reasoning or current-episode
content. Forcing them into `background_records` would create the new garbage bucket the review warns about.

### Correction

Allow a record to have:

```text
zero primary buckets + action_records flag
```

when its only clinically relevant content is a management action.

Amend the rule:

> Default one primary bucket per record. A record may have no primary bucket when its only clinically
> relevant content is a management action; it must appear in `action_records`. Do not force it into
> `background_records`.

This keeps `action_records` a flag, not a competing content family, while keeping action-only records
discoverable.

## Fixtures to add

1. pure safety/driving counseling -> action flag only;
2. admission/disposition recommendation -> action flag only;
3. referral/follow-up action -> action flag only;
4. medication start -> medication primary + action flag;
5. investigation order -> investigation primary + action flag;
6. pure consult/logistics with no clinical content -> uncensused.

Pass criteria:

- action-only fixture appears in `action_records`;
- it does not appear in `background_records`;
- medication/investigation actions retain their target primary bucket;
- no fixture is forced into a primary bucket just to satisfy the one-primary rule.

## Background-risk mitigation

Keep the review’s rule:

> `background_records` is never a fallback. A record enters only because it contains positively identifiable
> prior/baseline/family/social/non-neurologic background information.

If a record fits no primary family and is not action-only, treat that as taxonomy failure; do not hide it in
background.

## What to change in the prompt

- replace the eight peer categories with six primary + two flags;
- state the one-primary default;
- add the action-only exception;
- keep flags non-exclusive;
- keep record IDs only;
- add the fixtures before model testing.

No new stage. No selectors. No action-state enums.

No acceptance or production change.
