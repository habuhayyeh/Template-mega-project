#!/usr/bin/env python3
"""Generate Gate 0 seed artifacts from the CASE-01 clean parent.

Each seed is the parent with exactly one mutation. The generator is the
authority on what changed, so a seed cannot drift from its definition.

Usage: python make_seeds.py
"""
import copy
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
CASE = os.path.join(HERE, "..", "experiments", "architecture",
                    "AX-S1S2-D", "fixtures", "CASE-01")
OUT = os.path.join(HERE, "..", "experiments", "gate0", "seeds", "generated")


def load():
    with open(os.path.join(CASE, "parent.json"), encoding="utf-8") as fh:
        return json.load(fh)


def m_s1_01(a): a["s1"]["candidates"][0]["adopted"] = True
def m_s1_02(a): a["s1"]["candidates"][0]["selected_claim"] = "CC1"
def m_s1_04(a): a["s1"]["candidates"][0]["anchors"] = []
def m_s1_05(a):
    a["s1"]["candidates"].append({
        "id": "C2", "subject": "old left MCA infarct", "anchors": ["S01"],
        "salience": {}, "candidate_claims": [], "has_assessment_question": False,
    })
def m_s1_06(a): a["s1"]["candidates"][0]["status_current"] = True

def m_s2_01(a): a["s2"]["representations"][0]["support_refs"] = []
def m_s2_03(a): a["s2"]["adjudication"][0]["temporal"] = "now"
def m_s2_06(a): a["s2"]["adjudication"][0]["adoption"] = True
def m_s2_06_side(a): a["s2"]["adjudication"][0]["evidence"] = ["S02"]

def m_s3_01(a): a["s3"]["rendered"][0]["approved_representation"] = None
def m_s3_02(a): a["s3"]["rendered"][0]["selected_rep"] = "R-999"
def m_s3_04(a): a["s3"]["retained"].remove("O07")

def m_s4_01(a): a["s4"]["problems"].pop()
def m_s4_02(a):
    a["s4"]["problems"].append({"id": "P2", "source": "C9", "order": 2})
def m_s4_04(a): a["s4"]["units"][0]["members"].append("O99")
def m_s4_06(a): a["s4"]["units"] = [u for u in a["s4"]["units"] if u["id"] != "U2"]


SEEDS = [
    ("G0-S1-01", "S1-AUTH-01", m_s1_01),
    ("G0-S1-02", "S1-AUTH-02", m_s1_02),
    ("G0-S1-04", "S1-CAND-02", m_s1_04),
    ("G0-S1-05", "S1-CAND-01", m_s1_05),
    ("G0-S1-06", "S1-AUTH-01", m_s1_06),
    ("G0-S2-01", "S2-REP-01", m_s2_01),
    ("G0-S2-03", "S2-TEMP-01", m_s2_03),
    ("G0-S2-06", "S2-ADOPT-01", (m_s2_06, m_s2_06_side)),
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
    manifest = []

    clean = os.path.join(OUT, "PARENT-CLEAN.json")
    with open(clean, "w", encoding="utf-8") as fh:
        json.dump(parent, fh, indent=2)
    manifest.append({"artifact": "PARENT-CLEAN.json", "expect": "zero findings"})

    for seed_id, predicate, fn in SEEDS:
        art = copy.deepcopy(parent)
        fns = fn if isinstance(fn, tuple) else (fn,)
        for f in fns:
            f(art)
        name = seed_id + ".json"
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
            json.dump(art, fh, indent=2)
        manifest.append({"artifact": name, "must_fire": predicate})

    with open(os.path.join(OUT, "MANIFEST.json"), "w", encoding="utf-8") as fh:
        json.dump({"case": parent["case"], "seeds": manifest}, fh, indent=2)

    print("wrote %d artifacts to %s" % (len(manifest), OUT))


if __name__ == "__main__":
    main()
