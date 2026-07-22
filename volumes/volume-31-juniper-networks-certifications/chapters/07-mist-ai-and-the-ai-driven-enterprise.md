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

Cloud-dependent lab: with a Mist trial org (or emulated API responses
where no org is available), build the API inventory of one site, pull
wireless SLE summaries, and register a webhook to a local receiver;
onboard a vJunos-switch as a wired-assurance device where entitlement
permits, render a template VLAN change, and read the resulting Junos
diff. Document every artifact API-first — the exam's mental model.

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
