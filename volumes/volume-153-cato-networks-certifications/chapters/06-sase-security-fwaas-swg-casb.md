# Chapter 06: SASE Security — FWaaS, SWG, and CASB

## Learning Objectives

- Explain the core cloud-delivered security functions of SASE.
- Understand FWaaS, SWG, and CASB and what each protects.
- Place these functions as the security half of SASE (and the core of SSE).
- Recognize how convergence unifies them under one policy.

*Cert relevance: the security functions are core **SASE Expert**, **SSE Fundamentals**, and **Advanced Security** material.*

## The security half of SASE

[Chapter 5](05-sase-networking-sd-wan-and-the-edge.md) covered SASE's networking; this chapter covers its **security functions** — delivered as a service from the cloud PoPs, in the [single pass (Chapter 4)](04-single-pass-architecture-and-the-global-backbone.md), under one policy. Three functions form the core (together with [ZTNA, Chapter 7](07-ztna-zero-trust-network-access.md), they make up **SSE**, the security subset of SASE, [Chapter 8](08-sse-and-advanced-security.md)):

| Function | Protects | Answers |
|:---|:---|:---|
| **FWaaS** (Firewall-as-a-Service) | The network perimeter | What traffic is allowed between zones/sites/internet? |
| **SWG** (Secure Web Gateway) | Users' web/internet access | Is this website/download safe and allowed? |
| **CASB** (Cloud Access Security Broker) | Cloud/SaaS app usage | Which cloud apps are used, and is that safe and sanctioned? |

## FWaaS and SWG

**FWaaS** is the firewall delivered as a **cloud service** rather than an appliance — enforcing network security policy (which sources may reach which destinations on which ports/apps) for all traffic through the PoPs, everywhere, without a box at each site. It brings next-gen firewall capabilities (application awareness, IPS) to every site and user uniformly.

**SWG** secures **web access** — when a user browses or downloads, the SWG inspects the traffic, blocks malicious or policy-violating sites (malware, phishing, forbidden categories), and enforces acceptable-use policy. Because it runs at the PoP near the user, it protects users *wherever they are* (office, home, traveling), not just when they are behind the office firewall — the [perimeter-follows-the-user (Chapter 2)](02-what-is-sase.md) principle applied to web security. The lab is covered within the CASB exercise.

## CASB and shadow IT

**CASB** governs **cloud application usage** — and its signature value is solving **shadow IT.** Employees adopt cloud/SaaS apps freely (a file-sharing tool, an AI service, a note app), often without IT's knowledge or approval — "shadow IT" — and each unsanctioned app is a potential data-leak and compliance risk (corporate data flowing into an unvetted service). CASB **discovers** which cloud apps are actually being used (from the traffic), **assesses** their risk, and **enforces** policy — block the risky ones, allow the sanctioned ones, and control *what* can be done in them (e.g. allow the corporate Google Workspace but block uploads to personal Google Drive).

Because [all traffic flows through the converged cloud (Chapter 5)](05-sase-networking-sd-wan-and-the-edge.md), CASB sees *every* cloud app every user touches — complete shadow-IT visibility, which a point CASB bolted onto only some traffic cannot match. The lab models shadow-IT discovery.

## One policy

The convergence payoff ([Chapter 3](03-traditional-stack-vs-converged-sase.md)) is that FWaaS, SWG, and CASB are **one policy on one platform**, not three products. A rule about a user or group applies across network, web, and cloud-app access consistently, and the functions share context in the single pass. The lab shows the unified coverage.

## Hands-On Lab

Python models the security functions. **Cost:** none.

### Lab 6.1 — CASB discovers and governs shadow IT

**Objective:** See how CASB surfaces unsanctioned cloud apps from the traffic.

```bash
python3 - <<'EOF'
# cloud apps seen in the traffic (CASB discovers these); IT only "knew about" some
SANCTIONED = {"Microsoft 365", "Salesforce", "Corporate Google Workspace", "Slack"}
DISCOVERED_TRAFFIC = [
  # app,                    users, risk,     data_uploaded
  ("Microsoft 365",         800,  "low",    "sanctioned"),
  ("Salesforce",            300,  "low",    "sanctioned"),
  ("random-fileshare.io",   45,   "HIGH",   "customer data (!)"),   # shadow IT + data leak
  ("free-ai-tool.ai",       120,  "HIGH",   "source code pasted (!)"),  # shadow AI
  ("personal Dropbox",      60,   "medium", "files uploaded"),
  ("Slack",                 500,  "low",    "sanctioned"),
]
print("CASB discovers ALL cloud apps in use (not just the ones IT knew about):\n")
print(f"   {'app':24}{'users':>7}{'risk':>8}   status")
shadow = []
for app, users, risk, data in DISCOVERED_TRAFFIC:
    is_shadow = app not in SANCTIONED
    if is_shadow: shadow.append((app, users, risk, data))
    tag = "SHADOW IT" if is_shadow else "sanctioned"
    print(f"   {app:24}{users:>7}{risk:>8}   {tag} ({data})")
print(f"\n   SHADOW IT discovered: {len(shadow)} unsanctioned apps IT didn't know about")
for app, users, risk, data in shadow:
    if risk == "HIGH":
        print(f"   !! {app}: {users} users, {data} — HIGH risk, BLOCK / restrict")
print("\nThe shadow-IT problem: employees adopt cloud apps freely, and each unsanctioned")
print("one is a data-leak + compliance risk. Here CASB found 'random-fileshare.io' with")
print("CUSTOMER DATA and 'free-ai-tool.ai' with SOURCE CODE pasted into it — exactly the")
print("kind of leak nobody approved and nobody could see.")
print("\nCASB DISCOVERS every cloud app from the traffic, ASSESSES risk, and ENFORCES")
print("policy (block the risky, allow the sanctioned, control what's done in each).")
print("Because ALL traffic flows through the converged SASE cloud, CASB sees EVERYTHING")
print("— complete shadow-IT visibility a bolted-on point CASB can't match. You can't")
print("govern what you can't see; convergence is what lets you see it all.")
EOF
```

**Expected result:** CASB discovering unsanctioned shadow-IT cloud apps from the traffic — including a file-share with customer data and an AI tool with pasted source code — that IT did not know about, and flagging the high-risk ones to block. The CASB lesson is that shadow IT is invisible and risky, and because all traffic flows through the converged SASE cloud, CASB has complete visibility to discover, assess, and govern every cloud app.

**Negative test:** Governing only the cloud apps IT already knows about. Employees adopt unsanctioned apps freely, leaking data into unvetted services; CASB's discovery from the full traffic surfaces the shadow IT that a known-apps-only view misses entirely.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] The core SASE security functions (FWaaS, SWG, CASB) understood as cloud-delivered from the PoPs.
- [ ] FWaaS and SWG understood as firewall and web security protecting users wherever they are.
- [ ] CASB understood as discovering and governing cloud-app usage — solving shadow IT with complete visibility.
- [ ] The functions recognized as one policy on one converged platform, the security half of SASE and core of SSE.
