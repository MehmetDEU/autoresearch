# Research roadmap (brainstorming → study)

Working title: **English-Medium Instruction and Oral–Aural Attrition**  
Design: **explanatory sequential mixed methods** (QUANT → QUAL)

---

## Core claim (one paragraph)

Engineering EMI students sit the same institutional English test at **PYP exit (pre)** and **graduation (post)**. **Listening and Speaking** decline; **Reading and Writing** do not, because coursework is more **EAP / written-discourse dependent** than spoken **ELFA**-style interaction. We then ask **what this oral–aural attrition is attributed to**, mainly through **students**, with a short focused **lecturer** interview. Two explanations stay separate: (1) lecturers’ **limited English** for sustained EMI teaching, and (2) a **Golem effect** — lecturers presuppose that students are not proficient enough, so translanguaging and Turkish become the safe way to protect content when L1 is shared. Spoken English thins out, and oral–aural skills erode over four years.

---

## Phase 0 — Lock the frame (now)

| Step | Decision | Status |
| --- | --- | --- |
| 0.1 | Confirm design: QUANT first (pre/post), then QUAL (attribution) | Locked |
| 0.2 | Confirm skill pattern: L+S decline; R+W stable / slight gain | Locked in synthetic panel |
| 0.3 | Explanatory focus: translanguaging practice; motives = lecturer English **or** Golem underrating | Locked |
| 0.4 | Lecturer role: **short focused interview** (Golem expectancy has to be heard from lecturers) | Locked |
| 0.5 | Write / refresh lit review later (not blocking roadmap) | Pending |

### Lecturer interview (short, but required)

Student interviews stay primary for the experience of attrition. Lecturer interviews are short, not optional, because the Golem expectancy is a lecturer-held presupposition.

About five or six questions:

1. How often do you use Turkish in EMI classes?
2. Why? (content security, student level, your own English, time, materials)
3. How proficient do you judge your students’ English to be for EMI content?
4. What would be lost if the class stayed in English?
5. Does sharing Turkish as L1 change that judgment?

A longer lecturer study is unnecessary unless those answers diverge sharply.

---

## Phase 1 — Quantitative (RQ1)

**Purpose:** Establish *that* oral–aural attrition occurs (and written skills do not).

**RQ1.** To what extent do Listening, Reading, Writing, Speaking, and Overall change from PYP exit to graduation?

| Step | Task | Output |
| --- | --- | --- |
| 1.1 | Keep / replace synthetic *N* = 120 panel with live institutional Pre/Post | Excel / SPSS / R |
| 1.2 | Descriptives (0–100; threshold 60) | Table 1 |
| 1.3 | Paired *t* (+ Wilcoxon), *d_z*, 95% CIs by skill | Table 2 |
| 1.4 | One figure: Pre vs Post means by skill | Figure 1 |
| 1.5 | Brief instrument note (parallel forms, raters for W/S) | Methods |

**Stop here for QUANT.** No regressions/mediation required for the story you outlined.

**Scaffolding locked on this branch** (slim workbook + Methods/Results with Nicol Play-It-Safe Tables 1–2 + sole Figure 1). Lead analysis = paired *t* (not MANOVA/RM-ANOVA); see `STATISTICAL_AND_FIGURE_DECISIONS.md`. Ready for Phase 2 QUAL.

---

## Phase 2 — Qualitative attribution (RQ2–RQ3)

**Purpose:** Ask students what they attribute oral–aural attrition to. Then a prepared follow-up on frequent lecturer L1, expected from the researcher’s observation over years. Then ask lecturers what underlies their own L1 use. A Golem reading applies only if they cite students’ proficiency.

### Research questions

**RQ2 (students).** To what do students attribute their oral–aural attrition?

**Follow-up in the semi-structured guide (not an RQ).** *Why do you think lecturers use Turkish so often?* Prepared in advance from observation over years. Ask it after the open answer. If the student already mentioned L1, tie it to their words. If not, ask it anyway and report it as planned. Two anticipated accounts only: lecturers’ limited English, and underrating of students’ English. Content security and shared L1 belong inside the second, not as a third theme.

**RQ3 (lecturers).** When lecturers use L1, what do they say underlies that use? Expected answer, from observation: students’ low proficiency only. That answer is tied to the Golem effect.

### Working themes for RQ2 (students)

Keep three themes. Do not split written discourse from multimodality unless students talk about them as different reasons.

| Theme | What it covers | Not a separate theme |
| --- | --- | --- |
| **Lecturer L1 / translanguaging** | Too frequent Turkish in class; little spoken English | Factors *inside* this theme, from 2b: lecturer’s own English; students assumed too weak (Golem only if lecturers later say so); content security; materials too hard in English |
| **Written technical discourse** | Content carried by notes, problems, reports, textbooks | Inside the explanation: those texts are multimodal (diagrams, formulae, slides, figures). Same job as writing: meaning without extended speech |
| **Peer talk in Turkish** | Labs, groups, and study talk also in L1, not only the lecturer’s speech | Worth keeping if students raise it. Oral–aural attrition then sits in the whole interaction, not only in the lecture |

Assessment can stay inside the written-discourse theme: exams and reports do not require spoken English, so Listening and Speaking are not practised and Reading and Writing are.

### Student data plan

| Step | Task |
| --- | --- |
| 2.1 | Sampling: purposive from completers (vary major; include clear L/S decliners if IDs linkable) |
| 2.2 | Protocol: semi-structured interview or open questionnaire |
| 2.3 | Semi-structured. Open with RQ2. Then the prepared follow-up: “Why do you think lecturers use Turkish so often?” Expected from the researcher’s observation; not a second RQ. Listen also for written/visual technical work and peer talk in Turkish |
| 2.4 | Analysis: thematic analysis (Braun & Clarke or similar) |
| 2.5 | Joint display: QUANT skill pattern ↔ QUAL themes (explanatory integration) |

### Lecturer data plan (choose one)

| Option | Effort | What you get |
| --- | --- | --- |
| **A. Short probe (recommended)** | Low | Frequency/reasons for translanguaging + perception of student proficiency |
| **B. No lecturer data** | Lowest | Student-only attribution; still workable if student themes are rich |
| **C. Full interviews** | High | Deeper lecturer voice; only if Option A is too thin |

---

## Phase 3 — Integration & writing

| Step | Task |
| --- | --- |
| 3.1 | Integration statement: QUANT shows L/S loss; QUAL attributes it to translanguaging ecology driven by (A) lecturer English limits and/or (B) underrating |
| 3.2 | Theoretical note: EAP-heavy written demands protect R/W; spoken EMI (ELFA-like interaction) is under-practised |
| 3.3 | Literature review / introduction (build once RQs + theme map are stable) |
| 3.4 | Discussion: do not overclaim causal Golem statistics; keep underrating as **qualitative** explanation unless you later reintroduce measures |
| 3.5 | Limitations: synthetic → live scores; self-report; single faculty |

---

## Suggested sequence (practical)

1. **This week (brainstorm lock):** choose lecturer Option A/B/C; freeze RQ wording.  
2. **Quant polish:** keep Phase 1 tables/figure; swap in real scores when available.  
3. **Draft student interview guide** (10–12 questions).  
4. **Draft lecturer short probe** (3 questions) *or* skip.  
5. **Pilot 2–3 students** → refine themes.  
6. **Full QUAL collection + coding.**  
7. **Lit review + full manuscript** around the integrated story.

---

## What we already have vs what is next

| Have | Next |
| --- | --- |
| RQ frame + synthetic Pre/Post pattern | Live scores when possible |
| Methods + QUANT results draft | Student interview guide + sample |
| Fig 1 Pre/Post | Lecturer short probe (optional) |
| No lit review yet | Theme codebook; then lit review |

---

## One-page decision checklist

- [ ] Lecturer role: **A short probe** / **B none** / **C full interviews**
- [ ] Student mode: interview / open questionnaire / both
- [ ] Keep underrating as **QUAL theme only** (recommended) or revive QUANT measures later
- [ ] Explicit EAP vs spoken-interaction framing for why R/W hold
- [ ] Ethics / consent path for live data
