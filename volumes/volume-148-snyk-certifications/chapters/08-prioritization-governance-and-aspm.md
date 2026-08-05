# Chapter 08: Prioritization, Governance, and ASPM

## Learning Objectives

- Explain risk-based prioritization — exploit maturity and reachability.
- Understand ASPM — application security posture across the whole SDLC.
- Describe policies and CI/CD gates that scale governance.
- Recognize the operating model that turns scanning into risk reduction.

*Cert relevance: prioritization and ASPM are the operational layer — and the Enterprise Admin & Architecture learning path.*

## The prioritization problem

Across four engines, Snyk can find a great many issues — and, exactly as in the [Wiz volume (CXLVII)](../../volume-147-wiz-certifications/chapters/03-attack-paths-and-toxic-combinations.md), **raw counts and CVSS severity are not a work queue.** A "critical" CVE in a dependency you never actually call is lower risk than a "medium" in a function on your main request path. Prioritization needs **context beyond severity**.

Snyk's **priority score** blends signals:

| Signal | Question |
|:---|:---|
| **Severity** | How bad is the flaw itself (CVSS)? |
| **Exploit maturity** | Does a *known exploit* exist in the wild (not just theoretical)? |
| **Reachability** | Does your code actually *call* the vulnerable function? |
| **Fixability** | Is there a fix available (an upgrade)? |

**Reachability** is the sharp one: a vulnerability in an imported library that your code **never calls** is not exploitable through your app — the vulnerable function is dead weight, not a live risk. Snyk's reachability analysis distinguishes "vulnerable and *called*" from "vulnerable and *dormant*," which reorders the queue dramatically. The lab models it.

## ASPM

**Application Security Posture Management (ASPM)** is the cross-cutting layer: instead of four separate scanners' outputs, ASPM gives a **posture view across the whole SDLC and application portfolio** — which applications exist, which are business-critical, which have security coverage, where the gaps are, and how risk trends over time. It answers the leadership question the individual scanners cannot: "**across all our apps, where is our risk, and is it getting better?**"

ASPM also addresses **coverage** — the meta-risk that some applications are not being scanned at all. A perfect scanner on 60% of your apps leaves 40% dark; ASPM surfaces the untested apps, which is often where the real exposure hides (the [agentless-coverage lesson (CXLVII)](../../volume-147-wiz-certifications/chapters/02-cnapp-and-the-security-graph.md) applied to AppSec). The lab is covered within the prioritization exercise and the governance discussion.

## Governance and CI/CD gates

The enforcement layer is **policies and gates**: rules like "fail the build if a new *critical, exploitable, reachable* vulnerability is introduced" run in the **CI/CD pipeline**, stopping risky changes before they merge or deploy — while *not* blocking on the low-priority noise. The art is gating on the *right* threshold: gate too loosely and risk ships; gate too strictly and developers route around the tool (the [adoption lesson, Chapter 2](02-developer-first-application-security.md)). Good governance gates on **prioritized** risk — the exploitable, reachable, fixable issues — so the gate is credible and developers keep it on. The lab models the gate threshold.

## Hands-On Lab

Python models prioritization and gating. **Cost:** none.

### Lab 8.1 — Priority score with reachability

**Objective:** Reorder findings by context, not CVSS.

```bash
python3 - <<'EOF'
FINDINGS = [
  # id,      severity(CVSS), exploit_in_wild, reachable(you call it), fixable
  ("V1",     9.8,            False,           False,                  True),   # critical but dormant + no exploit
  ("V2",     6.5,            True,            True,                   True),   # medium but EXPLOITED + reachable
  ("V3",     9.1,            True,            True,                   True),   # critical + exploited + reachable
  ("V4",     7.5,            False,           True,                   False),  # reachable, no fix yet
  ("V5",     8.8,            False,           False,                  True),   # critical but NOT reachable
]
def priority(f):
    _, sev, exploit, reach, fix = f
    score = sev
    if exploit: score += 4          # a real-world exploit exists -> urgent
    if reach:   score += 5          # your code actually calls it -> live
    if not reach: score -= 4        # dormant -> deprioritize
    if fix:     score += 1          # fixable now -> actionable
    return score
print("CVSS-only ranking (what a naive tool shows):")
for fid, sev, *_ in sorted(FINDINGS, key=lambda x: -x[1]):
    print(f"   CVSS {sev}  {fid}")
print("   -> you'd fix V1 (9.8) first. But V1 is DORMANT (you never call it) with no")
print("      known exploit. Busywork.\n")
print("Snyk priority score (severity + exploit maturity + REACHABILITY + fixability):")
for f in sorted(FINDINGS, key=lambda x: -priority(x)):
    fid, sev, exploit, reach, fix = f
    tags = []
    if reach: tags.append("reachable")
    else: tags.append("DORMANT")
    if exploit: tags.append("exploited-in-wild")
    if not fix: tags.append("no-fix-yet")
    print(f"   score {priority(f):>5.1f}  {fid} (CVSS {sev})  [{', '.join(tags)}]")
print("\n   -> V3 and V2 rise to the top: EXPLOITED in the wild AND REACHABLE (your")
print("      code calls them). V1 and V5 sink: critical CVSS but DORMANT — the")
print("      vulnerable function is never called, so it's not exploitable through your app.")
print("\nReachability is the sharp signal: a critical vuln in a library function you")
print("NEVER CALL is dead weight, not live risk. A medium that's exploited in the wild")
print("AND on your request path is urgent. Severity ranks the FLAW; priority ranks the")
print("RISK to YOUR app. Same lesson as Wiz attack-paths (CXLVII) — context beats CVSS.")
EOF
```

**Expected result:** CVSS ranking putting a dormant critical first, while Snyk's priority score surfaces the exploited-and-reachable findings and sinks the unreachable criticals. The reachability lesson is that a vulnerability in a function your code never calls is not live risk — priority blends severity with exploit maturity, reachability, and fixability, the same context-beats-CVSS discipline as Wiz's attack paths.

**Negative test:** Patching by CVSS severity. The 9.8 is in a dormant, never-called function with no known exploit, while a reachable, actively-exploited medium waits — severity ranks the flaw, not the risk to your application.

**Cleanup:** None.

### Lab 8.2 — Gate on prioritized risk, not on noise

**Objective:** Set a CI/CD gate developers keep on.

```bash
python3 - <<'EOF'
import random
random.seed(8)
# a PR introduces some new findings; what should FAIL the build?
new_findings = [
  {"id": f"F{i}", "sev": random.choice([3,5,7,9]),
   "exploit": random.random()<0.2, "reachable": random.random()<0.4, "fixable": random.random()<0.8}
  for i in range(20)
]
def is_urgent(f): return f["sev"]>=7 and f["exploit"] and f["reachable"] and f["fixable"]
def any_critical(f): return f["sev"]>=7

print("A pull request introduces 20 new findings. What should the CI gate do?\n")
gate_all = [f for f in new_findings if any_critical(f)]
gate_smart = [f for f in new_findings if is_urgent(f)]
print(f"GATE ON 'any high/critical CVSS': would BLOCK on {len(gate_all)} findings")
print("   -> blocks constantly, including dormant/unexploitable criticals. Devs get")
print("      the tool DISABLED or the check marked non-blocking. Governance dies.\n")
print(f"GATE ON 'critical + exploited + reachable + fixable': blocks on {len(gate_smart)}")
print("   -> blocks only on genuinely urgent, ACTIONABLE risk (and there's a fix to")
print("      apply). The gate is credible, so it stays ON and actually stops bad code.\n")
print("The governance art: gate on PRIORITIZED risk, not raw severity.")
print("  too loose  -> real risk ships")
print("  too strict -> devs route around the tool (mark it non-blocking) and you get")
print("                NEITHER security nor velocity")
print("  just right -> block on exploitable + reachable + fixable; warn on the rest.")
print("\nA gate developers KEEP ON beats a strict gate they disable. Credibility is a")
print("security property (Chapter 2 again): the gate only reduces risk while it's")
print("enabled, and it only stays enabled if it blocks on things devs agree are real.")
EOF
```

**Expected result:** A CVSS-only gate blocking on many findings (including dormant criticals) that developers disable, versus a gate on exploitable-reachable-fixable risk that blocks on few and stays enabled. The gating lesson is to gate on prioritized risk — a credible gate developers keep on reduces more risk than a strict one they mark non-blocking, making gate credibility itself a security property.

**Negative test:** Gating the build on any high/critical CVSS finding. It blocks constantly on dormant, unexploitable issues, so developers mark the check non-blocking — and then it stops nothing; gating on prioritized risk keeps the gate credible and enabled.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Risk-based prioritization understood — severity plus exploit maturity, reachability, and fixability, with reachability the sharp signal.
- [ ] ASPM understood as posture across the whole SDLC and portfolio, including scan-coverage gaps.
- [ ] Policies and CI/CD gates understood as governance that must gate on prioritized risk to stay credible.
- [ ] The operating model recognized as what turns four scanners into actual, sustained risk reduction.
