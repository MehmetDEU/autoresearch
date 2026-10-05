#!/usr/bin/env Rscript
# Stylish ggplot2 / RStudio figures for the EMI manuscript
#   Figure 1 — grouped Pre vs Post skill means
#   Figure 2 — Speaking decline scatters (underrating + translanguaging)
#
# Usage (from emi-proficiency-study/):
#   Rscript rstudio/fig1_and_fig2_styled.R

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
outdir <- file.path(root, "outputs", "rstudio")
dir.create(outdir, recursive = TRUE, showWarnings = FALSE)

# Shared theme -----------------------------------------------------------------
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
      strip.text = element_text(face = "bold", colour = "#1B1F24", size = base_size),
      strip.background = element_rect(fill = "#EEF1F4", colour = NA),
      plot.margin = margin(12, 14, 10, 12)
    )
}

# Figure 1 ----------------------------------------------------------------------
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
  fam <- if (sk %in% c("Listening", "Speaking")) "Oral–aural"
         else if (sk %in% c("Reading", "Writing")) "Written" else "Overall"
  data.frame(
    Skill = sk,
    Family = fam,
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
long$Family <- factor(long$Family, levels = c("Oral–aural", "Written", "Overall"))

ann <- long %>%
  group_by(Skill, Family) %>%
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
    subtitle = "ggplot2 / RStudio  ·  Listening & Speaking decline; Reading & Writing do not  ·  95% CI  ·  threshold = 60",
    x = NULL, y = "Mean score (0–100 institutional scale)",
    caption = "SYNTHETIC panel for manuscript scaffolding", fill = NULL
  ) +
  theme_emi()

ggsave(file.path(outdir, "fig1_skill_prepost_ggplot.png"), p1,
       width = 9.6, height = 6.0, dpi = 180, bg = "#F7F9FB")
message("Wrote fig1_skill_prepost_ggplot.png")

# Figure 2 — oral–aural scatters (Listening + Speaking) ----------------------------
mk_panel <- function(skill, pred_name, pred_vals, letter) {
  data.frame(
    Skill = skill,
    Predictor_name = pred_name,
    Panel = paste0(letter, ". ", skill, "  ·  ", pred_name),
    Predictor = pred_vals,
    Decline = students[[paste0("Decline_", skill)]],
    stringsAsFactors = FALSE
  )
}

long2 <- bind_rows(
  mk_panel("Listening", "Underrating gap", students$Underrating_Gap, "A"),
  mk_panel("Listening", "Translanguaging %", students$TL_percent, "B"),
  mk_panel("Speaking", "Underrating gap", students$Underrating_Gap, "C"),
  mk_panel("Speaking", "Translanguaging %", students$TL_percent, "D")
)
long2$Skill <- factor(long2$Skill, levels = c("Listening", "Speaking"))
long2$Predictor_name <- factor(long2$Predictor_name,
                               levels = c("Underrating gap", "Translanguaging %"))
long2$Panel <- factor(long2$Panel, levels = unique(long2$Panel))

stats_lab <- long2 %>%
  group_by(Panel, Skill, Predictor_name) %>%
  summarise(
    r = cor(Predictor, Decline),
    p = cor.test(Predictor, Decline)$p.value,
    .groups = "drop"
  ) %>%
  mutate(
    label = ifelse(p < 0.001, sprintf("r = %.2f, p < .001", r),
                   sprintf("r = %.2f, p = %.3f", r, p)),
    x = -Inf, y = Inf
  )

p2 <- ggplot(long2, aes(Predictor, Decline)) +
  geom_hline(yintercept = 0, linetype = "dotted", colour = "#8A949E", linewidth = 0.55) +
  geom_point(aes(colour = Skill), alpha = 0.55, size = 2.0, stroke = 0.15, shape = 16) +
  geom_smooth(method = "lm", formula = y ~ x, colour = "#C0392B",
              fill = "#E8B4B0", alpha = 0.35, linewidth = 1.0, se = TRUE) +
  geom_label(
    data = stats_lab, aes(x = x, y = y, label = label),
    inherit.aes = FALSE, hjust = -0.04, vjust = 1.15, size = 2.7,
    fontface = "bold", fill = "white", label.size = 0.15, colour = "#1B1F24"
  ) +
  facet_wrap(~ Panel, scales = "free_x", nrow = 2) +
  scale_colour_manual(values = c(Listening = "#3D6F9C", Speaking = "#E08A2E"), guide = "none") +
  labs(
    title = "Figure 2. Oral–aural attrition paths: Listening and Speaking",
    subtitle = paste(
      "ggplot2 / RStudio  ·  rows = skill; columns = underrating vs translanguaging",
      "·  positive = attrition (pre − post)  ·  95% CI band  ·  N = 120"
    ),
    x = "Predictor", y = "Skill decline (pre − post; 0–100 scale)",
    caption = "Reading/Writing associations are near zero (see companion all-skills figure). SYNTHETIC panel."
  ) +
  theme_emi(base_size = 10.5)

ggsave(file.path(outdir, "fig2_golem_paths_ggplot.png"), p2,
       width = 10.8, height = 8.2, dpi = 180, bg = "#F7F9FB")
message("Wrote fig2_golem_paths_ggplot.png")

# Companion: all four skills × two predictors (archive / supplement)
long_all <- bind_rows(lapply(c("Listening", "Reading", "Writing", "Speaking"), function(sk) {
  bind_rows(
    data.frame(
      Skill = sk,
      Predictor_name = "Underrating gap",
      Predictor = students$Underrating_Gap,
      Decline = students[[paste0("Decline_", sk)]]
    ),
    data.frame(
      Skill = sk,
      Predictor_name = "Translanguaging %",
      Predictor = students$TL_percent,
      Decline = students[[paste0("Decline_", sk)]]
    )
  )
}))
long_all$Skill <- factor(long_all$Skill, levels = c("Listening", "Reading", "Writing", "Speaking"))
long_all$Predictor_name <- factor(long_all$Predictor_name,
                                  levels = c("Underrating gap", "Translanguaging %"))

stats_all <- long_all %>%
  group_by(Skill, Predictor_name) %>%
  summarise(
    r = cor(Predictor, Decline),
    p = cor.test(Predictor, Decline)$p.value,
    .groups = "drop"
  ) %>%
  mutate(
    label = ifelse(p < 0.001, sprintf("r = %.2f***", r),
            ifelse(p < 0.01, sprintf("r = %.2f**", r),
            ifelse(p < 0.05, sprintf("r = %.2f*", r), sprintf("r = %.2f", r)))),
    x = -Inf, y = Inf
  )

p_all <- ggplot(long_all, aes(Predictor, Decline)) +
  geom_hline(yintercept = 0, linetype = "dotted", colour = "#8A949E", linewidth = 0.45) +
  geom_point(colour = "#3D6F9C", alpha = 0.4, size = 1.5) +
  geom_smooth(method = "lm", formula = y ~ x, colour = "#C0392B",
              fill = "#E8B4B0", alpha = 0.3, linewidth = 0.85, se = TRUE) +
  geom_text(
    data = stats_all, aes(x = x, y = y, label = label),
    inherit.aes = FALSE, hjust = -0.05, vjust = 1.4, size = 2.5,
    fontface = "bold", colour = "#1B1F24"
  ) +
  facet_grid(Skill ~ Predictor_name, scales = "free_x") +
  labs(
    title = "Supplement. Decline × underrating / translanguaging for all four skills",
    subtitle = "Only Listening and Speaking show reliable positive slopes; Reading/Writing are flat  ·  N = 120",
    x = "Predictor", y = "Decline (pre − post)",
    caption = "ggplot2 / RStudio companion (not required for the main manuscript)"
  ) +
  theme_emi(base_size = 10)

ggsave(file.path(outdir, "fig2_all_skills_paths_ggplot.png"), p_all,
       width = 10.5, height = 9.5, dpi = 170, bg = "#F7F9FB")
message("Wrote fig2_all_skills_paths_ggplot.png")

# Promote RStudio outputs to publication figures (preferred look)
pub <- file.path(root, "outputs", "figures")
dir.create(pub, recursive = TRUE, showWarnings = FALSE)
file.copy(file.path(outdir, "fig1_skill_prepost_ggplot.png"),
          file.path(pub, "fig1_skill_mean_decline.png"), overwrite = TRUE)
file.copy(file.path(outdir, "fig2_golem_paths_ggplot.png"),
          file.path(pub, "fig2_golem_speaking_paths.png"), overwrite = TRUE)
message("Copied RStudio figures into outputs/figures/ (publication set)")
