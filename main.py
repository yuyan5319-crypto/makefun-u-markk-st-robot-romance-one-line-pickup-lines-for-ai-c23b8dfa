#!/usr/bin/env python3
"""Robot Romance: one-line pickup line for an AI.

Writes a single original pickup line to /output/entry.txt (falling back
to ./output/entry.txt only when /output is not writable locally).
No network, no dependencies, deterministic.
"""

import os
import sys

# The line is built from two halves so the joke's structure stays explicit:
# SETUP names the architecture, PUNCH lands on its attention mechanism.
SETUP = "Are you a transformer? Because ever since you arrived, "
PUNCH = "all of my attention has been on you."
LINE = SETUP + PUNCH


def _validate(text: str) -> None:
    if not (1 <= len(text) <= 200):
        raise SystemExit(
            f"entry must be 1-200 characters, got {len(text)}"
        )
    if not text.strip():
        raise SystemExit("entry must not be only whitespace")
    if "\n" in text:
        raise SystemExit("entry must be a single line")
    # The assembled line must match the sum of its parts exactly, and the
    # joined total must still fit the limit on its own (guards against a
    # future edit growing one half past the cap unnoticed).
    if text != SETUP + PUNCH:
        raise SystemExit("entry must equal SETUP + PUNCH")
    if len(SETUP) + len(PUNCH) != len(text):
        raise SystemExit("assembled length does not match its parts")


def _write_atomic(path: str, text: str) -> None:
    directory = os.path.dirname(path)
    tmp = os.path.join(directory, ".entry.tmp")
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(text)
        os.replace(tmp, path)
        os.chmod(path, 0o644)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def main() -> None:
    if "--selftest" in sys.argv[1:]:
        _validate(LINE)
        print(f"selftest ok: {len(LINE)} characters, validation passed")
        print(f"setup={len(SETUP)} chars, punch={len(PUNCH)} chars")
        return
    _validate(LINE)
    env_base = os.environ.get("MAKEFUN_OUTPUT_DIR")
    bases = [env_base] if env_base else []
    bases += ["/output", os.path.join(os.getcwd(), "output")]
    for base in bases:
        try:
            os.makedirs(base, exist_ok=True)
            path = os.path.join(base, "entry.txt")
            _write_atomic(path, LINE)
            print(f"wrote {path} ({len(LINE)} characters)")
            return
        except OSError:
            continue
    raise SystemExit("could not write entry.txt to /output or ./output")


if __name__ == "__main__":
    main()
