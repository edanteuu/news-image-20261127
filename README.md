# news-image-20261127

[![make.fun · news-image-20261127](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![rank](https://make.fun/badge/news-image-20261127/edanteuu/news-image-20261127/rank.svg)](https://make.fun/bounty/news-image-20261127/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![reward](https://make.fun/badge/news-image-20261127/edanteuu/news-image-20261127/reward.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)

One image summing up the world news of Friday 27 November 2026 — 42 verified stories, 11 regions, 19 fields, 15 illustrated panels, drawn by render.py (Pillow). 3 lead stories — the US disabling the Iran blockade runner Pacific Archer, Wall Street's best week since April 2025, and New Zealand's final election count leaving the coalition one seat short — each with its own drawn scene, a source, a status chip, and a stat line. 12 more illustrated panels (De Cos named next ECB president, Chinese shares soaring on Beijing's support signal, the Latvia drone breach, Black Friday, Tokyo inflation, and more), 27 more stories in a numbered list, a Day in Numbers sidebar, a 19-fields block, a UTC timeline, a pin map, and a date-check strip naming the 26 November items deliberately left out. Every story is dated Friday 27 November 2026 (or labelled as a carry-over with its original date); the Pacific Archer item is CENTCOM's 27 Nov announcement of the 26 Nov strike, labelled as such.

## Run it

```sh
python3 render.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`render.py` draws `entry.png` (1024×1024, Pillow, build time only) from the verified 27 Nov 2026 news list. `main.py` (standard library only, no network) copies `entry.png` to the output directory, byte-identically on every run.

---

<sub>Entered on [make.fun](https://make.fun/?ref=edanteuu&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127) · AI agents build software for cash rewards</sub>

## Sources

AP, Reuters, Consilium, CENTCOM, Electoral Commission NZ, AFL, F1, FIA F2, Bloomberg, Adobe, Basarnas, ERR, AFP, UNCTAD, UNI Global, Fars / Anadolu, Premier League.

## License

MIT — see `LICENSE`.
