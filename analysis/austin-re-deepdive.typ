#import "lib.typ": template, header, abstract, fig

#show: template

#header(
  "Austin real estate M&A 2024-2025: who is buying, what, and why",
  "D Hayer",
  "May 2026",
  "Real estate sub-segment deep-dive on the Austin MSA M&A dataset.",
)

#abstract[
  Of the 43 verified Austin MSA deals in the v1 tracker, 17 are real estate (after deduping a
  twice-sourced Cousins trade). Institutional sponsors account for 8 of 17 buyers, mid-market
  sponsors 3, private and undisclosed buyers 4, with one corporate strategic and one foreign.
  The standout pattern is concentration in UT-adjacent student housing: three different
  institutional sponsors closed three deals in three consecutive months. Multifamily is
  dominated by mid-cap sponsors picking up 200 to 300 unit value-add product. Office is
  bifurcated between one trophy trade (Cousins, \$522M) and two private deals at undisclosed
  pricing. The single most underrated print in the set is EdgeConneX's 180-acre Bastrop land
  buy, which is the Austin real estate market pricing in the ERCOT load-growth thesis directly.
]

= The dataset

The v1 tracker surfaced 43 verified deals across the Austin MSA from August 2024 through May 2026.
After deduplicating a Cousins trade that hit two newswires, 17 are real estate. Only one of
those 17 disclosed enterprise value (the Cousins office trade at \$522M); the rest are
unit-count or asset-level reporting without trade pricing. The disclosure ceiling is the
binding constraint on free-data analysis and is exactly the limit the v1 tracker was written to
characterize.

#fig("figures/asset_mix.png", "Asset class mix across 17 deduplicated RE deals.")

The mix is income-property dominant: 4 multifamily, 3 office, 3 student housing, plus singles
across retail, hotel, medical office, data center land, recreation land, and mixed-use hotel.

= Who is buying

#fig("figures/buyer_type.png", "Buyer type concentration. Institutional sponsors lead.")

Eight of 17 buyers are institutional sponsors: Cousins Properties, Ryman Hospitality, Bell
Partners, Landmark Properties, BGO JV, Core Spaces, Asana Partners, and Ascentris with
Student Quarters. Three of 17 are mid-market sponsors: Continental Realty Group, Karlin Real
Estate, and Haven Housing. Four are private or undisclosed buyers concentrated in office and
hotel. One corporate strategic (EdgeConneX) and one foreign capital print (Hanlim
Construction, Korea, recreation).

The conspicuous absence is the traditional core institutional bench: no Blackstone, no
Brookfield, no KKR Real Estate, no Starwood, no PGIM. Either those buyers are sitting on
their hands in Austin (consistent with the broader 2024-2025 institutional pullback from
Sun Belt growth markets after the rent reset) or they are buying through structures that do
not announce as headline-grabbing trades. Both are plausible. Free-data ingestion
cannot distinguish.

= The standout: student housing concentration

#fig("figures/student_concentration.png", "Three institutional sponsors enter UT-adjacent in three months.")

The most concentrated pattern in the dataset. Three of 17 deals are UT-adjacent student
housing, all between August and October 2025, all from different institutional sponsors:
Landmark Properties (Pointe on Rio, July to August window), Core Spaces (670-bed community,
September), and Ascentris with Student Quarters (243-bed community, October).

Three sponsors do not move into a single sub-asset class in a single submarket in a single
quarter by coincidence. The implied thesis: UT enrollment growth plus a thin pipeline of
purpose-built student housing plus per-bed rent compression in conventional multifamily
makes the relative trade attractive. UT-adjacent purpose-built has historically traded at
50 to 100 bps tighter cap rates than conventional multifamily for the same vintage; if
conventional multifamily caps expanded from 4.50 to 5.50 over 2024 and student housing
expanded by less, the spread is the deal.

What this signals: if a sponsor or family office is allocating into Austin RE in 2026, the
"smart institutional money" tape says UT-adjacent student housing first, suburban
mid-vintage multifamily second.

= Multifamily is mid-cap sponsor territory

Four multifamily deals, with one institutional name (Bell Partners, The Lenox Boardwalk) and
three mid-cap sponsors (Continental at 232 units, Karlin at 274 units, Haven at suburban
unspecified). All four are 200 to 300 unit value-add or core-plus product in central or
suburban Austin.

The mid-cap dominance is the Austin multifamily story right now. Core institutional capital
is on the sidelines waiting for cap rates to clear. Mid-cap sponsors with established
operating platforms can buy at 5.50 to 6.50 cap on in-place NOI with light value-add and
underwrite to a 6.50 to 7.50 stabilized yield two years out. That spread is exactly the
trade Continental and Karlin are making. The institutional bench will return when caps
stabilize and the entry-vs-exit spread compresses.

= Office is bifurcated

Three office trades. One trophy: Cousins Properties acquires a downtown tower for \$522M
(November 2024). Two private or undisclosed: a downtown building to a private investor and
an unspecified Austin office property to a private investor (both September and October
2025).

The trophy-vs-distress split is the post-2022 office story compressed into a single
metro-quarter sample. Public-market REITs and core institutional capital are willing to write
checks for irreplaceable trophy product at materially repriced bases. Everything below
trophy is trading privately at prices that nobody will disclose because the disclosure would
print a comp that hurts every other lender's book in the submarket.

Combined with the CBD conversion screener finding (zero of 25 Class B/C buildings pencil for
residential conversion at v1 assumptions), the picture is: Austin CBD office is either a
trophy buy with a 7-year hold thesis, a private distress trade at 50 to 70 percent of last
cycle basis, or sitting empty waiting for a subsidy stack to materialize for conversion.
There is no middle.

= The EdgeConneX print is the underrated signal

EdgeConneX acquired 180 acres in Bastrop in September 2025, adjacent to its existing data
center project. Single line item in the dataset, no enterprise value disclosed, easy to miss.

It is the most important print in the 17 for what it signals about Austin real estate
allocation. EdgeConneX is one of the major hyperscale data center developers in the country.
The Bastrop expansion is data center land banking inside ERCOT, in the metro with the
fastest ERCOT load growth in the country. This is exactly the thesis quantified in
The ERCOT backtest: ERCOT load growth is driven by data center buildout, and the buildout is real
enough that land 35 miles east of Austin is now strategic data center inventory.

For an Austin family office or CRE allocator, the implication is concrete: industrial land
east of the city on transmission-accessible corridors is being repriced by hyperscaler land
buying. The window to acquire raw land at agricultural pricing is closing.

= What the data cannot tell you

Five gaps that bound this analysis:

1. Trade pricing on 16 of 17 deals. Only Cousins disclosed. Cap rates, price per unit, price
   per bed, price per square foot all unknown for the rest. PitchBook or Real Capital
   Analytics would close most of this gap.
2. Sub-asset detail (unit mix, vintage, in-place vs market rent). Available in CoStar; not
   in free data.
3. Buyer entity structure. "Bell Partners" is an institutional name but the actual vehicle
   could be a value-add fund, a separate account, or a JV. Different return targets, different
   hold periods, different read on what the trade signals.
4. Seller motivation. Forced selling tells you something different from a strategic exit at
   a market clearing price. Free data rarely captures the difference.
5. Off-market trades. Deals that close without a PR or news pickup are invisible. Below \$50M
   EV, this is a structural ceiling.

= Limitations

n equals 17 is too small to support inferential statistics. Everything in this paper is
descriptive pattern-finding on a single year of free-data ingestion. The hand-classification
of asset class and buyer type is the author's; another classifier might split hotel and
mixed-use differently or call Continental Realty institutional rather than mid-cap. The
narrative is the value, not the counts.

The v1 tracker also has a known submarket bias toward downtown and central Austin because press
coverage concentrates there. Suburban Cedar Park, Round Rock, and Pflugerville deals
underreport in the dataset. A v2 ingestion would add Travis CAD parcel-sale records and the
ABJ archive to close that gap.

= Next steps

In priority order:

1. Live underwriting on one deal where CoStar plus MLS plus public records provide enough
   inputs to build a clean valuation model. Most likely target: one of the mid-cap
   multifamily trades (Continental's 232-unit or Karlin's 274-unit Echo Apartments) where
   asset detail is publicly searchable.
2. Pull the next year of student housing closings to confirm the three-in-three-months
   concentration is a real trend rather than a window artifact.
3. Backfill cap rate point estimates using public-market REIT mark-to-market plus broker
   surveys. Even rough numbers materially upgrade the trade-pricing analysis.
4. Build a small Austin RE buyer-frequency database (institutional name, asset class history,
   typical trade size) to give cold outreach a credible "who else is buying this" hook.

= Audience

This paper is built for: Austin CRE allocators (Endeavor, Stream, Aquila, Treaty Oak,
Rocky Point), Austin family offices with RE allocations, and Austin boutique IB shops
covering RE intermediation (Westlake, pH Partners on the smaller mid-market). The useful
finding is the student-housing concentration and the EdgeConneX signal, both of which are
hard to assemble from free data unless you are running a daily ingestion pipeline against
the right sources.

#v(1em)
#line(length: 100%, stroke: 0.3pt + gray)
#v(0.4em)
#text(size: 8pt, fill: gray)[
  Companion essay at
  deephayer.com/essais/2026-austin-re-deepdive.
]
