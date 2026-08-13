# Chapter 01: The Qualys Certification Program

## Learning Objectives

- Explain Qualys and its cloud-based security platform.
- Describe the Qualys Certified Specialist paths.
- Understand the free training model and VMDR flagship.
- Map credentials to products and plan a path.
- Verify current program facts from the authoritative source.

## Theory and Architecture

**Qualys** is a pioneer of **cloud-based vulnerability management, compliance, and exposure
management** — its entire platform runs as SaaS on the **Qualys Cloud Platform**, with lightweight
**sensors** (Cloud Agents, scanner appliances, passive network sensors, cloud connectors, and an API)
feeding a single console. Its certification program — the **Qualys Certified Specialist** series — is
**free** (self-paced or instructor-led, with hands-on labs), lowering the barrier to skilled
practitioners. Certifications are organized into **paths**: a **Vulnerability Management** path
(VM Foundations, the flagship **VMDR — Vulnerability Management, Detection and Response**, **CSAM —
CyberSecurity Asset Management**, **Enterprise TruRisk Management (ETM)**, scanning and reporting
strategies, and **TruRisk Eliminate**); a **Compliance** path (Policy Compliance, Policy Audit); a
**PCI Compliance** path; an **Endpoint Detection and Response (EDR)** path; and additional certified
courses (**Administration**, **QFlow**, **Custom Assessment and Remediation (CAR)**, **QQL — Qualys
Query Language**, **API Fundamentals**, **Cloud Agent**, **Container Security**, **File Integrity
Monitoring**, **TotalAppSec**, **TotalCloud**). The unifying theme is **risk-based** security via the
**TruRisk** score. Because vulnerability and compliance management exist to **find and fix weaknesses**,
this entire volume is defensive.

> **Scope.** Vulnerability, compliance, and exposure management is a defensive discipline. Every lab
> is **authorized administration** — scanning, assessing compliance, prioritizing, and remediating on
> systems you are authorized to assess — never an attack. Scan only assets you own or are authorized
> to scan.

## Design Considerations

Choose paths by role: **VMDR/CSAM** for vulnerability teams, **Policy/PCI Compliance** for GRC,
**EDR** for detection/response, **TotalCloud** for cloud. The training is **free** — a low-risk way to
build and validate skills. Learn **QQL** early (it powers search across the platform). Verify current
courses on qualys.com — the platform evolves under **Enterprise TruRisk**.

## Implementation and Automation

Confirm your practice toolset (used throughout the volume):

```bash
command -v python3 >/dev/null && echo "python3: ok" || echo "python3: install for labs"
echo "Sign up for a free Qualys Community Edition / trial and use authorized lab targets only"
```

## Validation and Troubleshooting

The verified program facts (qualys.com/training, 28 July 2026):

```text
Qualys Cloud Platform (SaaS) + sensors: Cloud Agents, scanner appliances, passive sensors, cloud connectors, API. Training/certification FREE.
Paths: Vulnerability Management (VMDR, CSAM, ETM, TruRisk Eliminate), Compliance (Policy Compliance), PCI, EDR; + QFlow/CAR/QQL/Cloud Agent/Container/FIM/TotalAppSec/TotalCloud.
Flagship: VMDR. Risk-based via TruRisk score. Certified Specialist series.
```

Common pitfalls: treating Qualys as a scanner only (it's a **cloud platform** spanning VM, compliance,
cloud, EDR); and ignoring **QQL** (it's how you find anything).

## Security and Best Practices

Learn the **current** paths and platform on qualys.com, take advantage of the **free** training,
learn **QQL** early, and scan only **authorized** targets. All work is defensive.

## References and Knowledge Checks

- qualys.com/training and the Qualys Certification Center: the paths and courses.
- qualys.com/documentation and the Qualys Cloud Platform docs.

**Knowledge checks**

1. What is distinctive about Qualys's delivery model?
2. Name Qualys's flagship certification.
3. Is Qualys certification training free?

## Hands-On Lab

Orientation walkthroughs. **Shared prerequisites for Labs 1.1–1.3** — a workstation with `python3`,
in a lab. **Cost:** none (Qualys training is free).

### Lab 1.1 — Map the certification paths

**Objective:** Learn the paths.

```python
python3 - <<'PY'
paths={"Vulnerability Management":["VMDR","CSAM","ETM","TruRisk Eliminate"],
       "Compliance":["Policy Compliance","Policy Audit"],"PCI":["PCI Compliance"],
       "EDR":["EDR"],"Additional":["QFlow","CAR","QQL","Cloud Agent","Container Security","TotalAppSec","TotalCloud"]}
for p,courses in paths.items(): print(f"{p:26}: {', '.join(courses)}")
PY
```

**Expected result:** the Qualys **paths and courses** — the map this volume follows.

**Negative test:** assume one Qualys cert covers all; each **path/course** targets a product area —
choose by role.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 1.2 — Understand the platform and sensors

**Objective:** Learn how data is collected.

```python
python3 - <<'PY'
sensors={"Cloud Agent":"lightweight always-on host sensor (continuous, no scan window)",
         "Scanner appliance":"network scanner (reachable targets)",
         "Passive sensor":"network traffic discovery (finds unmanaged assets)",
         "Cloud connector":"syncs cloud assets (AWS/Azure/GCP)","API":"automation + QQL search"}
for s,role in sensors.items(): print(f"{s:18}: {role}")
PY
```

**Expected result:** the **sensor types** feeding the Qualys Cloud Platform — coverage building
blocks.

**Negative test:** rely on network scans alone; **Cloud Agents** give continuous, off-network
coverage — use them.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 1.3 — Plan a certification path

**Objective:** Sequence credentials for a role.

```python
python3 - <<'PY'
plans={"Vuln analyst":"VMDR -> CSAM -> TruRisk (ETM)","Compliance/GRC":"Policy Compliance -> PCI",
       "Detection/response":"EDR","Cloud security":"TotalCloud","Automation":"QQL -> QFlow -> CAR -> API"}
for role,path in plans.items(): print(f"{role:20}: {path}")
PY
```

**Expected result:** role-to-path sequences — the certifications this volume follows.

**Negative test:** skip **VMDR/QQL** foundations and jump to automation; you need the platform basics —
build up.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Qualys certifies cloud-platform security practitioners across free Certified Specialist paths — VMDR,
CSAM, TruRisk/ETM, Policy/PCI Compliance, EDR, TotalCloud, and more — all risk-based via the TruRisk
score, taught here as defensive vulnerability, compliance, and exposure management.

- [ ] I can explain Qualys's cloud-platform model.
- [ ] I can name the flagship VMDR certification.
- [ ] I can describe the sensors and free training.
- [ ] I can plan a certification path.
- [ ] I completed Labs 1.1–1.3 including each negative test.
