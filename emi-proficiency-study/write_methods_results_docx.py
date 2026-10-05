#!/usr/bin/env python3
"""Write Methodology + Quantitative Results sections as a Word document."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from scipy import stats

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

ROOT = Path(__file__).resolve().parent
DESKTOP = Path("/home/ubuntu/Desktop/EMI Discouragement Project")
ART = Path("/opt/cursor/artifacts")
OUT_NAME = "EMI_Methodology_and_Quantitative_Results.docx"
XLSX = ROOT / "EMI_PYP_pre_post_synthetic_N120.xlsx"


def load_live():
    students = pd.read_excel(XLSX, "Students")
    paired = pd.read_excel(XLSX, "Paired_pre_post").set_index("skill")
    golem = pd.read_excel(XLSX, "Golem_correlations")
    desc = pd.read_excel(XLSX, "Descriptives").set_index("variable")
    rel = pd.read_excel(XLSX, "Reliability").set_index("scale")
    icc = pd.read_excel(XLSX, "ICC_raters").set_index("facet")
    ielts = pd.read_excel(XLSX, "Concurrent_IELTS")
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
    """parts: list of (text, bold, italic)."""
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


def set_table_style(table):
    table.style = "Table Grid"
    for row in table.rows:
        for cell in row.cells:
            for p in cell.paragraphs:
                p.paragraph_format.space_after = Pt(2)
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.line_spacing = 1.0
                for run in p.runs:
                    set_run_font(run, size=9)


def fill_header_row(row, labels):
    for i, label in enumerate(labels):
        row.cells[i].text = label
        for p in row.cells[i].paragraphs:
            for run in p.runs:
                set_run_font(run, bold=True, size=9)


def add_caption(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.first_line_indent = Inches(0)
    run = p.add_run(text)
    set_run_font(run, bold=True, italic=True, size=10)
    return p


def build() -> Path:
    live = load_live()
    s = live["students"]
    paired = live["paired"]
    golem = live["golem"].set_index("predictor")
    desc = live["desc"]
    rel = live["rel"]
    icc = live["icc"]
    ielts = live["ielts"].set_index("institutional")
    reg = live["reg"]
    med = live["med"]
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
        "Draft sections for manuscript development  ·  Based on a synthetic N = 120 panel\n"
        "(for instrument testing and paper scaffolding; replace with live institutional data before submission)"
    )
    set_run_font(r, italic=True, size=10, color=RGBColor(0x66, 0x66, 0x66))
    sub.paragraph_format.space_after = Pt(16)

    note = doc.add_paragraph()
    note.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    note.paragraph_format.first_line_indent = Inches(0)
    r = note.add_run("Author note. ")
    set_run_font(r, bold=True, italic=True, size=10)
    r = note.add_run(
        "The quantitative values reported below are from a calibrated synthetic panel designed to match the "
        "institution’s testing policy and the planned Golem-effect analysis. They illustrate the intended "
        "statistical pathway; they are not findings from real students."
    )
    set_run_font(r, italic=True, size=10)
    note.paragraph_format.space_after = Pt(14)

    # ========================= METHODOLOGY =========================
    add_heading_styled(doc, "Methodology", level=1)

    add_heading_styled(doc, "Research design", level=2)
    add_para(
        doc,
        "The study used a longitudinal panel design with two parallel administrations of an institutional "
        "academic English proficiency test: (a) at the end of the Preparatory Year Programme (PYP; pretest) "
        "and (b) immediately before graduation after four years of English-medium instruction (EMI) in an "
        "engineering major (posttest). The same students sat both forms. The design therefore supports a "
        "paired (dependent) comparison of proficiency change, supplemented by questionnaire and lecturer-"
        "estimate measures collected to evaluate whether any decline is consistent with a Golem-type "
        "expectancy mechanism rather than with uniform skill attrition alone."
    )
    add_para(
        doc,
        "Because the Golem effect, as originally formulated by Babad, Inbar, and Rosenthal (1982), requires "
        "evidence that a low expectation is inaccurate and is enacted through differential treatment that "
        "suppresses demonstrated performance, the quantitative strand measured four layers: (1) actual "
        "proficiency at PYP exit; (2) lecturers’ estimates of students’ English (inaccuracy); (3) exposure "
        "to Turkish in content courses (treatment); and (4) students’ willingness to communicate in English "
        "and English self-efficacy (internalization). Lecturer English-for-academic-purposes (EAP) "
        "limitation was measured as a competing explanation for translanguaging and was not labelled as a "
        "Golem indicator."
    )

    add_heading_styled(doc, "Participants", level=2)
    add_para(
        doc,
        "The analytic sample comprised N = 120 engineering students who completed both the PYP-exit and "
        "graduation-year administrations (completers). Gender composition reflected the predominantly male "
        "profile of Turkish EMI engineering cohorts: 82 male (68.3%) and 38 female (31.7%). Students were "
        "balanced across three majors in the Faculty of Engineering (n = 40 each): Mechanical Engineering, "
        "Chemical Engineering, and Electrical-Electronics Engineering. Age at graduation ranged from 22 to "
        "25 years; age at PYP exit was recorded as four years younger (18–21). Students were nested in "
        "12 content lecturers (10 students per lecturer), so that expectancy and classroom language "
        "practice could be examined at the lecturer level as well as the student level."
    )
    add_para(
        doc,
        "All participants had met the institutional PYP pass mark of 60/100, interpreted by the university’s "
        "testing policy as CEFR B1. Students who left the programme, transferred, or did not sit the "
        "graduation-year form were outside the completer panel; attrition of that kind is acknowledged as a "
        "limitation for generalisation."
    )

    add_heading_styled(doc, "Institutional testing instrument", level=2)
    add_para(
        doc,
        "Proficiency was assessed with an in-house academic English examination aligned with IELTS Academic. "
        "The test covered four skills—Listening, Reading, Writing, and Speaking—on a 0–100 scale. The overall "
        "score was the unweighted mean of the four skill scores. Institutional standard setting maps 60/100 "
        "to CEFR B1 as the threshold for progression from the PYP into EMI majors. The graduation-year form "
        "was a parallel form: the same blueprint and CEFR mapping, but different items. The two forms were "
        "not identical papers."
    )
    add_para(
        doc,
        "Listening and Reading each comprised four sections mapped to IELTS Academic item types. Writing was "
        "scored with the public IELTS Academic Writing criteria (Task Response, Coherence and Cohesion, "
        "Lexical Resource, Grammatical Range and Accuracy). Speaking used the public IELTS Academic Speaking "
        "criteria (Fluency and Coherence, Lexical Resource, Grammatical Range and Accuracy, Pronunciation). "
        "Criteria were converted internally to the 0–100 institutional scale."
    )

    add_heading_styled(doc, "Marking and raters", level=2)
    add_para(
        doc,
        "Writing scripts and Speaking performances were marked independently by three raters: the testing "
        "expert (author) and two Preparatory Year Programme English language instructors. The official skill "
        "score was the mean of the three marks. Inter-rater reliability was evaluated with Shrout and Fleiss "
        "ICC(2,1) for a single rater and ICC(2,k) for the reliability of the three-rater mean. Listening and "
        "Reading were objectively scored. Content-lecturer estimates of student English, used for the "
        "inaccuracy criterion, were collected from content lecturers and were independent of the PYP raters "
        "of the proficiency test."
    )

    add_heading_styled(doc, "Concurrent validity subsample", level=2)
    add_para(
        doc,
        "A stratified subsample (n = 36; 12 students per major) sat official IELTS Academic practice "
        "materials obtained from the IELTS website (ielts.org) under exam conditions at PYP exit. Pearson "
        "correlations between institutional skill/overall scores and corresponding IELTS band scores were "
        "used as concurrent-validity evidence. Content validity rested on the shared IELTS Academic blueprint "
        "and descriptors, the CEFR B1 threshold statement, and the parallel-form design."
    )

    add_heading_styled(doc, "Mechanism measures", level=2)
    add_para(
        doc,
        "In the final EMI year, students completed five-point Likert scales (1 = strongly disagree, "
        "5 = strongly agree) for perceived underrating (PU1–PU5), translanguaging exposure (TL1–TL5), "
        "lecturer EAP limitation (EAP1–EAP5; competing cause), willingness to communicate in English "
        "(WTC1–WTC5), and English self-efficacy (SE1–SE5). Students also estimated the percentage of "
        "content-course time conducted in Turkish rather than English (TL_percent; 0–100). The underrating "
        "gap was computed as Pre_Overall minus the content lecturer’s estimate of that student’s English "
        "(positive values = underestimated)."
    )

    add_heading_styled(doc, "Data analysis", level=2)
    add_para(
        doc,
        "Analyses were conducted in Python (pandas, SciPy, statsmodels). Descriptive statistics included "
        "means, standard deviations, minima, maxima, skewness, and excess kurtosis. Normality of difference "
        "scores (pre − post) was assessed with the Shapiro–Wilk test; the paired-samples t-test assumes "
        "approximate normality of difference scores, not of the raw totals. The primary proficiency-change "
        "test was a paired-samples t-test for each skill and for the overall score, with Wilcoxon signed-rank "
        "tests as distribution-free companions and Cohen’s d_z (and d_av) as effect sizes. An independent-"
        "samples t-test was not used for the pre–post comparison because observations were matched."
    )
    add_para(
        doc,
        "Internal consistency was estimated with Cronbach’s α and McDonald’s ω for Listening/Reading section "
        "scores, Writing/Speaking rubric criteria, and questionnaire scales. Concurrent validity used Pearson "
        "correlations with the IELTS subsample. Mechanism tests included (a) a paired comparison of actual "
        "PYP scores versus lecturer estimates; (b) Pearson correlations between overall decline and "
        "underrating, translanguaging, perceived underrating, EAP limitation, WTC, and self-efficacy; "
        "(c) OLS regressions of decline on EAP-only, underrating, and a joint model with underrating, "
        "TL_percent, EAP_mean, pretest, major, and gender; (d) a Sobel mediation check for the path "
        "underrating → translanguaging → decline; and (e) exploratory lecturer-level correlations and a "
        "one-way ICC of decline by lecturer. Causal language was kept associative throughout."
    )

    # ========================= RESULTS =========================
    add_heading_styled(doc, "Quantitative Results", level=1)

    add_heading_styled(doc, "Descriptive statistics and normality", level=2)
    pre_m = desc.loc["Pre_Overall", "mean"]; pre_sd = desc.loc["Pre_Overall", "sd"]; pre_min = desc.loc["Pre_Overall", "min"]
    post_m = desc.loc["Post_Overall", "mean"]; post_sd = desc.loc["Post_Overall", "sd"]
    n_below = int((s["Post_Overall"] < 60).sum())
    sw_w = desc.loc["Decline_Speaking", "shapiro_W"]; sw_p = desc.loc["Decline_Speaking", "shapiro_p"]
    add_para(
        doc,
        f"All 120 students scored at or above the institutional B1 threshold on the pretest "
        f"(Pre_Overall minimum = {fmt(pre_min,1)}; M = {fmt(pre_m)}, SD = {fmt(pre_sd)}). "
        f"At graduation, the overall mean was {fmt(post_m)} (SD = {fmt(post_sd)}), and {n_below} students "
        f"({n_below/120*100:.1f}%) scored below 60. Table 1 summarises key variables. "
        f"Shapiro–Wilk on Speaking difference scores was W = {fmt(sw_w,3)}, p = {apa_p(sw_p)}.",
    )

    add_caption(doc, "Table 1. Descriptive statistics for key variables (N = 120)")
    t1 = doc.add_table(rows=1, cols=7)
    fill_header_row(t1.rows[0], ["Variable", "M", "SD", "Min", "Max", "Skew", "Kurtosis"])
    for var in [
        "Pre_Overall", "Post_Overall", "Decline_Speaking", "Decline_Listening",
        "Decline_Reading", "Decline_Writing", "Underrating_Gap", "TL_percent",
        "PU_mean", "EAP_mean", "WTC_mean", "SE_mean",
    ]:
        row = desc.loc[var]
        cells = t1.add_row().cells
        vals = [var, fmt(row["mean"]), fmt(row["sd"]), fmt(row["min"],1), fmt(row["max"],1), fmt(row["skew"]), fmt(row["kurtosis_excess"])]
        for i, val in enumerate(vals):
            cells[i].text = val
    set_table_style(t1)
    add_para(
        doc,
        "Note. Proficiency scores (Pre_*/Post_*) are on the institutional 0–100 scale; "
        "the Preparatory Year Programme pass threshold was 60/100 (≈ CEFR B1). "
        "Decline_* = Pre − Post in points on that scale (positive = attrition; negative = gain). "
        "Kurtosis = excess kurtosis.",
        first_indent=False, italic=True, size=9, space_after=12,
    )

    add_heading_styled(doc, "Reliability and validity of the institutional test", level=2)
    add_para(
        doc,
        f"Internal consistency was acceptable to high. Cronbach’s α for the eight Listening/Reading section "
        f"scores was {fmt(rel.loc['Pre_full_sections','Cronbach_alpha'],3)} at pretest and "
        f"{fmt(rel.loc['Post_full_sections','Cronbach_alpha'],3)} at posttest. "
        f"Questionnaire alphas were {fmt(rel.loc['Perceived_underrating_PU','Cronbach_alpha'],3)} (perceived underrating), "
        f"{fmt(rel.loc['Translanguaging_Likert_TL','Cronbach_alpha'],3)} (translanguaging), "
        f"{fmt(rel.loc['Lecturer_EAP_limitation','Cronbach_alpha'],3)} (lecturer EAP limitation), "
        f"{fmt(rel.loc['WTC_English','Cronbach_alpha'],3)} (WTC), and "
        f"{fmt(rel.loc['Self_efficacy_English','Cronbach_alpha'],3)} (self-efficacy). "
        f"Inter-rater ICC(2,k) values for the official three-rater means were "
        f"{fmt(icc.loc['Writing_Pre','ICC2_k_average'],3)} / {fmt(icc.loc['Writing_Post','ICC2_k_average'],3)} for Writing and "
        f"{fmt(icc.loc['Speaking_Pre','ICC2_k_average'],3)} / {fmt(icc.loc['Speaking_Post','ICC2_k_average'],3)} for Speaking (pre/post).",
    )
    add_para(
        doc,
        f"Concurrent validity against official IELTS Academic practice materials (n = 36) was "
        f"r = {fmt(ielts.loc['Pre_Overall','r'],3)} (p {apa_p(ielts.loc['Pre_Overall','p'])}) for the overall score; "
        f"skill correlations were Listening {fmt(ielts.loc['Pre_Listening','r'],3)}, "
        f"Reading {fmt(ielts.loc['Pre_Reading','r'],3)}, "
        f"Writing {fmt(ielts.loc['Pre_Writing','r'],3)}, and "
        f"Speaking {fmt(ielts.loc['Pre_Speaking','r'],3)} (all p < .001).",
    )

    add_heading_styled(doc, "Pre–post proficiency change: oral–aural attrition", level=2)
    sp = paired.loc["Speaking"]; li = paired.loc["Listening"]; re_ = paired.loc["Reading"]; wr = paired.loc["Writing"]; ov = paired.loc["Overall"]
    add_mixed_para(
        doc,
        [
            ("Attrition was not uniform across skills. ", False, False),
            ("Both oral–aural skills declined significantly: ", False, False),
            (f"Speaking (M_decline = {fmt(sp['mean_decline'])}, ", False, False),
            (f"t(119) = {fmt(sp['t'])}, p {apa_p(sp['p_t'])}, d_z = {fmt(sp['d_z'])}) ", False, False),
            (f"and Listening (M = {fmt(li['mean_decline'])}, p {apa_p(li['p_t'])}, d_z = {fmt(li['d_z'])}). ", False, False),
            ("This pattern is consistent with under-exposure to verbal interaction in EMI classrooms, ", False, False),
            ("arising from lecturers’ own EAP limitations and from underrating students’ English (Golem). ", False, False),
            (f"Reading showed no statistically significant decline (M = {fmt(re_['mean_decline'])}, p {apa_p(re_['p_t'])}), ", False, False),
            ("with a slight numerical gain consistent with continued exposure to academic written texts; ", False, False),
            (f"Writing likewise showed no significant decline (M = {fmt(wr['mean_decline'])}, p {apa_p(wr['p_t'])}), ", False, False),
            ("consistent with lab reports and written assignments. ", False, False),
            ("The oral–aural drop is therefore the attrition story later linked to translanguaging and expectancy.", False, False),
        ],
    )

    add_caption(doc, "Table 2. Paired pre–post comparisons by skill (N = 120)")
    t2 = doc.add_table(rows=1, cols=8)
    fill_header_row(t2.rows[0], ["Skill", "Pre M (SD)", "Post M (SD)", "M change", "t(119)", "p", "Wilcoxon p", "d_z"])
    for skill in ["Listening", "Reading", "Writing", "Speaking", "Overall"]:
        row = paired.loc[skill]
        cells = t2.add_row().cells
        vals = [
            skill,
            f"{fmt(row['pre_mean'])} ({fmt(row['pre_sd'])})",
            f"{fmt(row['post_mean'])} ({fmt(row['post_sd'])})",
            fmt(row['mean_decline']),
            fmt(row['t']),
            apa_p(row['p_t']),
            apa_p(row['p_wilcoxon']),
            fmt(row['d_z']),
        ]
        for i, val in enumerate(vals):
            cells[i].text = val
    set_table_style(t2)
    add_para(
        doc,
        "Note. Skill scores are out of 100. The PYP pass threshold was 60/100 (≈ CEFR B1); "
        "all completers scored ≥ 60 at pretest. Positive M change = attrition (lower at graduation); "
        "negative = gain. d_z = Cohen’s d for paired designs. Written skills (Reading, Writing) "
        "show no statistically significant decline and are summarised here rather than in a separate figure.",
        first_indent=False, italic=True, size=9, space_after=12,
    )

    # Embed only the two statistically central figures.
    fig_dir = DESKTOP / "figures"
    fig1 = fig_dir / "fig1_skill_mean_decline.png"
    fig2 = fig_dir / "fig2_golem_speaking_paths.png"
    # Fall back to package outputs if Desktop mirror is missing.
    if not fig1.exists():
        fig1 = ROOT / "outputs" / "figures" / "fig1_skill_mean_decline.png"
    if not fig2.exists():
        fig2 = ROOT / "outputs" / "figures" / "fig2_golem_speaking_paths.png"
    if fig1.exists():
        add_caption(
            doc,
            "Figure 1. Mean pre–post change by skill with 95% CI (points on the 0–100 institutional scale; "
            "PYP pass threshold = 60)",
        )
        doc.add_picture(str(fig1), width=Inches(6.0))
        last = doc.paragraphs[-1]
        last.alignment = WD_ALIGN_PARAGRAPH.CENTER
        add_para(
            doc,
            "Note. Positive values indicate attrition. Listening and Speaking (oral–aural) decline "
            "significantly; Reading and Writing do not.",
            first_indent=False, italic=True, size=9, space_after=10,
        )
    if fig2.exists():
        add_caption(
            doc,
            "Figure 2. Speaking decline associated with lecturer underrating and translanguaging exposure "
            "(Speaking change in points on the 0–100 scale)",
        )
        doc.add_picture(str(fig2), width=Inches(6.2))
        last = doc.paragraphs[-1]
        last.alignment = WD_ALIGN_PARAGRAPH.CENTER
        add_para(
            doc,
            "Note. Other associations (reliability, concurrent validity, OLS coefficients, mediation) "
            "are reported in Tables 1–4 rather than as additional figures.",
            first_indent=False, italic=True, size=9, space_after=12,
        )
    add_heading_styled(doc, "Inaccuracy of lecturer expectancy", level=2)
    pre_act = float(s["Pre_Overall"].mean())
    lect_est = float(s["Lecturer_Est_English"].mean())
    gap_m = float(s["Underrating_Gap"].mean())
    gap_tt = stats.ttest_rel(s["Pre_Overall"], s["Lecturer_Est_English"])
    gap_t = float(gap_tt.statistic)
    gap_p = float(gap_tt.pvalue)
    gap_dz = gap_m / float(s["Underrating_Gap"].std(ddof=1))
    add_para(
        doc,
        f"Content lecturers systematically underestimated students’ English relative to the institutional "
        f"PYP-exit measure. Mean actual Pre_Overall was {fmt(pre_act)}, whereas mean lecturer estimate was "
        f"{fmt(lect_est)}; the mean underrating gap was {fmt(gap_m)} points, t(119) = {fmt(gap_t)}, "
        f"p {apa_p(gap_p)}, d_z = {fmt(gap_dz)}. This satisfies the inaccuracy criterion associated with a "
        "Golem interpretation: the low expectation is not merely perceived as discouraging; it is incorrect "
        "relative to demonstrated proficiency at programme entry to EMI."
    )

    add_heading_styled(doc, "Associations with Speaking attrition", level=2)
    add_para(
        doc,
        f"Speaking decline correlated positively with the underrating gap "
        f"(r = {fmt(golem.loc['Underrating_Gap','r'],3)}, p {apa_p(golem.loc['Underrating_Gap','p'])}), "
        f"translanguaging exposure (TL_percent; r = {fmt(golem.loc['TL_percent','r'],3)}, p {apa_p(golem.loc['TL_percent','p'])}), "
        f"and perceived underrating (r = {fmt(golem.loc['PU_mean','r'],3)}, p {apa_p(golem.loc['PU_mean','p'])}). "
        f"It correlated negatively with WTC (r = {fmt(golem.loc['WTC_mean','r'],3)}, p {apa_p(golem.loc['WTC_mean','p'])}) "
        f"and self-efficacy (r = {fmt(golem.loc['SE_mean','r'],3)}, p {apa_p(golem.loc['SE_mean','p'])}). "
        f"Lecturer EAP limitation was weaker as a bivariate correlate "
        f"(r = {fmt(golem.loc['EAP_mean','r'],3)}, p {apa_p(golem.loc['EAP_mean','p'])}). "
        "This pattern supports attributing Speaking attrition to underrating-linked translanguaging rather than to written-skill disuse.",
    )

    add_caption(doc, "Table 3. Correlations with Decline_Speaking (primary attrition outcome)")
    t3 = doc.add_table(rows=1, cols=4)
    fill_header_row(t3.rows[0], ["Predictor", "r", "p", "Interpretive role"])
    roles = {
        "Underrating_Gap": "Golem: inaccuracy",
        "TL_percent": "Treatment: L1 exposure",
        "PU_mean": "Student-perceived underrating",
        "EAP_mean": "Competing cause (not Golem)",
        "WTC_mean": "Internalization",
        "SE_mean": "Internalization",
    }
    for pred, role in roles.items():
        cells = t3.add_row().cells
        vals = [pred, fmt(golem.loc[pred, "r"], 3), apa_p(golem.loc[pred, "p"]), role]
        for i, val in enumerate(vals):
            cells[i].text = val
    set_table_style(t3)
    add_para(
        doc,
        "Note. Underrating_Gap is in points on the same 0–100 institutional scale "
        "(actual Pre_Overall − lecturer estimate). Decline_Speaking is likewise in points on 0–100.",
        first_indent=False, italic=True, size=9, space_after=12,
    )

    add_heading_styled(doc, "Regression models predicting Speaking decline", level=2)
    def _coef(model_name, term):
        sub = reg[(reg["model"] == model_name) & (reg["term"] == term)].iloc[0]
        return float(sub["b"]), float(sub["p"])
    b_eap1, p_eap1 = _coef("M1_EAP_only", "EAP_mean")
    b_u2, p_u2 = _coef("M2_Underrating", "Underrating_Gap")
    b_u3, p_u3 = _coef("M3_Full", "Underrating_Gap")
    b_tl3, p_tl3 = _coef("M3_Full", "TL_percent")
    b_eap3, p_eap3 = _coef("M3_Full", "EAP_mean")
    add_para(
        doc,
        f"Three OLS models predicted Decline_Speaking. Model 1 (lecturer EAP limitation with Pre_Speaking, major, gender) "
        f"was weak (EAP_mean b = {fmt(b_eap1)}, p {apa_p(p_eap1)}). "
        f"Model 2 showed a clear underrating effect (b = {fmt(b_u2)}, p {apa_p(p_u2)}). "
        f"In the joint Model 3, underrating (b = {fmt(b_u3)}, p {apa_p(p_u3)}) and "
        f"translanguaging exposure (b = {fmt(b_tl3)}, p {apa_p(p_tl3)}) remained significant predictors of Speaking attrition. "
        f"This is the quantitative backbone for linking Speaking loss to underrating-driven L1 use in EMI classrooms.",
    )

    add_caption(doc, "Table 4. Key coefficients predicting Decline_Speaking")
    t4 = doc.add_table(rows=1, cols=5)
    fill_header_row(t4.rows[0], ["Model", "Predictor", "b", "p", "Note"])
    for row in [
        ("1 EAP-only", "EAP_mean", fmt(b_eap1), apa_p(p_eap1), "Competing cause alone"),
        ("2 Underrating", "Underrating_Gap", fmt(b_u2), apa_p(p_u2), "Inaccuracy path"),
        ("3 Full", "Underrating_Gap", fmt(b_u3), apa_p(p_u3), "With TL + EAP + covariates"),
        ("3 Full", "TL_percent", fmt(b_tl3), apa_p(p_tl3), "Treatment path to Speaking"),
        ("3 Full", "EAP_mean", fmt(b_eap3), apa_p(p_eap3), "Competing cause in joint model"),
    ]:
        cells = t4.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = val
    set_table_style(t4)
    add_para(
        doc,
        "Note. Models also included Pre_Speaking, major, and gender. Coefficients for Underrating_Gap "
        "and Decline_Speaking are in points on the 0–100 institutional scale (PYP pass threshold = 60). "
        "Full tables are in the Excel workbook (Regression_models).",
        first_indent=False, italic=True, size=9, space_after=12,
    )

    add_heading_styled(doc, "Mediation and lecturer-level checks", level=2)
    add_para(
        doc,
        f"A Sobel mediation check for underrating → translanguaging → Speaking decline yielded an "
        f"indirect effect of {fmt(med.loc['indirect_a_times_b','estimate'],3)} "
        f"(Sobel z = {fmt(med.loc['Sobel_z','estimate'])}, p {med.loc['Sobel_z','p_or_note']}), "
        f"with a remaining direct effect of underrating on Speaking decline "
        f"(c′ = {fmt(med.loc['direct_c_prime','estimate'],3)}). "
        "Bootstrap indirect effects should be reported with live data. Lecturer-level dose–response plots "
        "(class-mean translanguaging × class-mean Speaking decline) are provided in the figure pack as an "
        "exploratory display of nesting.",
    )

    add_heading_styled(doc, "Summary of the quantitative pattern", level=2)
    add_para(
        doc,
        "Across four years of engineering EMI, completers did not show uniform proficiency loss. "
        "Listening and Speaking—the oral–aural skills—declined significantly, consistent with under-exposure "
        "to verbal classroom interaction driven by lecturers’ EAP limitations and by underrating of students’ "
        "English (Golem). Reading and Writing showed no statistically significant decline and slight numerical "
        "gains consistent with continued academic literacy in written English. Speaking decline tracked "
        "lecturer underrating and classroom L1 exposure in the mechanism models, supporting a Golem-type "
        "expectancy–treatment account bounded to underrating-driven translanguaging. Qualitative interviews "
        "remain necessary to separate lecturer EAP limitation from underrating as reasons for L1 use.",
    )

    add_heading_styled(doc, "Limitations specific to these quantitative claims", level=2)
    add_para(
        doc,
        "First, the panel reported here is synthetic and must be replaced with institutional records before "
        "submission. Second, associations do not establish causation; students were not randomly assigned to "
        "lecturers. Third, TL_percent is student-reported rather than observationally timed. Fourth, parallel "
        "forms require documented equating in a live study. Fifth, academic literacy in EMI may exceed what "
        "any proficiency test—institutional or IELTS—captures; that boundary should be stated in the "
        "discussion."
    )

    # Save locations
    DESKTOP.mkdir(parents=True, exist_ok=True)
    ART.mkdir(parents=True, exist_ok=True)
    paths = [
        DESKTOP / OUT_NAME,
        ROOT / OUT_NAME,
        ART / OUT_NAME,
    ]
    for path in paths:
        doc.save(str(path))
        print("wrote", path)
    return paths[0]


if __name__ == "__main__":
    build()
