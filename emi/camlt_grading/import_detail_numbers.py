#!/usr/bin/env python3
"""Import manual total overrides and report highlights from Numbers detail file."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

from numbers_parser import Document

ROOT = Path(__file__).resolve().parent
DEFAULT_NUMBERS = Path.home() / "Desktop/CAMLT_Final_Grades_Detail.numbers"
DETAIL_CSV = Path.home() / "Desktop/CAMLT_Final_Grades_Detail.csv"
MAIN_CSV = Path.home() / "Desktop/CAMLT_Final_Grades.csv"
RESULTS_DIR = ROOT / "results"
REPORT = ROOT / "numbers_import_report.txt"

SCORE_COLS = [
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
]


def norm_sid(value: object) -> str | None:
    if value is None:
        return None
    if isinstance(value, float):
        return str(int(value))
    text = str(value).strip()
    return text or None


def norm_score(value: object) -> str | int | None:
    if value is None or value == "":
        return None
    if isinstance(value, str) and value.upper() == "E":
        return "E"
    return int(round(float(value)))


def load_csv_rows(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def save_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()), extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def patch_batch_total(folder: str, new_total: int) -> None:
    if not folder:
        return
    for path in sorted(RESULTS_DIR.glob("batch*.json")):
        rows = json.loads(path.read_text(encoding="utf-8"))
        changed = False
        for row in rows:
            if row.get("folder") != folder:
                continue
            if row.get("total") == new_total:
                continue
            row["total"] = new_total
            note = row.get("notes", "")
            suffix = f"Manual total override: {new_total}."
            row["notes"] = suffix if not note else f"{note} | {suffix}"
            changed = True
        if changed:
            path.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    numbers_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_NUMBERS
    if not numbers_path.exists():
        print(f"Not found: {numbers_path}")
        sys.exit(1)

    doc = Document(str(numbers_path))
    table = doc.sheets[0].tables[0]
    headers = [table.cell(0, col).value for col in range(table.num_cols)]
    col_idx = {name: idx for idx, name in enumerate(headers)}

    highlighted: list[str] = []
    for row_idx in range(1, table.num_rows):
        cols = [
            headers[col]
            for col in range(table.num_cols)
            if table.cell(row_idx, col).style and table.cell(row_idx, col).style.bg_color
        ]
        if not cols:
            continue
        sid = norm_sid(table.cell(row_idx, col_idx["idnumber"]).value)
        name = table.cell(row_idx, col_idx["roster_fullname"]).value
        notes = table.cell(row_idx, col_idx["notes"]).value
        highlighted.append(
            f"Row {row_idx + 1}: {sid} {name}\n  highlighted: {', '.join(cols)}\n  notes: {notes}"
        )

    csv_rows = load_csv_rows(DETAIL_CSV)
    by_id = {row["idnumber"]: row for row in csv_rows if row.get("idnumber")}

    total_changes: list[str] = []
    field_changes: list[str] = []
    for row_idx in range(1, table.num_rows):
        sid = norm_sid(table.cell(row_idx, col_idx["idnumber"]).value)
        if not sid or sid not in by_id:
            continue
        row = by_id[sid]
        for col in SCORE_COLS:
            if col not in col_idx:
                continue
            new_val = norm_score(table.cell(row_idx, col_idx[col]).value)
            if new_val is None:
                continue
            old_raw = row.get(col, "")
            old_val = old_raw if old_raw == "E" else int(round(float(old_raw or 0)))
            if new_val == old_val:
                continue
            row[col] = str(new_val) if new_val != "E" else "E"
            label = f"{sid} {row.get('roster_fullname', '')} {col}: {old_val} -> {new_val}"
            if col == "total":
                total_changes.append(label)
                if isinstance(new_val, int):
                    patch_batch_total(row.get("folder", ""), new_val)
            else:
                field_changes.append(label)

    save_csv(DETAIL_CSV, csv_rows)
    roster_rows = [
        row
        for row in csv_rows
        if row.get("match_status") != "unmatched_paper" and row.get("idnumber")
    ]
    save_csv(MAIN_CSV, roster_rows)

    lines = [
        f"Source: {numbers_path}",
        "",
        "=== Highlighted rows ===",
        *highlighted,
        "",
        f"=== Total overrides ({len(total_changes)}) ===",
        *total_changes,
        "",
        f"=== Other score changes ({len(field_changes)}) ===",
        *field_changes,
    ]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
