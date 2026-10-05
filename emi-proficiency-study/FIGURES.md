# Figures (publication set)

Only figures that carry a primary inferential claim are retained for the manuscript.
All other results are reported in tables.

## Scale

Institutional skill and overall scores are on a **0–100** scale. The Preparatory Year Programme pass threshold is **60/100** (interpreted as CEFR B1).

## Publication figures (`outputs/figures/`)

1. `fig1_skill_mean_decline.png` — **grouped Pre vs Post mean scores** by skill (with 95% CI). Listening/Speaking post bars are lower; Reading/Writing are not. Signed-difference bars were retired because readers misread + as gain.
2. `fig2_golem_speaking_paths.png` — Speaking decline associated with underrating gap and translanguaging exposure.

## Tableau / RStudio companions for Figure 1

- `outputs/tableau/fig1_skill_prepost_tableau.csv` — long data for Tableau Public.
- `outputs/tableau/fig1_skill_prepost_wide_tableau.csv` — wide summary for Tableau.
- `rstudio/fig1_skill_prepost.R` — ggplot2 grouped Pre/Post bars (run in RStudio).
- `outputs/rstudio/fig1_skill_prepost_ggplot.png` — R ggplot2 grouped-bar output.

Publication Figure 2 remains the two-panel **scatter** (`fig2_golem_speaking_paths.png`).

## Tables (not figured)

- Descriptives, paired *t*/Wilcoxon by skill, reliability/ICC/IELTS validity
- Correlations with Speaking decline, OLS coefficients, mediation quantities
- Sample composition and lecturer-level exploratory summaries

Optional exploratory dashboards (not for the paper):

```bash
python make_styled_figures.py --archive
```

Rebuild publication figures:

```bash
python make_styled_figures.py
Rscript rstudio/fig1_skill_prepost.R
```
