"""Plots for the RE deep-dive paper."""
from __future__ import annotations
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from analysis.segment import load, classify

FIG = Path(__file__).resolve().parent / "figures"
FIG.mkdir(exist_ok=True)
ACCENT = "#2E5FA3"
ACCENT2 = "#C97B3A"

ASSET_LABELS = {
    "multifamily": "Multifamily",
    "office": "Office",
    "student_housing": "Student housing",
    "retail": "Retail",
    "retail_owner_op": "Retail (owner-op)",
    "medical_office": "Medical office",
    "data_center_land": "Data center land",
    "hotel": "Hotel",
    "hotel_mixed": "Hotel / mixed-use",
    "land_recreation": "Recreation land",
}

BUYER_LABELS = {
    "institutional": "Institutional sponsor",
    "sponsor_mid": "Mid-market sponsor",
    "private": "Private / undisclosed",
    "corporate": "Strategic corporate",
    "foreign": "Foreign capital",
}


def fig_asset_mix(df: pd.DataFrame) -> None:
    counts = df["asset_class"].value_counts()
    labels = [ASSET_LABELS.get(k, k) for k in counts.index]
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    ax.barh(labels[::-1], counts.values[::-1], color=ACCENT)
    ax.set_xlabel("Deal count")
    ax.set_title("Austin MSA real estate deal mix, Nov 2024 - Nov 2025")
    for i, v in enumerate(counts.values[::-1]):
        ax.text(v + 0.05, i, str(v), va="center", fontsize=9)
    fig.tight_layout()
    fig.savefig(FIG / "asset_mix.png", dpi=150)
    plt.close(fig)


def fig_buyer_type(df: pd.DataFrame) -> None:
    counts = df["buyer_type"].value_counts()
    labels = [BUYER_LABELS.get(k, k) for k in counts.index]
    fig, ax = plt.subplots(figsize=(7.5, 4.0))
    ax.barh(labels[::-1], counts.values[::-1], color=ACCENT)
    ax.set_xlabel("Deal count")
    ax.set_title("Who is buying Austin RE")
    for i, v in enumerate(counts.values[::-1]):
        ax.text(v + 0.05, i, str(v), va="center", fontsize=9)
    fig.tight_layout()
    fig.savefig(FIG / "buyer_type.png", dpi=150)
    plt.close(fig)


def fig_timeline(df: pd.DataFrame) -> None:
    d = df.copy()
    d["announced_date"] = pd.to_datetime(d["announced_date"])
    d["month"] = d["announced_date"].dt.to_period("M").dt.to_timestamp()
    cls_focus = ["student_housing", "multifamily", "office", "retail", "data_center_land"]
    d["bucket"] = d["asset_class"].where(d["asset_class"].isin(cls_focus), "other")
    pivot = d.pivot_table(index="month", columns="bucket", values="id", aggfunc="count", fill_value=0).sort_index()
    cols_ordered = [c for c in ["student_housing", "multifamily", "office", "retail", "data_center_land", "other"] if c in pivot.columns]
    pivot = pivot[cols_ordered]
    colors = ["#2E5FA3", "#C97B3A", "#5B8C5A", "#A04B5B", "#8B6FB3", "#8C8C8C"][:len(cols_ordered)]
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    pivot.plot(kind="bar", stacked=True, ax=ax, color=colors, width=0.8)
    ax.set_xticklabels([d.strftime("%b %Y") for d in pivot.index], rotation=45, ha="right")
    ax.set_ylabel("Deals")
    ax.set_title("Austin RE deal activity by month and asset class")
    ax.legend(title="", fontsize=8, loc="upper left")
    fig.tight_layout()
    fig.savefig(FIG / "timeline.png", dpi=150)
    plt.close(fig)


def fig_student_concentration(df: pd.DataFrame) -> None:
    """The standout finding: 3 student housing deals in 3 months from 3 different institutional sponsors."""
    sh = df[df["asset_class"] == "student_housing"].copy()
    sh["announced_date"] = pd.to_datetime(sh["announced_date"])
    sh = sh.sort_values("announced_date")
    fig, ax = plt.subplots(figsize=(7.5, 3.5))
    sponsors = sh["acquirer"].str.split("/").str[0].str.strip().str.split().str[0]
    labels = [f"{s}\n{d.strftime('%b %Y')}" for s, d in zip(sh["acquirer"], sh["announced_date"])]
    beds = [670, 243, "n/a"]
    ax.scatter(sh["announced_date"], range(len(sh)), s=200, color=ACCENT2)
    for i, (date, acq) in enumerate(zip(sh["announced_date"], sh["acquirer"])):
        ax.text(date, i + 0.15, acq, fontsize=9, ha="center")
    ax.set_yticks(range(len(sh)))
    ax.set_yticklabels(["Landmark (Pointe on Rio)", "Core Spaces (670-bed)", "Ascentris JV (243-bed)"])
    ax.set_xlabel("Announcement date")
    ax.set_title("Three institutional sponsors enter UT-adjacent student housing in 3 months")
    ax.grid(axis="x", linestyle=":", alpha=0.5)
    fig.tight_layout()
    fig.savefig(FIG / "student_concentration.png", dpi=150)
    plt.close(fig)


def main() -> None:
    df = classify(load())
    fig_asset_mix(df)
    fig_buyer_type(df)
    fig_timeline(df)
    fig_student_concentration(df)
    out = FIG.parent / "classified_deals.csv"
    df.to_csv(out, index=False)
    print(f"Wrote {out} and 4 figures.")


if __name__ == "__main__":
    main()
