# Chapter 07: Certified Cybersecurity Operations Analyst (CCOA)

## Learning Objectives

- Explain what CCOA certifies and its hands-on, hybrid exam format.
- List the five CCOA domains.
- Apply SOC-analyst skills: technology, principles, adversary TTPs, detection/response, and asset protection.
- Practice hands-on analysis (logs, HTTP) as the exam does.
- Complete a per-domain walkthrough for each CCOA domain.

## Theory and Architecture

The **Certified Cybersecurity Operations Analyst (CCOA)** is ISACA's newer,
**hands-on** credential for **SOC analysts** and technical defenders. Unlike
ISACA's classic knowledge exams, CCOA uses a **hybrid** format — multiple-choice
plus **performance-based lab questions** — in a **four-hour** exam with real
hands-on tasks (for example, HTTP and log analysis). Five domains:

| # | Domain |
|---|--------|
| 1 | Technology Essentials |
| 2 | Cybersecurity Principles and Risks |
| 3 | Adversarial Tactics, Techniques and Procedures |
| 4 | Incident Detection and Response |
| 5 | Securing Assets |

CCOA is ISACA's answer to the demand for **technical, job-ready** defenders,
complementing the audit/governance certifications with an operations credential.

## Design Considerations

CCOA rewards **doing**: analyzing traffic and logs, recognizing adversary
behavior (aligned to MITRE ATT&CK), and detecting and responding to incidents.
Prepare by practicing in a lab — packet/HTTP analysis, log triage, and detection
— not just reading. CCOA sits alongside the OffSec defensive track (OSDA/OSIR/
OSTH, Volume XLIII) and the encyclopedia's observability and cybersecurity
volumes (X, XI).

## Implementation and Automation

Because CCOA is hands-on, the labs below use **real commands** on your own
system: reading system facts (D1), a CIA/risk control (D2), mapping observed
behavior to ATT&CK (D3), detecting an event in logs (D4), and hardening an asset
(D5).

## Validation and Troubleshooting

Confirm the CCOA blueprint before studying:

```text
isaca.org > Credentialing > CCOA:
  - five domains; hybrid exam (multiple-choice + performance-based labs), 4 hours
  - hands-on lab components (e.g., HTTP/log analysis)
```

Common pitfalls: preparing for CCOA like a **knowledge** exam (it has **labs**);
and analyzing alerts without mapping to **TTPs** — behavior, not just indicators,
drives detection.

## Security and Best Practices

Work the analyst loop: **collect** telemetry, **detect** with tuned rules mapped
to **MITRE ATT&CK**, **triage** and **respond**, and feed findings back into
detections. Preserve evidence and document. Harden assets to shrink the attack
surface you must monitor. Renew via CPE.

## References and Knowledge Checks

- isaca.org: *CCOA* credential page and study resources; MITRE ATT&CK.

**Knowledge checks**

1. How does CCOA's exam format differ from CISA/CISM?
2. Why map detections to MITRE ATT&CK rather than only to indicators?
3. What is the analyst loop from collection to feedback?

## Hands-On Lab

Per-topic walkthroughs — **one lab for every CCOA domain**, on your own system.

**Shared prerequisites** — a Linux shell with `python3`, `ss`, `journalctl`/
`last`, and `curl`. **Cost:** none.

### Lab 7.1 — CCOA: Technology Essentials

**Objective:** Read the host and network fundamentals an analyst needs.

```bash
ip -brief addr | awk '{print $1,$3}'
ss -tuln | awk 'NR==1 || /LISTEN|UNCONN/' | head
```

**Expected result:** the host's addresses and listening services — the technology
fundamentals (Domain 1) an analyst reasons from.

**Negative test:** analyze alerts without knowing the environment's normal;
**baseline** the technology first.

**Cleanup:** none.

### Lab 7.2 — CCOA: Cybersecurity Principles and Risks

**Objective:** Apply CIA and a control to a risk.

```bash
python3 - <<'PY'
risks = {"Data tampering":"integrity -> hashing/signing + change monitoring",
         "Eavesdropping":"confidentiality -> TLS + encryption at rest",
         "Outage":"availability -> redundancy + backups"}
for r,c in risks.items(): print(f"{r:16} -> {c}")
PY
```

**Expected result:** risks mapped to CIA and controls — the principles/risk
foundation of Domain 2.

**Negative test:** treat all incidents as confidentiality breaches; classify by
which CIA property is threatened to pick the right control.

**Cleanup:** none.

### Lab 7.3 — CCOA: Adversarial Tactics, Techniques and Procedures

**Objective:** Map an observation to a MITRE ATT&CK technique.

```bash
python3 - <<'PY'
obs = {"New scheduled task by non-admin":"T1053 Scheduled Task/Job (Persistence)",
       "Many failed logins then success":"T1110 Brute Force (Credential Access)",
       "PowerShell downloading a file":"T1059.001 PowerShell (Execution)"}
for o,t in obs.items(): print(f"{o:34} -> {t}")
PY
```

**Expected result:** observations mapped to ATT&CK techniques — the TTP analysis
of Domain 3.

**Negative test:** track only file-hash indicators; **TTPs** catch variants that
change hashes — analyze behavior.

**Cleanup:** none.

### Lab 7.4 — CCOA: Incident Detection and Response

**Objective:** Detect a brute-force pattern in authentication logs.

```bash
journalctl _COMM=sshd --no-pager 2>/dev/null | grep -c 'Failed password' || echo 0
echo "Detection: >10 failures from one source in 5 min -> alert; respond: block + investigate."
```

**Expected result:** a failed-auth count and a detection/response rule — the
detect-and-respond core of Domain 4.

**Negative test:** alert on every failure; tune thresholds so true attacks stand
out — then respond.

**Cleanup:** none.

### Lab 7.5 — CCOA: Securing Assets

**Objective:** Harden an asset by reducing its attack surface.

```bash
ss -tlnp 2>/dev/null | awk '/LISTEN/{print $4}' | head
echo "Harden: disable unused services, patch, restrict by firewall, enforce least privilege."
```

**Expected result:** the listening surface to reduce and the hardening steps — the
asset-securing domain (D5) that shrinks what must be monitored.

**Negative test:** monitor a huge attack surface instead of reducing it; **harden
first**, then monitor what remains.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

CCOA is ISACA's hands-on SOC-analyst credential: a four-hour hybrid exam with
performance-based labs across five domains — technology essentials, principles/
risks, adversary TTPs, detection/response, and securing assets. It complements
ISACA's audit/governance certifications with a technical operations credential.

- [ ] I can list the five CCOA domains and the hybrid exam format.
- [ ] I can read host/network fundamentals and apply CIA controls.
- [ ] I can map observations to MITRE ATT&CK techniques.
- [ ] I can detect an event in logs and harden an asset.
- [ ] I completed Labs 7.1–7.5 including each negative test.
