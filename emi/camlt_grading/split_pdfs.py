#!/usr/bin/env python3
"""Split CAMLT scanned PDFs (cam1–cam3) into front-back pairs."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import fitz

DOWNLOADS = Path.home() / "Downloads"
ROOT = Path(__file__).resolve().parent
STUDENTS_DIR = ROOT / "students"
MANIFEST_PATH = ROOT / "manifest.json"

PDFS = [
    ("cam1.pdf", "cam1"),
    ("cam2.pdf", "cam2"),
    ("cam3.pdf", "cam3"),
]


def render_page(doc: fitz.Document, page_index: int, out_path: Path) -> None:
    pix = doc[page_index].get_pixmap(matrix=fitz.Matrix(2, 2))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    pix.save(str(out_path))


def main() -> None:
    if STUDENTS_DIR.exists():
        shutil.rmtree(STUDENTS_DIR)
    STUDENTS_DIR.mkdir(parents=True)

    manifest: dict = {"pairs": [], "anomalies": [], "sources": [p for p, _ in PDFS]}
    pair_id = 0

    for pdf_name, batch in PDFS:
        pdf_path = DOWNLOADS / pdf_name
        if not pdf_path.exists():
            raise SystemExit(f"Missing PDF: {pdf_path}")
        doc = fitz.open(pdf_path)
        page_count = doc.page_count
        full_pairs = page_count // 2
        remainder = page_count % 2

        for i in range(full_pairs):
            pair_id += 1
            front_idx = i * 2
            back_idx = front_idx + 1
            folder = STUDENTS_DIR / f"{pair_id:03d}_{batch}"
            render_page(doc, front_idx, folder / "front.png")
            render_page(doc, back_idx, folder / "back.png")
            manifest["pairs"].append(
                {
                    "id": pair_id,
                    "batch": batch,
                    "source_pdf": pdf_name,
                    "source_pages": [front_idx + 1, back_idx + 1],
                    "folder": f"students/{pair_id:03d}_{batch}",
                }
            )

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
