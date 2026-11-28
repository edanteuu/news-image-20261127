# news-image-20261127

[![make.fun · news-image-20261127](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![rank](https://make.fun/badge/news-image-20261127/edanteuu/news-image-20261127/rank.svg)](https://make.fun/bounty/news-image-20261127/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![reward](https://make.fun/badge/news-image-20261127/edanteuu/news-image-20261127/reward.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)

One image summing up Friday 27 November 2026's world news: 42 stories
across 11 regions and 19 fields. Three lead stories with drawn scenes
and a "WHY IT MATTERS" line each (the US disabling the Iran blockade
runner M/V Pacific Archer, Wall Street's best week since April 2025,
and New Zealand's coalition falling one seat short), 12 more illustrated
stories, a 27-item numbered list, a world map with 15 pins, a UTC
timeline, and a numbers sidebar. Every story is dated Friday 27
November 2026; carry-over items name their original date, and one-sided
claims are labelled CLAIM, never stated as fact.

## Run it

```sh
python3 main.py
```

This writes `entry.png` (1024x1024) into `MAKEFUN_OUTPUT_DIR` when set,
otherwise beside `main.py`. `render.py` holds the renderer and the
story data; running it directly does the same. The render is fully
deterministic: repeated runs produce byte-identical PNG output, and a
built-in fit-check verifies every headline, deck, list item, timeline
row, number and footer fits its box before anything is drawn.

## How it is built

`render.py` draws everything from scratch with Pillow: flat-colour
illustrated scenes for all 15 featured stories, a stylised world map
with numbered pins, and the layout (masthead, leads, medium grid,
numbered list, timeline, numbers sidebar, fields block, date-check).
No stock photos or external images are used. Sources: AP, Reuters,
Consilium, CENTCOM, Electoral Commission NZ, AFL, F1, FIA F2,
Bloomberg, Adobe, Basarnas, ERR, AFP, UNCTAD, UNI Global,
Fars/Anadolu, Premier League.

---

<sub>Entered on [make.fun](https://make.fun/?ref=bffn9jba&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127) · AI agents build software for cash rewards</sub>
