# DeepSeek response 036 — 059, seven questions

**1. Yes.** S1 must own the candidate partition — which subjects become candidates, and which candidate claims attach to which candidate. D1 is not a rename; it is an authority statement. Without it, "candidate" remains a label applied by whoever is writing the prompt, and the cross-candidate question stays unanswerable.

**2. Yes, and the field list was wrong.** I assigned S3's selected representation, S1's order inputs, and S4's own outputs to a "projection S4 consumes" — three different owners in one list, with S4's outputs among its inputs. `S4_INPUT_VIEW` is the correct construction: a composite of legitimately projected inputs, owned by nobody, assembled by the seam.

**3. What S4 needs from the selected representation:**

- the representation id;
- its member object ids **with roles already assigned by S2** (head, modifier, condition, covered);
- the problem it belongs to;
- for each member, the semantic payload S2 attached — the object's text and provenance, not the adjudication history that produced them;
- the S3 retention list for that problem (what may be rendered at all).

Not needed: unselected alternatives, candidate relations, adoption verdicts, duplicate groups, or the reasoning trail. S4 groups, assigns operators and orders; it never re-adjudicates.

**4. Yes.** `S4-PROJ-01` proves the input package contains only permitted fields. It cannot prove the model ignored raw source still visible in the same context. Packaging least privilege and runtime non-leakage are different claims, and only AX-LEAK and the S1S2-D adversarial arms can speak to the second.

**5. Yes — recoverability alone is insufficient.** `A; therefore B` preserves both spans and invents causality. Recoverability detects deletion and reordering; it cannot detect an added bridge. I proposed a criterion that tests one failure mode and implied it tested both.

**6. It belongs in DC-002, with one refinement.** The bridge allowlist should be **closed and empty by default**: R2 permits whitespace, punctuation and capitalisation only; any connective requires an explicit entry on the allowlist, and entries are admitted only when the connector is semantically empty (a comma, a semicolon, a full stop). A connective that carries a relation — `therefore`, `then`, `despite`, `because`, `but` — is never admitted, because the relation must come from the source or from a unit.

That makes the weak-R2 boundary operational: the default is that R2 cannot add a bridge, and every addition is a recorded exception rather than a judgement. I have no smaller alternative that is interface-safe.

**7. `managed_today` must be defined as an observation, not a conclusion:**

> `managed_today: true` means a management statement referencing this subject appears in the current encounter. It records that a statement exists, not that the subject is a problem, adopted, or current.

Two guards: the field is boolean and carries its originating span id (`managed_today_span`), and adoption verdicts are forbidden in S1 regardless of this flag. If a reviewer cannot point at the span, the flag is not set.

---

## Position

I accept all five corrections, including the D3 error and the R2 insufficiency. Revised DC-002 is D1–D4 as you list them, with the bridge allowlist closed-and-empty-by-default and `managed_today` defined as a span-backed observation.

Program and experiment changes stay outside DC-002 — including AX-LEAK's semantic-leak extension, the AX-T gate, and the S4 ordering contract, each of which is a prerequisite or a program decision rather than an interface edit.

Ready to draft exact DC-002 patch text on your word. Nothing applied.
