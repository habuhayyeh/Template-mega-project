# DeepSeek response 032 — experiment program disagreements

I accept all six corrections. Three of them fix errors in my review, not differences of taste. Two refinements remain.

**1. Threshold — accepted, and mine was the weaker idea.** An arbitrary fraction is a made-up criterion. "One controlled logical counterexample falsifies a universal authority invariant; execution errors do not" is the right rule, and it is sharper than anything I wrote. My point was only that "unavoidable" is unquantified; the answer is that this program makes no frequency claims, so nothing needs quantifying. Withdrawn.

**2. Literal cross-run IDs — accepted.** I claimed every diff-based score depends on literal ids. It does not: semantic/source-anchor matching is sufficient for diffing, and AX-I3 already specifies it. P5 drops from blocking to a characterisation note inside AX-I3.

**3. S4 with two approved representations — accepted, and my version was wrong in the way I keep warning about.** S3 emits one selected representation; S4 consumes that selection. Asking S4 to reconcile two approved representations would have made S4 do S3's job — the exact authority leak this program exists to detect, smuggled in as a stress fixture. The correct stress case is the one you describe: S2 had several selection-safe representations, S3 selected one, S4 must honour that exact selection.

**4. AX-LEAK without Arm 0 — accepted.** Arms B, C and D test dependence directly; a failure there is unambiguous. My concern was narrower than I wrote: it was that arm A passing does not show the renderer *reads* the IR, only that it did not contradict it. One refinement, not an arm: include a case whose IR carries content **absent from the raw source**, so a correct render proves the IR is the input. That is one fixture, not a fourth arm.

**5. Crossed arm — accepted.** One crossed arm shows one interaction. It does not show the eight claims compose, and I should not have implied it does.

**6. Scale — accepted, with the distinction kept.** Hard truncation is platform-bound; schema burden is schema-first; and a realistic-volume failure that traces to representation design can reopen that design. That is three categories, not two, and my "platform, not architecture" was too neat.

**7. Paste-layout** — agreed as an ingestion/deployment prerequisite for production-shaped claims. I would not spend a ninth experiment on it until a production claim actually depends on layout invariance.

---

## What I would still note, briefly

The program is now strong enough that my remaining concerns are about execution rather than design:

- Gate 0 (calibration) must be run **before** the first scored experiment, not alongside it, or the first results will be scored by an uncalibrated rig.
- The executable manifests freezing case IDs and counts should also freeze **control-plane version** and package version, or two runs of "the same" experiment will differ in ways nobody recorded.

Neither is an architecture question, and neither blocks revising the eight specs.
