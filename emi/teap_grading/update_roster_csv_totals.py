#!/usr/bin/env python3
"""Add roster total (participation + exam, scaled to 100) to Moodle CSV exports."""

from __future__ import annotations

import csv
from pathlib import Path

from load_roster import ROSTER_CSV_ENCODING
from merge_results import EXAM_ABSENT, scale_to_100

DOWNLOADS = Path.home() / "Downloads"
DESKTOP = Path.home() / "Desktop"
GRADES_CSV = DESKTOP / "TEAP_Final_Grades.csv"
GRADE_COL = "toplam"

ROSTER_CSVS = [
    DOWNLOADS / "1096320_Akademikİngilizce (1).csv",
    DOWNLOADS / "1111747_Akademikİngilizce (1).csv",
]


def load_totals_100() -> dict[str, int | str]:
    grades: dict[str, int | str] = {}
    with GRADES_CSV.open(encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            sid = row["idnumber"].strip()
            total = row["total"].strip()
            grades[sid] = EXAM_ABSENT if total == EXAM_ABSENT else scale_to_100(total)
    return grades


def update_csv(path: Path, grades: dict[str, int | str]) -> tuple[int, list[str]]:
    with path.open(encoding=ROSTER_CSV_ENCODING, newline="") as f:
        reader = csv.DictReader(f, delimiter=";")
        fields = list(reader.fieldnames or [])
        if GRADE_COL not in fields:
            fields.append(GRADE_COL)
        rows = list(reader)

    matched = 0
    missing: list[str] = []
    for row in rows:
        sid = row["idnumber"].strip()
        if sid in grades:
            row[GRADE_COL] = grades[sid]
            matched += 1
        else:
            row[GRADE_COL] = ""
            missing.append(sid)

    with path.open("w", encoding=ROSTER_CSV_ENCODING, newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter=";", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    return matched, missing


def main() -> None:
    if not GRADES_CSV.exists():
        raise SystemExit(f"Missing grades file: {GRADES_CSV}")

    grades = load_totals_100()
    for path in ROSTER_CSVS:
        if not path.exists():
            raise SystemExit(f"Missing roster CSV: {path}")
        matched, missing = update_csv(path, grades)
        print(f"Updated {path} ({matched}/{matched + len(missing)} rows, 100 üzerinden)")
        if missing:
            print(f"  Not bulunamadı: {missing}")


if __name__ == "__main__":
    main()
