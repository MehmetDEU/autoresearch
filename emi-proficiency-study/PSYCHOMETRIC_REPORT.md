# Psychometric and inferential report

> **Synthetic panel** (N = 120 completers). Generated for instrument testing and paper scaffolding. Do not treat as empirical findings.

- Random seed: `20261004`
- Gender: 82 male (68.3%), 38 female
- Majors: Mechanical Engineering n=40, Chemical Engineering n=40, Electrical-Electronics Engineering n=40
- Age at graduation: 22–25 (age at PYP exit = graduation age − 4)
- All pretest overall scores ≥ 60 (B1 institutional threshold): **True** (min = 60.1)
- Posttest scores below 60: **14** students (possible fall below B1 after four EMI years)

## 1. Why the test is paired, not independent

The same 120 students sat parallel forms four years apart. The correct test is a **paired-samples *t*-test** (and Wilcoxon signed-rank as a distribution-free companion). An independent-samples *t*-test would treat pre and post as unrelated groups and is the wrong model.

Paired *t* assumes that **difference scores** are approximately normal, not that the raw totals are normal. Raw totals are truncated at 60 on the pretest, so they can look skewed; that is expected.

## 2. Descriptive statistics and distributional checks

| Variable | n | M | SD | Min | Max | Skew | Excess kurtosis | Shapiro–Wilk W | p |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Pre_Listening | 120 | 68.54 | 5.08 | 57.5 | 79.2 | -0.05 | -0.76 | 0.984 | .183 |
| Pre_Reading | 120 | 67.81 | 5.43 | 56.8 | 81.4 | 0.20 | -0.39 | 0.987 | .320 |
| Pre_Writing | 120 | 67.23 | 5.80 | 55.7 | 83.7 | 0.18 | -0.36 | 0.979 | .054 |
| Pre_Speaking | 120 | 66.60 | 5.38 | 55.1 | 79.9 | 0.10 | -0.58 | 0.984 | .151 |
| Pre_Overall | 120 | 67.55 | 4.85 | 60.1 | 79.0 | 0.13 | -0.84 | 0.962 | .002 |
| Post_Listening | 120 | 68.04 | 5.46 | 55.1 | 83.6 | 0.35 | 0.05 | 0.988 | .382 |
| Post_Reading | 120 | 67.19 | 6.55 | 54.4 | 85.2 | 0.54 | 0.07 | 0.974 | .022 |
| Post_Writing | 120 | 66.09 | 8.02 | 52.2 | 88.0 | 0.54 | -0.14 | 0.972 | .012 |
| Post_Speaking | 120 | 65.47 | 7.63 | 49.6 | 84.5 | 0.56 | -0.17 | 0.964 | .003 |
| Post_Overall | 120 | 66.70 | 6.39 | 54.2 | 84.2 | 0.63 | 0.05 | 0.965 | .003 |
| Decline_Overall | 120 | 0.85 | 4.67 | -12.5 | 9.3 | -0.17 | -0.58 | 0.980 | .069 |
| Underrating_Gap | 120 | 8.44 | 3.74 | 1.4 | 18.6 | 0.39 | -0.10 | 0.981 | .097 |
| TL_percent | 120 | 38.45 | 8.57 | 19.0 | 62.2 | 0.38 | -0.31 | 0.981 | .095 |
| PU_mean | 120 | 3.07 | 0.69 | 1.2 | 4.8 | 0.06 | -0.21 | 0.988 | .369 |
| TL_mean | 120 | 3.30 | 0.61 | 1.8 | 4.6 | -0.00 | -0.51 | 0.975 | .026 |
| EAP_mean | 120 | 3.14 | 0.72 | 1.6 | 4.8 | -0.01 | -0.50 | 0.984 | .160 |
| WTC_mean | 120 | 3.87 | 0.70 | 2.0 | 5.0 | -0.44 | -0.52 | 0.962 | .002 |
| SE_mean | 120 | 3.86 | 0.72 | 2.2 | 5.0 | -0.36 | -0.68 | 0.960 | .001 |
| Lecturer_Est_English | 120 | 59.11 | 5.46 | 48.0 | 73.8 | 0.28 | -0.12 | 0.988 | .405 |

Shapiro–Wilk on **overall difference scores**: W = 0.980, p = .069. Difference scores are compatible with normality, so the paired *t*-test is appropriate; Wilcoxon is still reported.

## 3. Pre–post change (primary inferential test)

| Skill | Pre M (SD) | Post M (SD) | Mean decline | 95% CI | t(119) | p | Wilcoxon p | d_z | d_av | n post < 60 |
|---|---|---|---:|---|---:|---|---|---:|---:|---:|
| Listening | 68.54 (5.08) | 68.04 (5.46) | 0.50 | [-0.08, 1.09] | 1.72 | .088 | .075 | 0.16 | 0.10 | 6 |
| Reading | 67.81 (5.43) | 67.19 (6.55) | 0.62 | [-0.03, 1.28] | 1.88 | .063 | .060 | 0.17 | 0.10 | 13 |
| Writing | 67.23 (5.80) | 66.09 (8.02) | 1.14 | [0.06, 2.23] | 2.08 | .039 | .037 | 0.19 | 0.16 | 30 |
| Speaking | 66.60 (5.38) | 65.47 (7.63) | 1.14 | [0.04, 2.23] | 2.06 | .042 | .039 | 0.19 | 0.17 | 25 |
| Overall | 67.55 (4.85) | 66.70 (6.39) | 0.85 | [0.01, 1.69] | 2.00 | .048 | .039 | 0.18 | 0.15 | 14 |

**Headline:** overall proficiency declined by 0.85 points, t(119) = 2.00, p = .048, Cohen's d_z = 0.18 (small). Mean declines by skill: Listening 0.50, Reading 0.62, Writing 1.14, Speaking 1.14. A larger productive-skill drop is the pattern expected if students receive fewer English speaking/writing opportunities.

## 4. Reliability

Cronbach's α and McDonald's ω from section scores (Listening/Reading) or from the four IELTS-aligned rubric criteria (Writing/Speaking). Questionnaire scales are 5 Likert items (1–5).

| Scale | Items | Cronbach's α | McDonald's ω |
|---|---:|---:|---:|
| Pre_Listening_sections | 4 | 0.782 | 0.861 |
| Pre_Reading_sections | 4 | 0.794 | 0.866 |
| Post_Listening_sections | 4 | 0.846 | 0.897 |
| Post_Reading_sections | 4 | 0.875 | 0.914 |
| Perceived_underrating_PU | 5 | 0.849 | 0.894 |
| Translanguaging_Likert_TL | 5 | 0.878 | 0.912 |
| Lecturer_EAP_limitation | 5 | 0.885 | 0.916 |
| WTC_English | 5 | 0.854 | 0.896 |
| Self_efficacy_English | 5 | 0.871 | 0.908 |
| Pre_full_sections | 8 | 0.879 | 0.905 |
| Post_full_sections | 8 | 0.920 | 0.936 |
| Pre_Writing_criteria | 4 | 0.909 | 0.937 |
| Post_Writing_criteria | 4 | 0.956 | 0.968 |
| Pre_Speaking_criteria | 4 | 0.904 | 0.933 |
| Post_Speaking_criteria | 4 | 0.947 | 0.962 |

### Inter-rater reliability (Writing & Speaking)

Three independent marks (expert/author + two PYP instructors). ICC(2,1) = single-rater agreement; ICC(2,k) = reliability of the 3-rater mean (the official score).

| Facet | ICC(2,1) | ICC(2,k) |
|---|---:|---:|
| Writing_Pre | 0.901 | 0.965 |
| Writing_Post | 0.950 | 0.983 |
| Speaking_Pre | 0.906 | 0.966 |
| Speaking_Post | 0.941 | 0.979 |

## 5. Validity

### 5.1 Content validity (non-statistical, required in methods)

The institutional test uses the IELTS Academic skill split and the public IELTS band descriptors for Writing (Task Response, Coherence & Cohesion, Lexical Resource, Grammatical Range & Accuracy) and Speaking (Fluency & Coherence, Lexical Resource, Grammatical Range & Accuracy, Pronunciation). Listening and Reading use four sections each, mapped to IELTS Academic item types. Standard setting: 60/100 = B1 (institution policy). Pre and post forms share this blueprint (parallel forms; not identical items).

### 5.2 Concurrent validity vs IELTS Academic practice tests

A stratified subsample (n = 36; 12 per major) sat official IELTS Academic practice materials from ielts.org under exam conditions at PYP exit. Mapping used in generation: IELTS band ≈ 5.0 + (institutional − 60) × 0.05, plus small error, rounded to 0.5 bands.

| Institutional | IELTS | n | r | p |
|---|---|---:|---:|---|
| Pre_Overall | IELTS_Overall | 36 | 0.788 | <.001 |
| Pre_Listening | IELTS_Listening | 36 | 0.610 | <.001 |
| Pre_Reading | IELTS_Reading | 36 | 0.868 | <.001 |
| Pre_Writing | IELTS_Writing | 36 | 0.649 | <.001 |
| Pre_Speaking | IELTS_Speaking | 36 | 0.682 | <.001 |

### 5.3 Convergent structure

Pre-test skill intercorrelations (should be moderate-to-strong if they tap a common academic-English factor):

| Variable | Pre_Listening | Pre_Reading | Pre_Writing | Pre_Speaking | Pre_Overall |
|---|---|---|---|---|---|
| Pre_Listening | 1.000 | 0.775 | 0.715 | 0.721 | 0.891 |
| Pre_Reading | 0.775 | 1.000 | 0.750 | 0.748 | 0.913 |
| Pre_Writing | 0.715 | 0.750 | 1.000 | 0.709 | 0.891 |
| Pre_Speaking | 0.721 | 0.748 | 0.709 | 1.000 | 0.887 |
| Pre_Overall | 0.891 | 0.913 | 0.891 | 0.887 | 1.000 |

Post-test skill intercorrelations:

| Variable | Post_Listening | Post_Reading | Post_Writing | Post_Speaking | Post_Overall |
|---|---|---|---|---|---|
| Post_Listening | 1.000 | 0.825 | 0.742 | 0.750 | 0.881 |
| Post_Reading | 0.825 | 1.000 | 0.823 | 0.835 | 0.939 |
| Post_Writing | 0.742 | 0.823 | 1.000 | 0.846 | 0.934 |
| Post_Speaking | 0.750 | 0.835 | 0.846 | 1.000 | 0.937 |
| Post_Overall | 0.881 | 0.939 | 0.934 | 0.937 | 1.000 |

## 6. Mechanism (e): is the decline Golem-like or just attrition?

### 6.1 Inaccuracy of lecturer expectancy

Lecturers' estimates of students' English were lower than actual PYP-exit scores by 8.44 points (M_actual = 67.55, M_estimate = 59.11), t(119) = 24.75, p = <.001, d_z = 2.26. This is the inaccuracy criterion: the low expectation is not merely 'felt'; it is wrong relative to the institutional measure.

### 6.2 Correlations with decline (student level)

| Predictor | r with Decline_Overall | p | Role |
|---|---:|---|---|
| Underrating_Gap | 0.435 | <.001 | Golem: inaccuracy |
| TL_percent | 0.332 | <.001 | Treatment: L1 exposure |
| PU_mean | 0.290 | .001 | Student-perceived underrating |
| EAP_mean | -0.029 | .757 | Competing cause (not Golem) |
| WTC_mean | -0.259 | .004 | Internalization (lower WTC ↔ more decline) |
| SE_mean | -0.352 | <.001 | Internalization |

Mechanism intercorrelations:

| Variable | Decline_Overall | Underrating_Gap | TL_percent | PU_mean | EAP_mean | WTC_mean | SE_mean | Pre_Overall |
|---|---|---|---|---|---|---|---|---|
| Decline_Overall | 1.000 | 0.435 | 0.332 | 0.290 | -0.029 | -0.259 | -0.352 | 0.098 |
| Underrating_Gap | 0.435 | 1.000 | 0.456 | 0.535 | -0.076 | -0.590 | -0.508 | 0.213 |
| TL_percent | 0.332 | 0.456 | 1.000 | 0.404 | 0.435 | -0.668 | -0.454 | 0.094 |
| PU_mean | 0.290 | 0.535 | 0.404 | 1.000 | 0.045 | -0.375 | -0.305 | 0.092 |
| EAP_mean | -0.029 | -0.076 | 0.435 | 0.045 | 1.000 | -0.170 | -0.071 | 0.077 |
| WTC_mean | -0.259 | -0.590 | -0.668 | -0.375 | -0.170 | 1.000 | 0.364 | -0.174 |
| SE_mean | -0.352 | -0.508 | -0.454 | -0.305 | -0.071 | 0.364 | 1.000 | -0.069 |
| Pre_Overall | 0.098 | 0.213 | 0.094 | 0.092 | 0.077 | -0.174 | -0.069 | 1.000 |

### 6.3 Regression: does underrating survive controls?

**Model 1 — lecturer EAP limitation only (competing cause).** If decline were only about lecturers' own English, this would be the story.

```
                            OLS Regression Results                            
==============================================================================
Dep. Variable:        Decline_Overall   R-squared:                       0.021
Model:                            OLS   Adj. R-squared:                 -0.022
Method:                 Least Squares   F-statistic:                    0.4925
Date:                Sat, 03 Oct 2026   Prob (F-statistic):              0.781
Time:                        14:59:52   Log-Likelihood:                -353.30
No. Observations:                 120   AIC:                             718.6
Df Residuals:                     114   BIC:                             735.3
Df Model:                           5                                         
Covariance Type:            nonrobust                                         
==================================================================================================================
                                                     coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------------------------------------------
Intercept                                         -5.6706      6.402     -0.886      0.378     -18.352       7.011
C(Major)[T.Electrical-Electronics Engineering]     0.8387      1.101      0.762      0.448      -1.341       3.019
C(Major)[T.Mechanical Engineering]                -0.1640      1.413     -0.116      0.908      -2.964       2.636
C(Gender)[T.Male]                                  0.5920      0.943      0.628      0.531      -1.276       2.460
EAP_mean                                          -0.0501      0.815     -0.062      0.951      -1.665       1.564
Pre_Overall                                        0.0896      0.090      0.997      0.321      -0.088       0.268
==============================================================================
Omnibus:                        3.213   Durbin-Watson:                   1.574
Prob(Omnibus):                  0.201   Jarque-Bera (JB):                2.357
Skew:                          -0.183   Prob(JB):                        0.308
Kurtosis:                       2.420   Cond. No.                     1.01e+03
==============================================================================

Notes:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
[2] The condition number is large, 1.01e+03. This might indicate that there are
strong multicollinearity or other numerical problems.
```

**Model 2 — underrating gap.** Golem inaccuracy path.

```
                            OLS Regression Results                            
==============================================================================
Dep. Variable:        Decline_Overall   R-squared:                       0.195
Model:                            OLS   Adj. R-squared:                  0.159
Method:                 Least Squares   F-statistic:                     5.511
Date:                Sat, 03 Oct 2026   Prob (F-statistic):           0.000140
Time:                        14:59:52   Log-Likelihood:                -341.60
No. Observations:                 120   AIC:                             695.2
Df Residuals:                     114   BIC:                             711.9
Df Model:                           5                                         
Covariance Type:            nonrobust                                         
==================================================================================================================
                                                     coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------------------------------------------
Intercept                                         -4.1393      5.498     -0.753      0.453     -15.032       6.753
C(Major)[T.Electrical-Electronics Engineering]     0.7885      0.968      0.815      0.417      -1.129       2.706
C(Major)[T.Mechanical Engineering]                 0.5371      0.974      0.551      0.582      -1.393       2.467
C(Gender)[T.Male]                                  0.2725      0.849      0.321      0.749      -1.410       1.955
Underrating_Gap                                    0.5428      0.110      4.956      0.000       0.326       0.760
Pre_Overall                                       -0.0033      0.084     -0.039      0.969      -0.169       0.162
==============================================================================
Omnibus:                        2.591   Durbin-Watson:                   1.909
Prob(Omnibus):                  0.274   Jarque-Bera (JB):                2.465
Skew:                          -0.279   Prob(JB):                        0.292
Kurtosis:                       2.574   Cond. No.                         961.
==============================================================================

Notes:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
```

**Model 3 — underrating + translanguaging + EAP + pretest + major + gender.** Joint model. Golem claim is stronger if Underrating_Gap and/or TL_percent remain significant while EAP_mean weakens.

```
                            OLS Regression Results                            
==============================================================================
Dep. Variable:        Decline_Overall   R-squared:                       0.240
Model:                            OLS   Adj. R-squared:                  0.192
Method:                 Least Squares   F-statistic:                     5.040
Date:                Sat, 03 Oct 2026   Prob (F-statistic):           5.39e-05
Time:                        14:59:52   Log-Likelihood:                -338.16
No. Observations:                 120   AIC:                             692.3
Df Residuals:                     112   BIC:                             714.6
Df Model:                           7                                         
Covariance Type:            nonrobust                                         
==================================================================================================================
                                                     coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------------------------------------------
Intercept                                         -6.6051      5.823     -1.134      0.259     -18.142       4.932
C(Major)[T.Electrical-Electronics Engineering]     1.7346      1.038      1.672      0.097      -0.322       3.791
C(Major)[T.Mechanical Engineering]                 0.8034      1.270      0.633      0.528      -1.713       3.320
C(Gender)[T.Male]                                  0.3182      0.842      0.378      0.706      -1.350       1.987
Underrating_Gap                                    0.3458      0.132      2.611      0.010       0.083       0.608
TL_percent                                         0.1643      0.064      2.558      0.012       0.037       0.292
EAP_mean                                          -1.0550      0.800     -1.319      0.190      -2.640       0.530
Pre_Overall                                        0.0069      0.082      0.084      0.933      -0.156       0.169
==============================================================================
Omnibus:                        1.612   Durbin-Watson:                   1.894
Prob(Omnibus):                  0.447   Jarque-Bera (JB):                1.679
Skew:                          -0.247   Prob(JB):                        0.432
Kurtosis:                       2.698   Cond. No.                     1.20e+03
==============================================================================

Notes:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
[2] The condition number is large, 1.2e+03. This might indicate that there are
strong multicollinearity or other numerical problems.
```

### 6.4 Mediation (underrating → translanguaging → decline)

- Path a (Underrating_Gap → TL_percent): b = 1.046
- Path b (TL_percent → Decline | underrating): b = 0.092
- Indirect effect a×b = 0.096
- Direct effect c′ (underrating → decline | TL) = 0.447
- Sobel z = 1.74, p = .082

Treat Sobel as a conventional large-sample check. For the paper, also report a bootstrap indirect effect (PROCESS or `statsmodels` with resampling) on the real data.

### 6.5 Lecturer-level dose-response (n = 12, exploratory)

- Class-mean underrating × class-mean decline: r = 0.823, p = .001
- Class-mean translanguaging × class-mean decline: r = 0.575, p = .050

n = 12 is underpowered; use this as a display of the nesting (Golem is a lecturer-held expectancy) and rely on the student-level models plus qualitative interviews.

### 6.6 Major and gender

- One-way ANOVA on Decline_Overall by major: F = 0.51, p = .604; Kruskal–Wallis H = 0.90, p = .638.
- Welch t on decline, male vs female: t = 0.58, p = .565 (male M = 1.01, n = 82; female M = 0.50, n = 38).

A non-significant major ANOVA is acceptable: it means the Golem claim is **not** 'chemical engineering students decline because the discipline is local'. Variation is modelled at lecturer/student level.

### 6.7 Lecturer clustering

One-way ICC of Decline_Overall by Lecturer_ID = 0.233 (MS_between = 68.62, MS_within = 16.99). A small-to-moderate ICC is consistent with expectancy living at the lecturer; student-level models remain the primary tests.

A random-intercept mixed model was not retained (Random-intercept mixed models were not retained: underrating and translanguaging already capture most lecturer-level variance, so RE covariance is typically singular. The one-way ICC above is the clustering summary.).

## 7. What to tell a referee about alternative explanations

| Alternative | What we can say with these variables |
|---|---|
| Disuse / no EAP after prep year | Predicts a uniform drop. Here decline is tied to underrating and L1 exposure, so disuse-alone is incomplete. |
| Pretest inflated by cramming | Would predict regression toward a lower true score for everyone, especially high scorers. Pretest is a covariate in Model 3. |
| Unequal pre/post forms | Methods must document shared blueprint and (in a real study) statistical equating. This file assumes parallel forms. |
| Lecturer cannot lecture in English | Captured as EAP_mean and entered as a control; it is not labelled Golem. |
| Translanguaging is pedagogically good | The paper should bound the claim: *underrating-driven / avoidance-driven* L1 use, not translanguaging as a resource. |

## 8. Item wording (use or adapt in the real questionnaire)

**Perceived underrating (PU1–PU5)** 1 = strongly disagree … 5 = strongly agree
1. My content lecturers think my English is weaker than it actually is.
2. Lecturers switch to Turkish because they assume we will not understand English.
3. I am given fewer chances to speak English in class than I could handle.
4. Lecturers underestimate my ability to follow lectures in English.
5. I am treated as if I cannot handle academic English.

**Translanguaging exposure (TL1–TL5)** plus `TL_percent`
1. Key concepts are explained in Turkish.
2. Slides or board work are orally translated into Turkish.
3. Students are encouraged to ask questions in Turkish.
4. Assessment tasks are clarified in Turkish.
5. Whole-class discussion often continues in Turkish after a short English start.
`TL_percent`: About what percentage of content-course time is conducted in Turkish rather than English? (0–100)

**Lecturer EAP limitation (EAP1–EAP5)** — competing cause, **not** Golem
1. My lecturers seem more comfortable explaining in Turkish than in English.
2. Lecturers' spoken academic English appears limited.
3. Lecturers look relieved when the class moves into Turkish.
4. English explanations from lecturers are short; Turkish explanations are fuller.
5. Lecturers avoid extended English when the idea becomes technical.

**Willingness to communicate in English (WTC1–WTC5)**
1. I volunteer answers in English in content classes.
2. I am willing to give presentations in English.
3. I ask lecturers questions in English.
4. I discuss course problems with classmates in English.
5. I prefer English when both languages are possible.

**English self-efficacy (SE1–SE5)**
1. I can follow EMI lectures in English.
2. I can write engineering assignments in English.
3. I can read English research papers in my field.
4. I can take part in English technical discussion.
5. I can handle oral exams or critiques in English.

## 9. Ethics and labelling

This workbook is **synthetic**. For a real study: IRB/ethics, informed consent, rater training notes, and a statement that graduation-year testers were not the students' current content lecturers (to reduce expectancy contamination of the posttest).
