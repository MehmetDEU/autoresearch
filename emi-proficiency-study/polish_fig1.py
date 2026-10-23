#!/usr/bin/env python3
"""Regenerate publication Figure 1 in a calmer journal style.

Keeps the prior PNG under outputs/archive/*_before_polish.png when present.
"""

from __future__ import annotations

from pathlib import Path
import shutil

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parent
XLSX = ROOT / "EMI_PYP_pre_post_synthetic_N120.xlsx"
FIG = ROOT / "outputs" / "figures"
RST = ROOT / "outputs" / "rstudio"
ART = Path("/opt/cursor/artifacts")


def apa_stars(p: float) -> str:
    if p < 0.001:
        return "***"
    if p < 0.01:
        return "**"
    if p < 0.05:
        return "*"
    return "n.s."


def summary(s: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for skill in ["Listening", "Reading", "Writing", "Speaking", "Overall"]:
        pre = s[f"Pre_{skill}"]
        post = s[f"Post_{skill}"]
        t = stats.ttest_rel(pre, post)
        se_pre = pre.std(ddof=1) / np.sqrt(len(pre))
        se_post = post.std(ddof=1) / np.sqrt(len(post))
        ci_pre = stats.t.interval(0.95, len(pre) - 1, loc=pre.mean(), scale=se_pre)
        ci_post = stats.t.interval(0.95, len(post) - 1, loc=post.mean(), scale=se_post)
        mdiff = float((pre - post).mean())
        rows.append(
            {
                "Skill": skill,
                "Pre_Mean": float(pre.mean()),
                "Pre_lo": float(ci_pre[0]),
                "Pre_hi": float(ci_pre[1]),
                "Post_Mean": float(post.mean()),
                "Post_lo": float(ci_post[0]),
                "Post_hi": float(ci_post[1]),
                "Mdiff": mdiff,
                "p": float(t.pvalue),
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    s = pd.read_excel(XLSX, "Students")
    df = summary(s)

    pre_color, post_color = "#2F4A66", "#B5683C"
    ink, muted, grid = "#1C2430", "#6B7280", "#ECEFF2"

    fig, ax = plt.subplots(figsize=(9.0, 5.4), facecolor="white")
    ax.set_facecolor("white")
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color("#B8C0C8")
    ax.spines["bottom"].set_color("#B8C0C8")
    ax.tick_params(colors=muted, labelsize=9.5, length=3, width=0.7)
    ax.yaxis.grid(True, color=grid, linewidth=0.85, zorder=0)
    ax.set_axisbelow(True)

    x = np.arange(len(df))
    width = 0.36
    ax.bar(
        x - width / 2,
        df["Pre_Mean"],
        width,
        color=pre_color,
        edgecolor="none",
        label="Pre (PYP exit)",
        zorder=3,
    )
    ax.bar(
        x + width / 2,
        df["Post_Mean"],
        width,
        color=post_color,
        edgecolor="none",
        label="Post (graduation)",
        zorder=3,
    )
    ax.errorbar(
        x - width / 2,
        df["Pre_Mean"],
        yerr=[df["Pre_Mean"] - df["Pre_lo"], df["Pre_hi"] - df["Pre_Mean"]],
        fmt="none",
        ecolor=ink,
        elinewidth=0.9,
        capsize=2.8,
        zorder=4,
    )
    ax.errorbar(
        x + width / 2,
        df["Post_Mean"],
        yerr=[df["Post_Mean"] - df["Post_lo"], df["Post_hi"] - df["Post_Mean"]],
        fmt="none",
        ecolor=ink,
        elinewidth=0.9,
        capsize=2.8,
        zorder=4,
    )

    for i, row in df.iterrows():
        change = -row["Mdiff"]  # Post − Pre
        stars = apa_stars(row["p"])
        label = f"0  {stars}" if abs(change) < 0.05 else f"{change:+.1f}  {stars}"
        color = "#8B3A2F" if (change < -0.05 and stars != "n.s.") else muted
        y = max(row["Pre_hi"], row["Post_hi"]) + 0.55
        ax.text(
            i,
            y,
            label,
            ha="center",
            va="bottom",
            fontsize=8.2,
            color=color,
            fontweight="bold" if stars != "n.s." else "normal",
            zorder=5,
        )

    ax.axhline(60, color="#9AA3AD", ls=(0, (3, 2.5)), lw=1.0, zorder=2)
    ax.text(
        len(df) - 0.42,
        60.28,
        "threshold = 60",
        ha="right",
        va="bottom",
        fontsize=7.5,
        color=muted,
        style="italic",
    )
    ax.set_xticks(x)
    ax.set_xticklabels(list(df["Skill"]), fontsize=10.5, color=ink)
    ax.set_ylabel("Mean score (0–100)", fontsize=10, color=muted)
    ax.set_ylim(57, max(df["Pre_hi"].max(), df["Post_hi"].max()) + 3.2)
    ax.set_xlim(-0.55, len(df) - 0.45)

    fig.suptitle(
        "Mean Pre and Post scores by skill (N = 120)",
        x=0.02,
        ha="left",
        fontsize=12.5,
        fontweight="bold",
        color=ink,
        y=0.98,
    )
    ax.set_title(
        "Error bars = 95% CI of the mean. Labels = Post − Pre (negative = attrition).",
        loc="left",
        fontsize=8.2,
        color=muted,
        pad=8,
    )
    ax.legend(
        frameon=False,
        fontsize=9,
        loc="upper right",
        bbox_to_anchor=(1.0, 0.98),
        handlelength=1.1,
        borderaxespad=0.2,
    )

    FIG.mkdir(parents=True, exist_ok=True)
    RST.mkdir(parents=True, exist_ok=True)
    fig_path = FIG / "fig1_skill_mean_decline.png"
    rst_path = RST / "fig1_skill_prepost_ggplot.png"
    fig.tight_layout(rect=(0.02, 0.02, 0.99, 0.92))
    fig.savefig(fig_path, dpi=200, facecolor="white")
    fig.savefig(rst_path, dpi=200, facecolor="white")
    plt.close(fig)

    if ART.is_dir():
        shutil.copy2(rst_path, ART / "fig1_skill_prepost_ggplot.png")
        shutil.copy2(fig_path, ART / "fig1_skill_mean_decline.png")
        # side-by-side review copies
        before = ROOT / "outputs" / "archive" / "fig1_skill_prepost_ggplot_before_polish.png"
        if before.exists():
            shutil.copy2(before, ART / "fig1_before_polish.png")
        shutil.copy2(rst_path, ART / "fig1_after_polish.png")

    print("wrote", fig_path)
    print("wrote", rst_path)


if __name__ == "__main__":
    main()
