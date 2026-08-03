#!/usr/bin/env python3
"""Check that every relative link in every Markdown file resolves on disk.

AUTOMATION.md promises that validate.sh verifies "internal links resolve",
but until this script existed nothing enforced it: markdownlint has no rule
that resolves link targets against the filesystem, and the Lychee run in
check-external-links.sh needs network access so it sits outside the default
gate. That gap let four classes of dangling links accumulate undetected:
wrong ../ depth written from chapter files, ../../ escapes from volume
READMEs, stale renamed volume slugs, and links that escape the repository
entirely.

For each Markdown file (excluding generated output and tool directories),
every inline `](target)` is resolved against the file's own directory after
stripping any #fragment and decoding percent-escapes. External targets (any
URL scheme), same-file #fragments, and links inside fenced code blocks or
inline code spans are ignored. A target that resolves outside the repository
is reported even if it happens to exist on the host.

Exits 0 when every link resolves, 1 otherwise, printing one
"LINK <CLASS>:" line per problem in the style of validate.sh.
"""

from __future__ import annotations

import os
import re
import sys
from urllib.parse import unquote

# Directory names never descended into: generated output, dependencies, and
# Claude Code worktrees (full repo checkouts that would double-count files).
PRUNE_DIRS = {
    ".git",
    ".claude",
    ".cache",
    ".venv",
    "__pycache__",
    "_site",
    "dist",
    "node_modules",
    "output",
}

# Links that are deliberately dangling in the repository tree because they
# are resolved against a different layout when the book is built.
EXEMPT = {
    # Pandoc reads title-page.md with the repo root as its cwd, so this
    # build-input image path resolves via the cwd, not the file's directory.
    ("publishing/title-page.md", "publishing/cover.png"),
    # The interactive catalog exists only in the built portal/zip layout,
    # where the volume pages sit beside an interactive/ directory.
    (
        "volumes/volume-997-master-appendices/chapters/"
        "01-appendix-cisco-u-learning-paths-and-continuing-education-credits.md",
        "../../interactive/cisco-u-learning-paths.html",
    ),
}

FENCE = re.compile(r"^\s{0,3}(?:```|~~~)")
CODE_SPAN = re.compile(r"`[^`]+`")
# Matches the `](target)` tail of a link or image; matching only the tail
# also catches the outer link of nested forms like [![badge](img)](url).
LINK_TARGET = re.compile(r"\]\(\s*<?([^()<>\s]+?)>?(?:\s+\"[^\"]*\")?\s*\)")
SCHEME = re.compile(r"[A-Za-z][A-Za-z0-9+.-]*:")


def markdown_files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in PRUNE_DIRS)
        for name in sorted(filenames):
            if name.endswith(".md"):
                yield os.path.relpath(os.path.join(dirpath, name), root)


def link_targets(path):
    """Yield (lineno, raw_target) for every inline link in a Markdown file."""
    in_fence = False
    with open(path, encoding="utf-8") as handle:
        for lineno, line in enumerate(handle, 1):
            if FENCE.match(line):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for match in LINK_TARGET.finditer(CODE_SPAN.sub(" ", line)):
                yield lineno, match.group(1)


def main():
    root = os.getcwd()
    problems = []
    files = 0
    checked = 0

    for relpath in markdown_files(root):
        files += 1
        base = os.path.dirname(relpath)
        for lineno, target in link_targets(os.path.join(root, relpath)):
            if SCHEME.match(target) or target.startswith("#"):
                continue
            if (relpath, target) in EXEMPT:
                continue
            checked += 1
            where = "%s:%d" % (relpath, lineno)
            if target.startswith("/"):
                problems.append(
                    "LINK ABSOLUTE: %s: %s must be a relative path" % (where, target)
                )
                continue
            resolved = os.path.normpath(os.path.join(base, unquote(target.split("#", 1)[0])))
            if resolved == ".." or resolved.startswith(".." + os.sep):
                problems.append(
                    "LINK ESCAPE: %s: %s points outside the repository" % (where, target)
                )
            elif not os.path.exists(os.path.join(root, resolved)):
                problems.append(
                    "LINK DANGLING: %s: %s -> %s does not exist" % (where, target, resolved)
                )

    if problems:
        for problem in problems:
            print(problem)
        return 1

    print(
        "internal links: OK — %d relative link(s) across %d Markdown file(s) resolve"
        % (checked, files)
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
