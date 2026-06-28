#!/usr/bin/env python3
"""Generate teap-final-grades.canvas.tsx from Desktop CSV files."""

from __future__ import annotations

import csv
import re
import statistics
from pathlib import Path

from participation import PRESENTATION_CREDIT_IDS, SURVEY_Q1_CREDIT_IDS

CSV = Path.home() / "Desktop" / "TEAP_Final_Grades.csv"
OTHER_CSV = Path.home() / "Desktop" / "TEAP_Other_Courses_Exam.csv"
OUT = Path(
    "/Users/mehmetaltay/.cursor/projects/Users-mehmetaltay-Documents-GitHub-autoresearch/canvases/teap-final-grades.canvas.tsx"
)

EXAM_ABSENT = "E"


def esc(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")


def parse_row(r: dict) -> dict:
    notes = re.sub(r"\s*\[duplicate.*", "", r.get("notes") or "").strip()
    sid = r["idnumber"]
    absent = r.get("total") == EXAM_ABSENT
    if absent:
        return {
            "id": sid,
            "name": f'{r["firstname"].strip()} {r["lastname"].strip()}',
            "part": EXAM_ABSENT,
            "s1": EXAM_ABSENT,
            "s2": EXAM_ABSENT,
            "s3": EXAM_ABSENT,
            "total": EXAM_ABSENT,
            "pct100": EXAM_ABSENT,
            "folder": r.get("folder") or "—",
            "notes": notes,
            "survey_adj": False,
            "pres_adj": False,
            "absent": True,
        }
    total = float(r["total"])
    return {
        "id": sid,
        "name": f'{r["firstname"].strip()} {r["lastname"].strip()}',
        "part": float(r["participation"]),
        "s1": float(r["section_i"]),
        "s2": float(r["section_ii"]),
        "s3": float(r["section_iii"]),
        "total": total,
        "pct100": round(total * 100 / 60, 1),
        "folder": r["folder"],
        "notes": notes[:100] + ("..." if len(notes) > 100 else ""),
        "survey_adj": sid in SURVEY_Q1_CREDIT_IDS,
        "pres_adj": sid in PRESENTATION_CREDIT_IDS,
        "absent": False,
    }


def parse_other_row(r: dict) -> dict:
    total_60 = int(float(r["total"]))
    total_100 = int(r.get("total_100") or scale_to_100(total_60))
    part_100 = int(r.get("participation_100") or scale_to_100(float(r["participation"])))
    s1_100 = int(r.get("section_i_100") or scale_to_100(float(r["section_i"])))
    s2_100 = int(r.get("section_ii_100") or scale_to_100(float(r["section_ii"])))
    s3_100 = int(r.get("section_iii_100") or scale_to_100(float(r["section_iii"])))
    return {
        "id": r["idnumber"],
        "name": r.get("name_on_paper") or f'{r["firstname"]} {r["lastname"]}',
        "part": float(r["participation"]),
        "s1": float(r["section_i"]),
        "s2": float(r["section_ii"]),
        "s3": float(r["section_iii"]),
        "total": total_60,
        "part_100": part_100,
        "s1_100": s1_100,
        "s2_100": s2_100,
        "s3_100": s3_100,
        "total_100": total_100,
        "pct100": total_100,
        "folder": r["folder"],
        "group": r.get("course_group", "diğer dersler"),
    }


def fmt_cell(value: float | str) -> str:
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

    other_rows: list[dict] = []
    if OTHER_CSV.exists():
        with OTHER_CSV.open(encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                other_rows.append(parse_other_row(r))
    other_rows.sort(key=lambda x: -x["total"])

    mean = statistics.mean(r["total"] for r in entered) if entered else 0.0
    pass36 = sum(1 for r in entered if r["total"] >= 36)
    pass42 = sum(1 for r in entered if r["total"] >= 42)
    survey_rows = [r for r in entered if r["id"] in SURVEY_Q1_CREDIT_IDS]
    pres_rows = [r for r in entered if r["id"] in PRESENTATION_CREDIT_IDS]

    display_rows = entered + absent

    survey_md = "\n".join(
        f"- **{r['name']}** (`{r['id']}`) — Kat:{r['part']:.0f} · I:{r['s1']:.0f} · II:{r['s2']:.0f} · III:{r['s3']:.1f} · **{r['total']:.1f}/60**"
        for r in sorted(survey_rows, key=lambda x: -x["total"])
    )

    all_md = "\n".join(
        f"{i + 1}. **{r['name']}** — "
        + (
            f"**{EXAM_ABSENT}** (sınava girmedi)"
            if r["absent"]
            else f"Kat:{r['part']:.0f} · I:{r['s1']:.0f} · II:{r['s2']:.0f} · III:{r['s3']:.1f} · **{r['total']:.1f}/60** ({r['pct100']}/100)"
        )
        + (" · _anket listesinde_" if r.get("survey_adj") else "")
        + (" · _sunum listesinde_" if r.get("pres_adj") else "")
        for i, r in enumerate(display_rows)
    )

    absent_md = "\n".join(
        f"- **{r['name']}** (`{r['id']}`) — {EXAM_ABSENT}" for r in absent
    ) or "_Yok_"

    other_md = "\n".join(
        f"- **{r['name']}** (`{r['id']}`) — {r['folder']} — "
        f"{r['total']}/60 → **{r['total_100']}/100** · _diğer dersler, orantılı_"
        for r in other_rows
    ) or "_Yok_"

    full_md = f"""# TEAP Final Notları (güncel)

## Özet
- Roster: **{len(all_rows)}** öğrenci
- Sınava giren: **{len(entered)}**
- Sınava girmeyen ({EXAM_ABSENT}): **{len(absent)}**
- Diğer dersler (sınav kağıdı var, listede yok): **{len(other_rows)}**
- Ortalama (girenler): **{mean:.1f}/60** (~{mean * 100 / 60:.0f}/100)
- Geçen (≥36/60): **{pass36}/{len(entered)}**
- Soner Polat anketi Q1 kredisi: **{len(survey_rows)}** öğrenci
- EAP sunumu katılım listesi: **{len(pres_rows)}** öğrenci

## Sınava girmeyenler ({EXAM_ABSENT})
{absent_md}

## Diğer dersler
{other_md}

## Anket düzeltmesi (Q1 kredisi)
{survey_md}

## Tüm roster (toplam ↓, E en altta)
{all_md}
"""

    full_md_js = full_md.replace("\\", "\\\\").replace("`", "\\`")

    table_rows = []
    row_tones = []
    for i, r in enumerate(display_rows):
        mark = ""
        if r.get("survey_adj"):
            mark += " *"
        if r.get("pres_adj"):
            mark += " †"
        if r["absent"]:
            mark += " ‡"
        table_rows.append(
            f'          [{i + 1}, "{esc(r["name"])}{mark}", "{r["id"]}", {fmt_cell(r["part"])}, {fmt_cell(r["s1"])}, {fmt_cell(r["s2"])}, {fmt_cell(r["s3"])}, {fmt_cell(r["total"])}, {fmt_cell(r["pct100"])}, "{esc(r["folder"])}"],'
        )
        if r["absent"]:
            tone = "neutral"
        elif r["total"] >= 54:
            tone = "success"
        elif r["total"] >= 42:
            tone = "neutral"
        elif r["total"] >= 36:
            tone = "warning"
        else:
            tone = "danger"
        row_tones.append(f'          "{tone}",')

    other_table_rows = []
    for r in other_rows:
        other_table_rows.append(
            f'          ["{esc(r["name"])}", "{r["id"]}", "{esc(r["group"])}", '
            f'{r["part_100"]}, {r["s1_100"]}, {r["s2_100"]}, {r["s3_100"]}, '
            f'{r["total_100"]}, "{r["total"]}/60", "{r["folder"]}"],'
        )

    bands = [
        ("54–60", sum(1 for r in entered if r["total"] >= 54)),
        ("42–53.5", sum(1 for r in entered if 42 <= r["total"] < 54)),
        ("36–41.5", sum(1 for r in entered if 36 <= r["total"] < 42)),
        ("<36", sum(1 for r in entered if r["total"] < 36)),
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

    survey_table_rows = []
    for r in sorted(survey_rows, key=lambda x: -x["total"]):
        survey_table_rows.append(
            f'          ["{esc(r["name"])}", "{r["id"]}", {r["part"]}, {r["s1"]}, {r["s2"]}, {r["s3"]:.1f}, {r["total"]:.1f}],'
        )

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
const PASS36 = {pass36};
const PASS42 = {pass42};
const ROSTER_COUNT = {len(all_rows)};
const ENTERED_COUNT = {len(entered)};
const ABSENT_COUNT = {len(absent)};
const OTHER_COUNT = {len(other_rows)};
const SURVEY_COUNT = {len(survey_rows)};

const FULL_MD = `{full_md_js}`;

export default function TeapFinalGradesCanvas() {{
  const {{ tokens: t }} = useHostTheme();

  return (
    <Stack gap={{20}}>
      <Stack gap={{6}}>
        <H1>TEAP Final Notları</H1>
        <Text tone="secondary">
          {{ROSTER_COUNT}} roster · {{ENTERED_COUNT}} girdi · {{ABSENT_COUNT}} E (girmedi) · {{OTHER_COUNT}} diğer ders
        </Text>
      </Stack>

      <Grid columns={{4}} gap={{12}}>
        <Stat label="Ortalama (girenler)" value={{`${{MEAN.toFixed(1)}}}}/60`}} tone="info" />
        <Stat label="≥36/60 (geçti)" value={{`${{PASS36}}/${{ENTERED_COUNT}}`}} tone="success" />
        <Stat label="E — girmedi" value={{String(ABSENT_COUNT)}} tone="warning" />
        <Stat label="Diğer dersler" value={{String(OTHER_COUNT)}} tone="info" />
      </Grid>

      <Callout tone="info" title="E ve diğer dersler">
        CSV listesinde olup kağıdı olmayanlara sınav sonucu <strong>E</strong> (girmedi) yazıldı.
        Sınava girip bu dersin listesinde olmayanlar <strong>diğer dersler</strong> tablosunda.
        * anket Q1 · † sunum listesi · ‡ girmedi (E)
      </Callout>

      <H2>Diğer dersler (100 üzerinden, orantılı)</H2>
      <Text tone="secondary" size="small">
        Bu dersin Moodle listesinde değiller. Ham sınav 0–60; tabloda ×100/60 ile 100'e çevrildi.
      </Text>
      <Table
        headers={{["Ad (kağıt)", "ID", "Grup", "Kat./100", "I/100", "II/100", "III/100", "Toplam/100", "Ham/60", "Klasör"]}}
        columnAlign={{["left", "left", "left", "right", "right", "right", "right", "right", "right", "left"]}}
        rows={{[
{chr(10).join(other_table_rows) if other_table_rows else '          ["—", "—", "—", "—", "—", "—", "—", "—", "—", "—"],'}
        ]}}
      />

      <H2>Anket düzeltmeli öğrenciler</H2>
      <Table
        headers={{["Ad", "ID", "Kat.", "I", "II", "III", "Toplam"]}}
        columnAlign={{["left", "left", "right", "right", "right", "right", "right"]}}
        rows={{[
{chr(10).join(survey_table_rows)}
        ]}}
      />

      <H2>Tüm roster</H2>
      <Table
        headers={{["#", "Ad Soyad", "ID", "Kat.", "I", "II", "III", "Toplam", "/100", "Klasör"]}}
        columnAlign={{["right", "left", "left", "right", "right", "right", "right", "right", "right", "left"]}}
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
        <Stat label="Katılım" value="{statistics.mean(r['part'] for r in entered):.1f}" />
        <Stat label="Bölüm I" value="{statistics.mean(r['s1'] for r in entered):.1f}" />
        <Stat label="Bölüm II" value="{statistics.mean(r['s2'] for r in entered):.1f}" />
        <Stat label="Bölüm III" value="{statistics.mean(r['s3'] for r in entered):.1f}" />
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
        f"absent={len(absent)}, other={len(other_rows)})"
    )


if __name__ == "__main__":
    main()
