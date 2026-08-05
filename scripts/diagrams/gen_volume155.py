#!/usr/bin/env python3
"""Volume CLV (Sysdig) program map.

Chapter 1: Sysdig's Credly-badged accreditations (Kraken Hunter, Partner
Technical) + the open-source Falco path (CNCF/LF LFS254), over the runtime-first
CNAPP (Falco CDR + in-use vuln mgmt + CSPM/CIEM), built on eBPF deep visibility.

Run from scripts/diagrams:  python3 gen_volume155.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-155-sysdig-certifications"


def ch01():
    c = Canvas(960, 600,
        title="Chapter 1 Program Map: Sysdig Certification Tracks",
        subtitle="Credly badges (Kraken Hunter) + open-source Falco (CNCF/LF LFS254) · RUNTIME-FIRST CNAPP on eBPF",
        svg_title="Chapter 1 program map: the Sysdig accreditations and Falco path over the runtime-first platform",
        svg_desc="Sysdig's program has two strands. Its own credentials are Credly digital badges earned "
                 "through its enablement portal, most notably the Kraken Hunter accreditation, a hands-on "
                 "workshop of labs and presentations plus an exam validating Sysdig-tooling skill for cloud "
                 "and container security, and a Partner Technical Accreditation program. Separately, Falco, "
                 "the open-source runtime security engine that Sysdig created and donated to the Cloud Native "
                 "Computing Foundation, has its own training path: the twenty-hour Detecting Cloud Runtime "
                 "Threats with Falco course, LFS254, built by CNCF, the Linux Foundation, and Sysdig. The "
                 "platform beneath is runtime-first. Sysdig Secure is an enterprise cloud-native application "
                 "protection platform unifying cloud detection and response with Falco-powered five-second "
                 "detection, vulnerability management prioritized by in-use runtime context, cloud security "
                 "posture management, cloud infrastructure entitlement management right-sized from observed "
                 "usage, and compliance, all on shared deep runtime data captured by eBPF kernel "
                 "instrumentation. Sysdig Monitor adds Prometheus-based observability on the same "
                 "foundation. Runtime-first means securing what is actually running, complementing agentless "
                 "posture, which tells you what could be wrong, with runtime, which tells you what is "
                 "happening now, catching zero-days, drift, and insider actions that posture is blind to.")

    c.node_box(150, 42, 660, 44, "mgmt", [
        Line("SYSDIG — RUNTIME-FIRST cloud-native security (Sysdig Secure) + the creator of FALCO", 10.5, 700, "#111827"),
        Line("secure what's actually RUNNING — posture (Wiz CXLVII) says what COULD be wrong; runtime says what IS happening now", 8, 400, "#374151"),
    ])

    c.node_box(40, 120, 880, 26, "neutral", [
        Line("TWO STRANDS · Credly badges (enablement portal) + open-source FALCO (CNCF/LF) · a badges + hands-on-training model (NOT proctored exams)", 8, 700, "#111827"),
    ])

    # two strands
    c.node_box(40, 152, 430, 58, "data", [
        Line("SYSDIG accreditations (Credly)", 8.8, 700, "#111827"),
        Line("★ KRAKEN HUNTER — Sysdig tooling for cloud & container", 7.3, 400, "#374151"),
        Line("security (workshop LABS + exam) · Partner Technical Accred", 7.3, 400, "#374151"),
    ])
    c.node_box(490, 152, 430, 58, "alt", [
        Line("FALCO (open-source, CNCF)", 8.8, 700, "#111827"),
        Line("Sysdig CREATED Falco + donated it to CNCF", 7.3, 400, "#374151"),
        Line("★ LFS254 'Detecting Cloud Runtime Threats w/ Falco' (~20h)", 7.3, 400, "#374151"),
    ])

    # platform
    c.node_box(40, 224, 880, 60, "mgmt", [
        Line("RUNTIME-FIRST CNAPP (Sysdig Secure) — all on SHARED deep runtime data", 8.5, 700, "#111827"),
        Line("★ FALCO-powered CDR (detection-as-code rules · 5-SECOND detection · DRIFT: running container != image = tampering, signature-free)", 7.3, 400, "#374151"),
        Line("VULN MGMT (★ IN-USE: only ~fraction of packages LOADED at runtime = the real risk) · CSPM (posture) · CIEM (right-size from OBSERVED usage) · compliance", 7.2, 400, "#374151"),
    ])

    # ebpf foundation
    c.node_box(40, 298, 880, 34, "data", [
        Line("★ FOUNDATION: eBPF — safe in-kernel instrumentation of SYSTEM CALLS = ground truth of what actually happened · deep visibility, low overhead, no code changes, one agent/host", 7.8, 700, "#111827"),
    ])

    c.raw('<text x="40" y="356" font-size="9.5" font-weight="700" fill="#166534">'
          'Runtime is the CONNECTIVE TISSUE: the same observation sharpens vuln prioritization (in-use), posture (running+exposed), entitlements (used perms) AND detection. Security + observability, one data foundation.</text>')
    c.raw('<text x="40" y="375" font-size="9.5" font-weight="400" fill="#b91c1c">'
          'Containers are EPHEMERAL (live seconds) — a periodic scan misses them; only real-time runtime detection + eBPF capture sees + records what a short-lived container did. Defensive throughout.</text>')
    c.raw('<text x="40" y="394" font-size="9.5" font-weight="400" fill="#374151">'
          'Modeled free in Python: two-strand program · runtime-vs-posture coverage gap · Falco rule detection · syscall ground-truth (vs logs) · drift detection · in-use vuln prioritization ·</text>')
    c.raw('<text x="40" y="411" font-size="9.5" font-weight="400" fill="#374151">'
          'runtime-informed CIEM right-sizing · shared-runtime-data CNAPP. Completes the cloud-native security cluster: Wiz (CXLVII) posture, CNCF (XLI) K8s + Falco, SentinelOne (CLI) endpoint. Falco is open-source + CNCF = transferable.</text>')

    c.legend(40, 442, [
        ("data", "Sysdig / eBPF"),
        ("alt", "Falco (open-source)"),
        ("neutral", "Program shape"),
        ("mgmt", "Runtime-first platform"),
    ])
    c.save(f"{OUT}/chapter-01-program.svg")


if __name__ == "__main__":
    ch01()
