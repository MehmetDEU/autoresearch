"""Authored supervisor notes (Mehmet Altay) for the thesis.

Each entry: (pdf_page_1based, (x, y) anchor in page coords, content)

Anchors are placed where the issue actually appears on the page. Coordinates
were chosen by reading the per-page text and finding a stable column. PDF
coords are top-left origin (PyMuPDF convention via page.rect).
"""

NOTES = [
    # ---- Front matter / abstract ----
    (8, (540, 360),
     "Abstract reports the Syrian NNS share (59%) but switches to the Turkish "
     "NS share (60% / 41% NS). Same comparison, two different speakers. Make "
     "the two sentences parallel."),

    (11, (540, 130),
     "Only one figure across the whole research? With Tables 7-13 you have "
     "plenty of frequency data; at least two or three bar charts are expected."),

    (12, (540, 200),
     "Three slips on a single page: 'resaearch', 'reveald', 'witthin'. The "
     "abstract of a thesis cannot read like this."),

    # ---- Chapter I background and statement of problem ----
    (14, (540, 200),
     "Crystal 2003, Graddol 1997, Kachru 1985, Seidlhofer 2011. Twenty- to "
     "forty-year-old sources to justify a 2026 claim. Where is Galloway & "
     "Rose, Sifakis, Bayyurt of the last five years?"),

    (15, (540, 470),
     "If you accept (in your own note below on p.13) that Kachru's three "
     "circles are out-of-date, you must say so here too, before you build the "
     "whole rationale on it. Criticising it later is not coherent."),

    (16, (540, 600),
     "You quote Vettorel & Lopriore on 'fake foreign accents', but you do not "
     "analyse any audio in this thesis. Either rephrase or admit in 6.3 that "
     "this claim is not testable with your corpus."),

    (18, (540, 200),
     "Two student books from two countries cannot speak for 'Türkiye and Syria' "
     "as wholes. Soften the aim accordingly, otherwise the committee will."),

    (19, (540, 220),
     "Your SC/TC/IC follow Cortazzi & Jin 1999 letter-by-letter. A Syrian "
     "student chatting on social media with a Japanese friend fits none of the "
     "three. Address this here, not in 6.3."),

    (20, (540, 240),
     "If 'locally produced' is the boundary, also state edition year, print "
     "run and revision. Your Syrian book is 2021-2026 and the Turkish one "
     "2024-2029. They are not contemporaneous and that affects comparison."),

    # ---- Chapter II literature review ----
    (21, (540, 360),
     "Asian, European, Middle Eastern. Why nothing from Latin America or "
     "Africa? Your 'global' gap excludes half of the Expanding Circle."),

    (23, (540, 200),
     "Holliday 2005, Cook 1999, Phillipson 1992, Widdowson 1994. The same "
     "'current debate' since I was a student. Bring in the last decade."),

    (25, (540, 130),
     "Why Cortazzi & Jin and not Risager's transnational paradigm or "
     "Holliday's small-culture approach? One sentence of selection criteria "
     "is enough, but it must be there."),

    (28, (540, 280),
     "Mark this list: S5 Appeal for Help, S6 Correction, S7 Fillers, S8 "
     "Approximation, S9 Circumlocution, S10 Code-switching. On p.46 (4.6.1) "
     "you call S8 Circumlocution and S9 Expansion. Same codes, two different "
     "definitions. Fix this before defence."),

    (30, (540, 360),
     "Three Middle-Eastern sources for an entire regional section? Lebanon, "
     "Jordan, Gulf, KSA studies are easy to find. Expand or rename the "
     "subheading."),

    (36, (540, 360),
     "Your 'no research in Syria' claim relies on Google Scholar, ERIC, "
     "Scopus and WoS searches. Without search strings, date range and "
     "screening protocol it is a personal claim, not a systematic search."),

    # ---- Chapter III methodology ----
    (37, (540, 360),
     "Document analysis is not synonymous with 'reading the books carefully'. "
     "Tie Bowen 2009's six steps explicitly to your procedure here."),

    (38, (540, 130),
     "Self-described as qualitative but Chapter IV is almost entirely "
     "frequency tables. This is descriptive-quantitative with a qualitative "
     "wrapper. Reposition the design or add genuine qualitative depth."),

    (41, (540, 130),
     "Emar 12th grade, Literary Section only. The Scientific Section book is "
     "outside your corpus. Title and aim must reflect this restriction, "
     "otherwise the claim is overreach."),

    (43, (540, 130),
     "You say visual content was coded for cultural cues. Where is the visual "
     "coding rubric? Without it the image part of your analysis is not "
     "replicable."),

    (44, (540, 360),
     "Thirty-minute briefing for a 114-row stratified sample is thin. Who is "
     "the second coder, Yeşim Aşuroğlu from your acknowledgements? What is "
     "her field background? Was the briefing recorded? The defence will ask."),

    (45, (540, 600),
     "Landis & Koch 1977 benchmarks are convenient but contested; McHugh 2012 "
     "calls them too liberal. Report Krippendorff's α alongside κ."),

    (47, (540, 360),
     "No ethics committee approval is fine. But fair-use of textbook excerpts "
     "in Chapter IV still requires one explicit line on copyright / MoNE "
     "permission."),

    # ---- Chapter IV findings ----
    (50, (540, 480),
     "IC > 50%, NS 40-60%, S5-S10 presence. These three thresholds are yours. "
     "Cite a source or label them 'researcher-defined criteria' here."),

    (51, (540, 130),
     "Your 41%/59% Syrian and 60%/40% Turkish figures exclude 28 and 22 "
     "'uncertain' speakers respectively. That is around a quarter thrown out. "
     "Flag this where Table 7 is interpreted, not only later."),

    (53, (540, 600),
     "78 references in the Syrian book vs 121 in the Turkish one. Normalise "
     "by total pages or word count before saying anything is 'similar'. "
     "Otherwise you are comparing absolute counts on books of different size."),

    (54, (540, 600),
     "Only one SC excerpt per book is quoted (Nizar Qabbani, Atatürk/Kızılay). "
     "With 12 and 15 SC items respectively you can afford a fuller sample so "
     "the reader can verify the coding."),

    (56, (540, 600),
     "Monica, Chandler, Phoebe, Joey, Ross are sitcom characters coded as NS "
     "from the show's nationality. Spell out the rule: do fictional or "
     "transposed characters count as NS in the same way as real speakers?"),

    (56, (540, 420),
     "28% of Syrian speakers and 25% of Turkish ones are 'uncertain'. That is "
     "not a residual; it is a finding about textbook authorship. Devote a "
     "paragraph to it."),

    (58, (540, 200),
     "Here S8 is Circumlocution and S9 is Expansion. On p.16 the same codes "
     "are Approximation and Circumlocution. Settle on one set, then recompute "
     "Table 13 if anything moves."),

    # ---- Chapter V discussion ----
    (60, (540, 360),
     "Comparing a 2024 MoNE book with a 2021-2026 Syrian Ministry book "
     "treats the two contexts as symmetric. Wartime / post-war Syria, "
     "different teacher-training systems, different revision cycles. This "
     "belongs in the discussion, not buried in 6.3."),

    (62, (540, 600),
     "You blame 'international publishing policies' for locally produced "
     "books. There is a missing step: how exactly do those policies reach "
     "into MoNE / Syrian Ministry writing teams? Evidence it or drop it."),

    # ---- Chapter VI conclusion ----
    (70, (540, 360),
     "Limitations are too short. Add at least: single second coder, Student's "
     "Book only, no audio analysis, no teacher/learner perception data, no "
     "negative-case analysis. You hint at these earlier; collect them here."),

    (70, (540, 460),
     "Did you encounter items that did not fit any code? Negative cases are "
     "usually the most informative. They are missing from your account."),

    (71, (540, 540),
     "Pedagogical implications are still generic. Tie each one to a specific "
     "finding: e.g., because S10 (Code-switching) is 0% in Module 3 of Emar, "
     "recommend the exact task type to supplement it with."),

    (71, (540, 620),
     "Split your original contribution into three lines: empirical (first "
     "Syrian textbook ELF analysis), methodological (Yuen 4P combined with "
     "the Vettorel/Yağar inventory), theoretical (whatever you actually "
     "argue, name it explicitly)."),
]
