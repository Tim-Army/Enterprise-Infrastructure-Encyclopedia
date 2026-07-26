# Chapter 06: ZPA Advanced — Posture, Browser Access, and App Protection

## Learning Objectives

- Build **device posture profiles** and use them as conditions in ZPA access
  policy so only compliant devices reach sensitive apps.
- Configure **Browser Access** for clientless (agentless) access to private web
  apps through a browser alone.
- Explain **AppProtection** (inline inspection of private-app traffic) and
  **Privileged Remote Access** for third parties and OT.
- Combine identity, posture, and app sensitivity into a layered access policy.
- Validate posture logic and browser-access reachability.

## Theory and Architecture

Chapter 05 connected an authorized user to an app. Real policy adds two more
questions: *is the device trustworthy?* and *how should this particular app be
reached?* ZPA answers the first with **posture** and the second with access
methods — the full Client Connector path, clientless **Browser Access**, or
tightly scoped **Privileged Remote Access** — plus inline **AppProtection** for
apps that need content inspection.

### Device posture

A **posture profile** is a set of device checks — disk encryption, OS version,
a running EDR/antivirus, domain membership, a certificate present, firewall on.
Posture profiles become **conditions** in access policy: "allow HR to the HR app
*only if* the device is encrypted and running EDR." A non-compliant device is
denied or steered to a limited set of apps, so access depends on device state,
not just identity.

### Browser Access (clientless)

**Browser Access** publishes a private web application so an authorized user
can reach it through a browser with **no Client Connector installed** — useful
for contractors, BYOD, and unmanaged devices. ZPA presents the app over TLS
using a certificate for the app's external hostname; the connection is still
brokered through the exchange to an outbound-only connector, so the app stays
dark. It trades the full agent's breadth for reach without deployment.

### AppProtection and Privileged Remote Access

- **AppProtection** applies inline inspection (an OWASP-style ruleset) to
  private-app traffic, catching web attacks against internal apps that a plain
  tunnel would pass.
- **Privileged Remote Access (PRA)** gives third parties and OT/ICS operators
  browser-based RDP/SSH/VNC to specific systems, with no agent and no network
  access — recording and credential injection keep vendor access controlled.

## Design Considerations

- **Posture is a spectrum, not a gate.** Use tiers: full access for compliant
  managed devices, Browser Access only for unmanaged, deny for failing critical
  checks — rather than one all-or-nothing rule.
- **Browser Access for reach, agent for depth.** Clientless suits web apps and
  unmanaged devices; the agent is needed for non-web protocols and richest
  posture.
- **PRA for third parties** so vendors never get a VPN or an agent — scoped,
  recorded, credential-injected access to named systems only.

## Implementation and Automation

### A posture-gated access policy (portal shape)

```text
# ZPA Portal > Posture Profiles: "Compliant" = disk-encrypted AND EDR running AND OS>=min
# Access Policy:
#   Allow  group "HR"  -> "HR-App"  IF posture "Compliant"
#   Allow  group "HR"  -> "HR-App (Browser Access)"  IF NOT "Compliant"   (clientless, limited)
```

### Posture evaluation logic (local model)

```bash
python3 - <<'EOF'
def compliant(dev):  # model of a posture profile's AND-ed checks
    return dev["encrypted"] and dev["edr"] and dev["os_build"] >= 2200
managed   = {"encrypted": True,  "edr": True,  "os_build": 2300}
byod      = {"encrypted": False, "edr": False, "os_build": 2300}
for name, d in [("managed", managed), ("byod", byod)]:
    print(name, "->", "full access" if compliant(d) else "browser-access only / deny")
EOF
```

### Browser Access (portal shape)

```text
# ZPA Portal > Browser Access: publish app "wiki.internal.example.com" as
#   ba-wiki.example.com with a TLS certificate; broker still uses outbound-only connector.
```

## Validation and Troubleshooting

- **Compliant device denied.** A posture check is failing (EDR not detected, OS
  below minimum) — read which check failed rather than loosening the whole
  profile.
- **Browser Access cert error.** The Browser Access certificate for the
  external hostname is missing or untrusted — it is a separate certificate from
  ZIA's inspection chain.
- **Third-party over-access.** A vendor placed in a normal access policy gets
  more than intended — move them to Privileged Remote Access with named systems.

## Security and Best Practices

- **Gate sensitive apps on posture**, not identity alone — a valid user on a
  compromised device is a threat.
- **Prefer Browser Access / PRA for unmanaged and third-party** access so no
  agent or network membership is granted.
- **Turn on AppProtection for internet-adjacent internal apps** so brokered
  access still inspects for web attacks.

## References and Knowledge Checks

### References

- Zscaler Help Portal — *ZPA: Posture Profiles, Browser Access, AppProtection,
  Privileged Remote Access* (`help.zscaler.com`).

### Knowledge Checks

- How does a posture profile become a condition in access policy?
- When is clientless Browser Access the right access method over the agent?
- What does AppProtection add that a plain ZPA tunnel does not?
- Why is Privileged Remote Access preferable to a VPN for third-party vendors?

## Hands-On Lab

This chapter's labs cover posture-gated access, the clientless Browser Access
method, and privileged/third-party access. Posture logic runs locally; portal
steps reference a ZPA tenant. Each ends **`**Lab verified by:** *pending*`**
until a human runs it.

**Shared prerequisites for Labs 6.1–6.3** — `python3`; a ZPA tenant for portal
steps. **Cost:** none.

### Lab 6.1 — Posture-gated access (Topic: Device posture)

**Objective:** Allow an app only from compliant devices.

```bash
python3 - <<'EOF'
def compliant(dev):
    return dev["encrypted"] and dev["edr"] and dev["os_build"] >= 2200
cases = {"managed":{"encrypted":True,"edr":True,"os_build":2300},
         "byod":{"encrypted":False,"edr":True,"os_build":2300}}
for name, d in cases.items():
    print(name, "->", "FULL access" if compliant(d) else "denied / browser-access only")
assert compliant(cases["managed"]) and not compliant(cases["byod"])
print("posture gate verified")
EOF
```

**Expected result:** the managed device gets full access and the BYOD device is
denied/steered to limited access — a posture profile is a set of AND-ed device
checks used as a policy condition, so access depends on device trustworthiness,
not identity alone.

**Negative test:** grant access on identity only (no posture condition); a valid
user on a non-compliant or compromised device reaches the sensitive app —
posture is what closes that gap.

**Cleanup:** none.

### Lab 6.2 — Browser Access for unmanaged devices (Topic: Clientless access)

**Objective:** Reach a private web app with no agent.

```text
# ZPA Portal > Browser Access: publish wiki.internal.example.com as ba-wiki.example.com (TLS cert);
# authorized user opens https://ba-wiki.example.com in a plain browser.
```

**Expected result:** an authorized user reaches the internal web app through a
browser alone, brokered to an outbound-only connector — Browser Access trades
the full agent for reach on unmanaged/BYOD devices while keeping the app dark;
it needs its own TLS certificate for the external hostname.

**Negative test:** expect non-web protocols (RDP/SSH) to work through Browser
Access as-published; they need the agent or Privileged Remote Access — clientless
Browser Access is for web apps.

**Cleanup:** unpublish the lab Browser Access app.

### Lab 6.3 — Privileged Remote Access for a vendor (Topic: Third-party access)

**Objective:** Scope, record, and control third-party access.

```text
# ZPA Portal > Privileged Remote Access: give vendor browser-based RDP/SSH to named hosts only,
#   with session recording and credential injection; no agent, no network access.
```

**Expected result:** the vendor gets browser-based RDP/SSH to specific systems
with recording and injected credentials, and no network access — PRA controls
third-party/OT access to named systems only, so a vendor never receives a VPN,
an agent, or reachability beyond the listed hosts.

**Negative test:** put the vendor in a normal access policy with a broad
segment; they gain far more reach than intended — PRA's named-system scoping is
the control.

**Cleanup:** revoke the lab PRA console/policy.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Advanced ZPA layers device posture and access method onto identity: posture
profiles gate sensitive apps on device trust, Browser Access reaches web apps
from unmanaged devices with no agent, AppProtection inspects private-app traffic
inline, and Privileged Remote Access scopes and records third-party/OT access to
named systems. Access becomes a function of who, what device, and which app.

- [ ] Can gate an app on a posture profile and predict the outcome per device.
- [ ] Knows when Browser Access is the right clientless method.
- [ ] Can explain AppProtection and Privileged Remote Access.
- [ ] Understands posture as tiers rather than an all-or-nothing gate.
