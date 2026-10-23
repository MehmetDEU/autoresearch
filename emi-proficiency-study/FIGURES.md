# Figures (publication set)

**One figure only** (publishing economy; Nicol & Pexman, *Displaying Your Findings*).

## Figure 1

`outputs/rstudio/fig1_skill_prepost_ggplot.png`  
→ also copied to `outputs/figures/fig1_skill_mean_decline.png`

Grouped **Pre vs Post** mean scores by skill with 95% CIs of the mean.  
Threshold line = 60. Pattern: Listening & Speaking decline; Reading & Writing do not.

**Style (journal polish):** slate / copper bars, white ground, lean Post−Pre labels with APA stars (no family shading or badge boxes). Prior version archived as `outputs/archive/fig1_*_before_polish.png`.

## Not for the manuscript

Anything under `outputs/rstudio/fig2*` or `outputs/tableau/` or archived scatters.

## Rebuild

```bash
python3 polish_fig1.py
# or R:
Rscript rstudio/fig1_skill_prepost.R
```
