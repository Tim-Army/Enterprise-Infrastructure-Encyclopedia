#!/usr/bin/env python3
"""Volume CXLVIII (Snyk) Snyk Learn program map.

Chapter 1: Snyk Learn (free learning paths + lessons -> Certificates of
Completion, security education + product training + AI Security University) over
the developer-first platform (Open Source / Code / Container / IaC + ASPM). It is
a certificate-of-completion / badges program, not proctored exams.

Run from scripts/diagrams:  python3 gen_volume148.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-148-snyk-certifications"


def ch01():
    c = Canvas(960, 600,
        title="Chapter 1 Program Map: Snyk Certification Tracks (Snyk Learn)",
        subtitle="free learning paths -> Certificates of Completion · developer-first · NOT proctored exams",
        svg_title="Chapter 1 program map: Snyk Learn over the developer-first application-security platform",
        svg_desc="Snyk's education and credentialing is Snyk Learn, free interactive developer security "
                 "education and product training. It is a certificate-of-completion program, not proctored "
                 "exams: you complete a learning path, a sequence of interactive lessons, and earn a "
                 "downloadable Certificate of Completion, with a free account tracking progress. Snyk Learn "
                 "has two axes. By type, it splits into security education, about one hundred twenty-eight "
                 "items, and product training, about sixty-four items. By format, it splits into learning "
                 "paths, about eighteen, and individual lessons, about one hundred seventy-four. Learning "
                 "paths include Security for Developers, the OWASP Top 10, the OWASP Top 10 for large "
                 "language models and generative AI, the OWASP Top 10 for agentic applications, the OWASP "
                 "Top 10 for open source software, Secure AI Development, and Implementing Snyk enterprise "
                 "administration and architecture. A separate Snyk AI Security University Program offers "
                 "structured AI-security education. The platform the product training covers is developer "
                 "first, meeting developers in the IDE, command line, pull request, and CI/CD pipeline to "
                 "find and fix. It spans four scanning engines plus posture management: Snyk Open Source for "
                 "software composition analysis of open-source dependencies, Snyk Code for static "
                 "application security testing powered by DeepCode AI, Snyk Container for container image "
                 "scanning with base-image recommendations, Snyk Infrastructure as Code for scanning "
                 "Terraform, CloudFormation, and Kubernetes manifests before deployment, and Application "
                 "Security Posture Management across the software development lifecycle. Together the four "
                 "engines cover the application supply chain: your first-party code, open-source "
                 "dependencies, the container image, and the infrastructure.")

    c.node_box(150, 42, 660, 44, "mgmt", [
        Line("SNYK — the DEVELOPER-FIRST application security platform", 10.5, 700, "#111827"),
        Line("security delivered TO developers, in their workflow (IDE / CLI / PR / CI-CD) — find AND fix", 8, 400, "#374151"),
    ])

    # Snyk Learn box
    c.node_box(40, 120, 880, 60, "alt", [
        Line("SNYK LEARN — free, self-paced developer-security education + product training", 9.5, 700, "#111827"),
        Line("~18 LEARNING PATHS + ~174 LESSONS · TYPE: ~128 security education / ~64 product training · complete a PATH -> Certificate of Completion", 8, 400, "#374151"),
        Line("★ CERTIFICATE-OF-COMPLETION program, NOT proctored exams (a learning credential — free, hands-on, current) · + Snyk AI Security University Program", 7.5, 700, "#166534"),
    ])

    # learning paths row
    c.node_box(40, 196, 430, 60, "neutral", [
        Line("SECURITY EDUCATION paths (vendor-neutral)", 8.5, 700, "#111827"),
        Line("Security for Developers · OWASP Top 10 · OWASP for", 7.5, 400, "#374151"),
        Line("LLM/GenAI · Agentic · Open Source · Secure AI Dev", 7.5, 400, "#374151"),
    ])
    c.node_box(490, 196, 430, 60, "neutral", [
        Line("PRODUCT TRAINING paths", 8.5, 700, "#111827"),
        Line("the 4 engines + Implementing Snyk:", 7.5, 400, "#374151"),
        Line("Enterprise Administration & Architecture", 7.5, 400, "#374151"),
    ])

    # four engines
    c.node_box(40, 272, 215, 58, "data", [
        Line("Snyk Open Source", 8.5, 700, "#111827"),
        Line("SCA — dependencies", 7, 400, "#374151"),
        Line("transitive vulns", 7, 400, "#374151"),
    ])
    c.node_box(263, 272, 215, 58, "data", [
        Line("Snyk Code", 8.5, 700, "#111827"),
        Line("SAST — your code", 7, 400, "#374151"),
        Line("DeepCode AI · in-IDE", 7, 400, "#374151"),
    ])
    c.node_box(486, 272, 210, 58, "data", [
        Line("Snyk Container", 8.5, 700, "#111827"),
        Line("image scanning", 7, 400, "#374151"),
        Line("base-image fix multiplies", 7, 400, "#374151"),
    ])
    c.node_box(704, 272, 216, 58, "data", [
        Line("Snyk IaC", 8.5, 700, "#111827"),
        Line("Terraform/CF/K8s", 7, 400, "#374151"),
        Line("catch misconfig pre-deploy", 7, 400, "#374151"),
    ])

    c.node_box(40, 346, 880, 30, "mgmt", [
        Line("+ ASPM — Application Security Posture Management across the SDLC (portfolio risk, coverage gaps, priority score: severity + exploit maturity + REACHABILITY + fixability)", 7.5, 700, "#111827"),
    ])

    c.raw('<text x="40" y="400" font-size="9.5" font-weight="700" fill="#166534">'
          'The 4 engines cover the whole APPLICATION SUPPLY CHAIN: your first-party CODE + open-source DEPENDENCIES + the CONTAINER image + the INFRASTRUCTURE (IaC).</text>')
    c.raw('<text x="40" y="419" font-size="9.5" font-weight="400" fill="#b91c1c">'
          'Snyk Learn is a certificate-of-completion / badges program, stated plainly — NOT a proctored-exam certification. Free account, downloadable certificate per learning path.</text>')
    c.raw('<text x="40" y="438" font-size="9.5" font-weight="400" fill="#374151">'
          'Modeled free in Python: program-shape · supply-chain map · find-vs-fix · adoption math · transitive dependency + minimal upgrade · SAST source-to-sink + false positives ·</text>')
    c.raw('<text x="40" y="455" font-size="9.5" font-weight="400" fill="#374151">'
          'base-image multiplier · IaC drift + policy-as-code · AI-generated-code review gap · agent least-privilege · priority score (reachability) · CI/CD gate threshold.</text>')

    c.legend(40, 486, [
        ("alt", "Snyk Learn"),
        ("neutral", "Path types"),
        ("data", "Scanning engines"),
        ("mgmt", "Platform / posture"),
    ])
    c.save(f"{OUT}/chapter-01-snyk-learn-program.svg")


if __name__ == "__main__":
    ch01()
