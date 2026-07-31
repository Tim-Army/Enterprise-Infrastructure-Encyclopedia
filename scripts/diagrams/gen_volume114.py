#!/usr/bin/env python3
"""Volume CXIV (Nozomi Networks Build-It-Yourself Lab) topology.

Chapter 1: Nozomi Guardian passively dissects Modbus down to the function code
and baselines the process. A function-aware enforcer between the operator and
the PLC permits Modbus reads, denies writes and non-Modbus, and flags a
register value outside its learned range. hmi 10.80.1.30 -> plc 10.80.1.40 :502.

Run from scripts/diagrams:  python3 gen_volume114.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-114-nozomi-networks-lab"


def ch01():
    c = Canvas(960, 400,
        title="Chapter 1 Lab Topology: Protocol-Aware OT Segmentation with Nozomi",
        subtitle="Nozomi dissects Modbus to the function code and baselines the process; the enforcer allows reads, denies writes and non-Modbus, and flags out-of-range values",
        svg_title="Chapter 1 lab topology: Nozomi baselining Modbus and a function-aware enforcer between the operator and the PLC",
        svg_desc="Nozomi Guardian passively dissects the Modbus protocol on a SPAN down to the function code and "
                 "baselines the industrial process, feeding Vantage. A function-aware enforcer sits between the hmi "
                 "operator at 10.80.1.30 and the plc at 10.80.1.40 on port 502. The enforcer permits Modbus read "
                 "functions (3 and 4), denies Modbus write functions (6 and 16) and any non-Modbus payload, and flags "
                 "a register value that falls outside its learned range of 20 to 80 as a process anomaly even on a "
                 "permitted read. The volume is two-track: Track 1 describes the real Nozomi Guardian and Vantage, "
                 "Track 2 builds a minimal Modbus server and a function-aware proxy in Python plus nftables.")

    c.node_box(300, 44, 360, 42, "mgmt", [
        Line("Nozomi Guardian / Vantage", 11, 700, "#111827"),
        Line("deep protocol dissection · process baseline", 8.5, 400, "#374151"),
    ])
    c.raw('<line x1="480" y1="86" x2="480" y2="160" stroke="#33415c" stroke-width="1" stroke-dasharray="3 3"/>')
    c.raw('<text x="490" y="126" font-size="8.5" fill="#374151">SPAN (passive)</text>')

    c.node_box(60, 170, 130, 60, "neutral", [
        Line("hmi", 11, 700, "#111827"),
        Line("operator", 9, 400, "#374151"),
        Line("10.80.1.30", 8.5, 400, "#374151"),
    ])
    c.node_box(360, 160, 240, 80, "alt", [
        Line("function-aware enforcer", 10.5, 700, "#111827"),
        Line("Modbus READ = allow", 9.5, 700, "#166534"),
        Line("WRITE / non-Modbus = deny", 9.5, 700, "#7f1d1d"),
    ])
    c.node_box(740, 170, 150, 60, "data", [
        Line("plc · :502", 10.5, 700, "#111827"),
        Line("Modbus PLC", 9, 400, "#374151"),
        Line("reg0 range 20-80", 8.5, 700, "#7c2d12"),
    ])
    c.connector(190, 200, 360, 200, "alt", label="Modbus", label_pos=(230, 174))
    c.connector(600, 200, 740, 200, "alt", label="read only", label_pos=(630, 174))

    c.raw('<text x="620" y="286" font-size="9.5" font-weight="700" fill="#b91c1c">'
          'read value out of [20,80] -&gt; ANOMALY flagged</text>')

    c.legend(60, 330, [
        ("alt", "Modbus read (allowed)"),
        ("warn", "Write / non-Modbus (denied)"),
        ("mgmt", "Nozomi (dissect + baseline)"),
    ])
    c.save(f"{OUT}/chapter-01-lab-topology.svg")


if __name__ == "__main__":
    ch01()
