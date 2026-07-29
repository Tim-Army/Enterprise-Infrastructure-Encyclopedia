# Chapter 05: Penetration Testing — Authorized

## Learning Objectives

- Understand the CPENT professional penetration-testing process.
- Establish authorization, scope, and rules of engagement.
- Apply web-application assessment methodology (WAHS).
- Understand the LPT (Master) elite practical.
- Complete a walkthrough for each pentest domain — defensively.

## Theory and Architecture

The **Certified Penetration Testing Professional (CPENT)** validates a rigorous, **authorized**
penetration-testing process across enterprise networks, web apps, IoT, OT, cloud, and pivoting —
performed entirely in EC-Council's practical range. **Web Application Hacking and Security (WAHS)**
focuses on authorized web-app assessment methodology. The **Licensed Penetration Tester (LPT)
Master** is the elite, fully hands-on credential — a multi-hour practical proving end-to-end,
professional assessment under realistic constraints. As with CEH (Chapter 3), this volume teaches
these strictly as **authorized, educational methodology**: the value is the **process** — scoping,
rules of engagement, structured testing, and a **report that drives remediation** — not any
operational payload. Every action requires **written authorization and a defined scope**, uses
**safe, local** commands, and ends in a defender-focused report. This is the professional discipline
CPENT and LPT validate, and it is exactly how a legitimate engagement is run.

> **Scope.** This chapter is **authorized methodology only**. Written authorization and a defined
> scope gate every step; commands are safe and local (owned systems); the deliverable is a
> remediation-focused report. No operational attack against third parties.

## Design Considerations

**Authorization and scope first** — always. Document **rules of engagement** (windows, exclusions,
contacts, handling of sensitive data). Follow a **structured methodology** (recon → analysis →
validation → reporting). Minimize impact; avoid DoS on production. Deliver a **prioritized,
actionable report**, and retest to confirm fixes.

## Implementation and Automation

The labs build authorization/scope, plan a structured test, scope a web assessment, and report.

## Validation and Troubleshooting

Confirm the pentest map:

```text
CPENT = professional pentest process (networks/web/IoT/OT/cloud/pivoting) in a practical range. WAHS = web-app assessment method.
LPT (Master) = elite hands-on practical. Gate: written authorization + scope. Deliverable: remediation-focused report. Authorized only.
```

Common pitfalls: testing out of scope / without authorization (illegal); and delivering raw output
instead of a **prioritized report**.

## Security and Best Practices

Never test without **written authorization and scope**. Follow a structured methodology, minimize
impact, protect findings, and report for **remediation**. Retest. All work is authorized and
defensive in purpose.

## Hands-On Lab

Authorized-methodology walkthroughs. **Shared prerequisites** — Linux with `python3`, `nmap`, and a
target **you own** (`127.0.0.1`), in a lab. **Cost:** none.

### Lab 5.1 — CPENT: authorization and rules of engagement

**Objective:** Gate the engagement.

```python
python3 - <<'PY'
roe={"authorized":True,"scope":["127.0.0.1","10.20.0.0/24"],"exclusions":["prod DB"],
     "window":"2026-08-05 20:00–24:00","dos_allowed":False,"contact":"soc@lab.example"}
target="127.0.0.1"
go = roe["authorized"] and target in roe["scope"]
print("RoE:",roe)
print(f"test {target}? ->", "PROCEED" if go else "STOP")
PY
```

**Expected result:** the RoE and a **PROCEED** only because authorized and in scope — the CPENT gate.

**Negative test:** an out-of-scope or excluded target must return **STOP** — respect scope and
exclusions.

**Cleanup:** none.

### Lab 5.2 — CPENT: structured enumeration on an owned host

**Objective:** Begin the methodology.

```bash
nmap -sT -F 127.0.0.1 2>/dev/null | sed -n '1,12p' \
  || python3 -c "import socket;print('open ports check on localhost only')"
echo "CPENT: structured recon -> analysis -> validation -> report (all authorized, minimal impact)"
```

**Expected result:** enumeration of **your own** host as step one of a structured test.

**Negative test:** run high-impact scans against production in the window without care; **minimize
impact** — DoS is out of scope here.

**Cleanup:** none.

### Lab 5.3 — WAHS: scope a web assessment

**Objective:** Plan web methodology.

```python
python3 - <<'PY'
areas=["authn/session management","access control (IDOR/privilege)","injection classes (input validation)",
       "sensitive data exposure","security misconfig / headers","SSRF/business logic"]
print("WAHS assessment areas (authorized, in-scope app only):")
for a in areas: print(" -",a)
print("For each: test method + remediation for defenders")
PY
```

**Expected result:** structured **web-assessment areas** with a remediation focus — WAHS methodology.

**Negative test:** run web exploit tooling with no scope or method; professional assessment is
**structured and authorized** — plan first.

**Cleanup:** none.

### Lab 5.4 — Report findings for remediation

**Objective:** Deliver value to defenders.

```python
python3 - <<'PY'
findings=[{"title":"Missing patches (external)","risk":"Critical","fix":"patch + verify"},
          {"title":"Weak TLS ciphers","risk":"High","fix":"disable legacy suites"},
          {"title":"Verbose errors","risk":"Low","fix":"generic error pages"}]
order={"Critical":0,"High":1,"Medium":2,"Low":3}
for f in sorted(findings,key=lambda x:order[x["risk"]]):
    print(f"[{f['risk']:8}] {f['title']:28} -> {f['fix']}")
PY
```

**Expected result:** findings ordered by **risk** with fixes — an LPT-quality remediation report.

**Negative test:** hand over tool logs unsorted; defenders can't prioritize — deliver a **ranked,
actionable report**.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Penetration Testing (CPENT, WAHS, LPT Master) is taught here as authorized methodology: authorization
and scope gate every step, testing is structured and low-impact, and the deliverable is a
remediation-focused report — the professional process these credentials validate.

- [ ] I can establish authorization and rules of engagement (CPENT).
- [ ] I can run structured enumeration on an owned host.
- [ ] I can scope a web assessment (WAHS).
- [ ] I can report findings for remediation.
- [ ] I completed Labs 5.1–5.4 including each negative test.
