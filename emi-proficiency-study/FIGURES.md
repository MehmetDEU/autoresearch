# Figures (publication set)

**One figure only** (publishing economy; Nicol & Pexman, *Displaying Your Findings*).

## Figure 1

`outputs/rstudio/fig1_skill_prepost_ggplot.png`  
→ also copied to `outputs/figures/fig1_skill_mean_decline.png`

Grouped **Pre vs Post** mean scores by skill with 95% CIs of the mean.  
Threshold line = 60. Pattern: Listening & Speaking decline; Reading & Writing do not.

## Not for the manuscript

Anything under `outputs/rstudio/fig2*` or `outputs/tableau/` or archived scatters.

## Rebuild

```bash
Rscript rstudio/fig1_skill_prepost.R
# Python fallback (this environment):
python3 make_styled_figures.py
```
