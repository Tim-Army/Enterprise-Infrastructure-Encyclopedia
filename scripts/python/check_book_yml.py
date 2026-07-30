#!/usr/bin/env python3
"""Check book.yml against the volumes/ tree on disk.

book.yml is documentation: nothing in the build reads it, so it can silently
drift out of date as volumes and chapters are added. This script makes it
self-enforcing by comparing every declaration against the filesystem.

Checked, in both directions:

* every directory under volumes/ is declared, and every declared slug exists
* declared chapter_count == chapter entries listed == chapter files on disk
* every declared chapter path exists, and every chapter file on disk is listed
* each volume's id matches the number in its slug
* each volume's number and title match the "# Volume <Roman> — <Title>"
  heading in its README

Exits 0 when the manifest matches the tree, 1 otherwise, printing one
"BOOK.YML <CLASS>:" line per problem in the style of validate.sh.
"""

from __future__ import annotations

import os
import re
import sys

BOOK = "book.yml"
VOLUMES = "volumes"


def load_volumes(path):
    """Return book.yml's volume list as dicts.

    Prefers PyYAML; falls back to a strict parser for the generated layout so
    the check still runs on a host without PyYAML installed. The fallback
    raises rather than guessing if it meets a line it does not recognize.
    """
    try:
        import yaml  # optional dependency, deliberately probed at runtime
    except ImportError:
        return _parse_generated(path)
    with open(path, encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    return data.get("volumes") or []


def _parse_generated(path):
    """Parse the machine-generated subset of YAML that book.yml uses."""
    volumes = []
    volume = None
    chapter = None
    scalar = re.compile(r'^(\w+): (?:"(.*)"|(.*))$')
    with open(path, encoding="utf-8") as handle:
        for lineno, raw in enumerate(handle, 1):
            line = raw.rstrip("\n")
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            indent = len(line) - len(line.lstrip(" "))
            body = line.strip()
            if indent == 0:
                continue  # top-level title:/volumes: keys
            if indent == 2 and body.startswith("- id: "):
                volume = {"id": body[6:], "chapters": []}
                volumes.append(volume)
                chapter = None
                continue
            if volume is None:
                raise ValueError("%s:%d: field before any volume" % (path, lineno))
            if indent == 6 and body.startswith("- id: "):
                chapter = {"id": body[6:]}
                volume["chapters"].append(chapter)
                continue
            if re.match(r"^\w+:$", body):
                continue  # key opening a nested block, e.g. "chapters:"
            match = scalar.match(body)
            if not match:
                raise ValueError("%s:%d: unparsed line %r" % (path, lineno, body))
            key = match.group(1)
            value = match.group(2) if match.group(2) is not None else match.group(3)
            if indent == 4:
                volume[key] = value
                chapter = None
            elif indent == 8:
                if chapter is None:
                    raise ValueError("%s:%d: chapter field before entry" % (path, lineno))
                chapter[key] = value
            else:
                raise ValueError("%s:%d: unexpected indent %d" % (path, lineno, indent))
    for entry in volumes:
        if "chapter_count" in entry:
            entry["chapter_count"] = int(entry["chapter_count"])
    return volumes


def readme_heading(slug):
    """Return (roman, title) from a volume README's H1, or (None, None)."""
    path = os.path.join(VOLUMES, slug, "README.md")
    if not os.path.isfile(path):
        return None, None
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            if line.startswith("# "):
                match = re.match(r"Volume\s+([A-Z]+)\s+—\s+(.+)$", line[2:].strip())
                return match.groups() if match else (None, None)
    return None, None


def chapters_on_disk(slug):
    directory = os.path.join(VOLUMES, slug, "chapters")
    if not os.path.isdir(directory):
        return []
    return sorted(name for name in os.listdir(directory) if name.endswith(".md"))


def main():
    problems = []

    def report(kind, message):
        problems.append("BOOK.YML %s: %s" % (kind, message))

    try:
        declared = load_volumes(BOOK)
    except (OSError, ValueError) as error:
        print("BOOK.YML UNREADABLE: %s" % error)
        return 1

    on_disk = sorted(
        name
        for name in os.listdir(VOLUMES)
        if os.path.isdir(os.path.join(VOLUMES, name)) and not name.startswith(".")
    )
    slugs = [entry.get("slug", "") for entry in declared]

    for name in on_disk:
        if name not in slugs:
            report("UNDECLARED", "%s/%s is on disk but not in book.yml" % (VOLUMES, name))
    for slug in slugs:
        if slug and slug not in on_disk:
            report("MISSING DIR", "%s is declared but not under %s/" % (slug, VOLUMES))

    seen = set()
    for entry in declared:
        slug = entry.get("slug", "")
        if not slug:
            report("NO SLUG", "volume entry %r has no slug" % entry.get("id", "?"))
            continue
        if slug in seen:
            report("DUPLICATE", "%s is declared more than once" % slug)
            continue
        seen.add(slug)
        if slug not in on_disk:
            continue

        match = re.match(r"volume-(\d+)-", slug)
        if not match:
            report("SLUG SHAPE", "%s does not match volume-<digits>-<name>" % slug)
        else:
            expected_id = "volume-%s" % match.group(1)
            if entry.get("id") != expected_id:
                report(
                    "ID",
                    "%s declares id %r (expected %r)"
                    % (slug, entry.get("id"), expected_id),
                )

        disk = chapters_on_disk(slug)
        listed = entry.get("chapters") or []
        count = entry.get("chapter_count")
        if count != len(disk):
            report(
                "COUNT",
                "%s declares chapter_count %r but %d chapter file(s) on disk"
                % (slug, count, len(disk)),
            )
        if len(listed) != len(disk):
            report(
                "CHAPTER LIST",
                "%s lists %d chapter entr(ies) but %d file(s) on disk"
                % (slug, len(listed), len(disk)),
            )

        prefix = "%s/%s/chapters/" % (VOLUMES, slug)
        listed_names = []
        for chapter in listed:
            path = chapter.get("path", "")
            if not path:
                report("NO PATH", "%s has a chapter entry with no path" % slug)
                continue
            if not os.path.isfile(path):
                report("PATH", "%s is declared but does not exist" % path)
            if not path.startswith(prefix):
                report("PATH SHAPE", "%s is not under %s" % (path, prefix))
            else:
                listed_names.append(path[len(prefix) :])
            if not (chapter.get("title") or "").strip():
                report("CHAPTER TITLE", "%s has an empty title" % (path or slug))

        for name in disk:
            if name not in listed_names:
                report("UNLISTED", "%s%s is on disk but not listed" % (prefix, name))

        roman, title = readme_heading(slug)
        if roman is None:
            report("README HEADING", "%s/%s/README.md has no parsable H1" % (VOLUMES, slug))
        else:
            if entry.get("number") != roman:
                report(
                    "NUMBER",
                    "%s declares number %r but README says %r"
                    % (slug, entry.get("number"), roman),
                )
            if entry.get("title") != title:
                report(
                    "TITLE",
                    "%s declares title %r but README says %r"
                    % (slug, entry.get("title"), title),
                )

    if problems:
        for problem in problems:
            print(problem)
        return 1

    total = sum(len(entry.get("chapters") or []) for entry in declared)
    print(
        "book.yml: OK — %d volume(s), %d chapter(s) match the tree on disk"
        % (len(declared), total)
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
