#!/usr/bin/env python3
"""Write Methodology + Quantitative Results sections as a Word document."""

from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

ROOT = Path(__file__).resolve().parent
DESKTOP = Path("/home/ubuntu/Desktop/EMI Discouragement Project")
ART = Path("/opt/cursor/artifacts")
OUT_NAME = "EMI_Methodology_and_Quantitative_Results.docx"


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
    add_para(
        doc,
        "All 120 students scored at or above the institutional B1 threshold on the pretest "
        "(Pre_Overall minimum = 60.1; M = 67.55, SD = 4.85). At graduation, the overall mean was 66.70 "
        "(SD = 6.39), and 14 students (11.7%) scored below 60. Table 1 summarises distributional "
        "properties for key variables. Shapiro–Wilk on the overall difference scores was compatible with "
        "normality (W = 0.980, p = .069), supporting the paired t-test; Wilcoxon results are reported "
        "alongside."
    )

    add_caption(doc, "Table 1. Descriptive statistics for key variables (N = 120)")
    t1 = doc.add_table(rows=1, cols=7)
    fill_header_row(t1.rows[0], ["Variable", "M", "SD", "Min", "Max", "Skew", "Kurtosis"])
    for row in [
        ("Pre_Overall", "67.55", "4.85", "60.1", "79.0", "0.13", "−0.84"),
        ("Post_Overall", "66.70", "6.39", "54.2", "84.2", "0.63", "0.05"),
        ("Decline_Overall", "0.85", "4.67", "−12.5", "9.3", "−0.17", "−0.58"),
        ("Underrating_Gap", "8.44", "3.74", "1.4", "18.6", "0.39", "−0.10"),
        ("TL_percent", "38.45", "8.57", "19.0", "62.2", "0.38", "−0.31"),
        ("PU_mean", "3.07", "0.69", "1.2", "4.8", "0.06", "−0.21"),
        ("EAP_mean", "3.14", "0.72", "1.6", "4.8", "−0.01", "−0.50"),
        ("WTC_mean", "3.87", "0.70", "2.0", "5.0", "−0.44", "−0.52"),
        ("SE_mean", "3.86", "0.72", "2.2", "5.0", "−0.36", "−0.68"),
    ]:
        cells = t1.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = val
    set_table_style(t1)
    add_para(
        doc,
        "Note. Decline_Overall = Pre_Overall − Post_Overall (positive = lower score at graduation). "
        "Kurtosis = excess kurtosis.",
        first_indent=False,
        italic=True,
        size=9,
        space_after=12,
    )

    add_heading_styled(doc, "Reliability and validity of the institutional test", level=2)
    add_para(
        doc,
        "Internal consistency was acceptable to high across administrations. Cronbach’s α for the eight "
        "Listening/Reading section scores was .879 at pretest and .920 at posttest. Writing and Speaking "
        "criteria alphas ranged from .904 to .956. Questionnaire alphas were .849 (perceived underrating), "
        ".878 (translanguaging), .885 (lecturer EAP limitation), .854 (WTC), and .871 (self-efficacy). "
        "Inter-rater ICCs for the three-rater official means were high: Writing ICC(2,k) = .965 (pre) and "
        ".983 (post); Speaking ICC(2,k) = .966 (pre) and .979 (post)."
    )
    add_para(
        doc,
        "Concurrent validity against official IELTS Academic practice materials (n = 36) was substantial for "
        "the overall score (r = .788, p < .001) and moderate-to-strong by skill (Listening r = .610; "
        "Reading r = .868; Writing r = .649; Speaking r = .682; all p < .001). Pretest skill "
        "intercorrelations were moderate-to-strong (rs = .71–.78 among skills; .89–.91 with overall), "
        "consistent with a common academic-English factor."
    )

    add_heading_styled(doc, "Pre–post proficiency change", level=2)
    add_mixed_para(
        doc,
        [
            ("A paired-samples t-test showed a small but statistically significant decline in overall ", False, False),
            ("institutional proficiency from PYP exit to graduation, t(119) = 2.00, p = .048, ", False, False),
            ("95% CI [0.01, 1.69], Cohen’s d_z = 0.18 ", False, False),
            ("(Wilcoxon p = .039). ", False, False),
            ("The mean decline was 0.85 points (Pre M = 67.55, Post M = 66.70). ", False, False),
            ("Table 2 reports skill-level results. Writing and Speaking showed clearer declines ", False, False),
            ("(Writing: M_decline = 1.14, t(119) = 2.08, p = .039; Speaking: M_decline = 1.14, ", False, False),
            ("t(119) = 2.06, p = .042) than Listening (p = .088) and Reading (p = .063). ", False, False),
            ("This productive-skill emphasis is consistent with a classroom ecology in which students ", False, False),
            ("receive fewer opportunities to speak and write in English.", False, False),
        ],
    )

    add_caption(doc, "Table 2. Paired pre–post comparisons by skill (N = 120)")
    t2 = doc.add_table(rows=1, cols=8)
    fill_header_row(
        t2.rows[0],
        ["Skill", "Pre M (SD)", "Post M (SD)", "M decline", "t(119)", "p", "Wilcoxon p", "d_z"],
    )
    for row in [
        ("Listening", "68.54 (5.08)", "68.04 (5.46)", "0.50", "1.72", ".088", ".075", "0.16"),
        ("Reading", "67.81 (5.43)", "67.19 (6.55)", "0.62", "1.88", ".063", ".060", "0.17"),
        ("Writing", "67.23 (5.80)", "66.09 (8.02)", "1.14", "2.08", ".039", ".037", "0.19"),
        ("Speaking", "66.60 (5.38)", "65.47 (7.63)", "1.14", "2.06", ".042", ".039", "0.19"),
        ("Overall", "67.55 (4.85)", "66.70 (6.39)", "0.85", "2.00", ".048", ".039", "0.18"),
    ]:
        cells = t2.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = val
    set_table_style(t2)
    add_para(
        doc,
        "Note. Positive decline = lower score at graduation. d_z = Cohen’s d for paired designs "
        "(mean difference / SD of differences).",
        first_indent=False,
        italic=True,
        size=9,
        space_after=12,
    )

    # Embed key figures if present
    fig_dir = DESKTOP / "figures"
    overview = fig_dir / "tableau" / "tableau_dashboard_overview.png"
    golem = fig_dir / "rstudio" / "rstudio_golem_paths.png"
    if overview.exists():
        add_caption(doc, "Figure 1. Tableau-style overview of the pre–post panel and mechanism paths")
        doc.add_picture(str(overview), width=Inches(6.3))
        last = doc.paragraphs[-1]
        last.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if golem.exists():
        add_caption(doc, "Figure 2. Decline associated with underrating and translanguaging exposure")
        doc.add_picture(str(golem), width=Inches(6.3))
        last = doc.paragraphs[-1]
        last.alignment = WD_ALIGN_PARAGRAPH.CENTER

    add_heading_styled(doc, "Inaccuracy of lecturer expectancy", level=2)
    add_para(
        doc,
        "Content lecturers systematically underestimated students’ English relative to the institutional "
        "PYP-exit measure. Mean actual Pre_Overall was 67.55, whereas mean lecturer estimate was 59.11; "
        "the mean underrating gap was 8.44 points, t(119) = 24.75, p < .001, d_z = 2.26. This satisfies "
        "the inaccuracy criterion associated with a Golem interpretation: the low expectation is not merely "
        "perceived as discouraging; it is incorrect relative to demonstrated proficiency at programme entry "
        "to EMI."
    )

    add_heading_styled(doc, "Associations between mechanism variables and decline", level=2)
    add_para(
        doc,
        "Overall decline correlated positively with the underrating gap (r = .435, p < .001), "
        "translanguaging exposure (TL_percent; r = .332, p < .001), and perceived underrating "
        "(r = .290, p = .001). Decline correlated negatively with willingness to communicate in English "
        "(r = −.259, p = .004) and English self-efficacy (r = −.352, p < .001). Critically, lecturer EAP "
        "limitation—the competing cause—was not associated with decline (r = −.029, p = .757), although it "
        "was associated with translanguaging exposure (r = .435). Decline did not differ reliably by major "
        "(ANOVA F = 0.51, p = .604) or gender (Welch t = 0.58, p = .565)."
    )

    add_caption(doc, "Table 3. Correlations between mechanism predictors and overall decline")
    t3 = doc.add_table(rows=1, cols=4)
    fill_header_row(t3.rows[0], ["Predictor", "r", "p", "Interpretive role"])
    for row in [
        ("Underrating_Gap", ".435", "<.001", "Golem: inaccuracy"),
        ("TL_percent", ".332", "<.001", "Treatment: L1 exposure"),
        ("PU_mean", ".290", ".001", "Student-perceived underrating"),
        ("EAP_mean", "−.029", ".757", "Competing cause (not Golem)"),
        ("WTC_mean", "−.259", ".004", "Internalization"),
        ("SE_mean", "−.352", "<.001", "Internalization"),
    ]:
        cells = t3.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = val
    set_table_style(t3)
    add_para(doc, "", first_indent=False, space_after=6)

    add_heading_styled(doc, "Regression models", level=2)
    add_para(
        doc,
        "Three OLS models predicted overall decline. Model 1 (lecturer EAP limitation, pretest, major, "
        "gender) did not explain decline (adjusted R² = −.022; EAP_mean b = −0.05, p = .951). Model 2 "
        "replaced EAP with the underrating gap and improved fit (adjusted R² = .159; Underrating_Gap "
        "b = 0.54, p < .001). Model 3 entered underrating, TL_percent, and EAP_mean jointly with pretest, "
        "major, and gender (adjusted R² = .192). In the joint model, underrating (b = 0.35, p = .010) and "
        "translanguaging exposure (b = 0.16, p = .012) remained significant, whereas EAP_mean did not "
        "(b = −1.06, p = .190). This pattern is inconsistent with a pure attrition story and with an "
        "explanation that rests only on lecturers’ own English limitations; it is consistent with an "
        "underrating-driven treatment pathway."
    )

    add_caption(doc, "Table 4. Key coefficients from OLS models predicting Decline_Overall")
    t4 = doc.add_table(rows=1, cols=5)
    fill_header_row(t4.rows[0], ["Model", "Predictor", "b", "p", "Note"])
    for row in [
        ("1 EAP-only", "EAP_mean", "−0.05", ".951", "Competing cause alone"),
        ("2 Underrating", "Underrating_Gap", "0.54", "<.001", "Inaccuracy path"),
        ("3 Full", "Underrating_Gap", "0.35", ".010", "With TL + EAP + covariates"),
        ("3 Full", "TL_percent", "0.16", ".012", "Treatment path"),
        ("3 Full", "EAP_mean", "−1.06", ".190", "Not significant in joint model"),
    ]:
        cells = t4.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = val
    set_table_style(t4)
    add_para(
        doc,
        "Note. Models also included Pre_Overall, major, and gender. Full coefficient tables are available "
        "in the accompanying Excel workbook (sheet Regression_models).",
        first_indent=False,
        italic=True,
        size=9,
        space_after=12,
    )

    add_heading_styled(doc, "Mediation and lecturer-level checks", level=2)
    add_para(
        doc,
        "A conventional Sobel mediation check for underrating → translanguaging → decline yielded an "
        "indirect effect of 0.096 (Sobel z = 1.74, p = .082), with a remaining direct effect of underrating "
        "on decline (c′ = 0.447). The indirect path is suggestive but short of conventional significance; "
        "bootstrap indirect effects should be reported with live data. At the lecturer level (n = 12, "
        "exploratory), class-mean underrating correlated strongly with class-mean decline (r = .823, "
        "p = .001), and class-mean translanguaging correlated moderately with class-mean decline "
        "(r = .575, p = .050). The one-way ICC of student decline by lecturer was .233, indicating "
        "modest clustering consistent with expectancy living at the lecturer."
    )

    add_heading_styled(doc, "Summary of the quantitative pattern", level=2)
    add_para(
        doc,
        "Across four years of engineering EMI, completers showed a small overall decline in institutional "
        "academic English that was just statistically significant and larger in Writing and Speaking than "
        "in Listening and Reading. Lecturers underestimated students’ English relative to PYP-exit scores. "
        "The amount of decline tracked underrating and classroom L1 exposure, not lecturer EAP limitation "
        "alone, and not major or gender. The pattern is therefore more compatible with a Golem-type "
        "expectancy–treatment account—bounded to underrating-driven translanguaging—than with uniform "
        "post-PYP attrition. Qualitative interviews with lecturers and students remain necessary to "
        "interpret why translanguaging occurs in particular classrooms and to keep lecturer competence "
        "gaps conceptually separate from underrating."
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
