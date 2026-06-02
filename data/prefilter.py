from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

CACHE = Path(__file__).resolve().parent / "cache"

TRIGGERS = re.compile(
    r"\b("
    r"acquir(ed|es|ing|ition)|"
    r"merger|merges|merging|merged|"
    r"to acquire|"
    r"buyout|"
    r"sold to|sells .{0,30} to|"
    r"private equity|"
    r"completes acquisition|"
    r"closes acquisition|"
    r"signs (definitive )?agreement to acquire|"
    r"recapitalization|"
    r"strategic investment in"
    r")\b",
    re.IGNORECASE,
)

AUSTIN_LOC = re.compile(
    r"\b(Austin|Round Rock|Cedar Park|Pflugerville|Leander|Georgetown|Kyle|Buda|"
    r"Hutto|Lakeway|Bee Cave|Westlake|San Marcos|Manor|Travis County|Williamson County|"
    r"Hays County|Bastrop|Bastrop County|Caldwell County)\b",
    re.IGNORECASE,
)

AUSTIN_ONLY_SOURCES = {
    "Austin Business Journal",
    "Austin American-Statesman business",
}


def keep(row: pd.Series) -> bool:
    text = f"{row['title']} {row.get('summary', '') or ''}"
    if not TRIGGERS.search(text):
        return False
    if row["source"] in AUSTIN_ONLY_SOURCES:
        return True
    return bool(AUSTIN_LOC.search(text))


def main() -> None:
    df = pd.read_csv(CACHE / "raw_items.csv")
    df["summary"] = df["summary"].fillna("")
    mask = df.apply(keep, axis=1)
    out = df[mask].copy()
    print(f"prefilter: {len(df):,} raw items -> {len(out):,} candidate deals "
          f"({len(out)/max(len(df),1)*100:.1f}%)")
    out_path = CACHE / "candidates.csv"
    out.to_csv(out_path, index=False)
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
