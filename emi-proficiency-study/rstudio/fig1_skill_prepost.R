#!/usr/bin/env Rscript
# Figure 1 — Pre vs Post skill means (ggplot2 / RStudio)
# Explicit grouped bars so attrition cannot be misread as gain.
#
# Usage (from emi-proficiency-study/):
#   Rscript rstudio/fig1_skill_prepost.R
#
# Requires: readxl, dplyr, tidyr, ggplot2
# Install once:
#   install.packages(c("readxl", "dplyr", "tidyr", "ggplot2"))

suppressPackageStartupMessages({
  library(readxl)
  library(dplyr)
  library(tidyr)
  library(ggplot2)
})

root <- if (file.exists("EMI_PYP_pre_post_synthetic_N120.xlsx")) {
  normalizePath(".")
} else if (file.exists("../EMI_PYP_pre_post_synthetic_N120.xlsx")) {
  normalizePath("..")
} else {
  stop("Run from emi-proficiency-study/ or rstudio/")
}

xlsx <- file.path(root, "EMI_PYP_pre_post_synthetic_N120.xlsx")
students <- read_excel(xlsx, sheet = "Students")

skills <- c("Listening", "Reading", "Writing", "Speaking", "Overall")

ci95 <- function(x) {
  se <- sd(x) / sqrt(length(x))
  m <- mean(x)
  tcrit <- qt(0.975, df = length(x) - 1)
  c(lo = m - tcrit * se, hi = m + tcrit * se)
}

rows <- lapply(skills, function(sk) {
  pre <- students[[paste0("Pre_", sk)]]
  post <- students[[paste0("Post_", sk)]]
  tt <- t.test(pre, post, paired = TRUE)
  cp <- ci95(pre)
  cq <- ci95(post)
  delta <- mean(pre - post)
  data.frame(
    Skill = sk,
    Time = factor(c("Pre (PYP exit)", "Post (graduation)"),
                  levels = c("Pre (PYP exit)", "Post (graduation)")),
    Mean = c(mean(pre), mean(post)),
    lo = c(cp[["lo"]], cq[["lo"]]),
    hi = c(cp[["hi"]], cq[["hi"]]),
    Delta = delta,
    Sig = ifelse(tt$p.value < 0.001, "p < .001",
                 sprintf("p = %.2f", tt$p.value)),
    stringsAsFactors = FALSE
  )
})

long <- bind_rows(rows)
long$Skill <- factor(long$Skill, levels = skills)

ann <- long %>%
  group_by(Skill) %>%
  summarise(
    y = max(hi) + 0.8,
    Delta = first(Delta),
    Sig = first(Sig),
    .groups = "drop"
  ) %>%
  mutate(
    label = ifelse(
      Delta > 0.05,
      sprintf("down %.1f  %s", Delta, Sig),
      ifelse(Delta < -0.05,
             sprintf("up %.1f  %s", abs(Delta), Sig),
             sprintf("~0  %s", Sig))
    ),
    col = ifelse(Delta > 0.05, "#C0392B",
                 ifelse(Delta < -0.05, "#1E8449", "#555555"))
  )

p <- ggplot(long, aes(x = Skill, y = Mean, fill = Time)) +
  geom_col(position = position_dodge(width = 0.72), width = 0.68,
           colour = "#222222", linewidth = 0.3) +
  geom_errorbar(
    aes(ymin = lo, ymax = hi),
    position = position_dodge(width = 0.72),
    width = 0.18,
    linewidth = 0.5
  ) +
  geom_hline(yintercept = 60, linetype = "dashed", colour = "#888888", linewidth = 0.6) +
  geom_text(
    data = ann,
    aes(x = Skill, y = y, label = label, colour = I(col)),
    inherit.aes = FALSE,
    size = 3,
    fontface = "bold"
  ) +
  scale_fill_manual(values = c("Pre (PYP exit)" = "#4E79A7",
                               "Post (graduation)" = "#F28E2B")) +
  coord_cartesian(ylim = c(55, max(long$hi) + 4.5)) +
  labs(
    title = "Figure 1. Mean Pre and Post scores by skill (N = 120)",
    subtitle = paste(
      "Grouped bars: Pre (PYP exit) vs Post (graduation).",
      "Listening & Speaking decline; Reading & Writing do not.",
      "Error bars = 95% CI of the mean. Threshold = 60."
    ),
    x = NULL,
    y = "Mean score on the 0–100 institutional scale",
    fill = NULL,
    caption = "ggplot2 / RStudio  ·  SYNTHETIC panel"
  ) +
  theme_bw(base_size = 11) +
  theme(
    legend.position = "bottom",
    panel.grid.minor = element_blank(),
    plot.title = element_text(face = "bold", hjust = 0),
    plot.subtitle = element_text(size = 8.5, colour = "#555555")
  )

outdir <- file.path(root, "outputs", "rstudio")
dir.create(outdir, recursive = TRUE, showWarnings = FALSE)
outfile <- file.path(outdir, "fig1_skill_prepost_ggplot.png")
ggsave(outfile, p, width = 9.2, height = 5.8, dpi = 160)
message("Wrote ", outfile)

# Dumbbell companion
wide <- long %>%
  select(Skill, Time, Mean, Delta, Sig) %>%
  pivot_wider(names_from = Time, values_from = Mean)

# restore names after pivot (spaces become awkward)
names(wide) <- gsub(" ", "_", names(wide))
# safer rebuild
wide <- long %>%
  group_by(Skill) %>%
  summarise(
    Pre = Mean[Time == "Pre (PYP exit)"],
    Post = Mean[Time == "Post (graduation)"],
    Delta = first(Delta),
    Sig = first(Sig),
    .groups = "drop"
  )

pd <- ggplot(wide, aes(y = Skill)) +
  geom_segment(aes(x = Pre, xend = Post, yend = Skill,
                   colour = ifelse(Delta > 0.05, "decline", "gain_or_flat")),
               linewidth = 1.2) +
  geom_point(aes(x = Pre), colour = "#4E79A7", size = 3.2) +
  geom_point(aes(x = Post), colour = "#F28E2B", size = 3.2) +
  geom_vline(xintercept = 60, linetype = "dashed", colour = "#888888") +
  scale_colour_manual(values = c(decline = "#C0392B", gain_or_flat = "#1E8449"),
                      guide = "none") +
  labs(
    title = "Figure 1 (RStudio dumbbell). Pre → Post mean scores",
    x = "Mean score (0–100)",
    y = NULL,
    caption = "Blue = Pre; orange = Post. Red = attrition path."
  ) +
  theme_bw(base_size = 11) +
  theme(plot.title = element_text(face = "bold"))

dumbbell <- file.path(outdir, "fig1_skill_prepost_dumbbell_ggplot.png")
ggsave(dumbbell, pd, width = 8.5, height = 5.2, dpi = 160)
message("Wrote ", dumbbell)
