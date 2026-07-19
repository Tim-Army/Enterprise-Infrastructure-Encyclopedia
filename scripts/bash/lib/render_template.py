#!/usr/bin/env python3
"""Substitute {{TOKEN}} placeholders in a publishing template.

Used for the encyclopedia and per-volume title pages. Substitution happens
here rather than through sed because volume titles are arbitrary prose --
they contain em dashes, dots and version numbers, and could later contain
characters sed would treat as delimiters or backreferences.

Usage: render_template.py <template.md> TOKEN=value [TOKEN=value ...]
Prints the rendered document to stdout.
"""
import sys


def main():
    if len(sys.argv) < 2:
        print("usage: render_template.py <template.md> TOKEN=value ...",
              file=sys.stderr)
        sys.exit(2)

    with open(sys.argv[1], encoding="utf-8") as handle:
        text = handle.read()

    for pair in sys.argv[2:]:
        if "=" not in pair:
            print(f"render_template.py: expected TOKEN=value, got {pair!r}",
                  file=sys.stderr)
            sys.exit(2)
        token, value = pair.split("=", 1)
        text = text.replace("{{" + token + "}}", value)

    sys.stdout.write(text)


if __name__ == "__main__":
    main()
