# EMI four-year proficiency panel (synthetic)

**This workbook is simulated student data** for testing the scoring design, SPSS/R workflow, and the Golem-mechanism analysis. It is **not** a real institutional dataset. Replace it with live scores before any journal submission.

## What you asked for

| Requirement | How it is implemented |
|---|---|
| N = 120 PYP completers | Sheet `Students` |
| Pretest = PYP exit; posttest = graduation after 4 EMI years | `Pre_*` / `Post_*` |
| IELTS Academic alignment | Four skills; public IELTS Writing/Speaking criteria |
| Pass threshold 60 = CEFR B1 | Every `Pre_Overall` ≥ 60; pretest mean is in the mid-60s |
| ~68% male; ages 22–25 at graduation | 82 male / 38 female; `Age_at_post_graduation` 22–25 and `Age_at_pre_PYP_exit` = age − 4 |
| Balanced engineering majors | 40 Mechanical, 40 Chemical, 40 Electrical-Electronics |
| Two PYP instructors + you as expert | Sheets `Writing_*_raters`, `Speaking_*_raters`; ICC reported |
| Slightly significant pre/post change | **Paired** *t*-test (not independent-samples); p ≈ .05 |
| Psychometrics | Descriptives, Shapiro–Wilk, skew/kurtosis, α, ω, ICC, concurrent IELTS *r* |
| Validity vs IELTS website samples | 36-student subsample sat ielts.org Academic practice tests |

## How we test Golem rather than “English just rusted”

Read `HOW_WE_TEST_GOLEM.md`. Short version: decline is **heterogeneous** and tracks

1. **Inaccuracy** — `Underrating_Gap` = actual PYP score − lecturer’s estimate  
2. **Treatment** — `TL_percent` (share of content-course time in Turkish)  
3. **Internalization** — `WTC_mean`, `SE_mean`  
4. **Not Golem** — `EAP_mean` (lecturer’s own English limitation) is a control

If underrating and translanguaging predict how much a student drops, *after* controlling for pretest, major, gender, and lecturer EAP-gap, attrition-alone is not a sufficient explanation.

## Files

- `EMI_PYP_pre_post_synthetic_N120.xlsx` — main deliverable (19 sheets)
- `PSYCHOMETRIC_REPORT.md` — full statistical write-up
- `HOW_WE_TEST_GOLEM.md` — mechanism (e) in plain language
- `build_dataset.py` — generator (re-runnable; calibrated random seed)
- `outputs/` — CSV extracts and figures

## Rebuild

```bash
python -m pip install -r requirements.txt
python build_dataset.py
```
