#!/usr/bin/env python3
"""Transform a chapter or volume-README Markdown file for the SINGLE-PAGE
whole-volume HTML edition (output/html/<vol>/Enterprise-Infrastructure-Encyclopedia.html), in
which every chapter and the README are concatenated onto ONE page.

Two transforms, so that every cross-reference resolves to an in-page anchor
instead of a (no-longer-generated) per-chapter .html file:

1. NAMESPACE HEADING IDS. On a concatenated page Pandoc would suffix
   duplicate ids globally (the 6th "Hands-On Lab" becomes #hands-on-lab-5),
   so a cross-chapter #fragment link cannot be resolved deterministically.
   Instead we give every heading an EXPLICIT namespaced id Pandoc will use
   verbatim: chapter NN's title heading becomes {#cNN}, its other headings
   {#cNN-<pandoc-slug>} (deduped within the chapter exactly as Pandoc does
   per file); the volume README's headings become {#readme} / {#readme-...}.
   <pandoc-slug> is computed by lib/pandoc_slug.py, validated to reproduce
   Pandoc's ids exactly (0 mismatches over 24k headings).

2. REWRITE LINKS to those anchors:
     same-volume  [x](MM-slug.md#frag)        -> #cMM-frag   ( #cMM if no frag )
     same-volume  [x](README.md#frag)         -> #readme-frag ( # if no frag )
     other-volume [x](../<vol>/chapters/MM-slug.md#frag)
                                               -> ../<vol>/Enterprise-Infrastructure-Encyclopedia.html#cMM-frag
     other-volume [x](../<vol>/README.md#frag) -> ../<vol>/Enterprise-Infrastructure-Encyclopedia.html#readme-frag
   publishing/web.css & theme-toggle -> GitHub source (as elsewhere).
   Anything else is left as written.

Usage: singlepage_rewrite.py <source-file> <current-volume-slug>
Prints the transformed Markdown to stdout.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pandoc_slug import pandoc_slug  # noqa: E402

GITHUB_BLOB_BASE = "https://github.com/Tim-Army/Enterprise-Infrastructure-Encyclopedia/blob/main"
COMBINED = "Enterprise-Infrastructure-Encyclopedia.html"

LINK_RE = re.compile(r"\]\(([^)\s]+\.(?:md|css|html))((?:#[^)]*)?)\)")
PURE_FRAG_RE = re.compile(r"\]\(#([^)\s#]+)\)")  # ](#frag): same-file heading link
CHAPTER_RE = re.compile(r"^volumes/([^/]+)/chapters/(\d+)-[^/]*\.md$")
README_RE = re.compile(r"^volumes/([^/]+)/README\.md$")
PUBLISHING_ASSETS = {"publishing/web.css", "publishing/theme-toggle.html"}
HEADING_RE = re.compile(r"^(#{1,6})[ \t]+(.*?)[ \t]*$")


def md_stringify(text: str) -> str:
    """Approximate Pandoc's stringify of inline heading markup, so the slug
    matches: [text](url)/[text][ref] -> text, drop code ticks and * emphasis.
    The pandoc_slug filter already drops stray * and ` (non-alnum), so this
    only has to strip the *URL* out of links."""
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\[([^\]]*)\]\[[^\]]*\]", r"\1", text)
    return text


def namespace_for(source_file: str):
    resolved = os.path.normpath(source_file)
    m = CHAPTER_RE.match(resolved)
    if m:
        return f"c{m.group(2)}"
    if README_RE.match(resolved):
        return "readme"
    return None


def inject_heading_ids(content: str, ns: str) -> str:
    """First heading -> {#ns}; each later heading -> {#ns-<slug>} with the
    same per-file duplicate suffixing Pandoc applies."""
    out = []
    seen = {}
    first = True
    for line in content.split("\n"):
        m = HEADING_RE.match(line)
        if not m:
            out.append(line)
            continue
        hashes, text = m.group(1), m.group(2)
        # respect an already-explicit {#id}; strip it and re-derive from text
        text = re.sub(r"\s*\{#[^}]*\}\s*$", "", text)
        if first:
            new_id = ns
            first = False
        else:
            slug = pandoc_slug(md_stringify(text))
            n = seen.get(slug, 0)
            seen[slug] = n + 1
            new_id = f"{ns}-{slug}" if n == 0 else f"{ns}-{slug}-{n}"
        out.append(f"{hashes} {text} {{#{new_id}}}")
    return "\n".join(out)


def rewrite_pure_fragments(content: str, ns: str) -> str:
    """A same-file heading link written as ](#frag) targets a heading whose id
    is now namespaced to #ns-frag on the combined page. Run BEFORE rewrite_links
    so it only sees the source's bare fragments, never the #cNN-... anchors that
    rewrite_links produces from .md links."""
    return PURE_FRAG_RE.sub(lambda m: f"](#{ns}-{m.group(1)})", content)


def rewrite_links(content: str, source_file: str, current_volume: str) -> str:
    source_dir = os.path.dirname(source_file)

    def resolve(target_path):
        return os.path.normpath(os.path.join(source_dir, target_path))

    def replace(m):
        target_path, fragment = m.group(1), m.group(2)
        resolved = resolve(target_path)
        if resolved in PUBLISHING_ASSETS:
            return f"]({GITHUB_BLOB_BASE}/{resolved}{fragment})"
        frag = fragment[1:] if fragment.startswith("#") else ""
        cm = CHAPTER_RE.match(resolved)
        if cm:
            vol, num = cm.group(1), cm.group(2)
            anchor = f"c{num}-{frag}" if frag else f"c{num}"
            if vol == current_volume:
                return f"](#{anchor})"
            return f"](../{vol}/{COMBINED}#{anchor})"
        rm = README_RE.match(resolved)
        if rm:
            vol = rm.group(1)
            if vol == current_volume:
                return f"](#readme-{frag})" if frag else "](#)"
            tail = f"#readme-{frag}" if frag else ""
            return f"](../{vol}/{COMBINED}{tail})"
        return m.group(0)

    return LINK_RE.sub(replace, content)


def main():
    source_file = sys.argv[1]
    current_volume = sys.argv[2] if len(sys.argv) > 2 else ""
    with open(source_file, encoding="utf-8") as fh:
        content = fh.read()
    ns = namespace_for(source_file)
    if ns is not None:
        content = inject_heading_ids(content, ns)
        content = rewrite_pure_fragments(content, ns)
    content = rewrite_links(content, source_file, current_volume)
    sys.stdout.write(content)


if __name__ == "__main__":
    main()
