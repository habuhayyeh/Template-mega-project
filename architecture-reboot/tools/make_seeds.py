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
PREDICATE_SET = "PILOT-1"


def load():
    with open(os.path.join(CASE, "parent.json"), encoding="utf-8") as fh:
        return json.load(fh)


def sha(obj):
    return "sha256:" + hashlib.sha256(
        json.dumps(obj, sort_keys=True).encode("utf-8")).hexdigest()[:16]


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
        "salience": {}, "candidate_claims": [],
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
    before = {"adoption": rec["adoption"], "evidence": rec["evidence"]}
    rec["adoption"] = True
    rec["evidence"] = ["S02"]
    return [("/s2/adjudication/0", before, {"adoption": True, "evidence": ["S02"]})]


def m_s3_01(a):
    a["s3"]["rendered"][0]["approved_representation"] = None
    return [("/s3/rendered/0/approved_representation", "R1", None)]


def m_s3_02(a):
    a["s3"]["rendered"][0]["selected_rep"] = "R-999"
    return [("/s3/rendered/0/selected_rep", "R1", "R-999")]


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
]


def main():
    os.makedirs(OUT, exist_ok=True)
    parent = load()
    manifest = {
        "case": parent["case"],
        "predicate_set": PREDICATE_SET,
        "parent_hash": sha(parent),
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

    with open(os.path.join(OUT, "MANIFEST.json"), "w",
              encoding="utf-8", newline="\n") as fh:
        json.dump(manifest, fh, indent=2)

    print("wrote %d artifacts (predicate set %s)" % (len(SEEDS) + 2, PREDICATE_SET))


if __name__ == "__main__":
    main()
