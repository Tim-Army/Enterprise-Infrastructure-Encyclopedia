#!/usr/bin/env python3
"""Insert a lab topology/flow diagram image + figure caption right after
a chapter's H1 title, matching the pattern established in Volume V
Chapter 10. Idempotent: if the chapter already has an image reference to
the given diagram path, it does nothing (safe to re-run).

Usage: insert_diagram.py <chapter.md> <diagram-relative-path> <alt-text> <caption-text>
"""
import sys


def main():
    chapter_path, diagram_path, alt_text, caption = sys.argv[1:5]
    with open(chapter_path, encoding="utf-8") as f:
        text = f.read()

    if diagram_path in text:
        print(f"skip (already present): {chapter_path}")
        return

    lines = text.split("\n", 1)
    if not lines[0].startswith("# "):
        print(f"ERROR: {chapter_path} does not start with an H1 title", file=sys.stderr)
        sys.exit(1)

    title_line, rest = lines[0], lines[1] if len(lines) > 1 else ""
    block = f"{title_line}\n\n![{alt_text}]({diagram_path})\n\n*{caption}*\n"
    new_text = block + rest
    with open(chapter_path, "w", encoding="utf-8") as f:
        f.write(new_text)
    print(f"inserted: {chapter_path}")


if __name__ == "__main__":
    main()
