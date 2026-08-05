#!/usr/bin/env python3
"""Volume CLII (JFrog) certification-program map.

Chapter 1: JFrog Academy certifications (3 Associate: Artifactory / HA-DR /
Security + the flagship DevOps Engineer, 47Q/90min/70%/2yr proctored) over the
Software Supply Chain Platform (Artifactory + Xray + Curation + Distribution),
with Artifactory the single source of truth for binaries.

Run from scripts/diagrams:  python3 gen_volume152.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-152-jfrog-certifications"


def ch01():
    c = Canvas(960, 600,
        title="Chapter 1 Program Map: JFrog Certification Tracks",
        subtitle="3 Associate certs + DevOps Engineer (47Q/90min/70%/2yr, proctored) · JFrog Academy · Software Supply Chain Platform",
        svg_title="Chapter 1 program map: JFrog Academy certifications over the Software Supply Chain Platform",
        svg_desc="The JFrog certification program is delivered through JFrog Academy with free and paid "
                 "courses, learning paths, and certifications. Three Associate-level certifications, each "
                 "valid for two years, cover distinct domains: Associate JFrog Artifactory for artifact "
                 "management and deployment, Associate JFrog DevOps High Availability and Disaster Recovery "
                 "for distributed systems and repository federation, and Associate JFrog Security for "
                 "application security. Above them, the JFrog Artifactory Certified DevOps Engineer is the "
                 "flagship credential, a web-based proctored exam of forty-seven multiple-choice and "
                 "multiple-answer questions in ninety minutes with a passing score of seventy percent, valid "
                 "two years, validating binary repository management, security, and CI/CD pipelines. The "
                 "platform beneath is the JFrog Software Supply Chain Platform, centered on Artifactory, the "
                 "universal binary repository manager that stores every package type in local, remote, and "
                 "virtual repositories and is the single source of truth for binaries. Xray provides deep "
                 "recursive vulnerability and license scanning with impact analysis; JFrog Advanced Security "
                 "and Curation defend the supply chain by blocking malicious packages at the gate; "
                 "Distribution delivers signed release bundles to edges; and Pipelines provides CI/CD. "
                 "Binaries are built once, stored with build info for traceability, scanned, promoted "
                 "immutably from development through staging to production, and distributed to the edge, "
                 "traceable, secure, reproducible, and available the entire way.")

    c.node_box(160, 42, 640, 44, "mgmt", [
        Line("JFROG — the BINARY hub + Software Supply Chain Platform", 10.5, 700, "#111827"),
        Line("Git owns the SOURCE code; JFrog owns the BINARIES it becomes — the single source of truth", 8, 400, "#374151"),
    ])

    c.node_box(40, 120, 880, 26, "neutral", [
        Line("JFrog ACADEMY (free + paid courses, learning paths) · all certs 2-YEAR validity · JFrog PUBLISHES the DevOps Engineer mechanics", 8, 700, "#111827"),
    ])

    # associate certs
    c.node_box(40, 152, 280, 54, "alt", [
        Line("Associate ARTIFACTORY", 8.8, 700, "#111827"),
        Line("artifact mgmt + deployment", 7.3, 400, "#374151"),
        Line("the FOUNDATION", 7.3, 700, "#166534"),
    ])
    c.node_box(340, 152, 270, 54, "alt", [
        Line("Associate HA/DR", 8.8, 700, "#111827"),
        Line("high availability, disaster", 7.3, 400, "#374151"),
        Line("recovery, federation", 7.3, 400, "#374151"),
    ])
    c.node_box(630, 152, 290, 54, "alt", [
        Line("Associate SECURITY", 8.8, 700, "#111827"),
        Line("Xray, Curation,", 7.3, 400, "#374151"),
        Line("supply-chain security", 7.3, 400, "#374151"),
    ])
    # capstone
    c.node_box(40, 218, 880, 34, "data", [
        Line("★ JFrog Artifactory Certified DEVOPS ENGINEER (capstone) — repos + security + CI/CD together · 47 questions / 90 min / 70% to pass / proctored / 2-yr", 8.3, 700, "#111827"),
    ])
    c.connector(180, 206, 400, 218, "data", label="", label_pos=(0, 0))
    c.connector(760, 206, 500, 218, "data", label="", label_pos=(0, 0))

    # platform
    c.node_box(40, 268, 880, 60, "mgmt", [
        Line("SOFTWARE SUPPLY CHAIN PLATFORM", 8.5, 700, "#111827"),
        Line("ARTIFACTORY (universal binary repo — ALL package types; LOCAL/REMOTE-cache/VIRTUAL-aggregate; build info + immutable PROMOTION dev→stg→prod)", 7.3, 400, "#374151"),
        Line("XRAY (deep-recursive vuln+license scan · IMPACT ANALYSIS) · CURATION (block bad packages at the GATE) · DISTRIBUTION (release bundles → edges) · Pipelines (CI/CD)", 7.3, 400, "#374151"),
    ])

    c.raw('<text x="40" y="354" font-size="9.5" font-weight="700" fill="#166534">'
          'The end-to-end journey (DevOps Engineer mindset): BUILD ONCE → store + build info → Xray scan (Curation-gated deps) → PROMOTE immutably → DISTRIBUTE to edge — traceable, secure, reproducible.</text>')
    c.raw('<text x="40" y="373" font-size="9.5" font-weight="400" fill="#b91c1c">'
          'The binary hub is on the CRITICAL PATH of every build + deploy — so it must be HIGHLY AVAILABLE (a hub outage halts the whole pipeline org-wide). HA (cluster) != DR (site replication).</text>')
    c.raw('<text x="40" y="392" font-size="9.5" font-weight="400" fill="#374151">'
          'Modeled free in Python: program reading · source-vs-binaries · universal-repo consolidation · remote-cache resilience · virtual-repo aggregation · build-once-promote-many + immutability ·</text>')
    c.raw('<text x="40" y="409" font-size="9.5" font-weight="400" fill="#374151">'
          'deep-recursive Xray scan · CVE impact analysis · Curation gate · HA availability math · end-to-end pipeline. Completes the DevOps toolchain (GitLab CXXXVI, GitHub LXXXIX); Xray complements Snyk (CXLVIII).</text>')

    c.legend(40, 440, [
        ("alt", "Associate certs"),
        ("data", "DevOps Engineer"),
        ("neutral", "Program shape"),
        ("mgmt", "Platform"),
    ])
    c.save(f"{OUT}/chapter-01-certification-program.svg")


if __name__ == "__main__":
    ch01()
