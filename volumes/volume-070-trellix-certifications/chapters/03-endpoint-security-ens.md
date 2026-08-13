# Chapter 03: Endpoint Security (ENS)

## Learning Objectives

- Explain the Trellix Endpoint Security (ENS) modules.
- Configure Threat Prevention (access protection, exploit prevention, on-access scan).
- Configure the endpoint Firewall and Web Control.
- Apply Adaptive Threat Protection (ATP) with reputation.
- Complete a walkthrough for each ENS topic (defensive).

## Theory and Architecture

**Trellix Endpoint Security (ENS)** is the endpoint protection suite, managed through ePO. It is
modular: **Threat Prevention** (signature and behavioral anti-malware, **on-access** and
**on-demand** scanning, **access protection** rules that lock down files/registry/processes, and
**exploit prevention**); the **Firewall** (host-based, stateful, rule-based network control per
endpoint); **Web Control** (browser protection — blocking malicious/risky sites by reputation and
category); and **Adaptive Threat Protection (ATP)** (reputation-based dynamic defense — using file
and process **reputation** from Trellix Global Threat Intelligence and local analysis to allow,
block, or contain based on risk). Policy is authored in ePO and inherited by System Tree groups.
**Exclusions** tune false positives precisely. ENS replaces the legacy VirusScan/Host IPS/SiteAdvisor
stack with one integrated agent. Everything here is **defensive** endpoint protection.

## Design Considerations

Enable **on-access scanning** with tuned **exclusions** (scoped, not blanket), turn on **exploit
prevention** and **access protection** for behavioral defense, and use **ATP reputation** to catch
unknown threats. Start protective policies in **observe/report** where available before enforcing.
Firewall on **least privilege**; Web Control by **reputation/category**.

## Implementation and Automation

The labs configure Threat Prevention, an access-protection rule, the firewall, and ATP — all
**defensive**.

## Validation and Troubleshooting

Confirm the ENS model:

```text
ENS modules: Threat Prevention (on-access/on-demand scan, access protection, exploit prevention),
  Firewall (host stateful rules), Web Control (site reputation/category), ATP (reputation-based).
Managed via ePO policy + inheritance. Exclusions tune false positives precisely.
```

Common pitfalls: **blanket exclusions** that create blind spots; and enforcing a new policy with no
**observe** phase (breaks apps).

## Security and Best Practices

Layer **Threat Prevention + exploit prevention + ATP** for defense in depth, scope **exclusions**
narrowly, and phase enforcement (observe → enforce). Keep signatures/GTI current. Firewall and Web
Control on least privilege. Defensive protection throughout.

## Hands-On Lab

ENS walkthroughs (defensive). **Shared prerequisites** — ENS managed by ePO (or the policy
patterns), in an **authorized** lab. **Cost:** none.

### Lab 3.1 — Configure on-access scanning

**Objective:** Enable real-time malware scanning with a scoped exclusion.

```text
# ENS Threat Prevention policy (ePO): On-Access Scan = enabled; add a SCOPED exclusion for a known-good
#   high-I/O path (e.g., a database data directory) by full path, not a wildcard drive.
"on-access scan: ON + scoped exclusion (specific path) -> protection without breaking the app"
```

**Expected result:** **on-access scanning** enabled with a **precise** exclusion — real-time
protection tuned for the workload.

**Negative test:** exclude an entire drive to stop a performance complaint; that creates a **blind
spot** — scope the exclusion to the specific path.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.2 — Access protection rule

**Objective:** Lock down a sensitive resource behaviorally.

```text
# ENS Access Protection: add a rule to block untrusted processes from modifying a protected folder
#   or registry key (e.g., prevent non-approved processes writing to a startup location).
"access protection: block untrusted process -> protected path/registry (behavioral defense)"
```

**Expected result:** an **access-protection** rule stopping unauthorized modification — behavioral
defense beyond signatures.

**Negative test:** rely on signatures alone; **access protection/exploit prevention** stop
behaviors signatures miss — enable them.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.3 — Endpoint firewall

**Objective:** Apply host-based network control.

```text
# ENS Firewall policy: default deny inbound; allow established/related; allow only required apps/ports;
#   use location awareness (corporate vs public) for different rule sets.
"firewall: default-deny inbound + allow required + location-aware rule sets"
```

**Expected result:** a **host firewall** with least-privilege, location-aware rules — endpoint
network protection.

**Negative test:** allow all inbound on endpoints; **default-deny** with explicit allows — least
privilege.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.4 — Adaptive Threat Protection (ATP)

**Objective:** Use reputation to handle unknown files.

```text
# ATP: assign reputation-based rules -> files/processes with poor GTI/local reputation are blocked
#   or contained; unknown ("might be malicious") can be observed or contained pending verdict.
"ATP: reputation (GTI + local) -> allow / contain / block by risk -> catches unknown threats"
```

**Expected result:** **ATP** allowing/containing/blocking by **reputation** — protection against
never-before-seen files.

**Negative test:** trust any file with no known-bad signature; **ATP reputation** flags unknown
risk — enable it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

ENS is Trellix's integrated endpoint suite — Threat Prevention (scanning, access protection,
exploit prevention), Firewall, Web Control, and reputation-based ATP — managed via ePO. Layer the
modules, scope exclusions precisely, phase enforcement, and use ATP reputation for unknown threats.
Defensive throughout.

- [ ] I can configure on-access scanning with a scoped exclusion.
- [ ] I can write an access-protection rule.
- [ ] I can apply a least-privilege endpoint firewall.
- [ ] I can use ATP reputation for unknown files.
- [ ] I completed Labs 3.1–3.4 including each negative test.
