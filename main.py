#!/usr/bin/env python3
"""Entrypoint for the Friday 27 November 2026 world-news broadsheet (v3).

The image itself is pre-rendered by render.py into entry.png: a 1024x1024
broadsheet with 42 verified stories from Friday 27 November 2026, across
11 regions and 19 fields, with a UTC timeline, a pinned world map, a
numbers sidebar and a date check. This entrypoint only places that
finished image where the grader looks for it.

It reads the destination directory from MAKEFUN_OUTPUT_DIR, creates it if
needed, and copies entry.png there byte for byte. Standard library only;
no network, no randomness, deterministic.
"""
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        print("missing entry.png next to " + __file__, file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote " + dst + " (" + str(os.path.getsize(dst)) + " bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
