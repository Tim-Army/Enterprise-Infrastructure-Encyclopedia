# Chapter 06: Network Security (ONSA)

## Learning Objectives

- Cover ONSA: network access control, layer-2 vs layer-3 NAC, and network enforcement.
- Understand the risks of unsecured networks and NAC enforcement methods.
- Model a NAC admission decision and the L2-vs-L3 distinction.

## The certificate in brief

**ONSA** (Network Security Associate) covers securing networks: the risks of unsecured networks, network enforcement tool methodologies, network security principles, and the difference between **layer-2 and layer-3 NAC** deployments. It extends the device-trust theme from [Chapter 05](05-endpoint-compliance.md) to the network layer.

## NAC: control what connects to the network

**Network Access Control (NAC)** decides which devices may join the network and what they may reach, based on identity and posture. The enforcement point can sit at different layers:

| Layer | Enforcement | Trade-off |
|:---|:---|:---|
| **Layer 2 (802.1X)** | At the switch port / wireless — device is authenticated *before* getting an IP; assigned a VLAN | Strongest (blocks at the edge) but needs 802.1X-capable infrastructure and supplicants |
| **Layer 3** | At a gateway/inline device after the device has an IP — controls routed access | Easier to deploy on legacy gear; the device is already on the L2 segment |

ONSA tests knowing **where** enforcement happens and the trade-off: L2 stops an untrusted device at the door; L3 lets it onto the local segment but restricts where it can route.

## Hands-On Lab

Python and namespaces model NAC. **Cost:** none.

### Lab 6.1 — A NAC admission decision

**Objective:** Admit/deny/quarantine a device from identity + posture, assigning a network.

```bash
python3 - <<'EOF'
# NAC combines authentication + posture -> a network assignment (VLAN/segment)
def nac(identity_ok, posture_ok, device_type):
    if not identity_ok: return "DENY (authentication failed)"
    if not posture_ok:  return "QUARANTINE VLAN (remediation only)"
    return {"corporate":"PRODUCTION VLAN", "iot":"IOT VLAN (restricted)", "guest":"GUEST VLAN (internet only)"}.get(device_type, "DEFAULT VLAN")
print("corp laptop, authed, compliant:", nac(True, True, "corporate"))
print("corp laptop, authed, non-compl:", nac(True, False, "corporate"))
print("IP camera (IoT), authed:       ", nac(True, True, "iot"))
print("unknown device, no auth:       ", nac(False, False, "guest"))
EOF
```

**Expected result:** Each device lands in the right network — compliant corporate to production, non-compliant to a quarantine VLAN, IoT to a restricted segment, unauthenticated denied. NAC's output is not just yes/no but **which network** a device joins, enforcing segmentation by identity and posture. This is ONSA's core.

**Negative test:** A flat network where any device that plugs in reaches everything — an unmanaged IoT camera or a contractor laptop then has the run of the network; NAC's per-device segmentation is what prevents that, and its absence is the "unsecured network" risk ONSA names.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.2 — Layer 2 vs layer 3 enforcement

**Objective:** Make the L2/L3 distinction concrete.

```bash
python3 - <<'EOF'
scenarios = [
  {"desc":"802.1X on the switch port", "layer":"L2",
   "effect":"unauthenticated device never gets an IP or VLAN — blocked at the port"},
  {"desc":"inline gateway ACL after DHCP", "layer":"L3",
   "effect":"device gets an IP on the segment, but routing to other subnets is filtered"},
]
for s in scenarios:
    print(f"[{s['layer']}] {s['desc']}\n     -> {s['effect']}\n")
print("Rule: L2 stops the device at the door; L3 lets it onto the local segment but limits where it routes.")
print("Choose L2 for strongest control (802.1X infra required); L3 where legacy gear can't do 802.1X.")
EOF
```

**Expected result:** L2 (802.1X) blocks before an IP is issued; L3 admits to the segment but filters routing. ONSA tests this exact distinction — the enforcement layer determines whether an untrusted device is stopped **at the door** (L2) or merely **restricted after entry** (L3), and which you can deploy depends on your infrastructure.

**Negative test:** Assuming L3 NAC gives the same protection as L2 — an untrusted device on the L2 segment can already attack its neighbors (ARP spoofing, lateral scanning) before any L3 filter applies; the layer matters for the threat surface.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.3 — Segment an untrusted device (model)

**Objective:** Show segmentation confining an admitted-but-untrusted device.

```bash
sudo ip netns add iot; sudo ip netns add gw; sudo ip link add nbr type bridge; sudo ip link set nbr up
for n in iot:10.0.5.10 gw:10.0.5.1; do name="${n%%:*}"; ip="${n##*:}"
  sudo ip link add "$name-e" type veth peer name "$name-b"; sudo ip link set "$name-b" master nbr up
  sudo ip link set "$name-e" netns "$name"; sudo ip netns exec "$name" ip addr add "$ip/24" dev "$name-e"
  sudo ip netns exec "$name" ip link set "$name-e" up; sudo ip netns exec "$name" ip link set lo up; done
sudo ip netns exec iot ip route add default via 10.0.5.1
sudo ip netns exec gw sysctl -w net.ipv4.ip_forward=1 >/dev/null
# NAC put the IoT device in a restricted segment: it may reach its update server only, nothing else
sudo ip netns exec gw nft add table ip nac
sudo ip netns exec gw nft 'add chain ip nac f { type filter hook forward priority 0; policy drop; }'
sudo ip netns exec gw nft add rule ip nac f ip saddr 10.0.5.10 ip daddr 203.0.113.50 tcp dport 443 accept
sudo ip netns exec gw nft add rule ip nac f ct state established,related accept
echo "IoT device confined: update server (443) only; all other destinations dropped by the NAC segment policy"
sudo ip netns exec gw nft list chain ip nac f | grep -c accept
```

**Expected result:** The IoT device can reach only its update server and is denied everything else — segmentation confining an admitted-but-untrusted device to exactly what it needs. NAC + segmentation means even devices you must admit (an IP camera, a vendor tool) are boxed into a restricted segment, limiting blast radius.

**Negative test:** Admitting the IoT device to the production VLAN "because it's just a camera" — cameras are a common pivot point; the restricted segment is the control that contains them.

**Rollback:** `for ns in iot gw; do sudo ip netns del $ns 2>/dev/null; done; sudo ip link del nbr`.

## Summary and Completion Checklist

- [ ] NAC admission (identity + posture → network assignment) modeled.
- [ ] Layer-2 vs layer-3 enforcement distinction internalized.
- [ ] Segmentation confining an admitted untrusted device drilled.
