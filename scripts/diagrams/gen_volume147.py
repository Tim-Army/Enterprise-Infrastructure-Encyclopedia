#!/usr/bin/env python3
"""Volume CXLVII (Wiz) certified-program map.

Chapter 1: the Wiz Certified exam ladder (Cloud User / Cloud Fundamentals /
Defend Fundamentals) over the code-to-cloud-to-runtime platform (Wiz Code /
Wiz Cloud / Wiz Defend), all anchored on the Security Graph. Defend Fundamentals
mechanics are public (60Q/150min/2yr); the rest are portal-gated.

Run from scripts/diagrams:  python3 gen_volume147.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-147-wiz-certifications"


def ch01():
    c = Canvas(960, 600,
        title="Chapter 1 Program Map: Wiz Certification Tracks",
        subtitle="expanding exam ladder · code-to-cloud-to-runtime · Defend Fundamentals public · Security Graph beneath",
        svg_title="Chapter 1 program map: the Wiz Certified ladder over the code-to-cloud-to-runtime platform",
        svg_desc="The Wiz Certified program, launched February 2025, is an expanding portfolio of proctored "
                 "exams taken online or at an onsite test center and open to Wiz customers, partners, and "
                 "cloud security professionals. There are three current exams. Wiz Certified Cloud User is an "
                 "entry-level credential for day-to-day users of Wiz Cloud. Wiz Certified Cloud Fundamentals, "
                 "the first exam, validates deployment and management of Wiz Cloud and is the prerequisite "
                 "keystone for future specialized exams. Wiz Certified Defend Fundamentals validates cloud "
                 "threat detection and response with Wiz Defend for SOC, incident response, IT, and developer "
                 "roles; it is public at sixty multiple-choice questions in one hundred fifty minutes, a "
                 "two-year certification, and a shareable badge. Training is free through the CloudSec "
                 "Academy. The platform beneath spans three pillars in a code-to-cloud-to-runtime story. Wiz "
                 "Code is the shift-left pillar for securing code, infrastructure as code, and secrets before "
                 "deployment. Wiz Cloud is the cloud-native application protection posture pillar, "
                 "consolidating cloud security posture management, cloud workload protection, cloud "
                 "infrastructure entitlement management, and data security posture management, plus "
                 "vulnerability management, and it scans agentlessly. Wiz Defend is the cloud detection and "
                 "response pillar for runtime threats. Beneath all three is the Wiz Security Graph, which "
                 "models cloud resources and their relationships so that attack paths, the toxic combinations "
                 "of public exposure, critical vulnerability, high privilege, and access to sensitive data "
                 "that form an exploitable route, are prioritized over a flat list of findings. The exam "
                 "mechanics for Cloud User and Cloud Fundamentals are portal-gated; only Defend Fundamentals "
                 "is published.")

    c.node_box(150, 42, 660, 44, "mgmt", [
        Line("WIZ — the graph-based, AGENTLESS cloud security platform (CNAPP + CDR)", 10.5, 700, "#111827"),
        Line("prioritize the ATTACK PATH, not the pile of findings — 'if Wiz says critical, it actually is'", 8, 400, "#374151"),
    ])

    # exam ladder
    c.node_box(40, 122, 280, 66, "alt", [
        Line("Cloud User", 9.5, 700, "#111827"),
        Line("entry — day-to-day Wiz Cloud user", 7.5, 400, "#374151"),
        Line("mechanics portal-gated", 7, 400, "#b91c1c"),
    ])
    c.node_box(340, 122, 280, 66, "data", [
        Line("Cloud Fundamentals ★ KEYSTONE", 9.5, 700, "#111827"),
        Line("deploy & manage Wiz Cloud", 7.5, 400, "#374151"),
        Line("PREREQUISITE for specialized exams", 7.5, 700, "#166534"),
    ])
    c.node_box(640, 122, 280, 66, "data", [
        Line("Defend Fundamentals", 9.5, 700, "#111827"),
        Line("cloud detection & response (SOC/IR)", 7.5, 400, "#374151"),
        Line("PUBLIC: 60Q / 150min / 2yr + badge", 7.5, 700, "#166534"),
    ])
    c.connector(320, 155, 340, 155, "data", label="", label_pos=(0, 0))
    c.connector(620, 155, 640, 155, "data", label="", label_pos=(0, 0))

    c.node_box(40, 206, 880, 30, "neutral", [
        Line("proctored (online or onsite) · open to customers/partners/professionals · YOUNG + EXPANDING (Feb 2025) — pillars are the stable map · training FREE via CloudSec Academy", 8, 700, "#111827"),
    ])

    # three pillars
    c.node_box(40, 256, 280, 60, "alt", [
        Line("WIZ CODE — shift-left / ASPM", 9, 700, "#111827"),
        Line("code · IaC · secrets", 7.5, 400, "#374151"),
        Line("catch risk BEFORE deploy", 7.5, 400, "#374151"),
    ])
    c.node_box(340, 256, 280, 60, "mgmt", [
        Line("WIZ CLOUD — CNAPP posture", 9, 700, "#111827"),
        Line("CSPM · CWPP · CIEM · DSPM · vulns", 7.5, 400, "#374151"),
        Line("AGENTLESS — 100% day-one coverage", 7.5, 400, "#166534"),
    ])
    c.node_box(640, 256, 280, 60, "alt", [
        Line("WIZ DEFEND — CDR (defensive)", 9, 700, "#111827"),
        Line("runtime detection & response", 7.5, 400, "#374151"),
        Line("+ optional lightweight sensor", 7.5, 400, "#374151"),
    ])
    c.connector(180, 316, 180, 340, "neutral", label="", label_pos=(0, 0))
    c.connector(480, 316, 480, 340, "neutral", label="", label_pos=(0, 0))
    c.connector(780, 316, 780, 340, "neutral", label="", label_pos=(0, 0))

    # security graph substrate
    c.node_box(40, 340, 880, 46, "mgmt", [
        Line("★ WIZ SECURITY GRAPH — the ONE substrate beneath all three pillars", 9, 700, "#111827"),
        Line("nodes = cloud resources · edges = relationships · ATTACK PATH = public exposure + critical vuln + high privilege + reaches sensitive data (toxic combination)", 7.5, 400, "#374151"),
    ])

    c.raw('<text x="40" y="410" font-size="9.5" font-weight="700" fill="#166534">'
          'Code-to-cloud-to-runtime: a runtime detection (Defend) traces back through cloud posture (Cloud) to the IaC line / PR that introduced it (Code) — one graph, one root cause.</text>')
    c.raw('<text x="40" y="429" font-size="9.5" font-weight="400" fill="#b91c1c">'
          'Only Defend Fundamentals\' mechanics are public (60Q / 150min / 2-year validity + shareable badge); Cloud User &amp; Cloud Fundamentals are portal-gated — the volume asserts only what Wiz publishes.</text>')
    c.raw('<text x="40" y="448" font-size="9.5" font-weight="400" fill="#374151">'
          'Modeled free in Python: ladder/prereq · pillar-by-job · list-vs-graph · agentless coverage · toxic combination · path prioritization + chokepoint · CSPM-to-compliance · in-context vulns ·</text>')
    c.raw('<text x="40" y="465" font-size="9.5" font-weight="400" fill="#374151">'
          'effective (chain-resolved) permissions · DSPM data exposure · shift-left cost curve · code-to-cloud trace · Defend detection enrichment · incident loop · Posture Issues grouping · democratization math.</text>')

    c.legend(40, 496, [
        ("alt", "Self-paced / shift-left / detect"),
        ("data", "Proctored exams"),
        ("neutral", "Structure"),
        ("mgmt", "Platform / graph"),
    ])
    c.save(f"{OUT}/chapter-01-certified-program.svg")


if __name__ == "__main__":
    ch01()
