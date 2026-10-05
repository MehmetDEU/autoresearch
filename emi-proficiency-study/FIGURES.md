# Figures (publication set)

Only figures that carry a primary inferential claim are retained for the manuscript.
All other results are reported in tables.

## Scale

Institutional skill and overall scores are on a **0–100** scale. The Preparatory Year Programme pass threshold is **60/100** (interpreted as CEFR B1).

## Publication figures (`outputs/figures/`)

1. `fig1_skill_mean_decline.png` — **grouped Pre vs Post mean scores** by skill (with 95% CI). Listening/Speaking post bars are lower; Reading/Writing are not. Signed-difference bars were retired because readers misread + as gain.
2. `fig2_golem_speaking_paths.png` — **Listening + Speaking** decline × underrating / translanguaging (2×2; RStudio ggplot preferred).
   Companion: `outputs/rstudio/fig2_all_skills_paths_ggplot.png` shows all four skills (Reading/Writing flat).

## Styled companions (Tableau + RStudio)

### Tableau-style PNGs + CSVs (`outputs/tableau/`)

- `fig1_skill_prepost_tableau_style.png`
- `fig2_golem_paths_tableau_style.png`
- `fig1_skill_prepost_tableau.csv` / `fig1_skill_prepost_wide_tableau.csv`
- `fig2_golem_paths_tableau.csv`

### RStudio / ggplot2 (`rstudio/fig1_and_fig2_styled.R`)

- `outputs/rstudio/fig1_skill_prepost_ggplot.png`
- `outputs/rstudio/fig2_golem_paths_ggplot.png`

Publication Figure 2 remains the two-panel **scatter**.

## Tables (not figured)

- Descriptives, paired *t*/Wilcoxon by skill, reliability/ICC/IELTS validity
- Correlations with Speaking decline, OLS coefficients, mediation quantities
- Sample composition and lecturer-level exploratory summaries

Optional exploratory dashboards (not for the paper):

```bash
python make_styled_figures.py --archive
```

Rebuild publication + styled companions:

```bash
python make_styled_figures.py
Rscript rstudio/fig1_and_fig2_styled.R
```
