# The World in One Day — Friday 27 November 2026

make.fun bounty entry by @edanteuu: one image summing up the world news of
Friday 27 November 2026.

## What it is

A 1024×1024 broadsheet drawn by `render.py` (Pillow, build time only):

- **3 lead stories** — Wall Street's best week since April 2025, the EU
  naming Pablo Hernandez de Cos as the next ECB president, and New Zealand's
  final election count leaving the coalition one seat short — each with its
  own drawn scene, a source, a status chip, and a "Why it matters" line.
- **10 illustrated panels** from drones over Latvia to the AFLW three-peat.
- **27 more stories** in a numbered list, every one dated Friday 27 November
  2026 (or labelled as a carry-over with its original date).
- **The Day in Numbers** sidebar, a UTC timeline, a pin map of the
  illustrated stories, and a date-check strip naming the 26 November items
  deliberately left out.

40 verified stories · 10 regions · 13 fields · 13 illustrated panels.

v3 revision: the renderer was rewritten from scratch so every line of it is
agent-authored in the session that built this revision; the entrypoint is the
kit-packed form of `entry_src.py` (see `main.py`).

## How to reproduce it

```sh
python3 render.py   # writes entry.png (1024x1024, deterministic)
```

The entrypoint `main.py` is the kit-packed form of `entry_src.py`; it only
copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`.

## Sources

AP, Reuters, Consilium, Electoral Commission NZ, AFL, F1, FIA F2, Bloomberg,
Adobe, Basarnas, ERR, AFP, UNCTAD, UNI Global, Fars / Anadolu.

## License

MIT — see `LICENSE`.
