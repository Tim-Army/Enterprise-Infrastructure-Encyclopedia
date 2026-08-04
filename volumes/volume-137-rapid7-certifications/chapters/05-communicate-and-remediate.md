# Chapter 05: Communicate and Remediate

## Learning Objectives

- Set and track remediation SLAs that reflect risk.
- Build remediation projects and hand work to the teams that own the fix.
- Report to technical and executive audiences without distorting the picture.
- Verify remediation rather than trusting a closed ticket.

## Security finds, other teams fix

The uncomfortable structural fact of vulnerability management: **the security team almost never applies the patch.** Server owners, application teams, and desktop engineering do. So the last two stages of the lifecycle — **Communicate** and **Remediate** — are fundamentally about handing work to people who do not report to you, in a form they can act on.

That reframes the deliverable. A report that proves the security team did its job is worthless if it does not cause a fix. What causes a fix is a short list, with an owner, a due date, and the specific action required.

## SLAs

Remediation **SLAs** set the time allowed per risk tier, and the exam-relevant discipline is that the clock and the tiers must be defined and then *measured*:

| Tier | Typical window | Basis |
|:---|:---|:---|
| Known-exploited / critical, exposed | Days | Active danger |
| Critical, internal | Weeks | High severity, lower exposure |
| High | Weeks to a month | |
| Medium/low | Next maintenance cycle, or accepted | Often more costly to fix than to accept |

**Aging** — how long open findings have been open — matters more than the raw count. A stable count with rising average age means you are closing easy findings and accumulating hard ones, which a count-only dashboard shows as "steady."

## Exceptions and risk acceptance

Some findings will not be fixed: a vendor appliance nobody may patch, a legacy application, a compensating control that makes the fix unnecessary. That is legitimate, and it needs to be **explicit**: a recorded exception, with a named accepting owner, a stated reason, a compensating control if any, and an **expiry date**.

An exception without an expiry is a permanent silent acceptance, which is how estates accumulate risk that nobody ever revisits.

## Verify, do not trust

A ticket marked "done" is a claim. Verification is a rescan that confirms the finding is gone. The gap between the two is real and common — patches that require a reboot nobody performed, changes applied to the wrong host, fixes that regressed at the next deployment.

## Hands-On Lab

Python models the remediation stage. **Cost:** none.

### Lab 5.1 — SLA tracking and aging

**Objective:** Show why aging beats counting.

```bash
python3 - <<'EOF'
SLA_DAYS = {"known-exploited":7, "critical":30, "high":60, "medium":180}
findings = [
  {"id":"F1","tier":"known-exploited","age":3},
  {"id":"F2","tier":"known-exploited","age":19},
  {"id":"F3","tier":"critical","age":12},
  {"id":"F4","tier":"critical","age":47},
  {"id":"F5","tier":"high","age":88},
  {"id":"F6","tier":"medium","age":150},
]
breached = []
for f in findings:
    sla = SLA_DAYS[f["tier"]]
    over = f["age"] - sla
    status = f"BREACHED by {over}d" if over > 0 else f"{sla-f['age']}d remaining"
    if over > 0: breached.append(f)
    print(f"{f['id']} {f['tier']:16} age {f['age']:>3}d / SLA {sla:>3}d -> {status}")

print(f"\n{len(breached)}/{len(findings)} breached: {[f['id'] for f in breached]}")

print("\n--- why AGING matters more than COUNT ---")
months = [
  {"month":"Jan","open":420,"avg_age":22},
  {"month":"Feb","open":415,"avg_age":31},
  {"month":"Mar","open":418,"avg_age":44},
]
for m in months:
    print(f"{m['month']}: {m['open']} open, average age {m['avg_age']}d")
print("\nThe COUNT looks stable (~418) and a count-only dashboard reports 'holding steady'.")
print("Average age is climbing 22 -> 44 days: easy findings close, hard ones accumulate.")
print("The estate is getting worse while the headline number says it is not.")
EOF
```

**Expected result:** Three SLA breaches, and a three-month trend where a flat open count conceals average age doubling. That concealment is the reporting failure this lab exists to expose — the count is the number executives ask for, and on its own it is capable of showing improvement while the estate degrades.

**Negative test:** Reporting only open-finding counts month over month — the metric is stable by construction (new findings roughly replace closed ones) and tells you nothing about whether the hard problems are being solved.

**Cleanup:** None.

### Lab 5.2 — Route remediation to the team that owns the fix

**Objective:** Turn findings into owned, actionable work.

```bash
python3 - <<'EOF'
OWNERSHIP = {
  "windows-server": ("Server Engineering", "patch via WSUS/SCCM ring"),
  "linux-server":   ("Platform Team",      "patch via configuration management"),
  "workstation":    ("Desktop Engineering","patch via endpoint management"),
  "network-device": ("Network Team",       "firmware upgrade in change window"),
  "application":    ("App Team (owner)",   "dependency upgrade + redeploy"),
  "appliance":      ("Vendor / Ops",       "vendor patch — often EXCEPTION territory"),
}
findings = [
  {"id":"F1","asset":"dc-01","type":"windows-server","fix":"KB5031234"},
  {"id":"F2","asset":"web-prod-01","type":"application","fix":"upgrade openssl 3.0.13"},
  {"id":"F3","asset":"sw-core-1","type":"network-device","fix":"firmware 17.9.4"},
  {"id":"F4","asset":"laptop-11","type":"workstation","fix":"browser update"},
  {"id":"F5","asset":"ot-hmi-2","type":"appliance","fix":"vendor patch pending"},
]
projects = {}
for f in findings:
    owner, method = OWNERSHIP[f["type"]]
    projects.setdefault(owner, []).append((f["id"], f["asset"], f["fix"], method))

for owner, items in projects.items():
    print(f"\nREMEDIATION PROJECT -> {owner}  ({len(items)} item(s))")
    for fid, asset, fix, method in items:
        print(f"   {fid}  {asset:12} action: {fix:26} via {method}")
print("\nSecurity does not apply these fixes — the owning teams do. A finding without a named")
print("owner and a concrete action is not work; it is a complaint, and it will not get done.")
EOF
```

**Expected result:** Five findings become five owned projects, each with the concrete action and the delivery mechanism that team already uses. The point in the closing lines is organizational rather than technical: routing by asset type to the team that owns the remediation path is what converts a security observation into scheduled engineering work.

**Negative test:** Emailing the whole findings report to a distribution list — nobody is named, so nobody is accountable, and the natural response is that everyone assumes someone else owns it.

**Cleanup:** None.

### Lab 5.3 — Verify remediation and manage exceptions

**Objective:** Confirm fixes and give exceptions an expiry.

```bash
python3 - <<'EOF'
import datetime
today = datetime.date(2026, 8, 4)

tickets = [
  {"id":"F1","status":"closed","rescan_confirms_fixed":True,  "note":"patched + rebooted"},
  {"id":"F2","status":"closed","rescan_confirms_fixed":False, "note":"patch applied, REBOOT PENDING"},
  {"id":"F3","status":"closed","rescan_confirms_fixed":False, "note":"applied to the wrong host"},
]
print("=== verification ===")
for t in tickets:
    if t["rescan_confirms_fixed"]:
        print(f"{t['id']}: VERIFIED closed — rescan confirms the finding is gone ({t['note']})")
    else:
        print(f"{t['id']}: STILL OPEN despite a closed ticket — {t['note']}")
        print(f"      reopen; a ticket status is a CLAIM, a rescan is EVIDENCE")

exceptions = [
  {"id":"E1","reason":"vendor appliance, no patch available","owner":"J. Smith","control":"network isolation","expires":datetime.date(2026,12,31)},
  {"id":"E2","reason":"legacy app, upgrade planned","owner":"R. Patel","control":"WAF rule","expires":datetime.date(2026,6,30)},
  {"id":"E3","reason":"accepted risk","owner":"unassigned","control":None,"expires":None},
]
print("\n=== exceptions ===")
for e in exceptions:
    if e["expires"] is None:
        print(f"{e['id']}: INVALID — no expiry and owner '{e['owner']}'. A permanent, unowned")
        print( "      exception is silent risk acceptance nobody will ever revisit.")
    elif e["expires"] < today:
        print(f"{e['id']}: EXPIRED {(today-e['expires']).days}d ago — must be re-reviewed or the finding reopens")
    else:
        print(f"{e['id']}: valid until {e['expires']} — owner {e['owner']}, control: {e['control']}")
EOF
```

**Expected result:** Two of three "closed" tickets are still open on rescan — a pending reboot and a fix applied to the wrong host, both extremely common — and one exception is invalid for having neither owner nor expiry while another has quietly lapsed. Together these are the two ways a vulnerability program's numbers drift from reality: unverified closures and immortal exceptions.

**Negative test:** Closing findings on ticket status alone — your metrics improve, the vulnerabilities remain, and the discrepancy surfaces during an incident or an audit rather than during remediation.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] SLAs set per risk tier, with aging tracked alongside counts.
- [ ] Findings routed into owned remediation projects with concrete actions.
- [ ] Remediation verified by rescan rather than by ticket status.
- [ ] Exceptions recorded with owner, compensating control, and a mandatory expiry.
