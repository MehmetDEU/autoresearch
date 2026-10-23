# Psychometric and inferential report

> **Synthetic panel** (N = 120 completers). Generated for instrument testing and paper scaffolding. Do not treat as empirical findings.

- Random seed: `20261003`
- Gender: 82 male (68.3%), 38 female
- Majors: Mechanical Engineering n=40, Chemical Engineering n=40, Electrical-Electronics Engineering n=40
- Age at graduation: 22–25 (age at PYP exit = graduation age − 4)
- All pretest overall scores ≥ 60 (B1 institutional threshold): **True** (min = 60.1)
- Posttest scores below 60: **18** students (possible fall below B1 after four EMI years)

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
| Post_Listening | 120 | 63.70 | 6.12 | 51.4 | 80.2 | 0.25 | -0.35 | 0.986 | .268 |
| Post_Reading | 120 | 68.23 | 5.72 | 56.5 | 82.4 | 0.54 | 0.06 | 0.969 | .007 |
| Post_Writing | 120 | 66.69 | 6.51 | 49.9 | 85.7 | 0.15 | 0.24 | 0.991 | .599 |
| Post_Speaking | 120 | 60.62 | 6.33 | 47.9 | 81.0 | 0.23 | -0.19 | 0.987 | .290 |
| Post_Overall | 120 | 64.81 | 4.89 | 53.8 | 80.0 | 0.67 | 0.40 | 0.968 | .005 |
| Decline_Listening | 120 | 3.55 | 4.11 | -7.8 | 12.7 | -0.14 | -0.55 | 0.989 | .414 |
| Decline_Reading | 120 | -0.41 | 3.53 | -9.3 | 8.6 | -0.29 | -0.19 | 0.987 | .293 |
| Decline_Writing | 120 | -0.35 | 4.10 | -11.8 | 10.1 | -0.09 | 0.29 | 0.992 | .752 |
| Decline_Speaking | 120 | 5.10 | 4.57 | -8.0 | 16.6 | -0.35 | 0.21 | 0.988 | .347 |
| Decline_Overall | 120 | 1.97 | 2.54 | -4.1 | 7.2 | -0.18 | -0.20 | 0.986 | .228 |
| Underrating_Gap | 120 | 9.03 | 3.36 | 2.5 | 16.2 | 0.15 | -0.79 | 0.979 | .063 |
| TL_percent | 120 | 36.53 | 13.02 | 12.0 | 65.9 | -0.31 | -0.66 | 0.963 | .002 |
| PU_mean | 120 | 3.11 | 0.79 | 1.2 | 4.8 | 0.04 | -0.45 | 0.987 | .312 |
| TL_mean | 120 | 3.34 | 0.71 | 1.0 | 5.0 | -0.25 | 0.72 | 0.978 | .048 |
| EAP_mean | 120 | 2.86 | 0.79 | 1.0 | 4.6 | 0.15 | -0.46 | 0.979 | .059 |
| WTC_mean | 120 | 3.83 | 0.71 | 2.2 | 5.0 | -0.27 | -0.66 | 0.968 | .006 |
| SE_mean | 120 | 3.80 | 0.76 | 2.2 | 5.0 | -0.35 | -0.92 | 0.951 | <.001 |
| Lecturer_Est_English | 120 | 57.75 | 5.44 | 48.0 | 72.4 | 0.39 | -0.39 | 0.978 | .048 |

Shapiro–Wilk on **overall difference scores**: W = 0.986, p = .228. Difference scores are compatible with normality, so the paired *t*-test is appropriate; Wilcoxon is still reported.

## 3. Pre–post change (primary inferential test)

| Skill | Pre M (SD) | Post M (SD) | Mean decline | 95% CI | t(119) | p | Wilcoxon p | d_z | d_av | n post < 60 |
|---|---|---|---:|---|---:|---|---|---:|---:|---:|
| Listening | 67.25 (5.24) | 63.70 (6.12) | 3.55 | [2.81, 4.29] | 9.46 | <.001 | <.001 | 0.86 | 0.62 | 37 |
| Reading | 67.82 (4.86) | 68.23 (5.72) | -0.41 | [-1.04, 0.23] | -1.26 | .211 | .381 | -0.11 | -0.08 | 6 |
| Writing | 66.34 (5.22) | 66.69 (6.51) | -0.35 | [-1.09, 0.39] | -0.93 | .353 | .384 | -0.09 | -0.06 | 16 |
| Speaking | 65.72 (5.60) | 60.62 (6.33) | 5.10 | [4.27, 5.93] | 12.21 | <.001 | <.001 | 1.11 | 0.85 | 56 |
| Overall | 66.79 (4.61) | 64.81 (4.89) | 1.97 | [1.51, 2.43] | 8.50 | <.001 | <.001 | 0.78 | 0.41 | 18 |

**Headline (skill pattern):** Oral–aural skills decline significantly. Speaking attrition is large (M_decline = 5.10, t(119) = 12.21, p = <.001, d_z = 1.11), and Listening also declines substantially (M = 3.55, p = <.001, d_z = 0.86). Reading shows no statistically significant decline (M = -0.41, p = .211), and Writing likewise (M = -0.35, p = .353); both written skills are consistent with continued exposure to academic texts and lab/report writing. Overall change follows the oral–aural pattern (M = 1.97, p = <.001). The Listening+Speaking drop is attributed to under-exposure to verbal interaction (lecturer EAP limitation and underrating-driven translanguaging / Golem).

## 4. Reliability

Cronbach's α and McDonald's ω from section scores (Listening/Reading) or from the four IELTS-aligned rubric criteria (Writing/Speaking). Questionnaire scales are 5 Likert items (1–5).

| Scale | Items | Cronbach's α | McDonald's ω |
|---|---:|---:|---:|
| Pre_Listening_sections | 4 | 0.783 | 0.860 |
| Pre_Reading_sections | 4 | 0.791 | 0.865 |
| Post_Listening_sections | 4 | 0.855 | 0.903 |
| Post_Reading_sections | 4 | 0.850 | 0.901 |
| Perceived_underrating_PU | 5 | 0.885 | 0.917 |
| Translanguaging_Likert_TL | 5 | 0.914 | 0.936 |
| Lecturer_EAP_limitation | 5 | 0.891 | 0.920 |
| WTC_English | 5 | 0.859 | 0.900 |
| Self_efficacy_English | 5 | 0.876 | 0.911 |
| Pre_full_sections | 8 | 0.871 | 0.899 |
| Post_full_sections | 8 | 0.865 | 0.895 |
| Pre_Writing_criteria | 4 | 0.883 | 0.920 |
| Post_Writing_criteria | 4 | 0.931 | 0.952 |
| Pre_Speaking_criteria | 4 | 0.899 | 0.930 |
| Post_Speaking_criteria | 4 | 0.926 | 0.948 |

### Inter-rater reliability (Writing & Speaking)

Three independent marks (expert/author + two PYP instructors). ICC(2,1) = single-rater agreement; ICC(2,k) = reliability of the 3-rater mean (the official score).

| Facet | ICC(2,1) | ICC(2,k) |
|---|---:|---:|
| Writing_Pre | 0.872 | 0.954 |
| Writing_Post | 0.920 | 0.972 |
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
| Post_Listening | 1.000 | 0.486 | 0.462 | 0.696 | 0.834 |
| Post_Reading | 0.486 | 1.000 | 0.507 | 0.445 | 0.756 |
| Post_Writing | 0.462 | 0.507 | 1.000 | 0.436 | 0.766 |
| Post_Speaking | 0.696 | 0.445 | 0.436 | 1.000 | 0.815 |
| Post_Overall | 0.834 | 0.756 | 0.766 | 0.815 | 1.000 |

## 6. Mechanism (e): is the decline Golem-like or just attrition?

### 6.1 Inaccuracy of lecturer expectancy

Lecturers' estimates of students' English were lower than actual PYP-exit scores by 9.03 points (M_actual = 66.79, M_estimate = 57.75), t(119) = 29.42, p = <.001, d_z = 2.69. This is the inaccuracy criterion: the low expectation is not merely 'felt'; it is wrong relative to the institutional measure.

### 6.2 Correlations with Speaking decline (primary attrition outcome)

| Predictor | r with Decline_Speaking | p | Role |
|---|---:|---|---|
| Underrating_Gap | 0.603 | <.001 | Golem: inaccuracy |
| TL_percent | 0.732 | <.001 | Treatment: L1 exposure (key path) |
| PU_mean | 0.463 | <.001 | Student-perceived underrating |
| EAP_mean | 0.461 | <.001 | Competing cause (not Golem) |
| WTC_mean | -0.505 | <.001 | Internalization (lower WTC ↔ more Speaking decline) |
| SE_mean | -0.412 | <.001 | Internalization |

Mechanism intercorrelations:

| Variable | Decline_Speaking | Decline_Listening | Decline_Overall | Underrating_Gap | TL_percent | PU_mean | EAP_mean | WTC_mean | SE_mean | Pre_Speaking |
|---|---|---|---|---|---|---|---|---|---|---|
| Decline_Speaking | 1.000 | 0.600 | 0.726 | 0.603 | 0.732 | 0.463 | 0.461 | -0.505 | -0.412 | 0.238 |
| Decline_Listening | 0.600 | 1.000 | 0.756 | 0.500 | 0.643 | 0.361 | 0.407 | -0.394 | -0.345 | 0.113 |
| Decline_Overall | 0.726 | 0.756 | 1.000 | 0.499 | 0.633 | 0.392 | 0.372 | -0.367 | -0.381 | 0.181 |
| Underrating_Gap | 0.603 | 0.500 | 0.499 | 1.000 | 0.485 | 0.691 | -0.028 | -0.566 | -0.643 | 0.131 |
| TL_percent | 0.732 | 0.643 | 0.633 | 0.485 | 1.000 | 0.412 | 0.608 | -0.529 | -0.377 | 0.114 |
| PU_mean | 0.463 | 0.361 | 0.392 | 0.691 | 0.412 | 1.000 | 0.010 | -0.455 | -0.428 | 0.017 |
| EAP_mean | 0.461 | 0.407 | 0.372 | -0.028 | 0.608 | 0.010 | 1.000 | -0.283 | -0.023 | 0.046 |
| WTC_mean | -0.505 | -0.394 | -0.367 | -0.566 | -0.529 | -0.455 | -0.283 | 1.000 | 0.479 | -0.055 |
| SE_mean | -0.412 | -0.345 | -0.381 | -0.643 | -0.377 | -0.428 | -0.023 | 0.479 | 1.000 | -0.153 |
| Pre_Speaking | 0.238 | 0.113 | 0.181 | 0.131 | 0.114 | 0.017 | 0.046 | -0.055 | -0.153 | 1.000 |

### 6.3 Regression: does underrating survive controls?

**Model 1 — lecturer EAP limitation only (competing cause) predicting Decline_Speaking.** If Speaking attrition were only about lecturers' own English, this would be the story.

```
                            OLS Regression Results                            
==============================================================================
Dep. Variable:       Decline_Speaking   R-squared:                       0.344
Model:                            OLS   Adj. R-squared:                  0.315
Method:                 Least Squares   F-statistic:                     11.95
Date:                Mon, 05 Oct 2026   Prob (F-statistic):           2.62e-09
Time:                        19:12:20   Log-Likelihood:                -326.92
No. Observations:                 120   AIC:                             665.8
Df Residuals:                     114   BIC:                             682.6
Df Model:                           5                                         
Covariance Type:            nonrobust                                         
==================================================================================================================
                                                     coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------------------------------------------
Intercept                                        -12.8139      4.354     -2.943      0.004     -21.439      -4.189
C(Major)[T.Electrical-Electronics Engineering]     0.1971      0.921      0.214      0.831      -1.627       2.021
C(Major)[T.Mechanical Engineering]                -2.4668      0.871     -2.834      0.005      -4.191      -0.742
C(Gender)[T.Male]                                 -0.9254      0.761     -1.216      0.226      -2.433       0.582
EAP_mean                                           2.5630      0.487      5.262      0.000       1.598       3.528
Pre_Speaking                                       0.1821      0.062      2.926      0.004       0.059       0.305
==============================================================================
Omnibus:                        0.059   Durbin-Watson:                   1.526
Prob(Omnibus):                  0.971   Jarque-Bera (JB):                0.131
Skew:                          -0.051   Prob(JB):                        0.937
Kurtosis:                       2.875   Cond. No.                         834.
==============================================================================

Notes:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
```

**Model 2 — underrating gap → Decline_Speaking.** Golem inaccuracy path.

```
                            OLS Regression Results                            
==============================================================================
Dep. Variable:       Decline_Speaking   R-squared:                       0.549
Model:                            OLS   Adj. R-squared:                  0.529
Method:                 Least Squares   F-statistic:                     27.77
Date:                Mon, 05 Oct 2026   Prob (F-statistic):           2.65e-18
Time:                        19:12:20   Log-Likelihood:                -304.40
No. Observations:                 120   AIC:                             620.8
Df Residuals:                     114   BIC:                             637.5
Df Model:                           5                                         
Covariance Type:            nonrobust                                         
==================================================================================================================
                                                     coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------------------------------------------
Intercept                                         -8.8817      3.443     -2.580      0.011     -15.702      -2.062
C(Major)[T.Electrical-Electronics Engineering]    -3.8074      0.740     -5.142      0.000      -5.274      -2.340
C(Major)[T.Mechanical Engineering]                -3.0703      0.710     -4.327      0.000      -4.476      -1.665
C(Gender)[T.Male]                                 -1.4391      0.622     -2.314      0.022      -2.671      -0.207
Underrating_Gap                                    0.8901      0.093      9.602      0.000       0.706       1.074
Pre_Speaking                                       0.1402      0.052      2.702      0.008       0.037       0.243
==============================================================================
Omnibus:                        0.495   Durbin-Watson:                   1.602
Prob(Omnibus):                  0.781   Jarque-Bera (JB):                0.642
Skew:                          -0.117   Prob(JB):                        0.725
Kurtosis:                       2.729   Cond. No.                         801.
==============================================================================

Notes:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
```

**Model 3 — underrating + translanguaging + EAP + Pre_Speaking + major + gender → Decline_Speaking.** Joint model. The translanguaging path should remain for Speaking; EAP_mean should weaken.

```
                            OLS Regression Results                            
==============================================================================
Dep. Variable:       Decline_Speaking   R-squared:                       0.682
Model:                            OLS   Adj. R-squared:                  0.662
Method:                 Least Squares   F-statistic:                     34.28
Date:                Mon, 05 Oct 2026   Prob (F-statistic):           4.25e-25
Time:                        19:12:20   Log-Likelihood:                -283.50
No. Observations:                 120   AIC:                             583.0
Df Residuals:                     112   BIC:                             605.3
Df Model:                           7                                         
Covariance Type:            nonrobust                                         
==================================================================================================================
                                                     coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------------------------------------------
Intercept                                        -14.4588      3.075     -4.702      0.000     -20.552      -8.366
C(Major)[T.Electrical-Electronics Engineering]    -1.0411      0.835     -1.247      0.215      -2.696       0.614
C(Major)[T.Mechanical Engineering]                -1.3055      0.776     -1.682      0.095      -2.844       0.233
C(Gender)[T.Male]                                 -0.9446      0.536     -1.763      0.081      -2.006       0.117
Underrating_Gap                                    0.6532      0.118      5.543      0.000       0.420       0.887
TL_percent                                         0.0874      0.040      2.171      0.032       0.008       0.167
EAP_mean                                           1.5268      0.471      3.241      0.002       0.593       2.460
Pre_Speaking                                       0.1145      0.044      2.584      0.011       0.027       0.202
==============================================================================
Omnibus:                        0.370   Durbin-Watson:                   2.131
Prob(Omnibus):                  0.831   Jarque-Bera (JB):                0.094
Skew:                          -0.001   Prob(JB):                        0.954
Kurtosis:                       3.137   Cond. No.                         968.
==============================================================================

Notes:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
```

### 6.4 Mediation (underrating → translanguaging → Speaking decline)

- Path a (Underrating_Gap → TL_percent): b = 1.876
- Path b (TL_percent → Decline_Speaking | underrating): b = 0.202
- Indirect effect a×b = 0.379
- Direct effect c′ (underrating → Speaking decline | TL) = 0.441
- Sobel z = 4.97, p = <.001

Treat Sobel as a conventional large-sample check. For the paper, also report a bootstrap indirect effect (PROCESS or `statsmodels` with resampling) on the real data.

### 6.5 Lecturer-level dose-response for Speaking (n = 12, exploratory)

- Class-mean underrating × class-mean Speaking decline: r = 0.664, p = .019
- Class-mean translanguaging × class-mean Speaking decline: r = 0.887, p = <.001

n = 12 is underpowered; use this as a display of the nesting (Golem is a lecturer-held expectancy) and rely on the student-level models plus qualitative interviews.

### 6.6 Major and gender (Speaking decline)

- One-way ANOVA on Decline_Speaking by major: F = 5.99, p = .003; Kruskal–Wallis H = 10.18, p = .006.
- Welch t on Speaking decline, male vs female: t = -2.44, p = .017 (male M = 4.45, n = 82; female M = 6.50, n = 38).

A non-significant major ANOVA is acceptable: attrition is not framed as a discipline-local effect. Variation is modelled at lecturer/student level.

### 6.7 Lecturer clustering (Speaking decline)

One-way ICC of Decline_Speaking by Lecturer_ID = 0.556 (MS_between = 131.19, MS_within = 9.68). A small-to-moderate ICC is consistent with expectancy/treatment living at the lecturer; student-level models remain the primary tests.

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
