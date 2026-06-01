# Austin M&A Tracker

Austin MSA mid-market M&A pipeline. Ingests nine RSS feeds, regex-prefilters items, extracts structured deal records with the Claude CLI, stores to SQLite, and serves a Streamlit dashboard. Includes a real-estate sub-segment deep dive on the verified deal set.

**Paper:** https://deephayer.com/papers/austin-ma-tracker.pdf
**Deep dive paper:** https://deephayer.com/papers/austin-re-deepdive.pdf
**Essay:** https://deephayer.com/essays/2026-austin-ma-tracker

## Headline finding

43 hand-verified Austin MSA deals from August 2024 through May 2026. Only 4 of 43 had enterprise value disclosed; that 9 percent ceiling quantifies the structural limit of free-data M&A tracking. The RE sub-segment deep dive (17 deals) surfaces three institutional sponsors entering UT-adjacent student housing in three consecutive months and an EdgeConneX 180-acre Bastrop land buy that prices the ERCOT load-growth thesis into raw land.

## Stack

Python (feedparser, BeautifulSoup), SQLite, Claude CLI for structured extraction, Streamlit, Typst.

## Pipeline

```
RSS feeds  ->  raw_items.csv  ->  regex prefilter  ->  candidates.jsonl
                                                              |
                                                              v
                                                   Claude CLI extraction
                                                              |
                                                              v
                                                         deals.db
                                                         /        \
                                                   Streamlit    Typst paper
```

## Quick start

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e .
python -m data.ingest_rss
python -m data.prefilter
python -m data.extract
python -m src.aggregate
python -m src.plots
streamlit run app.py
cd paper && typst compile austin-ma-tracker.typ
```

## Layout

- `data/sources.py` — registry of RSS feeds covering Austin MSA
- `data/ingest_rss.py` — pull all feeds, dedupe to `raw_items.csv`
- `data/prefilter.py` — regex prefilter
- `data/extract.py` — `claude -p` per item, parse JSON, write to `deals.db`
- `src/aggregate.py` — sector and month rollups
- `src/plots.py` — paper figures
- `app.py` — Streamlit dashboard
- `paper/austin-ma-tracker.typ` — tracker paper source
- `analysis/` — RE sub-segment deep dive (segmenter, plots, Typst source)
