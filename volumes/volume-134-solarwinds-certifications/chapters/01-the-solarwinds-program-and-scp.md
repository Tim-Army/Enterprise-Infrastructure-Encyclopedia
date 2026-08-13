# Chapter 01: The SolarWinds Program and the SCP Credential

![The SolarWinds Certified Professional program: a single SCP credential earned per product-specific exam, in three steps — register with SolarWinds, study using that exam's preparation guide (plus virtual and on-demand training through the Customer Portal for customers with a product under active maintenance), and schedule through PSI Services remote proctoring. The exam fee is US$200, or 60,000 THWACK community points exchanged in the THWACK store for an SCP voucher. Eleven current exams span the rebranded portfolio: SolarWinds Observability SaaS Fundamentals; Observability Self-Hosted Fundamentals, Network Monitoring, Network Management, Architecture and Design, Diagnostics and Troubleshooting, and Federal Fundamentals; Server and Application Monitor; Database Performance Analyzer; Database Management; and Service Desk. Supporting resources are product documentation, virtual classrooms, eLearning videos, and the THWACK community forum.](../../../diagrams/volume-134-solarwinds-certifications/chapter-01-certification-program.svg)

*Figure 1-1. The SCP program: eleven product-specific exams across Observability SaaS and Self-Hosted, delivered by PSI remote proctoring, payable in dollars or THWACK points.*

## Learning Objectives

- Describe the SolarWinds Certified Professional (SCP) program and its three steps.
- Identify the eleven current exams and the Observability SaaS / Self-Hosted split.
- Use the THWACK points route as an alternative to the exam fee.
- Set up a free study environment for the monitoring labs.

## What SolarWinds does

SolarWinds builds IT **monitoring and observability** software: network, server, application, and database monitoring, plus configuration management and service desk. Its historical center of gravity was the **Orion Platform** — the on-premises suite whose Network Performance Monitor (NPM) was for years the default answer to "how do we monitor the network?"

Two things matter about the program's current shape:

1. **The portfolio has been rebranded around "SolarWinds Observability,"** split into **SaaS** and **Self-Hosted** editions. Self-Hosted is the lineage of the on-premises Orion platform.
2. **The certification list follows that rebrand.** If you encounter material selling "SCP-NPM" or "SCP-500," it is describing the **previous** scheme.

## The SCP credential

**SolarWinds Certified Professional (SCP)** is the single credential name; you earn it by passing a **product-specific exam**. There is no tiered ladder — you certify on the product you actually operate.

The program is deliberately simple, described by SolarWinds as **three easy steps**:

| Step | What happens |
|:---|:---|
| **Sign up** | Register with SolarWinds; receive a confirmation email with account and testing-service instructions |
| **Study** | Use that exam's **preparation guide**; customers with a product under **active maintenance** get virtual and on-demand training through the **Customer Portal** |
| **Schedule** | Create a **PSI Services** account and book the exam |

### Delivery

Exams are delivered by **PSI Services** using proprietary **remote proctoring** — "anywhere, anytime testing with integrity." That means an ID check, environment and system requirements, a compatibility check beforehand, and admission rules you should read rather than discover on exam day. Special accommodations are available.

### Who should sit it, and validity

**There are no eligibility prerequisites** — SolarWinds does not gate registration, so you can schedule with PSI as soon as you have registered on the SolarWinds site. What SolarWinds publishes instead is a **recommended profile**, and it is worth measuring yourself against honestly:

| Recommended minimum | Detail |
|:---|:---|
| **One year** in a technical role | Network, systems, applications, or security and compliance management or engineering |
| **Six months** hands-on with SolarWinds products | Day-to-day operational work, not occasional exposure |
| Familiarity with key product technologies | Including **PerfStack**, **NetPath**, and **AppStack** |

The exams are aimed at people who **actively participate in day-to-day operational tasks** supporting their environment — which is the honest test of readiness, since the questions are scenario-shaped rather than definitional.

**Your certification is valid for three years** from its date of issue. SolarWinds frames this as keeping certified professionals current with evolving product features — reasonable given that the portfolio itself was rebranded within that window.

### Cost — and the THWACK route

The exam fee is **US$200**. But there is a second path worth knowing about:

> Members of SolarWinds' user community, **THWACK**, may exchange **60,000 THWACK points** for the exam fee. You select an **SCP Voucher** in the THWACK store, receive a voucher code by email within three business days, and apply it at PSI checkout.

This is unusual among vendor certification programs and genuinely valuable: sustained participation in the community — answering questions, contributing content, testing betas — converts into a free certification attempt. If you are active in THWACK anyway, check your balance before paying.

## The eleven current exams

| Exam | Domain |
|:---|:---|
| **SolarWinds Observability SaaS Fundamentals** | The SaaS observability platform |
| **SolarWinds Observability Self-Hosted Fundamentals** | The self-hosted platform (Orion lineage) |
| **SolarWinds Observability Self-Hosted Network Monitoring** | Network availability and performance |
| **SolarWinds Observability Self-Hosted Network Management** | Configuration and change management |
| **SolarWinds Observability Self-Hosted Architecture & Design** | Deployment design, scaling, high availability |
| **SolarWinds Observability Self-Hosted Diagnostics & Troubleshooting** | Diagnosing the platform itself |
| **SolarWinds Observability Self-Hosted Federal Fundamentals** | The federal/public-sector variant |
| **SolarWinds Server and Application Monitor** | Server and application monitoring (SAM) |
| **SolarWinds Database Performance Analyzer** | Database wait-time performance analysis |
| **SolarWinds Database Management** | Database administration and management |
| **SolarWinds Service Desk** | IT service management |

Two observations worth carrying forward. First, the Self-Hosted family splits into **operational** exams (Fundamentals, Network Monitoring, Network Management) and **specialist** exams (Architecture & Design, Diagnostics & Troubleshooting) — a natural progression from using the platform to designing and debugging it. Second, the **Federal Fundamentals** exam exists because public-sector deployments carry distinct compliance, accreditation, and operational constraints ([Volume LXIII](../../volume-063-public-sector-data-governance/README.md) covers that governance world).

## Study resources

SolarWinds provides: **product documentation**, **virtual classrooms**, **eLearning videos**, and the **THWACK community forum**. Each exam has its own preparation guide, which is the correct starting point.

SolarWinds states plainly that **training from third parties is "not reviewed, monitored, or endorsed"** by them. Take that seriously here: the search results for SolarWinds certification are dominated by braindump and "practice exam" sites, many still selling preparation for the retired exam codes. Use the official preparation guide and the Customer Portal.

## Free study environment

SolarWinds products are commercial, so this volume's labs model the **monitoring and observability disciplines** — polling and collection, availability math, interface utilization, configuration drift, wait-time analysis, dependency-aware alerting, and capacity forecasting — in free Python. Those concepts are what the exams test and what transfer to any monitoring platform.

## Hands-On Lab

### Lab 1.1 — Set up the study environment

**Objective:** Confirm the free toolchain.

```bash
python3 --version
mkdir -p ~/solarwinds-study && cd ~/solarwinds-study
python3 - <<'EOF'
print("Monitoring/observability study environment ready.")
print("Labs model: polling & collection, availability, interface utilization,")
print("config drift, wait-time analysis, alert dependencies, capacity forecasting.")
print("No SolarWinds license required.")
EOF
```

**Expected result:** Python reports a version and the message prints. Every lab uses the standard library only.

**Negative test:** Assuming you need an Orion/Observability deployment to study — the underlying math (availability percentages, utilization, baselines, wait-time attribution) is vendor-independent and is what the exams actually probe.

**Rollback:** `rm -rf ~/solarwinds-study` when done.

### Lab 1.2 — Choose your exam and check the THWACK route

**Objective:** Pick the right exam and see whether points cover the fee.

```bash
python3 - <<'EOF'
EXAMS = {
  "monitor the network (self-hosted)": "Observability Self-Hosted Network Monitoring",
  "manage configs/changes":            "Observability Self-Hosted Network Management",
  "design/scale the deployment":       "Observability Self-Hosted Architecture & Design",
  "troubleshoot the platform":         "Observability Self-Hosted Diagnostics & Troubleshooting",
  "run it as SaaS":                    "Observability SaaS Fundamentals",
  "public sector / federal":           "Observability Self-Hosted Federal Fundamentals",
  "servers and applications":          "Server and Application Monitor",
  "database performance":              "Database Performance Analyzer",
  "database administration":           "Database Management",
  "ITSM / service desk":               "Service Desk",
}
for role, exam in EXAMS.items():
    print(f"{role:36} -> SCP: {exam}")

FEE_USD, POINTS_REQUIRED = 200, 60000
for balance in (72000, 45000, 0):
    if balance >= POINTS_REQUIRED:
        print(f"\nTHWACK balance {balance:>6}: redeem an SCP Voucher — exam costs you $0 "
              f"({balance - POINTS_REQUIRED} points left over)")
    else:
        print(f"\nTHWACK balance {balance:>6}: {POINTS_REQUIRED - balance} points short — pay US${FEE_USD} "
              f"or keep contributing to THWACK")
EOF
```

**Expected result:** Each role maps to one exam, and the points check shows that a 72,000-point balance covers the fee outright while smaller balances leave a gap. The mapping is the important half: because SCP is product-specific rather than tiered, choosing the exam is a question of **what you operate**, not what level you are.

**Negative test:** Booking "the SolarWinds exam" generically — there are eleven, and the Self-Hosted and SaaS platforms differ enough that preparing for the wrong one wastes the attempt.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] The SCP credential and its three steps (sign up, study, schedule) described.
- [ ] The eleven exams identified, with the Observability SaaS vs Self-Hosted split understood.
- [ ] PSI remote proctoring requirements noted.
- [ ] The THWACK 60,000-point alternative to the $200 fee recorded.
- [ ] Free Python study environment ready.
