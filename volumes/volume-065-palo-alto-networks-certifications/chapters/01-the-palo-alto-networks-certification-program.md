# Chapter 01: The Palo Alto Networks Certification Program

## Learning Objectives

- Explain the Palo Alto Networks role-based certification framework.
- Identify the four levels (Foundational, Professional, Specialist, Architect) and three tracks.
- Understand the 2025 restructure that retired the legacy code-based exams.
- Describe the platform the certifications test across the three tracks.
- Verify current program facts from the authoritative source.

## Theory and Architecture

Palo Alto Networks **restructured its certification program in 2025** from the legacy
code-based exams (the PCNSA/PCNSE/PCCSE/PCDRA/PCSAE/PCSFE/PCCET generation) into a **role-based
framework**. Credentials now map to **job roles** and are organized by **level** and **track**.
The four **levels** are **Foundational**, **Professional**, **Specialist**, and **Architect**;
the three **tracks** are **Network Security**, **Security Operations**, and **Cloud Security**.
Two **Foundational** credentials — **Cybersecurity Apprentice** and **Cybersecurity
Practitioner** — are shared across all tracks, then each track climbs through a Professional
credential to role-specific Specialist credentials and, for Network Security and Security
Operations, an Architect credential.

The framework spans Palo Alto's whole platform: **NGFW/PAN-OS**, Panorama, Strata, Prisma
SD-WAN, and Prisma Access/SASE for **Network Security**; **Cortex XDR, XSIAM, and XSOAR** for
**Security Operations**; and **Prisma Cloud / Cortex Cloud** (CNAPP) for **Cloud Security**.
Exams are delivered at **Pearson VUE**. This volume is the certification companion to
[Volume XVI — Palo Alto Networks Security](../../volume-016-palo-alto-networks-security/README.md),
which covers the product platform in depth; here the focus is the exam blueprints, one
walkthrough lab per role/domain.

> **Ethics and scope.** Palo Alto's firewall, XDR/XSIAM, and XSOAR are defensive platforms.
> Every lab in this volume is **authorized administration, detection, hunting, incident
> response, or automation** — never an operational attack technique.

## Design Considerations

Pick a **track** by role — network security, security operations, or cloud security — and start
with the shared **Foundational** credentials before the Professional and Specialist levels.
Because the program was **rebuilt in 2025**, verify the current credential names and blueprints
on the official site; legacy codes (PCNSE, etc.) are retired.

## Implementation and Automation

Confirm the framework from the source:

```bash
curl -sSL -A "Mozilla/5.0" "https://www.paloaltonetworks.com/services/education/certification" \
  | grep -oiE 'Foundational|Professional|Specialist|Architect|Network Security|Security Operations|Cloud Security' \
  | sort -u
```

## Validation and Troubleshooting

The verified program facts (paloaltonetworks.com, 28 July 2026):

```text
Levels : Foundational -> Professional -> Specialist -> Architect.
Tracks : Network Security | Security Operations | Cloud Security.
Foundational (shared): Cybersecurity Apprentice; Cybersecurity Practitioner.
Network Security: Professional; Analyst; Next-Generation Firewall Engineer; SD-WAN Engineer;
                  Security Service Edge Engineer; Architect.
Security Operations: Professional; XDR Analyst; XSIAM Analyst; XDR Engineer; XSIAM Engineer;
                     XSOAR Engineer; Architect.
Cloud Security: Professional; Cloud Security Engineer.
Delivery: Pearson VUE. 2025 restructure retired the legacy code-based exams.
```

Common pitfalls: studying for a **retired** exam (PCNSE/PCNSA/PCCSE); and confusing this
**cert-tracks** volume with the Vol XVI product volume.

## Security and Best Practices

Map your **role** to a track and level, study the **current** blueprint, and practice on real or
virtual Palo Alto platforms in an **authorized** lab. Verify credentials on
paloaltonetworks.com — third-party dump sites are neither authoritative nor permitted.

## References and Knowledge Checks

- paloaltonetworks.com/services/education/certification: the role-based framework, levels, and tracks.
- Volume XVI (Palo Alto Networks Security): the product platform in depth.

**Knowledge checks**

1. Name the four levels and three tracks.
2. What changed in the 2025 restructure?
3. Which two credentials are shared Foundational?

## Hands-On Lab

Orientation walkthroughs. **Shared prerequisites for Labs 1.1–1.3** — a shell with `curl` and
`python3`. **Cost:** none.

### Lab 1.1 — Confirm the levels and tracks

**Objective:** Read the framework from the source.

```bash
curl -sSL -A "Mozilla/5.0" "https://www.paloaltonetworks.com/services/education/certification" \
  | grep -oiE 'Foundational|Professional|Specialist|Architect|Network Security|Security Operations|Cloud Security' \
  | sort -u
```

**Expected result:** the four levels and three tracks — the program map.

**Negative test:** study a pre-2025 "PCNSE/PCNSA" cert list; those exams are **retired** —
confirm the role-based framework on paloaltonetworks.com.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 1.2 — Map credentials to level and track

**Objective:** Record the role-based credentials.

```python
python3 - <<'PY'
framework={
 "Network Security":["Professional","Analyst","Next-Generation Firewall Engineer",
                     "SD-WAN Engineer","Security Service Edge Engineer","Architect"],
 "Security Operations":["Professional","XDR Analyst","XSIAM Analyst","XDR Engineer",
                        "XSIAM Engineer","XSOAR Engineer","Architect"],
 "Cloud Security":["Professional","Cloud Security Engineer"],
}
print("Foundational (shared): Cybersecurity Apprentice; Cybersecurity Practitioner")
for track,creds in framework.items():
    print(f"\n{track}:")
    for c in creds: print("  -",c)
PY
```

**Expected result:** the credential list by track — your study map.

**Negative test:** register for a legacy code exam; those are **retired** — pick a current
role-based credential.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 1.3 — Plan a track and level path

**Objective:** Sequence credentials for a role.

```python
python3 - <<'PY'
paths={"Firewall engineer":"Apprentice/Practitioner -> Network Security Professional -> NGFW Engineer -> Architect",
       "SOC analyst":"Foundational -> Security Operations Professional -> XDR/XSIAM Analyst",
       "SOAR automation":"Foundational -> Security Operations Professional -> XSOAR Engineer",
       "Cloud security":"Foundational -> Cloud Security Professional -> Cloud Security Engineer"}
for role,path in paths.items(): print(f"{role:18}: {path}")
PY
```

**Expected result:** role-to-path sequences — the ladder this volume follows.

**Negative test:** attempt a Specialist exam with no Foundational base; start with the shared
**Foundational** credentials.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Palo Alto Networks rebuilt its certifications in 2025 into a role-based framework — four levels
(Foundational, Professional, Specialist, Architect) across three tracks (Network Security,
Security Operations, Cloud Security) — retiring the legacy code-based exams. Pick a track, start
Foundational, and verify the current blueprint on the official site.

- [ ] I can name the four levels and three tracks.
- [ ] I can explain the 2025 restructure.
- [ ] I can map credentials to level and track.
- [ ] I can plan a role-based path.
- [ ] I completed Labs 1.1–1.3 including each negative test.
