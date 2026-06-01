"""Seed the deals.db with deals hand-extracted from the first ingestion batch.

This exists so the dashboard and paper have real data immediately.
Production pipeline runs extract.py to grow the dataset automatically.
"""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path

CACHE = Path(__file__).resolve().parent / "cache"
DB = CACHE / "deals.db"


SEED_DEALS = [
    # source_id, target, acquirer, sector, deal_type, announced_date, ev_usd, description
    (0, "Austin multifamily property (Haven Housing target)", "Haven Housing", "real_estate", "acquisition", "2025-11-01", None, "Suburban Austin multifamily acquisition"),
    (1, "Downtown Austin office building", "Austin real estate firm (undisclosed)", "real_estate", "acquisition", "2025-10-01", None, "Large downtown office tower acquisition"),
    (2, "Austin office property", "Private investor (undisclosed)", "real_estate", "acquisition", "2025-09-01", None, "Austin office property sale to private investor"),
    (3, "Gitar", "Sonar", "tech", "acquisition", "2025-10-15", None, "Sonar acquires Gitar to enhance AI code review"),
    (9, "Cartograph", "Harvest Group", "consumer", "acquisition", "2025-08-15", None, "Rogers-based Harvest Group acquires Austin CPG agency"),
    (12, "Trudy's space", "Black's Barbecue", "real_estate", "asset_sale", "2025-09-15", None, "Black's BBQ acquires original Trudy's restaurant space for Austin expansion"),
    (16, "Austin Emergency Center (6 locations)", "St. David's HealthCare", "healthcare", "acquisition", "2025-11-15", None, "St. David's acquires 6 freestanding emergency care locations in Austin"),
    (17, "243-bed student housing community near UT Austin", "Ascentris / Student Quarters JV", "real_estate", "acquisition", "2025-10-01", None, "Joint venture acquires student housing near University of Texas"),
    (18, "The Arboretum retail center", "Asana Partners", "real_estate", "acquisition", "2025-09-01", None, "Asana acquires The Arboretum retail center in Austin"),
    (21, "Inpatient rehabilitation hospital near Austin", "Vital Capital Partners", "healthcare", "acquisition", "2025-08-01", None, "Vital Capital acquires inpatient rehab hospital near Austin"),
    (23, "Inland Geodetics", "SAM Companies", "services", "acquisition", "2025-07-15", None, "Austin-based SAM Companies acquires Inland Geodetics"),
    (24, "Pool Troopers", "SPS PoolCare", "services", "acquisition", "2025-09-15", None, "North Austin-based SPS PoolCare acquires Pool Troopers"),
    (28, "Wonderbelly", "Procter & Gamble", "consumer", "acquisition", "2025-10-15", None, "P&G acquires Austin-based health product startup Wonderbelly"),
    (32, "Austin medical facility", "BGO JV", "real_estate", "acquisition", "2025-08-01", None, "BGO joint venture acquires Austin medical office building"),
    (33, "180-acre parcel, Bastrop", "EdgeConneX", "real_estate", "acquisition", "2025-09-01", None, "EdgeConneX acquires 180 acres near its Bastrop data center project"),
    (34, "232-unit apartment community, Austin", "Continental Realty Group", "real_estate", "acquisition", "2025-08-15", None, "Continental Realty acquires 232-unit Austin multifamily"),
    (35, "Colorado diagnostics company", "Natera", "healthcare", "acquisition", "2025-11-01", None, "Austin biotech giant Natera acquires Colorado-based diagnostics company"),
    (41, "Viagen Pets and Equine", "Colossal Biosciences", "healthcare", "acquisition", "2025-10-15", None, "Colossal Biosciences acquires Austin-based ViaGen Pets and Equine"),
    (42, "Cactus Moon Lodge", "Delaware North", "consumer", "acquisition", "2025-08-01", None, "Delaware North acquires resort-style event venue near Austin"),
    (45, "670-bed student housing community, Austin", "Core Spaces", "real_estate", "acquisition", "2025-09-01", None, "Core Spaces acquires 670-bed student housing near UT Austin"),
    (46, "Plantscape design companies (2)", "Ambius", "services", "acquisition", "2025-08-15", None, "Ambius acquires two plantscape design companies in Austin"),
    (47, "Abt Insurance Agency", "Senior Market Sales", "financial_services", "acquisition", "2025-09-15", None, "SMS acquires Austin-based Abt Insurance Agency"),
    (48, "Cheer Up Charlies", "PRIDE Holdings Group (FL)", "consumer", "acquisition", "2025-10-01", None, "Florida investment firm acquires Austin LGBTQ+ nightclub"),
    (49, "271 acres, Austin", "CleanSpark", "energy", "acquisition", "2025-09-01", None, "CleanSpark acquires Austin land and executes power supply agreements"),
    (50, "Echo Apartments (274 units)", "Karlin Real Estate", "real_estate", "acquisition", "2025-10-01", None, "Karlin Real Estate acquires 274-unit Echo Apartments near downtown Austin"),
    (53, "LALO Tequila", "Tito's Vodka", "consumer", "acquisition", "2025-11-01", None, "Austin-based Tito's Vodka acquires Austin-based LALO Tequila"),
    (55, "Old Town hotel, Austin", "Austin investor (undisclosed)", "real_estate", "acquisition", "2025-08-15", None, "Austin investor acquires Old Town hotel"),
    (62, "Uno Health", "Findhelp", "tech", "acquisition", "2025-10-15", None, "Austin-based Findhelp acquires Uno Health to modernize benefits access"),
    (64, "2 grocery stores", "Wheatsville Co-op", "consumer", "asset_sale", "2025-09-01", None, "Wheatsville Co-op acquires 2 stores as part of Austin expansion"),
    (67, "Pointe on Rio student housing, Austin", "Landmark Properties", "real_estate", "acquisition", "2025-08-01", None, "Landmark Properties acquires Pointe on Rio student housing in Austin"),
    (71, "The Lenox Boardwalk apartments, Austin", "Bell Partners", "real_estate", "acquisition", "2025-07-15", None, "Bell Partners acquires The Lenox Boardwalk multifamily in Austin"),
    (79, "Silicon Labs", "Texas Instruments", "tech", "acquisition", "2025-06-01", 7500000000.0, "TI to acquire Austin-based Silicon Labs in $7.5B deal"),
    (80, "Austin Private Wealth", "Cerity Partners", "financial_services", "merger", "2025-04-15", None, "Cerity Partners merges with Austin Private Wealth ($1.4B AUM)"),
    (88, "3 Austin golf courses", "Hanlim Construction (Korea)", "real_estate", "acquisition", "2025-05-01", None, "Korean Hanlim Construction acquires three Austin-area golf courses"),
    (92, "Austin Eastciders", "Blake's Beverage Co. (merger of Blake's/Avid/Austin Eastciders)", "consumer", "merger", "2025-03-15", None, "Three-way cider company merger anchored by Austin Eastciders"),
    (98, "Block 21", "Ryman Hospitality Properties", "real_estate", "acquisition", "2024-12-15", None, "Ryman Hospitality plans to acquire Block 21 in downtown Austin"),
    (99, "Austin office tower (record pricing)", "Cousins Properties", "real_estate", "acquisition", "2024-11-01", 521800000.0, "Cousins Properties acquires downtown Austin office tower for $521.8M"),
    (100, "Downtown Austin office tower", "Cousins Properties", "real_estate", "acquisition", "2024-11-01", 521800000.0, "Cousins acquires downtown Austin office tower"),
    (102, "Nacogdoches Biomass Facility", "Austin Energy", "energy", "acquisition", "2024-10-01", 460000000.0, "Austin Energy to acquire Nacogdoches Biomass Facility for $460M"),
    (104, "Infineon Austin Fab 25", "SkyWater Technology", "industrial", "acquisition", "2024-09-15", None, "SkyWater Technology to acquire Infineon's Austin Fab 25"),
    (105, "Page (architecture firm)", "Stantec", "services", "acquisition", "2024-08-15", None, "Stantec acquires Page, an architecture firm with major Austin presence"),
    (108, "Austin-area doughnut shop", "Austin private equity firm", "consumer", "acquisition", "2024-07-15", None, "Austin PE firm acquires iconic Texas doughnut shop"),
    (109, "MSB School Services", "Private equity firm (undisclosed)", "education", "acquisition", "2024-09-01", None, "Private equity firm acquires Austin-based MSB School Services"),
]


def main() -> None:
    candidates = {json.loads(line)["id"]: json.loads(line)
                  for line in open(CACHE / "candidates.jsonl")}

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

    inserted = 0
    for source_id, target, acquirer, sector, deal_type, date, ev, desc in SEED_DEALS:
        src = candidates.get(source_id, {})
        conn.execute("""
            INSERT OR REPLACE INTO deals
            (source_id, target, acquirer, sector, deal_type, announced_date,
             ev_usd, status, description, title, link, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (source_id, target, acquirer, sector, deal_type, date, ev,
              "announced", desc,
              src.get("title", ""), src.get("link", ""), src.get("source", "")))
        inserted += 1
    conn.commit()
    conn.close()
    print(f"seeded {inserted} deals into {DB}")


if __name__ == "__main__":
    main()
