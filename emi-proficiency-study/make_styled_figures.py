#!/usr/bin/env python3
"""Tableau-style and ggplot2/RStudio-style figures for the EMI panel.

Outputs land in outputs/tableau/ and outputs/rstudio/ (plus /opt/cursor/artifacts).
All charts are drawn from the synthetic Students sheet — same data as the Excel workbook.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.gridspec import GridSpec
from plotnine import (
    aes,
    element_blank,
    element_line,
    element_rect,
    element_text,
    facet_wrap,
    geom_boxplot,
    geom_hline,
    geom_jitter,
    geom_point,
    geom_smooth,
    geom_violin,
    ggplot,
    labs,
    scale_color_manual,
    scale_fill_manual,
    theme,
)
from scipy import stats

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs"
TAB = OUT / "tableau"
RST = OUT / "rstudio"
ART = Path("/opt/cursor/artifacts")
XLSX = ROOT / "EMI_PYP_pre_post_synthetic_N120.xlsx"

# Tableau 10-inspired palette
T = {
    "blue": "#4E79A7",
    "orange": "#F28E2B",
    "red": "#E15759",
    "teal": "#76B7B2",
    "green": "#59A14F",
    "yellow": "#EDC948",
    "purple": "#B07AA1",
    "brown": "#9C755F",
    "pink": "#FF9DA7",
    "gray": "#BAB0AC",
    "ink": "#333333",
    "muted": "#666666",
    "grid": "#E6E6E6",
    "bg": "#F7F7F7",
    "card": "#FFFFFF",
    "header": "#1F4E79",
}

# ggplot2-ish greys
GG = {
    "ink": "#1A1A1A",
    "axis": "#4D4D4D",
    "grid": "#D9D9D9",
    "panel": "#FFFFFF",
    "strip": "#F0F0F0",
}


def load() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    students = pd.read_excel(XLSX, "Students")
    lecturers = pd.read_excel(XLSX, "Lecturers")
    ielts = pd.read_excel(XLSX, "IELTS_subsample")
    return students, lecturers, ielts


def long_skills(s: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for skill in ["Listening", "Reading", "Writing", "Speaking", "Overall"]:
        for time, col in [("Pre (PYP exit)", f"Pre_{skill}"), ("Post (graduation)", f"Post_{skill}")]:
            for val in s[col]:
                rows.append({"Skill": skill, "Time": time, "Score": float(val)})
    return pd.DataFrame(rows)


def theme_rstudio():
    """Close visual cousin of ggplot2 theme_bw / theme_minimal as seen in RStudio."""
    return theme(
        text=element_text(family="DejaVu Sans", color=GG["ink"], size=10),
        plot_title=element_text(size=13, weight="bold", ha="left", margin={"b": 8}),
        plot_subtitle=element_text(size=9.5, color="#555555", ha="left", margin={"b": 10}),
        axis_title=element_text(size=10),
        axis_text=element_text(size=9, color=GG["axis"]),
        axis_line=element_line(color=GG["ink"], size=0.6),
        panel_background=element_rect(fill=GG["panel"], color=GG["ink"], size=0.6),
        panel_border=element_rect(color=GG["ink"], fill=None, size=0.6),
        panel_grid_major=element_line(color=GG["grid"], size=0.4),
        panel_grid_minor=element_blank(),
        strip_background=element_rect(fill=GG["strip"], color=GG["ink"], size=0.5),
        strip_text=element_text(size=10, weight="bold"),
        legend_background=element_rect(fill="white", color=GG["ink"], size=0.4),
        legend_title=element_text(size=9, weight="bold"),
        figure_size=(8.2, 5.4),
        dpi=150,
    )


def save_ggplot(plot, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    plot.save(str(path), dpi=150, verbose=False)
    return path


def card(ax, title: str) -> None:
    ax.set_facecolor(T["card"])
    ax.set_title(title, loc="left", fontsize=11, fontweight="bold", color=T["header"], pad=8)
    for spine in ax.spines.values():
        spine.set_color("#DDDDDD")
    ax.tick_params(colors=T["muted"], labelsize=8)
    ax.yaxis.label.set_color(T["muted"])
    ax.xaxis.label.set_color(T["muted"])
    ax.grid(True, axis="y", color=T["grid"], linewidth=0.8)
    ax.set_axisbelow(True)


def kpi(ax, value: str, label: str, color: str) -> None:
    ax.set_facecolor(T["card"])
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.text(0.5, 0.62, value, ha="center", va="center", fontsize=22, fontweight="bold", color=color, transform=ax.transAxes)
    ax.text(0.5, 0.28, label, ha="center", va="center", fontsize=8.5, color=T["muted"], transform=ax.transAxes)
    ax.add_patch(
        mpatches.FancyBboxPatch(
            (0.04, 0.08),
            0.92,
            0.84,
            transform=ax.transAxes,
            boxstyle="round,pad=0.02,rounding_size=0.04",
            linewidth=1.2,
            edgecolor="#E0E0E0",
            facecolor="none",
        )
    )


# ---------------------------------------------------------------------------
# Tableau-style dashboard
# ---------------------------------------------------------------------------

def make_tableau_dashboard(s: pd.DataFrame, lect: pd.DataFrame) -> Path:
    TAB.mkdir(parents=True, exist_ok=True)
    pre, post = s["Pre_Overall"], s["Post_Overall"]
    speak_pre, speak_post = s["Pre_Speaking"], s["Post_Speaking"]
    t_speak = stats.ttest_rel(speak_pre, speak_post)
    d_speak = (speak_pre - speak_post).mean() / (speak_pre - speak_post).std(ddof=1)
    r_u = stats.pearsonr(s["Underrating_Gap"], s["Decline_Speaking"])
    r_t = stats.pearsonr(s["TL_percent"], s["Decline_Speaking"])

    fig = plt.figure(figsize=(14.5, 9.2), facecolor=T["bg"])
    fig.suptitle(
        "EMI proficiency panel  ·  Oral–aural attrition (L+S)  ·  SYNTHETIC N = 120",
        fontsize=15,
        fontweight="bold",
        color=T["header"],
        x=0.01,
        ha="left",
        y=0.98,
    )
    fig.text(
        0.01,
        0.945,
        "Paired PYP-exit vs graduation  |  Listening + Speaking decline; Reading/Writing not significantly down  |  B1 threshold = 60",
        fontsize=9,
        color=T["muted"],
    )

    gs = GridSpec(
        3,
        4,
        figure=fig,
        height_ratios=[0.85, 1.35, 1.45],
        hspace=0.42,
        wspace=0.28,
        left=0.05,
        right=0.98,
        top=0.90,
        bottom=0.07,
    )

    # KPI row
    ax0 = fig.add_subplot(gs[0, 0])
    kpi(ax0, f"{(speak_pre - speak_post).mean():.1f}", "Speaking mean decline (points)", T["red"])
    ax1 = fig.add_subplot(gs[0, 1])
    kpi(ax1, f"p < .001" if t_speak.pvalue < 0.001 else f"p = {t_speak.pvalue:.3f}", f"Speaking paired t  ·  d_z = {d_speak:.2f}", T["orange"])
    ax2 = fig.add_subplot(gs[0, 2])
    kpi(ax2, f"{s['Decline_Listening'].mean():.1f}", "Listening mean decline", T["blue"])
    ax3 = fig.add_subplot(gs[0, 3])
    kpi(ax3, f"r = {r_t.statistic:.2f}", "Speaking decline × translanguaging %", T["purple"])

    # Pre/post box + swarm
    ax = fig.add_subplot(gs[1, 0:2])
    card(ax, "Overall score distribution")
    data = [pre, post]
    bp = ax.boxplot(
        data,
        positions=[0, 1],
        widths=0.45,
        patch_artist=True,
        showfliers=False,
        medianprops={"color": T["ink"], "linewidth": 1.4},
        whiskerprops={"color": T["muted"]},
        capprops={"color": T["muted"]},
        boxprops={"linewidth": 1.0},
    )
    for patch, color in zip(bp["boxes"], [T["blue"], T["orange"]]):
        patch.set_facecolor(color)
        patch.set_alpha(0.85)
    rng = np.random.default_rng(7)
    for i, series in enumerate(data):
        x = i + rng.uniform(-0.12, 0.12, size=series.size)
        ax.scatter(x, series, s=12, alpha=0.35, color=T["ink"], zorder=3, linewidths=0)
    ax.axhline(60, color=T["red"], ls="--", lw=1.2, label="B1 threshold (60)")
    ax.set_xticks([0, 1], ["Pre (PYP exit)", "Post (graduation)"])
    ax.set_ylabel("Institutional overall (0–100)")
    ax.set_ylim(48, 90)
    ax.legend(frameon=False, fontsize=8, loc="upper right")

    # Skill decline bars
    ax = fig.add_subplot(gs[1, 2:4])
    card(ax, "Mean change by skill (pre − post; + = attrition)")
    skills = ["Listening", "Reading", "Writing", "Speaking", "Overall"]
    means = [s[f"Decline_{sk}"].mean() for sk in skills]
    colors = [T["orange"], T["teal"], T["green"], T["red"], T["blue"]]
    bars = ax.bar(skills, means, color=colors, width=0.65, edgecolor="white")
    for b, m in zip(bars, means):
        ytxt = m + (0.12 if m >= 0 else -0.25)
        ax.text(b.get_x() + b.get_width() / 2, ytxt, f"{m:.2f}", ha="center", va="bottom" if m >= 0 else "top", fontsize=8, color=T["ink"])
    ax.axhline(0, color=T["ink"], lw=0.8)
    ax.set_ylabel("Mean decline (points); negative = gain")
    ymin = min(0, min(means)) - 0.8
    ymax = max(means) * 1.25 + 0.4
    ax.set_ylim(ymin, ymax)

    # Mechanism scatters
    ax = fig.add_subplot(gs[2, 0:2])
    card(ax, "Golem inaccuracy → Speaking attrition")
    ax.scatter(s["Underrating_Gap"], s["Decline_Speaking"], s=28, alpha=0.75, c=T["blue"], edgecolors="white", linewidths=0.4)
    z = np.polyfit(s["Underrating_Gap"], s["Decline_Speaking"], 1)
    xs = np.linspace(s["Underrating_Gap"].min(), s["Underrating_Gap"].max(), 80)
    ax.plot(xs, np.polyval(z, xs), color=T["red"], lw=2.2)
    ax.set_xlabel("Underrating gap (actual − lecturer estimate)")
    ax.set_ylabel("Speaking decline")
    ax.text(
        0.03,
        0.95,
        f"r = {r_u.statistic:.2f}, p < .001",
        transform=ax.transAxes,
        va="top",
        fontsize=9,
        color=T["header"],
        fontweight="bold",
        bbox={"boxstyle": "round,pad=0.25", "facecolor": "white", "edgecolor": "#E0E0E0"},
    )

    ax = fig.add_subplot(gs[2, 2:4])
    card(ax, "Translanguaging → Speaking attrition")
    ax.scatter(s["TL_percent"], s["Decline_Speaking"], s=28, alpha=0.75, c=T["orange"], edgecolors="white", linewidths=0.4)
    z = np.polyfit(s["TL_percent"], s["Decline_Speaking"], 1)
    xs = np.linspace(s["TL_percent"].min(), s["TL_percent"].max(), 80)
    ax.plot(xs, np.polyval(z, xs), color=T["red"], lw=2.2)
    ax.set_xlabel("% of content-course time in Turkish")
    ax.set_ylabel("Speaking decline")
    ax.text(
        0.03,
        0.95,
        f"r = {r_t.statistic:.2f}, p < .001",
        transform=ax.transAxes,
        va="top",
        fontsize=9,
        color=T["header"],
        fontweight="bold",
        bbox={"boxstyle": "round,pad=0.25", "facecolor": "white", "edgecolor": "#E0E0E0"},
    )

    path = TAB / "tableau_dashboard_overview.png"
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


def make_tableau_lecturer_dashboard(s: pd.DataFrame, lect: pd.DataFrame) -> Path:  # noqa: ARG001 — s used when Speaking means absent
    fig = plt.figure(figsize=(13.5, 8.0), facecolor=T["bg"])
    fig.suptitle(
        "Lecturer-level dose–response  ·  Tableau-style  ·  SYNTHETIC",
        fontsize=14,
        fontweight="bold",
        color=T["header"],
        x=0.02,
        ha="left",
        y=0.97,
    )
    fig.text(0.02, 0.935, "12 content lecturers × 10 students  |  Class means of underrating, L1 use, and proficiency decline", fontsize=9, color=T["muted"])
    gs = GridSpec(2, 2, figure=fig, hspace=0.35, wspace=0.25, left=0.07, right=0.97, top=0.88, bottom=0.09)

    short = {
        "Mechanical Engineering": "ME",
        "Chemical Engineering": "ChE",
        "Electrical-Electronics Engineering": "EEE",
    }
    lect = lect.copy()
    if "Mean_Decline_Speaking" not in lect.columns:
        speak_by = s.groupby("Lecturer_ID")["Decline_Speaking"].mean()
        lect["Mean_Decline_Speaking"] = lect["Lecturer_ID"].map(speak_by)
    lect["Major_short"] = lect["Major"].map(short)
    palette = {"ME": T["blue"], "ChE": T["orange"], "EEE": T["teal"]}

    ax = fig.add_subplot(gs[0, 0])
    card(ax, "Class-mean underrating → Speaking decline")
    for m, g in lect.groupby("Major_short"):
        ax.scatter(g["Mean_Underrating_Gap"], g["Mean_Decline_Speaking"], s=70, c=palette[m], label=m, edgecolors="white", linewidths=0.6, zorder=3)
    z = np.polyfit(lect["Mean_Underrating_Gap"], lect["Mean_Decline_Speaking"], 1)
    xs = np.linspace(lect["Mean_Underrating_Gap"].min(), lect["Mean_Underrating_Gap"].max(), 50)
    ax.plot(xs, np.polyval(z, xs), color=T["red"], lw=2)
    r = stats.pearsonr(lect["Mean_Underrating_Gap"], lect["Mean_Decline_Speaking"])
    ax.set_xlabel("Mean underrating gap")
    ax.set_ylabel("Mean Speaking decline")
    ax.legend(frameon=False, fontsize=8, title="Major")
    ax.text(0.03, 0.95, f"r = {r.statistic:.2f}, p = {r.pvalue:.3f}", transform=ax.transAxes, va="top", fontsize=9, color=T["header"], fontweight="bold")

    ax = fig.add_subplot(gs[0, 1])
    card(ax, "Class-mean translanguaging → Speaking decline")
    for m, g in lect.groupby("Major_short"):
        ax.scatter(g["Mean_TL_percent"], g["Mean_Decline_Speaking"], s=70, c=palette[m], label=m, edgecolors="white", linewidths=0.6, zorder=3)
    z = np.polyfit(lect["Mean_TL_percent"], lect["Mean_Decline_Speaking"], 1)
    xs = np.linspace(lect["Mean_TL_percent"].min(), lect["Mean_TL_percent"].max(), 50)
    ax.plot(xs, np.polyval(z, xs), color=T["red"], lw=2)
    r = stats.pearsonr(lect["Mean_TL_percent"], lect["Mean_Decline_Speaking"])
    ax.set_xlabel("Mean % class time in Turkish")
    ax.set_ylabel("Mean Speaking decline")
    ax.legend(frameon=False, fontsize=8, title="Major")
    ax.text(0.03, 0.95, f"r = {r.statistic:.2f}, p = {r.pvalue:.3f}", transform=ax.transAxes, va="top", fontsize=9, color=T["header"], fontweight="bold")

    ax = fig.add_subplot(gs[1, :])
    card(ax, "Lecturers ranked by class-mean Speaking decline")
    order = lect.sort_values("Mean_Decline_Speaking")
    colors = [palette[m] for m in order["Major_short"]]
    ax.barh(order["Lecturer_ID"], order["Mean_Decline_Speaking"], color=colors, edgecolor="white", height=0.7)
    ax.axvline(0, color=T["ink"], lw=0.8)
    ax.set_xlabel("Mean Speaking decline (positive = lower Speaking at graduation)")
    handles = [mpatches.Patch(color=c, label=k) for k, c in palette.items()]
    ax.legend(handles=handles, frameon=False, fontsize=8, title="Major", loc="lower right")

    path = TAB / "tableau_lecturer_dose_response.png"
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


def make_tableau_demographics(s: pd.DataFrame) -> Path:
    fig = plt.figure(figsize=(12.5, 6.8), facecolor=T["bg"])
    fig.suptitle("Sample composition  ·  Tableau-style  ·  SYNTHETIC", fontsize=14, fontweight="bold", color=T["header"], x=0.02, ha="left", y=0.97)
    gs = GridSpec(1, 3, figure=fig, wspace=0.28, left=0.06, right=0.98, top=0.86, bottom=0.12)

    ax = fig.add_subplot(gs[0, 0])
    card(ax, "Gender")
    counts = s["Gender"].value_counts()
    ax.pie(
        counts,
        labels=[f"{i}\n{c} ({c/len(s)*100:.0f}%)" for i, c in counts.items()],
        colors=[T["blue"], T["pink"]],
        startangle=90,
        wedgeprops={"width": 0.45, "edgecolor": "white"},
        textprops={"fontsize": 9, "color": T["ink"]},
    )
    ax.set_aspect("equal")

    ax = fig.add_subplot(gs[0, 1])
    card(ax, "Engineering major")
    majors = s["Major"].value_counts()
    labels = ["Mechanical", "Chemical", "Electrical-\nElectronics"]
    ax.bar(labels, majors.values, color=[T["blue"], T["orange"], T["teal"]], edgecolor="white")
    for i, v in enumerate(majors.values):
        ax.text(i, v + 0.8, str(v), ha="center", fontsize=9, color=T["ink"])
    ax.set_ylim(0, 50)
    ax.set_ylabel("Students")

    ax = fig.add_subplot(gs[0, 2])
    card(ax, "Age at graduation")
    ages = s["Age_at_post_graduation"].value_counts().sort_index()
    ax.bar(ages.index.astype(str), ages.values, color=T["purple"], edgecolor="white")
    for i, (age, v) in enumerate(ages.items()):
        ax.text(i, v + 0.6, str(v), ha="center", fontsize=9, color=T["ink"])
    ax.set_ylabel("Students")
    ax.set_xlabel("Years")

    path = TAB / "tableau_sample_composition.png"
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


# ---------------------------------------------------------------------------
# RStudio / ggplot2-style figures (plotnine)
# ---------------------------------------------------------------------------

def make_rstudio_prepost(s: pd.DataFrame) -> Path:
    long = long_skills(s)
    long = long[long["Skill"] != "Overall"].copy()
    long["Time"] = pd.Categorical(long["Time"], categories=["Pre (PYP exit)", "Post (graduation)"], ordered=True)
    long["Skill"] = pd.Categorical(long["Skill"], categories=["Listening", "Reading", "Writing", "Speaking"], ordered=True)

    p = (
        ggplot(long, aes("Time", "Score", fill="Time"))
        + geom_violin(alpha=0.55, color="#333333", size=0.3, width=0.9, show_legend=False)
        + geom_boxplot(width=0.18, outlier_alpha=0, fill="white", color="#222222", size=0.5, show_legend=False)
        + geom_jitter(aes(color="Time"), width=0.08, height=0, size=1.1, alpha=0.35, show_legend=False)
        + geom_hline(yintercept=60, linetype="dashed", color="#C0392B", size=0.7)
        + facet_wrap("~Skill", nrow=1)
        + scale_fill_manual(values=["#4E79A7", "#F28E2B"])
        + scale_color_manual(values=["#4E79A7", "#F28E2B"])
        + labs(
            title="Pre–post skill distributions (ggplot2 / RStudio style)",
            subtitle="Institutional IELTS-aligned scores · dashed line = B1 threshold (60) · SYNTHETIC N = 120",
            x="",
            y="Score (0–100)",
        )
        + theme_rstudio()
        + theme(figure_size=(11.5, 4.8), axis_text_x=element_text(rotation=20, ha="right", size=8))
    )
    return save_ggplot(p, RST / "rstudio_skill_violins.png")


def _skill_prepost_summary(s: pd.DataFrame) -> pd.DataFrame:
    """Mean Pre/Post with 95% CI of the mean and paired p for each skill."""
    rows = []
    for skill in ["Listening", "Reading", "Writing", "Speaking", "Overall"]:
        pre = s[f"Pre_{skill}"]
        post = s[f"Post_{skill}"]
        d = s[f"Decline_{skill}"]
        t = stats.ttest_rel(pre, post)
        se_pre = pre.std(ddof=1) / np.sqrt(len(pre))
        se_post = post.std(ddof=1) / np.sqrt(len(post))
        ci_pre = stats.t.interval(0.95, len(pre) - 1, loc=pre.mean(), scale=se_pre)
        ci_post = stats.t.interval(0.95, len(post) - 1, loc=post.mean(), scale=se_post)
        if skill in {"Listening", "Speaking"}:
            family = "Oral–aural"
        elif skill in {"Reading", "Writing"}:
            family = "Written"
        else:
            family = "Overall"
        direction = "decline" if d.mean() > 0 else "gain"
        rows.append(
            {
                "Skill": skill,
                "Family": family,
                "Pre_Mean": float(pre.mean()),
                "Pre_lo": float(ci_pre[0]),
                "Pre_hi": float(ci_pre[1]),
                "Post_Mean": float(post.mean()),
                "Post_lo": float(ci_post[0]),
                "Post_hi": float(ci_post[1]),
                "Mean_decline": float(d.mean()),
                "Direction": direction,
                "p": float(t.pvalue),
                "Sig": "p < .001" if t.pvalue < 0.001 else f"p = {t.pvalue:.2f}",
            }
        )
    df = pd.DataFrame(rows)
    df["Skill"] = pd.Categorical(
        df["Skill"],
        categories=["Listening", "Reading", "Writing", "Speaking", "Overall"],
        ordered=True,
    )
    return df


def export_fig1_tableau_csv(s: pd.DataFrame, outdir: Path) -> Path:
    """Long-format CSV ready to open in Tableau (or Tableau Public)."""
    summary = _skill_prepost_summary(s)
    long_rows = []
    for _, row in summary.iterrows():
        for time_label, mean_key, lo_key, hi_key in [
            ("Pre (PYP exit)", "Pre_Mean", "Pre_lo", "Pre_hi"),
            ("Post (graduation)", "Post_Mean", "Post_lo", "Post_hi"),
        ]:
            long_rows.append(
                {
                    "Skill": row["Skill"],
                    "Skill_family": row["Family"],
                    "Time": time_label,
                    "Mean_score": row[mean_key],
                    "CI95_lo": row[lo_key],
                    "CI95_hi": row[hi_key],
                    "Mean_decline_pre_minus_post": row["Mean_decline"],
                    "Direction": row["Direction"],
                    "Paired_p_label": row["Sig"],
                    "Scale": "0–100 institutional",
                    "PYP_pass_threshold": 60,
                    "N": len(s),
                }
            )
    long = pd.DataFrame(long_rows)
    outdir.mkdir(parents=True, exist_ok=True)
    path = outdir / "fig1_skill_prepost_tableau.csv"
    long.to_csv(path, index=False)
    wide_path = outdir / "fig1_skill_prepost_wide_tableau.csv"
    summary.to_csv(wide_path, index=False)
    return path


def export_fig2_tableau_csv(s: pd.DataFrame, outdir: Path) -> Path:
    """Point-level CSV for Tableau scatter of Speaking decline paths."""
    outdir.mkdir(parents=True, exist_ok=True)
    long = pd.DataFrame(
        {
            "Student_ID": list(s["Student_ID"]) * 2,
            "Panel": (["A. Underrating gap"] * len(s)) + (["B. Translanguaging %"] * len(s)),
            "Predictor": np.concatenate([s["Underrating_Gap"], s["TL_percent"]]),
            "Speaking_decline": np.concatenate([s["Decline_Speaking"], s["Decline_Speaking"]]),
            "N": len(s),
            "Scale_note": "Speaking decline = Pre − Post on 0–100 scale",
        }
    )
    path = outdir / "fig2_golem_paths_tableau.csv"
    long.to_csv(path, index=False)
    return path


def _style_pub_axes(ax, *, grid_y: bool = True, grid_x: bool = False) -> None:
    ax.set_facecolor("#FFFFFF")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#C5CDD6")
    ax.spines["bottom"].set_color("#C5CDD6")
    ax.tick_params(colors="#4A5560", labelsize=9, length=3.5, width=0.8)
    if grid_y:
        ax.grid(True, axis="y", color="#EEF1F4", linewidth=0.9, zorder=0)
    if grid_x:
        ax.grid(True, axis="x", color="#EEF1F4", linewidth=0.9, zorder=0)
    ax.set_axisbelow(True)


def make_fig1_skill_decline(s: pd.DataFrame, outdir: Path) -> Path:
    """Publication Figure 1: polished grouped Pre vs Post means."""
    df = _skill_prepost_summary(s)
    outdir.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(9.6, 6.0), facecolor="#F7F9FB")
    _style_pub_axes(ax)
    x = np.arange(len(df))
    width = 0.34
    pre_color, post_color = "#3D6F9C", "#E08A2E"

    ax.bar(
        x - width / 2,
        df["Pre_Mean"],
        width,
        color=pre_color,
        edgecolor="white",
        linewidth=1.0,
        label="Pre (PYP exit)",
        zorder=3,
        alpha=0.95,
    )
    ax.bar(
        x + width / 2,
        df["Post_Mean"],
        width,
        color=post_color,
        edgecolor="white",
        linewidth=1.0,
        label="Post (graduation)",
        zorder=3,
        alpha=0.95,
    )
    ax.errorbar(
        x - width / 2,
        df["Pre_Mean"],
        yerr=[df["Pre_Mean"] - df["Pre_lo"], df["Pre_hi"] - df["Pre_Mean"]],
        fmt="none",
        ecolor="#2C3640",
        elinewidth=1.0,
        capsize=3.5,
        zorder=4,
    )
    ax.errorbar(
        x + width / 2,
        df["Post_Mean"],
        yerr=[df["Post_Mean"] - df["Post_lo"], df["Post_hi"] - df["Post_Mean"]],
        fmt="none",
        ecolor="#2C3640",
        elinewidth=1.0,
        capsize=3.5,
        zorder=4,
    )

    # Soft family underlays (oral–aural vs written)
    for i, (_, row) in enumerate(df.iterrows()):
        if row["Family"] == "Oral–aural":
            ax.axvspan(i - 0.48, i + 0.48, color="#F8E8E8", alpha=0.55, zorder=0)
        elif row["Family"] == "Written":
            ax.axvspan(i - 0.48, i + 0.48, color="#E8F3F1", alpha=0.55, zorder=0)

    for i, (_, row) in enumerate(df.iterrows()):
        delta = row["Mean_decline"]
        if delta > 0.05:
            label = f"↓ {delta:.1f}   {row['Sig']}"
            color = "#C0392B"
            face = "#FDEDEC"
        elif delta < -0.05:
            label = f"↑ {abs(delta):.1f}   {row['Sig']}"
            color = "#1E8449"
            face = "#E8F8F0"
        else:
            label = f"≈ 0   {row['Sig']}"
            color = "#555555"
            face = "#F2F3F4"
        y = max(row["Pre_hi"], row["Post_hi"]) + 0.85
        ax.text(
            i,
            y,
            label,
            ha="center",
            va="bottom",
            fontsize=8,
            color=color,
            fontweight="bold",
            bbox={
                "boxstyle": "round,pad=0.28",
                "facecolor": face,
                "edgecolor": "none",
                "alpha": 0.95,
            },
            zorder=5,
        )

    ax.axhline(60, color="#8A949E", ls=(0, (4, 3)), lw=1.15, zorder=2)
    ax.text(
        len(df) - 0.55,
        60.35,
        "threshold 60",
        ha="right",
        va="bottom",
        fontsize=7.5,
        color="#6A737C",
        style="italic",
    )
    ax.set_xticks(x)
    ax.set_xticklabels(list(df["Skill"]), fontsize=10, color="#1B1F24")
    ax.set_ylabel("Mean score (0–100 institutional scale)", fontsize=10, color="#4A5560")
    ax.set_ylim(55, max(df["Pre_hi"].max(), df["Post_hi"].max()) + 5.2)
    ax.set_xlim(-0.6, len(df) - 0.4)
    fig.suptitle(
        "Figure 1. Mean Pre and Post scores by skill (N = 120)",
        x=0.02,
        ha="left",
        fontsize=13,
        fontweight="bold",
        color="#1B1F24",
        y=0.98,
    )
    ax.set_title(
        "Oral–aural skills decline; written skills do not  ·  error bars = 95% CI of the mean",
        loc="left",
        fontsize=9,
        color="#5C6670",
        pad=10,
    )
    leg = ax.legend(
        frameon=True,
        fancybox=False,
        edgecolor="#D5DBE1",
        fontsize=8.5,
        loc="lower right",
        framealpha=0.96,
    )
    leg.get_frame().set_linewidth(0.8)
    # Small family key
    ax.text(
        0.01,
        0.02,
        "Shaded panels:  rose = oral–aural   ·   teal = written",
        transform=ax.transAxes,
        fontsize=7.5,
        color="#7A848E",
        va="bottom",
    )

    path = outdir / "fig1_skill_mean_decline.png"
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig(path, dpi=180, facecolor=fig.get_facecolor())
    plt.close(fig)

    tab_dir = outdir.parent / "tableau"
    tab_dir.mkdir(parents=True, exist_ok=True)
    export_fig1_tableau_csv(s, tab_dir)
    make_fig1_tableau_style(s, tab_dir)
    return path


def make_fig1_tableau_style(s: pd.DataFrame, outdir: Path) -> Path:
    """Tableau Public–inspired companion for Figure 1 (same design, dashboard card look)."""
    df = _skill_prepost_summary(s)
    outdir.mkdir(parents=True, exist_ok=True)
    fig = plt.figure(figsize=(11.2, 6.4), facecolor=T["bg"])
    gs = GridSpec(1, 1, figure=fig, left=0.08, right=0.97, top=0.82, bottom=0.12)
    ax = fig.add_subplot(gs[0, 0])
    card(ax, "")
    x = np.arange(len(df))
    w = 0.36
    ax.bar(x - w / 2, df["Pre_Mean"], w, color=T["blue"], edgecolor="white", label="Pre (PYP exit)", zorder=3)
    ax.bar(x + w / 2, df["Post_Mean"], w, color=T["orange"], edgecolor="white", label="Post (graduation)", zorder=3)
    ax.errorbar(
        x - w / 2,
        df["Pre_Mean"],
        yerr=[df["Pre_Mean"] - df["Pre_lo"], df["Pre_hi"] - df["Pre_Mean"]],
        fmt="none",
        ecolor=T["ink"],
        elinewidth=1.0,
        capsize=3,
        zorder=4,
    )
    ax.errorbar(
        x + w / 2,
        df["Post_Mean"],
        yerr=[df["Post_Mean"] - df["Post_lo"], df["Post_hi"] - df["Post_Mean"]],
        fmt="none",
        ecolor=T["ink"],
        elinewidth=1.0,
        capsize=3,
        zorder=4,
    )
    for i, (_, row) in enumerate(df.iterrows()):
        delta = row["Mean_decline"]
        col = T["red"] if delta > 0.05 else T["green"]
        arrow = "▼" if delta > 0.05 else "▲"
        ax.text(
            i,
            max(row["Pre_hi"], row["Post_hi"]) + 0.7,
            f"{arrow} {abs(delta):.1f}  {row['Sig']}",
            ha="center",
            fontsize=8.5,
            color=col,
            fontweight="bold",
        )
    ax.axhline(60, color=T["red"], ls="--", lw=1.2, alpha=0.7)
    ax.set_xticks(x, list(df["Skill"]))
    ax.set_ylabel("Mean score (0–100)")
    ax.set_ylim(55, max(df["Pre_hi"].max(), df["Post_hi"].max()) + 4.8)
    ax.legend(frameon=False, fontsize=9, loc="lower right")
    fig.suptitle(
        "Figure 1  ·  Tableau-style  ·  Pre vs Post skill means",
        x=0.02,
        ha="left",
        fontsize=15,
        fontweight="bold",
        color=T["header"],
        y=0.96,
    )
    fig.text(
        0.02,
        0.905,
        "Dashboard card view of the publication chart  ·  SYNTHETIC N = 120  ·  threshold = 60",
        fontsize=9.5,
        color=T["muted"],
    )
    path = outdir / "fig1_skill_prepost_tableau_style.png"
    fig.savefig(path, dpi=170)
    plt.close(fig)
    return path


def make_fig2_golem_paths(s: pd.DataFrame, outdir: Path) -> Path:
    """Publication Figure 2: polished two-panel scatter (Speaking decline paths)."""
    outdir.mkdir(parents=True, exist_ok=True)
    panels = [
        (
            "A. Underrating gap",
            "Actual PYP overall − lecturer estimate",
            s["Underrating_Gap"],
            "Underrating gap (points)",
        ),
        (
            "B. Translanguaging exposure",
            "% of content-course time in Turkish",
            s["TL_percent"],
            "Translanguaging (% Turkish)",
        ),
    ]
    fig, axes = plt.subplots(1, 2, figsize=(11.0, 5.4), facecolor="#F7F9FB", sharey=True)
    y = s["Decline_Speaking"].to_numpy()
    for ax, (title, subtitle, xser, xlabel) in zip(axes, panels):
        _style_pub_axes(ax, grid_y=True, grid_x=True)
        x = xser.to_numpy()
        ax.scatter(
            x,
            y,
            s=36,
            c="#3D6F9C",
            alpha=0.55,
            edgecolors="white",
            linewidths=0.55,
            zorder=3,
        )
        slope, intercept, r, p, _se = stats.linregress(x, y)
        xs = np.linspace(x.min(), x.max(), 120)
        ys = intercept + slope * xs
        # simple analytic CI band for mean line
        yhat = intercept + slope * x
        resid = y - yhat
        dof = max(len(x) - 2, 1)
        s_err = np.sqrt(np.sum(resid**2) / dof)
        x_mean = x.mean()
        ssx = np.sum((x - x_mean) ** 2)
        se_fit = s_err * np.sqrt(1 / len(x) + (xs - x_mean) ** 2 / ssx)
        tcrit = stats.t.ppf(0.975, dof)
        ax.fill_between(xs, ys - tcrit * se_fit, ys + tcrit * se_fit, color="#E8B4B0", alpha=0.45, zorder=1)
        ax.plot(xs, ys, color="#C0392B", lw=2.0, zorder=4)
        ax.axhline(0, color="#8A949E", ls=(0, (2, 2)), lw=1.0, zorder=2)
        plabel = "p < .001" if p < 0.001 else f"p = {p:.3f}"
        ax.text(
            0.04,
            0.96,
            f"r = {r:.2f},  {plabel}",
            transform=ax.transAxes,
            va="top",
            fontsize=9,
            color="#1B1F24",
            fontweight="bold",
            bbox={"boxstyle": "round,pad=0.3", "facecolor": "white", "edgecolor": "#D5DBE1", "alpha": 0.95},
        )
        ax.set_title(title, loc="left", fontsize=11, fontweight="bold", color="#1B1F24", pad=8)
        ax.text(0.0, 1.01, subtitle, transform=ax.transAxes, fontsize=8.5, color="#5C6670", va="bottom")
        ax.set_xlabel(xlabel, fontsize=9.5, color="#4A5560")
    axes[0].set_ylabel("Speaking decline (pre − post; points on 0–100)", fontsize=9.5, color="#4A5560")
    fig.suptitle(
        "Figure 2. Speaking decline associated with underrating and translanguaging",
        x=0.02,
        ha="left",
        fontsize=13,
        fontweight="bold",
        color="#1B1F24",
        y=0.99,
    )
    fig.text(
        0.02,
        0.935,
        "Positive values = attrition  ·  bands = 95% CI of the fitted line  ·  SYNTHETIC N = 120",
        fontsize=9,
        color="#5C6670",
    )
    path = outdir / "fig2_golem_speaking_paths.png"
    fig.tight_layout(rect=(0, 0, 1, 0.91))
    fig.savefig(path, dpi=180, facecolor=fig.get_facecolor())
    plt.close(fig)

    tab_dir = outdir.parent / "tableau"
    export_fig2_tableau_csv(s, tab_dir)
    make_fig2_tableau_style(s, tab_dir)
    return path


def make_fig2_tableau_style(s: pd.DataFrame, outdir: Path) -> Path:
    """Tableau-inspired companion scatter for Figure 2."""
    outdir.mkdir(parents=True, exist_ok=True)
    fig = plt.figure(figsize=(12.0, 5.8), facecolor=T["bg"])
    fig.suptitle(
        "Figure 2  ·  Tableau-style  ·  Speaking attrition paths",
        x=0.02,
        ha="left",
        fontsize=15,
        fontweight="bold",
        color=T["header"],
        y=0.97,
    )
    fig.text(0.02, 0.915, "Point + trend view of the Golem mechanism predictors  ·  SYNTHETIC N = 120", fontsize=9.5, color=T["muted"])
    gs = GridSpec(1, 2, figure=fig, wspace=0.22, left=0.07, right=0.98, top=0.86, bottom=0.12)
    specs = [
        (s["Underrating_Gap"], "Underrating gap", T["blue"]),
        (s["TL_percent"], "% class time in Turkish", T["orange"]),
    ]
    y = s["Decline_Speaking"]
    for i, (x, xlab, col) in enumerate(specs):
        ax = fig.add_subplot(gs[0, i])
        card(ax, ["A. Underrating → Speaking decline", "B. Translanguaging → Speaking decline"][i])
        ax.scatter(x, y, s=32, c=col, alpha=0.7, edgecolors="white", linewidths=0.4, zorder=3)
        slope, intercept, r, p, _ = stats.linregress(x, y)
        xs = np.linspace(x.min(), x.max(), 80)
        ax.plot(xs, intercept + slope * xs, color=T["red"], lw=2.2, zorder=4)
        ax.axhline(0, color=T["ink"], lw=0.7, alpha=0.5)
        plabel = "p < .001" if p < 0.001 else f"p = {p:.3f}"
        ax.text(0.04, 0.95, f"r = {r:.2f}, {plabel}", transform=ax.transAxes, va="top", fontsize=9, fontweight="bold", color=T["header"])
        ax.set_xlabel(xlab)
        if i == 0:
            ax.set_ylabel("Speaking decline (pre − post)")
    path = outdir / "fig2_golem_paths_tableau_style.png"
    fig.savefig(path, dpi=170)
    plt.close(fig)
    return path

def make_rstudio_decline_bars(s: pd.DataFrame) -> Path:
    """Archive alias — kept for optional --archive builds."""
    return make_fig1_skill_decline(s, RST)


def make_rstudio_mechanism(s: pd.DataFrame) -> Path:
    """Archive alias — kept for optional --archive builds."""
    return make_fig2_golem_paths(s, RST)


def make_rstudio_paired_slope(s: pd.DataFrame) -> Path:
    sample = s.sample(n=40, random_state=12)
    fig, ax = plt.subplots(figsize=(7.2, 5.6), facecolor="white")
    for _, row in sample.iterrows():
        color = "#E15759" if row["Decline_Overall"] > 0 else "#59A14F"
        ax.plot([0, 1], [row["Pre_Overall"], row["Post_Overall"]], color=color, alpha=0.35, lw=1.0)
        ax.scatter([0, 1], [row["Pre_Overall"], row["Post_Overall"]], color=color, s=14, alpha=0.55, zorder=3)
    ax.plot([0, 1], [s["Pre_Overall"].mean(), s["Post_Overall"].mean()], color="#1A1A1A", lw=2.6, zorder=4)
    ax.scatter([0, 1], [s["Pre_Overall"].mean(), s["Post_Overall"].mean()], color="#1A1A1A", s=55, zorder=5)
    ax.axhline(60, color="#888888", ls="--", lw=1)
    ax.set_xticks([0, 1], ["Pre\n(PYP exit)", "Post\n(graduation)"])
    ax.set_ylabel("Overall score (0–100)")
    ax.set_title(
        "Paired slopegraph (40 students + group means)\nggplot2 / RStudio style  ·  SYNTHETIC",
        loc="left",
        fontsize=12,
        fontweight="bold",
    )
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(True, axis="y", color="#D9D9D9")
    ax.legend(
        handles=[
            mpatches.Patch(color="#E15759", label="Declined"),
            mpatches.Patch(color="#59A14F", label="Improved / flat"),
            mpatches.Patch(color="#1A1A1A", label="Group mean"),
        ],
        frameon=True,
        fancybox=False,
        edgecolor="#222222",
        fontsize=8,
        loc="lower left",
    )
    RST.mkdir(parents=True, exist_ok=True)
    path = RST / "rstudio_paired_slopegraph.png"
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def make_rstudio_corr_heatmap(s: pd.DataFrame) -> Path:
    cols = [
        "Decline_Speaking",
        "Decline_Listening",
        "Underrating_Gap",
        "TL_percent",
        "PU_mean",
        "EAP_mean",
        "WTC_mean",
        "SE_mean",
    ]
    labels = [
        "Speaking\ndecline",
        "Listening\ndecline",
        "Underrating",
        "TL %",
        "Perceived\nunderrating",
        "Lecturer\nEAP gap",
        "WTC",
        "Self-\nefficacy",
    ]
    corr = s[cols].corr()
    fig, ax = plt.subplots(figsize=(7.8, 6.6), facecolor="white")
    mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
    sns.heatmap(
        corr,
        mask=mask,
        annot=True,
        fmt=".2f",
        cmap="RdBu_r",
        vmin=-1,
        vmax=1,
        square=True,
        linewidths=0.6,
        linecolor="white",
        cbar_kws={"shrink": 0.8, "label": "Pearson r"},
        xticklabels=labels,
        yticklabels=labels,
        ax=ax,
    )
    ax.set_title("Mechanism correlation matrix\nggplot2 / RStudio style  ·  SYNTHETIC", loc="left", fontsize=12, fontweight="bold")
    path = RST / "rstudio_mechanism_heatmap.png"
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def make_rstudio_ielts(s: pd.DataFrame, ielts: pd.DataFrame) -> Path:
    m = ielts.merge(s[["Student_ID", "Pre_Overall"]], on="Student_ID")
    r = stats.pearsonr(m["Pre_Overall"], m["IELTS_Overall"])
    p = (
        ggplot(m, aes("Pre_Overall", "IELTS_Overall"))
        + geom_point(size=2.4, alpha=0.8, color="#4E79A7")
        + geom_smooth(method="lm", color="#C0392B", fill="#F5B7B1", alpha=0.3, size=1.0)
        + labs(
            title="Concurrent validity: institutional overall vs IELTS Academic",
            subtitle=f"Official ielts.org practice materials under exam conditions  ·  n = {len(m)}  ·  r = {r.statistic:.2f}, p < .001  ·  SYNTHETIC",
            x="Institutional overall (PYP exit)",
            y="IELTS Academic overall band",
        )
        + theme_rstudio()
        + theme(figure_size=(7.8, 5.4))
    )
    return save_ggplot(p, RST / "rstudio_ielts_concurrent.png")


def make_rstudio_hist_diff(s: pd.DataFrame) -> Path:
    df = s[["Decline_Speaking"]].copy()
    sw = stats.shapiro(df["Decline_Speaking"])
    fig, ax = plt.subplots(figsize=(7.8, 5.0), facecolor="white")
    sns.histplot(df["Decline_Speaking"], bins=16, kde=True, color="#E15759", edgecolor="white", ax=ax)
    ax.axvline(df["Decline_Speaking"].mean(), color="#C0392B", ls="--", lw=1.6, label=f"Mean = {df['Decline_Speaking'].mean():.2f}")
    ax.axvline(0, color="#222222", lw=0.9)
    ax.set_xlabel("Speaking difference score (pre − post)")
    ax.set_ylabel("Count")
    ax.set_title(
        f"Speaking attrition distribution\nShapiro–Wilk W = {sw.statistic:.3f}, p = {sw.pvalue:.3f}  ·  ggplot2 / RStudio style  ·  SYNTHETIC",
        loc="left",
        fontsize=12,
        fontweight="bold",
    )
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(frameon=True, fancybox=False, edgecolor="#222222", fontsize=8)
    ax.grid(True, axis="y", color="#D9D9D9")
    path = RST / "rstudio_difference_hist.png"
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def copy_artifacts(paths: list[Path]) -> None:
    ART.mkdir(parents=True, exist_ok=True)
    for p in paths:
        dest = ART / p.name
        dest.write_bytes(p.read_bytes())


def main() -> None:
    import sys

    archive = "--archive" in sys.argv
    s, lect, ielts = load()
    FIG = OUT / "figures"
    FIG.mkdir(parents=True, exist_ok=True)

    # Only two figures are statistically central for the manuscript:
    # (1) paired skill change with CIs; (2) Speaking decline × mechanism predictors.
    # Everything else stays in tables (descriptives, paired tests, correlations, OLS, psychometrics).
    paths = [
        make_fig1_skill_decline(s, FIG),
        make_fig2_golem_paths(s, FIG),
    ]

    if archive:
        ARCH = OUT / "archive"
        TAB.mkdir(parents=True, exist_ok=True)
        RST.mkdir(parents=True, exist_ok=True)
        ARCH.mkdir(parents=True, exist_ok=True)
        extras = [
            make_tableau_dashboard(s, lect),
            make_tableau_lecturer_dashboard(s, lect),
            make_tableau_demographics(s),
            make_rstudio_prepost(s),
            make_rstudio_paired_slope(s),
            make_rstudio_corr_heatmap(s),
            make_rstudio_ielts(s, ielts),
            make_rstudio_hist_diff(s),
        ]
        for p in extras:
            dest = ARCH / p.name
            dest.write_bytes(p.read_bytes())
            paths.append(dest)

    copy_artifacts(paths[:2])
    index = ROOT / "FIGURES.md"
    lines = [
        "# Figures (publication set)",
        "",
        "Only figures that carry a primary inferential claim are retained for the manuscript.",
        "All other results are reported in tables.",
        "",
        "## Scale",
        "",
        "Institutional skill and overall scores are on a **0–100** scale. "
        "The Preparatory Year Programme pass threshold is **60/100** (interpreted as CEFR B1).",
        "",
        "## Publication figures (`outputs/figures/`)",
        "",
        "1. `fig1_skill_mean_decline.png` — **grouped Pre vs Post mean scores** by skill "
        "(with 95% CI). Listening/Speaking post bars are lower; Reading/Writing are not. "
        "Signed-difference bars were retired because readers misread + as gain.",
        "2. `fig2_golem_speaking_paths.png` — Speaking decline associated with underrating gap "
        "and translanguaging exposure.",
        "",
        "## Styled companions (Tableau + RStudio)",
        "",
        "### Tableau-style PNGs + CSVs (`outputs/tableau/`)",
        "",
        "- `fig1_skill_prepost_tableau_style.png`",
        "- `fig2_golem_paths_tableau_style.png`",
        "- `fig1_skill_prepost_tableau.csv` / `fig1_skill_prepost_wide_tableau.csv`",
        "- `fig2_golem_paths_tableau.csv`",
        "",
        "### RStudio / ggplot2 (`rstudio/fig1_and_fig2_styled.R`)",
        "",
        "- `outputs/rstudio/fig1_skill_prepost_ggplot.png`",
        "- `outputs/rstudio/fig2_golem_paths_ggplot.png`",
        "",
        "Publication Figure 2 remains the two-panel **scatter**.",
        "",
        "## Tables (not figured)",
        "",
        "- Descriptives, paired *t*/Wilcoxon by skill, reliability/ICC/IELTS validity",
        "- Correlations with Speaking decline, OLS coefficients, mediation quantities",
        "- Sample composition and lecturer-level exploratory summaries",
        "",
        "Optional exploratory dashboards (not for the paper):",
        "",
        "```bash",
        "python make_styled_figures.py --archive",
        "```",
        "",
        "Rebuild publication + styled companions:",
        "",
        "```bash",
        "python make_styled_figures.py",
        "Rscript rstudio/fig1_and_fig2_styled.R",
        "```",
        "",
    ]
    index.write_text("\n".join(lines), encoding="utf-8")
    print("wrote", len(paths), "figure(s)" + (" including archive" if archive else " (publication set)"))
    for p in paths:
        print(" ", p)


if __name__ == "__main__":
    main()
