#!/usr/bin/env python3
"""Zero scores where sections were blank or wholly off-topic (no real attempt)."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RESULTS_DIR = ROOT / "results"

# High-confidence corrections from full-paper audit (Jun 2025).
FIXES: dict[str, dict[str, float]] = {
    "001_cam1": {"q2": 0},
    "003_cam1": {"q2": 0},
    "010_cam1": {"q3b": 0},
    "013_cam1": {"q2": 0},
    "019_cam1": {"q2": 0},
    "025_cam2": {"q2": 0},
    "034_cam2": {"q2": 0},
    "045_cam2": {"q3c": 0},
    "051_cam3": {"q2": 0},
    "055_cam3": {"q2": 0},
    "057_cam3": {"q2": 0},
    "061_cam3": {"q2": 0},
    "064_cam3": {"q2": 0},
    "065_cam3": {"q2": 0},
}


def recompute(row: dict) -> None:
    row["section1"] = sum(row[k] for k in ("q1a", "q1b", "q1c", "q1d"))
    row["section2"] = row["q2"]
    row["section3"] = sum(row[k] for k in ("q3a", "q3b", "q3c"))
    row["total"] = int(round(row["section1"] + row["section2"] + row["section3"]))


def main() -> None:
    changed = 0
    for path in sorted(RESULTS_DIR.glob("batch*.json")):
        rows = json.loads(path.read_text(encoding="utf-8"))
        file_changed = False
        for row in rows:
            folder = row["folder"]
            if folder not in FIXES:
                continue
            for field, new_val in FIXES[folder].items():
                old = row.get(field)
                if old != new_val:
                    row[field] = new_val
                    file_changed = True
                    changed += 1
                    print(f"{folder}: {field} {old} -> {new_val}")
            recompute(row)
            print(f"  -> total {row['total']}")
        if file_changed:
            path.write_text(
                json.dumps(rows, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
    print(f"Applied {changed} field corrections.")


if __name__ == "__main__":
    main()
