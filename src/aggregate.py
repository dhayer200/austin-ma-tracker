from __future__ import annotations

import json
import sqlite3
from pathlib import Path

import pandas as pd

CACHE = Path(__file__).resolve().parent.parent / "data" / "cache"
DB = CACHE / "deals.db"


def load_deals() -> pd.DataFrame:
    conn = sqlite3.connect(DB)
    df = pd.read_sql("SELECT * FROM deals", conn)
    conn.close()
    df["announced_date"] = pd.to_datetime(df["announced_date"], errors="coerce")
    df = df.dropna(subset=["announced_date"]).copy()
    df["year_month"] = df["announced_date"].dt.to_period("M").astype(str)
    df["year"] = df["announced_date"].dt.year
    return df


def main() -> None:
    df = load_deals()
    summary = {
        "total_deals": int(len(df)),
        "date_range": [str(df["announced_date"].min().date()), str(df["announced_date"].max().date())],
        "disclosed_ev_total_usd": float(df["ev_usd"].dropna().sum()),
        "disclosed_ev_count": int(df["ev_usd"].notna().sum()),
        "by_sector": df["sector"].value_counts().to_dict(),
        "by_deal_type": df["deal_type"].value_counts().to_dict(),
        "by_month": df.groupby("year_month").size().to_dict(),
        "top_10_by_ev": df.dropna(subset=["ev_usd"]).nlargest(10, "ev_usd")[
            ["announced_date", "target", "acquirer", "sector", "ev_usd"]
        ].assign(announced_date=lambda d: d["announced_date"].dt.strftime("%Y-%m-%d")).to_dict(orient="records"),
    }
    out = CACHE / "aggregate_summary.json"
    out.write_text(json.dumps(summary, indent=2, default=str))
    print(f"wrote {out}")
    print(f"\n{summary['total_deals']} deals, {summary['disclosed_ev_count']} with disclosed EV totaling ${summary['disclosed_ev_total_usd']/1e9:.1f}B")
    print(f"\ntop sectors: {dict(list(summary['by_sector'].items())[:5])}")


if __name__ == "__main__":
    main()
