"""Registry of news / RSS sources covering Austin MSA M&A activity.

Categories:
  press_wire     -- press releases (PR Newswire, GlobeNewswire, BusinessWire) filtered for Texas
  news_general   -- general news with Austin business coverage
  trade_pubs     -- trade publications (real estate, tech, healthcare) with deal coverage

Each entry has: name, url, type (rss / google_news_query), category.
"""

SOURCES = [
    # Press wires (national press release distributors)
    {"name": "PR Newswire Texas", "url": "https://www.prnewswire.com/rss/news-releases/texas-news-list.rss", "type": "rss", "category": "press_wire"},
    {"name": "GlobeNewswire", "url": "https://www.globenewswire.com/RssFeed/orgclass/1/feedTitle/GlobeNewswire+-+News+from+Texas", "type": "rss", "category": "press_wire"},
    {"name": "BusinessWire Texas", "url": "https://feed.businesswire.com/rss/home/?rss=G1QFDERJXkJeGVtRVA==", "type": "rss", "category": "press_wire"},

    # General news (Austin / Texas coverage)
    {"name": "Austin Business Journal", "url": "https://www.bizjournals.com/austin/news/rss.xml", "type": "rss", "category": "news_general"},
    {"name": "Austin American-Statesman business", "url": "https://www.statesman.com/business/rss/", "type": "rss", "category": "news_general"},

    # Google News queries (RSS via news.google.com)
    {"name": "Google News: Austin acquisition", "url": "https://news.google.com/rss/search?q=%22Austin%22+%22acquires%22&hl=en-US&gl=US&ceid=US:en", "type": "rss", "category": "google_news"},
    {"name": "Google News: Austin merger", "url": "https://news.google.com/rss/search?q=%22Austin%2C+Texas%22+merger&hl=en-US&gl=US&ceid=US:en", "type": "rss", "category": "google_news"},
    {"name": "Google News: Austin to acquire", "url": "https://news.google.com/rss/search?q=%22Austin%2C+Texas%22+%22to+acquire%22&hl=en-US&gl=US&ceid=US:en", "type": "rss", "category": "google_news"},
    {"name": "Google News: Austin private equity", "url": "https://news.google.com/rss/search?q=%22Austin%2C+Texas%22+%22private+equity%22+acquisition&hl=en-US&gl=US&ceid=US:en", "type": "rss", "category": "google_news"},
]
