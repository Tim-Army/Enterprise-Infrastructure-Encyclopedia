#!/usr/bin/env python3
"""Volume CLI (SentinelOne) University program map.

Chapter 1: the role-based SentinelOne University certifications (SIREN / THP /
Administrator 1-3 / CTP / CSP, Credly-badged) over the autonomous Singularity
platform, unified by behavioral AI, Storyline correlation, and rollback. Exam
mechanics (scores/durations/validity) are portal-gated; SIREN ~45h public.

Run from scripts/diagrams:  python3 gen_volume151.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-151-sentinelone-certifications"


def ch01():
    c = Canvas(960, 600,
        title="Chapter 1 Program Map: SentinelOne Certification Tracks",
        subtitle="role-based · Credly badges · SIREN ~45h + simulations · autonomous Singularity platform · exam mechanics portal-gated",
        svg_title="Chapter 1 program map: SentinelOne University certifications over the autonomous Singularity platform",
        svg_desc="SentinelOne University runs a role-based certification program that issues Credly digital "
                 "badges. The flagship is SIREN, the SentinelOne Incident Response Engineer, a practical "
                 "credential for incident responders, threat hunters, and SOC engineers that requires roughly "
                 "forty-five hours of University training before an online exam of multiple-choice and "
                 "scenario-based simulations. Threat Hunting Professional is an advanced specialization "
                 "covering attack analysis, anomaly detection, and SIEM and SOAR integration. Administrator "
                 "Levels 1 through 3 progress from policy management to API-driven automation. Certified "
                 "Technical Professional is for partners and integrators, covering architecture, policy "
                 "design, and deployment, and Certified Sales Professional is for channel partners. Exam "
                 "passing scores, durations, and validity are not published. Training uses on-demand courses, "
                 "interactive sessions, and hands-on labs and simulations. The platform beneath is the "
                 "Singularity Platform: Singularity Endpoint for autonomous endpoint protection unifying EPP "
                 "and EDR, Singularity Cloud for cloud workloads, Singularity Identity for identity threats, "
                 "Singularity XDR for extended detection and response across surfaces, the Singularity Data "
                 "Lake and AI SIEM for log analytics, Purple AI as a generative-AI security analyst, and "
                 "RemoteOps and Ranger. Three signatures unify the platform: behavioral AI that detects by "
                 "behavior on the agent rather than signatures, Storyline that autonomously correlates "
                 "related events into one attack narrative, and one-click remediation with rollback that "
                 "restores ransomware-encrypted files to their pre-attack state.")

    c.node_box(150, 42, 660, 44, "mgmt", [
        Line("SENTINELONE — AUTONOMOUS endpoint & extended security (Singularity)", 10.5, 700, "#111827"),
        Line("the AGENT detects (behavioral AI), responds at machine speed, correlates (Storyline), and rolls back — even offline", 8, 400, "#374151"),
    ])

    c.node_box(40, 120, 880, 26, "neutral", [
        Line("ROLE-BASED program · Credly digital badges · exams = MC + scenario SIMULATIONS · passing scores/durations/validity PORTAL-GATED", 8, 700, "#111827"),
    ])

    # certs
    c.node_box(40, 152, 280, 60, "data", [
        Line("SIREN — Incident Response Engineer", 8.8, 700, "#111827"),
        Line("IR / threat hunter / SOC · the ANCHOR", 7.3, 400, "#374151"),
        Line("~45h training + simulations", 7.3, 700, "#166534"),
    ])
    c.node_box(340, 152, 270, 60, "data", [
        Line("THP — Threat Hunting Professional", 8.8, 700, "#111827"),
        Line("advanced: attack analysis, anomaly,", 7.3, 400, "#374151"),
        Line("SIEM/SOAR integration", 7.3, 400, "#374151"),
    ])
    c.node_box(630, 152, 290, 60, "alt", [
        Line("Administrator Levels 1-3", 8.8, 700, "#111827"),
        Line("deploy/policy -> API automation", 7.3, 400, "#374151"),
        Line("+ CTP (partner) · CSP (sales)", 7.3, 400, "#374151"),
    ])

    # three signatures
    c.node_box(40, 226, 880, 46, "alt", [
        Line("★ THREE SIGNATURES (what 'autonomous' means)", 8.5, 700, "#111827"),
        Line("BEHAVIORAL AI (detect by behavior, catches novel + fileless) · STORYLINE (auto-correlate events -> ONE attack narrative) · ROLLBACK (undo damage, restore ransomware-encrypted files)", 7.3, 400, "#374151"),
    ])

    # platform
    c.node_box(40, 286, 880, 60, "mgmt", [
        Line("SINGULARITY PLATFORM", 8.5, 700, "#111827"),
        Line("ENDPOINT (EPP+EDR, autonomous, on-agent, works OFFLINE) · IDENTITY (threats + deception) · CLOUD (CWPP/CNAPP) · XDR (cross-surface correlation)", 7.3, 400, "#374151"),
        Line("DATA LAKE + AI SIEM (log analytics, ingests 3rd-party telemetry) · PURPLE AI (GenAI analyst — natural-language hunting) · RemoteOps · Ranger", 7.3, 400, "#374151"),
    ])

    c.raw('<text x="40" y="372" font-size="9.5" font-weight="700" fill="#166534">'
          'Attacks move at MACHINE SPEED — only autonomous on-agent response is fast enough (a human SOC loses the disk before reading the alert). The human supervises + hunts.</text>')
    c.raw('<text x="40" y="391" font-size="9.5" font-weight="400" fill="#b91c1c">'
          'Defensive throughout (protect / detect / hunt / respond / recover). Completes the endpoint cluster with CrowdStrike (L) + Trellix; feeds the SOC/SIEM (Splunk XLV).</text>')
    c.raw('<text x="40" y="410" font-size="9.5" font-weight="400" fill="#374151">'
          'Modeled free in Python: role-program reading · behavioral-vs-signature detection · machine-speed response · Storyline event correlation · MTTR reduction ·</text>')
    c.raw('<text x="40" y="427" font-size="9.5" font-weight="400" fill="#374151">'
          'IR workflow (triage/scope/contain/remediate) · threat hunting · complete remediation · ransomware rollback at scale · cross-surface XDR · natural-language AI hunting · detect-vs-protect policy rollout.</text>')

    c.legend(40, 458, [
        ("data", "Responder certs"),
        ("alt", "Admin / signatures"),
        ("neutral", "Program shape"),
        ("mgmt", "Platform"),
    ])
    c.save(f"{OUT}/chapter-01-university-program.svg")


if __name__ == "__main__":
    ch01()
