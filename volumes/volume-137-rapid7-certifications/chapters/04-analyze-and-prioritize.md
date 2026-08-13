# Chapter 04: Analyze and Prioritize

## Learning Objectives

- Explain why raw CVSS is a poor prioritization key on its own.
- Combine exploitability, exposure, and asset criticality into a usable risk score.
- Apply threat intelligence (known-exploited status) to reorder a queue.
- Report a queue an engineering team can actually act on.

## The problem: too many findings

A mid-sized estate produces tens of thousands of findings. Nobody fixes tens of thousands of anything, so the entire value of the **Analyze** stage is turning a list into an **order** — and the order determines whether the program reduces risk or merely produces reports.

## Why raw CVSS misleads

**CVSS** (Common Vulnerability Scoring System) rates a vulnerability's intrinsic severity in the abstract. It is genuinely useful and routinely misused as a priority list, because it deliberately excludes the three things that decide whether *your* organization should care:

| CVSS does not know | Why it matters |
|:---|:---|
| **Is it being exploited in the wild?** | A CVSS 9.8 nobody has ever exploited is less urgent than a CVSS 7.5 in active campaigns |
| **Is the affected asset exposed?** | The same flaw on an internet-facing server and on an isolated lab VM are not the same problem |
| **Does the asset matter?** | A domain controller and a test box run the same software at very different stakes |

Rapid7's platform layers exactly these factors on top of the base score — exploitability and threat data, asset exposure, and business criticality — which is the reasoning the InsightVM exam expects you to reproduce. The vendor branding varies across the industry; the logic does not.

## Known-exploited status is the strongest single signal

Of all the modifiers, **evidence of real-world exploitation** moves priority the most. A vulnerability with a public, weaponized exploit and observed campaigns is qualitatively different from one with a theoretical proof of concept, regardless of the base score. Public catalogs of known-exploited vulnerabilities exist precisely because this signal is so much more actionable than severity alone.

## Report an order, not a list

The output of prioritization should be a **short, ordered, owned queue** — the top N items, each with an owner and a due date — rather than an export of everything. A team handed 4,000 findings fixes approximately none; the same team handed the twenty that matter fixes twenty.

## Hands-On Lab

Python models prioritization. **Cost:** none.

### Lab 4.1 — Where raw CVSS sends you wrong

**Objective:** Compare CVSS ordering against context-aware ordering.

```bash
python3 - <<'EOF'
findings = [
  {"id":"F1","cve":"CVE-2025-0001","cvss":9.8,"exploited":False,"internet_facing":False,"asset":"lab-vm-7",     "criticality":1},
  {"id":"F2","cve":"CVE-2025-0002","cvss":7.5,"exploited":True, "internet_facing":True,  "asset":"web-prod-01", "criticality":5},
  {"id":"F3","cve":"CVE-2025-0003","cvss":9.1,"exploited":False,"internet_facing":False,"asset":"print-srv",    "criticality":2},
  {"id":"F4","cve":"CVE-2025-0004","cvss":6.5,"exploited":True, "internet_facing":False,"asset":"dc-01",        "criticality":5},
]
def risk(f):
    score = f["cvss"]
    if f["exploited"]:        score *= 2.0     # actively exploited dominates
    if f["internet_facing"]:  score *= 1.5
    score *= (0.6 + 0.2 * f["criticality"])    # business criticality 1-5
    return round(score, 1)

print("=== ordered by RAW CVSS ===")
for f in sorted(findings, key=lambda x: -x["cvss"]):
    print(f"  {f['id']} cvss {f['cvss']} {f['asset']:12} exploited={str(f['exploited']):5} facing={str(f['internet_facing']):5}")

print("\n=== ordered by CONTEXT-AWARE RISK ===")
for f in sorted(findings, key=lambda x: -risk(x)):
    print(f"  {f['id']} risk {risk(f):>5} (cvss {f['cvss']}) {f['asset']:12} "
          f"exploited={str(f['exploited']):5} facing={str(f['internet_facing']):5} crit={f['criticality']}")

print("\nRaw CVSS puts F1 first — a 9.8 on an isolated lab VM that nobody has ever exploited.")
print("Context puts F2 first: a 7.5 that is ACTIVELY EXPLOITED, INTERNET-FACING, on a critical asset.")
print("Patch F1 first and you have spent the week reducing almost no real risk.")
EOF
```

**Expected result:** The two orderings invert. Raw CVSS leads with a 9.8 on a lab VM; context-aware risk leads with a 7.5 that is actively exploited on an internet-facing production system. The closing line states the cost of getting it wrong — not a wrong answer on paper, but a week of remediation effort spent where it does not reduce exposure.

**Negative test:** Filtering to "critical and high only" and working down by CVSS — F4 (a 6.5 actively exploited on a domain controller) is excluded by the filter entirely.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.2 — Known-exploited status reorders everything

**Objective:** Show the weight of real-world exploitation evidence.

```bash
python3 - <<'EOF'
kev = {"CVE-2025-0002", "CVE-2025-0004"}          # known-exploited catalog
findings = [
  {"cve":"CVE-2025-0001","cvss":9.8,"asset":"lab-vm-7"},
  {"cve":"CVE-2025-0002","cvss":7.5,"asset":"web-prod-01"},
  {"cve":"CVE-2025-0003","cvss":9.1,"asset":"print-srv"},
  {"cve":"CVE-2025-0004","cvss":6.5,"asset":"dc-01"},
  {"cve":"CVE-2025-0005","cvss":8.8,"asset":"app-srv-04"},
]
for f in findings:
    f["known_exploited"] = f["cve"] in kev

ordered = sorted(findings, key=lambda f: (not f["known_exploited"], -f["cvss"]))
print("Queue (known-exploited first, then by severity):\n")
for i, f in enumerate(ordered, 1):
    tag = "KNOWN EXPLOITED" if f["known_exploited"] else "no known exploitation"
    print(f"  {i}. {f['cve']} cvss {f['cvss']} on {f['asset']:12} [{tag}]")

n_kev = sum(f["known_exploited"] for f in findings)
print(f"\n{n_kev} of {len(findings)} findings are known-exploited — those are the ones with")
print("a demonstrated path from 'a flaw exists' to 'an attacker uses it against you'.")
print("Everything else is potential; these are actual. Fix them first regardless of base score.")
EOF
```

**Expected result:** The two known-exploited CVEs rise to the top despite having the *lowest* base scores in the set. The distinction in the closing lines is the one worth internalizing — most vulnerabilities are never exploited at scale, so evidence of exploitation is the closest thing vulnerability management has to a signal of actual, present danger.

**Negative test:** Treating a public catalog of known-exploited vulnerabilities as the complete definition of urgency — it is a floor, not a ceiling; targeted attacks use flaws that never appear in any catalog.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.3 — Produce a queue a team can actually work

**Objective:** Turn thousands of findings into an owned, dated shortlist.

```bash
python3 - <<'EOF'
TOTAL_FINDINGS = 4200
team_capacity_per_sprint = 20

buckets = {
  "known-exploited + internet-facing": 12,
  "known-exploited, internal":         31,
  "critical, internet-facing":         88,
  "critical, internal":               640,
  "everything else":                 3429,
}
print(f"total findings: {TOTAL_FINDINGS}\n")
running = 0
for name, count in buckets.items():
    running += count
    print(f"{name:34} {count:>5}   cumulative {running:>5}")

print(f"\nTeam capacity: {team_capacity_per_sprint} items per sprint.")
print("\n--- what to hand over ---")
top = buckets["known-exploited + internet-facing"]
print(f"Sprint 1 queue: the {top} known-exploited internet-facing findings, each with an OWNER and DUE DATE.")
print(f"NOT the {TOTAL_FINDINGS}-row export.")
print(f"\nAt {team_capacity_per_sprint}/sprint the full backlog is {TOTAL_FINDINGS/team_capacity_per_sprint:.0f} sprints —")
print("roughly 8 years. That number is why prioritization IS the job: the backlog will never")
print("be emptied, so the only question that matters is whether the RIGHT items are at the top.")
EOF
```

**Expected result:** 4,200 findings reduce to a sprint-one queue of **12**, and the arithmetic at the end shows the full backlog would take about eight years at the team's capacity. That figure reframes the work honestly: vulnerability management is not a project that finishes but a continuous triage function, and its quality is measured entirely by what sits at the top of the list.

**Negative test:** Handing engineering the full export with a request to "work through it" — the list is unworkable, so nothing gets prioritized and the highest-risk items receive no more attention than the rest.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Raw CVSS understood as intrinsic severity, not priority.
- [ ] Exploitability, exposure, and asset criticality combined into a context-aware risk order.
- [ ] Known-exploited status applied as the strongest single reprioritization signal.
- [ ] A short, owned, dated queue produced instead of a full export.
