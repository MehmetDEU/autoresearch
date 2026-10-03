# Styled figures

Generated from the synthetic Excel panel. Two visual languages:

## Tableau-style (`outputs/tableau/`)

KPI cards, clean dashboard chrome, Tableau 10 colours, left-aligned titles.

- `outputs/tableau/tableau_dashboard_overview.png`
- `outputs/tableau/tableau_lecturer_dose_response.png`
- `outputs/tableau/tableau_sample_composition.png`

## ggplot2 / RStudio-style (`outputs/rstudio/`)

White panels, light grey grids, black axes, facet strips — the look you get from `ggplot2` + `theme_bw()` / `theme_minimal()` in RStudio.

- `outputs/rstudio/rstudio_skill_violins.png`
- `outputs/rstudio/rstudio_skill_decline_ci.png`
- `outputs/rstudio/rstudio_golem_paths.png`
- `outputs/rstudio/rstudio_paired_slopegraph.png`
- `outputs/rstudio/rstudio_mechanism_heatmap.png`
- `outputs/rstudio/rstudio_ielts_concurrent.png`
- `outputs/rstudio/rstudio_difference_hist.png`

Rebuild:

```bash
python make_styled_figures.py
```
