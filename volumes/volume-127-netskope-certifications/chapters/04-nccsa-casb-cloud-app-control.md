# Chapter 04: NCCSA — CASB and Cloud App Control

## Learning Objectives

- Cover the NCCSA's CASB pillar: cloud app visibility and control.
- Understand sanctioned vs unsanctioned apps, app instances, and activity-level control.
- Model app-instance awareness and granular activity policy.

## What CASB does

A **Cloud Access Security Broker** gives visibility and control over SaaS usage. Netskope's differentiator is **granularity**: it understands not just "which app" but **which instance** (corporate vs personal), **which activity** (upload/download/share/post), and **what data**. That lets policy say "block *uploads* to *personal* OneDrive" while allowing the corporate instance — impossible with a coarse allow/block-by-domain firewall.

| Concept | Meaning |
|:---|:---|
| **Sanctioned app** | An app IT manages (corporate Microsoft 365, corporate Box) |
| **Unsanctioned / Shadow IT** | Apps users adopt without IT (a personal Dropbox) |
| **App instance** | A specific tenant/account of an app — corporate vs personal instance of the same SaaS |
| **Activity** | The action within the app: upload, download, share, post, edit |
| **Cloud Confidence Index (CCI)** | Netskope's risk rating of an app |

## Hands-On Lab

Python models instance and activity awareness. **Cost:** none.

### Lab 4.1 — App-instance awareness

**Objective:** Show why "which instance" matters — the CASB superpower.

```bash
python3 - <<'EOF'
# The same app (OneDrive), two instances; policy differs by instance
def decide(app, instance, activity):
    if app == "onedrive" and instance == "personal" and activity == "upload":
        return "BLOCK (upload to personal instance — exfiltration risk)"
    if app == "onedrive" and instance == "corporate":
        return "ALLOW (managed corporate instance)"
    return "ALLOW"
print("onedrive/corporate/upload:", decide("onedrive","corporate","upload"))
print("onedrive/personal/upload: ", decide("onedrive","personal","upload"))
EOF
```

**Expected result:**

```text
onedrive/corporate/upload: ALLOW (managed corporate instance)
onedrive/personal/upload:  BLOCK (upload to personal instance — exfiltration risk)
```

Same app, same activity, **different instance → different policy**. A domain-based firewall sees only `onedrive.com` and can't tell corporate from personal; CASB instance awareness is what stops data leaking to personal accounts, a headline NCCSA concept.

**Negative test:** Blocking `onedrive.com` wholesale to stop personal use — you break the sanctioned corporate instance too; instance awareness is precisely what avoids that blunt outcome.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.2 — Activity-level control

**Objective:** Model policy on the action, not just the app.

```bash
python3 - <<'EOF'
# Granular activity policy within a sanctioned app
policy = {
  ("box","corporate","view"): "ALLOW",
  ("box","corporate","download"): "ALLOW",
  ("box","corporate","share_external"): "BLOCK",   # allow use, block external sharing
  ("box","corporate","upload"): "ALLOW-WITH-DLP",   # allow but scan for sensitive data
}
for (app,inst,act), verdict in policy.items():
    print(f"{app}/{inst}/{act:15} -> {verdict}")
EOF
```

**Expected result:** Fine-grained verdicts per activity — allow viewing/downloading, block external sharing, scan uploads with DLP — within one sanctioned app. Activity-level control lets you keep an app usable while closing its risky actions, the NCCSA's CASB policy model.

**Negative test:** All-or-nothing app control (allow or block the whole app) — you either accept the risky activities or lose the app; granular activity policy is the middle path CASB provides.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.3 — Shadow IT discovery and CCI

**Objective:** Model discovering unsanctioned apps and rating their risk.

```bash
python3 - <<'EOF'
# Discovery: from steered traffic/logs, enumerate apps and rate them (Cloud Confidence Index)
discovered = [
  ("corp-box.com", "sanctioned", 95),
  ("random-filedrop.io", "shadow", 22),    # low CCI -> risky
  ("aichat-unknown.ai", "shadow", 35),
]
print(f"{'app':<22}{'status':<12}CCI")
for app, status, cci in discovered:
    flag = "  <-- review/block (low CCI)" if cci < 50 else ""
    print(f"{app:<22}{status:<12}{cci}{flag}")
EOF
```

**Expected result:** Discovered apps rated by Cloud Confidence Index, with low-CCI shadow apps flagged for review — CASB discovery turns steered-traffic visibility into a risk-ranked inventory of Shadow IT. NCCSA expects you to find unsanctioned apps and act on their risk score.

**Negative test:** Blocking every unsanctioned app reflexively — you drive users to workarounds and miss that some "shadow" apps are legitimately useful (coach/sanction them instead); CCI informs a nuanced response.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.4 — Inline CASB enforcement

**Objective:** Tie CASB back to steering — enforcement needs inline coverage.

```bash
cat <<'EOF'
CASB enforcement modes:
  Inline (real-time):  block/coach the upload/share/post as it happens (needs steering, Ch03)
  API (out-of-band):   find risky shares/exposed data already in sanctioned SaaS, remediate
Combine: inline stops new leaks; API cleans existing exposure and covers un-steered access paths.
EOF
```

**Expected result:** CASB works **inline** (real-time activity control) and via **API** (retroactive SaaS scanning) — the two modes from [Chapter 03](03-nccsa-platform-and-steering.md) applied to cloud apps. Full CASB coverage uses both.

**Negative test:** Inline-only CASB misses data users shared before onboarding Netskope, or via unmanaged devices hitting the SaaS directly; API-enabled protection closes that gap.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Sanctioned/unsanctioned, app-instance, and activity concepts internalized.
- [ ] Instance-aware and activity-level policy modeled (corporate vs personal).
- [ ] Shadow-IT discovery + Cloud Confidence Index and inline-vs-API CASB understood.
