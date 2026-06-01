"""Figures for the paper.

  fig1_volume.png   -- deal count by month
  fig2_sector.png   -- deal count by sector
  fig3_ev.png       -- disclosed EVs sorted, log scale
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

from src.aggregate import load_deals

FIGDIR = Path(__file__).resolve().parent.parent / "paper" / "figures"

plt.rcParams.update({
    "font.family": "serif",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.dpi": 120,
})

SECTOR_COLORS = {
    "real_estate": "#2E5FA3",
    "consumer": "#cc6633",
    "healthcare": "#3a8a3a",
    "tech": "#9070c8",
    "services": "#d4a000",
    "financial_services": "#888888",
    "energy": "#444444",
    "industrial": "#aa7733",
    "education": "#b06677",
    "other": "#999999",
}


def fig_volume() -> None:
    df = load_deals()
    monthly = df.groupby("year_month").size().reset_index(name="count")
    monthly = monthly.sort_values("year_month")
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.bar(monthly["year_month"], monthly["count"], color="#2E5FA3")
    ax.set_title("Austin MSA M&A announcements by month")
    ax.set_ylabel("Announced deals")
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", fontsize=8)
    fig.tight_layout()
    fig.savefig(FIGDIR / "fig1_volume.png")
    plt.close(fig)


def fig_sector() -> None:
    df = load_deals()
    counts = df["sector"].value_counts()
    fig, ax = plt.subplots(figsize=(8, 4.5))
    colors = [SECTOR_COLORS.get(s, "#999999") for s in counts.index]
    ax.barh(counts.index[::-1], counts.values[::-1], color=colors[::-1])
    ax.set_title("Austin MSA M&A deal count by sector")
    ax.set_xlabel("Deals")
    fig.tight_layout()
    fig.savefig(FIGDIR / "fig2_sector.png")
    plt.close(fig)


def fig_ev() -> None:
    df = load_deals().dropna(subset=["ev_usd"]).sort_values("ev_usd")
    if len(df) == 0:
        return
    fig, ax = plt.subplots(figsize=(8, 4.5))
    labels = [f"{r['target'][:40]} ({r['acquirer'][:25]})" for _, r in df.iterrows()]
    colors = [SECTOR_COLORS.get(s, "#999999") for s in df["sector"]]
    ax.barh(range(len(df)), df["ev_usd"].values / 1e6, color=colors)
    ax.set_yticks(range(len(df)))
    ax.set_yticklabels(labels, fontsize=7)
    ax.set_xscale("log")
    ax.set_xlabel("Enterprise value ($M, log scale)")
    ax.set_title("Disclosed Austin MSA M&A enterprise values")
    fig.tight_layout()
    fig.savefig(FIGDIR / "fig3_ev.png")
    plt.close(fig)


def main() -> None:
    FIGDIR.mkdir(parents=True, exist_ok=True)
    fig_volume()
    fig_sector()
    fig_ev()
    print(f"wrote figures to {FIGDIR}")


if __name__ == "__main__":
    main()
