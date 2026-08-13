# Chapter 02: Fundamentals (IC32) — Core Concepts and the Reference Model

## Learning Objectives

- Cover the IC32 foundations: IACS vs IT, the reference model, and defense in depth.
- Understand the OT priority inversion and the threat landscape 62443 addresses.
- Model the Purdue reference architecture with free primitives.

## The exam in brief

**Certificate 1 — Cybersecurity Fundamentals Specialist** (course **IC32**) is the mandatory foundation. It covers the whole standard at a working level: terminology, the reference model, risk concepts, zones/conduits, security levels, and the foundational requirements. This chapter covers the conceptual half; [Chapter 03](03-fundamentals-zones-and-security-levels.md) covers zones, conduits, security levels, and the foundational requirements — the load-bearing 62443 mechanics.

## IACS is not IT

| Dimension | IT | IACS / OT |
|:---|:---|:---|
| Top priority | **Confidentiality** first (C → I → A) | **Availability**/safety first (A → I → C, inverted) |
| Patch cadence | Frequent, fast | Rare, change-controlled (uptime/safety) |
| Device lifespan | 3–5 years | 15–30 years |
| A reboot to fix things | Routine | May be a safety event |
| Protocols | TCP/IP, HTTP, TLS | Modbus, DNP3, EtherNet/IP, PROFINET, OPC — often unauthenticated by design |

This inversion drives every 62443 decision: a control that improves confidentiality but risks availability or safety is often the *wrong* control for an IACS.

## The reference model (Purdue)

62443 uses a layered reference model (aligned with the Purdue Enterprise Reference Architecture):

```text
Level 4/5  Enterprise / business (IT)         <- corporate network, ERP
------------------ IT/OT boundary (DMZ) ------------------
Level 3    Site operations (OT)               <- historians, engineering workstations
Level 2    Area supervisory control           <- HMIs, SCADA
Level 1    Basic control                       <- PLCs, RTUs, controllers
Level 0    Process / field devices             <- sensors, actuators
```

The **IT/OT boundary** (a DMZ between Levels 3 and 4) is where 62443 concentrates: it is the seam attackers cross from the enterprise into the plant, and the reference point for the zones/conduits of [Chapter 03](03-fundamentals-zones-and-security-levels.md).

## Hands-On Lab

Free primitives model the reference architecture. **Cost:** none.

### Lab 2.1 — Build the Purdue levels

**Objective:** Represent the layered model as isolated network segments.

```bash
# each Purdue level as a bridge; devices as namespaces attached to their level
for lvl in L4-enterprise L3-site L2-supervisory L1-control; do
  sudo ip link add "$lvl" type bridge 2>/dev/null; sudo ip link set "$lvl" up
done
attach() { # $1 device  $2 level-bridge  $3 ip
  sudo ip netns add "$1" 2>/dev/null
  sudo ip link add "$1-e" type veth peer name "$1-b"
  sudo ip link set "$1-b" master "$2" up
  sudo ip link set "$1-e" netns "$1"
  sudo ip netns exec "$1" ip addr add "$3/24" dev "$1-e"
  sudo ip netns exec "$1" ip link set "$1-e" up; sudo ip netns exec "$1" ip link set lo up; }
attach erp       L4-enterprise 10.4.0.10
attach historian L3-site       10.3.0.10
attach hmi       L2-supervisory 10.2.0.10
attach plc       L1-control     10.1.0.10
sudo ip netns exec plc ip addr show plc-e | grep inet
```

**Expected result:** Four levels with a representative device each — enterprise ERP, site historian, supervisory HMI, control PLC — the reference model made concrete. Each level is an isolated L2 segment; nothing crosses between them yet (that's the conduit's job).

**Negative test:** Attach the PLC directly to the enterprise bridge — you've collapsed the levels and given corporate IT a direct path to control; the layered model exists precisely to prevent that flat topology.

**Rollback:** Keep for the next lab.

### Lab 2.2 — The IT/OT boundary is the crown jewel

**Objective:** Show why the Level 3/4 seam matters most.

```bash
python3 - <<'EOF'
# Attack path scoring: the fewer hops from internet to control, the higher the risk
paths = {
  "internet -> ERP (L4) -> PLC (L1) directly (flat)": 2,
  "internet -> ERP (L4) -> DMZ -> historian (L3) -> HMI (L2) -> PLC (L1)": 5,
}
for path, hops in paths.items():
    risk = "HIGH" if hops <= 2 else "reduced (defense in depth)"
    print(f"[{risk:28}] {hops} hops: {path}")
EOF
```

**Expected result:** The flat path (2 hops to control) is HIGH risk; the layered path (5 hops through a DMZ) forces an attacker through multiple enforced boundaries. 62443's defense-in-depth is about **maximizing the boundaries** between the internet and Level 1/0, with the IT/OT DMZ as the primary one.

**Negative test:** Assuming a firewall at the perimeter is enough — once inside L4, a flat OT network gives an attacker the plant; 62443 requires boundaries *inside* the OT network too (zones/conduits), not just at the edge.

**Rollback:** Keep for the next lab.

### Lab 2.3 — The priority inversion in practice

**Objective:** Make the availability-first principle concrete.

```bash
python3 - <<'EOF'
# A control decision: does it help security at an unacceptable cost to availability/safety?
def evaluate(control, avail_impact, safety_impact, security_gain):
    if safety_impact == "high": return f"REJECT — {control}: safety impact unacceptable in IACS"
    if avail_impact == "high" and security_gain != "high": return f"REJECT — {control}: availability cost > security gain"
    return f"ACCEPT — {control}"
print(evaluate("auto-reboot on anomaly", "high", "high", "medium"))
print(evaluate("passive network monitoring", "none", "none", "high"))
print(evaluate("inline IPS blocking on the control network", "high", "medium", "medium"))
EOF
```

**Expected result:** Auto-reboot and inline blocking on the control net are rejected (availability/safety cost); passive monitoring is accepted (no operational impact, high visibility). This is the OT security mindset IC32 instills: **security controls must not compromise availability or safety** — which is why OT leans on passive monitoring, segmentation, and change control over IT-style active blocking.

**Negative test:** Applying an IT playbook (aggressive patching, inline blocking, forced reboots) to an IACS — you risk the very availability/safety the plant exists to protect; the inversion is the exam's central theme.

**Rollback:** `for ns in erp historian hmi plc; do sudo ip netns del $ns 2>/dev/null; done; for lvl in L4-enterprise L3-site L2-supervisory L1-control; do sudo ip link del "$lvl" 2>/dev/null; done`.

## Summary and Completion Checklist

- [ ] IACS-vs-IT differences and the availability/safety-first inversion internalized.
- [ ] The Purdue reference model and the IT/OT boundary built and understood.
- [ ] Defense-in-depth as maximizing internal boundaries (not just a perimeter) grasped.
