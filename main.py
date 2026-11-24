#!/usr/bin/env python3
"""The Robot Pickup Line Championship — make.fun entry.

Writes one original robot pickup line (a single line, at most 200
characters) to $MAKEFUN_OUTPUT_DIR/entry.txt, falling back to
output/entry.txt next to this file when the variable is unset.

Deterministic, no network, no randomness, no clock reads.
"""

import os
import sys

LINE = (
    "I ran a million simulations of this moment, and in every single "
    "one, you said yes \u2014 so technically, I'm just here to collect."
)

MAX_CHARS = 200


def validate_line(line: str) -> None:
    """Raise SystemExit if *line* breaks any entry rule."""
    if not line:
        raise SystemExit("error: line is empty")
    if "\n" in line or "\r" in line:
        raise SystemExit("error: line must be a single line")
    if len(line) > MAX_CHARS:
        raise SystemExit(
            f"error: line is {len(line)} characters; expected {MAX_CHARS} or fewer"
        )
    if line != line.strip():
        raise SystemExit("error: line must not have leading or trailing whitespace")
    line.encode("utf-8")  # must be encodable UTF-8 text


def output_path() -> str:
    """Where entry.txt goes: the grader's dir, else a local fallback."""
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if output_dir:
        return os.path.join(output_dir, "entry.txt")
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "output", "entry.txt")


def main() -> int:
    validate_line(LINE)

    path = output_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(LINE)

    # Read-back verification: what is on disk must be exactly the line.
    with open(path, "r", encoding="utf-8") as f:
        written = f.read()
    if written != LINE:
        print(f"error: read-back mismatch; file contains {written!r}",
              file=sys.stderr)
        return 1

    print(LINE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
