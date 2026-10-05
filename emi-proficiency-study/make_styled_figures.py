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


def make_rstudio_decline_bars(s: pd.DataFrame) -> Path:
    rows = []
    for skill in ["Listening", "Reading", "Writing", "Speaking", "Overall"]:
        d = s[f"Decline_{skill}"]
        t = stats.ttest_rel(s[f"Pre_{skill}"], s[f"Post_{skill}"])
        se = d.std(ddof=1) / np.sqrt(len(d))
        ci = stats.t.interval(0.95, len(d) - 1, loc=d.mean(), scale=se)
        rows.append(
            {
                "Skill": skill,
                "Mean_decline": float(d.mean()),
                "lo": float(ci[0]),
                "hi": float(ci[1]),
                "p": float(t.pvalue),
                "Family": "Productive" if skill in {"Writing", "Speaking"} else ("Overall" if skill == "Overall" else "Receptive"),
            }
        )
    df = pd.DataFrame(rows)
    df["Skill"] = pd.Categorical(df["Skill"], categories=["Listening", "Reading", "Writing", "Speaking", "Overall"], ordered=True)
    df["ymin"] = df["Mean_decline"] - (df["Mean_decline"] - df["lo"])
    df["ymax"] = df["hi"]

    # plotnine has no built-in geom_errorbar convenience here for all versions; use annotate segments via matplotlib hybrid
    fig, ax = plt.subplots(figsize=(8.2, 5.2), facecolor="white")
    ax.set_facecolor("white")
    colors = {"Receptive": "#76B7B2", "Productive": "#F28E2B", "Overall": "#4E79A7"}
    for i, row in df.iterrows():
        ax.bar(i, row["Mean_decline"], color=colors[row["Family"]], edgecolor="#222222", linewidth=0.7, width=0.7)
        ax.plot([i, i], [row["lo"], row["hi"]], color="#222222", lw=1.2)
        ax.plot([i - 0.12, i + 0.12], [row["lo"], row["lo"]], color="#222222", lw=1.2)
        ax.plot([i - 0.12, i + 0.12], [row["hi"], row["hi"]], color="#222222", lw=1.2)
        ax.text(i, row["hi"] + 0.06, f"p={row['p']:.3f}", ha="center", va="bottom", fontsize=8, color="#333333")
    ax.axhline(0, color="#222222", lw=0.8)
    ax.set_xticks(range(len(df)))
    ax.set_xticklabels(df["Skill"])
    ax.set_ylabel("Mean decline (pre − post)")
    ax.set_title("Mean skill decline with 95% CI\nggplot2 / RStudio style  ·  SYNTHETIC", loc="left", fontsize=12, fontweight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for spine in ("left", "bottom"):
        ax.spines[spine].set_color("#222222")
    ax.grid(True, axis="y", color="#D9D9D9", linewidth=0.7)
    ax.set_axisbelow(True)
    handles = [mpatches.Patch(color=c, label=k) for k, c in colors.items()]
    ax.legend(handles=handles, frameon=True, fancybox=False, edgecolor="#222222", fontsize=8, title="Skill family")
    RST.mkdir(parents=True, exist_ok=True)
    path = RST / "rstudio_skill_decline_ci.png"
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def make_rstudio_mechanism(s: pd.DataFrame) -> Path:
    path_u = "1. Underrating gap (actual − lecturer estimate)"
    path_t = "2. Translanguaging exposure (% class time in Turkish)"
    long = pd.DataFrame(
        {
            "x": np.concatenate([s["Underrating_Gap"], s["TL_percent"]]),
            "Decline": np.concatenate([s["Decline_Speaking"], s["Decline_Speaking"]]),
            "Path": ([path_u] * len(s)) + ([path_t] * len(s)),
        }
    )
    long["Path"] = pd.Categorical(long["Path"], categories=[path_u, path_t], ordered=True)
    p = (
        ggplot(long, aes("x", "Decline"))
        + geom_point(alpha=0.55, size=1.8, color="#4E79A7")
        + geom_smooth(method="lm", color="#C0392B", fill="#F5B7B1", alpha=0.35, size=1.0)
        + geom_hline(yintercept=0, linetype="dotted", color="#666666")
        + facet_wrap("~Path", scales="free_x", nrow=1)
        + labs(
            title="Speaking attrition tracks underrating and translanguaging",
            subtitle="Primary outcome = Speaking decline  ·  ggplot2 / RStudio style  ·  SYNTHETIC N = 120",
            x="Predictor",
            y="Speaking decline (pre − post)",
        )
        + theme_rstudio()
        + theme(figure_size=(10.5, 5.0))
    )
    return save_ggplot(p, RST / "rstudio_golem_paths.png")


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
    s, lect, ielts = load()
    TAB.mkdir(parents=True, exist_ok=True)
    RST.mkdir(parents=True, exist_ok=True)

    paths = [
        make_tableau_dashboard(s, lect),
        make_tableau_lecturer_dashboard(s, lect),
        make_tableau_demographics(s),
        make_rstudio_prepost(s),
        make_rstudio_decline_bars(s),
        make_rstudio_mechanism(s),
        make_rstudio_paired_slope(s),
        make_rstudio_corr_heatmap(s),
        make_rstudio_ielts(s, ielts),
        make_rstudio_hist_diff(s),
    ]
    copy_artifacts(paths)
    index = ROOT / "FIGURES.md"
    lines = [
        "# Styled figures",
        "",
        "Generated from the synthetic Excel panel. Two visual languages:",
        "",
        "## Tableau-style (`outputs/tableau/`)",
        "",
        "KPI cards, clean dashboard chrome, Tableau 10 colours, left-aligned titles.",
        "",
    ]
    for p in paths:
        if "tableau" in str(p):
            lines.append(f"- `{p.relative_to(ROOT)}`")
    lines += [
        "",
        "## ggplot2 / RStudio-style (`outputs/rstudio/`)",
        "",
        "White panels, light grey grids, black axes, facet strips — the look you get from `ggplot2` + `theme_bw()` / `theme_minimal()` in RStudio.",
        "",
    ]
    for p in paths:
        if "rstudio" in str(p):
            lines.append(f"- `{p.relative_to(ROOT)}`")
    lines += [
        "",
        "Rebuild:",
        "",
        "```bash",
        "python make_styled_figures.py",
        "```",
        "",
    ]
    index.write_text("\n".join(lines), encoding="utf-8")
    print("wrote", len(paths), "figures")
    for p in paths:
        print(" ", p)


if __name__ == "__main__":
    main()
