#!/usr/bin/env python3
"""Export minimal JEAP grade xlsx files (idnumber + grade, no header)."""

from __future__ import annotations

import csv
from pathlib import Path

from openpyxl import Workbook

from load_roster import ROSTER_CSV_ENCODING
from merge_results import EXAM_ABSENT, scale_to_100

DOWNLOADS = Path.home() / "Downloads"
DESKTOP = Path.home() / "Desktop"
GRADES_CSV = DESKTOP / "TEAP_Final_Grades.csv"

JEAP_EXPORTS = [
    {
        "csv": DOWNLOADS / "1096320_Akademikİngilizce.csv",
        "xlsx": DESKTOP / "JEAP 1.xlsx",
    },
    {
        "csv": DOWNLOADS / "1111747_Akademikİngilizce.csv",
        "xlsx": DESKTOP / "JEAP 2.xlsx",
    },
]


def load_grade_by_id() -> dict[str, str | int]:
    grades: dict[str, str | int] = {}
    with GRADES_CSV.open(encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            sid = row["idnumber"].strip()
            total = row["total"].strip()
            grades[sid] = EXAM_ABSENT if total == EXAM_ABSENT else scale_to_100(total)
    return grades


def export_jeap_file(csv_path: Path, xlsx_path: Path, grades: dict[str, str | int]) -> int:
    with csv_path.open(encoding=ROSTER_CSV_ENCODING) as f:
        moodle_rows = list(csv.DictReader(f, delimiter=";"))

    wb = Workbook()
    ws = wb.active
    ws.title = "Notlar"

    for row in moodle_rows:
        sid = row["idnumber"].strip()
        grade = grades.get(sid, "")
        ws.append([sid, grade])

    wb.save(xlsx_path)
    return len(moodle_rows)


def main() -> None:
    if not GRADES_CSV.exists():
        raise SystemExit(f"Missing grades file: {GRADES_CSV}")

    grades = load_grade_by_id()
    for item in JEAP_EXPORTS:
        csv_path = item["csv"]
        xlsx_path = item["xlsx"]
        if not csv_path.exists():
            raise SystemExit(f"Missing roster CSV: {csv_path}")
        n = export_jeap_file(csv_path, xlsx_path, grades)
        print(f"Wrote {xlsx_path} ({n} rows, no header)")


if __name__ == "__main__":
    main()
