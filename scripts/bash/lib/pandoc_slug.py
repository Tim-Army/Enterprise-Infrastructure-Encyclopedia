#!/usr/bin/env python3
"""Pandoc-compatible auto-identifier (GFM/default). Mirrors Pandoc's
Text.Pandoc.Shared.inlineListToIdentifier:

    dropWhile (not . isAlpha)
    . intercalate "-" . words          -- split on whitespace runs, join single '-'
    . map toLower
    . filter (isAlphaNum || isSpace || c `elem` "_-.")
    . stringify

i.e. keep alnum/space/_-. (drop other punctuation such as em-dashes, parens,
colons), lowercase, then collapse whitespace runs into single hyphens, then
strip any leading non-letters. Duplicate ids within one document get -1, -2, …
suffixes (the caller tracks that).
"""
import sys


def pandoc_slug(text: str) -> str:
    s = "".join(c for c in text if c.isalnum() or c.isspace() or c in "_-.")
    s = s.lower()
    s = "-".join(s.split())            # words() collapses whitespace runs
    i = 0
    while i < len(s) and not s[i].isalpha():
        i += 1
    s = s[i:]
    return s or "section"


if __name__ == "__main__":
    for line in sys.stdin:
        print(pandoc_slug(line.rstrip("\n")))
