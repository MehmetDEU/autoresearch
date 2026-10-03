# How we test the Golem mechanism (not just attrition)

Pre/post decline by itself is **not** a Golem effect. Four years after a Preparatory Year Programme, English can rust from **disuse** even if lecturers are supportive. Reviewers will say exactly that unless the *amount* of decline is tied to the expectancy–treatment loop.

This sample dataset therefore measures three extra layers, plus one competing cause that must **not** be labelled Golem.

## The loop we need to show

```text
1. Inaccuracy     Lecturer's estimate of the student's English
                  is systematically LOWER than the student's
                  actual prep-year exit score.
                  (Referee 3's criterion: the low expectation
                  has to be wrong, not merely discouraging.)

2. Treatment      Those lecturers provide thinner English input:
                  more L1 / translanguaging, fewer chances to
                  speak or write in English.

3. Internalization Students report lower willingness to communicate
                  in English and lower English self-efficacy.
                  They start asking for Turkish and using L1 sources.

4. Outcome         Institutional proficiency change is skill-specific:
                  Speaking shows radical attrition; Listening a modest
                  drop; Reading and Writing stay flat or rise slightly
                  (academic written exposure / lab reports). Speaking
                  loss is the primary outcome linked to translanguaging.
```

Only step 1 + 2 + 4 is classic Golem (Babad, Inbar & Rosenthal, 1982). Step 3 is the student-side mediator; useful, not sufficient on its own.

## Two causes of translanguaging — keep them separate

| Cause | What it is | Golem? |
|---|---|---|
| Lecturer underrates students | Low *expectancy* about the class | **Yes** |
| Lecturer's own EAP limitation | Lecturer is more comfortable in Turkish | **No** |

Both can increase L1 use. Only underrating is a Golem effect. In the workbook this is why `EAP_limitation` is a **control**, not a Golem indicator.

## How the numbers answer "is this just attrition?"

Pure attrition predicts a **similar** drop for everyone (or a drop that only tracks how high the pretest was).

Golem predicts **heterogeneous** drop:

- students whose lecturers underestimate them more → larger **Speaking** decline
- students in higher-translanguaging classes → larger **Speaking** decline
- Speaking attrition dominates; Listening declines modestly; Reading/Writing show little loss or slight gains
- lecturer EAP-gap predicts translanguaging, but once underrating and translanguaging are in the model, EAP-gap should **not** remain the main predictor of Speaking decline

That is why the Excel file includes, for every student:

- `Lecturer_Est_English` and `Underrating_Gap` (inaccuracy)
- `TL_percent` plus five translanguaging Likert items (treatment)
- `PU1–PU5` perceived underrating (student lens)
- `EAP1–EAP5` lecturer EAP limitation (competing cause)
- `WTC1–WTC5` and `SE1–SE5` (internalization)
- `Lecturer_ID` (expectancy lives at the lecturer, 10 students each)

Primary quantitative tests for mechanism (e):

1. Paired *t*: `Pre_Overall` vs `Lecturer_Est_English` — lecturers underestimate.
2. Pearson / regression: `Decline_Speaking` ~ `Underrating_Gap` + `TL_percent` + `EAP_mean` + covariates.
3. Mediation (Baron & Kenny / Sobel): underrating → translanguaging → Speaking decline.
4. Skill pattern: Speaking ≫ Listening attrition; Reading/Writing near zero or slight gains.

Qualitative interviews (your existing lecturer/student data) then interpret *why* a given lecturer translanguages — underrating vs own EAP gap — so the two paths are not collapsed in the write-up.

## What this still does not prove

These are **associations** in a non-experimental panel. Causal language stays hedged ("associated with", "consistent with"). A journal will still want the qualitative strand and a limitations paragraph on: no random assignment of lecturers, possible curriculum differences by major, and no weekly classroom observation counts (student-reported `TL_percent` is a proxy).
