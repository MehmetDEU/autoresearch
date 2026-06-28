#!/usr/bin/env python3
"""Match CAMLT exam papers to Moodle roster (identification only, no grading)."""

from __future__ import annotations

import csv
import json
import re
import unicodedata
from pathlib import Path

from rapidfuzz import fuzz, process

ROOT = Path(__file__).resolve().parent
ROSTER_PATH = ROOT / "roster.json"
HEADERS_PATH = ROOT / "paper_headers.json"
MATCH_REPORT = ROOT / "match_report.md"
MATCH_CSV = Path.home() / "Desktop" / "CAMLT_Paper_Match.csv"

ID_RE = re.compile(r"\d{9}")
NAME_SCORE_OK = 82
NAME_SCORE_REVIEW = 70


def normalize_name(text: str) -> str:
    text = unicodedata.normalize("NFKD", text or "")
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return " ".join(text.upper().split())


def paper_full_name(paper: dict) -> str:
    return " ".join(
        part
        for part in [paper.get("student_name_read", ""), paper.get("student_surname_read", "")]
        if part
    ).strip()


def paper_name_norm(paper: dict) -> str:
    return normalize_name(paper_full_name(paper))


def clean_id(raw: str) -> str:
    m = ID_RE.search(raw or "")
    return m.group(0) if m else ""


def load_roster() -> list[dict]:
    return json.loads(ROSTER_PATH.read_text(encoding="utf-8"))


def load_papers() -> list[dict]:
    return json.loads(HEADERS_PATH.read_text(encoding="utf-8"))


def roster_by_id(roster: list[dict]) -> dict[str, dict]:
    return {s["idnumber"]: s for s in roster}


def best_name_match(
    query_norm: str,
    roster: list[dict],
    *,
    exclude_ids: set[str] | None = None,
) -> tuple[dict | None, int, list[tuple[str, int]]]:
    exclude_ids = exclude_ids or set()
    eligible = [s for s in roster if s["idnumber"] not in exclude_ids]
    if not eligible:
        return None, 0, []

    ranked = process.extract(
        query_norm,
        [s["fullname_norm"] for s in roster if s["idnumber"] not in exclude_ids],
        scorer=fuzz.token_sort_ratio,
        limit=3,
    )
    eligible = [s for s in roster if s["idnumber"] not in exclude_ids]
    norm_to_student = {s["fullname_norm"]: s for s in eligible}
    top3 = [
        (norm_to_student[name]["fullname"], int(score))
        for name, score, _ in ranked
        if name in norm_to_student
    ]
    if not ranked:
        return None, 0, top3
    best_name, score, _ = ranked[0]
    return norm_to_student.get(best_name), int(score), top3


def match_paper(paper: dict, roster: list[dict], by_id: dict[str, dict]) -> dict:
    folder = paper["folder"]
    id_read = clean_id(paper.get("student_id_read", ""))
    name_on_paper = paper_full_name(paper)
    name_norm = paper_name_norm(paper)

    result: dict = {
        "folder": folder,
        "name_on_paper": name_on_paper,
        "id_on_paper": id_read,
        "ocr_confidence": paper.get("ocr_confidence", ""),
        "match_method": "",
        "match_status": "",
        "idnumber": "",
        "roster_firstname": "",
        "roster_lastname": "",
        "roster_fullname": "",
        "course_group": "",
        "name_score": "",
        "name_crosscheck": "",
        "top_name_alternatives": "",
        "notes": "",
    }

    id_match = by_id.get(id_read) if id_read else None
    name_match, name_score, top3 = best_name_match(name_norm, roster)
    alt_text = "; ".join(f"{n} ({s})" for n, s in top3)

    if id_match:
        roster_norm = id_match["fullname_norm"]
        cross = fuzz.token_sort_ratio(name_norm, roster_norm)
        result.update(
            {
                "match_method": "id",
                "idnumber": id_match["idnumber"],
                "roster_firstname": id_match["firstname"],
                "roster_lastname": id_match["lastname"],
                "roster_fullname": id_match["fullname"],
                "course_group": id_match["course_group"],
                "name_score": cross,
                "name_crosscheck": "ok" if cross >= NAME_SCORE_OK else ("review" if cross >= NAME_SCORE_REVIEW else "mismatch"),
                "top_name_alternatives": alt_text,
            }
        )
        if cross >= NAME_SCORE_OK:
            result["match_status"] = "matched"
        elif cross >= NAME_SCORE_REVIEW:
            result["match_status"] = "matched_review"
            result["notes"] = f"ID eşleşti; isim benzerliği orta ({cross})."
        else:
            result["match_status"] = "id_name_mismatch"
            result["notes"] = (
                f"ID roster'da {id_match['fullname']} ama kağıt adı '{name_on_paper}' "
                f"(benzerlik {cross}). İsim alternatifleri: {alt_text}"
            )
        return result

    if name_match and name_score >= NAME_SCORE_OK:
        result.update(
            {
                "match_method": "fuzzy_name",
                "match_status": "matched_review",
                "idnumber": name_match["idnumber"],
                "roster_firstname": name_match["firstname"],
                "roster_lastname": name_match["lastname"],
                "roster_fullname": name_match["fullname"],
                "course_group": name_match["course_group"],
                "name_score": name_score,
                "name_crosscheck": "id_missing_or_wrong",
                "top_name_alternatives": alt_text,
                "notes": f"Kağıttaki ID ({id_read or 'yok'}) roster'da yok; isimle eşleştirildi ({name_score}).",
            }
        )
        return result

    if name_match and name_score >= NAME_SCORE_REVIEW:
        result.update(
            {
                "match_method": "fuzzy_name",
                "match_status": "needs_review",
                "idnumber": name_match["idnumber"],
                "roster_firstname": name_match["firstname"],
                "roster_lastname": name_match["lastname"],
                "roster_fullname": name_match["fullname"],
                "course_group": name_match["course_group"],
                "name_score": name_score,
                "name_crosscheck": "low_confidence",
                "top_name_alternatives": alt_text,
                "notes": f"Düşük güven isim eşleşmesi ({name_score}). ID: {id_read or 'yok'}.",
            }
        )
        return result

    result.update(
        {
            "match_method": "none",
            "match_status": "unmatched_paper",
            "name_score": name_score if name_match else 0,
            "top_name_alternatives": alt_text,
            "notes": f"Roster'da bulunamadı. Kağıt ID: {id_read or 'yok'}.",
        }
    )
    return result


def resolve_duplicate_ids(matches: list[dict]) -> None:
    """Flag when two papers claim the same roster ID."""
    by_id: dict[str, list[dict]] = {}
    for m in matches:
        if m["idnumber"]:
            by_id.setdefault(m["idnumber"], []).append(m)
    for sid, group in by_id.items():
        if len(group) > 1:
            folders = ", ".join(g["folder"] for g in group)
            for m in group:
                m["match_status"] = "duplicate_id"
                m["notes"] = (m.get("notes", "") + f" Aynı ID birden fazla kağıtta: {folders}.").strip()


def main() -> None:
    roster = load_roster()
    papers = load_papers()
    by_id = roster_by_id(roster)

    matches = [match_paper(p, roster, by_id) for p in papers]
    resolve_duplicate_ids(matches)

    matched_ids = {m["idnumber"] for m in matches if m["idnumber"]}
    absent = [s for s in roster if s["idnumber"] not in matched_ids]

    # Write CSV
    fieldnames = [
        "folder",
        "match_status",
        "match_method",
        "name_on_paper",
        "id_on_paper",
        "idnumber",
        "roster_fullname",
        "course_group",
        "name_score",
        "name_crosscheck",
        "ocr_confidence",
        "top_name_alternatives",
        "notes",
    ]
    with MATCH_CSV.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for row in sorted(matches, key=lambda r: r["folder"]):
            w.writerow(row)

    status_counts: dict[str, int] = {}
    for m in matches:
        status_counts[m["match_status"]] = status_counts.get(m["match_status"], 0) + 1

    lines = [
        "# CAMLT Paper ↔ Roster Match Report",
        "",
        f"- Roster: **{len(roster)}** öğrenci (3 CSV)",
        f"- Taranan kağıt: **{len(papers)}**",
        f"- Eşleşen (matched + matched_review): **{status_counts.get('matched', 0) + status_counts.get('matched_review', 0)}**",
        f"- İnceleme gerekli: **{status_counts.get('needs_review', 0) + status_counts.get('id_name_mismatch', 0) + status_counts.get('duplicate_id', 0)}**",
        f"- Listede yok (kağıt var): **{status_counts.get('unmatched_paper', 0)}**",
        f"- Listede var, kağıt yok (henüz E adayı): **{len(absent)}**",
        "",
        "## Durum özeti",
        "",
    ]
    for status, count in sorted(status_counts.items()):
        lines.append(f"- `{status}`: {count}")

  # Review items
    review = [m for m in matches if m["match_status"] not in ("matched",)]
    if review:
        lines.extend(["", "## İnceleme / istisna", ""])
        for m in sorted(review, key=lambda x: x["folder"]):
            lines.append(
                f"- **{m['folder']}** · kağıt: {m['name_on_paper']} (`{m['id_on_paper']}`) → "
                f"roster: {m['roster_fullname'] or '—'} (`{m['idnumber'] or '—'}`) · **{m['match_status']}**"
            )
            if m.get("notes"):
                lines.append(f"  - {m['notes']}")

    if absent:
        lines.extend(["", "## Listede var, sınav kağıdı yok", ""])
        for s in sorted(absent, key=lambda x: (x["course_group"], x["lastname"], x["firstname"])):
            lines.append(
                f"- `{s['idnumber']}` **{s['fullname']}** ({s['course_group']})"
            )

    off_roster = [m for m in matches if m["match_status"] == "unmatched_paper"]
    if off_roster:
        lines.extend(["", "## Kağıt var, roster'da yok", ""])
        for m in off_roster:
            lines.append(f"- **{m['folder']}**: {m['name_on_paper']} · ID `{m['id_on_paper']}`")

    MATCH_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Wrote {MATCH_CSV}")
    print(f"Wrote {MATCH_REPORT}")
    print(
        f"Papers: {len(papers)} | Matched: {len(matched_ids)} | Absent on scan: {len(absent)} | "
        f"Review: {len(review)}"
    )


if __name__ == "__main__":
    main()
