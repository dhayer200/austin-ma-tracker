from __future__ import annotations

import json
import sqlite3
import subprocess
from pathlib import Path

CACHE = Path(__file__).resolve().parent / "cache"
DB = CACHE / "deals.db"
BATCH = 20

PROMPT = """You are an M&A analyst. For each numbered news item below, output a JSON object with these fields:

- id (int, same as input)
- target (str): the company being acquired. Use the company name, not a description.
- acquirer (str)
- sector (str): one of real_estate, tech, healthcare, financial_services, consumer, industrial, energy, education, services, other
- deal_type (str): one of acquisition, merger, recap, strategic_investment, asset_sale
- announced_date (str, ISO YYYY-MM-DD or null)
- ev_usd (number or null): enterprise value in USD. Null if not disclosed.
- status (str): one of announced, completed, terminated
- description (str): one short sentence.
- is_real_deal (bool): true ONLY if this is a genuine corporate M&A, private equity transaction, or commercial real estate sale involving an Austin-area company or property. False for sports player trades, government land acquisitions, military mergers, university restructurings, film rights, or speculative articles.

Output ONLY a JSON array of objects, no prose. If an item cannot be classified, still output an object with is_real_deal=false.

News items:
"""


def init_db() -> None:
    conn = sqlite3.connect(DB)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS deals (
            id INTEGER PRIMARY KEY,
            source_id INTEGER UNIQUE,
            target TEXT,
            acquirer TEXT,
            sector TEXT,
            deal_type TEXT,
            announced_date TEXT,
            ev_usd REAL,
            status TEXT,
            description TEXT,
            title TEXT,
            link TEXT,
            source TEXT,
            ingested_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def claude_extract(batch: list[dict]) -> list[dict]:
    items_text = "\n".join(f"{it['id']}: {it['title']} | {it['summary'][:200]}" for it in batch)
    full_prompt = PROMPT + items_text
    try:
        result = subprocess.run(
            ["claude", "-p", full_prompt],
            capture_output=True, text=True, timeout=180,
        )
        out = result.stdout.strip()
        if out.startswith("```"):
            out = out.split("```")[1]
            if out.startswith("json"):
                out = out[4:]
        return json.loads(out)
    except Exception as e:
        print(f"  extraction error: {e}")
        return []


def main() -> None:
    init_db()
    candidates = [json.loads(line) for line in open(CACHE / "candidates.jsonl")]
    print(f"extracting {len(candidates)} candidates in batches of {BATCH}")

    conn = sqlite3.connect(DB)
    for i in range(0, len(candidates), BATCH):
        batch = candidates[i:i + BATCH]
        records = claude_extract(batch)
        kept = 0
        for r in records:
            if not r.get("is_real_deal"):
                continue
            source_id = r.get("id")
            src = next((c for c in batch if c["id"] == source_id), None)
            if not src:
                continue
            conn.execute("""
                INSERT OR REPLACE INTO deals
                (source_id, target, acquirer, sector, deal_type, announced_date,
                 ev_usd, status, description, title, link, source)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (source_id, r.get("target"), r.get("acquirer"), r.get("sector"),
                  r.get("deal_type"), r.get("announced_date"), r.get("ev_usd"),
                  r.get("status"), r.get("description"),
                  src["title"], src["link"], src["source"]))
            kept += 1
        conn.commit()
        print(f"  batch {i//BATCH + 1}: {len(records)} extracted, {kept} kept")

    conn.close()
    print(f"done. db at {DB}")


if __name__ == "__main__":
    main()
