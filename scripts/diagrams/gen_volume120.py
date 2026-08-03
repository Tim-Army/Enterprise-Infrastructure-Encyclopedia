#!/usr/bin/env python3
"""Volume CXX (NVIDIA BlueField Build-It-Yourself Lab) topology.

Chapter 1: each protected workload sits behind its own BlueField DPU, which
enforces segmentation at the NIC in an isolated trust domain the host CPU
cannot tamper with. DPU-web permits web->db:5432; DPU-hmi permits hmi->plc:502;
everything else is denied at the workload's own DPU, and a compromised host
cannot alter the DPU policy.

Run from scripts/diagrams:  python3 gen_volume120.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-120-nvidia-bluefield-lab"


def ch01():
    c = Canvas(960, 470,
        title="Chapter 1 Lab Topology: Per-Server DPU Microsegmentation with NVIDIA BlueField",
        subtitle="Each workload sits behind its own BlueField DPU, which enforces policy at the NIC in an isolated trust domain the host cannot tamper with; the segmentation survives host compromise",
        svg_title="Chapter 1 lab topology: NVIDIA BlueField DPUs enforcing per-workload segmentation out-of-band of the host",
        svg_desc="Each protected workload sits behind its own NVIDIA BlueField DPU on the server's network adapter, "
                 "which enforces segmentation at the NIC on its own Arm cores in a trust domain isolated from the "
                 "host CPU. The web workload is behind DPU-web, whose policy permits only web to db on 5432; the hmi "
                 "workload is behind DPU-hmi, whose policy permits only hmi to plc on 502. The db and plc targets sit "
                 "on the network. Every other flow, such as web to plc and hmi to db, is denied at the workload's own "
                 "DPU. Because the DPU is a separate computer from the host, a fully compromised host with root "
                 "cannot see, disable, or alter the DPU policy, so the segmentation survives host compromise. The "
                 "volume is design-leaning two-track: Track 1 describes BlueField and DOCA, Track 2 reproduces the "
                 "out-of-band property with Linux namespaces and nftables.")

    c.node_box(300, 42, 320, 42, "mgmt", [
        Line("DOCA / management", 11, 700, "#111827"),
        Line("per-server DPU policy (out-of-band)", 9, 400, "#374151"),
    ])

    def row(y, wl, wl_sub, dpu_pol, tgt, tgt_sub, port):
        c.node_box(45, y, 110, 52, "neutral", [Line(wl, 11, 700, "#111827"), Line(wl_sub, 8.5, 400, "#374151")])
        c.node_box(230, y - 4, 200, 60, "alt", [Line("BlueField DPU (isolated)", 9.5, 700, "#111827"),
                                                Line(dpu_pol, 9, 700, "#166534")])
        c.node_box(560, y, 120, 52, "data", [Line(tgt, 10.5, 700, "#111827"), Line(tgt_sub, 8.5, 400, "#374151")])
        c.connector(155, y + 26, 230, y + 26, "neutral", label="", label_pos=(0, 0))
        c.connector(430, y + 26, 560, y + 26, "alt", label=port, label_pos=(455, y - 6))

    row(120, "web", "workload", "policy: web -> db", "db · :5432", "target", "5432 allow")
    row(250, "hmi", "workload", "policy: hmi -> plc", "plc · :502", "target", "502 allow")

    c.raw('<text x="45" y="345" font-size="9.5" font-weight="700" fill="#b91c1c">'
          'web -&gt; plc and hmi -&gt; db are denied at the workload\'s own DPU</text>')

    # the out-of-band callout
    c.node_box(700, 110, 220, 96, "warn", [
        Line("Host compromise", 10, 700, "#111827"),
        Line("cannot see or change", 9, 400, "#7f1d1d"),
        Line("the DPU policy —", 9, 400, "#7f1d1d"),
        Line("enforcement survives", 9, 400, "#7f1d1d"),
        Line("root on the host", 9, 700, "#7f1d1d"),
    ])

    c.legend(45, 400, [
        ("alt", "Permitted by the DPU policy"),
        ("warn", "Out-of-band (host cannot tamper)"),
        ("mgmt", "DOCA / management"),
    ])
    c.save(f"{OUT}/chapter-01-lab-topology.svg")


if __name__ == "__main__":
    ch01()
