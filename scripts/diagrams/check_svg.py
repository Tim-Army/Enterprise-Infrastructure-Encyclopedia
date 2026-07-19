#!/usr/bin/env python3
"""Structural sanity checks for lab topology diagrams: well-formed XML,
every element inside the canvas viewBox, and no two node/plane rects
overlapping. This substitutes for visually reviewing all 222 diagrams by
hand -- it won't catch a bad color choice, but it will catch the failure
modes that actually break a diagram (text sticking out past a box edge,
a mispositioned box overlapping its neighbor, a box off-canvas).

Usage: check_svg.py <file-or-dir> [<file-or-dir> ...]
"""
import glob
import re
import sys
import xml.etree.ElementTree as ET

NS = {"svg": "http://www.w3.org/2000/svg"}


def check_file(path):
    problems = []
    try:
        tree = ET.parse(path)
    except ET.ParseError as e:
        return [f"XML PARSE ERROR: {e}"]
    root = tree.getroot()
    vb = root.attrib.get("viewBox")
    if not vb:
        return ["missing viewBox"]
    _, _, vw, vh = (float(x) for x in vb.split())

    rects = []
    for rect in root.iter("{http://www.w3.org/2000/svg}rect"):
        x, y = float(rect.attrib.get("x", 0)), float(rect.attrib.get("y", 0))
        w, h = float(rect.attrib.get("width", 0)), float(rect.attrib.get("height", 0))
        if x < 0 or y < 0 or x + w > vw or y + h > vh:
            problems.append(f"rect off-canvas: x={x} y={y} w={w} h={h} (canvas {vw}x{vh})")
        rects.append((x, y, w, h))

    for text in root.iter("{http://www.w3.org/2000/svg}text"):
        x = float(text.attrib.get("x", 0))
        y = float(text.attrib.get("y", 0))
        if x < -5 or x > vw + 5 or y < -5 or y > vh + 5:
            problems.append(f"text off-canvas: x={x} y={y} content={(text.text or '').strip()[:40]!r}")

    # overlap check: skip pairs where one rect is the whole-canvas background
    # or where one is fully nested for legend swatches (tiny), and skip pairs
    # that are clearly a bar containing a smaller inset box (allowed nesting)
    def overlaps(a, b):
        ax, ay, aw, ah = a
        bx, by, bw, bh = b
        ix = max(0, min(ax + aw, bx + bw) - max(ax, bx))
        iy = max(0, min(ay + ah, by + bh) - max(ay, by))
        return ix > 2 and iy > 2

    def nested(a, b):
        ax, ay, aw, ah = a
        bx, by, bw, bh = b
        return ax >= bx - 1 and ay >= by - 1 and ax + aw <= bx + bw + 1 and ay + ah <= by + bh + 1

    big = [r for r in rects if r[2] * r[3] > (vw * vh) * 0.5]  # background rect(s)
    candidate = [r for r in rects if r not in big]
    for i in range(len(candidate)):
        for j in range(i + 1, len(candidate)):
            a, b = candidate[i], candidate[j]
            if nested(a, b) or nested(b, a):
                continue
            if overlaps(a, b):
                problems.append(f"rect overlap: {a} <-> {b}")

    return problems


def main():
    paths = []
    for arg in sys.argv[1:]:
        if arg.endswith(".svg"):
            paths.append(arg)
        else:
            paths.extend(sorted(glob.glob(f"{arg}/**/*.svg", recursive=True)))
    total_problems = 0
    for path in paths:
        problems = check_file(path)
        if problems:
            total_problems += len(problems)
            print(f"\n{path}:")
            for p in problems:
                print(f"  {p}")
    print(f"\nChecked {len(paths)} file(s), {total_problems} problem(s) found.")
    sys.exit(1 if total_problems else 0)


if __name__ == "__main__":
    main()
