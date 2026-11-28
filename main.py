#!/usr/bin/env python3
"""Entrypoint for the news-image-20261127 entry.

Copies the pre-rendered entry.png (beside this file) into
MAKEFUN_OUTPUT_DIR (default /output). Stdlib only: the grader runs
this in a bare Python image with no third-party packages, so it
must not import render or PIL or touch fonts.
"""

import os
import shutil
import sys


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        print("entry.png not found beside main.py", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dest)
    print(dest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
