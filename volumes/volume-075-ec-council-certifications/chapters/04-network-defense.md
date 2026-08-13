# Chapter 04: Network Defense

## Learning Objectives

- Apply the Certified Network Defender (CND) defense-in-depth approach.
- Design network segmentation and access control.
- Secure ICS/SCADA and OT networks.
- Monitor and respond to network threats.
- Complete a walkthrough for each network-defense domain.

## Theory and Architecture

The **Certified Network Defender (CND)** is EC-Council's blue-team flagship — a hands-on credential
for **protecting, detecting, and responding** on networks, aligned to **US DoD 8140/8570**. CND
covers **defense-in-depth**: perimeter and internal controls, **network segmentation**, firewalls
and IDS/IPS, secure protocols, VPNs, endpoint and application defense, network traffic monitoring,
and incident response. The **ICS/SCADA Cybersecurity** program extends network defense into
**operational technology** — protecting the fragile control systems that run physical processes,
where safety and availability lead and passive monitoring is preferred. Together these validate the
defender's core skill: building a **layered, segmented, monitored** network that contains and detects
threats. This chapter teaches each with a hands-on defensive walkthrough (segmentation policy,
firewall rules, traffic monitoring, and OT-safe defense).

## Design Considerations

Layer controls (**defense-in-depth**) so no single failure is fatal. **Segment** the network by
trust and function, and default-deny between zones. Monitor **traffic and logs** continuously. For
**ICS/SCADA**, prefer **passive** monitoring and strict segmentation — never intrusive scanning of
OT. Plan **response** before an incident.

## Implementation and Automation

The labs build segmentation, a firewall policy, traffic monitoring, and OT-safe defense.

## Validation and Troubleshooting

Confirm the network-defense map:

```text
CND = defense-in-depth (perimeter+internal), segmentation, firewall/IDS/IPS, VPN, monitoring, response. DoD 8140 aligned.
ICS/SCADA = OT network defense (safety-first, passive monitoring, strict segmentation).
```

Common pitfalls: a flat network (one breach reaches everything); and treating OT like IT (intrusive
scans can disrupt a process).

## Security and Best Practices

Build **layered, segmented, monitored** networks with default-deny between zones, continuous traffic
monitoring, and a ready response plan. Protect OT with **passive** monitoring and segmentation. All
work is defensive.

## Hands-On Lab

Network-defense walkthroughs. **Shared prerequisites** — Linux with `python3`, `tcpdump`/`tshark`,
in a lab. **Cost:** none.

### Lab 4.1 — CND: design segmentation

**Objective:** Separate zones by trust.

```python
python3 - <<'PY'
zones=["internet","dmz","internal","management","ot"]
policy={("internet","dmz"):"allow 443","("dmz","internal")":"allow app port",
        ("internal","management"):"allow admin from jump host only",("internet","ot"):"DENY"}
for k,v in policy.items(): print(f"{k}: {v}")
print("CND: segment by trust; default-deny between zones; OT most isolated")
PY
```

**Expected result:** a **segmented** zone policy with default-deny and isolated OT — CND
defense-in-depth.

**Negative test:** allow internet→internal directly for convenience; that erases segmentation —
force traffic through the **DMZ** and controls.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.2 — CND: default-deny firewall policy

**Objective:** Allow only what's needed.

```python
python3 - <<'PY'
rules=[("allow","tcp",443,"web from any"),("allow","tcp",22,"ssh from mgmt subnet"),
       ("deny","any","any","default deny + log")]
for action,proto,port,desc in rules: print(f"{action:5} {proto}/{port}: {desc}")
print("CND: explicit allow-list + default-deny with logging")
PY
```

**Expected result:** an allow-list ending in **default-deny with logging** — the CND firewall
approach.

**Negative test:** end with default-allow; unlisted traffic passes — **default deny**, and log it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.3 — CND: monitor network traffic

**Objective:** See what's on the wire.

```bash
tcpdump -w /tmp/cnd.pcap -c 25 -i lo 2>/dev/null & (ping -c 4 127.0.0.1 >/dev/null); wait
tshark -r /tmp/cnd.pcap -q -z io,phs 2>/dev/null | head -15
echo "CND: continuous traffic monitoring reveals anomalies (unexpected protocols/hosts)"
```

**Expected result:** a **protocol breakdown** of captured traffic — network monitoring (CND).

**Negative test:** rely only on device logs; **traffic monitoring** catches what endpoints miss —
watch the wire too.

**Rollback:** `rm -f /tmp/cnd.pcap`.

### Lab 4.4 — ICS/SCADA: OT-safe defense

**Objective:** Protect OT without disruption.

```python
python3 - <<'PY'
ot_rules={"monitoring":"passive tap only (no active scans of PLCs)",
          "segmentation":"OT in its own zone behind an IT/OT DMZ",
          "access":"jump host + MFA for engineering access",
          "change":"safety-gated change windows"}
for k,v in ot_rules.items(): print(f"{k:12}: {v}")
print("ICS/SCADA: safety & availability first; never intrusive-scan OT")
PY
```

**Expected result:** OT-safe defense (passive monitoring, DMZ, controlled access) — ICS/SCADA
security.

**Negative test:** run an active vulnerability scan against a PLC; it can crash the process — use
**passive** monitoring in OT.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Network Defense (CND, ICS/SCADA) builds layered, segmented, monitored networks with default-deny
between zones and OT-safe passive defense — the DoD-8140-aligned blue-team core.

- [ ] I can design network segmentation (CND).
- [ ] I can write a default-deny firewall policy.
- [ ] I can monitor network traffic.
- [ ] I can defend OT safely (ICS/SCADA).
- [ ] I completed Labs 4.1–4.4 including each negative test.
