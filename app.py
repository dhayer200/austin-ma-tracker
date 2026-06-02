from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

DB = Path(__file__).resolve().parent / "data" / "cache" / "deals.db"

st.set_page_config(page_title="Austin M&A tracker", layout="wide")
st.title("Austin MSA M&A tracker")
st.caption("Announced mid-market transactions involving Austin-area targets or acquirers. Hourly RSS ingestion, LLM-extracted, hand-verified.")


@st.cache_data
def load() -> pd.DataFrame:
    conn = sqlite3.connect(DB)
    df = pd.read_sql("SELECT * FROM deals", conn)
    conn.close()
    df["announced_date"] = pd.to_datetime(df["announced_date"], errors="coerce")
    return df.sort_values("announced_date", ascending=False)


df = load()

with st.sidebar:
    st.header("Filters")
    sectors = sorted(df["sector"].dropna().unique())
    chosen_sectors = st.multiselect("Sectors", sectors, default=sectors)
    types = sorted(df["deal_type"].dropna().unique())
    chosen_types = st.multiselect("Deal types", types, default=types)
    only_disclosed = st.checkbox("Only disclosed EV", value=False)

filtered = df[df["sector"].isin(chosen_sectors) & df["deal_type"].isin(chosen_types)]
if only_disclosed:
    filtered = filtered.dropna(subset=["ev_usd"])

col1, col2, col3 = st.columns(3)
col1.metric("Total deals", f"{len(filtered):,}")
col2.metric("Disclosed EV", f"${filtered['ev_usd'].dropna().sum() / 1e9:.1f}B")
col3.metric("Sectors covered", f"{filtered['sector'].nunique()}")

st.subheader("Deal volume by month")
filtered = filtered.copy()
filtered["year_month"] = filtered["announced_date"].dt.to_period("M").astype(str)
monthly = filtered.groupby("year_month").size().reset_index(name="count").sort_values("year_month")
fig, ax = plt.subplots(figsize=(10, 3.5))
ax.bar(monthly["year_month"], monthly["count"], color="#2E5FA3")
plt.setp(ax.get_xticklabels(), rotation=45, ha="right", fontsize=8)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
st.pyplot(fig)

col_a, col_b = st.columns(2)
with col_a:
    st.subheader("By sector")
    sec = filtered["sector"].value_counts()
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.barh(sec.index[::-1], sec.values[::-1], color="#2E5FA3")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    st.pyplot(fig)

with col_b:
    st.subheader("By deal type")
    tp = filtered["deal_type"].value_counts()
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.barh(tp.index[::-1], tp.values[::-1], color="#cc6633")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    st.pyplot(fig)

st.subheader("Deal list")
display = filtered[["announced_date", "target", "acquirer", "sector", "deal_type", "ev_usd", "description", "source"]].copy()
display["announced_date"] = display["announced_date"].dt.strftime("%Y-%m-%d")
display["ev_usd"] = display["ev_usd"].apply(lambda v: f"${v/1e6:,.0f}M" if pd.notna(v) else "")
display.columns = ["Date", "Target", "Acquirer", "Sector", "Type", "EV", "Description", "Source"]
st.dataframe(display, use_container_width=True, height=600)

st.markdown("---")
st.markdown("Built by [D Hayer](https://deephayer.com). Source at [github.com/dhayer200/austin-ma-tracker](https://github.com/dhayer200/austin-ma-tracker).")
