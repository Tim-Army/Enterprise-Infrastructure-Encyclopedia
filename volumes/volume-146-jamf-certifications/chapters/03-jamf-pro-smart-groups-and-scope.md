# Chapter 03: Jamf Pro — Smart Groups and Scope

## Learning Objectives

- Explain the Jamf Pro inventory model and extension attributes.
- Design Smart Groups — dynamic membership from inventory criteria.
- Understand scoping: how policies and profiles target devices.
- Recognize the scope mistakes that deploy the right change to the wrong devices.

*Cert relevance: Smart Groups and scope are the heart of the **Jamf 200/300** (Tech/Admin) certifications — the mechanism everything else targets through.*

## Inventory: the foundation

Everything in Jamf Pro starts with **inventory** — what Jamf knows about each device: hardware, OS version, installed apps, storage, and whatever custom facts you collect. Jamf gathers this automatically and on a schedule, and **extension attributes** let you collect *anything else* a script can determine (a specific file's presence, a registry-like setting, a compliance check result).

Inventory is the foundation because **everything targets through it**: you do not assign a policy to "these 40 specific Macs" — you assign it to a *Smart Group* defined by inventory criteria, and membership follows the facts. Get the inventory model right and the rest of Jamf composes cleanly; get it wrong and you are managing device lists by hand, which does not scale.

## Smart Groups

A **Smart Group** is a dynamic set of devices defined by inventory criteria — "all Macs on macOS < 14.5," "all devices missing the security agent," "all devices in the Finance department." Its defining property is that **membership is automatic and live**: a device that starts matching the criteria joins the group; one that stops matching leaves. You never maintain the list.

This is the [rule-based-tagging lesson](../../volume-140-dynatrace-certifications/chapters/04-entities-topology-and-management-zones.md) from Dynatrace, [label-based policy](../../volume-143-akamai-certifications/chapters/07-guardicore-segmentation-certifications.md) from Guardicore, in Apple-management clothing: **define membership by criteria, not by hand.** A Smart Group of "macOS < 14.5" automatically includes the Mac someone unboxes next week on an old OS, and automatically excludes it the moment it updates — no admin action. Static groups (hand-picked device lists) exist but rot exactly as manual tags do; Smart Groups are the discipline.

## Scope

**Scope** is how a policy or configuration profile targets devices: you scope it to Smart Groups (usually), and it applies to their members. The power and the danger are the same as everywhere:

- **Scoping to a Smart Group means the target is live.** Scope a "install security agent" policy to the "missing security agent" Smart Group, and it applies to exactly the devices that need it, automatically, forever — including ones that appear tomorrow.
- **Scoping mistakes deploy the right change to the wrong devices.** Scope a "wipe and re-enroll" policy to the wrong group, or forget an exclusion, and the blast radius is measured in bricked devices. The lab models the pre-flight discipline: **know a scope's current membership before you deploy to it.**

Scope also supports **exclusions** and **limitations** — narrow a broad scope by excluding a group, or limit by network/building. The commonest scope error is a broad inclusion with a forgotten exclusion, the same shape as [Cloudflare's WAF allow-before-block](../../volume-142-cloudflare-certifications/chapters/03-waf-rules-and-rate-limiting.md).

## Hands-On Lab

Python models Jamf Pro targeting. **Cost:** none.

### Lab 3.1 — Smart Groups are live, static groups rot

**Objective:** Watch dynamic membership track reality as the fleet changes.

```bash
python3 - <<'EOF'
import random
random.seed(24)
def gen_fleet(n, start=0):
    out = []
    for i in range(start, start+n):
        out.append({"id": f"mac-{i:03d}", "os": random.choice(["14.6","14.5","14.4","13.6"]),
                    "dept": random.choice(["eng","sales","finance"])})
    return out

fleet = gen_fleet(60)
# Smart Group: os < 14.5 (needs update). Static group: hand-picked once.
def needs_update(m): return m["os"] < "14.5"
smart = [m["id"] for m in fleet if needs_update(m)]
static = list(smart)   # snapshot taken today, never updated

print(f"day 1: {len(fleet)} Macs")
print(f"   Smart Group 'os < 14.5': {len(smart)} members")
print(f"   Static group (snapshot): {len(static)} members  (identical today)\n")

# day 30: 20 new Macs arrive (mixed OS), and 8 existing ones get updated
for m in fleet:
    if m["id"] in smart and random.random() < 0.5:
        m["os"] = "14.6"   # updated -> should LEAVE the group
fleet += gen_fleet(20, start=60)
smart_now = [m["id"] for m in fleet if needs_update(m)]

print(f"day 30: {len(fleet)} Macs (20 arrived, some updated)")
print(f"   Smart Group 'os < 14.5': {len(smart_now)} members -> AUTOMATICALLY correct")
print(f"      (updated Macs LEFT, new out-of-date Macs JOINED — zero admin action)")
still_updated = [m['id'] for m in fleet if m['id'] in static and not needs_update(m)]
missing_new = [m['id'] for m in fleet if needs_update(m) and m['id'] not in static]
print(f"   Static group: still {len(static)} members -> WRONG")
print(f"      {len(still_updated)} already-updated Macs still listed (would be re-patched)")
print(f"      {len(missing_new)} new out-of-date Macs MISSING (would never get patched)")
print("\nThe Smart Group is CORRECT on day 30 with no maintenance; the static group")
print("is wrong in BOTH directions — it re-targets fixed devices AND misses new ones.")
print("\nThis is why Jamf certifications drill Smart Groups: membership-by-criteria is")
print("the ONLY thing that scales. Same lesson as Dynatrace rule-tags and Guardicore")
print("labels — define the WHAT, let membership follow the facts. Static groups are")
print("for genuinely fixed sets (a specific pilot cohort), never for 'devices matching X'.")
EOF
```

**Expected result:** The Smart Group staying correct as devices update and arrive, while the static snapshot drifts wrong in both directions. The membership-by-criteria lesson is the same one this shelf teaches repeatedly — Smart Groups scale because membership follows the facts, and static groups rot exactly like manual tags.

**Negative test:** Building a static group for "devices needing the update." It is correct the day you make it and wrong the day anything changes — re-patching fixed devices and missing new ones.

**Cleanup:** None.

### Lab 3.2 — Know the scope before you deploy

**Objective:** Run the pre-flight check that prevents blast-radius disasters.

```bash
python3 - <<'EOF'
FLEET = {
  "mac-eng":     {"dept": "eng", "os": "14.6", "role": "workstation"},
  "mac-finance": {"dept": "finance", "os": "14.5", "role": "workstation"},
  "mac-kiosk":   {"dept": "lobby", "os": "14.4", "role": "kiosk"},
  "mac-server":  {"dept": "it", "os": "14.6", "role": "server"},
  "mac-exec":    {"dept": "exec", "os": "14.4", "role": "workstation"},
}
# Policy: "erase and reinstall macOS" — scoped to a Smart Group 'os < 14.5'
def in_scope(m): return m["os"] < "14.5"
scoped = {k: v for k, v in FLEET.items() if in_scope(v)}
print("DESTRUCTIVE policy: 'erase and reinstall macOS'")
print("scoped to Smart Group: os < 14.5\n")
print("PRE-FLIGHT — current members of that scope RIGHT NOW:")
for k, v in scoped.items():
    danger = "  <-- WOULD BE WIPED" if v["role"] in ("kiosk","server") else ""
    print(f"   {k:12} dept={v['dept']:8} role={v['role']}{danger}")
print(f"\n{len(scoped)} devices in scope. Review BEFORE deploying:")
print("   mac-kiosk (lobby kiosk) and mac-server (a SERVER) are in scope by OS —")
print("   and a destructive policy would erase them. Neither should be.")
print("\nThe fix is EXCLUSIONS: exclude role=kiosk and role=server from the scope,")
print("or limit the scope to role=workstation. The Smart Group caught them by OS")
print("alone; the destructive action needs a NARROWER scope than the informational one.")
print("\nThe discipline the 300 exam tests: before deploying ANY policy — especially")
print("a destructive one — LIST the current scope members and read them. A scope is")
print("a live query; 'os < 14.5' silently includes whatever matches, and for an erase")
print("policy, 'whatever matches' must be verified, not assumed. Same as reviewing a")
print("shared scheme's blast radius (Atlassian, Vol CXLV) or a WAF scope (Cloudflare).")
EOF
```

**Expected result:** A destructive policy scoped by OS alone catching a kiosk and a server that should never be wiped, resolved by role-based exclusions. The pre-flight discipline is the Admin-level lesson — a scope is a live query, and destructive actions require listing and verifying current members plus narrowing exclusions, not trusting the broad criterion.

**Negative test:** Deploying a destructive policy to a Smart Group without reviewing current membership. The group's OS criterion silently includes the kiosk and the server, and the erase reaches them.

**Cleanup:** None.

### Lab 3.3 — Extension attributes: collect what you need to target

**Objective:** Show how custom inventory enables precise scoping.

```bash
python3 - <<'EOF'
# Built-in inventory can't answer everything; extension attributes fill the gap
DEVICES = [
  # id,        os,      built_in_only,                  ext_attr: has_security_agent, ext_attr: filevault
  ("mac-01",  "14.6",  "eng workstation",              True,  True),
  ("mac-02",  "14.6",  "eng workstation",              False, True),   # missing agent!
  ("mac-03",  "14.5",  "finance workstation",          True,  False),  # FileVault off!
  ("mac-04",  "14.6",  "sales workstation",            False, False),  # both problems
]
print("Question: 'which Macs are non-compliant (missing agent OR FileVault off)?'\n")
print("With BUILT-IN inventory only (OS, dept, apps):")
print("   you can see OS and department, but NOT whether the security agent is")
print("   installed or whether FileVault is on — those aren't standard inventory.")
print("   You cannot build a Smart Group for 'non-compliant' at all.\n")
print("With EXTENSION ATTRIBUTES (scripts that report agent status + FileVault):")
print(f"   {'device':10}{'agent':>8}{'filevault':>11}   compliant?")
noncompliant = []
for d, os, desc, agent, fv in DEVICES:
    ok = agent and fv
    if not ok: noncompliant.append(d)
    print(f"   {d:10}{'yes' if agent else 'NO':>8}{'yes' if fv else 'NO':>11}   {'compliant' if ok else 'NON-COMPLIANT'}")
print(f"\n   -> Smart Group 'non-compliant' = {noncompliant}")
print("      NOW you can scope a remediation policy to exactly these, automatically.")
print("\nExtension attributes are the KEY to precise management: a script collects the")
print("fact (is the agent running? is FileVault on? does this file exist?), Jamf")
print("stores it as inventory, and you build Smart Groups and scope on it like any")
print("built-in field. Without them you can only target on what Apple/Jamf collect")
print("by default; WITH them you can target on anything a script can determine.")
print("\nThis is the 200->300 progression: Tech uses built-in inventory + Smart Groups;")
print("Admin writes extension attributes to collect the facts the org actually needs")
print("to target on, turning 'compliance' from a spreadsheet into a live Smart Group.")
EOF
```

**Expected result:** Built-in inventory unable to answer a compliance question that extension attributes resolve into a precise, auto-scoped Smart Group. The extension-attribute lesson is the Admin-level skill — a script collects any fact, Jamf stores it as inventory, and you target on it like any field, turning compliance from a manual spreadsheet into a live group.

**Negative test:** Trying to target non-compliant devices with built-in inventory alone. The facts that define compliance (agent status, FileVault) are not standard fields; without extension attributes there is no Smart Group to build.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Inventory understood as the foundation everything targets through, extended by extension attributes.
- [ ] Smart Groups designed as live, criteria-based membership — the scaling discipline over static groups.
- [ ] Scope treated as a live query, with destructive policies pre-flighted and narrowed by exclusions.
- [ ] Extension attributes used to collect the facts precise targeting requires.
