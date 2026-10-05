# Figures (publication set)

Only figures that carry a primary inferential claim are retained for the manuscript.
All other results are reported in tables.

## Scale

Institutional skill and overall scores are on a **0–100** scale. The Preparatory Year Programme pass threshold is **60/100** (interpreted as CEFR B1).

## Publication figures (`outputs/figures/`)

1. `fig1_skill_mean_decline.png` — mean pre−post change by skill with 95% CI (oral–aural decline vs non-significant written change).
2. `fig2_golem_speaking_paths.png` — Speaking decline associated with underrating gap and translanguaging exposure.

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
```
