"""Pull all configured RSS feeds, normalize, dedupe by URL, store to CSV.

Writes data/cache/raw_items.csv with columns [source, title, link, published, summary].
"""
from __future__ import annotations

import time
from pathlib import Path

import feedparser
import pandas as pd

from data.sources import SOURCES

CACHE = Path(__file__).resolve().parent / "cache"


def fetch(src: dict) -> list[dict]:
    feed = feedparser.parse(src["url"])
    rows = []
    for e in feed.entries:
        rows.append({
            "source": src["name"],
            "category": src["category"],
            "title": e.get("title", "").strip(),
            "link": e.get("link", "").strip(),
            "published": e.get("published", e.get("updated", "")),
            "summary": (e.get("summary", "") or "").strip()[:1000],
        })
    return rows


def main() -> None:
    CACHE.mkdir(parents=True, exist_ok=True)
    all_rows = []
    for src in SOURCES:
        try:
            rows = fetch(src)
            print(f"  {src['name']:42s} {len(rows):4d} items")
            all_rows.extend(rows)
            time.sleep(0.5)
        except Exception as e:
            print(f"  {src['name']:42s} ERROR: {e}")

    df = pd.DataFrame(all_rows)
    df = df.drop_duplicates(subset=["link"]).reset_index(drop=True)
    df["published"] = pd.to_datetime(df["published"], errors="coerce", utc=True)
    out = CACHE / "raw_items.csv"
    df.to_csv(out, index=False)
    print(f"wrote {out} ({len(df):,} unique items)")


if __name__ == "__main__":
    main()
