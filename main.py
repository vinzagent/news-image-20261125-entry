#!/usr/bin/env python3
"""news-image-20261125 entrypoint (standard library only).

Copies the pre-rendered entry.png shipped in this repository to the
grader's output directory. The image itself is drawn offline by gen.py
(Pillow, run locally at build time); the grader runs this file with no
network and only the standard library, so the copy must stay byte-exact
and dependency-free. Running it twice writes identical bytes.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")

def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    # The grader collects outputs as another user: leave the file readable.
    os.chmod(dst, 0o644)
    print("wrote %s (%d bytes)" % (dst, os.path.getsize(dst)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
