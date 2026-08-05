#!/usr/bin/env python3
"""Volume CLVII (Cohesity) program map.

Chapter 1: the Cohesity Academy three-tier certifications (Associate/Professional/
Specialist; CCPA/CCIP/CCPP/CCSS; proctored $200 / 2yr) over the AI-powered Data
Cloud platform — DataProtect, ransomware resilience, SmartFiles, FortKnox, AI
(DataHawk/Gaia), and the Veritas/NetBackup portfolio.

Run from scripts/diagrams:  python3 gen_volume157.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-157-cohesity-certifications"


def ch01():
    c = Canvas(960, 620,
        title="Chapter 1 Program Map: Cohesity Certification Tracks",
        subtitle="Cohesity Academy — Associate/Professional/Specialist (CCPA/CCIP/CCPP/CCSS) · proctored $200 / 2yr · AI-powered Data Cloud",
        svg_title="Chapter 1 program map: the Cohesity Academy certifications over the AI-powered Data Cloud",
        svg_desc="Cohesity Academy offers proctored certification exams across three tiers. The Associate level "
                 "includes Protection Associate for DataProtect, exam COH100, and Protection Associate for "
                 "Multicloud, both carrying the Cohesity Certified Protection Associate credential. The "
                 "Professional level includes Implementation Professional for SmartFiles and two NetBackup "
                 "Protection Professional certifications from the Veritas heritage. The Specialist level is the "
                 "Security Specialist, exam COH350. Exams are proctored, cost two hundred dollars, are valid "
                 "for two years, and grant a digital badge; the DataProtect associate exam is ninety minutes "
                 "with a fifty-eight percent passing score. The platform beneath is the AI-powered Cohesity "
                 "Data Cloud: DataProtect for backup and recovery, ransomware resilience through immutable "
                 "snapshots, DataLock WORM, air-gapping and anomaly detection, SmartFiles for software-defined "
                 "file and object services, FortKnox for SaaS cyber-vaulting, and AI through DataHawk threat "
                 "detection and classification and Gaia generative search. Cohesity merged with Veritas in "
                 "December 2024, adding NetBackup. The thesis is that backup is both the last line of defense "
                 "against ransomware and a prime target of it, so data management and security have converged.")

    c.node_box(150, 42, 660, 44, "mgmt", [
        Line("COHESITY — AI-powered DATA SECURITY & MANAGEMENT (backup/recovery + ransomware resilience)", 10, 700, "#111827"),
        Line("backup = the LAST line of defense AND a ransomware TARGET -> data management + security have CONVERGED", 8, 400, "#374151"),
    ])

    c.node_box(40, 120, 880, 40, "neutral", [
        Line("COHESITY ACADEMY — 3 TIERS · proctored digital-badge exams · $200 · valid 2 YEARS · ~3 months hands-on recommended", 8.3, 700, "#111827"),
        Line("ASSOCIATE (CCPA): Protection Associate — DataProtect (COH100) · Multicloud   |   PROFESSIONAL (CCIP/CCPP): SmartFiles · Protection Pro · NetBackup ×2   |   SPECIALIST (CCSS): Security (COH350)", 6.9, 400, "#374151"),
    ])

    # platform capabilities
    c.node_box(40, 176, 288, 50, "data", [
        Line("DATAPROTECT (the core)", 8.5, 700, "#111827"),
        Line("policy-based backup + recovery +", 7.2, 400, "#374151"),
        Line("replication + archival · INSTANT MASS RESTORE", 7.0, 400, "#374151"),
    ])
    c.node_box(336, 176, 288, 50, "data", [
        Line("RANSOMWARE RESILIENCE", 8.5, 700, "#111827"),
        Line("IMMUTABLE snapshots · DataLock/WORM ·", 7.2, 400, "#374151"),
        Line("air-gap · anomaly detection · clean recovery", 7.0, 400, "#374151"),
    ])
    c.node_box(632, 176, 288, 50, "data", [
        Line("SMARTFILES (CCIP)", 8.5, 700, "#111827"),
        Line("software-defined FILE + OBJECT services", 7.2, 400, "#374151"),
        Line("(NFS/SMB/S3) — consolidate NAS, security-aware", 7.0, 400, "#374151"),
    ])
    c.node_box(40, 236, 288, 50, "alt", [
        Line("FORTKNOX (SaaS cyber-vault)", 8.3, 700, "#111827"),
        Line("ISOLATED + IMMUTABLE + AIR-GAPPED copy", 7.2, 400, "#374151"),
        Line("(3-2-1-1) · clean-room recovery", 7.0, 400, "#374151"),
    ])
    c.node_box(336, 236, 288, 50, "alt", [
        Line("AI — DataHawk + Gaia", 8.5, 700, "#111827"),
        Line("threat detection · sensitive-data classify ·", 7.2, 400, "#374151"),
        Line("Gaia GEN-AI conversational search", 7.0, 400, "#374151"),
    ])
    c.node_box(632, 236, 288, 50, "alt", [
        Line("NETBACKUP (Veritas, merged 12/2024)", 7.6, 700, "#111827"),
        Line("enterprise backup + NetBackup APPLIANCES;", 7.0, 400, "#374151"),
        Line("largest data-protection vendor · MULTICLOUD", 7.0, 400, "#374151"),
    ])

    c.raw('<text x="40" y="312" font-size="9.5" font-weight="700" fill="#166534">'
          'Ransomware resilience = IMMUTABILITY (a clean copy EXISTS) + ANOMALY DETECTION (know WHICH copy is clean) + RAPID MASS RESTORE (bring the estate back) -> ransomware becomes a RECOVERABLE event, not "pay or lose everything".</text>')
    c.raw('<text x="40" y="331" font-size="9.5" font-weight="400" fill="#b91c1c">'
          'Attackers delete mutable backups FIRST; immutable + air-gapped (FortKnox) copies survive even total compromise. Backup is a SECURITY function. Defensive throughout — data resilience.</text>')
    c.raw('<text x="40" y="350" font-size="9.5" font-weight="400" fill="#374151">'
          'Modeled free in Python: 3-tier program + exam rule set · immutable-vs-mutable survival · policy protection + mass restore · anomaly detection + clean recovery point · air-gap survives total breach ·</text>')
    c.raw('<text x="40" y="367" font-size="9.5" font-weight="400" fill="#374151">'
          'NAS consolidation · AI detection/classification/Gaia search · combined Cohesity+NetBackup portfolio. Data-security cluster: Rubrik (CXXX) peer, Commvault (CXXXIII), EDR CrowdStrike (L)/SentinelOne (CLI) = prevent, Cohesity = recover.</text>')

    c.legend(40, 398, [
        ("data", "Core (protect/resilience/files)"),
        ("alt", "Vault / AI / NetBackup"),
        ("neutral", "Academy program"),
        ("mgmt", "Data security thesis"),
    ])
    c.save(f"{OUT}/chapter-01-program.svg")


if __name__ == "__main__":
    ch01()
