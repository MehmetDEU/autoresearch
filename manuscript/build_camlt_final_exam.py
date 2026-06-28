#!/usr/bin/env python3
"""Build CAMLT final exam and answer key on Desktop."""

from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

DESKTOP = Path.home() / "Desktop"
EXAM_PATH = DESKTOP / "CAMLT_Final_Test.docx"
KEY_PATH = DESKTOP / "CAMLT_Final_Test_Answer_Key.docx"

FONT = "Times New Roman"
SIZE = Pt(11)


def set_run_font(run, *, bold: bool = False, italic: bool = False) -> None:
    run.font.name = FONT
    run.font.size = SIZE
    run.bold = bold
    run.italic = italic
    run._element.rPr.rFonts.set(qn("w:eastAsia"), FONT)


def add_para(
    doc: Document,
    text: str = "",
    *,
    bold: bool = False,
    italic: bool = False,
    align=WD_ALIGN_PARAGRAPH.LEFT,
    space_before: float = 0,
    space_after: float = 3,
) -> None:
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.05
    if text:
        run = p.add_run(text)
        set_run_font(run, bold=bold, italic=italic)


def add_mixed(
    doc: Document,
    parts: list[tuple[str, bool, bool]],
    *,
    space_before: float = 0,
    space_after: float = 3,
) -> None:
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.05
    for text, bold, italic in parts:
        run = p.add_run(text)
        set_run_font(run, bold=bold, italic=italic)


def add_answer_lines(doc: Document, count: int = 3) -> None:
    for _ in range(count):
        add_para(doc, "________________________________________________________________________", space_after=2)


def configure_doc(doc: Document) -> None:
    section = doc.sections[0]
    section.top_margin = Cm(2)
    section.bottom_margin = Cm(2)
    section.left_margin = Cm(2.5)
    section.right_margin = Cm(2.5)
    style = doc.styles["Normal"]
    style.font.name = FONT
    style.font.size = SIZE
    style._element.rPr.rFonts.set(qn("w:eastAsia"), FONT)


def add_header_block(doc: Document) -> None:
    add_para(doc, "Kocaeli University Faculty of Education TEFL Dept.", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    add_para(
        doc,
        "Final Test for Current Approaches and Methods in Language Teaching",
        bold=True,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        space_after=8,
    )
    add_para(doc, "Date: 17/06/2026     Duration: 75 minutes     Total: 100 points", space_after=4)
    add_para(doc, "Student's Name: ________________________________     Surname: ________________________________", space_after=2)
    add_para(doc, "Student ID No.: ________________________________", space_after=8)


def build_exam() -> None:
    doc = Document()
    configure_doc(doc)
    add_header_block(doc)

    add_para(
        doc,
        "Instructions. Answer all parts. Write clearly in full sentences unless a list is requested. "
        "Use course terminology.",
        space_after=8,
    )

    add_para(doc, "1. English Medium Instruction (40 points)", bold=True, space_after=4)

    add_para(
        doc,
        "1.a (8 points) Briefly state Macaro's (2018) and McKinley's definitions of EMI. "
        "How do they differ from one another?",
        space_after=3,
    )
    add_answer_lines(doc, 2)

    add_para(
        doc,
        "1.b (12 points) Macaro's five EMI models are described below. Write the correct model name "
        "for each description (2 points each).",
        space_before=4,
        space_after=2,
    )
    for i, text in enumerate(
        [
            "Students must meet required English proficiency before entering EMI programmes.",
            "Students complete an intensive English bridging year before subject courses begin.",
            "All eligible content students enter EMI; ongoing EAP/ESP support runs alongside subject courses.",
            "Some courses or sessions are in English, some in L1, or teachers switch languages within a lesson.",
            "Institutional leaders and teachers ignore EMI problems and provide no planned language support.",
        ],
        start=1,
    ):
        add_para(doc, f"{i}. {text}", space_after=1)
        add_para(doc, "   Model: ________________________________", space_after=3)

    add_para(
        doc,
        "1.c (8 points) Classify each subject as Hard EMI (H) or Soft EMI (S). Write H or S in the blank "
        "(2 points each).",
        space_before=4,
        space_after=2,
    )
    for i, subject in enumerate(
        [
            "Medicine",
            "Applied Linguistics",
            "Engineering",
            "TESOL",
            "History of Art",
            "Second Language Acquisition",
        ],
        start=1,
    ):
        add_para(doc, f"{i}. {subject}     (H / S): __________", space_after=1)

    add_mixed(
        doc,
        [
            ("1.d (12 points) Compare EMI and CLIL. State at least ", False, False),
            ("two", True, False),
            (" clear differences. You may refer to primary focus, language goal, typical setting, or learner profile.", False, False),
        ],
        space_before=4,
        space_after=3,
    )
    add_answer_lines(doc, 4)

    add_para(doc, "2. Task-Based Language Teaching (35 points)", bold=True, space_before=8, space_after=4)
    add_para(
        doc,
        "What are the five design features of a task in TBLT? List all five and briefly explain each "
        "(7 points each).",
        space_after=4,
    )
    for i in range(1, 6):
        add_para(doc, f"{i}. ________________________________________________________________________", space_after=1)
        add_para(doc, "________________________________________________________________________", space_after=1)
        add_para(doc, "________________________________________________________________________", space_after=4)

    add_para(doc, "3. Content-Based Instruction (25 points)", bold=True, space_before=8, space_after=4)
    add_para(
        doc,
        "Describe the three main CBI models taught in this course. For each model, explain how it works, "
        "who teaches, and the primary goal (about 4-5 sentences per model).",
        space_after=4,
    )
    for label, name in [
        ("a.", "Theme-based model"),
        ("b.", "Sheltered model"),
        ("c.", "Adjunct model"),
    ]:
        add_mixed(doc, [(f"{label} ", True, False), (f"({name}) ", False, True)], space_after=2)
        add_answer_lines(doc, 4)

    add_para(doc, "End of Test", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=10)
    doc.save(EXAM_PATH)


def build_answer_key() -> None:
    doc = Document()
    configure_doc(doc)

    add_para(doc, "Kocaeli University Faculty of Education TEFL Dept.", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    add_para(
        doc,
        "Final Test Answer Key — Current Approaches and Methods in Language Teaching",
        bold=True,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        space_after=4,
    )
    add_para(
        doc,
        "Date: 17/06/2026     Duration: 75 minutes     Total: 100 points",
        align=WD_ALIGN_PARAGRAPH.CENTER,
        space_after=2,
    )
    add_para(
        doc,
        "INSTRUCTOR COPY — DO NOT DISTRIBUTE",
        bold=True,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        space_after=8,
    )

    add_para(doc, "1. English Medium Instruction (40 points)", bold=True, space_after=4)

    add_para(doc, "1.a Macaro vs McKinley definitions (8 points)", bold=True, space_after=2)
    add_para(
        doc,
        "Macaro (2018): the use of English to teach academic subjects (other than English itself) in "
        "countries or jurisdictions where the L1 of the majority of the population is not English.",
        space_after=2,
    )
    add_para(
        doc,
        "McKinley (Rose & McKinley, 2018): an educational system in which content is taught through "
        "English in contexts where English is not the primary, first, or official language; often "
        "linked to internationalisation of higher education.",
        space_after=2,
    )
    add_para(
        doc,
        "Sample differences (award 4 pts per clear contrast, any two): Macaro specifies academic "
        "subjects other than English and restricts EMI to non-Anglophone jurisdictions by majority L1; "
        "McKinley defines EMI as an educational system and refers to English not being the "
        "primary/first/official language in the context; McKinley explicitly ties EMI to "
        "internationalisation/globalisation policy, whereas Macaro's definition is framed for "
        "comparative research across non-Anglophone settings. Partial credit for one accurate "
        "definition plus one difference.",
        space_after=6,
    )

    add_para(doc, "1.b EMI model names (12 points; 2 points each)", bold=True, space_after=2)
    add_para(doc, "1. Selection Model", space_after=1)
    add_para(doc, "2. Preparatory Year Model", space_after=1)
    add_para(doc, "3. Concurrent Support Model", space_after=1)
    add_para(doc, "4. Multilingual Model (accept Partial EMI Model)", space_after=1)
    add_para(doc, "5. Ostrich Model", space_after=2)
    add_para(doc, "Award 2 pts per correct model name.", space_after=6)

    add_para(doc, "1.c Hard / Soft EMI (2 points each; 3 Hard, 3 Soft)", bold=True, space_after=2)
    add_para(doc, "1. H  2. S  3. H  4. S  5. H  6. S", space_after=2)
    add_para(
        doc,
        "Hard EMI: discipline not inherently tied to English. Soft EMI: discipline linked to English.",
        space_after=6,
    )

    add_para(doc, "1.d EMI vs CLIL (12 points; 6 points per clear difference)", bold=True, space_after=2)
    add_para(
        doc,
        "Sample differences: (1) Primary focus: EMI = academic content through English with language "
        "development not the main intended outcome; CLIL = explicit dual focus on content and additional "
        "language. (2) Setting: EMI common in higher education in non-Anglophone contexts; CLIL common in "
        "school/bilingual programmes, often linked to European policy. (3) Language goal: EMI does not "
        "primarily aim at language learning; CBI/CLIL often include language objectives. Accept any two "
        "well-explained contrasts.",
        space_after=8,
    )

    add_para(doc, "2. TBLT task design features (35 points; 7 each)", bold=True, space_after=2)
    add_para(
        doc,
        "Expected features (any order): Goal, Input, Conditions, Procedures, Predicted outcomes.",
        space_after=2,
    )
    features = [
        "Goal: the general purpose of the task (prediction, ordering, problem-solving, etc.).",
        "Input: the data or material learners use (texts, maps, pictures, audio, etc.).",
        "Conditions: how information is distributed and how learners interact (split/shared information, roles, time limits).",
        "Procedures: the steps or operations learners carry out and the interaction pattern (pair, group, individual).",
        "Predicted outcomes: what learners should know, do, or produce by the end; may be open or closed.",
    ]
    for item in features:
        add_para(doc, item, space_after=2)
    add_para(doc, "Award about 2 pts for correct name and 5 pts for accurate explanation per feature.", space_after=8)

    add_para(doc, "3. CBI models (25 points; about 8-9 each)", bold=True, space_after=4)

    add_para(doc, "a. Theme-based model", bold=True, space_after=2)
    add_para(
        doc,
        "Syllabus organised around themes/topics in a language class; language functions and structures "
        "selected to fit the theme; language learning is the ultimate goal; typical in language classrooms "
        "at school or university.",
        space_after=4,
    )

    add_para(doc, "b. Sheltered model", bold=True, space_after=2)
    add_para(
        doc,
        "A content specialist teaches an academic subject to ESL learners; language is modified so learners "
        "can access content; primary goal is subject-matter learning with language as medium; common in "
        "university or secondary ESL contexts.",
        space_after=4,
    )

    add_para(doc, "c. Adjunct model", bold=True, space_after=2)
    add_para(
        doc,
        "A language course runs parallel to a content course; topics align; language teachers support learners "
        "in understanding content; often used in immersion programmes; requires coordination between language "
        "and content instructors.",
        space_after=8,
    )

    add_para(doc, "Score summary: Q1 ___/40   Q2 ___/35   Q3 ___/25   Total ___/100", bold=True, space_after=4)

    doc.save(KEY_PATH)


def main() -> None:
    build_exam()
    build_answer_key()
    print(f"Wrote {EXAM_PATH}")
    print(f"Wrote {KEY_PATH}")


if __name__ == "__main__":
    main()
