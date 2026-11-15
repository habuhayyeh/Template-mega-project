# CHANGE_CONTROL — four categories, four levels of scrutiny

The categories exist because on the old work a change that moved the goalposts was recorded as a patch, and nobody noticed the goalposts had moved.

## 1. PATCH

Typo, formatting, comment, link, whitespace. No behavioural effect.

Requirements: none beyond a commit. Must not touch a rule, a check, a fixture, or a contract statement.

If a "patch" changes any word that governs behaviour, it is not a patch.

## 2. IMPLEMENTATION CHANGE

A change that does not alter any contract, interface, or acceptance property — regardless of how many files it touches. Observed outputs may vary within those properties. Moving code between files is not a design change; changing what a consumer may rely on is.

Examples: rewriting an internal routine, improving error messages inside the module, refactoring internals.

Adding, removing, or altering a check or assertion is **not** an implementation change. See §4.

Requirements:
- the module's frozen contract and acceptance properties still hold. Observed outputs may change; frozen properties may not.
- no contract file changes;
- the reviewing agent confirms the contract, interface and acceptance properties are unchanged, and runs the module's regression fixtures. Diffs are judged by properties, not by size.

## 3. DESIGN CHANGE

Any change to the architecture, a submodule's goal or interface, a shared contract, or a decision that affects more than one module.

Requirements:
- written proposal with the problem it solves;
- review by the other agent;
- signer approval if it touches style, clinical behaviour, or product;
- all dependent fixtures re-run, and the results recorded.

A design change invalidates prior acceptance results. Re-running them is not optional; it is how non-local regression (C14) is found.

## 4. ACCEPTANCE CHANGE — the category we were missing

Any change to a fixture, an expected property, a deciding check, a threshold — **or the addition or removal of a check or assertion**.

Adding a test changes what is measured, and a test added after an implementation exists is a test shaped by that implementation.

This is the most dangerous category, because it makes a failing test pass without fixing anything.

Requirements:
- the change, and why the old expectation was wrong — not why it was inconvenient;
- explicit approval from the reviewer who wrote the original expectation;
- the old and new expectation both recorded in the fixture register with a date;
- if the change was prompted by a failing implementation, it is **still** an acceptance change — but it must show, from evidence, that the old expectation was wrong. If the correction implies an architectural change, a separate linked `DESIGN CHANGE` is recorded; the two are not merged and neither substitutes for the other.

A pattern of acceptance changes against the same fixture is evidence the architecture is wrong, and should be escalated rather than absorbed.

## 5. Who signs what

| Category | Engineer | Reviewer | Signer |
|---|---|---|---|
| PATCH | may proceed | none | none |
| IMPLEMENTATION CHANGE | may proceed | confirms invariance, runs regression | none |
| DESIGN CHANGE | proposes | reviews | approves if clinical/style/product |
| ACCEPTANCE CHANGE | may not self-approve | approves | **approves** when it alters a clinical baseline expectation |

The engineer may never approve an acceptance change alone. That rule exists because the engineer is the party most motivated to make the test pass.

The signer approves or is informed as set out in this section. "Informed" means notified before the change is used in any acceptance result — not archived silently.

## 6. Recording

Every change above PATCH is recorded in one line in `CHANGELOG.md`:

```text
2026-11-16  ACCEPTANCE CHANGE  F-09  expected "seizure precautions present" → "present or justified absent"  reason: trigger condition was ambiguous in the fixture, not in the system  approved: reviewer
```

If a change is not recorded, it did not happen, and the next person will re-litigate it.
