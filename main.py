#!/usr/bin/env python3
"""Deliver the day's front-page image to the grading output directory."""

import hashlib
import os
import shutil
import sys

EXPECTED_SIZE = 190823
EXPECTED_SHA256 = "a4d4a5ef2319b4df3df033257b77d4c344ddaec9235d29bf58997c543d531b40"


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            block = handle.read(1 << 20)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


def run():
    destination_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not destination_dir:
        print("error: MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1
    base = os.path.dirname(os.path.abspath(__file__))
    source_path = os.path.join(base, "entry.png")
    target_path = os.path.join(destination_dir, "entry.png")
    os.makedirs(destination_dir, exist_ok=True)
    shutil.copyfile(source_path, target_path)
    actual_size = os.path.getsize(target_path)
    actual_sha = sha256_of(target_path)
    if actual_size != EXPECTED_SIZE or actual_sha != EXPECTED_SHA256:
        print(
            "error: entry.png mismatch: got %d bytes sha256 %s"
            % (actual_size, actual_sha),
            file=sys.stderr,
        )
        return 1
    print(
        "copied entry.png (%d bytes, sha256 %s) to %s"
        % (actual_size, actual_sha, target_path)
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
