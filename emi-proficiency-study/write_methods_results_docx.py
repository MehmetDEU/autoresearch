#!/usr/bin/env python3
"""Methodology + Quantitative Results (Word), following Nicol & Pexman table/figure
conventions and Altay-style EMI methodology structure.

Sources consulted:
- Nicol & Pexman, Presenting Your Findings (APA) — Play-It-Safe tables for means,
  paired t tests, correlations, and multiple regression
- Nicol & Pexman, Displaying Your Findings (APA) — lean figures with CIs, clear axes/units
- Prior Altay EMI / Pygmalion manuscripts (mixed-methods methodology scaffold)
- Drive methods pack (APA 7, Field, Dörnyei, Creswell)
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor
from scipy import stats

ROOT = Path(__file__).resolve().parent
DESKTOP = Path("/home/ubuntu/Desktop/EMI Discouragement Project")
ART = Path("/opt/cursor/artifacts")
OUT_NAME = "EMI_Methodology_and_Quantitative_Results.docx"
XLSX = ROOT / "EMI_PYP_pre_post_synthetic_N120.xlsx"


def load_live():
    students = pd.read_excel(XLSX, "Students")
    paired = pd.read_excel(XLSX, "Paired_pre_post").set_index("skill")
    golem = pd.read_excel(XLSX, "Golem_correlations").set_index("predictor")
    desc = pd.read_excel(XLSX, "Descriptives").set_index("variable")
    rel = pd.read_excel(XLSX, "Reliability").set_index("scale")
    icc = pd.read_excel(XLSX, "ICC_raters").set_index("facet")
    ielts = pd.read_excel(XLSX, "Concurrent_IELTS").set_index("institutional")
    reg = pd.read_excel(XLSX, "Regression_models")
    med = pd.read_excel(XLSX, "Mediation").set_index("quantity")
    return {
        "students": students,
        "paired": paired,
        "golem": golem,
        "desc": desc,
        "rel": rel,
        "icc": icc,
        "ielts": ielts,
        "reg": reg,
        "med": med,
    }


def fmt(x, nd=2):
    return f"{float(x):.{nd}f}"


def apa_p(p):
    p = float(p)
    if p < 0.001:
        return "<.001"
    return f"{p:.3f}".replace("0.", ".")


def stars(p):
    p = float(p)
    if p < 0.001:
        return "***"
    if p < 0.01:
        return "**"
    if p < 0.05:
        return "*"
    return ""


def set_run_font(run, *, bold=False, italic=False, size=11, color=None):
    run.bold = bold
    run.italic = italic
    run.font.name = "Times New Roman"
    run._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    run.font.size = Pt(size)
    if color is not None:
        run.font.color.rgb = color


def add_para(doc, text, *, bold=False, italic=False, size=11, space_after=8, first_indent=True, align="justify"):
    p = doc.add_paragraph()
    if align == "justify":
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    elif align == "center":
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    elif align == "left":
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf = p.paragraph_format
    pf.space_after = Pt(space_after)
    pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    if first_indent:
        pf.first_line_indent = Inches(0.5)
    run = p.add_run(text)
    set_run_font(run, bold=bold, italic=italic, size=size)
    return p


def add_heading_styled(doc, text, level=1):
    h = doc.add_heading(text, level=level)
    for run in h.runs:
        set_run_font(run, bold=True, size=14 if level == 1 else 12)
        run.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)
    h.paragraph_format.space_before = Pt(14)
    h.paragraph_format.space_after = Pt(8)
    return h


def add_mixed_para(doc, parts, *, first_indent=True, space_after=8):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf = p.paragraph_format
    pf.space_after = Pt(space_after)
    pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    if first_indent:
        pf.first_line_indent = Inches(0.5)
    for text, bold, italic in parts:
        run = p.add_run(text)
        set_run_font(run, bold=bold, italic=italic, size=11)
    return p


def _set_cell_border(cell, **sides):
    """APA-style borders: top/bottom/insideH only; no verticals."""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = OxmlElement("w:tcBorders")
    for edge in ("top", "left", "bottom", "right"):
        element = OxmlElement(f"w:{edge}")
        spec = sides.get(edge, {"val": "nil"})
        element.set(qn("w:val"), spec.get("val", "nil"))
        if spec.get("val") != "nil":
            element.set(qn("w:sz"), str(spec.get("sz", 8)))
            element.set(qn("w:space"), "0")
            element.set(qn("w:color"), spec.get("color", "000000"))
        tcBorders.append(element)
    tcPr.append(tcBorders)


def apply_apa_table_borders(table):
    thin = {"val": "single", "sz": 8, "color": "000000"}
    thick = {"val": "single", "sz": 12, "color": "000000"}
    n = len(table.rows)
    for r_i, row in enumerate(table.rows):
        for cell in row.cells:
            top = thick if r_i == 0 else (thin if r_i == 1 else {"val": "nil"})
            bottom = thick if r_i == n - 1 else (thin if r_i == 0 else {"val": "nil"})
            _set_cell_border(cell, top=top, bottom=bottom, left={"val": "nil"}, right={"val": "nil"})


def fill_header_row(row, labels):
    for i, label in enumerate(labels):
        row.cells[i].text = label
        for p in row.cells[i].paragraphs:
            for run in p.runs:
                set_run_font(run, bold=True, size=9)


def style_body_cells(table):
    for r_i, row in enumerate(table.rows):
        for c_i, cell in enumerate(row.cells):
            for p in cell.paragraphs:
                p.paragraph_format.space_after = Pt(1)
                p.paragraph_format.space_before = Pt(1)
                p.paragraph_format.line_spacing = 1.0
                if c_i == 0:
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                else:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for run in p.runs:
                    set_run_font(run, bold=(r_i == 0), size=9)


def add_table_number_title(doc, number: str, title: str):
    """Nicol/APA: Table number (bold) then italic title on next line."""
    p1 = doc.add_paragraph()
    p1.paragraph_format.space_before = Pt(12)
    p1.paragraph_format.space_after = Pt(0)
    p1.paragraph_format.first_line_indent = Inches(0)
    r = p1.add_run(number)
    set_run_font(r, bold=True, size=11)
    p2 = doc.add_paragraph()
    p2.paragraph_format.space_before = Pt(0)
    p2.paragraph_format.space_after = Pt(6)
    p2.paragraph_format.first_line_indent = Inches(0)
    r = p2.add_run(title)
    set_run_font(r, italic=True, size=11)
    return p1, p2


def add_table_note(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.first_line_indent = Inches(0)
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(10)
    # General note starts with italic Note.
    run = p.add_run("Note. ")
    set_run_font(run, italic=True, size=9)
    run = p.add_run(text)
    set_run_font(run, italic=False, size=9)
    return p


def add_figure_caption(doc, number: str, title: str, note: str | None = None):
    """Nicol/APA Displaying Your Findings: Figure number + italic title; optional note."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.first_line_indent = Inches(0)
    r = p.add_run(f"{number}. ")
    set_run_font(r, bold=True, size=10)
    r = p.add_run(title)
    set_run_font(r, italic=True, size=10)
    if note:
        add_table_note(doc, note)
    return p


def model_r2(s: pd.DataFrame, formula_terms_present: bool = True) -> dict:
    """Refit OLS models to recover R² for Nicol regression table notes."""
    import statsmodels.formula.api as smf

    m1 = smf.ols(
        "Decline_Speaking ~ EAP_mean + Pre_Speaking + C(Major) + C(Gender)", data=s
    ).fit()
    m2 = smf.ols(
        "Decline_Speaking ~ Underrating_Gap + Pre_Speaking + C(Major) + C(Gender)", data=s
    ).fit()
    m3 = smf.ols(
        "Decline_Speaking ~ Underrating_Gap + TL_percent + EAP_mean + Pre_Speaking + C(Major) + C(Gender)",
        data=s,
    ).fit()
    return {"M1_EAP_only": m1, "M2_Underrating": m2, "M3_Full": m3}


def beta_from_b(b: float, x: pd.Series, y: pd.Series) -> float:
    return float(b) * (float(x.std(ddof=1)) / float(y.std(ddof=1)))


def build() -> Path:
    live = load_live()
    s = live["students"]
    paired = live["paired"]
    golem = live["golem"]
    desc = live["desc"]
    rel = live["rel"]
    icc = live["icc"]
    ielts = live["ielts"]
    reg = live["reg"]
    med = live["med"]
    models = model_r2(s)

    n = len(s)
    n_male = int((s["Gender"] == "Male").sum())
    n_female = n - n_male
    age_m = float(s["Age_at_post_graduation"].mean())
    age_sd = float(s["Age_at_post_graduation"].std(ddof=1))

    doc = Document()
    section = doc.sections[0]
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)

    # Title
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = title.add_run(
        "English-Medium Instruction, Lecturer Underrating, and Four-Year Proficiency Change:\n"
        "Methodology and Quantitative Results"
    )
    set_run_font(r, bold=True, size=14)
    title.paragraph_format.space_after = Pt(6)

    sub = doc.add_paragraph()
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = sub.add_run(
        "Draft sections for manuscript development · Synthetic N = 120 panel "
        "(instrument testing / paper scaffolding; replace with live institutional data before submission)"
    )
    set_run_font(r, italic=True, size=10, color=RGBColor(0x66, 0x66, 0x66))
    sub.paragraph_format.space_after = Pt(10)

    note = doc.add_paragraph()
    note.paragraph_format.first_line_indent = Inches(0)
    r = note.add_run("Author note. ")
    set_run_font(r, bold=True, italic=True, size=10)
    r = note.add_run(
        "Quantitative values below are from a calibrated synthetic completer panel designed to match "
        "institutional testing policy and the planned Golem-mechanism analysis. They illustrate the "
        "intended statistical pathway and presentation format (Nicol & Pexman Play-It-Safe tables; "
        "lean figures). They are not findings from real students. Presentation follows Adelheid A. M. "
        "Nicol and Penny M. Pexman (Presenting Your Findings; Displaying Your Findings) and APA Style "
        "table/figure conventions."
    )
    set_run_font(r, italic=True, size=10)
    note.paragraph_format.space_after = Pt(14)

    # ========================= METHODOLOGY =========================
    add_heading_styled(doc, "Methodology", level=1)

    add_heading_styled(doc, "Research design", level=2)
    add_para(
        doc,
        "The study used a longitudinal completer-panel design with two parallel administrations of an "
        "institutional academic English proficiency test: (a) at the end of the Preparatory Year Programme "
        "(PYP; pretest) and (b) immediately before graduation after four years of English-medium instruction "
        "(EMI) in an engineering major (posttest). The same students sat both forms. The design therefore "
        "supports a paired (dependent-samples) comparison of proficiency change (Field, 2013; Nicol & Pexman, "
        "2010a), supplemented by questionnaire and lecturer-estimate measures collected to evaluate whether "
        "any decline is consistent with a Golem-type expectancy–treatment mechanism (Babad, Inbar, & Rosenthal, "
        "1982) rather than with uniform skill attrition alone.",
    )
    add_para(
        doc,
        "Because a Golem interpretation requires evidence that a low expectation is inaccurate and is enacted "
        "through differential treatment that suppresses demonstrated performance, the quantitative strand "
        "measured four layers: (1) actual proficiency at PYP exit; (2) content lecturers’ estimates of students’ "
        "English (inaccuracy); (3) exposure to Turkish in content courses (treatment / translanguaging); and "
        "(4) students’ willingness to communicate in English and English self-efficacy (internalization). "
        "Lecturer English-for-academic-purposes (EAP) limitation was measured as a competing explanation for "
        "translanguaging and was not labelled as a Golem indicator. The overall architecture mirrors the "
        "mixed-methods expectancy logic used in related EMI expectancy work (e.g., Altay, 2025, on Pygmalion "
        "processes in EMI enrolment), while shifting the outcome from enrolment choice to within-student "
        "proficiency change over the EMI degree.",
    )

    add_heading_styled(doc, "Research questions", level=2)
    add_para(
        doc,
        "The quantitative strand addressed four research questions, worded associatively rather than causally:",
        first_indent=True,
    )
    rqs = [
        "RQ1. To what extent do institutional English proficiency scores change from PYP exit to graduation after four years of engineering EMI, and does change differ across Listening, Reading, Writing, and Speaking?",
        "RQ2. Do content lecturers systematically underestimate students’ demonstrated English relative to the PYP-exit measure (inaccuracy criterion)?",
        "RQ3. Is greater underrating and greater classroom translanguaging exposure associated with larger Speaking attrition, after accounting for pretest Speaking, major, gender, and lecturer EAP limitation?",
        "RQ4. Does translanguaging statistically mediate the association between underrating and Speaking decline?",
    ]
    for rq in rqs:
        p = doc.add_paragraph()
        p.paragraph_format.first_line_indent = Inches(0.25)
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(rq)
        set_run_font(r, size=11)

    add_heading_styled(doc, "Setting and institutional context", level=2)
    add_para(
        doc,
        "The institutional setting is a Turkish public university engineering faculty in which students "
        "complete an English Preparatory Year Programme before entering EMI content courses. Progression "
        "from the PYP into the major requires a minimum overall score of 60 on the institutional academic "
        "English examination, institutionally interpreted as CEFR B1 through local standard setting. During "
        "the degree, content lecturers may use Turkish (translanguaging) to varying degrees. Official "
        "programme rhetoric privileges English; classroom practice often includes L1 for clarification, "
        "pace, and comprehension—creating the expectancy–treatment ecology in which underrating and EAP "
        "limitation can both increase L1 use, but only underrating satisfies a Golem reading.",
    )

    add_heading_styled(doc, "Participants and sampling", level=2)
    add_para(
        doc,
        f"The analytic sample comprised {n} EMI engineering completers who sat both the PYP-exit and "
        f"graduation-year parallel forms (synthetic panel for method demonstration). Gender composition "
        f"approximated the faculty profile ({n_male} male, {100*n_male/n:.1f}%; {n_female} female, "
        f"{100*n_female/n:.1f}%). Age at graduation averaged {fmt(age_m)} years (SD = {fmt(age_sd)}; range 22–25), "
        f"with PYP-exit age = graduation age − 4. Majors were balanced across Mechanical, Chemical, and "
        f"Electrical-Electronics Engineering (n = 40 each). Students nested under 12 content lecturers "
        f"(10 students per lecturer), allowing exploratory lecturer-level displays of underrating and "
        f"translanguaging dose. Students who left the programme, transferred, or did not sit the "
        f"graduation-year form were outside the completer panel; such attrition is acknowledged as a "
        f"boundary condition for live institutional data.",
    )

    add_heading_styled(doc, "Instruments", level=2)
    add_heading_styled(doc, "Institutional academic English proficiency test", level=3)
    add_para(
        doc,
        "The test covered four skills—Listening, Reading, Writing, and Speaking—on a 0–100 scale. The overall "
        "score was the unweighted mean of the four skill scores. A minimum overall of 60/100 was mapped "
        "to CEFR B1 as the threshold for progression from the PYP into EMI majors. The graduation-year form "
        "was a parallel form (same blueprint and rubric family; different items), not a resit of the identical "
        "paper. Listening and Reading each comprised four sections mapped to IELTS Academic item types. Writing "
        "was scored with the public IELTS Academic Writing criteria (Task Response, Coherence and Cohesion, "
        "Lexical Resource, Grammatical Range and Accuracy). Speaking used the public IELTS Academic Speaking "
        "criteria (Fluency and Coherence, Lexical Resource, Grammatical Range and Accuracy, Pronunciation). "
        "Criteria were converted internally to the 0–100 institutional scale.",
    )
    add_para(
        doc,
        "Writing scripts and Speaking performances were marked independently by three raters: the testing "
        "expert (author) and two Preparatory Year Programme English language instructors. The official skill "
        "score was the mean of the three marks. Inter-rater reliability was evaluated with Shrout and Fleiss "
        "ICC(2,1) for a single rater and ICC(2,k) for the reliability of the three-rater mean. Listening and "
        "Reading were objectively scored. Content-lecturer estimates of student English, used for the "
        "inaccuracy criterion, were collected separately from the PYP raters of the test.",
    )

    add_heading_styled(doc, "Lecturer expectancy and translanguaging measures", level=3)
    add_para(
        doc,
        "Each student’s content lecturer provided an estimate of the student’s English proficiency on the "
        "same 0–100 metric as the institutional test. Underrating_Gap was defined as Pre_Overall − "
        "Lecturer_Est_English (positive values = underestimation). Students reported the approximate "
        "percentage of content-course time conducted in Turkish rather than English (TL_percent; 0–100). "
        "Five-point Likert scales (1 = strongly disagree, 5 = strongly agree) measured perceived underrating "
        "(PU1–PU5), translanguaging exposure (TL1–TL5), lecturer EAP limitation (EAP1–EAP5; competing cause), "
        "willingness to communicate in English (WTC1–WTC5), and English self-efficacy (SE1–SE5).",
    )

    add_heading_styled(doc, "Concurrent validity subsample", level=3)
    add_para(
        doc,
        "A stratified subsample (n = 36; 12 per major) additionally sat official IELTS Academic practice "
        "materials under exam conditions to support concurrent validity claims for the institutional test. "
        "Pearson correlations between institutional pretest skill scores and corresponding IELTS skill scores "
        "were computed.",
    )

    add_heading_styled(doc, "Procedure", level=2)
    add_para(
        doc,
        "Pretest scores were taken from the institutional PYP-exit administration. Posttest scores were "
        "taken from the parallel graduation-year administration. Lecturer estimates and student questionnaires "
        "were collected in the final year. All proficiency scores and lecturer estimates used the same 0–100 "
        "metric; the PYP pass threshold of 60 remained the interpretive anchor for B1-level competence at "
        "programme entry. For the synthetic demonstration panel, data were generated under calibrated "
        "constraints matching these institutional rules; live studies should replace the panel with "
        "de-identified institutional records under ethics approval.",
    )

    add_heading_styled(doc, "Data analysis", level=2)
    add_para(
        doc,
        "Analyses used paired-samples t tests (and Wilcoxon signed-rank companions) for pre–post skill "
        "change, with Cohen’s d_z and 95% confidence intervals for mean differences (Nicol & Pexman, 2010a, "
        "Chapter 5 Play-It-Safe multi-t-test format). Shapiro–Wilk tests were applied to difference scores. "
        "Internal consistency used Cronbach’s α and McDonald’s ω. Inter-rater reliability used ICC(2,1) and "
        "ICC(2,k). Concurrent validity used Pearson correlations with the IELTS subsample.",
    )
    add_para(
        doc,
        "Mechanism tests included (a) paired comparison of Pre_Overall versus Lecturer_Est_English; "
        "(b) Pearson correlations of Decline_Speaking with underrating, TL_percent, PU, EAP, WTC, and SE "
        "(Nicol & Pexman correlation / means–SD formats); (c) OLS regressions of Decline_Speaking on "
        "EAP-only, underrating, and a joint model with underrating, TL_percent, EAP_mean, Pre_Speaking, "
        "major, and gender (Nicol & Pexman multiple-regression Play-It-Safe summary: B, SE B, β, t, p, with "
        "R² in the table note); (d) a Sobel mediation check for underrating → translanguaging → Speaking "
        "decline; and (e) exploratory lecturer-level correlations. Only two figures were retained—skill "
        "mean change with 95% CIs, and Speaking decline against underrating/translanguaging—consistent with "
        "Displaying Your Findings guidance to include figures only when they clarify a pattern not already "
        "transparent in tables (Nicol & Pexman, 2010b).",
    )

    add_heading_styled(doc, "Ethical considerations", level=2)
    add_para(
        doc,
        "A live institutional study would require ethics-board approval, informed consent for questionnaires "
        "and lecturer estimates, and secure handling of linked proficiency records. The present draft uses a "
        "synthetic panel expressly to prototype instruments, analysis, and reporting without processing "
        "identifiable student data.",
    )

    # ========================= RESULTS =========================
    add_heading_styled(doc, "Quantitative Results", level=1)
    add_para(
        doc,
        "Results are organised by research question. Tables follow Nicol and Pexman’s Play-It-Safe formats "
        "for means, paired t tests, correlations, and multiple regression. Figures are limited to two "
        "inferentially central displays. All proficiency scores are on a 0–100 institutional scale; the "
        "PYP pass threshold was 60/100 (≈ CEFR B1).",
    )

    # --- Table 1 Demographics / key descriptives (Nicol Ch.2/3) ---
    add_heading_styled(doc, "Sample profile and score distributions", level=2)
    pre_m = desc.loc["Pre_Overall", "mean"]
    pre_sd = desc.loc["Pre_Overall", "sd"]
    pre_min = desc.loc["Pre_Overall", "min"]
    post_m = desc.loc["Post_Overall", "mean"]
    post_sd = desc.loc["Post_Overall", "sd"]
    n_below = int((s["Post_Overall"] < 60).sum())
    add_para(
        doc,
        f"All {n} completers scored at or above the institutional B1 threshold on the pretest "
        f"(Pre_Overall minimum = {fmt(pre_min,1)}; M = {fmt(pre_m)}, SD = {fmt(pre_sd)}). "
        f"At graduation, overall M = {fmt(post_m)} (SD = {fmt(post_sd)}), and {n_below} students "
        f"({n_below/n*100:.1f}%) scored below 60. Table 1 summarises key variables on the 0–100 scale "
        f"(and Likert means where applicable).",
    )

    add_table_number_title(
        doc,
        "Table 1",
        "Descriptive Statistics for Key Study Variables (N = 120)",
    )
    t1 = doc.add_table(rows=1, cols=6)
    fill_header_row(t1.rows[0], ["Variable", "M", "SD", "Min", "Max", "Skew"])
    for var in [
        "Pre_Overall",
        "Post_Overall",
        "Decline_Listening",
        "Decline_Reading",
        "Decline_Writing",
        "Decline_Speaking",
        "Underrating_Gap",
        "TL_percent",
        "PU_mean",
        "EAP_mean",
        "WTC_mean",
        "SE_mean",
    ]:
        row = desc.loc[var]
        cells = t1.add_row().cells
        vals = [
            var,
            fmt(row["mean"]),
            fmt(row["sd"]),
            fmt(row["min"], 1),
            fmt(row["max"], 1),
            fmt(row["skew"]),
        ]
        for i, val in enumerate(vals):
            cells[i].text = val
    style_body_cells(t1)
    apply_apa_table_borders(t1)
    add_table_note(
        doc,
        "Proficiency scores (Pre_*/Post_*) and Underrating_Gap are on the institutional 0–100 scale; "
        "PYP pass threshold = 60 (≈ CEFR B1). Decline_* = Pre − Post in points (positive = attrition; "
        "negative = gain). PU/EAP/WTC/SE means are Likert composites (1–5). TL_percent = estimated % of "
        "content-course time in Turkish.",
    )

    # --- Reliability (brief + compact table) ---
    add_heading_styled(doc, "Reliability and concurrent validity", level=2)
    add_para(
        doc,
        f"Internal consistency was acceptable to high. Cronbach’s α for the eight Listening/Reading section "
        f"scores was {fmt(rel.loc['Pre_full_sections','Cronbach_alpha'],3)} at pretest and "
        f"{fmt(rel.loc['Post_full_sections','Cronbach_alpha'],3)} at posttest. Questionnaire alphas were "
        f"{fmt(rel.loc['Perceived_underrating_PU','Cronbach_alpha'],3)} (perceived underrating), "
        f"{fmt(rel.loc['Translanguaging_Likert_TL','Cronbach_alpha'],3)} (translanguaging), "
        f"{fmt(rel.loc['Lecturer_EAP_limitation','Cronbach_alpha'],3)} (lecturer EAP limitation), "
        f"{fmt(rel.loc['WTC_English','Cronbach_alpha'],3)} (WTC), and "
        f"{fmt(rel.loc['Self_efficacy_English','Cronbach_alpha'],3)} (self-efficacy). "
        f"Inter-rater ICC(2,k) for three-rater means was "
        f"{fmt(icc.loc['Writing_Pre','ICC2_k_average'],3)} / {fmt(icc.loc['Writing_Post','ICC2_k_average'],3)} "
        f"for Writing and "
        f"{fmt(icc.loc['Speaking_Pre','ICC2_k_average'],3)} / {fmt(icc.loc['Speaking_Post','ICC2_k_average'],3)} "
        f"for Speaking (pre/post). Concurrent validity against IELTS Academic practice materials (n = 36) was "
        f"r = {fmt(ielts.loc['Pre_Overall','r'],3)} for overall score; skill rs were "
        f"Listening {fmt(ielts.loc['Pre_Listening','r'],3)}, "
        f"Reading {fmt(ielts.loc['Pre_Reading','r'],3)}, "
        f"Writing {fmt(ielts.loc['Pre_Writing','r'],3)}, and "
        f"Speaking {fmt(ielts.loc['Pre_Speaking','r'],3)} (all p < .001).",
    )

    # --- RQ1 paired t Play-It-Safe ---
    add_heading_styled(doc, "Pre–post proficiency change (RQ1)", level=2)
    sp = paired.loc["Speaking"]
    li = paired.loc["Listening"]
    re_ = paired.loc["Reading"]
    wr = paired.loc["Writing"]
    ov = paired.loc["Overall"]
    add_mixed_para(
        doc,
        [
            ("Attrition was not uniform across skills. ", False, False),
            ("Both oral–aural skills declined significantly: ", False, False),
            (f"Speaking (M_decline = {fmt(sp['mean_decline'])}, ", False, False),
            (f"t(119) = {fmt(sp['t'])}, p {apa_p(sp['p_t'])}, d_z = {fmt(sp['d_z'])}) ", False, False),
            (f"and Listening (M = {fmt(li['mean_decline'])}, p {apa_p(li['p_t'])}, d_z = {fmt(li['d_z'])}). ", False, False),
            ("This pattern is consistent with under-exposure to verbal interaction arising from lecturers’ ", False, False),
            ("EAP limitations and from underrating students’ English (Golem). ", False, False),
            (f"Reading showed no statistically significant decline (M = {fmt(re_['mean_decline'])}, p {apa_p(re_['p_t'])}), ", False, False),
            ("with a slight numerical gain consistent with academic written exposure; ", False, False),
            (f"Writing likewise showed no significant decline (M = {fmt(wr['mean_decline'])}, p {apa_p(wr['p_t'])}), ", False, False),
            ("consistent with lab reports and written assignments. ", False, False),
            (f"Overall change followed the oral–aural pattern (M = {fmt(ov['mean_decline'])}, p {apa_p(ov['p_t'])}).", False, False),
        ],
    )

    add_table_number_title(
        doc,
        "Table 2",
        "Paired-Samples Comparisons of Pretest and Posttest Skill Scores (N = 120)",
    )
    t2 = doc.add_table(rows=1, cols=9)
    fill_header_row(
        t2.rows[0],
        ["Skill", "Pre M", "Pre SD", "Post M", "Post SD", "Mdiff", "t(119)", "p", "d_z"],
    )
    for skill in ["Listening", "Reading", "Writing", "Speaking", "Overall"]:
        row = paired.loc[skill]
        cells = t2.add_row().cells
        vals = [
            skill,
            fmt(row["pre_mean"]),
            fmt(row["pre_sd"]),
            fmt(row["post_mean"]),
            fmt(row["post_sd"]),
            f"{fmt(row['mean_decline'])}{stars(row['p_t'])}",
            fmt(row["t"]),
            apa_p(row["p_t"]),
            fmt(row["d_z"]),
        ]
        for i, val in enumerate(vals):
            cells[i].text = val
    style_body_cells(t2)
    apply_apa_table_borders(t2)
    add_table_note(
        doc,
        "Scores are out of 100. PYP pass threshold = 60 (≈ CEFR B1); all completers scored ≥ 60 at pretest. "
        "Mdiff = Pre − Post (positive = attrition; negative = gain). d_z = Cohen’s d for paired designs. "
        "95% CIs for mean differences are reported in the Excel workbook (Paired_pre_post). "
        "Wilcoxon signed-rank p values were consistent with the paired t conclusions. "
        "*p < .05. **p < .01. ***p < .001.",
    )

    # Figure 1 only
    fig1 = DESKTOP / "figures" / "fig1_skill_mean_decline.png"
    if not fig1.exists():
        fig1 = ROOT / "outputs" / "figures" / "fig1_skill_mean_decline.png"
    if fig1.exists():
        add_figure_caption(
            doc,
            "Figure 1",
            "Mean pre–post change by skill with 95% confidence intervals (points on the 0–100 institutional scale).",
            note="Positive values indicate attrition. Listening and Speaking (oral–aural) decline significantly; "
            "Reading and Writing do not. PYP pass threshold = 60. Error bars are 95% CIs for mean differences "
            "(Nicol & Pexman, 2010b).",
        )
        doc.add_picture(str(fig1), width=Inches(5.9))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER

    # --- RQ2 inaccuracy ---
    add_heading_styled(doc, "Inaccuracy of lecturer expectancy (RQ2)", level=2)
    pre_act = float(s["Pre_Overall"].mean())
    lect_est = float(s["Lecturer_Est_English"].mean())
    gap_m = float(s["Underrating_Gap"].mean())
    gap_tt = stats.ttest_rel(s["Pre_Overall"], s["Lecturer_Est_English"])
    gap_dz = gap_m / float(s["Underrating_Gap"].std(ddof=1))
    add_para(
        doc,
        f"Content lecturers systematically underestimated students’ English relative to the institutional "
        f"PYP-exit measure. Mean actual Pre_Overall was {fmt(pre_act)}, whereas mean lecturer estimate was "
        f"{fmt(lect_est)}; the mean underrating gap was {fmt(gap_m)} points on the 0–100 scale, "
        f"t(119) = {fmt(gap_tt.statistic)}, p {apa_p(gap_tt.pvalue)}, d_z = {fmt(gap_dz)}. "
        "This satisfies the inaccuracy criterion associated with a Golem interpretation: the low expectation "
        "is not merely perceived as discouraging; it is incorrect relative to demonstrated proficiency at "
        "programme entry to EMI.",
    )

    # --- RQ3 correlations Nicol style ---
    add_heading_styled(doc, "Associations with Speaking attrition (RQ3)", level=2)
    add_para(
        doc,
        f"Speaking decline correlated positively with the underrating gap "
        f"(r = {fmt(golem.loc['Underrating_Gap','r'],3)}, p {apa_p(golem.loc['Underrating_Gap','p'])}), "
        f"translanguaging exposure (r = {fmt(golem.loc['TL_percent','r'],3)}, p {apa_p(golem.loc['TL_percent','p'])}), "
        f"and perceived underrating (r = {fmt(golem.loc['PU_mean','r'],3)}, p {apa_p(golem.loc['PU_mean','p'])}). "
        f"It correlated negatively with WTC (r = {fmt(golem.loc['WTC_mean','r'],3)}, p {apa_p(golem.loc['WTC_mean','p'])}) "
        f"and self-efficacy (r = {fmt(golem.loc['SE_mean','r'],3)}, p {apa_p(golem.loc['SE_mean','p'])}). "
        f"Lecturer EAP limitation was a weaker bivariate correlate "
        f"(r = {fmt(golem.loc['EAP_mean','r'],3)}, p {apa_p(golem.loc['EAP_mean','p'])}).",
    )

    add_table_number_title(
        doc,
        "Table 3",
        "Means, Standard Deviations, and Correlations of Predictors With Decline_Speaking",
    )
    t3 = doc.add_table(rows=1, cols=5)
    fill_header_row(t3.rows[0], ["Variable", "M", "SD", "r with Decline_Speaking", "p"])
    # outcome row first
    cells = t3.add_row().cells
    cells[0].text = "Decline_Speaking (outcome)"
    cells[1].text = fmt(desc.loc["Decline_Speaking", "mean"])
    cells[2].text = fmt(desc.loc["Decline_Speaking", "sd"])
    cells[3].text = "—"
    cells[4].text = "—"
    roles_order = [
        "Underrating_Gap",
        "TL_percent",
        "PU_mean",
        "EAP_mean",
        "WTC_mean",
        "SE_mean",
    ]
    for pred in roles_order:
        cells = t3.add_row().cells
        m = desc.loc[pred, "mean"] if pred in desc.index else float("nan")
        sd = desc.loc[pred, "sd"] if pred in desc.index else float("nan")
        r = golem.loc[pred, "r"]
        p = golem.loc[pred, "p"]
        cells[0].text = pred
        cells[1].text = fmt(m)
        cells[2].text = fmt(sd)
        cells[3].text = f"{fmt(r, 3)}{stars(p)}"
        cells[4].text = apa_p(p)
    style_body_cells(t3)
    apply_apa_table_borders(t3)
    add_table_note(
        doc,
        "Decline_Speaking and Underrating_Gap are in points on the 0–100 institutional scale "
        "(PYP pass threshold = 60). TL_percent is percentage of class time in Turkish. "
        "PU/EAP/WTC/SE are Likert means (1–5). Format follows Nicol and Pexman (2010a) correlation "
        "Play-It-Safe practice of reporting M, SD, and r. *p < .05. **p < .01. ***p < .001.",
    )

    fig2 = DESKTOP / "figures" / "fig2_golem_speaking_paths.png"
    if not fig2.exists():
        fig2 = ROOT / "outputs" / "figures" / "fig2_golem_speaking_paths.png"
    if fig2.exists():
        add_figure_caption(
            doc,
            "Figure 2",
            "Speaking decline associated with lecturer underrating (A) and translanguaging exposure (B).",
            note="Speaking change is in points on the 0–100 scale (pre − post). Fitted lines are OLS "
            "with 95% confidence bands. Multipanel layout follows Displaying Your Findings conventions "
            "for related scatterplots (Nicol & Pexman, 2010b).",
        )
        doc.add_picture(str(fig2), width=Inches(6.1))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER

    # --- Regression Play-It-Safe ---
    add_heading_styled(doc, "Multiple regression predicting Speaking decline (RQ3)", level=2)
    add_para(
        doc,
        "Three OLS models predicted Decline_Speaking. Model 1 entered lecturer EAP limitation with "
        "Pre_Speaking, major, and gender (competing-cause baseline). Model 2 entered underrating with the "
        "same covariates. Model 3 jointly entered underrating, TL_percent, and EAP_mean with covariates. "
        "Table 4 reports the Play-It-Safe regression summary for the focal joint model; Models 1–2 are "
        "summarised in text and fully tabulated in the Excel workbook.",
    )

    m3 = models["M3_Full"]
    m1 = models["M1_EAP_only"]
    m2 = models["M2_Underrating"]
    # key coeffs from live reg sheet
    def coef_row(model_name, term):
        sub = reg[(reg["model"] == model_name) & (reg["term"] == term)].iloc[0]
        return float(sub["b"]), float(sub["SE"]), float(sub["t"]), float(sub["p"])

    b_eap1, se_eap1, t_eap1, p_eap1 = coef_row("M1_EAP_only", "EAP_mean")
    b_u2, se_u2, t_u2, p_u2 = coef_row("M2_Underrating", "Underrating_Gap")
    add_para(
        doc,
        f"Model 1 (EAP-only) yielded a significant EAP coefficient (B = {fmt(b_eap1)}, SE = {fmt(se_eap1)}, "
        f"t = {fmt(t_eap1)}, p {apa_p(p_eap1)}; R² = {fmt(m1.rsquared,3)}). "
        f"Model 2 showed a clear underrating effect (B = {fmt(b_u2)}, SE = {fmt(se_u2)}, "
        f"t = {fmt(t_u2)}, p {apa_p(p_u2)}; R² = {fmt(m2.rsquared,3)}). "
        f"In the joint Model 3 (R² = {fmt(m3.rsquared,3)}), underrating and translanguaging remained "
        f"significant predictors of Speaking attrition (Table 4).",
    )

    add_table_number_title(
        doc,
        "Table 4",
        "Regression Analysis Summary for Variables Predicting Decline_Speaking (Model 3)",
    )
    t4 = doc.add_table(rows=1, cols=6)
    fill_header_row(t4.rows[0], ["Variable", "B", "SE B", "β", "t", "p"])
    y = s["Decline_Speaking"]
    focal = [
        ("Underrating_Gap", s["Underrating_Gap"]),
        ("TL_percent", s["TL_percent"]),
        ("EAP_mean", s["EAP_mean"]),
        ("Pre_Speaking", s["Pre_Speaking"]),
    ]
    for term, series in focal:
        b, se, t_val, p_val = coef_row("M3_Full", term)
        beta = beta_from_b(b, series, y)
        cells = t4.add_row().cells
        vals = [term, fmt(b), fmt(se), fmt(beta, 3), fmt(t_val), f"{apa_p(p_val)}{stars(p_val)}"]
        for i, val in enumerate(vals):
            cells[i].text = val
    # report major/gender briefly as covariates without cluttering — optional rows
    for term, label in [
        ("C(Major)[T.Mechanical Engineering]", "Major: Mechanical (vs Chemical)"),
        ("C(Major)[T.Electrical-Electronics Engineering]", "Major: Electrical-Electronics (vs Chemical)"),
        ("C(Gender)[T.Male]", "Gender: Male (vs Female)"),
    ]:
        b, se, t_val, p_val = coef_row("M3_Full", term)
        cells = t4.add_row().cells
        vals = [label, fmt(b), fmt(se), "—", fmt(t_val), apa_p(p_val)]
        for i, val in enumerate(vals):
            cells[i].text = val
    style_body_cells(t4)
    apply_apa_table_borders(t4)
    add_table_note(
        doc,
        f"N = 120. Outcome and continuous predictors are in points on the 0–100 institutional scale "
        f"(or Likert means for EAP_mean). β = standardized coefficient (B × SD_x / SD_y). "
        f"R² = {fmt(m3.rsquared,3)} (p {apa_p(m3.f_pvalue)}). Format follows Nicol and Pexman (2010a) "
        f"Play-It-Safe multiple-regression summary (Table 17.2). *p < .05. **p < .01. ***p < .001.",
    )

    # --- RQ4 mediation ---
    add_heading_styled(doc, "Mediation check (RQ4)", level=2)
    add_para(
        doc,
        f"A Sobel mediation check for underrating → translanguaging → Speaking decline yielded an "
        f"indirect effect of {fmt(med.loc['indirect_a_times_b','estimate'],3)} "
        f"(Sobel z = {fmt(med.loc['Sobel_z','estimate'])}, p {med.loc['Sobel_z','p_or_note']}), "
        f"with a remaining direct effect of underrating on Speaking decline "
        f"(c′ = {fmt(med.loc['direct_c_prime','estimate'],3)}). "
        "Bootstrap indirect effects should be reported with live data. Path coefficients are tabulated in "
        "the Excel Mediation sheet rather than as an additional figure.",
    )

    add_heading_styled(doc, "Summary of the quantitative pattern", level=2)
    add_para(
        doc,
        "Across four years of engineering EMI, completers did not show uniform proficiency loss. "
        "Listening and Speaking—the oral–aural skills—declined significantly, consistent with under-exposure "
        "to verbal classroom interaction driven by lecturers’ EAP limitations and by underrating of students’ "
        "English (Golem). Reading and Writing showed no statistically significant decline and slight numerical "
        "gains consistent with continued academic literacy in written English. Speaking decline tracked "
        "lecturer underrating and classroom L1 exposure in the mechanism models. Qualitative interviews remain "
        "necessary to separate lecturer EAP limitation from underrating as reasons for L1 use.",
    )

    add_heading_styled(doc, "Limitations specific to these quantitative claims", level=2)
    add_para(
        doc,
        "First, the panel reported here is synthetic and must be replaced with institutional records before "
        "submission. Second, associations do not establish causation; students were not randomly assigned to "
        "lecturers. Third, TL_percent is student-reported rather than observationally timed. Fourth, parallel "
        "forms require documented equating in a live study. Fifth, academic literacy in EMI may exceed what "
        "any proficiency test—institutional or IELTS—captures; that boundary should be stated in the discussion.",
    )

    add_heading_styled(doc, "References cited in these draft sections", level=2)
    refs = [
        "Altay, M. (2025). The Pygmalion effect as a driving force behind students’ English medium instruction pursuits. Language Awareness. https://doi.org/10.1080/09658416.2025.2523440",
        "Babad, E. Y., Inbar, J., & Rosenthal, R. (1982). Pygmalion, Galatea, and the Golem: Investigations of biased and unbiased teachers. Journal of Educational Psychology, 74(4), 459–474.",
        "Field, A. (2013). Discovering statistics using IBM SPSS statistics (4th ed.). Sage.",
        "Nicol, A. A. M., & Pexman, P. M. (2010a). Presenting your findings: A practical guide for creating tables (6th ed.). American Psychological Association.",
        "Nicol, A. A. M., & Pexman, P. M. (2010b). Displaying your findings: A practical guide for creating figures, posters, and presentations (6th ed.). American Psychological Association.",
    ]
    for ref in refs:
        p = doc.add_paragraph()
        p.paragraph_format.first_line_indent = Inches(-0.5)
        p.paragraph_format.left_indent = Inches(0.5)
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(ref)
        set_run_font(r, size=10)

    DESKTOP.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    paths = [DESKTOP / OUT_NAME, ROOT / OUT_NAME, ART / OUT_NAME]
    for path in paths:
        doc.save(str(path))
        print("wrote", path)
    return paths[0]


if __name__ == "__main__":
    build()
