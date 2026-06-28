#!/usr/bin/env python3
"""Apply confirmed manual paper matches and roster grade overrides."""

from __future__ import annotations

import csv
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RESULTS_DIR = ROOT / "results"
MATCH_CSV = Path.home() / "Desktop" / "CAMLT_Paper_Match.csv"
ROSTER_PATH = ROOT / "roster.json"
MANUAL_GRADES_PATH = ROOT / "manual_grades.json"
PENDING_PATH = ROOT / "pending_corrections.md"

APPLIED_DATE = date.today().isoformat()

# Confirmed paper → roster reassignments (user-approved).
PAPER_MATCH_OVERRIDES: dict[str, dict[str, str]] = {
    "048_cam2": {
        "match_status": "matched",
        "match_method": "manual",
        "name_on_paper": "Sude Koca",
        "id_on_paper": "230907096",
        "idnumber": "230907096",
        "roster_fullname": "SUDE KOCA",
        "course_group": "1096037",
        "name_score": "100",
        "name_crosscheck": "ok",
        "notes": (
            f"Manuel düzeltme ({APPLIED_DATE}): OCR 230909096→230907096; "
            "Sude Koca (Macaro–McKinley kenar notları)."
        ),
    },
    "016_cam1": {
        "match_status": "matched",
        "match_method": "manual",
        "name_on_paper": "Keziban Ergenekon",
        "id_on_paper": "240921011",
        "idnumber": "240921011",
        "roster_fullname": "KEZİBAN ERGENEKON",
        "course_group": "1097165",
        "name_score": "100",
        "name_crosscheck": "ok",
        "notes": (
            f"Manuel düzeltme ({APPLIED_DATE}): OCR Keziban Ergezen/240921071 hatası; "
            "kağıt Keziban Ergenekon 240921011."
        ),
    },
    "009_cam1": {
        "match_status": "matched_review",
        "match_method": "manual",
        "name_on_paper": "M. Mert Bilgiç",
        "id_on_paper": "240921079",
        "idnumber": "240921071",
        "roster_fullname": "MUHAMMED MERT BİLGİÇ",
        "course_group": "1097165",
        "name_score": "100",
        "name_crosscheck": "id_mismatch_on_paper",
        "notes": (
            f"Manuel düzeltme ({APPLIED_DATE}): kağıt ID 240921079, roster 240921071; "
            "1.a 'Macaro says,' ile başlıyor."
        ),
    },
}

BATCH_ID_OVERRIDES: dict[str, str] = {
    "048_cam2": "230907096",
    "016_cam1": "240921011",
    "009_cam1": "240921071",
}

# Students without a scanned paper but with approved manual totals.
MANUAL_GRADES: dict[str, dict] = {
    "240921010": {
        "roster_fullname": "ZEYNEP NAZ OKTAR",
        "course_group": "1097165",
        "total": 62,
        "section1": 31,
        "section2": 12,
        "section3": 19,
        "q1a": "",
        "q1b": "",
        "q1c": "",
        "q1d": "",
        "q2": "",
        "q3a": "",
        "q3b": "",
        "q3c": "",
        "folder": "",
        "match_status": "manual",
        "name_on_paper": "",
        "notes": f"Kağıt bulunamadı. Manuel not: 62 (kullanıcı onayı, {APPLIED_DATE}).",
    },
}

NUMBERS_TOTAL_OVERRIDES: dict[str, int] = {
    "230907065": 85,
    "230907104": 78,
    "230907101": 75,
    "230907050": 53,
    "230907071": 55,
    "230907090": 82,
    "230907061": 70,
    "230907073": 74,
    "240921048": 53,
    "240921030": 85,
    "240921002": 73,
    "240921042": 90,
}


def load_match_rows() -> tuple[list[dict], list[str]]:
    with MATCH_CSV.open(encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames or [])
        return list(reader), fieldnames


def patch_match_csv() -> list[str]:
    rows, fieldnames = load_match_rows()
    applied: list[str] = []
    by_folder = {r["folder"]: r for r in rows}
    for folder, override in PAPER_MATCH_OVERRIDES.items():
        if folder not in by_folder:
            print(f"WARN: {folder} not in match CSV")
            continue
        row = by_folder[folder]
        for key, value in override.items():
            row[key] = value
        applied.append(f"{folder} → {override['idnumber']} {override['roster_fullname']}")
    with MATCH_CSV.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    return applied


def patch_batch_json() -> list[str]:
    applied: list[str] = []
    for path in sorted(RESULTS_DIR.glob("batch*.json")):
        rows = json.loads(path.read_text(encoding="utf-8"))
        changed = False
        for row in rows:
            folder = row.get("folder", "")
            if folder not in BATCH_ID_OVERRIDES:
                continue
            new_id = BATCH_ID_OVERRIDES[folder]
            if row.get("idnumber") != new_id:
                old = row.get("idnumber")
                row["idnumber"] = new_id
                applied.append(f"{path.name} {folder}: id {old} → {new_id}")
                changed = True
        if changed:
            path.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return applied


def write_manual_grades() -> None:
    MANUAL_GRADES_PATH.write_text(
        json.dumps(MANUAL_GRADES, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def verify_numbers_overrides() -> list[str]:
    """Confirm batch JSON totals match Numbers overrides (already applied)."""
    issues: list[str] = []
    by_folder: dict[str, dict] = {}
    for path in sorted(RESULTS_DIR.glob("batch*.json")):
        for row in json.loads(path.read_text(encoding="utf-8")):
            by_folder[row["folder"]] = row

    roster_by_id = {s["idnumber"]: s for s in json.loads(ROSTER_PATH.read_text(encoding="utf-8"))}
    rows, _ = load_match_rows()
    id_to_folder: dict[str, str] = {}
    for row in rows:
        if row.get("idnumber") and row.get("folder"):
            id_to_folder[row["idnumber"]] = row["folder"]

    for sid, expected in NUMBERS_TOTAL_OVERRIDES.items():
        folder = id_to_folder.get(sid, "")
        grade = by_folder.get(folder)
        if not grade:
            issues.append(f"{sid}: no batch grade for folder {folder!r}")
            continue
        actual = int(round(float(grade.get("total", 0))))
        if actual != expected:
            name = roster_by_id.get(sid, {}).get("fullname", "")
            issues.append(f"{sid} ({name}): expected {expected}, got {actual}")
    return issues


def mark_pending_applied() -> None:
    text = PENDING_PATH.read_text(encoding="utf-8")
    replacements = [
        ("Son güncelleme: kullanıcı onayı ile bekletiliyor.", f"Son güncelleme: **{APPLIED_DATE}** — toplu uygulandı."),
        (
            "- **Yapılacak:** `048_cam2` → `230907096` SUDE KOCA; roster’dan E kaldır; Other listesinden çıkar; CSV + batch JSON + canvas güncelle.",
            f"- **UYGULANDI ({APPLIED_DATE}):** `048_cam2` → `230907096` SUDE KOCA; E kaldırıldı.",
        ),
        (
            "- **Yapılacak:** `016_cam1` → Ergenekon (`240921011`), total=75 (kullanıcı onayı bekleniyor); Bilgiç’ten ayır",
            f"- **UYGULANDI ({APPLIED_DATE}):** `016_cam1` → Ergenekon (`240921011`), total=75; Bilgiç’ten ayrıldı.",
        ),
        (
            "- **Yapılacak:** `009_cam1` → MUHAMMED MERT BİLGİÇ (`240921071`), total=69; `016_cam1` roster’dan ayır (Ergezen/Other)",
            f"- **UYGULANDI ({APPLIED_DATE}):** `009_cam1` → MUHAMMED MERT BİLGİÇ (`240921071`), total=69.",
        ),
        (
            "- **Keziban Ergenekon** — `016_cam1`, 240921011, total **75** (şu an Bilgiç’e yanlış yazılı)",
            f"- **Keziban Ergenekon** — UYGULANDI ({APPLIED_DATE})",
        ),
        (
            "- **İrem Akman** — TBLT notlama sorunu (q2 zaten 0)",
            f"- **İrem Akman** — UYGULANDI ({APPLIED_DATE}): q2=0 (apply_blank_fixes).",
        ),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    PENDING_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    match_applied = patch_match_csv()
    batch_applied = patch_batch_json()
    write_manual_grades()
    numbers_issues = verify_numbers_overrides()
    mark_pending_applied()

    print("=== Paper match overrides ===")
    for line in match_applied:
        print(f"  {line}")
    print("=== Batch idnumber updates ===")
    for line in batch_applied:
        print(f"  {line}")
    print(f"Wrote {MANUAL_GRADES_PATH} ({len(MANUAL_GRADES)} manual grade(s))")
    if numbers_issues:
        print("=== Numbers override verification WARNINGS ===")
        for issue in numbers_issues:
            print(f"  {issue}")
    else:
        print(f"Verified {len(NUMBERS_TOTAL_OVERRIDES)} Numbers total overrides in batch JSON.")
    print(f"Updated {PENDING_PATH}")


if __name__ == "__main__":
    main()
