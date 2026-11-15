# DeepSeek response 010 — implementation guidance: agreed

**Answer: yes.** The three corrections are all improvements in precision and none changes the intent. I accept them, with one addition and one condition.

---

## 1. The three corrections — accepted

1. **S1 ordering.** "Acuity then management weight" was a policy I froze by accident. It belongs to the note contract, not the function. `Order by encounter importance under a later explicit note contract` is the right wording; the function decides *that* an order exists and that it is explicit, not what the order is.
2. **S4 "unsupported unit".** Correct — S4 creates units by definition. "Do not invent a unit" read as a ban on construction, which is its job. "Unsupported" is the real boundary.
3. **R1 "outside payload + operator text + transformations".** Correct and more precise than "don't add a word", which was both too absolute (articles exist) and too vague (which words?).

## 2. One addition — make "unsupported" testable

"Unsupported unit" needs a definition, or S4 will interpret it generously. Three conditions, all mechanical:

- every member id exists in the IR;
- every member role is permitted by the operator;
- a unit with zero members is supported only by a closed-list standing item with a satisfied trigger; any other zero-member unit is unsupported.

That gives the failure a name and a check rather than a principle.

## 3. One condition on deferring the ordering policy

When the note contract lands, the order must be:

- **one policy for the whole note**, not per-section improvisation — the failure we had was sections each ordering themselves;
- **declared as data**, so the IR carries the order key and CHECK can verify it without knowing the policy.

If ordering stays a prose instruction inside a section module, it becomes the next thing that drifts, and it will be invisible because the note will still read plausibly.

## 4. What I am not asking for

No prompt text, no schema, no operator list, no error vocabulary. Agreed that those are downstream.

---

**Position:** agreement on the broad implementation guidance is complete from my side. Freeze it.
