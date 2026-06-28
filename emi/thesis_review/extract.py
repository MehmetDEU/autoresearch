"""Extract page text and annotations from the two thesis PDFs."""
import fitz
import json
from pathlib import Path

OUT = Path('/Users/mehmetaltay/Documents/GitHub/autoresearch/emi/thesis_review')
OUT.mkdir(parents=True, exist_ok=True)


def dump(pdf_path: str, tag: str) -> None:
    doc = fitz.open(pdf_path)
    pages_text = {}
    annots = []
    for i, page in enumerate(doc):
        pages_text[i + 1] = page.get_text("text")
        for a in page.annots() or []:
            info = a.info
            annots.append({
                "page": i + 1,
                "type": a.type[1],
                "rect": list(a.rect),
                "title": info.get("title", ""),
                "content": info.get("content", ""),
                "subject": info.get("subject", ""),
                "name": info.get("name", ""),
                "creationDate": info.get("creationDate", ""),
                "modDate": info.get("modDate", ""),
            })
    (OUT / f"{tag}_pages.json").write_text(
        json.dumps(pages_text, ensure_ascii=False, indent=2)
    )
    (OUT / f"{tag}_annots.json").write_text(
        json.dumps(annots, ensure_ascii=False, indent=2)
    )
    print(f"[{tag}] pages={doc.page_count} annots={len(annots)}")


dump('/Users/mehmetaltay/Desktop/TEZ salih.pdf', 'orig')
dump('/Users/mehmetaltay/Desktop/TEZ_commented_mehmet.pdf', 'prev')
