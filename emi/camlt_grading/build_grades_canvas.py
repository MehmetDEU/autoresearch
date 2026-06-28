#!/usr/bin/env python3
"""Generate camlt-final-grades.canvas.tsx from Desktop CSV files."""

from __future__ import annotations

import csv
import re
import statistics
from pathlib import Path

CSV = Path.home() / "Desktop" / "CAMLT_Final_Grades.csv"
OTHER_CSV = Path.home() / "Desktop" / "CAMLT_Other_Exam.csv"
OUT = Path(
    "/Users/mehmetaltay/.cursor/projects/Users-mehmetaltay-Documents-GitHub-autoresearch/canvases/camlt-final-grades.canvas.tsx"
)

EXAM_ABSENT = "E"


def esc(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")


def parse_row(r: dict) -> dict:
    notes = (r.get("notes") or "").strip()
    absent = r.get("total") == EXAM_ABSENT
    if absent:
        return {
            "id": r["idnumber"],
            "name": r["roster_fullname"].strip(),
            "group": r.get("course_group", ""),
            "s1": EXAM_ABSENT,
            "s2": EXAM_ABSENT,
            "s3": EXAM_ABSENT,
            "total": EXAM_ABSENT,
            "folder": r.get("folder") or "—",
            "notes": notes,
            "review": r.get("match_status", "") in ("matched_review", "id_name_mismatch"),
            "absent": True,
        }
    return {
        "id": r["idnumber"],
        "name": r["roster_fullname"].strip(),
        "group": r.get("course_group", ""),
        "s1": float(r["section1"]),
        "s2": float(r["section2"]),
        "s3": float(r["section3"]),
        "total": int(round(float(r["total"]))),
        "folder": r.get("folder") or "—",
        "notes": notes[:100] + ("..." if len(notes) > 100 else ""),
        "review": r.get("match_status", "") in ("matched_review", "id_name_mismatch"),
        "absent": False,
    }


def parse_other_row(r: dict) -> dict:
    return {
        "id": r.get("idnumber") or "—",
        "name": r.get("name_on_paper") or "—",
        "group": r.get("course_group") or "—",
        "s1": int(round(float(r["section1"]))),
        "s2": int(round(float(r["section2"]))),
        "s3": int(round(float(r["section3"]))),
        "total": int(round(float(r["total"]))),
        "folder": r.get("folder") or "—",
    }


def fmt_cell(value: float | int | str) -> str:
    if isinstance(value, str):
        return f'"{value}"'
    if value == int(value):
        return str(int(value))
    return str(value)


def main() -> None:
    all_rows: list[dict] = []
    with CSV.open(encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            all_rows.append(parse_row(r))

    entered = [r for r in all_rows if not r["absent"]]
    absent = [r for r in all_rows if r["absent"]]
    entered.sort(key=lambda x: -x["total"])
    absent.sort(key=lambda x: x["name"])

    other_rows: list[dict] = []
    if OTHER_CSV.exists():
        with OTHER_CSV.open(encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                other_rows.append(parse_other_row(r))
    other_rows.sort(key=lambda x: -x["total"])

    mean = statistics.mean(r["total"] for r in entered) if entered else 0.0
    pass50 = sum(1 for r in entered if r["total"] >= 50)
    pass60 = sum(1 for r in entered if r["total"] >= 60)
    review_rows = [r for r in entered if r["review"]]

    display_rows = entered + absent

    all_md = "\n".join(
        f"{i + 1}. **{r['name']}** — "
        + (
            f"**{EXAM_ABSENT}** (sınava girmedi)"
            if r["absent"]
            else f"EMI:{r['s1']:.0f} · TBLT:{r['s2']:.0f} · CBI:{r['s3']:.0f} · **{r['total']}/100**"
        )
        + (" · _eşleşme kontrolü_" if r.get("review") else "")
        for i, r in enumerate(display_rows)
    )

    absent_md = "\n".join(f"- **{r['name']}** (`{r['id']}`) — {EXAM_ABSENT}" for r in absent) or "_Yok_"

    other_md = "\n".join(
        f"- **{r['name']}** — EMI:{r['s1']} · TBLT:{r['s2']} · CBI:{r['s3']} · **{r['total']}/100** · `{r['folder']}`"
        for r in other_rows
    ) or "_Yok_"

    full_md = f"""# CAMLT Final Notları

## Özet
- Roster: **{len(all_rows)}** öğrenci
- Sınava giren: **{len(entered)}**
- Sınava girmeyen ({EXAM_ABSENT}): **{len(absent)}**
- Roster dışı kağıt: **{len(other_rows)}**
- Ortalama (girenler): **{mean:.1f}/100**
- ≥50/100: **{pass50}/{len(entered)}**
- ≥60/100: **{pass60}/{len(entered)}**

## Bölümler
- **Bölüm 1 — EMI:** 50 puan (1.a–1.d)
- **Bölüm 2 — TBLT:** 20 puan
- **Bölüm 3 — CBI:** 30 puan

## Sınava girmeyenler ({EXAM_ABSENT})
{absent_md}

## Roster dışı kağıtlar
{other_md}

## Tüm roster (toplam ↓, E en altta)
{all_md}
"""

    full_md_js = full_md.replace("\\", "\\\\").replace("`", "\\`")

    table_rows = []
    row_tones = []
    for i, r in enumerate(display_rows):
        mark = " ‡" if r["absent"] else (" †" if r.get("review") else "")
        table_rows.append(
            f'          [{i + 1}, "{esc(r["name"])}{mark}", "{r["id"]}", "{r["group"]}", '
            f'{fmt_cell(r["s1"])}, {fmt_cell(r["s2"])}, {fmt_cell(r["s3"])}, '
            f'{fmt_cell(r["total"])}, "{esc(r["folder"])}"],'
        )
        if r["absent"]:
            tone = "neutral"
        elif r["total"] >= 80:
            tone = "success"
        elif r["total"] >= 60:
            tone = "neutral"
        elif r["total"] >= 50:
            tone = "warning"
        else:
            tone = "danger"
        row_tones.append(f'          "{tone}",')

    other_table_rows = []
    for r in other_rows:
        other_table_rows.append(
            f'          ["{esc(r["name"])}", "{r["id"]}", {r["s1"]}, {r["s2"]}, {r["s3"]}, '
            f'{r["total"]}, "{r["folder"]}"],'
        )

    bands = [
        ("80–100", sum(1 for r in entered if r["total"] >= 80)),
        ("60–79", sum(1 for r in entered if 60 <= r["total"] < 80)),
        ("50–59", sum(1 for r in entered if 50 <= r["total"] < 60)),
        ("<50", sum(1 for r in entered if r["total"] < 50)),
        (f"{EXAM_ABSENT} (girmedi)", len(absent)),
    ]
    band_js = ""
    for label, count in bands:
        band_js += f"""
        <Row gap={{12}} align="center">
          <Text style={{{{ width: 160, fontSize: 12 }}}}>{{"{label}"}}</Text>
          <Text style={{{{ width: 32, fontSize: 12, textAlign: "right" }}}}>{{{count}}}</Text>
          <div style={{{{ flex: 1, height: 8, background: t.fill.tertiary, borderRadius: 2, overflow: "hidden" }}}}>
            <div style={{{{ width: `${{({count} / {len(all_rows)}) * 100}}%`, height: "100%", background: t.text.secondary }}}} />
          </div>
        </Row>"""

    content = f'''import {{
  Callout,
  Card,
  CardBody,
  Divider,
  Grid,
  H1,
  H2,
  H3,
  Row,
  Stack,
  Stat,
  Table,
  Text,
  useHostTheme,
}} from "cursor/canvas";

const MEAN = {mean:.4f};
const PASS50 = {pass50};
const PASS60 = {pass60};
const ROSTER_COUNT = {len(all_rows)};
const ENTERED_COUNT = {len(entered)};
const ABSENT_COUNT = {len(absent)};
const OTHER_COUNT = {len(other_rows)};
const REVIEW_COUNT = {len(review_rows)};

const FULL_MD = `{full_md_js}`;

export default function CamltFinalGradesCanvas() {{
  const {{ tokens: t }} = useHostTheme();

  return (
    <Stack gap={{20}}>
      <Stack gap={{6}}>
        <H1>CAMLT Final Notları</H1>
        <Text tone="secondary">
          Current Approaches and Methods in Language Teaching · {{ROSTER_COUNT}} roster · {{ENTERED_COUNT}} girdi · {{ABSENT_COUNT}} E
        </Text>
      </Stack>

      <Grid columns={{4}} gap={{12}}>
        <Stat label="Ortalama (girenler)" value={{`${{MEAN.toFixed(1)}}}}/100`}} tone="info" />
        <Stat label="≥60/100" value={{`${{PASS60}}/${{ENTERED_COUNT}}`}} tone="success" />
        <Stat label="≥50/100" value={{`${{PASS50}}/${{ENTERED_COUNT}}`}} tone="neutral" />
        <Stat label="E — girmedi" value={{String(ABSENT_COUNT)}} tone="warning" />
      </Grid>

      <Callout tone="info" title="Bölüm puanları">
        <strong>EMI</strong> (Bölüm 1): /50 · <strong>TBLT</strong> (Bölüm 2): /20 · <strong>CBI</strong> (Bölüm 3): /30 · Toplam: /100.
        † eşleşme kontrolü (ID/isim) · ‡ girmedi (E)
      </Callout>

      <H2>Roster dışı kağıtlar ({{OTHER_COUNT}})</H2>
      <Table
        headers={{["Ad (kağıt)", "ID", "EMI/50", "TBLT/20", "CBI/30", "Toplam/100", "Klasör"]}}
        columnAlign={{["left", "left", "right", "right", "right", "right", "left"]}}
        rows={{[
{chr(10).join(other_table_rows) if other_table_rows else '          ["—", "—", "—", "—", "—", "—", "—"],'}
        ]}}
      />

      <H2>Tüm roster</H2>
      <Table
        headers={{["#", "Ad Soyad", "ID", "Grup", "EMI/50", "TBLT/20", "CBI/30", "Toplam", "Klasör"]}}
        columnAlign={{["right", "left", "left", "left", "right", "right", "right", "right", "left"]}}
        rowTone={{[
{chr(10).join(row_tones)}
        ]}}
        striped
        rows={{[
{chr(10).join(table_rows)}
        ]}}
      />

      <Divider />

      <H2>Markdown rapor</H2>
      <Card>
        <CardBody>
          <Text
            as="span"
            style={{{{
              whiteSpace: "pre-wrap",
              display: "block",
              fontFamily: "ui-monospace, SFMono-Regular, Menlo, monospace",
              fontSize: 12,
              lineHeight: 1.55,
              color: t.text.primary,
            }}}}
          >
            {{FULL_MD}}
          </Text>
        </CardBody>
      </Card>

      <H3>Bölüm ortalamaları (girenler)</H3>
      <Grid columns={{4}} gap={{12}}>
        <Stat label="EMI (Bölüm 1)" value="{statistics.mean(r['s1'] for r in entered):.1f}/50" />
        <Stat label="TBLT (Bölüm 2)" value="{statistics.mean(r['s2'] for r in entered):.1f}/20" />
        <Stat label="CBI (Bölüm 3)" value="{statistics.mean(r['s3'] for r in entered):.1f}/30" />
        <Stat label="Eşleşme kontrolü" value="{len(review_rows)}" />
      </Grid>

      <H3>Not dağılımı</H3>
      <Stack gap={{8}}>{band_js}
      </Stack>
    </Stack>
  );
}}
'''
    OUT.write_text(content, encoding="utf-8")
    print(
        f"Wrote {OUT} (roster={len(all_rows)}, entered={len(entered)}, "
        f"absent={len(absent)}, other={len(other_rows)}, mean={mean:.1f})"
    )


if __name__ == "__main__":
    main()
