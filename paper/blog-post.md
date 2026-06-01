---
title: Tracking Austin M&A from free sources
date: 2026-05-29
tags: [m-and-a, austin, investment-banking, data]
summary: I built a free-data Austin M&A tracker because I wanted to cold-email boutique investment banks with something more useful than my resume. 43 deals, $9B disclosed, what the data shows, and where it falls short.
---

This post is the short version of [a paper](/papers/austin-ma-tracker.pdf) I wrote because I was about to cold-email a list of Austin boutique investment banks and I wanted to show up with the kind of internal tool an analyst would build in their first month rather than the kind of pitch deck a high school junior would send.

## The question

If you are a boutique IB analyst in Austin, two questions land in your inbox every week. Who is buying in our sector right now, and what comparable deals can we cite in this pitch. The standard answer is PitchBook or S&P Capital IQ. Those are excellent and they cost more than a 16 year old's allowance.

So the question I wanted to answer is: how much of that picture do you actually need a subscription for? What fraction of useful Austin M&A signal is reachable from free public sources, if you build the right pipeline?

## The pipeline

The answer turned out to be: most of the deal *existence* signal, almost none of the *valuation* signal.

The build is straightforward. Nine RSS feeds: national press wires (PR Newswire Texas, GlobeNewswire, BusinessWire), local business news (Austin Business Journal, Austin American-Statesman), and four Google News standing queries for M&A phrasing localized to Austin. Dedupe by URL. Regex prefilter for items that look like deal announcements involving Austin metro localities. Send the survivors to the Claude CLI with a strict JSON schema asking for target, acquirer, sector, deal type, date, EV, and a hard boolean for "is this a real corporate or RE transaction, not a sports trade or a parkland purchase." Upsert to SQLite. Serve a Streamlit dashboard on top.

The regex cuts about 70 percent of items. The LLM classifier handles the remaining 30 percent, and crucially it is what distinguishes "Texas Instruments acquires Silicon Labs for \$7.5B" from "Austin FC acquires forward Christian Ramirez." Both match the regex. Only one belongs in the dataset.

## What surfaced

43 verified deals over about 18 months, totaling \$9B in disclosed enterprise value across four deals where value was actually published.

Real estate dominates at 18 deals, 42 percent of the visible flow. This is partly cycle (Austin office and multifamily are transacting heavily on repricing) and partly a reporting artifact (CRE deals get covered by trade publications with reliable RSS feeds). Names you see repeatedly on the buyer side: Cousins Properties, Asana Partners, Karlin Real Estate, Continental Realty Group, Bell Partners, Landmark Properties, Core Spaces. If you wanted a starting list of active Austin commercial real estate buyers, that's the table.

Consumer comes in second at 8 deals. The Austin consumer story right now is food and beverage roll-ups: Tito's acquired LALO Tequila (two Austin-born spirits brands), Black's Barbecue acquired the original Trudy's restaurant space, P&G acquired Austin-based Wonderbelly health products, and Blake's, Avid, and Austin Eastciders merged into a three-way cider company. The pattern is strategic acquirers picking up well-positioned Austin brands.

Healthcare ties services at four deals each. The healthcare bucket is dominated by St. David's HealthCare acquiring six freestanding emergency care locations, Natera acquiring a Colorado diagnostics company, Vital Capital Partners acquiring an inpatient rehab hospital, and Colossal Biosciences acquiring Austin-based ViaGen Pets. Tech is thinner than expected at three deals, with the TI / Silicon Labs deal towering over the others by a factor of more than ten.

## Where free data falls down

The honest limitation: of 43 deals, only 4 had publicly disclosed enterprise values. That is the structural problem. Mid-market private deals in the \$10M to \$250M range, which is exactly the range Westlake Securities and pH Partners and Morgan Kingston actually advise on, almost never disclose valuations in press releases. Those numbers live in subscription databases.

What free data does well: it tells you *that* deals happened, *who* the buyers are, *which sectors* are moving. That is enough to answer "who should we pitch to next" and "what comparable deals can we cite." It is not enough to answer "what multiple should we expect."

For a boutique analyst the right read is that a free Austin tracker narrows the search. It does not replace a subscription, but it covers the daily-monitoring layer at zero cost, freeing the subscription budget for actual diligence.

## What I would build next

A v2 has obvious work:

- Crunchbase Pro free-tier scraping to surface a multiples table where deals are reported there but not on press wires.
- Direct scraping of the Austin Business Journal with a session cookie, since their public RSS returned zero items in my run and that's the most concentrated Austin business news source.
- Texas Secretary of State filing ingestion to catch the legal-entity formation events that often follow a closed deal but never make the press wire.
- Per-acquirer "tear sheets" auto-generated from the dataset, ready to drop into a banker's pitch deck.

If you work at an Austin boutique IB, a family office, or anywhere else this kind of tool would be useful, I would love to talk. Contact info on [about](/about).
