# Chapter 07: Application Security

## Learning Objectives

- Explain runtime vulnerability analytics and why it prioritizes differently from a scanner.
- Distinguish third-party from code-level vulnerabilities.
- Describe attack detection and blocking, and the caution that belongs with blocking.
- Place Dynatrace Application Security in a DevSecOps lifecycle.

*Exam relevance: the whole **Advanced Security Specialist** skill list — third-party vulnerabilities, code-level vulnerabilities, attack detection and blocking, DevSecOps lifecycle, security events, threat hunting, DQL/DPL, licensing, third-party integrations. This chapter is **defensive**: detecting, prioritizing, and remediating, never exploiting.*

## Runtime vulnerability analytics

A conventional scanner reads a dependency manifest and reports every known CVE in it. That list is correct and, at scale, nearly useless — a large estate produces thousands of findings, most of them irrelevant, and the team learns to ignore the report.

Dynatrace's contribution is that OneAgent is already inside the running process, so it knows things a manifest cannot express:

| Question | Manifest scanner | Runtime analytics |
|:---|:---|:---|
| Is the vulnerable library present? | Yes | Yes |
| Is it actually **loaded** at runtime? | No | Yes |
| Is the vulnerable **code path reachable**? | No | Yes |
| Is the process **internet-exposed**? | No | Yes |
| Does it touch **sensitive data**? | No | Yes |
| Is there a **public exploit**? | Via feed | Yes |

The reprioritization this produces is severe and it inverts orderings. A CVSS 9.8 in a library that is present but never loaded, on an internal batch host, is a lower operational risk than a CVSS 6.5 in a code path that is reachable from the internet on a service handling cardholder data. **CVSS scores severity in the abstract; runtime context scores risk in your estate.** This is the same argument [Volume CXXXVII](../../volume-137-rapid7-certifications/README.md) makes for context-aware risk over raw CVSS, reached from a different direction — the agent is in the process rather than scanning it from outside.

## Third-party versus code-level

| | Third-party | Code-level |
|:---|:---|:---|
| Where | Libraries and dependencies | Your own code |
| Examples | A CVE in a JSON parser | SQL injection, command injection in your handler |
| Fix | Upgrade the dependency | Change the code |
| Detection | Known CVE matched to loaded libraries | Runtime observation of unsafe data flow |

Third-party findings are usually easier to act on — there is a version to move to. Code-level findings are yours to fix and often reveal a pattern rather than a single defect.

## Attack detection and blocking

Dynatrace can detect attacks against monitored applications at runtime — injection attempts and similar — and can **block** them.

Blocking deserves a caution stated plainly rather than buried:

> **Blocking is an application-availability decision, not only a security one.** A false positive does not produce a noisy alert; it produces a rejected legitimate request. That is an outage for the affected user.

The defensible sequence is: **detect first, measure precision, then block.** Run in detection mode long enough to know your false-positive rate on real traffic, review what would have been blocked, and enable blocking where the evidence supports it — narrowly at first. Enabling blocking on day one, estate-wide, converts a security control into an availability risk.

## Threat hunting

Security events land in Grail and are queried with DQL (Chapter 03), which means hunting uses the same language as the rest of the platform — no separate query dialect, and security events can be joined against the topology and the application telemetry around them.

## Hands-On Lab

Python models security prioritization. **Cost:** none. All labs are **defensive** — prioritization, detection quality, remediation planning.

### Lab 7.1 — Runtime context inverts the CVSS ordering

**Objective:** Rank by real risk instead of abstract severity.

```bash
python3 - <<'EOF'
FINDINGS = [
  # id,    cvss, loaded, reachable, internet, sensitive_data, exploit_known, where
  ("V-101", 9.8, False, False, False, False, True,  "batch host, lib present but never loaded"),
  ("V-102", 6.5, True,  True,  True,  True,  True,  "public checkout service, cardholder data"),
  ("V-103", 9.1, True,  False, False, False, False, "internal admin, loaded but path unreachable"),
  ("V-104", 7.5, True,  True,  True,  False, False, "public marketing site"),
  ("V-105", 5.3, True,  True,  False, True,  True,  "internal HR service, PII"),
  ("V-106",10.0, False, False, False, False, True,  "container image layer, not in running process"),
]
def risk(f):
    _, cvss, loaded, reach, inet, sens, exploit_known, _ = f
    if not loaded:  return 0.0, "NOT LOADED at runtime"
    s = cvss
    s *= 1.0 if reach else 0.25
    s *= 2.0 if inet else 1.0
    s *= 1.5 if sens else 1.0
    s *= 1.4 if exploit_known else 1.0
    return s, ""

print("--- ordered by CVSS (what a manifest scanner gives you) ---")
for f in sorted(FINDINGS, key=lambda x: -x[1]):
    print(f"   {f[0]}  CVSS {f[1]:>4}   {f[7]}")

print("\n--- ordered by RUNTIME RISK ---")
scored = sorted(((risk(f)[0], risk(f)[1], f) for f in FINDINGS), key=lambda x: -x[0])
for s, note, f in scored:
    tag = f"  [{note}]" if note else ""
    print(f"   {f[0]}  risk {s:>6.1f}  (CVSS {f[1]:>4}){tag}   {f[7]}")

top_cvss = max(FINDINGS, key=lambda x: x[1])[0]
top_risk = scored[0][2][0]
print(f"\nCVSS says fix {top_cvss} first (10.0). Runtime says fix {top_risk} first (CVSS 6.5).")
print(f"{top_cvss} is in an image layer that never loads into a running process —")
print("real, reportable, and not currently exploitable in this estate.")
ignorable = [f[0] for f in FINDINGS if not f[2]]
print(f"\n{len(ignorable)} of {len(FINDINGS)} findings ({', '.join(ignorable)}) are NOT LOADED.")
print("They are not 'fixed' — they still belong in the backlog and in any report to")
print("an auditor. They are DEPRIORITIZED, which is a different claim, and the")
print("distinction is what keeps this honest rather than a way of hiding findings.")
EOF
```

**Expected result:** The CVSS 10.0 finding drops to the bottom because it never loads, while a CVSS 6.5 on an internet-facing service handling cardholder data rises to the top. The closing distinction is essential: deprioritized is not fixed. Runtime context justifies *ordering* the queue, not deleting entries from it, and a finding that is unreachable today becomes reachable the moment someone changes a route.

**Negative test:** Suppressing not-loaded findings entirely. Reachability is a property of the current deployment, not of the vulnerability.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.2 — Measure precision before enabling blocking

**Objective:** Show what a false-positive rate costs when blocking is on.

```bash
python3 - <<'EOF'
DAILY_REQUESTS = 2_000_000
TRUE_ATTACKS   = 400
SCENARIOS = [
  ("day 1, default rules, block ON",   0.62, 0.95, 0.0009),
  ("after 2 weeks tuning, detect only",0.88, 0.93, 0.0002),
  ("after tuning, block ON",           0.88, 0.93, 0.0002),
  ("aggressive rules, block ON",       0.41, 0.99, 0.0040),
]
print(f"{'scenario':36}{'prec':>6}{'recall':>8}{'FP/day':>10}{'missed':>8}   effect")
for name, prec, recall, fp_rate in SCENARIOS:
    fps = int(DAILY_REQUESTS * fp_rate)
    missed = int(TRUE_ATTACKS * (1 - recall))
    blocking = "block ON" in name
    if blocking:
        eff = f"{fps:,} legitimate requests REJECTED/day"
    else:
        eff = f"{fps:,} noisy alerts/day (no user impact)"
    print(f"{name:36}{prec:>6.2f}{recall:>8.2f}{fps:>10,}{missed:>8}   {eff}")

print("\nThe same false-positive rate has completely different consequences:")
print("   detection mode -> an analyst sees noise")
print("   blocking mode  -> a customer sees an error")
print("\n'aggressive rules, block ON' catches 99% of attacks and rejects 8,000")
print("legitimate requests every day. At that volume it is an outage with a")
print("security justification, and it will be switched off in week one —")
print("taking the 99% recall with it.")
print("\nThe defensible sequence:")
print("   1. detect only, on real production traffic")
print("   2. review what WOULD have been blocked, measure precision")
print("   3. enable blocking narrowly where precision is high")
print("   4. widen slowly, watching rejection counts as an availability metric")
EOF
```

**Expected result:** Aggressive rules with blocking on reject 8,000 legitimate requests daily while catching 99% of attacks. The comparison across modes is the argument: an identical false-positive rate is an analyst's annoyance in detection mode and a customer-facing outage in blocking mode, which is why precision must be measured on real traffic before blocking is enabled.

**Negative test:** Enabling blocking estate-wide on default rules at go-live. The first false positive lands on a paying customer, and the control gets disabled entirely rather than tuned.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.3 — Plan remediation with DQL

**Objective:** Turn findings into an ordered, defensible plan.

```bash
python3 - <<'EOF'
print("DQL — find internet-facing services with reachable, exploitable vulnerabilities:\n")
print('  fetch events, from:-7d')
print('  | filter event.kind == "SECURITY_EVENT"')
print('  | filter vulnerability.risk.level == "CRITICAL"')
print('       and vulnerability.davis_assessment.exposure_status == "PUBLIC_NETWORK"')
print('       and vulnerability.davis_assessment.data_assets_status == "REACHABLE"')
print('  | summarize affected = countDistinct(affected_entity.id), by:{vulnerability.title}')
print('  | sort affected desc\n')

BACKLOG = [
  # title,                     affected, fix_type,    effort_days, blocked_by
  ("CVE-2026-1111 json-parse",   14, "dependency bump", 0.5, None),
  ("SQLi in /admin/search",       1, "code change",     3.0, None),
  ("CVE-2026-2222 tls-lib",      31, "dependency bump", 1.0, "vendor image rebuild"),
  ("Command injection in report", 2, "code change",     5.0, None),
  ("CVE-2026-3333 log4j-like",    8, "dependency bump", 0.5, None),
]
print("Remediation plan — ordered by affected services per day of effort:\n")
rows = sorted(BACKLOG, key=lambda r: -(r[1]/r[3]))
print(f"{'finding':32}{'services':>9}{'days':>6}{'svc/day':>9}   note")
for t, n, kind, days, blocked in rows:
    note = f"BLOCKED: {blocked}" if blocked else kind
    print(f"{t:32}{n:>9}{days:>6.1f}{n/days:>9.1f}   {note}")

print("\nDependency bumps dominate the top of the list — high blast radius, low effort.")
print("Code changes sit lower not because they matter less but because they are slower;")
print("they need to START now precisely because they will not finish this week.")
print("\nThe blocked item is the one to escalate today. It affects the most services")
print("(31) and no amount of team effort moves it — it needs the vendor. Ranking by")
print("effort alone would bury it; ranking by impact alone would hide that it is stuck.")
EOF
```

**Expected result:** Dependency bumps rank highest on services-fixed-per-day, with the vendor-blocked item flagged despite affecting the most services. The final observation is the practical one — a plan sorted purely by impact or purely by effort loses the blocked item, and a finding nobody on your team can fix is the one that most needs escalating today.

**Negative test:** Working the backlog in CVSS order. You spend the week on a 3-day code fix affecting one service while a half-day dependency bump affecting fourteen waits.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Runtime vulnerability analytics used to re-rank, not to suppress, findings.
- [ ] Third-party and code-level vulnerabilities distinguished by fix path.
- [ ] Blocking treated as an availability decision, enabled only after measuring precision.
- [ ] Security events queried with DQL and turned into an ordered remediation plan.
