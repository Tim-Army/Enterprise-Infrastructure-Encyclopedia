# Chapter 04: INE — NIOS DDI Expert

## Learning Objectives

- Explain what the INE certifies and its prerequisite knowledge.
- Summarize the expert topic areas.
- Design Grid setup and high availability.
- Perform upgrades, root-cause analysis, and DNS/DHCP troubleshooting.
- Complete a walkthrough for each expert topic.

## Theory and Architecture

The **NIOS DDI Expert (INE)** validates expert-level deployment and troubleshooting,
building on administrator knowledge. Its topic areas: **Grid setup and high
availability** (Grid Master Candidate, HA pairs, VRRP), **upgrades** (Grid upgrade
process, rollback), **root-cause analysis**, and a **DNS/DHCP troubleshooting
methodology**. The expert keeps the Grid resilient and diagnoses failures
systematically.

## Design Considerations

The expert designs for resilience: a **Grid Master Candidate** for Master failover, **HA
pairs** for members, and tested **upgrade/rollback** procedures. Troubleshooting follows
a **methodology** — reproduce, isolate the layer (Grid comms, DNS, DHCP), inspect logs/
captures, and confirm the fix — rather than guessing.

## Implementation and Automation

The labs use the WAPI and CLI/log tools for each expert topic — HA status, upgrade
state, RCA data, and troubleshooting.

## Validation and Troubleshooting

Confirm the topic areas:

```text
INE topics: Grid setup + high availability (GMC, HA pairs, VRRP);
upgrades (+ rollback); root-cause analysis; DNS/DHCP troubleshooting methodology.
```

Common pitfalls: no **Grid Master Candidate** (no Master failover); and upgrading without
a tested **rollback**.

## Security and Best Practices

Deploy a **Grid Master Candidate** and **HA member pairs**, test **upgrade and rollback**
before production, follow a repeatable **troubleshooting methodology**, and capture
evidence (logs, syslog, packet captures) for **root-cause analysis**.

## Hands-On Lab

Per-topic walkthroughs — INE. **Shared prerequisites** — a NIOS Grid; WAPI/CLI access.
**Cost:** none beyond a lab Grid.

### Lab 4.1 — Grid setup and high availability

**Objective:** Check HA and Master-candidate status.

```bash
curl -sS -k -u admin:infoblox "https://<grid>/wapi/v2.13/member?_return_fields=host_name,master_candidate,ha_enabled" \
  | python3 -c "import sys,json;print([(m['host_name'],m.get('master_candidate'),m.get('ha_enabled')) for m in json.load(sys.stdin)])"
```

**Expected result:** which members are **HA-enabled** and **Master candidates** — the
Grid HA topic.

**Negative test:** run a single Grid Master with no candidate; a **GMC** is required for
Master failover — designate one.

**Rollback:** none (read-only).

### Lab 4.2 — Upgrades

**Objective:** Review the Grid upgrade status.

```bash
curl -sS -k -u admin:infoblox "https://<grid>/wapi/v2.13/upgradestatus?_return_fields=type,upgrade_state" \
  | python3 -c "import sys,json;print([(u.get('type'),u.get('upgrade_state')) for u in json.load(sys.stdin)][:5])"
```

**Expected result:** the current **upgrade state** across the Grid — the upgrades topic.

**Negative test:** upgrade all members at once with no rollback plan; use the **staged
Grid upgrade** (with distribution/test/rollback) — never big-bang.

**Rollback:** none (read-only).

### Lab 4.3 — Root-cause analysis

**Objective:** Pull recent Grid/service events for RCA.

```bash
curl -sS -k -u admin:infoblox "https://<grid>/wapi/v2.13/grid:servicerestart:status" 2>/dev/null \
  || echo "review: Grid > Reporting/Syslog + member logs for service events"
```

**Expected result:** service-restart/event data (or the log sources) to anchor **root-
cause analysis** — the RCA topic.

**Negative test:** restart services hoping it fixes the issue; **find the root cause**
from logs/events first.

**Rollback:** none (read-only).

### Lab 4.4 — DNS/DHCP troubleshooting methodology

**Objective:** Apply a structured troubleshooting flow.

```text
# Methodology: reproduce -> isolate layer (Grid comms / DNS resolution / DHCP lease)
#   -> inspect (dig, query logs, DHCP lease history, packet capture) -> fix -> verify.
dig @<grid-dns-member> web1.lab.example A     # DNS layer check
```

**Expected result:** a repeatable **isolate-and-verify** methodology (starting with a
`dig` at the DNS layer) — the troubleshooting topic.

**Negative test:** change many settings at once; **isolate one layer at a time** so you
know what fixed it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The INE certifies expert NIOS deployment and troubleshooting across Grid setup and HA
(GMC, HA pairs), upgrades with rollback, root-cause analysis, and a DNS/DHCP
troubleshooting methodology.

- [ ] I can check HA and Master-candidate status.
- [ ] I can review the staged Grid upgrade state.
- [ ] I can gather evidence for root-cause analysis.
- [ ] I can apply a layer-by-layer troubleshooting methodology.
- [ ] I completed Labs 4.1–4.4 including each negative test.
