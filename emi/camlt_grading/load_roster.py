#!/usr/bin/env python3
"""Load CAMLT Moodle rosters from three CSV exports."""

from __future__ import annotations

import csv
import json
import unicodedata
from pathlib import Path

DOWNLOADS = Path.home() / "Downloads"
ROOT = Path(__file__).resolve().parent
ROSTER_PATH = ROOT / "roster.json"

ROSTER_CSV_ENCODING = "cp1254"
MOJIBAKE_MAP = str.maketrans(
    {"Ý": "İ", "ý": "ı", "Þ": "Ş", "þ": "ş", "Ð": "Ğ", "ð": "ğ"}
)

CSV_FILES = [
    {
        "path": DOWNLOADS / "1096037_DilÖğrenmeveÖğretimYaklaşımlarıII.csv",
        "group": "1096037",
        "label": "Dil Öğrenme ve Öğretim Yaklaşımları II (A)",
    },
    {
        "path": DOWNLOADS / "1097165_DilÖğrenmeveÖğretimYaklaşımlarıII.csv",
        "group": "1097165",
        "label": "Dil Öğrenme ve Öğretim Yaklaşımları II (B)",
    },
    {
        "path": DOWNLOADS / "1105959_İngilizceÖğretimProgramları.csv",
        "group": "1105959",
        "label": "İngilizce Öğretim Programları",
    },
]


def fix_turkish_mojibake(text: str) -> str:
    return (text or "").translate(MOJIBAKE_MAP)


def normalize_name(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return " ".join(text.upper().split())


def load_students() -> list[dict]:
    students: list[dict] = []
    for item in CSV_FILES:
        path = item["path"]
        if not path.exists():
            raise FileNotFoundError(path)
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
                        "lastname_norm": normalize_name(last),
                        "firstname_norm": normalize_name(first),
                        "source_csv": path.name,
                        "course_group": item["group"],
                        "course_label": item["label"],
                    }
                )
    return students


def main() -> None:
    students = load_students()
    ROSTER_PATH.write_text(json.dumps(students, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Loaded {len(students)} students -> {ROSTER_PATH}")


if __name__ == "__main__":
    main()
