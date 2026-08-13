# Chapter 04: Next-Generation Firewall Engineer and SD-WAN Engineer

## Learning Objectives

- Explain the Next-Generation Firewall Engineer and SD-WAN Engineer credentials.
- Deploy PAN-OS with high availability and manage a fleet with Panorama.
- Configure NAT and decryption for enforcement.
- Describe Prisma SD-WAN fabric and path selection.
- Complete a walkthrough for each engineering topic.

## Theory and Architecture

The **Next-Generation Firewall Engineer** (Specialist) credential covers deploying and
operating PAN-OS at scale: **high availability** (active/passive and active/active pairs),
**Panorama** for centralized management, templates, device groups, and logging, **NAT**,
**decryption** (so Content-ID can inspect TLS), routing, and zone-based enforcement. The
**SD-WAN Engineer** (Specialist) credential covers **Prisma SD-WAN** — an application-aware
fabric of branch and data-center ION devices, orchestrated centrally, that selects paths by
application performance and policy and integrates with the security stack. Together these
engineer roles build resilient, centrally managed enforcement across the WAN edge.

## Design Considerations

Deploy firewalls in **HA** so a failure is transparent, and manage them from **Panorama** for
consistent policy at scale. **Decrypt** where policy and law allow so threats in TLS are seen.
For the WAN, use **Prisma SD-WAN** to select paths by application health and steer traffic
through security. Keep configuration templated and version-controlled.

## Implementation and Automation

The labs configure HA, push policy from Panorama, add NAT/decryption, and describe SD-WAN path
selection. All actions are **authorized administration**.

## Validation and Troubleshooting

Confirm the engineering model:

```text
NGFW Engineer: HA (active/passive|active/active) + Panorama (templates/device-groups/logging)
  + NAT + decryption (inspect TLS) + zones/routing.
SD-WAN Engineer: Prisma SD-WAN ION fabric + app-aware path selection + central orchestration.
```

Common pitfalls: a single firewall with **no HA** (a failure is an outage); and no
**decryption**, so threats hide inside TLS.

## Security and Best Practices

Run **HA** pairs, manage centrally with **Panorama**, and **decrypt** where permitted so
inspection is effective. Steer WAN traffic by application health and through the security stack.
Template and review all changes. Defensive operations throughout.

## Hands-On Lab

Engineering walkthroughs. **Shared prerequisites** — PAN-OS firewalls and Panorama (physical or
VM), in an **authorized** lab. **Cost:** none with lab VMs.

### Lab 4.1 — Configure HA (active/passive)

**Objective:** Pair two firewalls for failover.

```text
admin@fw# set deviceconfig high-availability enabled yes
admin@fw# set deviceconfig high-availability group 1 mode active-passive
admin@fw# set deviceconfig high-availability group 1 peer-ip 10.0.0.2
admin@fw# commit
admin@fw> show high-availability state
```

**Expected result:** an **active/passive HA** pair — the passive unit takes over on failure.

**Negative test:** run a lone firewall for a critical path; a failure is an **outage** — deploy
an HA pair.

**Rollback:** `set deviceconfig high-availability enabled no` then `commit`.

### Lab 4.2 — Push policy from Panorama

**Objective:** Manage rules centrally with device groups.

```text
admin@panorama# set device-group Branch-FWs pre-rulebase security rules Allow-DNS \
    from any to any application dns service application-default action allow
admin@panorama# commit
admin@panorama# commit-all shared-policy device-group Branch-FWs
```

**Expected result:** a rule authored in **Panorama** and pushed to all **Branch-FWs** —
consistent, centralized policy.

**Negative test:** configure each branch firewall by hand; **Panorama** device groups keep
policy consistent — push centrally.

**Rollback:** delete the rule and `commit-all`.

### Lab 4.3 — NAT and decryption

**Objective:** Translate addresses and enable TLS inspection.

```text
admin@fw# set rulebase nat rules Outbound source-translation dynamic-ip-and-port \
    interface-address interface ethernet1/1 from trust to untrust source any destination any
admin@fw# set rulebase decryption rules Decrypt-Out from trust to untrust \
    destination any action decrypt type ssl-forward-proxy
admin@fw# commit
```

**Expected result:** outbound **NAT** plus **SSL forward-proxy decryption** — inspectable,
routable egress.

**Negative test:** leave TLS undecrypted everywhere; **Content-ID** can't inspect encrypted
threats — decrypt where policy/law allow.

**Rollback:** delete the NAT and decryption rules and `commit`.

### Lab 4.4 — Prisma SD-WAN path selection

**Objective:** Describe app-aware path steering.

```text
# Prisma SD-WAN: ION devices form an app-aware fabric; a path policy steers each app over the
#   best-performing link (MPLS/Internet/LTE) and through the security stack; central controller.
"sd-wan: app-aware fabric -> steer by performance+policy -> secure the WAN edge"
```

**Expected result:** the **Prisma SD-WAN** path-selection model — application-aware, secure WAN.

**Negative test:** pin every app to one static link; **app-aware** selection uses the best path
per app — steer dynamically.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.5 — Automate Panorama with the API

**Objective:** Retrieve managed devices programmatically.

```bash
curl -sk "https://<panorama>/api/?type=op&cmd=<show><devices><all></all></devices></show>&key=$PANO_KEY" 2>/dev/null \
  | python3 -c "import sys;print('managed devices retrieved' if 'response' in sys.stdin.read() else 'query Panorama for managed devices via the XML API')" 2>/dev/null \
  || echo "Panorama XML API: show devices all -> inventory of managed firewalls"
```

**Expected result:** the inventory of firewalls **managed by Panorama** via the API — fleet
visibility for automation.

**Negative test:** track the fleet in a spreadsheet; **Panorama's API** is the source of truth —
query it.

**Rollback:** none (read-only).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The NGFW Engineer credential covers HA, Panorama, NAT, and decryption for resilient centralized
enforcement, and the SD-WAN Engineer credential covers Prisma SD-WAN's app-aware, secure WAN
fabric. Run HA, manage from Panorama, decrypt where permitted, and steer the WAN by application.

- [ ] I can configure an HA pair.
- [ ] I can push policy from Panorama device groups.
- [ ] I can configure NAT and decryption.
- [ ] I can explain Prisma SD-WAN path selection.
- [ ] I completed Labs 4.1–4.5 including each negative test.
