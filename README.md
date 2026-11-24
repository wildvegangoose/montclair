# Montclair Through Time

An unofficial fan history site for **Montclair, New Jersey**, built from the same architecture as
[South Orange Through Time](https://wildvegangoose.github.io/south-orange/) and
[Maplewood Through Time](https://wildvegangoose.github.io/maplewood/).

## What's Included

- **Time Machine (`index.html`)**: Interactive 1600–2026 Montclair panorama (Watchung ridge, Toney's Brook, Cranetown & Speertown, Crane House, Shultz House, Carnegie Library, First Congregational Church, Lackawanna Terminal, Montclair Art Museum, Wellmont Theater, Presby Iris Gardens, Anderson Park, Upper Montclair depot, Van Reyper-Bond House, Cliffside Hose Co. No. 4, College Hall), census sparkline, and sourced era histories.
- **Explore the Map (`explore.html`)**: 53 documented Montclair & historic-township places over 7 single-quad USGS historical topographic overlays (1888, 1898, 1906, 1924, 1947, 1955, 1972) and 4 NJ Office of GIS aerial WMS layers (1930, 1995, 2007, 2020), with approximate pre-1868 jurisdiction boundaries (Newark 1666–1811, Bloomfield Township 1812–1867, Montclair 1868–present) and seats of government.
- **Your House's Story (`house.html`)**: Geocoded neighborhood narrative + 201,778 pre-1951 directory listings across 318 streets and 10,166 addresses (16 editions from 1910–1949 via Montclair History Online, with 29,990 cropped line scans for 1910, 1925, 1935, and 1949) + **1885 & 1907 Sanborn fire-insurance maps** (Library of Congress, public domain) + Library of Congress Gottscho-Schleisner historic house photos.
- **16 Landmarks (`landmarks.html`, `landmarks/*.html`)**: In-depth histories, timelines, public-domain/CC photographs with credits, Sanborn sheets, and 11-layer Through-the-Ages map/aerial progressions (176 crops).
- **Notable People (`people.html`)**: 278 notable people with Montclair ties; home addresses shown strictly for verified deceased pre-1951 residents (never for living or post-1950 residents).
- **Timeline (`timeline.html`) & Research Guide (`research.html`)**: Chronological history, 8-step house research guide, and full 55-source bibliography.
- **Static SEO & Analytics**: `robots.txt`, `sitemap.xml` (23 indexable URLs), 16 pre-rendered static landmark pages, Schema.org JSON-LD, Open Graph / Twitter Cards, crawlable HTML containers, and Cloudflare Web Analytics across all pages.

## Tools & Tests

- Town settings: [`tools/town.json`](tools/town.json)
- Rebuild street index: `python3 tools/archive/build_index.py`
- Rebuild static SEO & landmark pages: `python3 tools/seo/build_seo.py`
- Run regression & accuracy suite: `python3 -m unittest discover -s tests -v`
