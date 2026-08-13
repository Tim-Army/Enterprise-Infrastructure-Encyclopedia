# Chapter 03: Fundamentals (IC32) — Zones, Conduits, Security Levels, and Foundational Requirements

## Learning Objectives

- Cover the load-bearing 62443 mechanics: zones, conduits, security levels (SL), and foundational requirements (FR).
- Understand the SL vector and how the seven FRs map to controls.
- Build zones and conduits with default-deny, and score a security level.

## The four mechanics every 62443 exam tests

| Mechanic | What it is |
|:---|:---|
| **Zone** | A grouping of assets with common security requirements (e.g. "control zone", "DMZ zone") |
| **Conduit** | A controlled communication path *between* zones — the only sanctioned way data crosses |
| **Security Level (SL)** | A measure of the strength of protection required/achieved, SL 0–4, expressed as a vector across the seven FRs |
| **Foundational Requirement (FR)** | One of seven categories of security capability every zone is measured against |

## The seven foundational requirements

| FR | Name | Question it answers |
|:---|:---|:---|
| **FR1** | Identification & Authentication Control (IAC) | Who/what is it, and is that proven? |
| **FR2** | Use Control (UC) | Is this actor allowed to do this action? |
| **FR3** | System Integrity (SI) | Is the data/software unaltered? |
| **FR4** | Data Confidentiality (DC) | Is the data protected from disclosure? |
| **FR5** | Restricted Data Flow (RDF) | Is traffic confined to sanctioned conduits (zoning)? |
| **FR6** | Timely Response to Events (TRE) | Are events detected and responded to? |
| **FR7** | Resource Availability (RA) | Is the system kept available (the OT priority)? |

A **security level is a vector**: `SL = { IAC, UC, SI, DC, RDF, TRE, RA }`, each 0–4. A zone's **SL-Target (SL-T)** is what risk demands; its **SL-Achieved (SL-A)** is what the deployed controls deliver; the gap between them drives design ([Chapters 06–07](06-design-requirements.md)).

## Hands-On Lab

Namespaces model zones; nftables models conduits with default-deny; Python scores SL. **Cost:** none.

### Lab 3.1 — Zones and a default-deny conduit

**Objective:** Build two zones connected only by a controlled conduit — FR5 (restricted data flow) made concrete.

```bash
# a control zone and a DMZ zone, joined by a conduit gateway that default-denies
sudo ip link add zbr type bridge; sudo ip link set zbr up
sudo ip netns add conduit   # the conduit enforcement point (firewall between zones)
sudo ip link add cd-e type veth peer name cd-b; sudo ip link set cd-b master zbr up
sudo ip link set cd-e netns conduit; sudo ip netns exec conduit ip addr add 172.16.0.1/24 dev cd-e
sudo ip netns exec conduit ip link set cd-e up; sudo ip netns exec conduit ip link set lo up
sudo ip netns exec conduit sysctl -w net.ipv4.ip_forward=1 >/dev/null
mkasset() { sudo ip netns add "$1"; sudo ip link add "$1-e" type veth peer name "$1-b"
  sudo ip link set "$1-b" master zbr up; sudo ip link set "$1-e" netns "$1"
  sudo ip netns exec "$1" ip addr add "$2/24" dev "$1-e"; sudo ip netns exec "$1" ip link set "$1-e" up
  sudo ip netns exec "$1" ip link set lo up; sudo ip netns exec "$1" ip route add default via 172.16.0.1; }
mkasset scada 172.16.0.10     # control zone asset
mkasset histn 172.16.0.20     # DMZ zone asset
# the conduit default-denies; permit ONLY the sanctioned flow (historian pulls from SCADA on 502)
sudo ip netns exec conduit nft add table ip conduit
sudo ip netns exec conduit nft 'add chain ip conduit fwd { type filter hook forward priority 0; policy drop; }'
sudo ip netns exec conduit nft add rule ip conduit fwd ct state established,related accept
sudo ip netns exec conduit nft add rule ip conduit fwd ip saddr 172.16.0.20 ip daddr 172.16.0.10 tcp dport 502 accept
sudo ip netns exec conduit nft list chain ip conduit fwd | grep -c drop
```

**Expected result:** A conduit that permits only the historian→SCADA Modbus (502) flow and denies everything else by default — **FR5 restricted data flow**: zones talk *only* through sanctioned conduits. This default-deny-plus-explicit-permit is the heart of 62443 network security.

**Negative test:** Set the conduit chain policy to `accept` "to get things working" — you've dissolved the zone boundary; the sanctioned-conduit-only rule is the control, and a default-permit conduit fails FR5.

**Rollback:** Keep for the next lab.

### Lab 3.2 — Prove the conduit enforces

**Objective:** Verify only the sanctioned flow crosses.

```bash
sudo ip netns exec scada bash -c 'nohup nc -lk -p 502 >/dev/null 2>&1 &'
sudo ip netns exec scada bash -c 'nohup nc -lk -p 22  >/dev/null 2>&1 &'
sudo ip netns exec histn bash -c 'nc -z -w2 172.16.0.10 502 && echo "historian->SCADA:502 ALLOWED (sanctioned)"'
sudo ip netns exec histn bash -c 'nc -z -w2 172.16.0.10 22  || echo "historian->SCADA:22 DENIED (not a sanctioned conduit)"'
```

**Expected result:**

```text
historian->SCADA:502 ALLOWED (sanctioned)
historian->SCADA:22 DENIED (not a sanctioned conduit)
```

The Modbus flow crosses the conduit; an SSH attempt to the control asset is denied. A conduit is not "a firewall between zones" in the abstract — it is a **specific, enumerated set of permitted flows**, and everything else is denied.

**Negative test:** An engineering-workstation flow you forgot to enumerate is also denied — which is correct for FR5, and the reason conduit design (Chapter 06) must capture every legitimate flow up front.

**Rollback:** Keep for the next lab.

### Lab 3.3 — Score a security level vector

**Objective:** Express a zone's SL as a vector across the seven FRs.

```bash
python3 - <<'EOF'
# SL vector: each FR rated 0-4 by the controls in place
FRS = ["IAC","UC","SI","DC","RDF","TRE","RA"]
control_zone = {"IAC":2, "UC":2, "SI":3, "DC":1, "RDF":3, "TRE":2, "RA":3}
target       = {"IAC":3, "UC":3, "SI":3, "DC":1, "RDF":3, "TRE":2, "RA":3}
print("FR   SL-A  SL-T  gap")
for fr in FRS:
    a, t = control_zone[fr], target[fr]
    gap = "OK" if a >= t else f"GAP (+{t-a})"
    print(f"{fr:<4} {a:^4} {t:^4}  {gap}")
overall_a = min(control_zone.values())
print(f"\nzone SL-A (worst FR) = SL{overall_a};  SL-T = SL{min(target.values())}")
EOF
```

**Expected result:**

```text
FR   SL-A  SL-T  gap
IAC   2    3    GAP (+1)
UC    2    3    GAP (+1)
...
zone SL-A (worst FR) = SL1;  SL-T = SL1
```

The SL is a **per-FR vector**, and the gaps (IAC and UC below target) are the design work items. A zone's headline SL is often the **weakest** FR — a strong zone with one weak requirement is only as strong as that requirement. This vector is the language of the risk-assessment and design certificates.

**Negative test:** Reporting a single scalar "this zone is SL2" without the vector — hides which FR is weak; 62443 requires the per-FR breakdown, and the exam tests the vector, not a scalar.

**Rollback:** `for ns in conduit scada histn; do sudo ip netns del $ns 2>/dev/null; done; sudo ip link del zbr`.

## Summary and Completion Checklist

- [ ] Zones, conduits, security levels, and the seven FRs internalized.
- [ ] A default-deny conduit built and proven (FR5 restricted data flow).
- [ ] The SL vector (per-FR, SL-A vs SL-T, weakest-FR headline) scored.
- [ ] IC32 Fundamentals coverage complete across Chapters 02–03.
