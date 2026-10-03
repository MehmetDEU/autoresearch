# Psychometric and inferential report

> **Synthetic panel** (N = 120 completers). Generated for instrument testing and paper scaffolding. Do not treat as empirical findings.

- Random seed: `20261003`
- Gender: 82 male (68.3%), 38 female
- Majors: Mechanical Engineering n=40, Chemical Engineering n=40, Electrical-Electronics Engineering n=40
- Age at graduation: 22–25 (age at PYP exit = graduation age − 4)
- All pretest overall scores ≥ 60 (B1 institutional threshold): **True** (min = 60.1)
- Posttest scores below 60: **11** students (possible fall below B1 after four EMI years)

## 1. Why the test is paired, not independent

The same 120 students sat parallel forms four years apart. The correct test is a **paired-samples *t*-test** (and Wilcoxon signed-rank as a distribution-free companion). An independent-samples *t*-test would treat pre and post as unrelated groups and is the wrong model.

Paired *t* assumes that **difference scores** are approximately normal, not that the raw totals are normal. Raw totals are truncated at 60 on the pretest, so they can look skewed; that is expected.

## 2. Descriptive statistics and distributional checks

| Variable | n | M | SD | Min | Max | Skew | Excess kurtosis | Shapiro–Wilk W | p |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Pre_Listening | 120 | 67.25 | 5.24 | 57.1 | 83.5 | 0.66 | 0.34 | 0.967 | .005 |
| Pre_Reading | 120 | 67.82 | 4.86 | 57.5 | 81.7 | 0.55 | 0.36 | 0.968 | .005 |
| Pre_Writing | 120 | 66.34 | 5.22 | 53.5 | 80.9 | 0.40 | 0.15 | 0.984 | .182 |
| Pre_Speaking | 120 | 65.72 | 5.60 | 54.4 | 80.5 | 0.33 | -0.62 | 0.975 | .027 |
| Pre_Overall | 120 | 66.79 | 4.61 | 60.1 | 81.4 | 0.72 | 0.39 | 0.955 | <.001 |
| Post_Listening | 120 | 65.90 | 5.80 | 54.7 | 80.1 | 0.26 | -0.41 | 0.983 | .128 |
| Post_Reading | 120 | 68.73 | 5.26 | 58.3 | 82.7 | 0.61 | 0.14 | 0.968 | .006 |
| Post_Writing | 120 | 67.04 | 5.95 | 50.8 | 84.2 | 0.21 | 0.20 | 0.991 | .614 |
| Post_Speaking | 120 | 60.12 | 6.27 | 48.1 | 80.5 | 0.26 | -0.15 | 0.985 | .199 |
| Post_Overall | 120 | 65.45 | 4.72 | 55.0 | 79.6 | 0.69 | 0.45 | 0.964 | .003 |
| Decline_Listening | 120 | 1.35 | 3.75 | -9.1 | 8.4 | -0.24 | -0.68 | 0.977 | .038 |
| Decline_Reading | 120 | -0.90 | 2.54 | -7.3 | 5.7 | -0.28 | -0.15 | 0.987 | .300 |
| Decline_Writing | 120 | -0.70 | 3.11 | -9.3 | 7.1 | -0.12 | 0.31 | 0.990 | .576 |
| Decline_Speaking | 120 | 5.60 | 4.57 | -7.1 | 17.7 | -0.29 | 0.17 | 0.990 | .517 |
| Decline_Overall | 120 | 1.34 | 2.17 | -4.5 | 5.9 | -0.14 | -0.23 | 0.991 | .608 |
| Underrating_Gap | 120 | 9.03 | 3.36 | 2.5 | 16.2 | 0.15 | -0.79 | 0.979 | .063 |
| TL_percent | 120 | 36.53 | 13.02 | 12.0 | 65.9 | -0.31 | -0.66 | 0.963 | .002 |
| PU_mean | 120 | 3.11 | 0.79 | 1.2 | 4.8 | 0.04 | -0.45 | 0.987 | .312 |
| TL_mean | 120 | 3.34 | 0.71 | 1.0 | 5.0 | -0.25 | 0.72 | 0.978 | .048 |
| EAP_mean | 120 | 2.86 | 0.79 | 1.0 | 4.6 | 0.15 | -0.46 | 0.979 | .059 |
| WTC_mean | 120 | 3.83 | 0.71 | 2.2 | 5.0 | -0.27 | -0.66 | 0.968 | .006 |
| SE_mean | 120 | 3.80 | 0.76 | 2.2 | 5.0 | -0.35 | -0.92 | 0.951 | <.001 |
| Lecturer_Est_English | 120 | 57.75 | 5.44 | 48.0 | 72.4 | 0.39 | -0.39 | 0.978 | .048 |

Shapiro–Wilk on **overall difference scores**: W = 0.991, p = .608. Difference scores are compatible with normality, so the paired *t*-test is appropriate; Wilcoxon is still reported.

## 3. Pre–post change (primary inferential test)

| Skill | Pre M (SD) | Post M (SD) | Mean decline | 95% CI | t(119) | p | Wilcoxon p | d_z | d_av | n post < 60 |
|---|---|---|---:|---|---:|---|---|---:|---:|---:|
| Listening | 67.25 (5.24) | 65.90 (5.80) | 1.35 | [0.67, 2.03] | 3.93 | <.001 | <.001 | 0.36 | 0.24 | 22 |
| Reading | 67.82 (4.86) | 68.73 (5.26) | -0.90 | [-1.36, -0.45] | -3.90 | <.001 | <.001 | -0.36 | -0.18 | 3 |
| Writing | 66.34 (5.22) | 67.04 (5.95) | -0.70 | [-1.26, -0.14] | -2.46 | .015 | .017 | -0.22 | -0.12 | 14 |
| Speaking | 65.72 (5.60) | 60.12 (6.27) | 5.60 | [4.78, 6.43] | 13.44 | <.001 | <.001 | 1.23 | 0.94 | 62 |
| Overall | 66.79 (4.61) | 65.45 (4.72) | 1.34 | [0.95, 1.73] | 6.77 | <.001 | <.001 | 0.62 | 0.29 | 11 |

**Headline (skill pattern):** Speaking shows the radical attrition (M_decline = 5.60, t(119) = 13.44, p = <.001, d_z = 1.23). Listening also declines more modestly (M = 1.35, p = <.001). Reading shows little attrition / slight gain (M = -0.90, p = <.001), and Writing a slight gain (M = -0.70, p = .015), consistent with continued exposure to academic written texts and lab/report writing. Overall change is secondary to Speaking (M = 1.34, p = <.001). The oral–aural pattern—especially Speaking—is the attrition story later linked to translanguaging.

## 4. Reliability

Cronbach's α and McDonald's ω from section scores (Listening/Reading) or from the four IELTS-aligned rubric criteria (Writing/Speaking). Questionnaire scales are 5 Likert items (1–5).

| Scale | Items | Cronbach's α | McDonald's ω |
|---|---:|---:|---:|
| Pre_Listening_sections | 4 | 0.783 | 0.860 |
| Pre_Reading_sections | 4 | 0.791 | 0.865 |
| Post_Listening_sections | 4 | 0.836 | 0.892 |
| Post_Reading_sections | 4 | 0.821 | 0.884 |
| Perceived_underrating_PU | 5 | 0.885 | 0.917 |
| Translanguaging_Likert_TL | 5 | 0.914 | 0.936 |
| Lecturer_EAP_limitation | 5 | 0.891 | 0.920 |
| WTC_English | 5 | 0.859 | 0.900 |
| Self_efficacy_English | 5 | 0.876 | 0.911 |
| Pre_full_sections | 8 | 0.871 | 0.899 |
| Post_full_sections | 8 | 0.865 | 0.895 |
| Pre_Writing_criteria | 4 | 0.883 | 0.920 |
| Post_Writing_criteria | 4 | 0.917 | 0.943 |
| Pre_Speaking_criteria | 4 | 0.899 | 0.930 |
| Post_Speaking_criteria | 4 | 0.925 | 0.947 |

### Inter-rater reliability (Writing & Speaking)

Three independent marks (expert/author + two PYP instructors). ICC(2,1) = single-rater agreement; ICC(2,k) = reliability of the 3-rater mean (the official score).

| Facet | ICC(2,1) | ICC(2,k) |
|---|---:|---:|
| Writing_Pre | 0.872 | 0.954 |
| Writing_Post | 0.905 | 0.966 |
| Speaking_Pre | 0.891 | 0.961 |
| Speaking_Post | 0.926 | 0.974 |

## 5. Validity

### 5.1 Content validity (non-statistical, required in methods)

The institutional test uses the IELTS Academic skill split and the public IELTS band descriptors for Writing (Task Response, Coherence & Cohesion, Lexical Resource, Grammatical Range & Accuracy) and Speaking (Fluency & Coherence, Lexical Resource, Grammatical Range & Accuracy, Pronunciation). Listening and Reading use four sections each, mapped to IELTS Academic item types. Standard setting: 60/100 = B1 (institution policy). Pre and post forms share this blueprint (parallel forms; not identical items).

### 5.2 Concurrent validity vs IELTS Academic practice tests

A stratified subsample (n = 36; 12 per major) sat official IELTS Academic practice materials from ielts.org under exam conditions at PYP exit. Mapping used in generation: IELTS band ≈ 5.0 + (institutional − 60) × 0.05, plus small error, rounded to 0.5 bands.

| Institutional | IELTS | n | r | p |
|---|---|---:|---:|---|
| Pre_Overall | IELTS_Overall | 36 | 0.782 | <.001 |
| Pre_Listening | IELTS_Listening | 36 | 0.759 | <.001 |
| Pre_Reading | IELTS_Reading | 36 | 0.766 | <.001 |
| Pre_Writing | IELTS_Writing | 36 | 0.738 | <.001 |
| Pre_Speaking | IELTS_Speaking | 36 | 0.854 | <.001 |

### 5.3 Convergent structure

Pre-test skill intercorrelations (should be moderate-to-strong if they tap a common academic-English factor):

| Variable | Pre_Listening | Pre_Reading | Pre_Writing | Pre_Speaking | Pre_Overall |
|---|---|---|---|---|---|
| Pre_Listening | 1.000 | 0.727 | 0.690 | 0.705 | 0.884 |
| Pre_Reading | 0.727 | 1.000 | 0.719 | 0.711 | 0.889 |
| Pre_Writing | 0.690 | 0.719 | 1.000 | 0.680 | 0.874 |
| Pre_Speaking | 0.705 | 0.711 | 0.680 | 1.000 | 0.883 |
| Pre_Overall | 0.884 | 0.889 | 0.874 | 0.883 | 1.000 |

Post-test skill intercorrelations:

| Variable | Post_Listening | Post_Reading | Post_Writing | Post_Speaking | Post_Overall |
|---|---|---|---|---|---|
| Post_Listening | 1.000 | 0.555 | 0.513 | 0.603 | 0.825 |
| Post_Reading | 0.555 | 1.000 | 0.593 | 0.499 | 0.802 |
| Post_Writing | 0.513 | 0.593 | 1.000 | 0.489 | 0.802 |
| Post_Speaking | 0.603 | 0.499 | 0.489 | 1.000 | 0.811 |
| Post_Overall | 0.825 | 0.802 | 0.802 | 0.811 | 1.000 |

## 6. Mechanism (e): is the decline Golem-like or just attrition?

### 6.1 Inaccuracy of lecturer expectancy

Lecturers' estimates of students' English were lower than actual PYP-exit scores by 9.03 points (M_actual = 66.79, M_estimate = 57.75), t(119) = 29.42, p = <.001, d_z = 2.69. This is the inaccuracy criterion: the low expectation is not merely 'felt'; it is wrong relative to the institutional measure.

### 6.2 Correlations with Speaking decline (primary attrition outcome)

| Predictor | r with Decline_Speaking | p | Role |
|---|---:|---|---|
| Underrating_Gap | 0.647 | <.001 | Golem: inaccuracy |
| TL_percent | 0.732 | <.001 | Treatment: L1 exposure (key path) |
| PU_mean | 0.492 | <.001 | Student-perceived underrating |
| EAP_mean | 0.392 | <.001 | Competing cause (not Golem) |
| WTC_mean | -0.515 | <.001 | Internalization (lower WTC ↔ more Speaking decline) |
| SE_mean | -0.439 | <.001 | Internalization |

Mechanism intercorrelations:

| Variable | Decline_Speaking | Decline_Listening | Decline_Overall | Underrating_Gap | TL_percent | PU_mean | EAP_mean | WTC_mean | SE_mean | Pre_Speaking |
|---|---|---|---|---|---|---|---|---|---|---|
| Decline_Speaking | 1.000 | 0.316 | 0.726 | 0.647 | 0.732 | 0.492 | 0.392 | -0.515 | -0.439 | 0.253 |
| Decline_Listening | 0.316 | 1.000 | 0.690 | 0.292 | 0.271 | 0.191 | 0.085 | -0.152 | -0.188 | 0.071 |
| Decline_Overall | 0.726 | 0.690 | 1.000 | 0.524 | 0.576 | 0.398 | 0.256 | -0.344 | -0.380 | 0.192 |
| Underrating_Gap | 0.647 | 0.292 | 0.524 | 1.000 | 0.485 | 0.691 | -0.028 | -0.566 | -0.643 | 0.131 |
| TL_percent | 0.732 | 0.271 | 0.576 | 0.485 | 1.000 | 0.412 | 0.608 | -0.529 | -0.377 | 0.114 |
| PU_mean | 0.492 | 0.191 | 0.398 | 0.691 | 0.412 | 1.000 | 0.010 | -0.455 | -0.428 | 0.017 |
| EAP_mean | 0.392 | 0.085 | 0.256 | -0.028 | 0.608 | 0.010 | 1.000 | -0.283 | -0.023 | 0.046 |
| WTC_mean | -0.515 | -0.152 | -0.344 | -0.566 | -0.529 | -0.455 | -0.283 | 1.000 | 0.479 | -0.055 |
| SE_mean | -0.439 | -0.188 | -0.380 | -0.643 | -0.377 | -0.428 | -0.023 | 0.479 | 1.000 | -0.153 |
| Pre_Speaking | 0.253 | 0.071 | 0.192 | 0.131 | 0.114 | 0.017 | 0.046 | -0.055 | -0.153 | 1.000 |

### 6.3 Regression: does underrating survive controls?

**Model 1 — lecturer EAP limitation only (competing cause) predicting Decline_Speaking.** If Speaking attrition were only about lecturers' own English, this would be the story.

```
                            OLS Regression Results                            
==============================================================================
Dep. Variable:       Decline_Speaking   R-squared:                       0.302
Model:                            OLS   Adj. R-squared:                  0.272
Method:                 Least Squares   F-statistic:                     9.887
Date:                Sat, 03 Oct 2026   Prob (F-statistic):           7.14e-08
Time:                        16:12:14   Log-Likelihood:                -330.40
No. Observations:                 120   AIC:                             672.8
Df Residuals:                     114   BIC:                             689.5
Df Model:                           5                                         
Covariance Type:            nonrobust                                         
==================================================================================================================
                                                     coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------------------------------------------
Intercept                                        -12.1287      4.482     -2.706      0.008     -21.008      -3.249
C(Major)[T.Electrical-Electronics Engineering]     0.1423      0.948      0.150      0.881      -1.735       2.020
C(Major)[T.Mechanical Engineering]                -2.6728      0.896     -2.982      0.003      -4.448      -0.897
C(Gender)[T.Male]                                 -0.8418      0.783     -1.075      0.285      -2.393       0.710
EAP_mean                                           2.1550      0.501      4.298      0.000       1.162       3.148
Pre_Speaking                                       0.1975      0.064      3.083      0.003       0.071       0.324
==============================================================================
Omnibus:                        0.076   Durbin-Watson:                   1.468
Prob(Omnibus):                  0.963   Jarque-Bera (JB):                0.132
Skew:                          -0.058   Prob(JB):                        0.936
Kurtosis:                       2.887   Cond. No.                         834.
==============================================================================

Notes:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
```

**Model 2 — underrating gap → Decline_Speaking.** Golem inaccuracy path.

```
                            OLS Regression Results                            
==============================================================================
Dep. Variable:       Decline_Speaking   R-squared:                       0.597
Model:                            OLS   Adj. R-squared:                  0.580
Method:                 Least Squares   F-statistic:                     33.83
Date:                Sat, 03 Oct 2026   Prob (F-statistic):           4.75e-21
Time:                        16:12:14   Log-Likelihood:                -297.43
No. Observations:                 120   AIC:                             606.9
Df Residuals:                     114   BIC:                             623.6
Df Model:                           5                                         
Covariance Type:            nonrobust                                         
==================================================================================================================
                                                     coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------------------------------------------
Intercept                                         -9.5281      3.248     -2.933      0.004     -15.963      -3.093
C(Major)[T.Electrical-Electronics Engineering]    -3.6891      0.699     -5.280      0.000      -5.073      -2.305
C(Major)[T.Mechanical Engineering]                -3.1267      0.669     -4.671      0.000      -4.453      -1.801
C(Gender)[T.Male]                                 -1.2395      0.587     -2.112      0.037      -2.402      -0.077
Underrating_Gap                                    0.9400      0.087     10.747      0.000       0.767       1.113
Pre_Speaking                                       0.1485      0.049      3.032      0.003       0.051       0.246
==============================================================================
Omnibus:                        0.566   Durbin-Watson:                   1.706
Prob(Omnibus):                  0.754   Jarque-Bera (JB):                0.705
Skew:                          -0.134   Prob(JB):                        0.703
Kurtosis:                       2.737   Cond. No.                         801.
==============================================================================

Notes:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
```

**Model 3 — underrating + translanguaging + EAP + Pre_Speaking + major + gender → Decline_Speaking.** Joint model. The translanguaging path should remain for Speaking; EAP_mean should weaken.

```
                            OLS Regression Results                            
==============================================================================
Dep. Variable:       Decline_Speaking   R-squared:                       0.695
Model:                            OLS   Adj. R-squared:                  0.676
Method:                 Least Squares   F-statistic:                     36.52
Date:                Sat, 03 Oct 2026   Prob (F-statistic):           3.86e-26
Time:                        16:12:14   Log-Likelihood:                -280.69
No. Observations:                 120   AIC:                             577.4
Df Residuals:                     112   BIC:                             599.7
Df Model:                           7                                         
Covariance Type:            nonrobust                                         
==================================================================================================================
                                                     coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------------------------------------------
Intercept                                        -13.8069      3.004     -4.596      0.000     -19.759      -7.855
C(Major)[T.Electrical-Electronics Engineering]    -1.0165      0.816     -1.246      0.215      -2.633       0.600
C(Major)[T.Mechanical Engineering]                -1.2660      0.758     -1.669      0.098      -2.769       0.237
C(Gender)[T.Male]                                 -0.8752      0.524     -1.672      0.097      -1.912       0.162
Underrating_Gap                                    0.6688      0.115      5.810      0.000       0.441       0.897
TL_percent                                         0.1074      0.039      2.730      0.007       0.029       0.185
EAP_mean                                           0.9357      0.460      2.033      0.044       0.024       1.848
Pre_Speaking                                       0.1237      0.043      2.858      0.005       0.038       0.209
==============================================================================
Omnibus:                        0.326   Durbin-Watson:                   2.126
Prob(Omnibus):                  0.849   Jarque-Bera (JB):                0.077
Skew:                          -0.022   Prob(JB):                        0.962
Kurtosis:                       3.115   Cond. No.                         968.
==============================================================================

Notes:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
```

### 6.4 Mediation (underrating → translanguaging → Speaking decline)

- Path a (Underrating_Gap → TL_percent): b = 1.876
- Path b (TL_percent → Decline_Speaking | underrating): b = 0.192
- Indirect effect a×b = 0.360
- Direct effect c′ (underrating → Speaking decline | TL) = 0.519
- Sobel z = 4.96, p = <.001

Treat Sobel as a conventional large-sample check. For the paper, also report a bootstrap indirect effect (PROCESS or `statsmodels` with resampling) on the real data.

### 6.5 Lecturer-level dose-response for Speaking (n = 12, exploratory)

- Class-mean underrating × class-mean Speaking decline: r = 0.711, p = .009
- Class-mean translanguaging × class-mean Speaking decline: r = 0.870, p = <.001

n = 12 is underpowered; use this as a display of the nesting (Golem is a lecturer-held expectancy) and rely on the student-level models plus qualitative interviews.

### 6.6 Major and gender (Speaking decline)

- One-way ANOVA on Decline_Speaking by major: F = 6.22, p = .003; Kruskal–Wallis H = 10.47, p = .005.
- Welch t on Speaking decline, male vs female: t = -2.24, p = .027 (male M = 5.01, n = 82; female M = 6.87, n = 38).

A non-significant major ANOVA is acceptable: attrition is not framed as a discipline-local effect. Variation is modelled at lecturer/student level.

### 6.7 Lecturer clustering (Speaking decline)

One-way ICC of Decline_Speaking by Lecturer_ID = 0.546 (MS_between = 128.62, MS_within = 9.87). A small-to-moderate ICC is consistent with expectancy/treatment living at the lecturer; student-level models remain the primary tests.

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
