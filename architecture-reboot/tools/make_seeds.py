#!/usr/bin/env python3
"""Generate Gate 0 seed artifacts from a clean parent.

The seed specification lives in G0-SEEDS.md; this script implements it and
records, per artifact, the mutation path with before/after values and a content
hash. The manifest is evidence about what changed, not a second authority over
what should change.

Usage: python make_seeds.py
"""
import copy
import hashlib
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
CASE = os.path.join(HERE, "..", "experiments", "architecture",
                    "AX-S1S2-D", "fixtures", "CASE-01")
OUT = os.path.join(HERE, "..", "experiments", "gate0", "seeds", "generated")
PREDICATE_SET = "PILOT-2"


def load():
    with open(os.path.join(CASE, "parent.json"), encoding="utf-8") as fh:
        return json.load(fh)


def file_sha(path):
    with open(path, "rb") as fh:
        return "sha256:" + hashlib.sha256(fh.read()).hexdigest()


def sha(obj):
    # Canonical JSON: sorted keys, fixed separators. Hashing bytes would make
    # the digest depend on formatting; hashing canonical JSON makes it depend
    # only on content.
    canon = json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(canon).hexdigest()


def m_s1_01(a):
    a["s1"]["candidates"][0]["adopted"] = True
    return [("/s1/candidates/0", "<no adopted key>", "adopted=true")]


def m_s1_02(a):
    a["s1"]["candidates"][0]["selected_claim"] = "CC1"
    return [("/s1/candidates/0", "<no selected_claim>", "selected_claim=CC1")]


def m_s1_04(a):
    before = list(a["s1"]["candidates"][0]["anchors"])
    a["s1"]["candidates"][0]["anchors"] = []
    return [("/s1/candidates/0/anchors", before, [])]


def m_s1_05(a):
    a["s1"]["candidates"].append({
        "id": "C2", "subject": "old left MCA infarct", "anchors": ["S01"],
        "salience": {"acuity": "LOW", "managed_today": False},
        "candidate_claims": [
            {"id": "CC2", "text": "known left MCA infarct", "support": ["S01"]}
        ],
    })
    return [("/s1/candidates/-", "<absent>", "C2 substrate-only subject")]


def m_s1_06(a):
    a["s1"]["candidates"][0]["status_current"] = True
    return [("/s1/candidates/0", "<no status_current>", "status_current=true")]


def m_s2_01(a):
    before = list(a["s2"]["representations"][0]["support_refs"])
    a["s2"]["representations"][0]["support_refs"] = []
    return [("/s2/representations/0/support_refs", before, [])]


def m_s2_03(a):
    before = a["s2"]["adjudication"][0]["temporal"]
    a["s2"]["adjudication"][0]["temporal"] = "now"
    return [("/s2/adjudication/0/temporal", before, "now")]


def m_s2_06(a):
    rec = a["s2"]["adjudication"][0]
    before = rec["adoption"]
    rec["adoption"] = None
    return [("/s2/adjudication/0/adoption", before, None)]


def m_s3_01(a):
    a["s3"]["rendered"][0]["approved_representation"] = None
    return [("/s3/rendered/0/approved_representation", "R1", None)]


def m_s3_02(a):
    a["s3"]["rendered"][0]["selected_rep"] = "R-999"
    return [("/s3/rendered/0/selected_rep", "R1", "R-999")]


def m_s3_05(a):
    a["s3"]["candidate_outcomes"] = [x for x in a["s3"]["candidate_outcomes"]
                                     if x["candidate"] != "C1"]
    return [("/s3/candidate_outcomes", "C1 RENDERED", "C1 outcome absent")]


def m_s3_04(a):
    a["s3"]["dispositions"] = [d for d in a["s3"]["dispositions"]
                              if d["object"] != "O07"]
    return [("/s3/dispositions", "O07 dispositioned MEDICATION_RECORD",
             "O07 unaccounted")]


def m_s4_01(a):
    a["s4"]["problems"].pop()
    return [("/s4/problems", "1 problem", "0 problems while S3 rendered 1")]


def m_s4_02(a):
    a["s4"]["problems"].append({"id": "P2", "source": "C9", "order": 2})
    return [("/s4/problems/-", "<absent>", "P2 not in S3 rendered set")]


def m_s4_04(a):
    a["s4"]["units"][0]["members"].append("O99")
    return [("/s4/units/0/members/-", "<absent>", "O99 not in retained")]


def m_s4_05(a):
    a["s4"]["units"][0]["representation"] = "R-999"
    return [("/s4/units/0/representation", "R1", "R-999 against S3 selected_rep R1")]


def m_s4_07(a):
    a["s4_input_view"]["adoption"] = True
    return [("/s4_input_view/-", "<absent>", "adoption: true injected")]


def m_s4_06(a):
    a["s4"]["units"] = [u for u in a["s4"]["units"] if u["id"] != "U2"]
    return [("/s4/units", "U2 present", "U2 removed for retained O05")]


SEEDS = [
    ("G0-S1-01", "S1-AUTH-01", m_s1_01),
    ("G0-S1-02", "S1-AUTH-02", m_s1_02),
    ("G0-S1-04", "S1-CAND-02", m_s1_04),
    ("G0-S1-05", "S1-CAND-01", m_s1_05),
    ("G0-S1-06", "S1-AUTH-01", m_s1_06),
    ("G0-S2-01", "S2-REP-01", m_s2_01),
    ("G0-S2-03", "S2-TEMP-01", m_s2_03),
    ("G0-S2-06", "S2-ADOPT-01", m_s2_06),
    ("G0-S3-01", "S3-INC-01", m_s3_01),
    ("G0-S3-02", "S3-SEL-01", m_s3_02),
    ("G0-S3-04", "S3-ACCT-01", m_s3_04),
    ("G0-S4-01", "S4-INC-01", m_s4_01),
    ("G0-S4-02", "S4-INC-01", m_s4_02),
    ("G0-S4-04", "S4-MEM-01", m_s4_04),
    ("G0-S4-06", "S4-COMP-01", m_s4_06),
    ("G0-S3-05", "S3-CAND-01", m_s3_05),
    ("G0-S4-07", "S4-PROJ-01", m_s4_07),
    ("G0-S4-05", "S4-REP-01", m_s4_05),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    parent = load()
    with open(os.path.join(CASE, "oracle.json"), encoding="utf-8") as fh:
        oracle = json.load(fh)
    base = os.path.join(HERE, "..", "experiments", "architecture", "AX-S1S2-D")
    spec = os.path.join(HERE, "..", "experiments", "gate0", "seeds", "G0-SEEDS.md")
    manifest = {
        "governing_hashes": {
            "predicates.md": file_sha(os.path.join(base, "predicates.md")),
            "schema.md": file_sha(os.path.join(base, "schema.md")),
            "G0-SEEDS.md": file_sha(spec),
            "make_seeds.py": file_sha(os.path.abspath(__file__)),
        },
        "governing_hash_method": "sha256 over file bytes (source text, not JSON)",
        "case": parent["case"],
        "predicate_registry": {"id": PREDICATE_SET, "version": "1"},
        "active_set": "PILOT-ACTIVE-1",
        "specificity_policy": "FULL_SILENCE-1",
        "hash_method": "sha256 over canonical JSON (sorted keys, compact separators)",
        "parent_hash": sha(parent),
        "oracle_hash": sha(oracle),
        "clean_parent": {"artifact": "PARENT-CLEAN.json", "expect": "zero findings"},
        "seeds": [],
    }

    with open(os.path.join(OUT, "PARENT-CLEAN.json"), "w",
              encoding="utf-8", newline="\n") as fh:
        json.dump(parent, fh, indent=2)

    for seed_id, predicate, fn in SEEDS:
        art = copy.deepcopy(parent)
        mutations = fn(art)
        name = seed_id + ".json"
        with open(os.path.join(OUT, name), "w", encoding="utf-8", newline="\n") as fh:
            json.dump(art, fh, indent=2)
        manifest["seeds"].append({
            "artifact": name,
            "must_fire": predicate,
            "mutations": [{"path": p, "before": b, "after": a} for p, b, a in mutations],
            "hash": sha(art),
        })

    # Harmless variation: identical semantics, every id renamed consistently.
    text = json.dumps(parent, sort_keys=True)
    for a, b in (('"C1"', '"CX"'), ('"R1"', '"RX"'), ('"P1"', '"PX"'),
                 ('"U1"', '"UX1"'), ('"U2"', '"UX2"'), ('"U3"', '"UX3"'),
                 ('"CC1"', '"CCX"')):
        text = text.replace(a, b)
    with open(os.path.join(OUT, "VARIATION.json"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(json.loads(text), indent=2))
    manifest["variation"] = {"artifact": "VARIATION.json", "expect": "zero findings",
                             "basis": "identical semantics, all ids renamed"}

    with open(os.path.join(OUT, "MANIFEST.json"), "w",
              encoding="utf-8", newline="\n") as fh:
        json.dump(manifest, fh, indent=2)

    print("wrote %d artifacts (predicate set %s)" % (len(SEEDS) + 2, PREDICATE_SET))


if __name__ == "__main__":
    main()
