#!/usr/bin/env python3
"""Entrypoint for the 27 November 2026 news broadsheet (v3 revision).

The image is drawn at build time by render.py and shipped as entry.png.
This program only places that exact file at the grader's output path.
Standard library only; no network, no randomness, deterministic.
"""
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    if not os.path.isfile(src):
        print("missing entry.png next to " + __file__, file=sys.stderr)
        return 1
    shutil.copyfile(src, dst)
    print("wrote " + dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
