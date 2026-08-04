#!/usr/bin/env python3
"""Volume CXXXVI (GitLab Certification Tracks) program map.

Chapter 1: GitLab University's five Associate certifications, their shared
exam mechanics ($150, 75 min, 50 Q, unproctored, 75% pass, 2 attempts in a
14-day window), the defined Professional tier, free learning paths, and
GitLab's distinctive version-based (non-expiring) certification model.

Run from scripts/diagrams:  python3 gen_volume136.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-136-gitlab-certifications"


def ch01():
    c = Canvas(960, 560,
        title="Chapter 1 Program Map: GitLab Certification (DevSecOps Platform)",
        subtitle="Five Associate certifications · $150 · 75 min / 50 Q unproctored · 75% to pass · 2 attempts in a 14-day window · certifications DO NOT EXPIRE",
        svg_title="Chapter 1 program map: the GitLab certification program",
        svg_desc="GitLab Certification runs in GitLab University and currently offers five Associate "
                 "certifications. Certified Fundamentals Associate is the recommended starting point, covering core "
                 "merge request and issue workflows, basic CI/CD pipelines, security scanning setup, and agile "
                 "planning. Certified CI/CD Associate covers pipeline components and GitLab's CI/CD functions. "
                 "Certified Agile Portfolio Management Associate covers organizational structure, issue lifecycles, "
                 "boards, epics, roadmaps, and velocity. Certified Security Associate covers SAST, DAST, secret "
                 "detection, dependency and container scanning, security policies, merge request approval workflows, "
                 "and license compliance. The new Certified GitLab Duo Agent Platform Associate covers agentic chat, "
                 "selecting the appropriate agent, configuring and publishing custom agents and flows, connecting "
                 "external tools via MCP, and AI-assisted code creation, review, and security workflows. Each "
                 "Associate exam costs 150 US dollars, runs 75 minutes with 50 multiple-choice and multiple-select "
                 "questions delivered unproctored online, requires 75 percent to pass, and allows two attempts "
                 "within a 14-day access window that begins at purchase. The handbook also defines a Professional "
                 "tier at 90 minutes and 60 questions, proctored through Certiverse. Free self-paced learning paths "
                 "back every exam. Distinctively, GitLab certifications do not expire and are governed by product "
                 "versioning rather than time, so candidates track major releases instead of a renewal date. Badges "
                 "issue through Credly, and using artificial intelligence or automated tools during exams is "
                 "prohibited by the Code of Conduct.")

    c.node_box(230, 42, 500, 44, "mgmt", [
        Line("GitLab — the single-application DevSecOps platform", 10.5, 700, "#111827"),
        Line("source · review · CI/CD · security · planning · deploy, one data model", 8.5, 400, "#374151"),
    ])

    # free paths band
    c.node_box(40, 122, 880, 34, "neutral", [
        Line("FREE self-paced learning paths back every exam: Fundamentals · CI Fundamentals · Agile Portfolio Mgmt · Security Essentials · Duo", 8.5, 400, "#374151"),
    ])

    # the five certs
    c.node_box(40, 176, 880, 30, "alt", [
        Line("ASSOCIATE CERTIFICATIONS  —  start with Fundamentals (GitLab's own recommendation)", 9.5, 700, "#111827"),
    ])
    c.node_box(40, 214, 172, 58, "data", [
        Line("Fundamentals", 9, 700, "#111827"),
        Line("MRs · issues", 7.5, 400, "#374151"),
        Line("basic CI/CD", 7.5, 400, "#374151"),
        Line("+ scanning setup", 7.5, 400, "#374151"),
    ])
    c.node_box(220, 214, 172, 58, "data", [
        Line("CI/CD", 9, 700, "#111827"),
        Line("pipelines · jobs", 7.5, 400, "#374151"),
        Line("runners", 7.5, 400, "#374151"),
        Line("artifacts/cache", 7.5, 400, "#374151"),
    ])
    c.node_box(400, 214, 172, 58, "data", [
        Line("Agile Portfolio", 9, 700, "#111827"),
        Line("labels · boards", 7.5, 400, "#374151"),
        Line("epics · roadmaps", 7.5, 400, "#374151"),
        Line("velocity", 7.5, 400, "#374151"),
    ])
    c.node_box(580, 214, 172, 58, "data", [
        Line("Security", 9, 700, "#111827"),
        Line("SAST · DAST", 7.5, 400, "#374151"),
        Line("secrets · deps", 7.5, 400, "#374151"),
        Line("policies · license", 7.5, 400, "#374151"),
    ])
    c.node_box(760, 214, 160, 58, "alt", [
        Line("Duo Agent (NEW)", 9, 700, "#111827"),
        Line("agentic chat", 7.5, 400, "#374151"),
        Line("agents + flows", 7.5, 400, "#374151"),
        Line("MCP tools", 7.5, 400, "#374151"),
    ])

    # mechanics band
    c.node_box(40, 292, 880, 56, "mgmt", [
        Line("Exam mechanics (Associate): $150 · 75 min · 50 Q · multiple choice/select · UNPROCTORED online · 75% to pass", 8.5, 700, "#111827"),
        Line("14-day access window STARTS AT PURCHASE (auto-unenroll) · 2 attempts per window · retakes at full price", 8.5, 400, "#374151"),
        Line("Professional tier defined: 90 min · 60 Q · proctored via Certiverse · Associate recommended first", 8.5, 400, "#374151"),
    ])

    c.raw('<text x="40" y="386" font-size="9.5" font-weight="700" fill="#166534">'
          'Certifications DO NOT EXPIRE — governed by GitLab PRODUCT VERSIONING, not a clock. Track major releases instead of a renewal date.</text>')
    c.raw('<text x="40" y="405" font-size="9.5" font-weight="400" fill="#374151">'
          'Credly badges. Code of Conduct PROHIBITS AI/automated tools during exams. Modeled free in Python: pipeline DAGs · rules · scanner triage · agent permissions · runner sizing.</text>')

    c.legend(40, 436, [
        ("neutral", "Free learning paths"),
        ("data", "Associate exams"),
        ("alt", "New / tier header"),
        ("mgmt", "Program facts"),
    ])
    c.save(f"{OUT}/chapter-01-certification-program.svg")


if __name__ == "__main__":
    ch01()
