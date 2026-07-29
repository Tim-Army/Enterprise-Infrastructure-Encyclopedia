# Chapter 03: Network Security — Professional and Analyst

## Learning Objectives

- Explain the Network Security Professional and Analyst credentials.
- Configure PAN-OS security policy using App-ID, User-ID, and Content-ID.
- Apply Security Profiles for threat prevention.
- Read firewall state and logs via the PAN-OS API.
- Complete a walkthrough for each Network Security foundation topic.

## Theory and Architecture

The **Network Security Professional** (Professional) and **Network Security Analyst**
(Specialist) credentials cover the core of Palo Alto's next-generation firewall: **PAN-OS**
running **single-pass parallel processing**, where traffic is classified once and all controls
apply together. The defining technologies are **App-ID** (identifies the application regardless
of port/protocol), **User-ID** (maps traffic to a user identity), and **Content-ID**
(inspects content for threats, URLs, and data patterns). Security policy is written on
**applications and users**, not ports, and **Security Profiles** (Antivirus, Anti-Spyware,
Vulnerability Protection, URL Filtering, WildFire, File Blocking, Data Filtering) attach threat
prevention to allowed traffic. The Analyst role adds operational depth — monitoring, log
analysis, and troubleshooting. Everything is administrable via CLI, the **XML/REST API**, and
the **pan-os-python** SDK.

## Design Considerations

Write policy on **App-ID and User-ID**, not ports — a port-based rule is blind to what actually
flows. Attach **Security Profiles** to every allow rule so permitted traffic is still inspected.
Default to **deny** and allow explicitly. Use the **API** for automation and monitoring at scale.

## Implementation and Automation

The labs configure an App-ID/User-ID rule, attach a Security Profile, and query firewall state
and logs via the API. All actions are **authorized administration and monitoring**.

## Validation and Troubleshooting

Confirm the policy model:

```text
PAN-OS single-pass: classify once, apply all controls together.
App-ID (application) + User-ID (identity) + Content-ID (threat/URL/data) -> policy on apps+users.
Security Profiles: AV, Anti-Spyware, Vuln Protection, URL Filtering, WildFire, File Blocking, Data Filtering.
Default deny; allow explicitly; inspect every allow.
```

Common pitfalls: **port-based** rules (App-ID sees the real app); and **allow** rules with **no
Security Profile** (permitted traffic goes uninspected).

## Security and Best Practices

Least-privilege policy on **apps and users**, threat **inspection on every allow**, and a final
**deny** with logging. Keep signatures/WildFire current. Restrict and audit admin/API access.
These are defensive administration practices.

## Hands-On Lab

Network Security walkthroughs. **Shared prerequisites** — a PAN-OS firewall (physical, or the
VM-Series/PAN-OS in a lab) with API access, in an **authorized** environment. **Cost:** none
with a lab VM.

### Lab 3.1 — Security policy on App-ID and User-ID

**Objective:** Allow an application for a user group by identity.

```text
admin@fw> configure
admin@fw# set rulebase security rules Allow-Web from trust to untrust \
    source any destination any application [ ssl web-browsing ] service application-default \
    source-user "corp\\employees" action allow
admin@fw# set rulebase security rules Allow-Web profile-setting group best-practice
admin@fw# commit
```

**Expected result:** a rule permitting web apps for the **employees** group by **App-ID** and
**User-ID** with profiles attached — identity- and application-based policy.

**Negative test:** write `service tcp/443 action allow` with no App-ID; that trusts the port —
use **App-ID** so only the real application is allowed.

**Cleanup:** `delete rulebase security rules Allow-Web` then `commit`.

### Lab 3.2 — Attach a threat-prevention profile

**Objective:** Inspect allowed traffic with Security Profiles.

```text
admin@fw# set profile-group best-practice virus default anti-spyware strict \
    vulnerability strict url-filtering default wildfire-analysis default
admin@fw# set rulebase security rules Allow-Web profile-setting group best-practice
admin@fw# commit
```

**Expected result:** the allow rule now applies **AV, Anti-Spyware, Vulnerability, URL, and
WildFire** inspection — threat prevention on permitted traffic.

**Negative test:** allow traffic with no profile group; permitted traffic is **uninspected** —
attach profiles to every allow.

**Cleanup:** remove the profile-setting from the rule and `commit`.

### Lab 3.3 — Read policy via the PAN-OS API

**Objective:** Retrieve the running security rules over the API.

```bash
curl -sk "https://<fw>/api/?type=op&cmd=<show><running><security-policy></security-policy></running></show>&key=$PANOS_KEY" 2>/dev/null \
  | python3 -c "import sys;print('security-policy retrieved' if 'response' in sys.stdin.read() else 'query the PAN-OS XML API for running policy')" 2>/dev/null \
  || echo "PAN-OS exposes config/op state via the XML API (type=op / type=config) with an API key"
```

**Expected result:** the running security policy returned by the **PAN-OS XML API** — the
firewall is programmable for automation and audit.

**Negative test:** screen-scrape the GUI to audit rules; the **API** returns structured output —
use it.

**Cleanup:** none (read-only).

### Lab 3.4 — Query traffic logs by application

**Objective:** Analyze what App-ID observed (Analyst skill).

```bash
curl -sk "https://<fw>/api/?type=log&log-type=traffic&query=(app eq ssl)&key=$PANOS_KEY" 2>/dev/null \
  | python3 -c "import sys;print('traffic log job queued' if 'response' in sys.stdin.read() else 'use type=log to query traffic logs by App-ID/user')" 2>/dev/null \
  || echo "PAN-OS log API: type=log&log-type=traffic&query=(app eq ...) for App-ID-based analysis"
```

**Expected result:** a traffic-log query filtered by **App-ID** — the analyst view of what the
firewall saw.

**Negative test:** analyze by destination port alone; **App-ID** identifies the real
application — query by app.

**Cleanup:** none (read-only).

### Lab 3.5 — pan-os-python automation

**Objective:** Manage the firewall from Python.

```python
from panos.firewall import Firewall
from panos.policies import Rulebase, SecurityRule
fw = Firewall("10.0.0.1", api_key="$PANOS_KEY")
rb = Rulebase(); fw.add(rb)
rule = SecurityRule(name="Allow-DNS", application=["dns"], action="allow",
                    fromzone=["trust"], tozone=["untrust"])
rb.add(rule); rule.create()
print("rule created via pan-os-python")
```

**Expected result:** a rule created through the **pan-os-python** SDK — programmatic,
repeatable firewall administration.

**Negative test:** paste CLI over SSH for bulk changes; the **SDK/API** is structured and
idempotent — use it.

**Cleanup:** `rule.delete()`.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Network Security Professional and Analyst credentials cover PAN-OS single-pass policy built
on App-ID, User-ID, and Content-ID, with Security Profiles inspecting every allow, all
administrable via CLI, API, and pan-os-python. Write policy on apps and users, inspect every
allow, and default to deny.

- [ ] I can write policy on App-ID and User-ID.
- [ ] I can attach threat-prevention Security Profiles.
- [ ] I can read policy and logs via the PAN-OS API.
- [ ] I can automate the firewall with pan-os-python.
- [ ] I completed Labs 3.1–3.5 including each negative test.
