# Chapter 06: Design (IC34) — Cybersecurity Requirements and Zone/Conduit Design

## Learning Objectives

- Cover the IC34 Design Specialist's first half: the Cybersecurity Requirements Specification (CRS) and zone/conduit design.
- Translate SL-T into concrete system security requirements (SRs).
- Model a CRS and a segmented zone/conduit design.

## The exam in brief

**Certificate 3 — Cybersecurity Design Specialist** (course **IC34**) maps to the **Design** phase and to **IEC 62443-3-3** (system security requirements and security levels). It takes the risk assessment's **SL-T** output and produces a **secure design**: a Cybersecurity Requirements Specification (CRS), a zone/conduit architecture, and selected countermeasures. This chapter covers the CRS and segmentation; [Chapter 07](07-design-countermeasures.md) covers countermeasures and verifying SL-Achieved.

## From SL-T to system requirements

IEC 62443-3-3 defines **System Requirements (SRs)** grouped under the seven FRs, each with **Requirement Enhancements (REs)** that raise the achieved SL. The design maps each zone's SL-T to the specific SRs that deliver it:

| SL-T on FR1 (IAC) | Representative requirement |
|:---|:---|
| SL1 | Identify and authenticate human users |
| SL2 | + unique identification, unsuccessful-attempt handling |
| SL3 | + multifactor for untrusted networks, hardware-backed auth for some assets |
| SL4 | + multifactor for all interactive access |

The CRS captures these SRs per zone, with the SL-T that justifies each — the contract between the risk assessment and the implementation.

## Hands-On Lab

Python generates a CRS from SL-T; nftables models the segmented design. **Cost:** none.

### Lab 6.1 — Generate a Cybersecurity Requirements Specification

**Objective:** Turn an SL-T vector into concrete system requirements.

```bash
python3 - <<'EOF'
# CRS: for each FR's SL-T, list the requirement(s) the design must satisfy
sl_t = {"IAC":3,"UC":3,"SI":3,"DC":1,"RDF":3,"TRE":2,"RA":3}
catalog = {
  "IAC": {1:"authenticate users", 2:"unique IDs + lockout", 3:"MFA from untrusted networks"},
  "UC":  {1:"authorize actions", 2:"least privilege roles", 3:"enforce + audit privileged use"},
  "SI":  {1:"integrity checks", 2:"malware protection", 3:"verified boot / signed firmware"},
  "RDF": {1:"basic segmentation", 2:"zone firewalls", 3:"deny-by-default conduits + monitoring"},
  "TRE": {1:"log events", 2:"centralize + alert"},
  "RA":  {1:"backups", 2:"redundancy", 3:"DoS protection + tested recovery"},
}
print("CRS (control zone):")
for fr, lvl in sl_t.items():
    reqs = catalog.get(fr, {})
    chosen = reqs.get(lvl) or reqs.get(max((k for k in reqs if k<=lvl), default=0)) or "(no requirement at this SL)"
    if fr == "DC": chosen = "minimal (OT: confidentiality low priority)"
    print(f"  FR {fr} (SL-T {lvl}): {chosen}")
EOF
```

**Expected result:** A per-FR requirements list derived from the SL-T — e.g. FR1 SL3 requires MFA from untrusted networks, FR5 SL3 requires deny-by-default conduits plus monitoring. The CRS is **traceable**: every requirement traces back to an SL-T that traces back to a risk. That traceability is what the Design exam tests.

**Negative test:** A design with requirements that don't trace to an SL-T (gold-plating) or SL-Ts with no requirement (gaps) — 62443 design is a closed loop from risk to requirement; untraceable requirements and unmet SL-Ts both fail review.

**Cleanup:** None.

### Lab 6.2 — Zone/conduit architecture

**Objective:** Design the segmented network the CRS demands (FR5 at SL3).

```bash
python3 - <<'EOF'
# The design: zones, their SL-T, and the conduits (with sanctioned flows) between them
design = {
  "zones": {
    "Enterprise (L4)":   {"sl_t": 1},
    "IT/OT DMZ":         {"sl_t": 2},
    "Site ops (L3)":     {"sl_t": 2},
    "Supervisory (L2)":  {"sl_t": 3},
    "Control (L1)":      {"sl_t": 3},
  },
  "conduits": [
    ("Enterprise (L4)", "IT/OT DMZ",   "HTTPS to DMZ broker only; no direct L4->L3"),
    ("IT/OT DMZ",       "Site ops (L3)","historian replication (one-way where possible)"),
    ("Site ops (L3)",   "Supervisory (L2)","engineering access, brokered + logged"),
    ("Supervisory (L2)","Control (L1)", "control protocol (Modbus/OPC), deny-by-default"),
  ],
}
print("Zones (SL-T):");  [print(f"  {z}: SL{v['sl_t']}") for z,v in design["zones"].items()]
print("Conduits (sanctioned flow only):")
for a,b,flow in design["conduits"]: print(f"  {a} <-> {b}: {flow}")
print("\nNo conduit skips a level (no L4->L1 direct) — the DMZ is the mandatory hop.")
EOF
```

**Expected result:** A layered design where SL-T rises toward the control zone, conduits connect only adjacent zones, and no path skips the IT/OT DMZ. The design's core rule: **the DMZ is the mandatory break between IT and OT**, and each conduit carries only enumerated flows — FR5 (restricted data flow) realized architecturally.

**Negative test:** A "convenience" conduit from Enterprise straight to Control (for a vendor's remote support) — it bypasses the DMZ and every intermediate zone's protection; such flows must be brokered through the DMZ (jump host, one-time access), never a direct conduit.

**Cleanup:** None.

### Lab 6.3 — Enforce the design with default-deny conduits

**Objective:** Implement one conduit of the design and prove the segmentation.

```bash
sudo ip netns add l2sup; sudo ip netns add l1ctl; sudo ip netns add gw
sudo ip link add cbr type bridge; sudo ip link set cbr up
for n in l2sup:10.2.0.10 l1ctl:10.1.0.10 gw:10.0.0.1; do
  name="${n%%:*}"; ip="${n##*:}"
  sudo ip link add "$name-e" type veth peer name "$name-b"; sudo ip link set "$name-b" master cbr up
  sudo ip link set "$name-e" netns "$name"; sudo ip netns exec "$name" ip addr add "$ip/16" dev "$name-e"
  sudo ip netns exec "$name" ip link set "$name-e" up; sudo ip netns exec "$name" ip link set lo up
done
sudo ip netns exec l2sup ip route add default via 10.0.0.1
sudo ip netns exec l1ctl ip route add default via 10.0.0.1
sudo ip netns exec gw sysctl -w net.ipv4.ip_forward=1 >/dev/null
# conduit: supervisory -> control, ONLY Modbus 502, default deny
sudo ip netns exec gw nft add table ip cd
sudo ip netns exec gw nft 'add chain ip cd f { type filter hook forward priority 0; policy drop; }'
sudo ip netns exec gw nft add rule ip cd f ct state established,related accept
sudo ip netns exec gw nft add rule ip cd f ip saddr 10.2.0.10 ip daddr 10.1.0.10 tcp dport 502 accept
sudo ip netns exec l1ctl bash -c 'nohup nc -lk -p 502 >/dev/null 2>&1 &'
sudo ip netns exec l2sup bash -c 'nc -z -w2 10.1.0.10 502 && echo "L2->L1:502 permitted (control protocol conduit)"'
sudo ip netns exec l2sup bash -c 'nc -z -w2 10.1.0.10 80 || echo "L2->L1:80 denied (not in the conduit)"'
```

**Expected result:** The supervisory→control Modbus flow is permitted and a web request denied — the design's conduit enforced. Design isn't a diagram; it is enumerated, default-deny conduits that a firewall/gateway implements, which is what makes SL-A verifiable in [Chapter 07](07-design-countermeasures.md).

**Negative test:** Implementing the zones but leaving the conduit default-accept — the diagram says "segmented" but the traffic says "flat"; the design is only real when the enforcement matches it.

**Cleanup:** `for ns in l2sup l1ctl gw; do sudo ip netns del $ns 2>/dev/null; done; sudo ip link del cbr`.

## Summary and Completion Checklist

- [ ] A traceable CRS generated from SL-T (risk → SL-T → requirement).
- [ ] A zone/conduit architecture with the DMZ as the mandatory IT/OT break designed.
- [ ] A default-deny conduit implemented and proven against the design.
