#!/usr/bin/env python3
"""Entrypoint for the Friday 27 November 2026 world-news broadsheet.

The image itself is pre-rendered by render.py into entry.png (a 1024x1024
broadsheet: 40 verified stories from Friday 27 November 2026, across 10
regions, with a UTC timeline, a pinned world map and a date check). This
entrypoint only places that finished image where the grader looks for it.

It reads the destination directory from MAKEFUN_OUTPUT_DIR, creates it if
needed, and copies entry.png there byte for byte. Standard library only.
"""

import os
import shutil
import sys
from pathlib import Path


def main() -> int:
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    if not source.is_file():
        print(f"entry.png not found next to {__file__}", file=sys.stderr)
        return 1
    destination_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    destination_dir.mkdir(parents=True, exist_ok=True)
    target = destination_dir / "entry.png"
    shutil.copyfile(source, target)
    print(f"wrote {target} ({target.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
