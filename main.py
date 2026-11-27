#!/usr/bin/env python3
"""Deliver the pre-rendered entry image for news-image-20261127.

The picture itself was drawn ahead of time by gen_image.py (which uses
PIL and is never run by the grader). This file only uses the Python
standard library, so it works in the grader's bare python3.13 image:
it copies the bundled entry.png next to this script into the output
directory and checks the result is a real, reasonably sized PNG.

Output directory: $MAKEFUN_OUTPUT_DIR, falling back to /output.
"""

import os
import shutil
import struct
import sys

MAX_BYTES = 1_048_576
MAX_SIDE = 1024
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def read_png_size(path):
    """Return (width, height) from a PNG file's IHDR chunk."""
    with open(path, "rb") as handle:
        header = handle.read(33)
    if len(header) < 33 or header[:8] != PNG_SIGNATURE:
        raise ValueError("not a PNG file: bad signature")
    if header[12:16] != b"IHDR":
        raise ValueError("not a PNG file: first chunk is not IHDR")
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    if not os.path.isfile(source):
        raise FileNotFoundError("bundled entry.png not found next to main.py")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")

    shutil.copyfile(source, target)

    # The copy must be byte-for-byte the bundled image.
    if os.path.getsize(target) != os.path.getsize(source):
        raise ValueError("copied entry.png does not match the bundled file")

    size = os.path.getsize(target)
    if not 0 < size <= MAX_BYTES:
        raise ValueError(
            "entry.png is %d bytes; expected between 1 and %d"
            % (size, MAX_BYTES)
        )
    width, height = read_png_size(target)
    if width > MAX_SIDE or height > MAX_SIDE:
        raise ValueError(
            "entry.png is %dx%d; sides must be at most %d"
            % (width, height, MAX_SIDE)
        )

    print("wrote %s (%dx%d) %d bytes" % (target, width, height, size))
    return 0


if __name__ == "__main__":
    sys.exit(main())
