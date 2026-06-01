// Austin MSA M&A Activity, 2024 to 2026
#import "lib.typ": *

#show: template

#set document(
  title: "Austin MSA Mid-Market M&A Activity, 2024 to 2026",
  author: "Deep Hayer",
)

#header(
  "Austin MSA Mid-Market M&A Activity, 2024 to 2026",
  "Deep Hayer",
  "May 2026",
  "M&A | Private Markets | Austin",
)

#abstract[
  This paper documents 43 announced corporate M&A and commercial real estate
  transactions involving Austin MSA targets or acquirers, surfaced from public
  RSS and press wire ingestion between mid-2024 and May 2026. Real estate
  dominates the visible deal flow (42 percent), followed by consumer (19
  percent), healthcare (9 percent), and services (9 percent). The largest
  deal is Texas Instruments' \$7.5 billion acquisition of Austin-based
  Silicon Labs. The paper documents the data pipeline, the limits of free
  data, and what a free-data Austin deal tracker actually surfaces.
]

= Why Track Austin M&A

Austin sits at the intersection of three deal-flow drivers: the technology
build-out of the last decade, a hot commercial real estate cycle, and a
maturing wave of founder-owned businesses approaching transition. For a
boutique investment bank or family office targeting central Texas, the
relevant data is rarely "did this deal happen" but "did this deal happen
and what does it tell us about the next one." That requires a continuously
maintained dataset.

The standard answer is a PitchBook, S&P Capital IQ, or Mergermarket
subscription. Those are excellent and expensive. This paper asks how much
of the same picture is reachable from free public sources alone.

= Data Pipeline

We ingest from nine RSS feeds spanning national press wires (PR Newswire
Texas, GlobeNewswire, BusinessWire), local business news (Austin Business
Journal, Austin American-Statesman), and four Google News standing
queries on M&A-related phrasing localized to Austin. Items are deduplicated
by URL.

A regex prefilter keeps items containing at least one M&A trigger phrase
("acquires," "to acquire," "merger," "buyout," "private equity," and
similar) along with at least one Austin-metro locality mention. The
prefilter cuts the candidate set by about 70 percent and reduces downstream
cost.

The classifier is the Claude CLI invoked in batch with a JSON-only output
schema. For each candidate it returns the deal target, acquirer, sector,
deal type, announced date, disclosed enterprise value, and a strict
boolean for whether the item is a genuine corporate M&A or commercial real
estate transaction. This step rejects sports player acquisitions, City of
Austin land purchases, military command mergers, university restructurings,
and movie-rights deals, all of which match the regex prefilter.

Surviving records are upserted to a SQLite database keyed by source item
ID. The dashboard reads from SQLite. Re-running ingestion is incremental.

= What the First Pass Shows

#fig("figures/fig1_volume.png", [Announced Austin MSA deals by month, mid-2024 through May 2026.])

The visible deal flow runs roughly two to four announced deals per month in
the dataset, with clustering in mid-2025. This is a floor, not a ceiling.
Many small deals never hit a press wire; many large deals are first
reported in subscription outlets. The shape of the curve is meaningful;
the absolute count understates true activity.

#fig("figures/fig2_sector.png", [Deal count by sector. Real estate dominates, consumer is second, healthcare and services tie for third.])

Real estate is the largest visible sector at 18 of 43 deals. This reflects
both the cycle (Austin office and multifamily transacting heavily on
repricing) and a reporting artifact (CRE deals are more reliably covered
by trade publications with public RSS than smaller private business sales).
Consumer follows with eight deals, dominated by food and beverage
roll-ups: Tito's acquired LALO Tequila, Black's Barbecue acquired the
original Trudy's space, Procter & Gamble acquired Austin-based Wonderbelly,
and Blake's, Avid, and Austin Eastciders merged into a three-way cider
combination. Healthcare and services tie for third.

== Disclosed enterprise values

#fig("figures/fig3_ev.png", [Disclosed enterprise values, log scale. Tech and real estate concentrate the top of the range; most other deals do not disclose.])

Four deals in the dataset have publicly disclosed enterprise values:

#table(
  columns: (1fr, 1fr, 1fr, auto),
  align: (left, left, left, right),
  [*Target*], [*Acquirer*], [*Sector*], [*EV*],
  [Silicon Labs], [Texas Instruments], [Tech], [\$7,500M],
  [Downtown Austin office tower], [Cousins Properties], [Real Estate], [\$522M],
  [Nacogdoches Biomass Facility], [Austin Energy], [Energy], [\$460M],
  [Block 21 office tower], [Ryman Hospitality], [Real Estate], [n/d at signing],
)

The \$9 billion disclosed sum is a small fraction of the true total. The
core limitation of free-source M&A tracking is that small and mid-market
deals (the \$10M to \$100M EV range that Westlake Securities, pH Partners,
and Morgan Kingston actually advise on) rarely disclose values publicly.
What free sources surface well is deal *existence* and target / acquirer /
sector. What they do not surface is multiples, structures, or financials.

= Use Cases for a Boutique Analyst

Even with the limits above, the dataset answers questions an Austin
boutique IB analyst is asked weekly:

- *Which buyers are active in our sector right now.* The data answers
  this directly. Cousins, Asana Partners, Karlin, Continental Realty, Bell,
  Landmark, and Core Spaces are all active Austin RE buyers.
- *What types of consumer assets are trading.* Food and beverage roll-ups,
  hospitality, and specialty retail. The sector counts make this visible.
- *Who is doing strategic versus financial deals.* Strategic acquirers
  (P&G, TI, Procter, St. David's) versus PE buyers cluster differently in
  the data.
- *Calendar of comparable deals to cite in a pitch.* Filterable by sector
  and date.

For the questions free data cannot answer (multiples, deal structures,
financials), the right answer is either a paid subscription or direct
sourcing. The dataset narrows the search; it does not replace it.

= Limitations

Honest caveats:

- *Disclosure bias.* The dataset is biased toward deals that hit a public
  press release. Private equity middle-market deals routinely do not.
- *Coverage gaps in the Austin-specific feeds.* The Austin Business
  Journal RSS and the Austin American-Statesman business RSS returned zero
  items in the first ingestion run, suggesting their feeds are stale or
  block automated readers. The dashboard relies more heavily on Google
  News and the national press wires than is ideal.
- *Classifier error.* The Claude classifier achieves high precision (all 43
  surfaced deals were verified by hand) but uncertain recall. Real deals
  almost certainly fell through.
- *Sample size.* 43 deals over ~18 months is enough to see sector
  composition but not enough for serious cross-sectional analysis.

= Next Steps

A v2 would add (1) Mergr or Crunchbase Pro free-tier scraping for a
multiples table where available, (2) direct Austin Business Journal
scraping with a session cookie to recover the local feed, (3) state
filings ingestion (Texas Secretary of State filings for new LLC
formations tied to recent transactions), and (4) automatic generation
of "active in sector" tear sheets per acquirer.

= Reproducibility

Companion essay at #link("https://deephayer.com/essais/2026-austin-ma-tracker")[deephayer.com].
Run `python -m data.ingest_rss && python -m data.prefilter && python -m data.extract && python -m src.aggregate && python -m src.plots && cd paper && typst compile dealiq.typ`.
The interactive dashboard is `streamlit run app.py`.
