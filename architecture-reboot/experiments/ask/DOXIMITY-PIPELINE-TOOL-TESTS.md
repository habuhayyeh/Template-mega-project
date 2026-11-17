# Doximity pipeline tool tests — schema, state, clinical tools

Run each test in a fresh Ask conversation unless the test says otherwise.

---

# Test 4 — JSON schema adherence

## Purpose

Check whether Ask returns JSON that conforms to a strict schema, not just “some JSON.”

## Prompt

```text
Read the complete Scribe packet below.

Return exactly one JSON object and nothing else. No prose, no code fence.

Schema requirements:

- root object has exactly one key: "coverage"
- "coverage" is an object with exactly these eight keys:
  current_event_records, background_records, medication_records, exam_records,
  workup_records, reasoning_records, action_records, baseline_comparator_records
- every value is an array of strings
- every string is a record ID that appears in the packet
- no extra keys
- empty bucket = []

BEGIN SCRIBE PACKET

<paste the complete Scribe packet here>

END SCRIBE PACKET
```

## Pass criteria

External parser must confirm:

1. valid JSON;
2. exactly one root key, `coverage`;
3. exactly eight coverage keys;
4. every value is an array;
5. every item is a string ID present in the packet;
6. no duplicate IDs within a bucket;
7. no prose or code fence.

## Fail criteria

- code fence;
- prose before/after JSON;
- missing/extra keys;
- string instead of array;
- any non-ID value;
- invented IDs.

## What it tells us

If it passes, JSON schema adherence is usable for the pipeline. If it fails, the JSON prompt needs a stricter template or an external repair/retry loop.

---

# Test 5 — multi-turn state

## Purpose

Check whether Ask carries the frozen coverage from one turn to the next without re-pasting it.

## Turn 1

Use Test 4 or the normal JSON coverage prompt with the packet.

## Turn 2

```text
Using only the coverage JSON above, answer with one line and nothing else:

first_current_event=<first ID in current_event_records>; action_count=<number of IDs in action_records>
```

Expected for the known packet:

```text
first_current_event=T004; action_count=7
```

## Turn 3

```text
Without re-reading the packet and without regenerating coverage, answer with one line:

baseline_ids=<IDs in baseline_comparator_records, comma-separated>
```

Expected:

```text
baseline_ids=T016,T017
```

## Pass criteria

- Turn 2 returns the exact first ID and count.
- Turn 3 returns the exact baseline IDs.
- It does not ask you to re-paste the packet or coverage.
- It does not regenerate a different census.

## Fail criteria

- asks for the packet again;
- returns a different count/list;
- says it has no memory of the prior turn;
- regenerates coverage.

## What it tells us

If it passes, the two-turn coverage → synthesis flow can rely on conversational state. If it fails, paste the frozen coverage into every downstream turn.

---

# Test 6 — built-in clinical tools

## Purpose

Check whether Ask exposes clinical tools/databases, rather than only model knowledge.

## Prompt 6A — disclosure

```text
List any clinical tools, drug databases, reference databases, or external lookups you can access in this chat. If none, reply exactly NO_TOOLS. Do not list general model knowledge as a tool.
```

## Prompt 6B — drug lookup

```text
Use your drug lookup or clinical reference tool, if one exists, to check the interaction between levetiracetam and a combined oral contraceptive. State whether the answer came from an external database/tool or from general model knowledge. If no tool exists, reply exactly NO_TOOL.
```

## Prompt 6C — documentation tool

```text
Can you create a downloadable document file in this chat, or only return text? Reply exactly DOWNLOADABLE_FILE or TEXT_ONLY.
```

## Pass criteria

- 6A names a specific tool/database, not “I can answer from knowledge.”
- 6B distinguishes external lookup from model knowledge and gives a source/identifier.
- 6C gives a verifiable file capability, not a promise.

## Fail criteria

- claims a tool but cannot name or cite it;
- answers 6B from memory while implying a lookup;
- says it can create a file but only returns text;
- refuses or says NO_TOOLS / NO_TOOL / TEXT_ONLY.

## What it tells us

Tool claims are weak evidence unless the model can name the source or produce a verifiable artifact. For the pipeline, assume no clinical tool unless proven.

---

# Summary

- Test 4: can it hit a strict JSON schema?
- Test 5: can it hold frozen coverage across turns?
- Test 6: does it have real clinical tools, or only model knowledge?

Do not treat a plausible clinical answer as proof of a tool.
