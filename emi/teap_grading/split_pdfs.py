#!/usr/bin/env python3
"""Split TEAP scanned PDFs into front-back page pairs."""

from __future__ import annotations

import json
from pathlib import Path

import fitz

DOWNLOADS = Path.home() / "Downloads"
ROOT = Path(__file__).resolve().parent
STUDENTS_DIR = ROOT / "students"
MANIFEST_PATH = ROOT / "manifest.json"

PDFS = [
    ("jeap1.pdf", "batch1"),
    ("jeap2.pdf", "batch2"),
    ("jeap3.pdf", "batch3"),
    ("eap4.pdf", "batch4"),
]


def render_page(doc: fitz.Document, page_index: int, out_path: Path) -> None:
    pix = doc[page_index].get_pixmap(matrix=fitz.Matrix(2, 2))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    pix.save(str(out_path))


def main() -> None:
    manifest: dict = {"pairs": [], "anomalies": []}
    pair_id = 0

    if STUDENTS_DIR.exists():
        import shutil

        shutil.rmtree(STUDENTS_DIR)
    STUDENTS_DIR.mkdir(parents=True)

    for pdf_name, batch in PDFS:
        pdf_path = DOWNLOADS / pdf_name
        doc = fitz.open(pdf_path)
        page_count = doc.page_count
        full_pairs = page_count // 2
        remainder = page_count % 2

        for i in range(full_pairs):
            pair_id += 1
            front_idx = i * 2
            back_idx = front_idx + 1
            folder = STUDENTS_DIR / f"{pair_id:03d}_{batch}"
            front_png = folder / "front.png"
            back_png = folder / "back.png"
            render_page(doc, front_idx, front_png)
            render_page(doc, back_idx, back_png)
            entry = {
                "id": pair_id,
                "batch": batch,
                "source_pdf": pdf_name,
                "source_pages": [front_idx + 1, back_idx + 1],
                "folder": str(folder.relative_to(ROOT)),
                "status": "pending_identification",
            }
            manifest["pairs"].append(entry)

        if remainder:
            orphan_idx = page_count - 1
            orphan_png = ROOT / "anomalies" / f"{batch}_orphan_p{orphan_idx + 1}.png"
            render_page(doc, orphan_idx, orphan_png)
            manifest["anomalies"].append(
                {
                    "type": "orphan_page",
                    "source_pdf": pdf_name,
                    "page": orphan_idx + 1,
                    "image": str(orphan_png.relative_to(ROOT)),
                    "note": "Unpaired page at end of PDF. jeap2 p31 verified as duplicate front of pair 038 (230907107).",
                    "status": "duplicate_not_missing",
                }
            )

        doc.close()

    manifest["summary"] = {
        "total_pairs": len(manifest["pairs"]),
        "total_anomalies": len(manifest["anomalies"]),
        "by_batch": {b: sum(1 for p in manifest["pairs"] if p["batch"] == b) for _, b in PDFS},
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(manifest["summary"], indent=2))


if __name__ == "__main__":
    main()
