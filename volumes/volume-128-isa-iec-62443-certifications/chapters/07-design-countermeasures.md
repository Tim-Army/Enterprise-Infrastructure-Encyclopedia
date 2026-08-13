# Chapter 07: Design (IC34) — Countermeasures and Verifying Security Levels

## Learning Objectives

- Cover the IC34 design's second half: selecting countermeasures and verifying SL-Achieved.
- Understand compensating controls and the OT constraints on countermeasure choice.
- Model SL-A verification against the CRS.

## Closing the gap without breaking the plant

The design selects countermeasures to raise SL-Achieved to SL-Target — but under the OT constraint from [Chapter 02](02-fundamentals-concepts.md): **the countermeasure must not harm availability or safety.** Where an ideal control is operationally impossible (you cannot patch a running safety PLC), 62443 relies on **compensating controls** (segmentation, monitoring, access brokering) that reduce risk without touching the asset.

| Gap (FR) | Ideal control | OT-viable / compensating control |
|:---|:---|:---|
| FR1 IAC | MFA on the PLC | MFA at the access broker/jump host in front of it |
| FR3 SI | Patch the PLC firmware CVE | Virtual patch: block the exploit at the conduit; monitor |
| FR5 RDF | — | Deny-by-default conduits + passive monitoring |
| FR7 RA | — | Redundancy, tested backups, DoS protection at the boundary |

## Hands-On Lab

Python and nftables model countermeasure selection and SL-A verification. **Cost:** none.

### Lab 7.1 — Select countermeasures under OT constraints

**Objective:** Choose controls that close the gap without operational harm.

```bash
python3 - <<'EOF'
# For each gap, pick a control that raises SL-A without hurting availability/safety
gaps = [
  {"fr":"IAC", "need":"SL3", "asset":"safety PLC (cannot add local MFA)"},
  {"fr":"SI",  "need":"SL3", "asset":"unpatchable legacy controller (vendor EOL)"},
  {"fr":"RDF", "need":"SL3", "asset":"control zone"},
]
def choose(g):
    if g["fr"]=="IAC": return "MFA at jump host / access broker in front of the PLC (compensating)"
    if g["fr"]=="SI":  return "virtual patch at conduit + integrity monitoring (asset untouched)"
    if g["fr"]=="RDF": return "deny-by-default conduits + passive IDS (no active blocking on control net)"
    return "review"
for g in gaps:
    print(f"FR {g['fr']} -> {g['need']} for {g['asset']}")
    print(f"   control: {choose(g)}\n")
EOF
```

**Expected result:** Compensating controls that raise SL-A without modifying the fragile assets — MFA at the broker (not the PLC), virtual patching at the conduit (not the controller), passive monitoring (not inline blocking). This is the design's defining skill: **reach the SL-T with controls the plant can actually run.**

**Negative test:** Specifying "install MFA and EDR agent on the safety PLC" — the device may not support it, and forcing it risks the safety function; the compensating control (protect *around* the asset) is the 62443-correct answer.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.2 — Virtual patching as a compensating control

**Objective:** Implement a virtual patch — block a known exploit at the conduit without touching the asset.

```bash
sudo ip netns add plc-old; sudo ip netns add cdgw
sudo ip link add vp type bridge; sudo ip link set vp up
for n in plc-old:10.1.0.50 cdgw:10.1.0.1; do
  name="${n%%:*}"; ip="${n##*:}"
  sudo ip link add "$name-e" type veth peer name "$name-b"; sudo ip link set "$name-b" master vp up
  sudo ip link set "$name-e" netns "$name"; sudo ip netns exec "$name" ip addr add "$ip/24" dev "$name-e"
  sudo ip netns exec "$name" ip link set "$name-e" up; sudo ip netns exec "$name" ip link set lo up
done
sudo ip netns exec plc-old ip route add default via 10.1.0.1
sudo ip netns exec cdgw sysctl -w net.ipv4.ip_forward=1 >/dev/null
# virtual patch: the legacy PLC has a CVE reachable on tcp/20000 (DNP3-ish); block it at the conduit
sudo ip netns exec cdgw nft add table ip vpatch
sudo ip netns exec cdgw nft 'add chain ip vpatch f { type filter hook forward priority 0; policy accept; }'
sudo ip netns exec cdgw nft add rule ip vpatch f ip daddr 10.1.0.50 tcp dport 20000 counter drop
sudo ip netns exec cdgw nft add rule ip vpatch f ip daddr 10.1.0.50 tcp dport 502 accept
echo "legacy PLC untouched; the vulnerable service is unreachable through the conduit"
sudo ip netns exec cdgw nft list chain ip vpatch f | grep 20000
```

**Expected result:** The vulnerable port is blocked at the conduit while the legitimate Modbus (502) still reaches the PLC — the CVE is mitigated **without patching or rebooting the controller**. Virtual patching (block/monitor the exploit path at the network) is how 62443 designs protect unpatchable OT assets, which are the norm.

**Negative test:** Insisting on patching the EOL controller — the vendor ships no fix and a firmware attempt could brick a running asset; the conduit-level virtual patch is the viable control.

**Rollback:** `for ns in plc-old cdgw; do sudo ip netns del $ns 2>/dev/null; done; sudo ip link del vp`.

### Lab 7.3 — Verify SL-Achieved against the CRS

**Objective:** Confirm the designed controls meet the SL-T for every FR.

```bash
python3 - <<'EOF'
FRS = ["IAC","UC","SI","DC","RDF","TRE","RA"]
sl_t = {"IAC":3,"UC":3,"SI":3,"DC":1,"RDF":3,"TRE":2,"RA":3}
# SL-A after the designed (compensating) controls:
sl_a = {"IAC":3,"UC":3,"SI":3,"DC":1,"RDF":3,"TRE":2,"RA":3}
ok = True
print("FR   SL-T SL-A  verdict")
for fr in FRS:
    meets = sl_a[fr] >= sl_t[fr]
    ok = ok and meets
    print(f"{fr:<4} {sl_t[fr]:^4}{sl_a[fr]:^4}  {'MEETS' if meets else 'SHORT'}")
print(f"\nDesign {'VERIFIED — SL-A >= SL-T on all FRs' if ok else 'INCOMPLETE — gaps remain'}")
EOF
```

**Expected result:** SL-A meets SL-T on every FR — the design is verified. The Design certificate closes when the **verified SL-A** demonstrates the CRS is satisfied; that verification (and the residual risk being tolerable) is the hand-off to operations. Any FR still SHORT is unfinished design work.

**Negative test:** Declaring the design done with FR1 still SHORT — the zone doesn't achieve its target protection; SL-A ≥ SL-T on **every** FR is the bar, not most of them.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Countermeasures selected under OT constraints (compensating controls).
- [ ] Virtual patching implemented for an unpatchable asset.
- [ ] SL-A verified against SL-T on every FR — the design closed.
- [ ] IC34 Design coverage complete across Chapters 06–07.
