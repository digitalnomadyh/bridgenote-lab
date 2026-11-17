"""Privacy-first storage helpers for BridgeNote Lab.

The lab records structured observations under a participant code. It is a
reflection and program-learning tool, not a diagnostic or clinical record.
"""

import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(__file__)
OBSERVATIONS_PATH = os.path.join(BASE_DIR, "data", "lab_observations.json")
INQUIRIES_PATH = os.path.join(BASE_DIR, "data", "lab_inquiries.json")
ACCESS_DESIGNS_PATH = os.path.join(BASE_DIR, "data", "lab_access_designs.json")


def _read(path: str) -> list:
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def _write(path: str, records: list) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(records, file, ensure_ascii=False, indent=2)


def save_observation(record: dict) -> None:
    records = _read(OBSERVATIONS_PATH)
    record["timestamp"] = datetime.now().isoformat(timespec="minutes")
    records.append(record)
    _write(OBSERVATIONS_PATH, records)


def save_inquiry(record: dict) -> None:
    records = _read(INQUIRIES_PATH)
    record["timestamp"] = datetime.now().isoformat(timespec="minutes")
    records.append(record)
    _write(INQUIRIES_PATH, records)


def save_access_design(record: dict) -> None:
    records = _read(ACCESS_DESIGNS_PATH)
    record["timestamp"] = datetime.now().isoformat(timespec="minutes")
    records.append(record)
    _write(ACCESS_DESIGNS_PATH, records)


def observations() -> list:
    return _read(OBSERVATIONS_PATH)


def inquiries() -> list:
    return _read(INQUIRIES_PATH)


def access_designs() -> list:
    return _read(ACCESS_DESIGNS_PATH)


def metrics() -> dict:
    records = observations()
    if not records:
        return {"sessions": 0, "participants": 0, "engagement": None, "regulation": None}
    return {
        "sessions": len(records),
        "participants": len({r["participant_code"] for r in records}),
        "engagement": round(sum(r["engagement"] for r in records) / len(records), 1),
        "regulation": round(sum(r["regulation"] for r in records) / len(records), 1),
    }


def portfolio_markdown() -> str:
    stats = metrics()
    questions = inquiries()
    designs = access_designs()
    lines = [
        "# BridgeNote Lab - Evidence Portfolio",
        "",
        "## Purpose",
        "A privacy-first musical-access and inquiry tool created to connect compassionate practice with evidence-based iteration.",
        "",
        "## Current learning record",
        f"- {stats['sessions']} structured session observation(s)",
        f"- {stats['participants']} de-identified participant code(s)",
        f"- {len(designs)} musical access design(s) documented",
    ]
    if stats["engagement"] is not None:
        lines += [
            f"- Mean observer engagement score: {stats['engagement']}/5",
            f"- Mean observer regulation score: {stats['regulation']}/5",
        ]
    lines += ["", "## Musical access designs"]
    if designs:
        for item in designs[-5:][::-1]:
            lines += [
                f"### {item['musical_context']}",
                f"- Access consideration: {item['access_consideration']}",
                f"- Adjustment tried: {item['adjustment']}",
                f"- Observable response: {item['response']}",
                f"- Next question: {item['next_question']}",
            ]
    else:
        lines.append("No access designs yet. Document one small adjustment before making a claim.")
    lines += ["", "## Inquiry cycle"]
    if questions:
        for item in questions[-5:][::-1]:
            lines += [
                f"### {item['question']}",
                f"- Hypothesis: {item['hypothesis']}",
                f"- Adjustment: {item['adjustment']}",
                f"- Reflection: {item['reflection']}",
            ]
    else:
        lines.append("No inquiry entries yet. Add a question before drawing conclusions.")
    lines += [
        "",
        "## Ethical boundary",
        "These observations describe a learning setting. They do not diagnose, treat, or establish clinical outcomes. Share only de-identified, consented summaries.",
    ]
    return "\n".join(lines)

