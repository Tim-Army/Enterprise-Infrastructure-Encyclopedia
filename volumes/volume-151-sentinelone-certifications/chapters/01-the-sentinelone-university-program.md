# Chapter 01: The SentinelOne University Program

![The SentinelOne University certification program and the Singularity platform beneath it. The program is role-based and issues Credly digital badges. Certifications include SIREN, the SentinelOne Incident Response Engineer, the flagship practical credential for incident responders, threat hunters, and SOC engineers, which requires roughly forty-five hours of University training before an online exam of multiple-choice and scenario-based simulations; Threat Hunting Professional for advanced analysts covering attack analysis and SIEM and SOAR integration; Administrator Levels 1 through 3 for administrators progressing from policy management to API-driven automation; Certified Technical Professional for partners and integrators covering architecture, policy design, and deployment; and Certified Sales Professional for channel partners. Passing scores, durations, and validity are not published. Training is delivered through on-demand courses, interactive enablement sessions, and hands-on labs and simulations. The platform beneath is the Singularity Platform, spanning Singularity Endpoint for autonomous endpoint protection combining EPP and EDR, Singularity Cloud for cloud workload security, Singularity Identity for identity threat detection, Singularity XDR for extended detection and response, the Singularity Data Lake and AI SIEM for log analytics, Purple AI as a generative-AI security analyst, and RemoteOps and Ranger, unified by behavioral AI, Storyline autonomous correlation, and one-click remediation with rollback.](../../../diagrams/volume-151-sentinelone-certifications/chapter-01-university-program.svg)

*Figure 1-1. Role-based certifications with Credly badges over the autonomous Singularity platform.*

## Learning Objectives

- Describe the SentinelOne University program — its role-based certifications and Credly badges.
- Distinguish the certification tracks: SIREN, THP, Administrator, and partner credentials.
- Place the Singularity platform and its signature autonomous, AI-driven model.
- Recognize SentinelOne's position in the endpoint/XDR security landscape.

> **Defensive framing.** This volume is about *defending* endpoints and responding to threats — detection, autonomous response, forensics, and recovery. The mechanisms (behavioral AI, correlation, rollback) are the tools a SOC and incident-response team use to protect an organization. Nothing here is about conducting attacks.

## What SentinelOne is

SentinelOne is a leader in **autonomous endpoint and extended security** — the **Singularity Platform** protects endpoints, cloud workloads, identities, and more, using **behavioral AI** that runs *on the agent* to detect and **autonomously respond** to threats at machine speed. Where [CrowdStrike (L)](../../volume-050-crowdstrike-certifications/README.md) pioneered cloud-delivered EDR, SentinelOne's distinctive pitch is **autonomy on the agent**: the endpoint itself detects, correlates ([Storyline, Chapter 3](03-storyline-autonomous-correlation.md)), responds, and can **roll back** damage — even offline, without waiting on a human analyst or a cloud round-trip.

## The certification program

**SentinelOne University** delivers **role-based** learning paths — on-demand courses, interactive sessions, and hands-on labs and simulations — culminating in certifications that issue **Credly digital badges**. The program maps to the jobs on a security team:

| Certification | For | Notes |
|:---|:---|:---|
| **SIREN** (Incident Response Engineer) | IR analysts, threat hunters, SOC engineers | The flagship practical cert; ~**45 hours** of training before the exam |
| **THP** (Threat Hunting Professional) | Advanced analysts | Attack analysis, anomaly detection, SIEM/SOAR |
| **Administrator (Levels 1–3)** | Administrators, support | Policy management → API-driven automation |
| **CTP** (Certified Technical Professional) | Partners, integrators | Architecture, policy design, deployment |
| **CSP** (Certified Sales Professional) | Channel, resellers | Positioning, value, segmentation |

**SIREN is the anchor** — a practical, simulation-heavy credential validating that you can *actually respond to incidents* on the Singularity platform, not just recall facts. The ~45-hour training requirement signals its depth. Exams combine **multiple choice with scenario-based simulations**.

## What is published

SentinelOne publishes the program, the role tracks, and the Credly-badge model, and the ~45-hour training expectation for SIREN.

> **The published-versus-portal split:** exam **passing scores, exact durations, and validity periods are not publicly published** — they sit behind SentinelOne University. This volume asserts the program structure and the SIREN training expectation, and points at the University portal for per-exam mechanics. The certifications are **hands-on and simulation-based**, reflecting a platform whose value is *doing* incident response, not memorizing it.

## The Singularity platform

Every certification sits on the **Singularity Platform**:

| Module | Secures |
|:---|:---|
| **Singularity Endpoint** | Endpoints — EPP + EDR, autonomous ([Chapter 2](02-autonomous-endpoint-protection.md)) |
| **Singularity Cloud** | Cloud workloads (CWPP/CNAPP) |
| **Singularity Identity** | Identity threats + deception |
| **Singularity XDR** | Extended detection across surfaces ([Chapter 6](06-singularity-xdr-and-the-data-lake.md)) |
| **Singularity Data Lake / AI SIEM** | Log analytics at scale |
| **Purple AI** | GenAI security analyst ([Chapter 7](07-purple-ai-and-the-ai-soc.md)) |

Three signatures unify them: **behavioral AI** (detect by behavior, not signatures), **Storyline** (autonomous correlation into an attack narrative), and **one-click remediation with rollback** (undo the damage). The lab reads the program and the platform.

## Hands-On Lab

The labs in this volume model endpoint-security concepts in Python at no cost — SentinelOne is enterprise software, so the labs model the *decisions and disciplines* the certifications test (behavioral detection, correlation, response, rollback). SentinelOne offers **free trials** of Singularity.

### Lab 1.1 — Read the role-based program

**Objective:** Place a certification by role and what it validates.

```bash
python3 - <<'EOF'
CERTS = [
  # cert,          role,                              validates,                     note
  ("SIREN",        "IR analyst / threat hunter / SOC","respond to incidents (hands-on)","~45h training; MC + simulations"),
  ("THP",          "advanced analyst",                "threat hunting, anomaly, SIEM/SOAR","advanced specialization"),
  ("Administrator 1-3","admin / support",             "deploy, policy, API automation","3-tier progression"),
  ("CTP",          "partner / integrator",            "architecture, policy, deployment","technical partner"),
  ("CSP",          "channel / reseller",              "positioning, value",           "sales"),
]
print(f"{'cert':18}{'role':34}validates")
for cert, role, val, note in CERTS:
    print(f"{cert:18}{role:34}{val}")
    print(f"{'':18}{'':34}  ({note})")
print("\nHow to read it — ROLE-BASED, issuing Credly badges:")
print("  - SIREN is the ANCHOR: a practical, SIMULATION-heavy Incident Response")
print("    Engineer cert (~45h training). It validates you can DO IR on Singularity,")
print("    not recall facts — exams are MC + scenario SIMULATIONS.")
print("  - THP goes deeper on threat hunting; ADMINISTRATOR 1-3 is the ops/deploy")
print("    ladder; CTP/CSP are partner tracks.")
print("  - pick the cert for your SEAT (responder -> SIREN/THP, admin -> ADM 1-3).")
print("\nPassing scores/durations are portal-gated (SentinelOne University); the volume")
print("asserts the STRUCTURE + the SIREN training expectation, not unpublished numbers.")
print("The simulation-heavy format fits the platform's whole pitch: security is DOING")
print("(detect, correlate, respond, roll back), so the certs make you do it.")
EOF
```

**Expected result:** The certifications placed by role — SIREN (incident response), THP (threat hunting), Administrator 1–3 (ops), and CTP/CSP (partner) — with SIREN the simulation-heavy anchor. The role-based lesson is to certify for your seat, with SIREN validating hands-on incident response (not recall) via scenario simulations, and per-exam mechanics identified as portal-gated.

**Negative test:** Treating SIREN as a multiple-choice knowledge exam. It requires ~45 hours of training and is simulation-heavy — it validates *doing* incident response on the platform, which a question bank cannot cram.

**Cleanup:** None.

### Lab 1.2 — The three signatures of the platform

**Objective:** See what makes Singularity "autonomous."

```bash
python3 - <<'EOF'
SIGNATURES = [
  # signature,             is,                                        vs the old way
  ("behavioral AI",        "detect by BEHAVIOR, on the agent",        "signatures (known-bad hashes only)"),
  ("autonomous response",  "the agent stops the threat at machine speed","wait for a human analyst / cloud"),
  ("Storyline",            "auto-CORRELATE events into one attack story","manually stitch scattered alerts"),
  ("rollback",             "UNDO the damage (restore encrypted files)", "reimage the machine from scratch"),
]
print(f"{'signature':22}{'what it does':46}vs the old way")
for sig, does, old in SIGNATURES:
    print(f"{sig:22}{does:46}{old}")
print("\nThe unifying idea: AUTONOMY. The AGENT — not a cloud, not a human — detects")
print("(behavioral AI, so it catches NOVEL threats signatures miss), responds at")
print("MACHINE SPEED (stops the attack before a human could even read the alert),")
print("CORRELATES the mess into one readable story (Storyline), and can ROLL BACK the")
print("damage. And because it runs ON the agent, it works even OFFLINE — no cloud")
print("round-trip required.")
print("\nWhy it matters for the certs: SIREN/THP teach you to work WITH an autonomous")
print("system — validate its decisions, hunt beyond them, tune policy — not to do")
print("everything by hand. That's the modern SOC: humans supervising machine-speed")
print("defense, not racing it. (CrowdStrike L is the EDR peer; SentinelOne's edge is")
print("on-agent autonomy + Storyline + rollback.)")
EOF
```

**Expected result:** The three platform signatures — behavioral AI, autonomous machine-speed response, Storyline correlation, and rollback — contrasted with the old signature-based, human-paced, manual-stitching, reimage approach. The autonomy lesson is that the agent itself detects, responds, correlates, and recovers (even offline), and the certifications teach analysts to supervise and extend that machine-speed defense rather than race it by hand.

**Negative test:** Expecting a signature-based antivirus model. Signatures only catch known-bad hashes and miss novel threats; SentinelOne's behavioral AI detects by behavior and responds autonomously, which is what the certifications teach you to operate.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] The SentinelOne University program understood as role-based, simulation-heavy, and Credly-badged.
- [ ] The certification tracks (SIREN, THP, Administrator 1–3, CTP, CSP) matched to security-team roles.
- [ ] The Singularity platform and its three signatures (behavioral AI, Storyline, rollback) placed.
- [ ] Per-exam mechanics identified as portal-gated; the SIREN ~45-hour, simulation-based nature understood.
