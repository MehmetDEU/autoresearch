#!/usr/bin/env python3
"""Load Moodle CSV rosters for TEAP grading."""

from __future__ import annotations

import csv
import json
import unicodedata
from pathlib import Path

DOWNLOADS = Path.home() / "Downloads"
ROOT = Path(__file__).resolve().parent
ROSTER_PATH = ROOT / "roster.json"

CSV_FILES = [
    DOWNLOADS / "1096320_Akademikİngilizce.csv",
    DOWNLOADS / "1111747_Akademikİngilizce.csv",
]

# Moodle exports for this course use Windows Turkish (cp1254), not latin-1.
ROSTER_CSV_ENCODING = "cp1254"

# Fallback repair if text was already saved with latin-1 misread.
MOJIBAKE_MAP = str.maketrans(
    {
        "Ý": "İ",
        "ý": "ı",
        "Þ": "Ş",
        "þ": "ş",
        "Ð": "Ğ",
        "ð": "ğ",
    }
)


def fix_turkish_mojibake(text: str) -> str:
    return (text or "").translate(MOJIBAKE_MAP)


def normalize_name(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return " ".join(text.upper().split())


def main() -> None:
    students: list[dict] = []
    for path in CSV_FILES:
        with path.open(encoding=ROSTER_CSV_ENCODING) as f:
            reader = csv.DictReader(f, delimiter=";")
            for row in reader:
                first = fix_turkish_mojibake(row["firstname"].strip())
                last = fix_turkish_mojibake(row["lastname"].strip())
                full = f"{first} {last}"
                students.append(
                    {
                        "idnumber": row["idnumber"].strip(),
                        "firstname": first,
                        "lastname": last,
                        "fullname": full,
                        "fullname_norm": normalize_name(full),
                        "source_csv": path.name,
                    }
                )
    ROSTER_PATH.write_text(json.dumps(students, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Loaded {len(students)} students -> {ROSTER_PATH}")


if __name__ == "__main__":
    main()
