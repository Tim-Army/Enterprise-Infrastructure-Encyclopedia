#!/usr/bin/env python3
"""Shared SVG toolkit for the encyclopedia's lab topology diagrams.

Establishes one consistent visual language (colors, fonts, arrow styles,
legend) across every chapter's diagram, matching the style first used in
Volume V Chapter 10 (NSX installation lab topology), while leaving actual
topology layout -- which nodes exist, how they're grouped, what they're
labeled -- to each chapter's own script, since lab shapes vary enormously
across the encyclopedia (a single-host Wireshark capture lab looks
nothing like a multi-AZ AWS VPC lab or a Palo Alto firewall lab).

Two plane colors are built in and reused everywhere they fit: "mgmt"
(navy, solid connectors) for management/control-plane traffic, and
"data" (amber, dashed connectors) for the primary data/traffic plane
under study. A third neutral gray is available for anything that's
neither (a plain informational box). Chapters whose lab genuinely needs
a third distinct plane (for example a security-zone diagram with
Trust/Untrust/DMZ) can call plane_bar()/connector() with an explicit
color pair instead of the "mgmt"/"data" shorthand.

Usage pattern (see any generate_*.py script under scripts/diagrams/ for
a full example):

    from labtopo import Canvas

    c = Canvas(960, 660, title="...", subtitle="...",
               svg_title="...", svg_desc="...")
    c.plane_bar(60, 80, 840, 34, "mgmt", "Management Network — 10.0.0.0/24")
    c.node_box(380, 150, 200, 120, "mgmt", [
        Line("NSX Manager", size=15, weight=700, color="#111827"),
        Line("10.0.0.11", size=11.5, weight=700, color=c.colors["mgmt"]["accent"]),
    ])
    c.connector(440, 150, 270, 114, "mgmt")
    c.legend(60, 646)
    c.save("../../diagrams/.../foo.svg")
"""
from dataclasses import dataclass, field
from typing import Optional

PALETTES = {
    "mgmt": {
        "fill": "#eaf2ff", "stroke": "#1d4ed8", "text": "#111827",
        "accent": "#1d4ed8", "line": "#33415c", "dash": None,
        "bar_fill": "#eef2f8", "bar_stroke": "#33415c", "bar_text": "#1f2937",
    },
    "data": {
        "fill": "#fff7ed", "stroke": "#b45309", "text": "#111827",
        "accent": "#7c2d12", "line": "#b45309", "dash": "7 4",
        "bar_fill": "#fff7ed", "bar_stroke": "#b45309", "bar_text": "#7c2d12",
    },
    "alt": {
        "fill": "#f0faf2", "stroke": "#166534", "text": "#111827",
        "accent": "#166534", "line": "#166534", "dash": None,
        "bar_fill": "#f0faf2", "bar_stroke": "#166534", "bar_text": "#14532d",
    },
    "warn": {
        "fill": "#fef2f2", "stroke": "#b91c1c", "text": "#111827",
        "accent": "#b91c1c", "line": "#b91c1c", "dash": "3 3",
        "bar_fill": "#fef2f2", "bar_stroke": "#b91c1c", "bar_text": "#7f1d1d",
    },
    "neutral": {
        "fill": "#f4f7fb", "stroke": "#33415c", "text": "#111827",
        "accent": "#374151", "line": "#6b7280", "dash": "4 3",
        "bar_fill": "#f4f7fb", "bar_stroke": "#6b7280", "bar_text": "#374151",
    },
}


@dataclass
class Line:
    text: str
    size: float = 11
    weight: int = 400
    color: str = "#1f2937"
    dy: Optional[float] = None  # override auto line spacing if set


def esc(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


class Canvas:
    def __init__(self, width, height, title, subtitle, svg_title, svg_desc,
                 title_y=30, subtitle_y=50):
        self.w, self.h = width, height
        self.colors = PALETTES
        self._markers_used = set()
        self.body = []
        self.body.append(f'<rect x="0" y="0" width="{width}" height="{height}" fill="#ffffff"/>')
        self.body.append(f'<text x="{width/2}" y="{title_y}" text-anchor="middle" '
                          f'font-size="20" font-weight="700" fill="#111827">{esc(title)}</text>')
        if subtitle:
            self.body.append(f'<text x="{width/2}" y="{subtitle_y}" text-anchor="middle" '
                              f'font-size="13" fill="#4b5563">{esc(subtitle)}</text>')
        self.svg_title = svg_title
        self.svg_desc = svg_desc

    def _marker(self, plane):
        name = f"arrow-{plane}"
        if name not in self._markers_used:
            self._markers_used.add(name)
        return name

    def plane_bar(self, x, y, w, h, plane, label, sub_label=None):
        pal = self.colors[plane] if isinstance(plane, str) else plane
        dash_attr = f' stroke-dasharray="{pal["dash"]}"' if pal.get("dash") else ""
        self.body.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" '
            f'fill="{pal["bar_fill"]}" stroke="{pal["bar_stroke"]}" stroke-width="1.5"{dash_attr}/>'
        )
        cx = x + w / 2
        if sub_label:
            self.body.append(f'<text x="{cx}" y="{y + h/2 - 3}" text-anchor="middle" '
                              f'font-size="14" font-weight="700" fill="{pal["bar_text"]}">{esc(label)}</text>')
            self.body.append(f'<text x="{cx}" y="{y + h/2 + 14}" text-anchor="middle" '
                              f'font-size="11" fill="{pal["bar_text"]}">{esc(sub_label)}</text>')
        else:
            self.body.append(f'<text x="{cx}" y="{y + h/2 + 5}" text-anchor="middle" '
                              f'font-size="14" font-weight="600" fill="{pal["bar_text"]}">{esc(label)}</text>')
        return (x, y, w, h)

    def node_box(self, x, y, w, h, plane, lines: list, dashed=False, rx=8):
        pal = self.colors[plane] if isinstance(plane, str) else plane
        dash_attr = f' stroke-dasharray="4 3"' if dashed else ""
        self.body.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
            f'fill="{pal["fill"]}" stroke="{pal["stroke"]}" stroke-width="{1.25 if dashed else 2}"{dash_attr}/>'
        )
        cx = x + w / 2
        n = len(lines)
        step = min(18, max(13, (h - 16) / max(n, 1)))
        start = y + (h - step * (n - 1)) / 2 + (lines[0].size * 0.35 if n else 0)
        for i, ln in enumerate(lines):
            ty = ln.dy if ln.dy is not None else start + i * step
            self.body.append(
                f'<text x="{cx}" y="{ty:.1f}" text-anchor="middle" font-size="{ln.size}" '
                f'font-weight="{ln.weight}" fill="{ln.color}">{esc(ln.text)}</text>'
            )
        return (x, y, w, h)

    def divider(self, x1, y, x2, color="#93a3b8"):
        self.body.append(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{color}" stroke-width="1"/>')

    def connector(self, x1, y1, x2, y2, plane, width=1.75, label=None, label_pos=None):
        pal = self.colors[plane] if isinstance(plane, str) else plane
        marker = self._marker(plane if isinstance(plane, str) else "custom")
        dash_attr = f' stroke-dasharray="{pal["dash"]}"' if pal.get("dash") else ""
        w = width if not pal.get("dash") else max(width, 2)
        self.body.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{pal["line"]}" '
            f'stroke-width="{w}"{dash_attr} marker-end="url(#{marker})"/>'
        )
        self._marker_colors = getattr(self, "_marker_colors", {})
        self._marker_colors[marker] = pal["line"]
        if label:
            lx, ly = label_pos if label_pos else ((x1 + x2) / 2 + 6, (y1 + y2) / 2)
            self.body.append(f'<text x="{lx}" y="{ly}" font-size="10.5" fill="{pal["line"]}">{esc(label)}</text>')

    def text(self, x, y, s, size=11, weight=400, color="#1f2937", anchor="middle"):
        self.body.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" '
                          f'font-weight="{weight}" fill="{color}">{esc(s)}</text>')

    def legend(self, x, y, entries=None):
        if entries is None:
            entries = [("mgmt", "Management-plane connection"), ("data", "Data-plane connection")]
        cx = x
        for plane, label in entries:
            pal = self.colors[plane] if isinstance(plane, str) else plane
            marker = self._marker(plane if isinstance(plane, str) else "custom")
            dash_attr = f' stroke-dasharray="{pal["dash"]}"' if pal.get("dash") else ""
            w = 1.75 if not pal.get("dash") else 2
            self.body.append(
                f'<line x1="{cx}" y1="{y}" x2="{cx+40}" y2="{y}" stroke="{pal["line"]}" '
                f'stroke-width="{w}"{dash_attr} marker-end="url(#{marker})"/>'
            )
            self._marker_colors = getattr(self, "_marker_colors", {})
            self._marker_colors[marker] = pal["line"]
            self.body.append(f'<text x="{cx+48}" y="{y+4}" font-size="11" fill="{pal["line"]}">{esc(label)}</text>')
            cx += 48 + 9 * len(label) + 30

    def raw(self, svg_fragment: str):
        """Escape hatch for anything the toolkit doesn't model directly."""
        self.body.append(svg_fragment)

    def render(self) -> str:
        defs = ['  <defs>']
        marker_colors = getattr(self, "_marker_colors", {})
        for marker, color in sorted(marker_colors.items()):
            defs.append(
                f'    <marker id="{marker}" viewBox="0 0 10 10" refX="9" refY="5" '
                f'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
                f'<path d="M0,0 L10,5 L0,10 z" fill="{color}"/></marker>'
            )
        defs.append('  </defs>')
        parts = [
            f'<svg viewBox="0 0 {self.w} {self.h}" xmlns="http://www.w3.org/2000/svg" '
            f'font-family="Helvetica, Arial, sans-serif">',
            f'  <title>{esc(self.svg_title)}</title>',
            f'  <desc>\n    {esc(self.svg_desc)}\n  </desc>',
            *defs,
            *("  " + b for b in self.body),
            '</svg>',
        ]
        return "\n".join(parts) + "\n"

    def save(self, path: str):
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.render())
        print(f"wrote {path}")
