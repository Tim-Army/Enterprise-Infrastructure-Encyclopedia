# Chapter 05: Endpoint Compliance (OECA)

## Learning Objectives

- Cover OECA: endpoint posture, network access control, and BYOD risk.
- Understand enforcement that maximizes security without killing productivity.
- Model an endpoint-posture decision.

## The certificate in brief

**OECA** (Endpoint Compliance Associate) covers securing endpoints: enforcement methodologies that maximize security without decreasing productivity, local device security policies, BYOD risks, and attacker targets/exploitation. OPSWAT's product here is **MetaAccess** — device posture and network access control that admits only compliant endpoints.

## Posture: prove the device is safe before it connects

The premise from [Chapter 02](02-cip-fundamentals.md) — trust no device — becomes concrete: before an endpoint reaches critical resources, verify its **posture** (patch level, antivirus running and current, disk encryption, no risky apps, compliant configuration). Non-compliant devices are denied, quarantined, or remediated.

## Hands-On Lab

Python models posture and enforcement. **Cost:** none.

### Lab 5.1 — An endpoint-posture check

**Objective:** Decide admission from device posture — the OECA core.

```bash
python3 - <<'EOF'
# Posture assessment: a device is admitted only if it meets policy
policy = {"av_running": True, "av_current": True, "disk_encrypted": True,
          "os_patched": True, "firewall_on": True, "no_risky_apps": True}
def assess(device):
    failures = [k for k, required in policy.items() if required and not device.get(k, False)]
    if not failures: return "ADMIT (compliant)"
    return f"DENY/REMEDIATE — non-compliant: {', '.join(failures)}"
managed  = {"av_running":True,"av_current":True,"disk_encrypted":True,"os_patched":True,"firewall_on":True,"no_risky_apps":True}
byod     = {"av_running":True,"av_current":False,"disk_encrypted":False,"os_patched":True,"firewall_on":True,"no_risky_apps":False}
print("managed laptop:", assess(managed))
print("personal BYOD: ", assess(byod))
EOF
```

**Expected result:**

```text
managed laptop: ADMIT (compliant)
personal BYOD:  DENY/REMEDIATE — non-compliant: av_current, disk_encrypted, no_risky_apps
```

The compliant managed device is admitted; the BYOD laptop (stale AV, no encryption, risky apps) is denied or sent to remediation. OECA's model is **verify posture, then admit** — the endpoint half of "trust no device."

**Negative test:** Admitting by identity alone (the user authenticated) without checking the device — a valid user on a compromised, unpatched laptop carries the threat inside; posture is a separate, necessary gate.

**Cleanup:** None.

### Lab 5.2 — Enforcement without killing productivity

**Objective:** Model graduated enforcement — the OECA balance.

```bash
python3 - <<'EOF'
# Enforcement should maximize security without needless disruption: graduated responses.
def enforce(severity, remediable_automatically):
    if severity == "critical": return "BLOCK access now"
    if remediable_automatically: return "AUTO-REMEDIATE (update AV / enable firewall) then admit"
    if severity == "medium": return "LIMITED access (quarantine VLAN) + user notified to fix"
    return "ADMIT with monitoring + coaching"
print("critical (malware active):     ", enforce("critical", False))
print("medium (AV out of date, auto): ", enforce("medium", True))
print("medium (config drift, manual): ", enforce("medium", False))
print("low (minor policy):            ", enforce("low", False))
EOF
```

**Expected result:** Graduated enforcement — block critical, auto-remediate what can be fixed silently, quarantine-and-notify for manual fixes, coach for minor issues. OECA stresses that **enforcement must not needlessly halt work**: auto-remediation and limited (quarantine-VLAN) access keep users productive while closing risk, which is what makes the control sustainable.

**Negative test:** Blocking every non-compliant device outright — the help desk drowns and users route around the control (personal hotspots, shadow IT); graduated enforcement with auto-remediation is why posture control survives contact with real users.

**Cleanup:** None.

### Lab 5.3 — BYOD and the risk it adds

**Objective:** Enumerate the BYOD risks OECA tests.

```bash
python3 - <<'EOF'
byod_risks = [
  "unmanaged patch state (no enterprise patching)",
  "personal apps / unknown software (larger attack surface)",
  "no enterprise EDR/AV guarantee",
  "shared/family use (other users, malware exposure)",
  "data exfiltration to personal cloud from the same device",
]
print("BYOD risk factors OECA expects you to control:")
for r in byod_risks: print(f"  - {r}")
print("\nControl: posture-gate BYOD harder than managed; consider clientless/limited access or a managed container.")
EOF
```

**Expected result:** The BYOD risk list — unmanaged patching, personal apps, no guaranteed EDR, shared use, personal-cloud exfiltration — and the control response (stricter posture gating, limited/clientless access, managed containers). BYOD widens the attack surface, so OECA treats personal devices as higher-risk and gates them accordingly.

**Negative test:** Treating a BYOD device like a managed one — it lacks the enterprise controls a managed device has; equal treatment under-protects the critical environment.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Endpoint posture assessment (verify then admit) modeled.
- [ ] Graduated enforcement (block/auto-remediate/quarantine/coach) drilled.
- [ ] BYOD risks and stricter gating understood.
