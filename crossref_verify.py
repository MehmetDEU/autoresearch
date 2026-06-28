#!/usr/bin/env python3
"""Cross-check APA7 references against Crossref API and verify in-text citations."""

import json
import re
import sys
import time
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

DOI_RE = re.compile(r"https?://doi\.org/([^\s\)]+)", re.I)


@dataclass
class Reference:
    line_no: int
    raw: str
    key: str
    doi: Optional[str] = None
    authors_str: str = ""
    year: str = ""
    title: str = ""
    journal: str = ""
    volume: str = ""
    issue: str = ""
    pages: str = ""
    is_book: bool = False
    issues: list = field(default_factory=list)
    status: str = "PASS"
    corrected_raw: Optional[str] = None


def normalize(s: str) -> str:
    s = s.lower().strip()
    s = s.replace("’", "'").replace("‘", "'").replace("–", "-").replace("—", "-")
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"[^\w\s\-']", "", s)
    return s


def parse_apa_ref(line: str, line_no: int) -> Optional[Reference]:
    line = line.strip()
    if not line.startswith("- "):
        return None
    raw = line[2:].strip()
    doi_match = DOI_RE.search(raw)
    doi = doi_match.group(1) if doi_match else None

    # Extract year
    year_match = re.search(r"\((\d{4})\)", raw)
    year = year_match.group(1) if year_match else ""

    # Extract authors (before year)
    if year_match:
        authors_str = raw[: year_match.start()].strip().rstrip(",")
    else:
        authors_str = raw.split(".")[0] if "." in raw else raw

    # Build key: first author surname + year
    first_author = authors_str.split(",")[0].split("&")[0].strip()
    # Handle "Ekoç Özçelik" style
    surname = first_author.split()[-1] if first_author else "Unknown"
    key = f"{surname} ({year})" if year else surname

    # Parse title, journal, volume, issue, pages
    title = journal = volume = issue = pages = ""
    is_book = doi is None and "*" in raw

    if year_match:
        after_year = raw[year_match.end() :].strip().lstrip(". ")
        # Split title (italic) from rest
        italic_match = re.match(r"\*(.+?)\*(.*)", after_year, re.S)
        if italic_match:
            title_part = italic_match.group(1).strip()
            rest = italic_match.group(2).strip()
            if rest.startswith(","):
                rest = rest[1:].strip()
            # Journal article: *Journal, vol*(issue), pages
            jm = re.match(
                r"^(.+?),\s*(\d+)\*\((\d+)\),\s*(.+?)(?:\.\s*https?://|$)",
                title_part + ("," + rest if rest else ""),
            )
            if jm:
                journal = jm.group(1).strip()
                volume = jm.group(2)
                issue = jm.group(3)
                pages = jm.group(4).strip().rstrip(".")
                # Title is before the italic journal part in full string
                title_before = after_year.split("*")[0].strip().rstrip(".")
                title = title_before if title_before else ""
            else:
                # Try: *Title* or *Journal, vol*, pages (no issue)
                # Pattern: title. *Journal, vol*(issue), pages
                tm = re.match(
                    r"^(.+?)\.\s*\*(.+?),\s*(\d+)\*\((\d+)\),\s*(.+?)(?:\.\s*https?://|$)",
                    after_year,
                    re.S,
                )
                if tm:
                    title = tm.group(1).strip()
                    journal = tm.group(2).strip()
                    volume = tm.group(3)
                    issue = tm.group(4)
                    pages = tm.group(5).strip().rstrip(".")
                else:
                    tm2 = re.match(
                        r"^(.+?)\.\s*\*(.+?),\s*(\d+)\*,\s*(.+?)(?:\.\s*https?://|$)",
                        after_year,
                        re.S,
                    )
                    if tm2:
                        title = tm2.group(1).strip()
                        journal = tm2.group(2).strip()
                        volume = tm2.group(3)
                        pages = tm2.group(4).strip().rstrip(".")
                    else:
                        # Book/chapter: title in italics only
                        title = title_part
                        if rest:
                            title += " " + rest.split(".")[0]

    return Reference(
        line_no=line_no,
        raw=raw,
        key=key,
        doi=doi,
        authors_str=authors_str,
        year=year,
        title=title,
        journal=journal,
        volume=volume,
        issue=issue,
        pages=pages,
        is_book=is_book,
    )


def fetch_crossref(doi: str) -> dict:
    url = f"https://api.crossref.org/works/{doi}"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "autoresearch-ref-check/1.0 (mailto:verify@example.com)"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def cr_author_surnames(cr: dict) -> list[str]:
    names = []
    for a in cr.get("author", []):
        fam = a.get("family", "")
        if fam:
            names.append(normalize(fam))
    return names


def cr_year(cr: dict) -> str:
    for field in ("published-print", "published-online", "created", "issued"):
        parts = cr.get(field, {}).get("date-parts", [[]])
        if parts and parts[0]:
            return str(parts[0][0])
    return ""


def cr_title(cr: dict) -> str:
    t = cr.get("title", [""])[0] if cr.get("title") else ""
    return t


def cr_journal(cr: dict) -> str:
    for key in ("container-title", "short-container-title"):
        if cr.get(key):
            return cr[key][0]
    return ""


def cr_volume(cr: dict) -> str:
    return str(cr.get("volume", "") or "")


def cr_issue(cr: dict) -> str:
    return str(cr.get("issue", "") or "")


def cr_pages(cr: dict) -> str:
    page = cr.get("page", "")
    if page:
        return page
    sp = cr.get("article-number", "")
    return str(sp) if sp else ""


def format_apa_authors(cr_authors: list, max_shown: int = 20) -> str:
    """Format Crossref authors in APA7 style."""
    if not cr_authors:
        return ""
    formatted = []
    for a in cr_authors:
        fam = a.get("family", "")
        given = a.get("given", "")
        initials = ". ".join(g[0] for g in given.replace(".", " ").split() if g) + "."
        if fam:
            formatted.append(f"{fam}, {initials}" if initials else fam)
    n = len(formatted)
    if n == 0:
        return ""
    if n == 1:
        return formatted[0]
    if n == 2:
        return f"{formatted[0]}, & {formatted[1]}"
    if n <= 20:
        return ", ".join(formatted[:-1]) + f", & {formatted[-1]}"
    # 21+ authors: first 19, ..., last
    return ", ".join(formatted[:19]) + ", . . . " + formatted[-1]


def pages_match(ref_pages: str, cr_pages: str) -> bool:
    rp = normalize(ref_pages)
    cp = normalize(cr_pages)
    if rp == cp:
        return True
    # Article number vs pages
    if rp == cp:
        return True
    # Range: 1125-1142 vs 1125–1142
    rp2 = rp.replace("-", "")
    cp2 = cp.replace("-", "")
    if rp2 == cp2:
        return True
    # One might be article number
    if rp in cp or cp in rp:
        return True
    return False


def compare_ref(ref: Reference, cr: dict) -> list[str]:
    issues = []
    cr_authors = cr.get("author", [])
    cr_surnames = cr_author_surnames(cr)

    # Check first author surname
    ref_first = normalize(ref.authors_str.split(",")[0].split("&")[0].strip().split()[-1])
    if cr_surnames and ref_first not in cr_surnames[0] and cr_surnames[0] not in ref_first:
        # Handle compound surnames, special chars
        if not any(ref_first in s or s in ref_first for s in cr_surnames[:3]):
            issues.append(
                f"First author mismatch: ref='{ref.authors_str.split(',')[0]}' vs Crossref='{cr_surnames[0] if cr_surnames else '?'}'"
            )

    # Year
    cy = cr_year(cr)
    if ref.year and cy and ref.year != cy:
        issues.append(f"Year mismatch: ref={ref.year} vs Crossref={cy}")

    # Title (fuzzy)
    rt = normalize(ref.title)
    ct = normalize(cr_title(cr))
    if rt and ct:
        # Compare first 40 chars or full if short
        if rt[:40] != ct[:40] and rt not in ct and ct not in rt:
            # Check if ref title is empty due to parse failure - use raw
            issues.append(f"Title mismatch: ref='{ref.title[:60]}...' vs Crossref='{cr_title(cr)[:60]}...'")

    # Journal
    rj = normalize(ref.journal)
    cj = normalize(cr_journal(cr))
    if rj and cj and rj[:20] != cj[:20] and rj not in cj and cj not in rj:
        issues.append(f"Journal mismatch: ref='{ref.journal}' vs Crossref='{cr_journal(cr)}'")

    # Volume
    cv = cr_volume(cr)
    if ref.volume and cv and ref.volume != cv:
        issues.append(f"Volume mismatch: ref={ref.volume} vs Crossref={cv}")

    # Issue
    ci = cr_issue(cr)
    if ref.issue and ci and ref.issue != ci:
        issues.append(f"Issue mismatch: ref={ref.issue} vs Crossref={ci}")

    # Pages
    cp = cr_pages(cr)
    if ref.pages and cp and not pages_match(ref.pages, cp):
        issues.append(f"Pages mismatch: ref={ref.pages} vs Crossref={cp}")

    return issues


def build_corrected_entry(ref: Reference, cr: dict) -> str:
    """Rebuild APA7 entry from Crossref metadata."""
    authors = format_apa_authors(cr.get("author", []))
    year = cr_year(cr)
    title = cr_title(cr)
    journal = cr_journal(cr)
    volume = cr_volume(cr)
    issue = cr_issue(cr)
    pages = cr_pages(cr)
    doi = ref.doi

    if journal and volume:
        if issue:
            body = f"{authors} ({year}). {title}. *{journal}, {volume}*({issue}), {pages}."
        else:
            body = f"{authors} ({year}). {title}. *{journal}, {volume}*, {pages}."
    elif cr.get("type") == "book-chapter":
        # Keep original book info if chapter
        return ref.raw
    else:
        body = f"{authors} ({year}). {title}."
    if doi:
        body += f" https://doi.org/{doi}"
    return body


def extract_citation_keys(text: str) -> set[str]:
    """Extract author-year keys from in-text citations."""
    keys = set()
    # Find all parenthetical citations
    for m in re.finditer(r"\(([^)]+)\)", text):
        inner = m.group(1)
        if not re.search(r"\d{4}", inner):
            continue
        # Split on semicolon for multiple citations
        for part in inner.split(";"):
            part = part.strip()
            # Extract year(s)
            years = re.findall(r"\b(19|20)\d{2}\b", part)
            if not years:
                continue
            # Remove years and et al for author extraction
            author_part = re.sub(r",?\s*\d{4}(?:,\s*\d{4})*", "", part).strip()
            author_part = author_part.replace("et al.", "").strip().rstrip(",")
            # Get first author surname
            if "&" in author_part:
                first = author_part.split("&")[0].strip()
            elif " and " in author_part.lower():
                first = re.split(r"\s+and\s+", author_part, flags=re.I)[0].strip()
            else:
                first = author_part.split(",")[0].strip() if "," in author_part else author_part.split()[-1]
            surname = first.split()[-1] if first else ""
            for year in re.findall(r"\b((?:19|20)\d{2})\b", part):
                keys.add(f"{surname} ({year})")
                # Also add normalized
                keys.add(f"{normalize(surname)} ({year})")
    return keys


def main():
    refs_text = REFS_PATH.read_text(encoding="utf-8")
    ms_text = MS_PATH.read_text(encoding="utf-8")

    lines = refs_text.splitlines()
    references: list[Reference] = []
    seen_dois: dict[str, Reference] = {}

    for i, line in enumerate(lines, 1):
        ref = parse_apa_ref(line, i)
        if ref and ref.doi:
            if ref.doi in seen_dois:
                continue  # skip duplicate instrument section entries
            seen_dois[ref.doi] = ref
            references.append(ref)
        elif ref and not ref.doi and ref.year:
            references.append(ref)  # books without DOI

    results = []
    corrections = {}  # line_no -> new text

    for ref in references:
        if not ref.doi:
            results.append((ref.key, "PASS", "No DOI (book/chapter); skipped Crossref", ref))
            continue

        try:
            data = fetch_crossref(ref.doi)
            cr = data.get("message", {})
            issues = compare_ref(ref, cr)
            ref.issues = issues

            if issues:
                corrected = build_corrected_entry(ref, cr)
                ref.corrected_raw = corrected
                ref.status = "CORRECTED"
                corrections[ref.line_no] = f"- {corrected}"
                results.append((ref.key, "CORRECTED", "; ".join(issues), ref))
            else:
                ref.status = "PASS"
                results.append((ref.key, "PASS", "", ref))

            time.sleep(0.15)  # polite rate limiting
        except urllib.error.HTTPError as e:
            ref.status = "UNRESOLVED"
            msg = f"Crossref HTTP {e.code} for DOI {ref.doi}"
            results.append((ref.key, "UNRESOLVED", msg, ref))
        except Exception as e:
            ref.status = "UNRESOLVED"
            results.append((ref.key, "UNRESOLVED", str(e), ref))

    # Build ref keys from reference list
    ref_keys = set()
    for ref in references:
        ref_keys.add(ref.key)
        ref_keys.add(normalize(ref.key.split(" (")[0]) + " (" + ref.key.split("(")[1] if "(" in ref.key else ref.key)

    # Parse all refs for citation matching (including no-DOI)
    all_refs = []
    for i, line in enumerate(lines, 1):
        r = parse_apa_ref(line, i)
        if r and r.year and line.strip().startswith("- ") and not line.strip().startswith("- Ryan & Connell"):
            # skip instrument duplicate lines
            if "validated instrument" in line or "autonomy-support" in line or "L2MSS" in line or "large-scale" in line or "Self-Construal" in line or "self-construal review" in line or "linguistic capital" in line:
                continue
            all_refs.append(r)

    ref_key_map = {}
    for r in all_refs:
        first = r.authors_str.split(",")[0].split("&")[0].strip()
        surname = first.split()[-1]
        k = f"{surname} ({r.year})"
        ref_key_map[normalize(surname)] = k
        ref_key_map[k] = k
        # Two-author: also map second author
        if "&" in r.authors_str:
            parts = re.split(r"\s*&\s*", r.authors_str)
            if len(parts) == 2:
                s2 = parts[1].split()[-1]
                ref_key_map[normalize(s2)] = f"{s2} ({r.year})"

    # Check in-text citations
    citation_issues = []
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
            elif " and " in author_part.lower():
                surnames = [p.strip().split()[-1] for p in re.split(r"\s+and\s+", author_part, flags=re.I)]
            else:
                surnames = [author_part.split()[-1]] if author_part else []

            for year in years:
                surname = surnames[0] if surnames else "?"
                nk = normalize(surname)
                found = False
                for r in all_refs:
                    rs = normalize(r.authors_str.split(",")[0].split("&")[0].strip().split()[-1])
                    if rs == nk and r.year == year:
                        found = True
                        break
                    if nk in normalize(r.authors_str) and r.year == year:
                        found = True
                        break
                if not found and surname != "?":
                    citation_issues.append(f"({surname}, {year}) — not in reference list")

    # Apply corrections to file
    if corrections:
        new_lines = []
        for i, line in enumerate(lines, 1):
            if i in corrections:
                new_lines.append(corrections[i])
            else:
                new_lines.append(line)
        # Update total count if needed
        new_text = "\n".join(new_lines)
        if not new_text.endswith("\n"):
            new_text += "\n"
        REFS_PATH.write_text(new_text, encoding="utf-8")

    # Output report
    print("=" * 80)
    print("REFERENCE CROSS-CHECK REPORT")
    print("=" * 80)
    print(f"\n{'Reference key':<35} {'Status':<12} What was wrong")
    print("-" * 80)
    for key, status, wrong, ref in sorted(results, key=lambda x: x[0]):
        wrong_display = wrong[:80] + "..." if len(wrong) > 80 else wrong
        print(f"{key:<35} {status:<12} {wrong_display}")

    print("\n" + "=" * 80)
    print("IN-TEXT CITATION CHECK")
    print("=" * 80)
    if citation_issues:
        for ci in sorted(set(citation_issues)):
            print(f"  MISMATCH: {ci}")
    else:
        print("  All in-text citations match the reference list.")

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    passed = sum(1 for _, s, _, _ in results if s == "PASS")
    corrected = sum(1 for _, s, _, _ in results if s == "CORRECTED")
    unresolved = sum(1 for _, s, _, _ in results if s == "UNRESOLVED")
    print(f"Total DOI references checked: {len([r for r in references if r.doi])}")
    print(f"PASS: {passed} | CORRECTED: {corrected} | UNRESOLVED: {unresolved}")
    print(f"Citation mismatches: {len(set(citation_issues))}")
    if corrections:
        print(f"\nApplied {len(corrections)} correction(s) to {REFS_PATH}")

    # Write detailed JSON for debugging
    report_path = Path("/Users/mehmetaltay/Documents/GitHub/autoresearch/crossref_report.json")
    report = {
        "results": [(k, s, w) for k, s, w, _ in results],
        "citation_issues": list(set(citation_issues)),
        "corrections_applied": len(corrections),
    }
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Detailed report: {report_path}")


if __name__ == "__main__":
    main()
