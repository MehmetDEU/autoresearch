#!/usr/bin/env python3
"""Merge grading results, match roster, export CSV."""

from __future__ import annotations

import csv
import json
import statistics
import unicodedata
from pathlib import Path

from participation import apply_participation_credits, SURVEY_Q1_CREDIT_IDS
from load_roster import fix_turkish_mojibake

ROOT = Path(__file__).resolve().parent
RESULTS_DIR = ROOT / "results"
ROSTER_PATH = ROOT / "roster.json"
OUT_CSV = Path.home() / "Desktop" / "TEAP_Final_Grades.csv"
OUT_OTHER_CSV = Path.home() / "Desktop" / "TEAP_Other_Courses_Exam.csv"
OUT_DETAIL = Path.home() / "Desktop" / "TEAP_Final_Grades_Detail.csv"
ANOMALY_REPORT = ROOT / "anomalies_report.md"

EXAM_ABSENT = "E"
EXAM_RAW_MAX = 60
EXAM_FULL_SCALE = 100


def scale_to_100(value: object) -> int | str:
    """Proportional conversion from 60-point exam scale to 100 (nearest integer)."""
    if value in (None, "", EXAM_ABSENT):
        return ""
    return int(round(float(value) * EXAM_FULL_SCALE / EXAM_RAW_MAX))


def round_score(value: object) -> int | str:
    if value in (None, "", EXAM_ABSENT):
        return EXAM_ABSENT if value == EXAM_ABSENT else value
    return int(round(float(value)))


def round_graded_row(row: dict) -> None:
    if row.get("total") == EXAM_ABSENT:
        return
    for key in (
        "participation",
        "section_i",
        "section_ii",
        "section_iii_q15",
        "section_iii_q16",
        "section_iii",
        "total",
    ):
        if key in row and row[key] not in ("", EXAM_ABSENT):
            row[key] = round_score(row[key])

# Name on scan -> corrected (other-course papers).
OTHER_COURSE_NAME_OVERRIDES: dict[str, str] = {
    "019_batch1": "Uğurcan Sarualtun",
}

# Paper matched by roster ID but name on sheet indicates another student.
FOLDER_ROSTER_OVERRIDE = {
    "017_batch1": "230907035",  # Sheet name Eren Özdemir; ID written as 230907055
}

# Handwriting on paper vs roster name — confirmed by instructor.
CONFIRMED_PAPER_NAMES: dict[str, tuple[str, str]] = {
    "220907002": ("Idril Ege Atis", "İdil Ezgi Atiş"),
    "230907058": ("Şenol Ceren", "Şevval Ceren Topdemir"),
    "230907095": ("Kahroman", "Kahriman"),  # OCR also read as Kohriman
    "220907036": ("DOLAR", "Dolak"),
}

# Known OCR misreads -> roster idnumber
ID_OVERRIDES = {
    "243907025": "240907025",
    "230927046": "230907046",
    "230507032": "230907032",
    "230307038": "230907058",
    "200907032": "240907032",
    "230977087": "230907087",
    "230907022": "230907082",
    "220909017": "220907017",
    "222907016": "220907016",
    "210907034": "240907034",
    "220307067": "220907067",
    "20907052": "220907052",
    "220307025": "220907025",
    "210907020": "240907020",
}


def normalize_name(text: str) -> str:
    text = unicodedata.normalize("NFKD", text or "")
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return " ".join(text.upper().split())


def apply_confirmed_name_note(row: dict) -> None:
    """Replace tentative name-mismatch notes with instructor-confirmed identity."""
    sid = row.get("idnumber", "")
    entry = CONFIRMED_PAPER_NAMES.get(sid)
    if not entry:
        return
    paper_name, roster_name = entry
    note = row.get("notes") or ""
    drop_phrases = [
        "Name written as Idril Ege Atis on paper.",
        "Name written as DOLAR on paper. ",
        "Name written as DOLAR on paper.",
        "Surname written as Kohriman (roster: Kahriman). ",
        "Name written as Şenol Ceren; ",
    ]
    for phrase in drop_phrases:
        note = note.replace(phrase, "")
    confirm = f"Kağıt adı doğrulandı: «{paper_name}» → {roster_name}."
    if confirm not in note:
        note = f"{note} {confirm}".strip()
    row["notes"] = note


def absent_row(student: dict) -> dict:
    """Roster student with no exam paper — did not sit the exam."""
    return {
        "idnumber": student["idnumber"],
        "firstname": fix_turkish_mojibake(student["firstname"]),
        "lastname": fix_turkish_mojibake(student["lastname"]),
        "participation": EXAM_ABSENT,
        "section_i": EXAM_ABSENT,
        "section_ii": EXAM_ABSENT,
        "section_iii_q15": EXAM_ABSENT,
        "section_iii_q16": EXAM_ABSENT,
        "section_iii": EXAM_ABSENT,
        "total": EXAM_ABSENT,
        "folder": "",
        "notes": "Sınava girmedi (E).",
    }


def other_course_row(scan: dict) -> dict:
    """Exam paper from a student not on this course roster."""
    folder = scan.get("folder", "")
    paper_name = fix_turkish_mojibake(
        OTHER_COURSE_NAME_OVERRIDES.get(folder, scan.get("student_name_read") or "")
    )
    parts = paper_name.split(maxsplit=1)
    first = parts[0] if parts else ""
    last = parts[1] if len(parts) > 1 else ""
    sid = normalize_id(scan.get("student_id_read", ""))
    part = scan.get("participation", "")
    s1 = scan.get("section_i", "")
    s2 = scan.get("section_ii", "")
    s3q15 = scan.get("section_iii_q15", "")
    s3q16 = scan.get("section_iii_q16", "")
    s3 = scan.get("section_iii", "")
    total = scan.get("total", "")
    return {
        "idnumber": sid,
        "firstname": first,
        "lastname": last,
        "name_on_paper": paper_name,
        "course_group": "diğer dersler",
        "participation": part,
        "section_i": s1,
        "section_ii": s2,
        "section_iii_q15": s3q15,
        "section_iii_q16": s3q16,
        "section_iii": s3,
        "total": total,
        "participation_100": scale_to_100(part),
        "section_i_100": scale_to_100(s1),
        "section_ii_100": scale_to_100(s2),
        "section_iii_100": scale_to_100(s3),
        "total_100": scale_to_100(total),
        "folder": folder,
        "notes": ((scan.get("notes") or "").strip() + " 100 üzerinden orantılı (×100/60).").strip()
        or "Bu dersin CSV listesinde yok; sınav kağıdı diğer ders öğrencisine ait. 100 üzerinden orantılı (×100/60).",
    }


def normalize_id(raw: str) -> str:
    digits = "".join(ch for ch in (raw or "") if ch.isdigit())
    if digits in ID_OVERRIDES:
        return ID_OVERRIDES[digits]
    if len(digits) == 7:
        digits = "2" + digits
    if len(digits) == 9 and digits.startswith("222"):
        digits = "220" + digits[3:]
    if digits.startswith("210907") and len(digits) >= 8:
        digits = "240907" + digits[6:]
    if digits.startswith("220307") and len(digits) >= 8:
        digits = "220907" + digits[6:]
    return digits


def load_results() -> list[dict]:
    """Load canonical batch files only (avoid batch1a/b double-count with batch1)."""
    rows: list[dict] = []
    for name in ("batch1.json", "batch2.json", "batch3.json", "batch4.json"):
        path = RESULTS_DIR / name
        if path.exists():
            rows.extend(json.loads(path.read_text(encoding="utf-8")))
    rows.sort(key=lambda r: r.get("pair_id", 0))
    return rows


def match_roster(row: dict, roster: list[dict]) -> dict | None:
    folder = row.get("folder", "")
    if folder in FOLDER_ROSTER_OVERRIDE:
        sid = FOLDER_ROSTER_OVERRIDE[folder]
        hits = [s for s in roster if s["idnumber"] == sid]
        if len(hits) == 1:
            return hits[0]

    sid = normalize_id(row.get("student_id_read", ""))
    if sid:
        hits = [s for s in roster if s["idnumber"] == sid]
        if len(hits) == 1:
            return hits[0]

    name_norm = normalize_name(row.get("student_name_read", ""))
    hits = [s for s in roster if s["fullname_norm"] == name_norm]
    if len(hits) == 1:
        return hits[0]

    tokens = set(name_norm.split())
    if tokens:
        hits = [
            s
            for s in roster
            if len(tokens & set(s["fullname_norm"].split())) >= 2
            and len(tokens & set(s["fullname_norm"].split())) >= len(tokens) - 1
        ]
        if len(hits) == 1:
            return hits[0]
    return None


def main() -> None:
    roster = json.loads(ROSTER_PATH.read_text(encoding="utf-8"))
    results = load_results()
    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))

    for row in results:
        row["student_id_normalized"] = normalize_id(row.get("student_id_read", ""))
        row["roster_match"] = match_roster(row, roster)

    id_to_rows: dict[str, list[dict]] = {}
    unmatched: list[dict] = []
    for row in results:
        match = row["roster_match"]
        if match:
            sid = match["idnumber"]
            row["idnumber"] = sid
            row["firstname"] = fix_turkish_mojibake(match["firstname"])
            row["lastname"] = fix_turkish_mojibake(match["lastname"])
            id_to_rows.setdefault(sid, []).append(row)
        else:
            unmatched.append(row)

    duplicates = {k: v for k, v in id_to_rows.items() if len(v) > 1}
    final_rows: list[dict] = []
    for sid, group in id_to_rows.items():
        best = max(group, key=lambda r: float(r.get("total", 0)))
        note = best.get("notes") or ""
        if len(group) > 1:
            folders = ", ".join(g["folder"] for g in group)
            note = f"{note} [duplicate scan x{len(group)}: {folders}; kept highest]".strip()
        best["notes"] = note
        part, credit_note = apply_participation_credits(best)
        best["participation"] = part
        best["total"] = (
            float(best["section_i"])
            + float(best["section_ii"])
            + float(best["section_iii"])
            + part
        )
        if credit_note:
            best["notes"] = (best.get("notes") or "") + credit_note
        apply_confirmed_name_note(best)
        round_graded_row(best)
        final_rows.append(best)

    roster_ids = {s["idnumber"] for s in roster}
    graded_ids = {r["idnumber"] for r in final_rows}
    roster_by_id = {s["idnumber"]: s for s in roster}
    for sid in sorted(roster_ids - graded_ids):
        final_rows.append(absent_row(roster_by_id[sid]))

    final_rows.sort(key=lambda r: (r.get("lastname", ""), r.get("firstname", "")))
    absent_ids = sorted(roster_ids - graded_ids)
    other_course_rows = [other_course_row(row) for row in unmatched]
    for row in other_course_rows:
        for key in (
            "participation",
            "section_i",
            "section_ii",
            "section_iii_q15",
            "section_iii_q16",
            "section_iii",
            "total",
        ):
            row[key] = round_score(row[key])
        row["participation_100"] = scale_to_100(row["participation"])
        row["section_i_100"] = scale_to_100(row["section_i"])
        row["section_ii_100"] = scale_to_100(row["section_ii"])
        row["section_iii_100"] = scale_to_100(row["section_iii"])
        row["total_100"] = scale_to_100(row["total"])
    other_course_rows.sort(key=lambda r: (r.get("lastname", ""), r.get("firstname", "")))

    fieldnames = [
        "idnumber",
        "firstname",
        "lastname",
        "participation",
        "section_i",
        "section_ii",
        "section_iii_q15",
        "section_iii_q16",
        "section_iii",
        "total",
        "folder",
        "notes",
    ]
    other_fieldnames = fieldnames + [
        "name_on_paper",
        "course_group",
        "participation_100",
        "section_i_100",
        "section_ii_100",
        "section_iii_100",
        "total_100",
    ]
    with OUT_CSV.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for row in final_rows:
            w.writerow(row)

    with OUT_OTHER_CSV.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=other_fieldnames, extrasaction="ignore")
        w.writeheader()
        for row in other_course_rows:
            w.writerow(row)

    detail_fields = fieldnames + ["student_name_read", "student_id_read", "pair_id"]
    with OUT_DETAIL.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=detail_fields, extrasaction="ignore")
        w.writeheader()
        for row in sorted(results, key=lambda r: r.get("pair_id", 0)):
            if row.get("roster_match"):
                m = row["roster_match"]
                row["idnumber"] = m["idnumber"]
                row["firstname"] = m["firstname"]
                row["lastname"] = m["lastname"]
            w.writerow(row)

    scored = [r for r in final_rows if r.get("total") != EXAM_ABSENT]
    totals = [float(r["total"]) for r in scored]
    mean = statistics.mean(totals) if totals else 0

    lines = [
        "# TEAP Grading Anomalies Report",
        "",
        f"- Papers scanned (pairs): **{len(results)}**",
        f"- Roster size: **{len(roster)}**",
        f"- Roster with exam score: **{len(scored)}**",
        f"- Roster absent (E): **{len(absent_ids)}**",
        f"- Other courses (exam only): **{len(other_course_rows)}**",
        f"- Class mean (sat exam): **{mean:.1f} / 60**",
        f"- Pass mark reference: **60** (raw exam scale is 0–60)",
        f"- **Soner Polat anketi:** {len(SURVEY_Q1_CREDIT_IDS)} öğrenciye Q1 katılım kredisi uygulandı (kağıtta işaretlenmemiş).",
        "- **EAP sunumu:** 17 öğrenciye sunum katılım kredisi tanımlandı (İdil Ezgi Atış 2× → 20).",
        "- **017_batch1** Eren Özdemir (230907035) kağıdı; yazılı ID Zehranur Acar'a aitti.",
        "",
        "## Scan structure",
        "",
        "- Front-back pairing rule applied: consecutive pages = one sheet.",
        "- **jeap2.pdf page 31**: duplicate front scan of **Batuhan Ahmet Aydın (230907107)**; pair 038 is complete. Not missing.",
        "",
    ]
    for a in manifest.get("anomalies", []):
        lines.append(f"- {a['source_pdf']} p{a['page']}: {a.get('note', a['type'])}")

    if duplicates:
        lines.extend(["", "## Duplicate scans (kept highest total)", ""])
        for sid, group in sorted(duplicates.items()):
            s = next(x for x in roster if x["idnumber"] == sid)
            lines.append(
                f"- **{s['firstname']} {s['lastname']}** ({sid}): "
                + ", ".join(f"{g['folder']}={g['total']}" for g in group)
            )

    if absent_ids:
        lines.extend(["", "## Absent — on roster, no exam paper (E)", ""])
        for sid in absent_ids:
            s = roster_by_id[sid]
            lines.append(f"- {sid}: {s['firstname']} {s['lastname']}")

    if other_course_rows:
        lines.extend(["", "## Other courses — sat exam, not on this roster", ""])
        for row in other_course_rows:
            lines.append(
                f"- {row.get('folder')}: **{row.get('name_on_paper')}** / `{row.get('idnumber')}` "
                f"{row.get('total')}/60 → **{row.get('total_100')}/100** (orantılı)"
            )

    if unmatched and not other_course_rows:
        lines.extend(["", "## Papers not matched to roster", ""])
        for row in unmatched:
            lines.append(
                f"- {row.get('folder')}: `{row.get('student_name_read')}` / "
                f"`{row.get('student_id_read')}` (normalized `{row.get('student_id_normalized')}`) "
                f"total={row.get('total')}"
            )

    lines.extend(
        [
            "",
            "## Scan pairing review (manual)",
            "",
            "- **008/009/010_batch1**: İlhan Can Yaren back truncated; Mukaddes Karavil scanned twice. "
            "009 may have front/back swapped — Section III on 009 front might belong to İlhan.",
            "- **017_batch1**: Re-attributed to **Eren Özdemir (230907035)** by name; written ID was 230907055.",
            "- **Kağıt adı doğrulandı:** Idril Ege Atis → İdil Ezgi Atiş; Şenol Ceren → Şevval Ceren Topdemir; "
            "Kahroman → Kahriman; DOLAR → Dolak.",
            "- **jeap2 p31**: Duplicate front only; not a missing student.",
        ]
    )

    ANOMALY_REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_OTHER_CSV}")
    print(f"Wrote {OUT_DETAIL}")
    print(f"Wrote {ANOMALY_REPORT}")
    print(
        f"Roster: {len(final_rows)} | Sat exam: {len(scored)} | Absent E: {len(absent_ids)} | "
        f"Other courses: {len(other_course_rows)} | Mean: {mean:.1f}"
    )


if __name__ == "__main__":
    main()
