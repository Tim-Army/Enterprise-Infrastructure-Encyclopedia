# Chapter 04: Offensive Operations — Authorized Methodology

## Learning Objectives

- Establish authorization, scope, and rules of engagement before any test (GPEN).
- Apply web-application and exploit-assessment methodology safely (GWAPT, GXPN).
- Understand mobile assessment scope (GMOB).
- Run authorized vulnerability assessment and prioritize findings (GEVA).
- Complete a walkthrough for each Offensive Operations domain — defensively.

## Theory and Architecture

The **Offensive Operations** focus area validates **authorized** security assessment. **GPEN
(Penetration Tester)** covers the professional penetration-testing process — **scoping, rules of
engagement, authorization**, reconnaissance, and structured, documented testing. **GWAPT (Web
Application Penetration Tester)** covers web-app assessment methodology (the OWASP-style classes of
weakness and how to test for them). **GXPN (Exploit Researcher and Advanced Penetration Tester)**
covers advanced technique and exploit research **concepts**. **GMOB (Mobile Device Security
Analyst)** covers mobile app/device assessment. **GEVA (Enterprise Vulnerability Assessor)** covers
running and interpreting vulnerability assessments at scale. In this volume every one of these is
taught as **authorized, educational methodology**: the gate is always **written authorization and a
defined scope**, the commands are **safe and local** (against systems you own in a lab), and the
deliverable is a **report that helps defenders**. No operational attack payload appears here — the
value is the *process*, which is exactly what GIAC's offensive exams and professional engagements
demand.

> **Scope.** This chapter is **authorized assessment methodology only**. Every technique requires
> written authorization and an in-scope target you own. Labs use safe local commands, scope/RoE
> files, and report structures — never an attack against a third party.

## Design Considerations

**Authorization first**: no testing without written permission and a defined scope. Document
**rules of engagement** (windows, excluded systems, emergency contacts). Prefer **least-impact**
techniques; avoid denial-of-service on production. Turn findings into a **prioritized, actionable
report** for defenders. Retest to confirm remediation.

## Implementation and Automation

The labs build a scope/RoE, run an authorized local scan, and prioritize findings.

## Validation and Troubleshooting

Confirm the offensive-methodology map:

```text
GPEN = pentest process (scope + RoE + authorization + methodology + report). GWAPT = web-app testing method.
GXPN = advanced/exploit research concepts. GMOB = mobile assessment. GEVA = enterprise vuln assessment/prioritization.
Gate: written authorization + defined scope. Deliverable: report for defenders. Authorized/educational only.
```

Common pitfalls: testing **out of scope** or without written authorization (illegal/unethical); and
delivering raw scanner output instead of a **prioritized report**.

## Security and Best Practices

Never test without **written authorization and scope**. Stay in scope, minimize impact, and protect
findings (they are sensitive). Report in terms of **risk and remediation**, not just tool output.
All work is authorized and defensive in purpose.

## Hands-On Lab

Authorized-methodology walkthroughs. **Shared prerequisites** — Linux with `python3`, `nmap`, and a
target **you own** (use `127.0.0.1`/localhost), in a lab. **Cost:** none.

### Lab 4.1 — GPEN: define authorization and scope

**Objective:** Gate testing on authorization.

```python
python3 - <<'PY'
engagement={"authorized":True,"client":"Lab Corp (self-owned lab)",
            "in_scope":["127.0.0.1","10.10.0.0/24"],"out_of_scope":["10.10.0.1 (gateway)"],
            "window":"2026-08-01 18:00–22:00","contact":"soc@lab.example"}
target="127.0.0.1"
ok = engagement["authorized"] and any(target.startswith(s.split('/')[0][:5]) or target==s for s in engagement["in_scope"])
print("engagement:",engagement["client"],"| window:",engagement["window"])
print(f"test {target}? ->", "PROCEED (authorized + in scope)" if ok else "STOP")
PY
```

**Expected result:** the engagement record and a **PROCEED** only because it is authorized and in
scope — the GPEN gate.

**Negative test:** point at an out-of-scope or third-party host; the gate must return **STOP** — no
authorization, no test.

**Cleanup:** none.

### Lab 4.2 — GPEN/GEVA: run an authorized local scan

**Objective:** Enumerate a target you own.

```bash
# Authorized, against localhost only:
nmap -sT -F 127.0.0.1 2>/dev/null | sed -n '1,15p' \
  || python3 -c "import socket;print('open' if socket.socket().connect_ex(('127.0.0.1',22))==0 else 'closed','22/tcp')"
```

**Expected result:** the open ports on **your own** host — structured enumeration, the first
assessment step.

**Negative test:** scan an address you were not authorized for; that is out of scope and
prohibited — scan only **in-scope, owned** systems.

**Cleanup:** none (read-only scan of localhost).

### Lab 4.3 — GEVA: prioritize findings by risk

**Objective:** Turn results into an actionable report.

```python
python3 - <<'PY'
findings=[{"id":"weak-tls","cvss":7.4,"exposure":"external"},
          {"id":"missing-patch","cvss":9.8,"exposure":"external"},
          {"id":"verbose-banner","cvss":3.1,"exposure":"internal"}]
for f in sorted(findings,key=lambda x:(x["exposure"]!="external",-x["cvss"])):
    print(f"{f['id']:16} CVSS {f['cvss']:<4} {f['exposure']:8} -> fix order by external+severity")
PY
```

**Expected result:** findings ordered by **external exposure then severity** — a prioritized GEVA
report defenders can act on.

**Negative test:** hand over raw scanner output unsorted; defenders can't tell what to fix first —
**prioritize** by risk.

**Cleanup:** none.

### Lab 4.4 — GWAPT/GMOB: scope a web/mobile assessment

**Objective:** Plan methodology, not payloads.

```python
python3 - <<'PY'
web_checks=["authn/session mgmt","access control (IDOR)","input validation/injection classes",
            "sensitive data exposure","security headers/TLS"]
mobile_checks=["local data storage","transport security (cert pinning)","platform API misuse",
               "hardcoded secrets","auth token handling"]
print("GWAPT methodology areas:"); [print(" -",c) for c in web_checks]
print("GMOB methodology areas:");  [print(" -",c) for c in mobile_checks]
print("Test each ONLY on authorized, in-scope apps you own; report findings to defenders.")
PY
```

**Expected result:** structured **methodology areas** for web and mobile assessment — the GWAPT/GMOB
approach (process, not exploit code).

**Negative test:** jump to running exploit tooling with no methodology or scope; professional
assessment is **structured and authorized** — plan first.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Offensive Operations (GPEN, GWAPT, GXPN, GMOB, GEVA) is taught here as authorized methodology:
authorization and scope gate every action, techniques stay safe and local, and the deliverable is a
prioritized report that helps defenders — the professional process GIAC's offensive exams validate.

- [ ] I can define authorization, scope, and rules of engagement (GPEN).
- [ ] I can run an authorized local scan on a system I own.
- [ ] I can prioritize findings into a report (GEVA).
- [ ] I can scope web/mobile assessment methodology (GWAPT/GMOB).
- [ ] I completed Labs 4.1–4.4 including each negative test.
