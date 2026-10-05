#!/usr/bin/env Rscript
# Figure 1 only — Pre vs Post skill means (ggplot2 / RStudio)
# Matches RQ1 quantitative strand (paired proficiency comparison).
#
# Usage (from emi-proficiency-study/):
#   Rscript rstudio/fig1_and_fig2_styled.R

suppressPackageStartupMessages({
  library(readxl)
  library(dplyr)
  library(ggplot2)
})

root <- if (file.exists("EMI_quantitative_prepost_N120.xlsx") ||
             file.exists("EMI_PYP_pre_post_synthetic_N120.xlsx")) {
  normalizePath(".")
} else if (file.exists("../EMI_quantitative_prepost_N120.xlsx") ||
           file.exists("../EMI_PYP_pre_post_synthetic_N120.xlsx")) {
  normalizePath("..")
} else {
  stop("Run from emi-proficiency-study/ or rstudio/")
}

xlsx <- if (file.exists(file.path(root, "EMI_quantitative_prepost_N120.xlsx"))) {
  file.path(root, "EMI_quantitative_prepost_N120.xlsx")
} else {
  file.path(root, "EMI_PYP_pre_post_synthetic_N120.xlsx")
}

students <- read_excel(xlsx, sheet = "Students")
outdir <- file.path(root, "outputs", "rstudio")
dir.create(outdir, recursive = TRUE, showWarnings = FALSE)
pub <- file.path(root, "outputs", "figures")
dir.create(pub, recursive = TRUE, showWarnings = FALSE)

theme_emi <- function(base_size = 11) {
  theme_minimal(base_size = base_size, base_family = "sans") %+replace%
    theme(
      plot.title = element_text(face = "bold", hjust = 0, colour = "#1B1F24",
                                size = base_size + 2, margin = margin(b = 4)),
      plot.subtitle = element_text(hjust = 0, colour = "#5C6670", size = base_size - 1.5,
                                   margin = margin(b = 10)),
      plot.caption = element_text(colour = "#8A949E", size = base_size - 2.5, hjust = 0),
      axis.title = element_text(colour = "#4A5560", size = base_size - 0.5),
      axis.text = element_text(colour = "#4A5560"),
      panel.grid.minor = element_blank(),
      panel.grid.major = element_line(colour = "#EEF1F4", linewidth = 0.5),
      legend.position = "bottom",
      legend.title = element_blank(),
      plot.background = element_rect(fill = "#F7F9FB", colour = NA),
      panel.background = element_rect(fill = "white", colour = NA),
      plot.margin = margin(12, 14, 10, 12)
    )
}

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
  cp <- ci95(pre); cq <- ci95(post)
  delta <- mean(pre - post)
  data.frame(
    Skill = sk,
    Time = factor(c("Pre (PYP exit)", "Post (graduation)"),
                  levels = c("Pre (PYP exit)", "Post (graduation)")),
    Mean = c(mean(pre), mean(post)),
    lo = c(cp[["lo"]], cq[["lo"]]),
    hi = c(cp[["hi"]], cq[["hi"]]),
    Delta = delta,
    Sig = ifelse(tt$p.value < 0.001, "p < .001", sprintf("p = %.2f", tt$p.value)),
    stringsAsFactors = FALSE
  )
})
long <- bind_rows(rows)
long$Skill <- factor(long$Skill, levels = skills)

ann <- long %>%
  group_by(Skill) %>%
  summarise(
    y = max(hi) + 0.9,
    Delta = first(Delta),
    Sig = first(Sig),
    .groups = "drop"
  ) %>%
  mutate(
    label = ifelse(Delta > 0.05, sprintf("down %.1f  %s", Delta, Sig),
            ifelse(Delta < -0.05, sprintf("up %.1f  %s", abs(Delta), Sig),
                   sprintf("~0  %s", Sig))),
    col = ifelse(Delta > 0.05, "#C0392B",
          ifelse(Delta < -0.05, "#1E8449", "#555555"))
  )

p1 <- ggplot(long, aes(x = Skill, y = Mean, fill = Time)) +
  geom_col(position = position_dodge(width = 0.72), width = 0.66,
           colour = "white", linewidth = 0.4) +
  geom_errorbar(aes(ymin = lo, ymax = hi),
                position = position_dodge(width = 0.72), width = 0.16,
                linewidth = 0.45, colour = "#2C3640") +
  geom_hline(yintercept = 60, linetype = "dashed", colour = "#8A949E", linewidth = 0.6) +
  geom_label(
    data = ann, aes(x = Skill, y = y, label = label, colour = I(col)),
    inherit.aes = FALSE, size = 2.85, fontface = "bold",
    fill = "#FFFFFF", label.size = 0,
    label.padding = unit(0.18, "lines")
  ) +
  scale_fill_manual(values = c("Pre (PYP exit)" = "#3D6F9C",
                               "Post (graduation)" = "#E08A2E")) +
  coord_cartesian(ylim = c(55, max(long$hi) + 5)) +
  labs(
    title = "Figure 1. Mean Pre and Post scores by skill (N = 120)",
    subtitle = "RQ1 · Listening & Speaking decline; Reading & Writing do not · 95% CI · threshold = 60",
    x = NULL, y = "Mean score (0–100 institutional scale)",
    caption = "Quantitative strand only (explanatory mixed methods QUANT → QUAL)", fill = NULL
  ) +
  theme_emi()

outfile <- file.path(outdir, "fig1_skill_prepost_ggplot.png")
ggsave(outfile, p1, width = 9.6, height = 6.0, dpi = 180, bg = "#F7F9FB")
file.copy(outfile, file.path(pub, "fig1_skill_mean_decline.png"), overwrite = TRUE)
message("Wrote ", outfile)
message("Copied to outputs/figures/fig1_skill_mean_decline.png")
