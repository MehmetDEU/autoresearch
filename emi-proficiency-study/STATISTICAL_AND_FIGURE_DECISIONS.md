# Statistical and figure decisions (publishing economy)

## Comparison: paired *t* vs ANOVA / MANOVA

| Option | What it answers | Fit to RQ1 | Nicol presentation |
| --- | --- | --- | --- |
| **Paired-samples *t* (chosen)** | Did each skill (and Overall) change Pre→Post? | Direct | *Presenting Your Findings*: *t* Test of means — Play-It-Safe multi-*t* table |
| RM-ANOVA Time × Skill | Do skills change *differently*? | Useful omnibus, extra table | ANOVA chapter — more economy cost |
| MANOVA on skill vector | Did the multivariate profile change? | Omnibus only; still needs univariate follow-ups | MANOVA chapter — heaviest for little gain |

**Decision:** Use **paired-samples *t* tests** (Wilcoxon companions in table note) for Listening, Reading, Writing, Speaking, and Overall.  
RQ1 asks for **skill-specific** change; paired *t* is the clearest and most economical report. MANOVA/RM-ANOVA are not required for the manuscript story (Speaking > Listening decline; R/W n.s.).

## Figure economy (*Displaying Your Findings*)

Nicol & Pexman: use a figure only when it clarifies a pattern not already transparent in tables; prefer lean bar graphs with clear legends / error bars.

**Publication set = 1 figure only**

- **Figure 1.** Grouped Pre vs Post mean bars by skill, 95% CI of the mean, threshold = 60 (RStudio / ggplot2).  
- **Removed from manuscript:** Golem/translanguaging scatters, all-skills path grids, Tableau dashboards (archive only if kept on disk).

## Tables (*Presenting Your Findings* Play-It-Safe)

1. **Table 1** — Pre/Post *M* and *SD* by skill (means chapter)  
2. **Table 2** — Paired *t*: *M*diff, *SD*diff, *t*, *df*, *p*, *d_z*, 95% CI (*t*-test Play-It-Safe)

## Preserved attrition pattern

Speaking > Listening (both significant); Reading & Writing non-significant slight gains.
