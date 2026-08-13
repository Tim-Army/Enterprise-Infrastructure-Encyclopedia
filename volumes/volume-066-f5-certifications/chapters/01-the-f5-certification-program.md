# Chapter 01: The F5 Certification Program

## Learning Objectives

- Explain the F5 certification ladder (Administrator, Technology Specialist, Solution Expert).
- Understand the 2025 update that split the Administrator credential into five focused exams.
- Map the CTS specializations (LTM, DNS, Advanced WAF/ASM, APM) to exams.
- Describe the platform the certifications test: BIG-IP TMOS, plus NGINX and Distributed Cloud.
- Verify current program facts from the authoritative source.

## Theory and Architecture

F5's certification program certifies engineers who deploy and operate **BIG-IP** — F5's
application delivery and security platform running the **TMOS** operating system. The ladder has
three technical levels. The **F5 Certified Administrator, BIG-IP (F5-CA)** is the foundation;
**in 2025 F5 rebuilt it into five short, focused exams** (F5CAB1–F5CAB5) — Install/Initial
Configuration/Upgrade, Data Plane Concepts, Data Plane Configuration, Control Plane
Administration, and Support and Troubleshooting — replacing the legacy 101 + 201 exams. Above it,
the **F5 Certified Technology Specialist (F5-CTS)** adds product specializations: **LTM** (Local
Traffic Manager — load balancing; exams 301a/301b), **DNS** (302), **Advanced WAF / ASM**
(Application Security Manager; 303), and **APM** (Access Policy Manager; 304), each requiring the
F5-CA first. The **F5 Certified Solution Expert (F5-CSE), Security** (401) sits at the top,
requiring the F5-CA and all four CTS specializations.

The exams test the BIG-IP platform: **virtual servers, pools, profiles, and iRules** for traffic
management, **SSL/TLS** handling, **HA/config sync**, and the security modules (WAF, access).
F5's modern portfolio also spans **NGINX** and **F5 Distributed Cloud (XC)**; this volume centers
on the BIG-IP certification ladder, one walkthrough lab per exam domain.

> **Scope.** The WAF/ASM and APM modules are security controls. Every lab is **authorized
> administration, policy, and defense** — never an operational attack technique.

## Design Considerations

Start with the **F5-CA** foundation (the five exams can be taken in any order), then add the
**CTS** specialization your role needs — LTM for load balancing, DNS for GSLB, Advanced WAF for
application security, APM for access. Because the Administrator credential was **restructured in
2025**, verify the current exams on the official site; the legacy 101/201 path is retired.

## Implementation and Automation

Confirm the program from the source:

```bash
curl -sSL -A "Mozilla/5.0" "https://education.f5.com/learning-path/view/9" \
  | grep -oiE 'F5CAB[1-5]|Administrator|Technology Specialist|LTM|DNS|ASM|APM' | sort -u
```

## Validation and Troubleshooting

The verified program facts (education.f5.com and clouddocs.f5.com, 28 July 2026):

```text
F5-CA (Administrator, 2025): 5 exams F5CAB1-F5CAB5 (install/config/upgrade; data plane concepts;
  data plane config; control plane admin; support & troubleshooting). Replaces legacy 101+201.
F5-CTS (requires F5-CA): LTM 301a+301b; DNS 302; Advanced WAF/ASM 303; APM 304.
F5-CSE Security 401 (requires F5-CA + all four CTS).
Platform: BIG-IP TMOS (+ NGINX, F5 Distributed Cloud/XC). Delivery: Pearson VUE.
```

Common pitfalls: studying the **legacy 101/201** as current (the Administrator path is now five
exams); and attempting a **CTS** without the F5-CA prerequisite.

## Security and Best Practices

Match the CTS specialization to your production role and platform, and practice on **BIG-IP
Virtual Edition** in an authorized lab. Verify exams on education.f5.com / my.f5.com —
third-party dumps are neither authoritative nor permitted.

## References and Knowledge Checks

- education.f5.com and clouddocs.f5.com: the certification learning paths and program overview.
- my.f5.com: the F5 knowledge base and product documentation.

**Knowledge checks**

1. What are the three technical certification levels?
2. What changed for the Administrator credential in 2025?
3. Name the four CTS specializations.

## Hands-On Lab

Orientation walkthroughs. **Shared prerequisites for Labs 1.1–1.3** — a shell with `curl` and
`python3`. **Cost:** none.

### Lab 1.1 — Confirm the certification ladder

**Objective:** Read the program structure from the source.

```bash
curl -sSL -A "Mozilla/5.0" "https://education.f5.com/learning-path/view/9" \
  | grep -oiE 'F5CAB[1-5]|Administrator|Technology Specialist|Solution Expert|LTM|DNS|ASM|APM' | sort -u
```

**Expected result:** the Administrator exams and the CTS/CSE levels — the program map.

**Negative test:** study a pre-2025 "101/201" outline; the Administrator path is now **five
exams** — confirm on education.f5.com.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 1.2 — Map exams to credentials

**Objective:** Record the verified exam structure.

```python
python3 - <<'PY'
program={
 "F5-CA (Administrator)":["F5CAB1","F5CAB2","F5CAB3","F5CAB4","F5CAB5"],
 "CTS LTM":["301a","301b"], "CTS DNS":["302"], "CTS Advanced WAF/ASM":["303"], "CTS APM":["304"],
 "CSE Security":["401 (after F5-CA + 4x CTS)"],
}
for cred,exams in program.items(): print(f"{cred:24}: {', '.join(exams)}")
PY
```

**Expected result:** a credential → exam table — your scheduling reference.

**Negative test:** register for a retired 201 exam; confirm the **current** F5CAB exams on the
portal.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 1.3 — Plan a specialization path

**Objective:** Sequence credentials for a role.

```python
python3 - <<'PY'
paths={"ADC engineer":"F5-CA -> CTS LTM (301a/301b)",
       "GSLB/DNS":"F5-CA -> CTS DNS (302)",
       "App security":"F5-CA -> CTS Advanced WAF (303) -> CSE Security (401)",
       "Access/VPN":"F5-CA -> CTS APM (304)"}
for role,path in paths.items(): print(f"{role:14}: {path}")
PY
```

**Expected result:** role-to-path sequences — the ladder this volume follows.

**Negative test:** attempt a CTS first; earn the **F5-CA** foundation before any specialization.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

F5's program certifies BIG-IP/TMOS engineers across the Administrator (rebuilt in 2025 into five
F5CAB exams), Technology Specialist (LTM, DNS, Advanced WAF, APM), and Solution Expert levels,
delivered by Pearson VUE. Earn the F5-CA foundation, add the CTS specialization your role needs,
and verify the current exams on the official site.

- [ ] I can name the three technical levels.
- [ ] I can explain the 2025 Administrator restructure.
- [ ] I can map exams to credentials.
- [ ] I can plan a specialization path.
- [ ] I completed Labs 1.1–1.3 including each negative test.
