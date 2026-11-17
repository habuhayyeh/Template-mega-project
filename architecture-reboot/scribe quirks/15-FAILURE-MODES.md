# Failure modes in the Doximity tests

**Purpose:** describe the recurring test failures, how they happened, why, how to diagnose them, and how to
avoid them.

Most were test-contract defects, not model randomness.

---

## 1. Ambiguous expected output

**How it happened**

The prompt named a result but not its exact shape, order or line breaks:

- `S1_ROUTE=<sections JSON>` — wrapper omitted in one run;
- `FINAL:` followed by items — one run joined every item with spaces;
- handoff V2 expected HPI first even though the rule said Stage A order.

**Why it happened**

Natural-language placeholders leave more than one valid serialization. The model chose a plausible one; the
test expected a different one.

**How to diagnose**

- Ask: is the exact shape, key order, item order and newline behavior written down?
- Parse both outputs. If parsed values match but raw text differs, the contract was underspecified.
- Check whether the test’s expected output follows the test’s own ordering rule.

**How to avoid**

- Give an exact template, not a placeholder noun.
- State required keys, order and line breaks.
- Make the expected output follow the same rule.
- Separate semantic comparison from byte comparison.

---

## 2. No clear gold output

**How it happened**

Free synthesis was run three times and judged against exact labels. No adjudicated reference existed. Runs
produced 12/14/12 units, 5/6/7 actions and 0/5/3 unresolved entries.

**Why it happened**

Semantic synthesis has multiple defensible outputs. Without a gold standard, “different” was misread as
“wrong.”

**How to diagnose**

- Can you write one canonical answer by hand?
- If not, the test cannot be exact.
- Check whether differences are labels, ordering or genuinely different clinical content.

**How to avoid**

- Test invariants: fixed IDs, types, counts, action coverage, unresolved set.
- Or freeze one adjudicated facts JSON and test D-S/D-T on that.
- Do not compare free labels exactly.

---

## 3. Under-specified schema and field counts

**How it happened**

- `@@PROBLEM` stopped after four fields instead of nine.
- A keyed one-item test truncated `P001` and `CU001`.
- `unresolved=no` appeared where `NONE` was required.
- JSON trace placeholders were copied instead of filled.

**Why it happened**

Long positional records invite field loss. The model does not reliably count separators across free text.

**How to diagnose**

- Count fields per record.
- Check required keys and types.
- Identify the first missing field.
- Check whether the prompt used a placeholder that could be copied.

**How to avoid**

- Use JSON objects with named keys.
- Show the exact schema.
- Split large outputs into smaller stages.
- Validate required keys before judging content.

---

## 4. Fallback allowed

**How it happened**

The first handoff test allowed Stage B to use both Stage A and `FACTS`. Stage A lost IDs in some runs, but
Stage B still produced correct labels and IDs. That proved Stage B reread `FACTS`.

**Why it happened**

The prompt did not ban fallback and had no sentinel. The model took the easier source.

**How to diagnose**

- Remove the source from Stage B and rerun.
- Add a sentinel that exists only in Stage A.
- If a “correct” line lacks the sentinel, Stage B cheated.

**How to avoid**

- Stage A carries every field Stage B needs.
- Stage B uses only Stage A.
- Missing field returns `HANDOFF_ERROR`.
- Add a sentinel and require it in every output line.

---

## 5. Format fragility

**How it happened**

- Custom `@@` output records collapsed or emitted only `@@END`.
- Pipe-delimited records rendered as Markdown tables.
- YAML lost indentation under `coverage`.
- `<done>` was stripped and became an empty string.

**Why it happened**

Doximity and its renderer treat these characters as control, Markdown or HTML syntax, not plain data.

**How to diagnose**

- Test the same content in plain text.
- Test a neutral token with no `<`, `[`, `|` or `@@`.
- Compare raw output with parsed output.
- Check whether only the special-character field failed.

**How to avoid**

- Use JSON for structured handoffs.
- Do not use `@@` output records.
- Do not use `|` as a delimiter.
- Avoid angle brackets and bracket sentinels; use plain tokens such as `WRAP_done`.
- Compare JSON semantically, not by whitespace.

---

## 6. Too much in one prompt

**How it happened**

- Coverage plus synthesis in one prompt omitted whole coverage categories.
- Eight categories at once dropped `current_event` and `action_bearing`.
- A 12-call test had one `F_WRAP` miss while all other calls matched.

**Why it happened**

Multiple functions compete for attention and output budget. The model satisfies most of the prompt and drops
the rest.

**How to diagnose**

- Count required sections or calls.
- Locate the first omission.
- Run that function alone.
- Check whether the omission moves when the prompt order changes.

**How to avoid**

- One function per prompt.
- Split coverage and synthesis.
- Split large call scripts.
- Add required counts, but do not rely on counts alone.

---

## 7. Implicit ordering

**How it happened**

A routing test said “preserve input order” while items came from separate `problems`, `units`, `actions` and
`unresolved` arrays. One run put `CU006` before `P001`; another put problems first.

**Why it happened**

There is no single input order across separate arrays. The model grouped by type or array.

**How to diagnose**

- Reorder input arrays and rerun.
- If output order changes without an explicit rule, ordering is undefined.
- Check whether every item has a numeric `order`.

**How to avoid**

- Put `order` on every item.
- Sort by numeric `order`.
- State section order separately.
- Make the expected output follow the same rule.

---

## 8. Test hygiene

**How it happened**

- The packet placeholder `<paste the complete Scribe packet here>` was left in place; the model correctly
  said no packet was present.
- The expected JSON sat in the same file as the prompt.
- Old attachment versions were reused after a fix.
- One run was treated as determinism.
- The exact failing prompt version was edited and lost.

**Why it happened**

Copy/paste boundaries, stale files and no version tracking.

**How to diagnose**

- Check the packet’s first and last record IDs.
- Check whether the prompt has an expected block attached.
- Check file names and timestamps.
- Count fresh runs.
- Confirm the prompt version matches the test record.

**How to avoid**

- Replace every placeholder explicitly.
- Keep expected output in a separate file or clearly below “do not paste.”
- Version prompt files; never overwrite a failing version.
- Run three fresh times.
- Record prompt file and run count in the traceability table.

---

## One-line rule

> Before blaming the model, check whether the prompt defined the exact shape, the gold, the field count, the
> fallback rule, the sentinel, the order and the run count.
