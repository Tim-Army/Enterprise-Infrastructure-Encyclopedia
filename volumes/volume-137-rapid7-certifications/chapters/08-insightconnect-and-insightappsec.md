# Chapter 08: InsightConnect (SOAR) and InsightAppSec

## Learning Objectives

- Build automation playbooks with appropriate human decision points.
- Choose what to automate and what must stay manual.
- Scope and schedule dynamic application security testing.
- Handle authenticated web-application scanning safely.

## Two exams in one chapter

**InsightConnect (Rapid7 Automation) Certified Specialist** and **InsightAppSec (Rapid7 Application Security) Certified Specialist** cover different products, and they share a theme: both **act on** systems, so both need careful scoping.

## InsightConnect: orchestration and automation

SOAR turns a written runbook into an executable **playbook**: a trigger, some enrichment, a decision, and actions.

| Playbook element | Purpose |
|:---|:---|
| **Trigger** | The alert or event that starts it |
| **Enrichment** | Gather context — asset owner, user, threat intel, recent activity |
| **Decision** | Branch on the enriched facts |
| **Action** | Do something: notify, ticket, block, isolate, disable |
| **Human step** | Pause for a person to approve a consequential action |

**Enrichment is where SOAR earns its keep, unambiguously.** Automatically gathering the five facts an analyst would otherwise look up by hand saves minutes per alert at zero risk, because gathering information changes nothing.

Actions are where judgment is required. The automation question is not "can this be automated?" but **"what is the cost of this firing on a false positive?"**

| Action | Cost if wrong | Automate? |
|:---|:---|:---|
| Enrich and attach context | None | **Always** |
| Open a ticket | Trivial | **Yes** |
| Notify the analyst | Trivial | **Yes** |
| Block an external IP | Small, reversible | Usually |
| Quarantine a workstation | One person cannot work | With care, often with approval |
| Disable a user account | That person stops working | **Human approval** |
| Isolate a production server | Potential outage | **Human approval** |

Automating containment on a detection with 30% precision means being wrong seven times in ten — and each of those is a self-inflicted outage. The precision measurement from Chapter 07 is precisely what tells you whether a detection is trustworthy enough to automate.

## InsightAppSec: dynamic application scanning

**InsightAppSec** is DAST — it exercises a **running** web application looking for exploitable behavior, complementing the static analysis in a CI pipeline (see [GitLab Chapter 06](../../volume-136-gitlab-certifications/chapters/06-security-scanning-and-compliance.md)).

Practical concerns:

- **Scope precisely.** A crawler that wanders outside the intended host can scan systems you do not own — which is at best rude and at worst unlawful. Scope is the first thing to get right.
- **Authenticate.** Most of an application is behind login; an unauthenticated scan tests the login page and little else.
- **Beware destructive actions.** A scanner submitting every form will create, modify, and delete data. Scan non-production where possible, and use test accounts.
- **Rate-limit.** A thorough scan can look exactly like a denial-of-service attempt to the application and its defenses.

## Hands-On Lab

Python models automation and DAST scoping. **Cost:** none.

### Lab 8.1 — Playbook branching with a human gate

**Objective:** Decide which actions fire automatically.

```bash
python3 - <<'EOF'
AUTO_SAFE = {"enrich","ticket","notify","block_ip"}
NEEDS_HUMAN = {"quarantine_host","disable_user","isolate_server"}

def playbook(alert):
    steps = ["TRIGGER: " + alert["name"],
             "ENRICH: asset owner, user, threat intel, recent activity  [automatic, zero risk]"]
    for action in alert["proposed_actions"]:
        if action in AUTO_SAFE:
            steps.append(f"AUTO: {action}")
        elif alert["detection_precision"] >= 90 and alert["severity"] == "critical":
            steps.append(f"AUTO (precision {alert['detection_precision']}%): {action}"
                         "  — justified only by a highly reliable detection")
        else:
            steps.append(f"HOLD FOR HUMAN: {action}  — precision {alert['detection_precision']}%; "
                         f"automating this is wrong {100-alert['detection_precision']}% of the time")
    return steps

alerts = [
  {"name":"Known-exploited CVE on internet-facing host","detection_precision":98,"severity":"critical",
   "proposed_actions":["ticket","block_ip"]},
  {"name":"Impossible travel","detection_precision":28,"severity":"high",
   "proposed_actions":["notify","disable_user"]},
  {"name":"Honey credential used","detection_precision":99,"severity":"critical",
   "proposed_actions":["notify","quarantine_host"]},
]
for a in alerts:
    print(f"\n=== {a['name']} ===")
    for s in playbook(a): print(f"   {s}")
print("\nThe deciding question is never 'can this be automated?' but 'what does it cost when")
print("this fires on a false positive?'. Impossible travel at 28% precision would disable")
print("the wrong user's account roughly 7 times in 10.")
EOF
```

**Expected result:** Enrichment, tickets, notifications, and IP blocks fire automatically; the 28%-precision impossible-travel alert holds its account-disable for a human; the 99%-precision honey-credential alert earns automated quarantine. The link back to Chapter 07 is deliberate — **measured precision is the input that decides what may be automated**, which is why the two chapters belong together.

**Negative test:** Automating containment because the product supports it — a noisy detection wired to a disruptive action produces self-inflicted outages, and the team's response is to disable the automation entirely, losing the good cases too.

**Cleanup:** None.

### Lab 8.2 — Scope a DAST scan safely

**Objective:** Keep the scanner inside the intended target.

```bash
python3 - <<'EOF'
SCOPE = {"include":["https://app.example.com/"], "exclude":["https://app.example.com/admin/delete",
                                                            "https://app.example.com/api/v1/payments"]}
crawled = [
  "https://app.example.com/login",
  "https://app.example.com/search?q=test",
  "https://app.example.com/admin/delete?id=42",
  "https://cdn.thirdparty.net/lib.js",
  "https://partner-api.example.org/v2/orders",
  "https://app.example.com/api/v1/payments",
]
for url in crawled:
    in_scope = any(url.startswith(i) for i in SCOPE["include"])
    excluded = any(url.startswith(e) for e in SCOPE["exclude"])
    if not in_scope:
        print(f"BLOCKED  {url}")
        print("         OUT OF SCOPE — a different host. Scanning it without authorization is")
        print("         at best rude and potentially unlawful; the crawler must never wander.")
    elif excluded:
        print(f"SKIPPED  {url}")
        print("         explicitly excluded — destructive or financial endpoint")
    else:
        print(f"SCAN     {url}")
print("\nDAST exercises a RUNNING app: it submits forms, follows links, and triggers actions.")
print("Scope first, exclude destructive endpoints, use test accounts, and rate-limit —")
print("a thorough scan looks exactly like an attack to the application and its defenses.")
EOF
```

**Expected result:** Two in-scope URLs scanned, two destructive endpoints skipped, and two third-party hosts blocked outright. The authorization point is the serious one: a DAST crawler following links off-host will scan systems belonging to other parties, and "the scanner did it automatically" is not a defense.

**Negative test:** Pointing a scanner at production with no exclusions and a privileged account — it will submit every form it finds, which means creating, modifying, and deleting real data.

**Cleanup:** None.

### Lab 8.3 — Authenticated scanning coverage

**Objective:** Show how much of an application is invisible without login.

```bash
python3 - <<'EOF'
app_surface = {
  "public pages (login, marketing)": {"endpoints":8,  "needs_auth":False},
  "user dashboard":                  {"endpoints":34, "needs_auth":True},
  "reporting":                       {"endpoints":21, "needs_auth":True},
  "admin console":                   {"endpoints":45, "needs_auth":True},
  "API (authenticated)":             {"endpoints":62, "needs_auth":True},
}
total = sum(a["endpoints"] for a in app_surface.values())
unauth = sum(a["endpoints"] for a in app_surface.values() if not a["needs_auth"])
print(f"{'area':34}{'endpoints':>10}{'unauth sees':>13}")
for name, a in app_surface.items():
    print(f"{name:34}{a['endpoints']:>10}{(a['endpoints'] if not a['needs_auth'] else 0):>13}")
print(f"{'TOTAL':34}{total:>10}{unauth:>13}")
print(f"\nUnauthenticated scanning reaches {unauth}/{total} = {unauth/total*100:.0f}% of the application.")
print("The other 95% — dashboards, reporting, admin, and the API — is behind login and simply")
print("not tested. Configure authentication, and verify the scanner STAYS logged in:")
print("a session that expires mid-scan silently reverts you to the 5% result.")
EOF
```

**Expected result:** An unauthenticated scan covers 8 of 170 endpoints — under 5% of the application. The warning about session expiry is the practical trap: a scan configured with credentials that logs out partway through produces a report that *looks* authenticated while covering almost nothing, and nothing in the output announces it.

**Negative test:** Accepting a clean DAST report without checking authenticated coverage — the low finding count reflects the scanner never getting past the login page.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Playbooks built with automatic enrichment and human gates on consequential actions.
- [ ] Automation decisions tied to measured detection precision.
- [ ] DAST scoped precisely, with destructive endpoints excluded and third-party hosts blocked.
- [ ] Authenticated scanning configured and session persistence verified.
