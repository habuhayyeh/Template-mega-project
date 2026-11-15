#!/usr/bin/env python3
"""allocate.py - deterministic kind-to-bucket allocation for the frozen substrate.

Development-time tool. Replaces the semantic behaviour of 02 with a pure lookup.

Usage:
    python allocate.py frozen_objects.txt --out allocation.txt

Input:  O1 | KIND | text | [letter, source_name, date]
Output: O1 | BUCKET | KIND | text | [letter, source_name, date]

Mapping (total, mutually exclusive):
    DIAGNOSTIC_FORMULATION -> CLAIM
    ETIOLOGY               -> ETIOLOGY
    OBSERVATION            -> EVIDENCE
    COURSE                 -> COURSE
    MANAGEMENT             -> MANAGEMENT
    DEMOGRAPHIC            -> NOT_ALLOCATED

Guarantees: ID, kind, text, and provenance are copied byte for byte; no merging,
no deduplication, no omission, no invention; every input ID appears exactly once.

Exit 0 = clean, 1 = failure, 2 = usage error.
"""

import re
import sys

KIND_TO_BUCKET = {
    "DIAGNOSTIC_FORMULATION": "CLAIM",
    "ETIOLOGY": "ETIOLOGY",
    "OBSERVATION": "EVIDENCE",
    "COURSE": "COURSE",
    "MANAGEMENT": "MANAGEMENT",
    "DEMOGRAPHIC": "NOT_ALLOCATED",
}

RECORD_RE = re.compile(
    r"^(O\d+)\s*\|\s*([A-Z_]+)\s*\|\s*(.*?)\s*\|\s*\[([A-D])\s*,\s*([^,]*?)\s*,\s*([^\]]*)\]\s*$"
)

failures = []


def fail(message):
    failures.append(message)


def main():
    path = None
    out_path = None
    index = 1
    while index < len(sys.argv):
        value = sys.argv[index]
        if value == "--out":
            if index + 1 >= len(sys.argv):
                print(__doc__)
                return 2
            out_path = sys.argv[index + 1]
            index += 2
        else:
            path = value
            index += 1
    if path is None:
        print(__doc__)
        return 2

    rows = []
    seen = []
    with open(path, encoding="utf-8-sig") as handle:
        for line in handle:
            raw = line.strip()
            if not raw:
                continue
            match = RECORD_RE.match(raw)
            if not match:
                fail("malformed input record: " + raw[:90])
                continue
            oid, kind, text, letter, name, date = match.groups()
            if oid in seen:
                fail("duplicate ID in input: " + oid)
                continue
            if kind not in KIND_TO_BUCKET:
                fail(oid + ": kind not allocatable: " + kind)
                continue
            seen.append(oid)
            bucket = KIND_TO_BUCKET[kind]
            rows.append(oid + " | " + bucket + " | " + kind + " | " + text.strip()
                        + " | [" + letter + ", " + name.strip() + ", " + date.strip() + "]")

    if failures:
        for message in failures:
            print("FAIL " + message)
        print("")
        print(str(len(failures)) + " failure(s); no allocation written")
        return 1

    # post-conditions: every input ID exactly once, mapping exact
    out_ids = [row.split(" | ")[0] for row in rows]
    if len(out_ids) != len(set(out_ids)):
        fail("duplicate IDs in output")
    if set(out_ids) != set(seen):
        fail("output IDs differ from input IDs")
    for row in rows:
        parts = row.split(" | ")
        expected = KIND_TO_BUCKET.get(parts[2])
        if expected != parts[1]:
            fail("destination does not match kind mapping: " + parts[0])

    if failures:
        for message in failures:
            print("FAIL " + message)
        print("")
        print(str(len(failures)) + " failure(s); no allocation written")
        return 1

    text = "\n".join(rows) + "\n"
    if out_path:
        open(out_path, "w", encoding="utf-8").write(text)
    else:
        sys.stdout.write(text)
    print("allocated " + str(len(rows)) + " objects, each exactly once")
    return 0


if __name__ == "__main__":
    sys.exit(main())
