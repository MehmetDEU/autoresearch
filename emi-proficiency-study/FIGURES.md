# Figures (publication set — quantitative strand)

Only **Figure 1** is retained for the quantitative manuscript (RQ1).

Explanatory paths (translanguaging, underrating, etc.) belong to the **qualitative** strand (RQ2–RQ3) and are not figured statistically here.

## Scale

Institutional skill and overall scores are on a **0–100** scale.  
PYP pass threshold = **60/100** (≈ CEFR B1).

## Publication figure

1. `outputs/rstudio/fig1_skill_prepost_ggplot.png` (preferred) — grouped Pre vs Post means by skill with 95% CI.  
   Listening/Speaking decline; Reading/Writing do not.

Copied to `outputs/figures/fig1_skill_mean_decline.png` for the Word draft.

## Rebuild

```bash
Rscript rstudio/fig1_and_fig2_styled.R   # Fig 1 (+ optional archive scatters)
python write_methods_results_docx.py
```

Optional archive scatters under `outputs/rstudio/` are **not** part of the current quantitative RQs.
