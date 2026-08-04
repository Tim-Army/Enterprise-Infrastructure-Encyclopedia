# Chapter 01: The Netskope Certification Program and SASE/SSE Foundations

![The Netskope certification program: the free, vendor-agnostic SASE Accreditation (on-demand SASE architecture course + 45-minute exam) as the on-ramp, then the NCCSA (Netskope Certified Cloud Security Administrator, exam NSK101, Pearson VUE) on the Netskope One Administrator course, and the NCCSI (Netskope Certified Cloud Security Integrator) on the Netskope One Professional course. All teach the Netskope One SASE platform — SSE (CASB, SWG, ZTNA, DLP) plus SD-WAN — delivered over the NewEdge network.](../../../diagrams/volume-127-netskope-certifications/chapter-01-certification-program.svg)

*Figure 1-1. The Netskope program: a free vendor-agnostic SASE Accreditation, then the platform certifications NCCSA (administer) and NCCSI (integrate) on Netskope One — the converged SASE/SSE platform.*

## Learning Objectives

- Describe the Netskope certification program: the SASE Accreditation, NCCSA, and NCCSI.
- Understand SASE and SSE — the architectural frameworks the certifications teach.
- Know the Netskope One platform's building blocks: CASB, SWG, ZTNA, DLP, and the NewEdge network.
- Know the exam logistics and set up a free study environment.

## What Netskope certifies

Netskope is a **SASE** (Secure Access Service Edge) vendor. Its **Netskope One** platform converges networking and security in the cloud: instead of backhauling traffic to a data-center stack, users and sites connect to Netskope's cloud, which applies web filtering, cloud-app control, data protection, and zero-trust access to private apps — close to the user, at the edge.

The certifications validate both the **SASE/SSE concepts** and the **Netskope platform** that implements them.

## The certifications

Verified on netskope.com, 3 August 2026:

| Credential | Exam / format | Prerequisite | Focus |
|:---|:---|:---|:---|
| **SASE Accreditation** | On-demand course + optional exam (45 min, 80% pass, 2 attempts); **FREE** (limited time) | Security/network/architecture basics | Vendor-agnostic SASE architecture |
| **NCCSA** — Certified Cloud Security Administrator | **NSK101** (replaced NSK100), Pearson VUE, 70 questions, ~2 hours, **70% pass**, valid **2 years** | Netskope One Administrator course recommended | Configure, monitor, and troubleshoot the Netskope platform |
| **NCCSI** — Certified Cloud Security Integrator | **NSK200**-series, Pearson VUE | NCCSA-level knowledge; Netskope One Professional course | Integrate Netskope into an enterprise — SSO/SAML, API, advanced DLP, IaaS/SSPM |

The ladder: **SASE Accreditation** (free, vendor-agnostic on-ramp) → **NCCSA** (administer the platform) → **NCCSI** (integrate it deeply). Exam codes churn (NSK100 → NSK101); re-verify on netskope.com before booking.

## SASE and SSE in one page

| Framework | What it is |
|:---|:---|
| **SASE** | Secure Access Service Edge — converges networking (SD-WAN) and security (SSE) into one cloud-delivered service at the edge |
| **SSE** | Security Service Edge — the security half of SASE: **CASB + SWG + ZTNA** (plus DLP, cloud firewall, threat protection) |
| **CASB** | Cloud Access Security Broker — visibility and control over cloud app (SaaS) usage |
| **SWG** | Secure Web Gateway — web filtering, SSL inspection, threat protection for internet traffic |
| **ZTNA** | Zero Trust Network Access — identity-based access to private apps without a network-level VPN |
| **DLP** | Data Loss Prevention — detect and control sensitive data in motion |

The mental model: **SASE = SD-WAN (networking) + SSE (security)**, delivered from the cloud edge, with **Zero Trust** as the access principle throughout.

## The Netskope One platform

| Component | Role |
|:---|:---|
| **NewEdge** | Netskope's private security cloud/network — the edge that traffic steers to |
| **Steering** | How traffic reaches Netskope: the Netskope Client (agent), or steering by proxy/tunnel/API |
| **Inline (proxy)** | Real-time inspection of web/cloud traffic passing through Netskope |
| **API-enabled protection** | Out-of-band scanning of SaaS via vendor APIs (data at rest) |
| **Policy engine** | One policy across web, cloud apps, private apps, and data |

## Hands-On Lab

The concepts model on **free primitives** (a forward proxy, regex DLP, a reverse-broker for ZTNA); the Netskope tenant is design-level. **Cost:** none.

### Lab 1.1 — Register for the free on-ramps

**Objective:** Enroll in the free SASE Accreditation and map the ladder.

```bash
cat <<'EOF'
SASE Accreditation: netskope.com/sase-accreditation  (FREE for a limited time; on-demand; optional exam)
  agenda: SASE origin -> architecture -> Zero Trust -> SD-WAN -> SSE -> org dynamics -> deployment
NCCSA: NSK101 (Pearson VUE, 70Q/~2hr/70%/valid 2yr) — Netskope One Administrator course
NCCSI: NSK200-series — Netskope One Professional course (integration depth)
EOF
```

**Expected result:** The ladder mapped — free vendor-agnostic accreditation first, then NCCSA to administer, NCCSI to integrate. The SASE Accreditation is genuinely vendor-agnostic (it teaches the framework, not just Netskope), which makes it a useful first step regardless of vendor.

**Negative test:** Registering for NSK100 — retired; the current NCCSA exam is NSK101. Exam-code churn is why re-verification precedes booking.

**Cleanup:** None.

### Lab 1.2 — Build the study lab

**Objective:** Stand up the free primitives the volume uses to model SSE.

```bash
sudo apt-get update -qq && sudo apt-get install -y squid nginx nftables python3 netcat-openbsd 2>/dev/null || \
  echo "install a forward proxy (squid), nginx, nftables, python3"
command -v squid && echo "squid models the SWG/inline proxy"
python3 -c "import re; print('regex available for DLP pattern modeling')"
echo "lab ready: squid=SWG/steering, python regex=DLP, namespaces/nginx=ZTNA broker"
```

**Expected result:** A forward proxy and scripting present — this volume models SWG steering, DLP detection, and ZTNA brokering on one host, so the SSE concepts are concrete without a Netskope tenant.

**Negative test:** Expecting the labs to *be* Netskope — they model the **SSE concepts** the exams test; the real Netskope One console appears at design level.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] The three credentials (SASE Accreditation, NCCSA, NCCSI) and their sequence understood.
- [ ] SASE = SD-WAN + SSE, and SSE = CASB + SWG + ZTNA (+ DLP), internalized.
- [ ] The Netskope One platform (NewEdge, steering, inline vs API) mapped.
- [ ] The free study lab stood up; exam-code churn (NSK100→NSK101) noted.
