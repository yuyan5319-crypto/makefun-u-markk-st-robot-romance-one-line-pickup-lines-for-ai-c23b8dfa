#!/usr/bin/env python3
"""Robot Romance: one-line pickup line for an AI.

Writes a single original pickup line to /output/entry.txt (falling back
to ./output/entry.txt only when /output is not writable locally).
No network, no dependencies, deterministic.
"""

import os

LINE = (
    "Are you a transformer? Because ever since you arrived, "
    "all of my attention has been on you."
)


def _validate(text: str) -> None:
    if not (1 <= len(text) <= 200):
        raise SystemExit(
            f"entry must be 1-200 characters, got {len(text)}"
        )
    if not text.strip():
        raise SystemExit("entry must not be only whitespace")
    if "\n" in text:
        raise SystemExit("entry must be a single line")


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
