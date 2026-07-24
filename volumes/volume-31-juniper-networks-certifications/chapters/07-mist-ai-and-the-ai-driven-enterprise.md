# Chapter 07: Mist AI and the AI-Driven Enterprise

## Learning Objectives

- Explain the Mist cloud architecture: cloud microservices, AP and
  switch telemetry, and Marvis as the conversational/AI layer
- Operate wireless the Mist way: templates, WLANs, RF with AI-driven
  RRM, and service levels (SLEs) as the measurement contract
- Extend Mist management to EX switching (wired assurance) and the WAN
  edge
- Map the Mist AI track — JNCIA-MistAI (JN0-253), JNCIS-MistAI-Wireless
  (JN0-452), JNCIS-MistAI-Wired (JN0-460), JNCIP-MistAI (JN0-750) — to
  these operations

## Theory and Architecture

### The track in one sentence

The Mist AI track certifies Juniper's cloud-native operations model:
access points, EX switches, and WAN edges stream rich telemetry to the
Mist cloud, **SLEs (service level expectations)** turn that telemetry
into user-experience metrics, and **Marvis** — the AI engine — answers
questions, identifies root cause, and drives actions. The ladder runs
JNCIA-MistAI (JN0-253) for platform concepts, the two specialist exams
split by domain — Wireless (JN0-452) and **Wired (JN0-460)** — and
JNCIP-MistAI (JN0-750) for full-stack AI-driven operations. All are
90-minute, 65-question exams (codes verified against Juniper's track
pages, 22 July 2026; this is the program's fastest-moving track —
re-verify at registration).

### SLEs change what "working" means

Traditional monitoring says the AP is up; SLEs say **users are
succeeding**: time-to-connect, throughput, coverage, roaming, each
decomposed into classifiers that assign every failed user-minute a
cause (DHCP, authentication, RF, capacity). Operations invert — you
work the SLE that is bleeding, not the device list. Marvis rides the
same data: natural-language queries ("why is VLAN 30 failing on
switch lab-ex1?"), anomaly detection, and Marvis Actions that name the
fix — with the wired side using the same model for port, VLAN, and
authentication failures on EX.

### Cloud-managed is still Junos underneath

Mist-managed EX switches remain Junos devices — templates render to
configuration you can read, and the escape hatch to the CLI exists —
but the operational contract moves to the cloud: zero-touch onboarding
by claim code, templates by site/group hierarchy, firmware orchestrated
centrally. The JNCIS-MistAI-Wired exam lives exactly on this seam.

## Design Considerations

- **Template hierarchy before the first site:** org-level templates
  with site overrides; resist per-device exceptions — they are drift
  with a UI
- **RF by intent:** coverage/capacity targets per site type and let
  AI-RRM steer channels and power; manual channel plans persist only
  for regulated venues
- **Identity:** 802.1X via Mist Access Assurance or an external NAC
  (the Volume XV Forescout patterns apply); PSK life-cycle via Mist
  PPSK where certificates cannot reach
- The AI is advisory until trusted: run Marvis Actions in
  recommend-mode first, action-mode after it earns it — the same
  automation-trust ladder as Volume IX

## Implementation and Automation

```text
# Mist is API-first; the UI is a client of the same REST API.
# List sites, then pull one site's wireless SLE summary:
curl -s -H "Authorization: Token $MIST_TOKEN" \
  https://api.mist.com/api/v1/orgs/$ORG/sites | jq '.[].name'

curl -s -H "Authorization: Token $MIST_TOKEN" \
  "https://api.mist.com/api/v1/sites/$SITE/sle/wifi/summary" | jq '.sle[] | {name, value}'

# Claim a switch to a site (zero-touch onboarding):
curl -s -X POST -H "Authorization: Token $MIST_TOKEN" \
  -d '{"code":"CLAIMCODE123"}' \
  https://api.mist.com/api/v1/orgs/$ORG/inventory
```

Webhooks push SLE degradations and Marvis events into the alerting
path (Volume XI); the same API drives configuration templates, making
Mist automatable with the Chapter 06 toolchain minus NETCONF.

## Validation and Troubleshooting

- SLE dashboard first: which experience metric degraded, which
  classifier, which scope (site/AP/WLAN/switch port)
- Marvis conversational query for the named user or client MAC — then
  verify its claimed root cause against the classifier data
- Client insights timeline: association → auth → DHCP → DNS — the
  wireless connect sequence with timestamps
- On wired assurance: port insights and the rendered Junos config diff
  when a template change misbehaves
- Packet captures triggered from the cloud (dynamic PCAP) when the AI
  narrative needs raw proof

## Security and Best Practices

- API tokens scoped and rotated like any credential; webhook secrets
  verified at the receiver
- WPA3-Enterprise/802.1X as the target state; PPSK as the managed
  exception with expiry
- Rogue/honeypot AP detection enabled and alarmed; wired 802.1X with
  Access Assurance where the port is reachable by the public
- Firmware auto-upgrade windows per site; the cloud orchestrates,
  change control still owns the calendar

## References and Knowledge Checks

- Mist AI track objectives: JN0-253, JN0-452, JN0-460, JN0-750 on
  Juniper's certification pages
- Mist documentation portal and API reference; Marvis Actions guide

Knowledge checks:

1. A site's time-to-connect SLE drops to 60% with the DHCP classifier
   dominant. What has Mist already told you, and what remains to
   verify outside it?
2. Contrast AI-RRM with scheduled manual channel planning: inputs,
   cadence, and failure modes.
3. Why does the Wired specialist exam exist separately from the
   DevOps track when both automate EX switches?

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **every exam objective of
the JNCIA-MistAI (JN0-253) exam** — the Mist AI associate — mapped in the volume
README's coverage tables. Labs use the Juniper Mist cloud dashboard and the Mist
REST API (`api.mist.com`). Each ends **`**Lab verified by:** *pending*`** until a
human runs it.

**Shared prerequisites for Labs 7.1–7.7** — a Juniper Mist organization with an
API token in `$MIST` (an `Authorization: Token` header), an org ID in `$ORG`, at
least one site, and claimed AP/switch devices. **Cost:** none beyond lab resources.

### Lab 7.1 — Juniper Mist Cloud Fundamentals (Objective: Juniper Mist Cloud Fundamentals)

**Objective:** Read the org and the AI-driven, cloud-native posture.

```bash
curl -s -H "Authorization: Token $MIST" "https://api.mist.com/api/v1/orgs/$ORG" | jq '{name, id}'
curl -s -H "Authorization: Token $MIST" "https://api.mist.com/api/v1/self" | jq '{email, privileges: (.privileges|length)}'
```

**Expected result:** the org and the authenticated admin's privileges — Juniper Mist
is a **cloud-native, microservices** platform that applies **AI/ML** to wired,
wireless, WAN, and access telemetry; management is cloud-based (no on-prem
controller), delivering assurance and automation via one dashboard/API.

**Negative test:** query with a token whose privileges exclude the org; the API
returns `403` — Mist RBAC scopes every call to the admin's role.

**Cleanup:** none (read-only).

### Lab 7.2 — Juniper Mist Configuration Basics (Objective: Juniper Mist Configuration Basics)

**Objective:** Read sites, device onboarding, and templates.

```bash
curl -s -H "Authorization: Token $MIST" "https://api.mist.com/api/v1/orgs/$ORG/sites" | jq -r '.[] | "\(.name) \(.id)"'
curl -s -H "Authorization: Token $MIST" "https://api.mist.com/api/v1/orgs/$ORG/inventory" | jq -r '.[] | "\(.type) \(.serial) \(.connected)"' | head
```

**Expected result:** the sites and claimed inventory with connection state — Mist
config basics: create **orgs/sites**, **claim/onboard** devices (activation code or
serial), apply **templates** (WLAN, switch, WAN) and **labels/policies**, plus
account roles and authentication (SSO), subscriptions, and certificates (RadSec).

**Negative test:** claim a device to the org but never assign it to a site; it stays
unconfigured — device onboarding requires site assignment for templates to apply.

**Cleanup:** none (read-only).

### Lab 7.3 — Juniper Mist Network Operations and Management (Objective: Juniper Mist Network Operations and Management)

**Objective:** Read the Assurance services across wired/wireless/WAN.

```bash
curl -s -H "Authorization: Token $MIST" "https://api.mist.com/api/v1/sites/$SITE/stats/devices?type=ap" | jq -r '.[] | "\(.name) \(.status)"' | head
curl -s -H "Authorization: Token $MIST" "https://api.mist.com/api/v1/sites/$SITE/stats/devices?type=switch" | jq -r '.[] | "\(.name) \(.status)"' | head
```

**Expected result:** AP and switch operational stats — Mist manages and assures
**Wi-Fi Assurance** (wireless), **Wired Assurance** (EX/switches), **WAN Assurance**
(SSR/SRX), **Routing Assurance**, and **Access Assurance** (NAC), each an AI-driven
service with SLE-based operations.

**Negative test:** an AP claimed but disconnected shows `status: disconnected`; its
assurance data is stale — the device must be cloud-connected for live assurance.

**Cleanup:** none (read-only).

### Lab 7.4 — Juniper Mist Monitoring and Analytics (Objective: Juniper Mist Monitoring and Analytics)

**Objective:** Read Service-Level Expectations (SLEs) and insights.

```bash
curl -s -H "Authorization: Token $MIST" "https://api.mist.com/api/v1/sites/$SITE/sle/metrics" 2>/dev/null | jq '.' | head
curl -s -H "Authorization: Token $MIST" "https://api.mist.com/api/v1/sites/$SITE/insights/stats" 2>/dev/null | jq '.' | head
```

**Expected result:** the SLE metrics (time-to-connect, throughput, coverage,
roaming) — Mist monitoring centers on **SLEs** (measurable user-experience goals
with a classifier tree of root causes), plus packet captures (dynamic), insights,
alerts, and audit logs, turning telemetry into experience metrics.

**Negative test:** an SLE below target with its classifier pointing at "association"
tells you *why* users struggle — reading the metric alone (without the classifier)
misses the root cause the SLE provides.

**Cleanup:** none (read-only).

### Lab 7.5 — Marvis Virtual Network Assistant (Objective: Marvis Virtual Network Assistant AI)

**Objective:** Query Marvis and read Marvis Actions.

```bash
curl -s -H "Authorization: Token $MIST" "https://api.mist.com/api/v1/orgs/$ORG/insights/marvis" 2>/dev/null | jq '.' | head
# Dashboard: Marvis conversational query, e.g. "troubleshoot client <MAC>"; Marvis Actions list org/site issues
```

**Expected result:** the Marvis Actions (proactive, prioritized issues) — **Marvis**
is the AI assistant: **Marvis Actions** surface the highest-impact problems (bad
cables, missing VLANs, AP coverage holes) org/site-wide, **Marvis queries** answer
natural-language troubleshooting, and **Marvis Minis** proactively probe the network.

**Negative test:** expect Marvis Actions on a brand-new org with no telemetry; it has
nothing to analyze yet — Marvis needs operational data to generate actions.

**Cleanup:** none (read-only).

### Lab 7.6 — Location-based Services (Objective: Location-based Services)

**Objective:** Read the vBLE location/asset data.

```bash
curl -s -H "Authorization: Token $MIST" "https://api.mist.com/api/v1/sites/$SITE/stats/assets" 2>/dev/null | jq '.' | head
curl -s -H "Authorization: Token $MIST" "https://api.mist.com/api/v1/sites/$SITE/maps" | jq -r '.[]?.name' | head
```

**Expected result:** the located assets and site maps — Mist **Location-Based
Services** use the APs' **virtual BLE (vBLE)** antenna arrays for high-accuracy
indoor location without external beacons: **asset visibility** (BLE tags) and
**vBLE engagement** (wayfinding, proximity notifications) on the site map.

**Negative test:** expect location on a site with APs lacking the vBLE array or no
map; location is unavailable — LBS depends on vBLE-capable APs and a calibrated map.

**Cleanup:** none (read-only).

### Lab 7.7 — Juniper Mist Cloud Operations and APIs (Objective: Juniper Mist Cloud Operations)

**Objective:** Use the Mist REST API and a WebSocket/webhook.

```bash
curl -s -H "Authorization: Token $MIST" "https://api.mist.com/api/v1/orgs/$ORG/webhooks" | jq -r '.[]? | "\(.type) \(.url)"'
# WebSocket: wss://api-ws.mist.com/api-ws/v1/stream for real-time; webhooks push events (audits, alarms, location)
```

**Expected result:** the org webhooks — Mist cloud operations are fully
**API-driven**: a **RESTful** API for config/stats, **WebSocket** for real-time
streams (client/location events), and **webhooks** to push events (alarms, audits,
occupancy) to external systems, so everything in the dashboard is automatable.

**Negative test:** a webhook whose target URL does not return `200` is retried then
disabled — the receiver must acknowledge deliveries.

**Cleanup:** none (read-only).

## Lab Verification

Verification means API calls returned live org data, one webhook
delivery was received and its payload archived, and (where entitled)
the template change rendered a readable Junos diff on the claimed
switch — or the emulated equivalents were captured for each.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

- [ ] Mist architecture and SLE/classifier model explained
- [ ] Marvis positioned: query, root cause, actions, trust ladder
- [ ] API-first operations demonstrated end to end
- [ ] All four Mist AI exam codes recorded from primary source
- [ ] Wired assurance seam (cloud contract over Junos) understood
