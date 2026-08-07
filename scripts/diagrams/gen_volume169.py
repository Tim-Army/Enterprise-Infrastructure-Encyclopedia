#!/usr/bin/env python3
"""Volume CLXIX (Hitachi Vantara) program map.

Chapter 1: the Hitachi Vantara Certified Professional program — Qualification (HQT-)
Associate/Professional and Certification (HCE-) Specialist/Expert credentials — across
tracks: block/file/object storage (VSP), data protection, Hitachi Ops Center, Pentaho,
and converged/UCP. Enterprise data infrastructure: hold, protect, manage, archive, analyze.

Run from scripts/diagrams:  python3 gen_volume169.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-169-hitachi-vantara-certifications"


def ch01():
    c = Canvas(960, 620,
        title="Chapter 1 Program Map: Hitachi Vantara Certification Tracks",
        subtitle="HVCP — Qualification (HQT-) Associate/Professional + Certification (HCE-) Specialist/Expert · VSP storage · valid 2-3 yr",
        svg_title="Chapter 1 program map: the Hitachi Vantara certification categories and tracks over its data infrastructure",
        svg_desc="Hitachi Vantara is the data-infrastructure arm of Hitachi — enterprise storage, the VSP Virtual "
                 "Storage Platform, data protection, Hitachi Ops Center management, and Pentaho data software. The "
                 "Hitachi Vantara Certified Professional program splits into two categories: Qualification "
                 "credentials, earned through HQT exams, at Associate and Professional levels, medium-stakes and "
                 "some open-book; and Certification credentials, earned through HCE exams, at Specialist and "
                 "Expert levels, high-stakes, closed-book, and proctored, validating hands-on skills. The tracks "
                 "span block storage on VSP 5000, VSP One Block, VSP Midrange, and VSP 360; file storage on VSP "
                 "One File; object storage on Content Platform; data protection and replication with ShadowImage, "
                 "Thin Image, TrueCopy, and Universal Replicator; Hitachi Ops Center Administrator, Automator, "
                 "Protector, and Analyzer; Pentaho Data Integration and Business Analytics; and converged UCP with "
                 "hybrid cloud. A representative exam, HQT-6742 for VSP 360 Storage Administration, is thirty-five "
                 "questions in sixty minutes at sixty-five percent to pass for one hundred dollars. Credentials "
                 "are valid two to three years. The lifecycle is hold, protect, manage, archive, and analyze.")

    c.node_box(150, 42, 660, 44, "mgmt", [
        Line("HITACHI VANTARA — enterprise DATA INFRASTRUCTURE: VSP storage · data protection · Ops Center · Pentaho data software", 8.3, 700, "#111827"),
        Line("VSP (Virtual Storage Platform): block/file/object · dual controllers + cache + RAID · storage VIRTUALIZATION · SVOS", 7.0, 400, "#374151"),
    ])

    c.node_box(40, 120, 880, 40, "neutral", [
        Line("HITACHI VANTARA CERTIFIED PROFESSIONAL (HVCP) — two categories, four levels", 8.3, 700, "#111827"),
        Line("QUALIFICATION (HQT- exams): Associate → Professional (medium-stakes, some open-book)   ·   CERTIFICATION (HCE- exams): Specialist → Expert (high-stakes, PROCTORED, hands-on)   |   valid 2-3 yr", 6.0, 400, "#374151"),
    ])

    c.node_box(40, 176, 288, 46, "data", [
        Line("BLOCK STORAGE ADMIN (VSP 360)", 7.4, 700, "#111827"),
        Line("HQT-6742 (35Q/60min/65%/$100) · pools/LDEVs · thin · tiering", 5.7, 400, "#374151"),
    ])
    c.node_box(336, 176, 288, 46, "data", [
        Line("FILE + OBJECT STORAGE", 7.8, 700, "#111827"),
        Line("VSP One File (NFS/SMB) · Content Platform (S3, WORM, scale)", 5.8, 400, "#374151"),
    ])
    c.node_box(632, 176, 288, 46, "data", [
        Line("DATA PROTECTION + REPLICATION", 7.2, 700, "#111827"),
        Line("ShadowImage/Thin Image · TrueCopy (sync) · Univ Replicator (async) · RPO/RTO", 5.2, 400, "#374151"),
    ])
    c.node_box(40, 236, 288, 46, "alt", [
        Line("HITACHI OPS CENTER", 7.8, 700, "#111827"),
        Line("Administrator · Automator (self-service) · Protector · Analyzer", 5.7, 400, "#374151"),
    ])
    c.node_box(336, 236, 288, 46, "alt", [
        Line("PENTAHO (data track)", 7.8, 700, "#111827"),
        Line("Data Integration (PDI: transforms + jobs) · Business Analytics", 5.8, 400, "#374151"),
    ])
    c.node_box(632, 236, 288, 46, "alt", [
        Line("CONVERGED / UCP + HYBRID CLOUD", 7.2, 700, "#111827"),
        Line("UCP validated stack vs hyperconverged · cloud tiering (S3)", 5.8, 400, "#374151"),
    ])

    c.raw('<text x="40" y="308" font-size="9.5" font-weight="700" fill="#166534">'
          'HOLD (storage) + PROTECT (snapshots + replication) + MANAGE (Ops Center automate/analyze) + ARCHIVE (object/cloud) + ANALYZE (Pentaho) — the enterprise data-infrastructure lifecycle.</text>')
    c.raw('<text x="40" y="330" font-size="9.5" font-weight="400" fill="#374151">'
          'Modeled free in Python: categories + levels + tracks/mechanics · VSP redundancy + virtualization · pool→LDEV→host + thin + monitor · file quotas + object WORM/metadata · local snapshot + sync/async replication + DR ·</text>')
    c.raw('<text x="40" y="347" font-size="9.5" font-weight="400" fill="#374151">'
          'Ops Center automate + capacity forecast · PDI transform/job + Business Analytics · converged-vs-HCI + cloud tiering · capstone data-infra end-to-end. Peers: NetApp (LXXXIV), Dell (XXXII), Everpure (CXXXVIII).</text>')

    c.legend(40, 376, [
        ("data", "Storage / protect"),
        ("alt", "Manage / data / cloud"),
        ("neutral", "Cert categories"),
        ("mgmt", "VSP data infrastructure"),
    ])
    c.save(f"{OUT}/chapter-01-program.svg")


if __name__ == "__main__":
    ch01()
