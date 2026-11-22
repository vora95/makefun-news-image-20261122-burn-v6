#!/usr/bin/env python3
"""THE BARRAGE LEAD — entrypoint.

Copies the sealed front page (entry.png, rendered deterministically from
the 22 November 2026 wires) into $MAKEFUN_OUTPUT_DIR and verifies the copy
byte-for-byte against the sealed SHA-256.
Standard library only.
"""
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
EXPECTED_SHA256 = "a4d4a5ef2319b4df3df033257b77d4c344ddaec9235d29bf58997c543d531b40"
EXPECTED_SIZE = 190823  # bytes of the sealed entry.png


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1
    # Fail fast if the sealed source itself is not the expected file.
    if os.path.getsize(SRC) != EXPECTED_SIZE or sha256_of(SRC) != EXPECTED_SHA256:
        print("sealed entry.png does not match its expected size/sha256",
              file=sys.stderr)
        return 2
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    # Read the copy back once; every check below works on these bytes.
    copied = open(dst, "rb").read()
    digest = hashlib.sha256(copied).hexdigest()
    if len(copied) != EXPECTED_SIZE or digest != EXPECTED_SHA256:
        print(f"copy mismatch: {len(copied)} bytes, sha256 {digest}",
              file=sys.stderr)
        return 1
    print(f"copied entry.png (190823 bytes, sha256 {digest}) to {dst}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
