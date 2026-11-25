#!/usr/bin/env python3
"""Copy the entry image sitting beside this file to the output directory.

Reads entry.png next to main.py (resolved via __file__, never via the
process working directory) and writes it to
$MAKEFUN_OUTPUT_DIR/entry.png (default /output), creating the output
directory if needed. Deterministic, stdlib only, no network.
"""
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print(dst)


if __name__ == "__main__":
    sys.exit(main())
