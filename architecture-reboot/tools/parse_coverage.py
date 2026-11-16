"""Whitespace-tolerant parser for the Doximity coverage/action protocol.

The protocol is sentinel-delimited, not indentation-delimited. Records may be separated by
any whitespace; a parser must not depend on line breaks surviving the renderer.
"""

from __future__ import annotations

import re
from typing import Any

COVERAGE_CATEGORIES = {
    "current_event_records",
    "baseline_comparator_records",
    "neuro_history_records",
    "medication_context_records",
    "exam_records",
    "workup_records",
    "action_bearing_records",
    "context_records",
}

RECORD_TYPES = {"COV", "PROBLEM", "UNIT", "ACTION", "UNRESOLVED", "END"}


class ProtocolError(ValueError):
    pass


def _split_ids(value: str) -> list[str]:
    value = value.strip()
    if value in {"", "NONE"}:
        return []
    return [part.strip() for part in value.split(",") if part.strip()]


def _require(fields: list[str], count: int, record: str) -> None:
    if len(fields) != count:
        raise ProtocolError(
            f"{record} expects {count} pipe-delimited fields, got {len(fields)}: {fields!r}"
        )


def parse_packet(text: str) -> dict[str, Any]:
    """Parse a coverage/action handoff.

    Returns coverage, problems, units, actions, unresolved and an ended flag.
    Raises ProtocolError on malformed records.
    """

    segments = [seg.strip() for seg in re.split(r"(?=@@)", text) if seg.strip()]
    if not segments:
        raise ProtocolError("empty packet")

    coverage: dict[str, list[str]] = {}
    problems: list[dict[str, Any]] = []
    units: list[dict[str, Any]] = []
    actions: list[dict[str, Any]] = []
    unresolved: list[dict[str, Any]] = []
    ended = False

    for segment in segments:
        if not segment.startswith("@@"):
            raise ProtocolError(f"record does not start with @@: {segment[:80]!r}")

        separator = ";;" if ";;" in segment else "|"
        fields = [field.strip() for field in segment.split(separator)]
        marker = fields[0][2:]
        if marker not in RECORD_TYPES:
            raise ProtocolError(f"unknown record marker: {fields[0]!r}")

        if marker == "COV":
            _require(fields, 3, "@@COV")
            category = fields[1]
            if category not in COVERAGE_CATEGORIES:
                raise ProtocolError(f"unknown coverage category: {category!r}")
            if category in coverage:
                raise ProtocolError(f"duplicate coverage category: {category!r}")
            coverage[category] = _split_ids(fields[2])
            continue

        if marker == "PROBLEM":
            _require(fields, 9, "@@PROBLEM")
            problems.append(
                {
                    "id": fields[1],
                    "encounter_role": fields[2],
                    "label": fields[3],
                    "evidence": _split_ids(fields[4]),
                    "counterevidence": _split_ids(fields[5]),
                    "contains": fields[6],
                    "separate_from": fields[7],
                    "order": fields[8],
                }
            )
            continue

        if marker == "UNIT":
            _require(fields, 7, "@@UNIT")
            units.append(
                {
                    "id": fields[1],
                    "unit_type": fields[2],
                    "label": fields[3],
                    "source_records": _split_ids(fields[4]),
                    "chronology": fields[5],
                    "problem_relation": fields[6],
                }
            )
            continue

        if marker == "ACTION":
            _require(fields, 7, "@@ACTION")
            actions.append(
                {
                    "id": fields[1],
                    "source_records": _split_ids(fields[2]),
                    "target": fields[3],
                    "wording": fields[4],
                    "owner": fields[5],
                    "unresolved": fields[6],
                }
            )
            continue

        if marker == "UNRESOLVED":
            _require(fields, 5, "@@UNRESOLVED")
            unresolved.append(
                {
                    "id": fields[1],
                    "source_records": _split_ids(fields[2]),
                    "topic": fields[3],
                    "issue": fields[4],
                }
            )
            continue

        if marker == "END":
            _require(fields, 1, "@@END")
            ended = True

    missing = COVERAGE_CATEGORIES - set(coverage)
    if missing:
        raise ProtocolError(f"missing coverage categories: {sorted(missing)}")
    if not ended:
        raise ProtocolError("missing @@END")

    return {
        "coverage": coverage,
        "problems": problems,
        "units": units,
        "actions": actions,
        "unresolved": unresolved,
        "ended": ended,
    }


if __name__ == "__main__":
    sample = """
    @@COV|current_event_records|T001,T004
    @@COV|baseline_comparator_records|T016,T017
    @@COV|neuro_history_records|T002,T003
    @@COV|medication_context_records|T015,T022
    @@COV|exam_records|P1.003
    @@COV|workup_records|T008,T020,T021
    @@COV|action_bearing_records|T008,T015,T020,T021
    @@COV|context_records|T001,T017
    @@PROBLEM|P001|PRIMARY|current recurrent events|T001,T004|NONE|baseline spells as comparator|NONE|1
    @@UNIT|CU001|current_event|current events|T001,T004|NONE|P001
    @@ACTION|AV001|T015|levetiracetam|reported treatment on ship|P001|NONE
    @@UNRESOLVED|X001|T021|CT result availability|CT completed without available result
    @@END
    """
    parsed = parse_packet(sample)
    print("coverage categories:", len(parsed["coverage"]))
    print("problems:", len(parsed["problems"]))
    print("units:", len(parsed["units"]))
    print("actions:", len(parsed["actions"]))
    print("unresolved:", len(parsed["unresolved"]))
    print("ended:", parsed["ended"])
