#!/usr/bin/env python3
"""Merge CAMLT batch grade JSON files into roster CSV exports."""

from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RESULTS_DIR = ROOT / "results"
MATCH_CSV = Path.home() / "Desktop" / "CAMLT_Paper_Match.csv"
ROSTER_PATH = ROOT / "roster.json"
MANUAL_GRADES_PATH = ROOT / "manual_grades.json"
OUT_CSV = Path.home() / "Desktop" / "CAMLT_Final_Grades.csv"
OUT_DETAIL = Path.home() / "Desktop" / "CAMLT_Final_Grades_Detail.csv"
OUT_OTHER = Path.home() / "Desktop" / "CAMLT_Other_Exam.csv"
EXAM_ABSENT = "E"


def load_json_batches() -> dict[str, dict]:
    by_folder: dict[str, dict] = {}
    for path in sorted(RESULTS_DIR.glob("batch*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        for row in data:
            by_folder[row["folder"]] = row
    return by_folder


def load_matches() -> dict[str, dict]:
    matches: dict[str, dict] = {}
    with MATCH_CSV.open(encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            matches[row["folder"]] = row
    return matches


def load_manual_grades() -> dict[str, dict]:
    if not MANUAL_GRADES_PATH.exists():
        return {}
    return json.loads(MANUAL_GRADES_PATH.read_text(encoding="utf-8"))


def main() -> None:
    roster = json.loads(ROSTER_PATH.read_text(encoding="utf-8"))
    grades_by_folder = load_json_batches()
    matches = load_matches()
    manual_grades = load_manual_grades()

    roster_rows: list[dict] = []
    other_rows: list[dict] = []
    graded_ids: set[str] = set()

    for folder, match in sorted(matches.items()):
        g = grades_by_folder.get(folder)
        if not g:
            continue
        sid = match.get("idnumber") or g.get("idnumber", "")
        row = {
            "folder": folder,
            "idnumber": sid,
            "roster_fullname": match.get("roster_fullname", ""),
            "course_group": match.get("course_group", ""),
            "match_status": match.get("match_status", ""),
            "name_on_paper": match.get("name_on_paper", ""),
            "q1a": g.get("q1a", ""),
            "q1b": g.get("q1b", ""),
            "q1c": g.get("q1c", ""),
            "q1d": g.get("q1d", ""),
            "q2": g.get("q2", ""),
            "q3a": g.get("q3a", ""),
            "q3b": g.get("q3b", ""),
            "q3c": g.get("q3c", ""),
            "section1": g.get("section1", ""),
            "section2": g.get("section2", ""),
            "section3": g.get("section3", ""),
            "total": int(round(float(g.get("total", 0)))),
            "notes": g.get("notes", ""),
        }
        if match.get("match_status") == "unmatched_paper" or not sid:
            other_rows.append(row)
        else:
            roster_rows.append(row)
            graded_ids.add(sid)

    for sid, manual in manual_grades.items():
        if sid in graded_ids:
            continue
        roster_rows.append(
            {
                "folder": manual.get("folder", ""),
                "idnumber": sid,
                "roster_fullname": manual.get("roster_fullname", ""),
                "course_group": manual.get("course_group", ""),
                "match_status": manual.get("match_status", "manual"),
                "name_on_paper": manual.get("name_on_paper", ""),
                "q1a": manual.get("q1a", ""),
                "q1b": manual.get("q1b", ""),
                "q1c": manual.get("q1c", ""),
                "q1d": manual.get("q1d", ""),
                "q2": manual.get("q2", ""),
                "q3a": manual.get("q3a", ""),
                "q3b": manual.get("q3b", ""),
                "q3c": manual.get("q3c", ""),
                "section1": manual.get("section1", ""),
                "section2": manual.get("section2", ""),
                "section3": manual.get("section3", ""),
                "total": int(round(float(manual["total"]))),
                "notes": manual.get("notes", ""),
            }
        )
        graded_ids.add(sid)

    for student in roster:
        sid = student["idnumber"]
        if sid in graded_ids:
            continue
        roster_rows.append(
            {
                "folder": "",
                "idnumber": sid,
                "roster_fullname": student["fullname"],
                "course_group": student["course_group"],
                "match_status": "absent",
                "name_on_paper": "",
                "q1a": EXAM_ABSENT,
                "q1b": EXAM_ABSENT,
                "q1c": EXAM_ABSENT,
                "q1d": EXAM_ABSENT,
                "q2": EXAM_ABSENT,
                "q3a": EXAM_ABSENT,
                "q3b": EXAM_ABSENT,
                "q3c": EXAM_ABSENT,
                "section1": EXAM_ABSENT,
                "section2": EXAM_ABSENT,
                "section3": EXAM_ABSENT,
                "total": EXAM_ABSENT,
                "notes": "Sınav kağıdı yok.",
            }
        )

    roster_rows.sort(key=lambda r: (r["course_group"], r.get("roster_fullname", "")))

    fields = [
        "idnumber",
        "roster_fullname",
        "course_group",
        "total",
        "section1",
        "section2",
        "section3",
        "q1a",
        "q1b",
        "q1c",
        "q1d",
        "q2",
        "q3a",
        "q3b",
        "q3c",
        "folder",
        "match_status",
        "name_on_paper",
        "notes",
    ]
    with OUT_CSV.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for row in roster_rows:
            w.writerow(row)

    with OUT_DETAIL.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for row in roster_rows + other_rows:
            w.writerow(row)

    if other_rows:
        with OUT_OTHER.open("w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
            w.writeheader()
            for row in other_rows:
                w.writerow(row)

    entered = [r for r in roster_rows if r["total"] != EXAM_ABSENT]
    mean = sum(int(r["total"]) for r in entered) / len(entered) if entered else 0
    print(f"Wrote {OUT_CSV}")
    print(f"Graded papers: {len(grades_by_folder)} | Roster entered: {len(entered)} | Absent: {len(roster)-len(graded_ids)} | Other: {len(other_rows)} | Mean: {mean:.1f}/100")


if __name__ == "__main__":
    main()
