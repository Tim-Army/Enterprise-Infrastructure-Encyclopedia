# Chapter 03: CEH — Certified Ethical Hacker

## Learning Objectives

- Understand the CEH v13 ethical-hacking methodology and its 20 modules.
- Apply reconnaissance, scanning, and enumeration — authorized and paired with countermeasures.
- Analyze vulnerabilities and understand system-hacking defenses.
- Frame every technique as authorized assessment plus its defensive countermeasure.
- Complete a walkthrough for each CEH phase — defensively.

## Theory and Architecture

The **Certified Ethical Hacker (CEH) v13** validates **authorized** security assessment using the
same methodology adversaries use — so defenders can find and fix weaknesses first. Its 20 modules
follow the assessment lifecycle: **reconnaissance/footprinting**, **scanning networks**,
**enumeration**, **vulnerability analysis**, **system hacking**, and specialized topics (malware,
sniffing, social engineering, web/app, wireless, mobile, IoT/OT, cloud, cryptography). CEH is
explicitly **ethical**: every technique is performed **only with authorization and scope**, and the
professional value is knowing the technique **and its countermeasure**. The knowledge exam (4 hours,
125 MCQ) covers the methodology; the practical (6 hours, 20 iLabs challenges) proves hands-on skill
for **CEH Master**. In this volume, each CEH phase is taught as **authorized methodology paired with
the defensive control** — recon paired with attack-surface reduction, scanning paired with
firewalling, and so on — using **safe, local** commands against systems you own. No operational
attack payload appears.

> **Scope.** Every technique here is **authorized and educational**. The gate is written
> authorization and a defined scope; commands are safe and local (localhost / your own lab); the
> emphasis is the **countermeasure**. CEH is ethical hacking — never an attack on systems you do not
> own.

## Design Considerations

Always **authorize and scope** first. For every offensive technique, learn the **countermeasure** —
that is what CEH tests and what defenders need. Minimize impact; prefer passive/low-impact steps.
Document findings for remediation. Map techniques to **MITRE ATT&CK** so defenders can build
detections.

## Implementation and Automation

The labs walk recon, scanning, enumeration, and vulnerability analysis — each with its countermeasure.

## Validation and Troubleshooting

Confirm the CEH methodology map:

```text
CEH v13 lifecycle: recon/footprint -> scan -> enumerate -> vuln analysis -> (system hacking) + specialized modules.
Each technique paired with its COUNTERMEASURE. Authorized + scoped only. Knowledge exam (125 MCQ) + practical (iLabs) -> CEH Master.
```

Common pitfalls: learning techniques without **countermeasures** (half the value); and acting
outside **authorization/scope** (unethical and illegal).

## Security and Best Practices

Authorize and scope, pair every technique with its **countermeasure**, minimize impact, and report
for remediation. Practice only on **owned lab systems**. CEH is authorized, defensive-purpose work.

## Hands-On Lab

Authorized ethical-hacking walkthroughs. **Shared prerequisites** — Linux with `python3`, `nmap`,
and a target **you own** (`127.0.0.1`), in a lab. **Cost:** none.

### Lab 3.1 — Recon with countermeasure

**Objective:** Map attack surface, then reduce it.

```python
python3 - <<'PY'
# Passive "footprint" of what YOUR OWN host exposes (authorized self-assessment)
exposed={"open_ports":[22,80,443],"banner":"OpenSSH_9.6","dns_records":["www","vpn","dev"]}
print("attack surface:", exposed)
print("countermeasure: close unused ports, suppress banners, remove stale DNS (dev), least exposure")
PY
```

**Expected result:** the host's **attack surface** plus the **countermeasure** (reduce exposure) —
CEH recon done defensively.

**Negative test:** footprint a third party "to practice"; recon is **authorized-only** — assess only
what you own.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.2 — Scan a host you own, then firewall

**Objective:** Enumerate open ports and mitigate.

```bash
nmap -sT -F 127.0.0.1 2>/dev/null | sed -n '1,12p' \
  || python3 -c "import socket;print('22/tcp', 'open' if socket.socket().connect_ex(('127.0.0.1',22))==0 else 'closed')"
echo "countermeasure: host firewall default-deny; expose only required services from known sources"
```

**Expected result:** open ports on **your own** host, plus the **firewall countermeasure** — CEH
scanning done defensively.

**Negative test:** scan an address outside your authorization/scope; that is prohibited — scan only
**in-scope, owned** systems.

**Rollback:** none (read-only scan of localhost).

### Lab 3.3 — Enumeration with hardening

**Objective:** Identify service detail, then reduce it.

```bash
# Authorized banner check on your own service:
python3 - <<'PY'
banner="Server: nginx/1.25.3 (Ubuntu)"
print("enumerated:", banner)
print("countermeasure: set server_tokens off / suppress version banners -> less info to an attacker")
PY
```

**Expected result:** the enumerated service **banner** and the **hardening countermeasure** — CEH
enumeration done defensively.

**Negative test:** rely on a hidden banner for security; **suppress** it and patch — obscurity is not
a control.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.4 — Vulnerability analysis and prioritization

**Objective:** Turn findings into fixes.

```python
python3 - <<'PY'
vulns=[{"id":"CVE-lab-1","cvss":9.8,"fix":"patch to current"},
       {"id":"weak-cipher","cvss":7.4,"fix":"disable TLS<1.2"},
       {"id":"info-leak","cvss":3.1,"fix":"suppress banner"}]
for v in sorted(vulns,key=lambda x:-x["cvss"]):
    print(f"CVSS {v['cvss']:<4} {v['id']:14} -> {v['fix']}")
print("CEH vuln analysis: prioritize by severity, drive remediation")
PY
```

**Expected result:** vulnerabilities ranked by **CVSS** with fixes — CEH vulnerability analysis
feeding defense.

**Negative test:** stop at "found vulnerabilities"; CEH's value is **prioritized remediation** —
finish with fixes.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.5 — Map techniques to ATT&CK for defenders

**Objective:** Make offensive knowledge defensible.

```python
python3 - <<'PY'
mapping={"Footprinting":"T1595 Active Scanning -> detect: external scan alerting",
         "Enumeration":"T1046 Network Service Discovery -> detect: internal scan analytics",
         "System hacking":"T1078 Valid Accounts -> detect: anomalous login + MFA"}
for tech,defense in mapping.items(): print(f"{tech:14}: {defense}")
print("CEH knowledge -> ATT&CK -> detections defenders can build")
PY
```

**Expected result:** CEH techniques mapped to **ATT&CK** with detections — offensive knowledge turned
defensive.

**Negative test:** keep offensive knowledge separate from defense; CEH's purpose is **better
defense** — map it to detections.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

CEH v13 teaches the authorized ethical-hacking methodology across 20 modules — recon, scanning,
enumeration, vulnerability analysis, and beyond — always gated on authorization and paired with
countermeasures, with a practical exam earning CEH Master.

- [ ] I can perform recon and its countermeasure (authorized).
- [ ] I can scan a host I own and firewall it.
- [ ] I can enumerate and harden a service.
- [ ] I can prioritize vulnerabilities and map techniques to ATT&CK.
- [ ] I completed Labs 3.1–3.5 including each negative test.
