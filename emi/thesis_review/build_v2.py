"""Build TEZ_commented_mehmet_v2.pdf.

Strategy:
- Open the ORIGINAL thesis (which already carries the 35 hand-written
  Mehmet Altay annotations).
- Add the 29 new content-specific sticky notes from notes.py.
- Save to v2.
- Reopen and verify every annotation has /T = "Mehmet Altay".
- Print the page-by-page list of new notes.

This way the 35 originals are preserved byte-equivalent and the 15 generic
"Supervisor Note" entries from the previous attempt are dropped.
"""
from __future__ import annotations

import sys
from pathlib import Path

import fitz  # PyMuPDF
import pikepdf

sys.path.insert(0, str(Path(__file__).parent))
from notes import NOTES  # noqa: E402

SRC = "/Users/mehmetaltay/Desktop/TEZ salih.pdf"
OUT = "/Users/mehmetaltay/Desktop/TEZ_commented_mehmet_v2.pdf"
AUTHOR = "Mehmet Altay"


def add_notes(src_path: str, out_path: str) -> int:
    doc = fitz.open(src_path)
    added = 0
    for page_no, point, content in NOTES:
        page = doc[page_no - 1]
        x, y = point
        page_rect = page.rect
        x = max(20.0, min(x, page_rect.width - 40))
        y = max(40.0, min(y, page_rect.height - 40))
        annot = page.add_text_annot(fitz.Point(x, y), content, icon="Note")
        annot.set_info(
            title=AUTHOR,
            content=content,
            subject="Yapışkan Not",
        )
        annot.set_colors(stroke=(1.0, 0.85, 0.2))
        annot.update()
        added += 1
    doc.save(out_path, garbage=4, deflate=True)
    doc.close()
    return added


def force_author_pikepdf(path: str) -> int:
    """Make absolutely sure every annotation /T is 'Mehmet Altay'."""
    fixed = 0
    with pikepdf.open(path, allow_overwriting_input=True) as pdf:
        for page in pdf.pages:
            if "/Annots" not in page:
                continue
            for ref in page["/Annots"]:
                annot = ref
                if "/Subtype" not in annot:
                    continue
                subtype = str(annot["/Subtype"])
                if subtype in ("/Link",):
                    continue
                annot["/T"] = pikepdf.String(AUTHOR)
                fixed += 1
        pdf.save(path)
    return fixed


def verify(path: str):
    doc = fitz.open(path)
    rows = []
    bad = []
    for i, page in enumerate(doc):
        for a in page.annots() or []:
            info = a.info
            rows.append({
                "page": i + 1,
                "type": a.type[1],
                "title": info.get("title", ""),
                "content": info.get("content", ""),
            })
            if info.get("title", "") != AUTHOR:
                bad.append((i + 1, info.get("title", ""), a.type[1]))
    doc.close()
    return rows, bad


if __name__ == "__main__":
    added = add_notes(SRC, OUT)
    fixed = force_author_pikepdf(OUT)
    rows, bad = verify(OUT)
    print(f"Added new sticky notes: {added}")
    print(f"pikepdf /T rewrites:     {fixed}")
    print(f"Total annotations:       {len(rows)}")
    print(f"Non-Mehmet annotations:  {len(bad)}")
    if bad:
        for b in bad:
            print("  BAD:", b)
    else:
        print("All annotations carry /T = 'Mehmet Altay'.")
