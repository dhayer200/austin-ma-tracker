"""Sub-segment the 18 real estate deals from dealIQ into asset classes and buyer types.

Hand-classification because n=17 unique. Source of truth is the seeded SQLite DB.
"""
from __future__ import annotations
import sqlite3
from pathlib import Path
import pandas as pd

DB = Path(__file__).resolve().parents[1] / "data" / "cache" / "deals.db"

# (target_substring, asset_class, buyer_type)
# buyer_type: institutional, sponsor_mid, private, foreign, corporate
CLASSIFICATION = [
    # target_match, asset_class, buyer_type, unit_count, sub_market
    ("Cousins Properties", "office", "institutional", None, "downtown"),
    ("Block 21", "hotel_mixed", "institutional", None, "downtown"),
    ("Ryman Hospitality", "hotel_mixed", "institutional", None, "downtown"),
    ("Hanlim", "land_recreation", "foreign", None, "metro"),
    ("Bell Partners", "multifamily", "institutional", None, "central"),
    ("Lenox Boardwalk", "multifamily", "institutional", None, "central"),
    ("Landmark Properties", "student_housing", "institutional", None, "ut_adjacent"),
    ("Pointe on Rio", "student_housing", "institutional", None, "ut_adjacent"),
    ("BGO", "medical_office", "institutional", None, "metro"),
    ("Austin investor", "hotel", "private", None, "old_town"),
    ("Continental Realty", "multifamily", "sponsor_mid", 232, "metro"),
    ("Core Spaces", "student_housing", "institutional", 670, "ut_adjacent"),
    ("EdgeConneX", "data_center_land", "corporate", None, "bastrop"),
    ("Asana Partners", "retail", "institutional", None, "arboretum"),
    ("Austin office property", "office", "private", None, "metro"),
    ("Black's Barbecue", "retail_owner_op", "private", None, "central"),
    ("Karlin Real Estate", "multifamily", "sponsor_mid", 274, "central"),
    ("Ascentris", "student_housing", "institutional", 243, "ut_adjacent"),
    ("Haven Housing", "multifamily", "sponsor_mid", None, "suburban"),
    ("Downtown Austin office building", "office", "private", None, "downtown"),
]


def load() -> pd.DataFrame:
    with sqlite3.connect(DB) as con:
        df = pd.read_sql("SELECT * FROM deals WHERE sector='real_estate'", con)
    # dedupe Cousins (same deal, two sources)
    # Two Cousins rows are the same deal from two sources; dedupe on acquirer+ev when ev disclosed
    disclosed = df[df["ev_usd"].notna()].drop_duplicates(subset=["acquirer", "ev_usd"])
    undisclosed = df[df["ev_usd"].isna()]
    df = pd.concat([disclosed, undisclosed], ignore_index=True).sort_values("announced_date", ascending=False).reset_index(drop=True)
    return df


def classify(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["asset_class"] = None
    out["buyer_type"] = None
    out["unit_count"] = None
    out["sub_market"] = None
    for match, ac, bt, units, sub in CLASSIFICATION:
        mask = out["target"].str.contains(match, case=False, na=False) | out["acquirer"].str.contains(match, case=False, na=False)
        for col, val in [("asset_class", ac), ("buyer_type", bt), ("unit_count", units), ("sub_market", sub)]:
            out.loc[mask & out[col].isna(), col] = val
    return out


if __name__ == "__main__":
    df = classify(load())
    print(df[["target", "acquirer", "asset_class", "buyer_type", "sub_market", "announced_date", "ev_usd"]].to_string(index=False))
    print()
    print("Asset class mix:")
    print(df["asset_class"].value_counts())
    print()
    print("Buyer type mix:")
    print(df["buyer_type"].value_counts())
    print()
    print("Sub-market mix:")
    print(df["sub_market"].value_counts())
