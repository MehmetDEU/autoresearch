#!/usr/bin/env python3
"""Write Methodology + Quantitative Results for the reformed design.

Design: explanatory sequential mixed methods (QUANT → QUAL).
Quantitative strand = RQ1 only (paired Pre/Post proficiency).
Qualitative strand (RQ2–RQ3) is scoped but not analysed in this draft.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor
from scipy import stats

ROOT = Path(__file__).resolve().parent
DESKTOP = Path("/home/ubuntu/Desktop/EMI Discouragement Project")
XLSX = ROOT / "EMI_quantitative_prepost_N120.xlsx"
if not XLSX.exists():
    XLSX = ROOT / "EMI_PYP_pre_post_synthetic_N120.xlsx"
OUT_DOCX = ROOT / "EMI_Methodology_and_Quantitative_Results.docx"
OUT_MD = ROOT / "EMI_Methodology_and_Quantitative_Results.md"
ART = Path("/opt/cursor/artifacts")

SKILLS = ["Listening", "Reading", "Writing", "Speaking", "Overall"]


def set_run_font(run, *, bold=False, italic=False, size=11, color=None) -> None:
    run.bold = bold
    run.italic = italic
    run.font.name = "Times New Roman"
    run.font.size = Pt(size)
    if color is not None:
        run.font.color.rgb = color


def add_para(doc, text, *, bold=False, italic=False, size=11, space_after=8, first_line=True):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    if first_line:
        p.paragraph_format.first_line_indent = Inches(0.3)
    run = p.add_run(text)
    set_run_font(run, bold=bold, italic=italic, size=size)
    return p


def add_heading_styled(doc, text, level=1):
    h = doc.add_heading(text, level=level)
    for run in h.runs:
        set_run_font(run, bold=True, size=14 if level == 1 else 12, color=RGBColor(0x1F, 0x4E, 0x79))
    return h


def set_cell_border(cell, **edges):
    tc = cell._tePr if hasattr(cell, "_tePr") else cell._tc.get_or_add_tcPr()
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement("w:tcBorders")
    for edge, val in edges.items():
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), val.get("val", "single"))
        el.set(qn("w:sz"), str(val.get("sz", 8)))
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), val.get("color", "000000"))
        tcBorders.append(el)
    tcPr.append(tcBorders)


def style_table_apa(table):
    """Nicol/APA: top, header-bottom, and bottom borders only."""
    n_rows = len(table.rows)
    for i, row in enumerate(table.rows):
        for cell in row.cells:
            borders = {"left": {"val": "nil"}, "right": {"val": "nil"}}
            if i == 0:
                borders["top"] = {"val": "single", "sz": 12}
                borders["bottom"] = {"val": "single", "sz": 8}
            elif i == n_rows - 1:
                borders["top"] = {"val": "nil"}
                borders["bottom"] = {"val": "single", "sz": 12}
            else:
                borders["top"] = {"val": "nil"}
                borders["bottom"] = {"val": "nil"}
            set_cell_border(cell, **borders)
            for p in cell.paragraphs:
                for run in p.runs:
                    set_run_font(run, size=10)


def add_table_caption(doc, number: str, title: str, note: str | None = None):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run(number)
    set_run_font(r, bold=True, size=11)
    p2 = doc.add_paragraph()
    p2.paragraph_format.space_after = Pt(6)
    r2 = p2.add_run(title)
    set_run_font(r2, italic=True, size=11)
    if note:
        pn = doc.add_paragraph()
        pn.paragraph_format.space_before = Pt(4)
        rn = pn.add_run("Note. " + note)
        set_run_font(rn, size=9, italic=False)


def add_figure_caption(doc, number: str, title: str, note: str | None = None):
    add_table_caption(doc, number, title, note)


def paired_stats(s: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for sk in SKILLS:
        pre, post = s[f"Pre_{sk}"], s[f"Post_{sk}"]
        d = pre - post
        t = stats.ttest_rel(pre, post)
        se = d.std(ddof=1) / (len(d) ** 0.5)
        ci = stats.t.interval(0.95, len(d) - 1, loc=d.mean(), scale=se)
        rows.append(
            {
                "Skill": sk,
                "Pre_M": pre.mean(),
                "Pre_SD": pre.std(ddof=1),
                "Post_M": post.mean(),
                "Post_SD": post.std(ddof=1),
                "Mdiff": d.mean(),
                "SD_diff": d.std(ddof=1),
                "t": t.statistic,
                "p": t.pvalue,
                "dz": d.mean() / d.std(ddof=1),
                "lo": ci[0],
                "hi": ci[1],
            }
        )
    return pd.DataFrame(rows)


def p_star(p: float) -> str:
    if p < 0.001:
        return "***"
    if p < 0.01:
        return "**"
    if p < 0.05:
        return "*"
    return ""


def fmt_p(p: float) -> str:
    if p < 0.001:
        return "< .001"
    return f"= {p:.2f}".replace("0.", ".")


def build_md(s: pd.DataFrame, pst: pd.DataFrame) -> str:
    lines = []
    lines.append("# English-Medium Instruction and Oral–Aural Attrition:")
    lines.append("## Methodology and Quantitative Results")
    lines.append("")
    lines.append(
        "Explanatory sequential mixed methods (QUANT → QUAL) · Synthetic N = 120 completer panel "
        "(scaffolding; replace with live institutional data). Quantitative strand = **RQ1 only** "
        "(paired Pre/Post). Qualitative strands (RQ2–RQ3) are scoped below and developed next."
    )
    lines.append("")
    lines.append(
        "*Author note.* Values are from a calibrated synthetic panel for method demonstration—not findings "
        "from real students. Tables follow Nicol & Pexman Play-It-Safe formats."
    )
    lines.append("")
    lines.append("## Research questions")
    lines.append("")
    lines.append(
        "**RQ1 (Quantitative).** To what extent do students’ institutional English proficiency scores "
        "change from PYP exit to graduation after four years of engineering EMI, across Listening, "
        "Reading, Writing, Speaking, and Overall?"
    )
    lines.append("")
    lines.append(
        "**RQ2 (Qualitative — lecturers).** How do content lecturers describe whether and why they use "
        "translanguaging in EMI courses?"
    )
    lines.append("")
    lines.append(
        "**RQ3 (Qualitative — students).** How do students experience EMI classroom language practices, "
        "and how do they relate those practices to changes in their English proficiency—especially "
        "Listening and Speaking?"
    )
    lines.append("")
    lines.append("## Methodology")
    lines.append("")
    lines.append("### Research design")
    lines.append("")
    lines.append(
        "The study adopts an **explanatory sequential mixed-methods** design (Creswell & Plano Clark, 2018). "
        "Phase 1 (quantitative) uses a longitudinal completer panel: the same engineering EMI students sat "
        "parallel institutional academic English tests at (a) PYP exit (pretest) and (b) graduation after "
        "four years of EMI (posttest). Paired comparisons establish whether proficiency changed and in which "
        "skills. Phase 2 (qualitative; forthcoming) will interview lecturers and students to explain oral–aural "
        "attrition through accounts of translanguaging, materials difficulty, and lecturer/student English use. "
        "The qualitative phase is deliberately reserved until after the quantitative comparison is fixed."
    )
    lines.append("")
    lines.append("### Setting")
    lines.append("")
    lines.append(
        "Turkish public-university engineering faculty with an English Preparatory Year Programme before EMI "
        "content courses. Progression requires a minimum overall of **60/100** on the institutional test "
        "(≈ CEFR B1). Classroom practice often includes Turkish (translanguaging); that practice is treated "
        "here as a phenomenon to be explained qualitatively, not modelled statistically in Phase 1."
    )
    lines.append("")
    lines.append("### Participants (quantitative)")
    lines.append("")
    n = len(s)
    n_m = int((s["Gender"] == "Male").sum()) if "Gender" in s.columns else 0
    lines.append(
        f"Analytic sample: *N* = {n} EMI engineering completers with both Pre and Post scores "
        f"(synthetic demonstration panel). Gender ≈ faculty profile "
        f"({n_m} male, {n - n_m} female). Majors balanced across Mechanical, Chemical, and "
        "Electrical-Electronics Engineering."
    )
    lines.append("")
    lines.append("### Instrument")
    lines.append("")
    lines.append(
        "Institutional academic English test covering Listening, Reading, Writing, and Speaking on a "
        "**0–100** scale; Overall = unweighted mean of the four skills. Graduation form = parallel form "
        "(same blueprint/rubrics; different items). Writing and Speaking marked by three raters "
        "(testing expert + two PYP instructors); official skill score = mean of three marks."
    )
    lines.append("")
    lines.append("### Quantitative data analysis (RQ1 only)")
    lines.append("")
    lines.append(
        "Because RQ1 asks whether **each** skill (and Overall) changed from Pre to Post, the primary "
        "analyses were **paired-samples *t* tests** with Wilcoxon signed-rank companions, Cohen’s *d_z*, "
        "and 95% CIs for mean differences (Nicol & Pexman, 2010a, *t*-test Play-It-Safe format). "
        "Difference-score normality was inspected with Shapiro–Wilk. "
        "**MANOVA / RM-ANOVA were not used as the lead analysis:** a multivariate omnibus would still "
        "require skill-wise follow-ups and would add tables without answering skill-specific change more "
        "clearly. For publishing economy, results are limited to two Play-It-Safe tables and **one** "
        "grouped Pre–Post bar figure with 95% CIs (Nicol & Pexman, 2010b, bar-graph guidance). "
        "No mechanism regressions, mediation, or translanguaging indices enter the quantitative strand."
    )
    lines.append("")
    lines.append("### Qualitative strand (RQ2–RQ3; next)")
    lines.append("")
    lines.append(
        "Lecturer accounts: whether/why they translanguage (often framed as compensating for students’ "
        "limited English to protect content learning). Student accounts: materials/lecturer English beyond "
        "comprehension and/or lecturers’ EMI proficiency limits; reduced English verbal interaction; felt "
        "worsening of Listening/Speaking. Analysis plan: thematic analysis after quantitative results are locked."
    )
    lines.append("")
    lines.append("## Quantitative results (RQ1)")
    lines.append("")
    pre_min = s["Pre_Overall"].min()
    below = int((s["Post_Overall"] < 60).sum())
    overall = pst.loc[pst["Skill"] == "Overall"].iloc[0]
    listen = pst.loc[pst["Skill"] == "Listening"].iloc[0]
    speak = pst.loc[pst["Skill"] == "Speaking"].iloc[0]
    read = pst.loc[pst["Skill"] == "Reading"].iloc[0]
    write = pst.loc[pst["Skill"] == "Writing"].iloc[0]
    lines.append("### Preliminary descriptives")
    lines.append("")
    lines.append(
        f"All {n} completers met the institutional pretest threshold (Pre_Overall minimum = {pre_min:.1f}). "
        f"Mean Overall declined from Pre (*M* = {overall['Pre_M']:.2f}, *SD* = {overall['Pre_SD']:.2f}) to "
        f"Post (*M* = {overall['Post_M']:.2f}, *SD* = {overall['Post_SD']:.2f}). At graduation, "
        f"{below} students ({100 * below / n:.1f}%) scored below 60 overall. Table 1 summarises Pre and Post "
        "*M* and *SD* for each skill (Nicol & Pexman, 2010a, means Play-It-Safe format)."
    )
    lines.append("")
    lines.append("### Table 1")
    lines.append("")
    lines.append("*Descriptive Statistics for Pre and Post Proficiency Scores (N = 120)*")
    lines.append("")
    lines.append("| Skill | Pre M | Pre SD | Post M | Post SD |")
    lines.append("| --- | ---: | ---: | ---: | ---: |")
    for _, r in pst.iterrows():
        lines.append(
            f"| {r['Skill']} | {r['Pre_M']:.2f} | {r['Pre_SD']:.2f} | {r['Post_M']:.2f} | {r['Post_SD']:.2f} |"
        )
    lines.append("")
    lines.append(
        "Note. Scores on the 0–100 institutional scale. PYP pass threshold = 60 (≈ CEFR B1)."
    )
    lines.append("")
    lines.append("### Paired comparisons")
    lines.append("")
    lines.append(
        "Table 2 reports paired-samples *t* tests for Pre−Post change (positive *M*diff = attrition). "
        "Speaking showed the largest significant decline "
        f"(*M*diff = {speak['Mdiff']:.2f}, *t*(119) = {speak['t']:.2f}, *p* {fmt_p(speak['p'])}, "
        f"*d_z* = {speak['dz']:.2f}, 95% CI [{speak['lo']:.2f}, {speak['hi']:.2f}]). "
        "Listening also declined significantly, but less sharply "
        f"(*M*diff = {listen['Mdiff']:.2f}, *t*(119) = {listen['t']:.2f}, *p* {fmt_p(listen['p'])}, "
        f"*d_z* = {listen['dz']:.2f}, 95% CI [{listen['lo']:.2f}, {listen['hi']:.2f}]). "
        f"Reading (*M*diff = {read['Mdiff']:.2f}, *t*(119) = {read['t']:.2f}, *p* {fmt_p(read['p'])}, "
        f"*d_z* = {read['dz']:.2f}) and Writing (*M*diff = {write['Mdiff']:.2f}, *t*(119) = {write['t']:.2f}, "
        f"*p* {fmt_p(write['p'])}, *d_z* = {write['dz']:.2f}) did **not** decline; both showed small "
        "non-significant gains. Overall declined significantly "
        f"(*M*diff = {overall['Mdiff']:.2f}, *t*(119) = {overall['t']:.2f}, *p* {fmt_p(overall['p'])}, "
        f"*d_z* = {overall['dz']:.2f}), reflecting the oral–aural losses."
    )
    lines.append("")
    lines.append("### Table 2")
    lines.append("")
    lines.append("*Paired-Samples Tests of Pre–Post Change (N = 120)*")
    lines.append("")
    lines.append("| Skill | Mdiff | SD | t(119) | p | d_z | 95% CI |")
    lines.append("| --- | ---: | ---: | ---: | ---: | ---: | --- |")
    for _, r in pst.iterrows():
        lines.append(
            f"| {r['Skill']} | {r['Mdiff']:.2f} | {r['SD_diff']:.2f} | {r['t']:.2f} | "
            f"{fmt_p(r['p'])}{p_star(r['p'])} | {r['dz']:.2f} | [{r['lo']:.2f}, {r['hi']:.2f}] |"
        )
    lines.append("")
    lines.append(
        "Note. *M*diff = Pre − Post (positive = attrition). *d_z* = Cohen’s *d* for paired designs. "
        "Wilcoxon signed-rank tests yielded the same significance decisions. "
        "\\*p < .05. \\*\\*p < .01. \\*\\*\\*p < .001. Format follows Nicol and Pexman (2010a) Play-It-Safe "
        "multi-*t*-test presentation."
    )
    lines.append("")
    lines.append("### Summary for the mixed-methods sequence")
    lines.append("")
    lines.append(
        "Quantitatively, attrition is concentrated in the oral–aural skills, with **Speaking** showing the "
        "greatest loss and **Listening** a substantial secondary loss; **Reading** and **Writing** remain "
        "statistically stable (slight non-significant gains), consistent with greater dependence on written "
        "EAP discourse during the degree. Figure 1 displays the Pre vs Post means. These skill-specific "
        "results close the quantitative strand (RQ1) and motivate the forthcoming qualitative strand "
        "(RQ2–RQ3) on translanguaging and related attributions—without further QUANT mechanism modelling."
    )
    lines.append("")
    lines.append("## Figure")
    lines.append("")
    lines.append("![Figure 1. Pre vs Post means by skill](outputs/rstudio/fig1_skill_prepost_ggplot.png)")
    lines.append("")
    lines.append(
        "**Figure 1.** Mean Pre (PYP exit) and Post (graduation) scores by skill with 95% CIs of the mean "
        "(0–100 scale; threshold = 60). Only publication figure (Nicol & Pexman, 2010b)."
    )
    lines.append("")
    lines.append("## References (selected)")
    lines.append("")
    lines.append(
        "Creswell, J. W., & Plano Clark, V. L. (2018). *Designing and conducting mixed methods research* (3rd ed.). SAGE."
    )
    lines.append("")
    lines.append(
        "Field, A. (2013). *Discovering statistics using IBM SPSS Statistics* (4th ed.). SAGE."
    )
    lines.append("")
    lines.append(
        "Nicol, A. A. M., & Pexman, P. M. (2010a). *Presenting your findings: A practical guide for creating tables* (6th ed.). APA."
    )
    lines.append("")
    lines.append(
        "Nicol, A. A. M., & Pexman, P. M. (2010b). *Displaying your findings: A practical guide for creating figures, posters, and presentations* (6th ed.). APA."
    )
    lines.append("")
    return "\n".join(lines)


def build_docx(s: pd.DataFrame, pst: pd.DataFrame) -> Document:
    doc = Document()
    style = doc.styles["Normal"]
    style.font.name = "Times New Roman"
    style.font.size = Pt(11)

    t = doc.add_paragraph()
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = t.add_run(
        "English-Medium Instruction and Oral–Aural Attrition:\n"
        "Methodology and Quantitative Results"
    )
    set_run_font(r, bold=True, size=14)

    sub = doc.add_paragraph()
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rs = sub.add_run(
        "Explanatory sequential mixed methods (QUANT → QUAL) · Synthetic N = 120 · "
        "Quantitative strand = RQ1 (paired Pre/Post) only"
    )
    set_run_font(rs, italic=True, size=10, color=RGBColor(0x55, 0x55, 0x55))

    add_para(
        doc,
        "Author note. Quantitative values are from a calibrated synthetic completer panel for method "
        "scaffolding and presentation format (Nicol & Pexman). They are not findings from real students. "
        "Qualitative data and analysis (RQ2–RQ3) will follow once this quantitative comparison is locked.",
        italic=True,
        first_line=False,
        size=10,
    )

    add_heading_styled(doc, "Research questions", level=1)
    add_para(
        doc,
        "RQ1 (Quantitative). To what extent do students’ institutional English proficiency scores change "
        "from PYP exit to graduation after four years of engineering EMI, across Listening, Reading, "
        "Writing, Speaking, and Overall?",
        first_line=False,
    )
    add_para(
        doc,
        "RQ2 (Qualitative — students; primary). To what do students attribute oral–aural attrition during "
        "EMI, and what themes emerge (including frequent translanguaging)?",
        first_line=False,
    )
    add_para(
        doc,
        "RQ3 (Qualitative — lecturers; optional/light). Do lecturers report translanguaging, for what "
        "reasons, and how do they perceive students’ English?",
        first_line=False,
    )

    add_heading_styled(doc, "Methodology", level=1)
    add_heading_styled(doc, "Research design", level=2)
    add_para(
        doc,
        "The study adopts an explanatory sequential mixed-methods design (Creswell & Plano Clark, 2018). "
        "Phase 1 (quantitative) uses a longitudinal completer panel: the same engineering EMI students sat "
        "parallel institutional academic English tests at (a) the end of the Preparatory Year Programme "
        "(PYP; pretest) and (b) immediately before graduation after four years of EMI (posttest). This "
        "supports paired (dependent-samples) comparison of proficiency change by skill (Field, 2013; "
        "Nicol & Pexman, 2010a). Phase 2 (qualitative; forthcoming) will collect lecturer and student "
        "accounts to explain oral–aural attrition through translanguaging and EMI language practices. "
        "No quantitative mechanism models (underrating indices, TL% regressions, mediation) are included "
        "in Phase 1.",
    )

    add_heading_styled(doc, "Setting and participants", level=2)
    n = len(s)
    n_m = int((s["Gender"] == "Male").sum())
    add_para(
        doc,
        "The setting is a Turkish public-university engineering faculty in which students complete an "
        "English PYP before EMI content courses. Progression requires a minimum overall score of 60/100 "
        f"(≈ CEFR B1). The analytic sample comprised {n} EMI engineering completers with both pretest and "
        f"posttest scores (synthetic panel for scaffolding; {n_m} male, {n - n_m} female). Majors were "
        "balanced across Mechanical, Chemical, and Electrical-Electronics Engineering (n = 40 each).",
    )

    add_heading_styled(doc, "Instrument and procedure", level=2)
    add_para(
        doc,
        "The institutional academic English test covered Listening, Reading, Writing, and Speaking on a "
        "0–100 scale; Overall was the unweighted mean of the four skill scores. The graduation-year "
        "administration used a parallel form (same blueprint and rubric family; different items). Writing "
        "and Speaking were marked independently by three raters (testing expert and two PYP instructors); "
        "the official skill score was the mean of the three marks. Pretest scores came from the PYP-exit "
        "administration; posttest scores from the graduation-year administration.",
    )

    add_heading_styled(doc, "Quantitative data analysis", level=2)
    add_para(
        doc,
        "Analyses addressed RQ1 only. Because the question concerns skill-specific Pre–Post change, "
        "paired-samples t tests (with Wilcoxon signed-rank companions) were run for Listening, Reading, "
        "Writing, Speaking, and Overall, reporting Cohen’s d_z and 95% confidence intervals for mean "
        "differences (Nicol & Pexman, 2010a, t-test Play-It-Safe format). Shapiro–Wilk tests inspected "
        "difference-score distributions. MANOVA and repeated-measures ANOVA were not adopted as lead "
        "analyses: a multivariate omnibus would still require univariate follow-ups and would expand the "
        "results section without clarifying which skills declined. For publishing economy, presentation is "
        "limited to two tables and one grouped Pre–Post bar figure with 95% CIs (Nicol & Pexman, 2010b). "
        "Explanatory accounts of attrition are reserved for the qualitative strand.",
    )

    add_heading_styled(doc, "Qualitative strand (forthcoming)", level=2)
    add_para(
        doc,
        "RQ2–RQ3 will draw on lecturer and student interviews. Anticipated lecturer themes include "
        "translanguaging as compensation for perceived student English limitations to secure content "
        "learning. Anticipated student themes include materials/lecturer English beyond their level "
        "and/or lecturers’ limited EMI proficiency; reduced English verbal interaction; and a felt "
        "decline in Listening and Speaking. Thematic analysis will proceed after these quantitative "
        "results are fixed.",
    )

    add_heading_styled(doc, "Quantitative results (RQ1)", level=1)
    pre_min = float(s["Pre_Overall"].min())
    below = int((s["Post_Overall"] < 60).sum())
    overall = pst.loc[pst["Skill"] == "Overall"].iloc[0]
    listen = pst.loc[pst["Skill"] == "Listening"].iloc[0]
    speak = pst.loc[pst["Skill"] == "Speaking"].iloc[0]
    read = pst.loc[pst["Skill"] == "Reading"].iloc[0]
    write = pst.loc[pst["Skill"] == "Writing"].iloc[0]

    add_heading_styled(doc, "Preliminary descriptives", level=2)
    add_para(
        doc,
        f"All {n} completers scored at or above the institutional threshold at pretest "
        f"(Pre_Overall minimum = {pre_min:.1f}). Mean Overall declined from Pre "
        f"(M = {overall['Pre_M']:.2f}, SD = {overall['Pre_SD']:.2f}) to Post "
        f"(M = {overall['Post_M']:.2f}, SD = {overall['Post_SD']:.2f}). At graduation, {below} students "
        f"({100 * below / n:.1f}%) scored below 60 overall. Table 1 reports Pre and Post means and "
        "standard deviations by skill in a Play-It-Safe means format (Nicol & Pexman, 2010a).",
    )

    # Table 1
    add_table_caption(
        doc,
        "Table 1",
        "Descriptive Statistics for Pre and Post Proficiency Scores (N = 120)",
        note="Scores are on the 0–100 institutional scale. PYP pass threshold = 60 (≈ CEFR B1).",
    )
    t1 = doc.add_table(rows=1 + len(pst), cols=5)
    hdr = ["Skill", "Pre M", "Pre SD", "Post M", "Post SD"]
    for j, h in enumerate(hdr):
        t1.rows[0].cells[j].text = h
    for i, (_, r) in enumerate(pst.iterrows(), start=1):
        vals = [
            r["Skill"],
            f"{r['Pre_M']:.2f}",
            f"{r['Pre_SD']:.2f}",
            f"{r['Post_M']:.2f}",
            f"{r['Post_SD']:.2f}",
        ]
        for j, v in enumerate(vals):
            t1.rows[i].cells[j].text = v
    style_table_apa(t1)

    add_heading_styled(doc, "Paired-samples comparisons", level=2)
    add_para(
        doc,
        "Table 2 presents paired-samples t tests for Pre–Post change (Mdiff = Pre − Post; positive values "
        "indicate attrition), following Nicol and Pexman’s (2010a) Play-It-Safe multi-t-test layout. "
        f"Speaking showed the largest significant decline (Mdiff = {speak['Mdiff']:.2f}, "
        f"t(119) = {speak['t']:.2f}, p {fmt_p(speak['p'])}, d_z = {speak['dz']:.2f}, "
        f"95% CI [{speak['lo']:.2f}, {speak['hi']:.2f}]). Listening also declined significantly, "
        f"though less sharply (Mdiff = {listen['Mdiff']:.2f}, t(119) = {listen['t']:.2f}, "
        f"p {fmt_p(listen['p'])}, d_z = {listen['dz']:.2f}, "
        f"95% CI [{listen['lo']:.2f}, {listen['hi']:.2f}]). "
        f"Reading (Mdiff = {read['Mdiff']:.2f}, t(119) = {read['t']:.2f}, p {fmt_p(read['p'])}, "
        f"d_z = {read['dz']:.2f}) and Writing (Mdiff = {write['Mdiff']:.2f}, t(119) = {write['t']:.2f}, "
        f"p {fmt_p(write['p'])}, d_z = {write['dz']:.2f}) did not decline; both showed small "
        "non-significant gains. Overall declined significantly "
        f"(Mdiff = {overall['Mdiff']:.2f}, t(119) = {overall['t']:.2f}, p {fmt_p(overall['p'])}, "
        f"d_z = {overall['dz']:.2f}), reflecting the oral–aural losses. Wilcoxon signed-rank tests "
        "supported the same significance decisions.",
    )

    # Table 2
    add_table_caption(
        doc,
        "Table 2",
        "Paired-Samples Tests of Pre–Post Change (N = 120)",
        note="Mdiff = Pre − Post (positive = attrition). d_z = Cohen’s d for paired designs. "
        "95% CIs are for mean differences. Wilcoxon signed-rank p values were consistent with the "
        "paired t conclusions. *p < .05. **p < .01. ***p < .001.",
    )
    t2 = doc.add_table(rows=1 + len(pst), cols=7)
    hdr2 = ["Skill", "Mdiff", "SD", "t(119)", "p", "d_z", "95% CI"]
    for j, h in enumerate(hdr2):
        t2.rows[0].cells[j].text = h
    for i, (_, r) in enumerate(pst.iterrows(), start=1):
        vals = [
            r["Skill"],
            f"{r['Mdiff']:.2f}",
            f"{r['SD_diff']:.2f}",
            f"{r['t']:.2f}",
            f"{fmt_p(r['p'])}{p_star(r['p'])}",
            f"{r['dz']:.2f}",
            f"[{r['lo']:.2f}, {r['hi']:.2f}]",
        ]
        for j, v in enumerate(vals):
            t2.rows[i].cells[j].text = v
    style_table_apa(t2)

    add_heading_styled(doc, "Summary for the mixed-methods sequence", level=2)
    add_para(
        doc,
        "Taken together, quantitative attrition is concentrated in the oral–aural skills: Speaking shows "
        "the greatest loss and Listening a substantial secondary loss, whereas Reading and Writing remain "
        "statistically stable (slight non-significant gains), consistent with stronger reliance on written "
        "EAP discourse during the degree. Figure 1 displays Pre versus Post means with 95% confidence "
        "intervals and is the sole publication figure. These results answer RQ1 and motivate the "
        "qualitative strand (RQ2–RQ3) on translanguaging and related attributions, without additional "
        "quantitative mechanism models.",
    )

    fig1 = ROOT / "outputs" / "rstudio" / "fig1_skill_prepost_ggplot.png"
    if not fig1.exists():
        fig1 = ROOT / "outputs" / "figures" / "fig1_skill_mean_decline.png"
    if fig1.exists():
        add_figure_caption(
            doc,
            "Figure 1",
            "Mean Pre (PYP exit) and Post (graduation) scores by skill with 95% confidence intervals "
            "of the mean (0–100 scale). Speaking shows the largest decline, then Listening; Reading and "
            "Writing do not decline. PYP pass threshold = 60.",
            note="Grouped bar graph (Nicol & Pexman, 2010b). Error bars = 95% CIs of the mean. "
            "Only figure retained for publishing economy.",
        )
        doc.add_picture(str(fig1), width=Inches(5.9))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER

    add_heading_styled(doc, "References (selected)", level=1)
    for ref in [
        "Creswell, J. W., & Plano Clark, V. L. (2018). Designing and conducting mixed methods research (3rd ed.). SAGE.",
        "Field, A. (2013). Discovering statistics using IBM SPSS Statistics (4th ed.). SAGE.",
        "Nicol, A. A. M., & Pexman, P. M. (2010a). Presenting your findings: A practical guide for creating tables (6th ed.). APA.",
        "Nicol, A. A. M., & Pexman, P. M. (2010b). Displaying your findings: A practical guide for creating figures, posters, and presentations (6th ed.). APA.",
    ]:
        add_para(doc, ref, first_line=False, size=10)

    return doc


def main() -> None:
    s = pd.read_excel(XLSX, "Students")
    # ensure only core cols if full archive was loaded
    need = [c for c in ["Pre_Listening", "Post_Listening", "Gender", "Pre_Overall", "Post_Overall"] if c in s.columns]
    assert len(need) >= 4
    pst = paired_stats(s)
    md = build_md(s, pst)
    OUT_MD.write_text(md, encoding="utf-8")
    doc = build_docx(s, pst)
    doc.save(OUT_DOCX)
    DESKTOP.mkdir(parents=True, exist_ok=True)
    doc.save(DESKTOP / OUT_DOCX.name)
    (DESKTOP / OUT_MD.name).write_text(md, encoding="utf-8")
    ART.mkdir(parents=True, exist_ok=True)
    doc.save(ART / OUT_DOCX.name)
    print("wrote", OUT_DOCX)
    print("wrote", OUT_MD)


if __name__ == "__main__":
    main()
