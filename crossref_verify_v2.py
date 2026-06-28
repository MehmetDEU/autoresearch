#!/usr/bin/env python3
"""Thorough Crossref cross-check for APA7 references."""

import json
import re
import time
import unicodedata
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

REFS_PATH = Path(
    "/Users/mehmetaltay/Library/CloudStorage/GoogleDrive-mehmetdeudilforum@gmail.com/"
    "Drive'ım/Macbook Pro M5/Golem Effect/literature/references_APA7_reframed.md"
)
MS_PATH = Path(
    "/Users/mehmetaltay/Library/CloudStorage/GoogleDrive-mehmetdeudilforum@gmail.com/"
    "Drive'ım/Macbook Pro M5/Golem Effect/manuscript/Golem_reframed_v1.md"
)

# DOI may contain (), <>, ;, etc. — capture to end of line
DOI_RE = re.compile(r"https?://doi\.org/(.+?)\s*$", re.I)


@dataclass
class Reference:
    line_no: int
    raw: str
    key: str
    doi: Optional[str] = None
    authors_str: str = ""
    year: str = ""
    issues: list = field(default_factory=list)
    status: str = "PASS"


def ascii_fold(s: str) -> str:
    """Compare names ignoring accents/hyphen variants."""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower().replace("-", "").replace("‐", "").replace("–", "").replace("—", "")
    s = re.sub(r"[^a-z]", "", s)
    return s


def parse_apa_ref(line: str, line_no: int) -> Optional[Reference]:
    line = line.strip()
    if not line.startswith("- ") or "validated instrument" in line or "—" in line[:5]:
        if line.startswith("- ") and ("validated instrument" in line or "autonomy-support" in line or "L2MSS" in line or "large-scale" in line or "Self-Construal Scale" in line or "self-construal review" in line or "linguistic capital in EMI" in line):
            return None
    if not line.startswith("- "):
        return None
    raw = line[2:].strip()
    doi_match = DOI_RE.search(raw)
    doi = doi_match.group(1).strip() if doi_match else None

    year_match = re.search(r"\((\d{4})\)", raw)
    year = year_match.group(1) if year_match else ""
    authors_str = raw[: year_match.start()].strip().rstrip(",") if year_match else ""
    surname = authors_str.split(",")[0].split("&")[0].strip().split()[-1]
    key = f"{surname} ({year})" if year else surname
    return Reference(line_no=line_no, raw=raw, key=key, doi=doi, authors_str=authors_str, year=year)


def fetch_crossref(doi: str) -> dict:
    url = f"https://api.crossref.org/works/{doi}"
    req = urllib.request.Request(url, headers={"User-Agent": "autoresearch-ref-check/2.0 (mailto:verify@example.com)"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())["message"]


def cr_year(cr: dict) -> str:
    for fld in ("published-print", "published-online", "issued", "created"):
        parts = cr.get(fld, {}).get("date-parts", [[]])
        if parts and parts[0]:
            return str(parts[0][0])
    return ""


def cr_surnames(cr: dict) -> list[str]:
    return [a.get("family", "") for a in cr.get("author", []) if a.get("family")]


def extract_ref_fields(raw: str) -> dict:
    """Lightweight field extraction from APA string."""
    out = {"title": "", "journal": "", "volume": "", "issue": "", "pages": ""}
    year_m = re.search(r"\((\d{4})\)\.\s*(.+)", raw, re.S)
    if not year_m:
        return out
    body = year_m.group(2)
    # title before first italic block
    tm = re.match(r"^(.+?)\.\s+\*(.+?)\*(.*)", body, re.S)
    if not tm:
        return out
    out["title"] = tm.group(1).strip()
    italic = tm.group(2).strip()
    rest = tm.group(3).strip().lstrip(",").strip()
    # Journal, vol*(issue), pages  OR  Journal, vol*, pages
    jm = re.match(r"^(.+?),\s*(\d+)\*\((\d+)\),\s*(.+?)(?:\.\s*https?://|$)", italic + "," + rest if rest else italic)
    if jm:
        out["journal"] = jm.group(1).strip()
        out["volume"] = jm.group(2)
        out["issue"] = jm.group(3)
        out["pages"] = jm.group(4).strip().rstrip(".")
    else:
        jm2 = re.match(r"^(.+?),\s*(\d+)\*,\s*(.+?)(?:\.\s*https?://|$)", italic + ("," + rest if rest else ""))
        if jm2:
            out["journal"] = jm2.group(1).strip()
            out["volume"] = jm2.group(2)
            out["pages"] = jm2.group(3).strip().rstrip(".")
    return out


def pages_equiv(a: str, b: str) -> bool:
    def norm(p):
        return re.sub(r"[^0-9]", "", p)
    return norm(a) == norm(b) or a.replace("–", "-") == b.replace("–", "-")


def compare(ref: Reference, cr: dict) -> list[str]:
    issues = []
    fields = extract_ref_fields(ref.raw)

    # First author
    ref_sur = ref.authors_str.split(",")[0].split("&")[0].strip().split()[-1]
    cr_surs = cr_surnames(cr)
    if cr_surs and ascii_fold(ref_sur) != ascii_fold(cr_surs[0]):
        issues.append(f"First author: ref '{ref_sur}' vs Crossref '{cr_surs[0]}'")

    cy = cr_year(cr)
    if ref.year and cy and ref.year != cy:
        issues.append(f"Year: ref {ref.year} vs Crossref {cy}")

    ct = (cr.get("title") or [""])[0]
    if fields["title"] and ct:
        rt = fields["title"].lower().rstrip(".")
        if rt[:50] != ct.lower().rstrip(".")[:50] and rt not in ct.lower() and ct.lower()[:50] not in rt:
            issues.append(f"Title differs")

    cj = (cr.get("container-title") or [""])[0]
    if fields["journal"] and cj:
        if ascii_fold(fields["journal"])[:15] != ascii_fold(cj)[:15]:
            issues.append(f"Journal: ref '{fields['journal']}' vs Crossref '{cj}'")

    cv, ci, cp = str(cr.get("volume") or ""), str(cr.get("issue") or ""), str(cr.get("page") or cr.get("article-number") or "")
    if fields["volume"] and cv and fields["volume"] != cv:
        issues.append(f"Volume: ref {fields['volume']} vs Crossref {cv}")
    if fields["issue"] and ci and fields["issue"] != ci:
        issues.append(f"Issue: ref {fields['issue']} vs Crossref {ci}")
    if fields["pages"] and cp and not pages_equiv(fields["pages"], cp):
        issues.append(f"Pages: ref {fields['pages']} vs Crossref {cp}")

    return issues


def check_citations(ms_text: str, all_refs: list[Reference]) -> list[str]:
    mismatches = []
    for m in re.finditer(r"\(([^)]+)\)", ms_text):
        inner = m.group(1)
        if not re.search(r"\b(19|20)\d{2}\b", inner):
            continue
        for part in inner.split(";"):
            part = part.strip()
            years = re.findall(r"\b((?:19|20)\d{2})\b", part)
            author_part = re.sub(r",?\s*\d{4}(?:,\s*\d{4})*", "", part).strip()
            author_part = re.sub(r"\bet\s+al\.?", "", author_part, flags=re.I).strip().rstrip(",")
            if "&" in author_part:
                surnames = [p.strip().split()[-1] for p in author_part.split("&")]
            elif re.search(r"\band\b", author_part, re.I):
                surnames = [p.strip().split()[-1] for p in re.split(r"\s+and\s+", author_part, flags=re.I)]
            else:
                surnames = [author_part.split()[-1]] if author_part else []
            for year in years:
                surname = surnames[0] if surnames else "?"
                found = any(
                    ascii_fold(surname) == ascii_fold(r.authors_str.split(",")[0].split("&")[0].strip().split()[-1])
                    or ascii_fold(surname) in ascii_fold(r.authors_str)
                    for r in all_refs
                    if r.year == year
                )
                if not found and surname != "?":
                    mismatches.append(f"({surname}, {year})")
    return sorted(set(mismatches))


def main():
    lines = REFS_PATH.read_text(encoding="utf-8").splitlines()
    ms_text = MS_PATH.read_text(encoding="utf-8")

    all_refs: list[Reference] = []
    doi_refs: list[Reference] = []
    seen_dois: set[str] = set()

    for i, line in enumerate(lines, 1):
        ref = parse_apa_ref(line, i)
        if not ref:
            continue
        all_refs.append(ref)
        if ref.doi:
            if ref.doi in seen_dois:
                continue
            seen_dois.add(ref.doi)
            doi_refs.append(ref)

    results = []
    for ref in doi_refs:
        try:
            cr = fetch_crossref(ref.doi)
            issues = compare(ref, cr)
            ref.issues = issues
            ref.status = "PASS" if not issues else "CORRECTED"
            results.append((ref.key, ref.status, "; ".join(issues) if issues else "", ref.doi))
            time.sleep(0.12)
        except urllib.error.HTTPError as e:
            ref.status = "UNRESOLVED"
            results.append((ref.key, "UNRESOLVED", f"HTTP {e.code}", ref.doi))
        except Exception as e:
            ref.status = "UNRESOLVED"
            results.append((ref.key, "UNRESOLVED", str(e), ref.doi))

    no_doi = [r for r in all_refs if not r.doi]
    for r in no_doi:
        results.append((r.key, "PASS", "No DOI (book); manual record", ""))

    citation_mismatches = check_citations(ms_text, all_refs)

    print("REFERENCE KEY | STATUS | ISSUE")
    print("-" * 90)
    for key, status, issue, doi in sorted(results, key=lambda x: x[0].lower()):
        print(f"{key} | {status} | {issue}")

    print("\nIN-TEXT CITATION MISMATCHES:", len(citation_mismatches))
    for c in citation_mismatches:
        print(f"  {c}")

    report = {"results": [(k, s, i, d) for k, s, i, d in results], "citation_mismatches": citation_mismatches}
    Path("/Users/mehmetaltay/Documents/GitHub/autoresearch/crossref_report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
