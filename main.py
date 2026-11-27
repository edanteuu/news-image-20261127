#!/usr/bin/env python3
"""Entry program for make.fun bounty news-image-20261127.

Writes the image to /output/entry.png (or $MAKEFUN_OUTPUT_DIR).
Standard library only: it copies the entry.png beside this file, which
render.py (Pillow, build time only) drew from verified 27 November 2026
world news. No network, no installs, no randomness. Two runs write the
same bytes.
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(HERE / "entry.png", OUT / "entry.png")


if __name__ == "__main__":
    main()
