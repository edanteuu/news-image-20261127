#!/usr/bin/env python3
"""Entrypoint for the news-image-20261127 entry.

Renders the 1024x1024 news summary for Friday 27 November 2026 and
writes it as entry.png: into MAKEFUN_OUTPUT_DIR when that is set,
otherwise beside this file. The render is deterministic, so repeated
runs produce byte-identical output.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import render

if __name__ == "__main__":
    print(render.main(os.environ.get("MAKEFUN_OUTPUT_DIR")))
