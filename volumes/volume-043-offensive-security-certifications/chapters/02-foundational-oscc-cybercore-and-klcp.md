# Chapter 02: Foundational — OSCC (CyberCore) and KLCP

## Learning Objectives

- Explain the foundational OffSec credentials: OSCC (CyberCore) and KLCP.
- Describe the CyberCore courses (SEC-100, SJD-100) and the Kali course (PEN-103).
- Establish the cybersecurity fundamentals and Kali Linux skills the later courses assume.
- Practice foundational methodology and Kali administration on your own system.
- Complete per-topic walkthroughs for the foundational topic areas.

## Theory and Architecture

Two foundational tracks prepare newcomers for OffSec's harder courses:

- **OSCC (OffSec CyberCore Certified)** — earned through the **CyberCore**
  courses **SEC-100** and **SJD-100**. It builds broad cybersecurity literacy:
  the CIA triad, threats and attackers, networking and operating-system basics,
  and an introduction to both offensive and defensive practice. It uses the
  three-year **"+" renewal** model.
- **KLCP (Kali Linux Certified Professional)** — earned through **PEN-103**. It
  certifies fluency with **Kali Linux**, the distribution OffSec's offensive
  courses run on: installation and configuration, the tool ecosystem, **Debian
  package management**, and customization.

Together they are the on-ramp: CyberCore gives the conceptual base, and KLCP
gives the platform fluency that PEN-200 and beyond assume.

## Design Considerations

Use the foundational tier to **remove friction later**. Candidates who struggle
with OSCP often lack Linux and tooling fundamentals, not offensive concepts — KLCP
fixes that. CyberCore suits genuine newcomers and career-changers who need the
vocabulary before the hands-on courses. Neither is required for the harder
courses, but both shorten the climb.

## Implementation and Automation

The labs below practice foundational skills on **your own system**: cybersecurity
fundamentals (CIA, hashing, permissions) for CyberCore, and Kali administration
(package management, tool inventory, service control) for KLCP.

## Validation and Troubleshooting

Confirm the foundational courses on offsec.com:

```text
offsec.com/courses:
  - SEC-100 / SJD-100 -> OSCC (CyberCore) — fundamentals, "+" renewal
  - PEN-103 -> KLCP — Kali Linux administration and tooling
```

Common pitfalls: skipping fundamentals and then stalling on OSCP; and treating
**Kali** as "just a tool bag" rather than a Debian system you must administer
(update, configure, troubleshoot).

## Security and Best Practices

Keep Kali **updated** (`apt update && apt full-upgrade`) and run it in a VM you
control. Learn the CIA triad, least privilege, and defense in depth as the frame
for everything offensive that follows — offensive skill is only ethical when
paired with defensive understanding and authorization.

## References and Knowledge Checks

- offsec.com: *SEC-100 / SJD-100 (OSCC)* and *PEN-103 (KLCP)* course pages; kali.org documentation.

**Knowledge checks**

1. What do the CyberCore courses cover, and which credential do they earn?
2. What does KLCP certify beyond "using tools"?
3. Why do Linux and Kali fundamentals matter for the OSCP?

## Hands-On Lab

Per-topic walkthroughs for the foundational areas. **All commands run on your own
Kali/Linux system.**

**Shared prerequisites** — a Kali (or Debian-based) shell with `sudo`, `apt`,
`sha256sum`, and standard tools. **Cost:** none.

### Lab 2.1 — CyberCore: the CIA triad in practice

**Objective:** Demonstrate confidentiality and integrity concretely.

```bash
echo "sensitive" > f.txt
sha256sum f.txt                                   # integrity baseline
chmod 600 f.txt; ls -l f.txt | awk '{print $1}'   # confidentiality via permissions
```

**Expected result:** a SHA-256 digest (integrity) and `-rw-------` (confidentiality
by least-privilege permissions) — two legs of the CIA triad CyberCore teaches.

**Negative test:** `chmod 777 f.txt`; world access breaks confidentiality — least
privilege protects it.

**Rollback:** `rm -f f.txt`

### Lab 2.2 — CyberCore: threats and the attacker mindset

**Objective:** Classify a threat and its control (defensive framing).

```bash
python3 - <<'PY'
threats = {"Phishing":"user training + MFA","Weak password":"length + MFA + lockout",
           "Unpatched service":"patch management + minimize exposure"}
for t,c in threats.items(): print(f"{t:18} -> control: {c}")
PY
```

**Expected result:** common threats mapped to controls — the threat-and-defense
literacy CyberCore builds before any offensive work.

**Negative test:** study attacks without the defensive mapping; OffSec teaches
offense to strengthen defense — always know the control.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.3 — CyberCore: networking and services fundamentals

**Objective:** Read your own host's listening services (foundation for
enumeration).

```bash
ss -tlnp 2>/dev/null | awk 'NR==1 || /LISTEN/' | head
```

**Expected result:** the TCP services listening on your own host — the
service-and-port literacy every later course builds on.

**Negative test:** assume a closed-looking port is safe; services can bind to
specific interfaces — enumerate thoroughly.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.4 — KLCP: Kali package management (Debian apt)

**Objective:** Manage Kali as the Debian system it is.

```bash
apt-cache policy nmap | head -3           # installed vs candidate version
dpkg -l | grep -c '^ii'                    # count installed packages
```

**Expected result:** nmap's version policy and a package count — Debian package
management, a core KLCP skill.

**Negative test:** install tools from random scripts instead of `apt`; use the
package manager so updates and dependencies are tracked.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.5 — KLCP: the Kali tool ecosystem

**Objective:** Inventory the core offensive toolkit Kali ships.

```bash
for t in nmap gobuster hydra sqlmap john hashcat metasploit-framework; do
  dpkg -l "$t" 2>/dev/null | grep -q '^ii' && echo "$t: installed" || echo "$t: available via apt"
done
```

**Expected result:** the presence of the standard tools (nmap, gobuster, hydra,
sqlmap, john, hashcat, Metasploit) — the Kali ecosystem KLCP covers.

**Negative test:** assume every tool is preinstalled; some are `apt install`-only
— know how to add them.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.6 — KLCP: service and privilege control

**Objective:** Control a service and use privileges correctly.

```bash
sudo systemctl status ssh --no-pager 2>/dev/null | head -3 || echo "ssh not enabled"
id
```

**Expected result:** the ssh service state and your user/UID — service management
and privilege awareness, KLCP administration skills.

**Negative test:** run everything as root by habit; use `sudo` for specific
privileged actions and understand what each requires.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.7 — KLCP: customization and updates

**Objective:** Keep the platform current (the first step before any engagement).

```bash
apt-get -s update >/dev/null 2>&1 && echo "apt sources reachable (simulate update)"
echo "Before an engagement: apt update && apt full-upgrade; snapshot the VM."
```

**Expected result:** confirmation the update mechanism works and the pre-engagement
hygiene step — keeping Kali current and snapshotted, a KLCP practice.

**Negative test:** work from a months-old Kali image; outdated tools miss recent
techniques and fixes — update first.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The foundational tier prepares newcomers for OffSec's hands-on courses: **OSCC
(CyberCore)** builds cybersecurity literacy (CIA, threats, networking, offense and
defense), and **KLCP** certifies Kali Linux fluency (package management, the tool
ecosystem, administration). Both shorten the climb to OSCP and beyond.

- [ ] I can name the CyberCore and Kali courses and the credentials they earn.
- [ ] I can demonstrate the CIA triad and map threats to controls.
- [ ] I can manage Kali with apt and inventory the toolkit.
- [ ] I can keep Kali current and control services with least privilege.
- [ ] I completed Labs 2.1–2.7 including each negative test.
