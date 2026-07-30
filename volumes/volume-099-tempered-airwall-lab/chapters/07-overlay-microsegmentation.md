# Chapter 07: Overlay Microsegmentation

## Learning Objectives

- Express microsegmentation as overlay trust policy — which identities may connect — and enforce it on the hub.
- Confirm that overlay traffic is encrypted on the underlay.
- Confirm that an unauthorized overlay identity cannot reach a protected device.

You built and cloaked the overlay in Chapter 06. Now you decide *which overlay identities may talk*, which is how Airwall expresses microsegmentation — membership and trust, not firewall rules.

## Hands-On Lab

### Lab 7.1 — Enforce the trust policy on the hub

**Objective.** Permit only `aw-app01 → aw-db01` on 5432 across the overlay; deny every other overlay approach to the database.

**Track 1 — Real Airwall.** In the Conductor, place `aw-app01` and `aw-db01` in an overlay network together and leave `aw-win01` out of it. Overlay membership *is* the policy: the HMI, not being in that overlay, cannot see or reach the database.

**Track 2 — Native equivalent.** Because all overlay traffic routes through the hub, enforce the trust policy on `aw-gw`'s overlay forward path:

```bash
sudo nft add table inet airwall
sudo nft add chain inet airwall forward '{ type filter hook forward priority 0 ; policy accept ; }'
# overlay-to-overlay only; established first
sudo nft add rule inet airwall forward iifname "wg0" oifname "wg0" ct state established,related accept
# the one authorized relationship: app -> db on 5432
sudo nft add rule inet airwall forward iifname "wg0" oifname "wg0" \
    ip saddr 10.99.0.11 ip daddr 10.99.0.12 tcp dport 5432 accept
# everything else toward the database identity is denied
sudo nft add rule inet airwall forward iifname "wg0" oifname "wg0" \
    ip daddr 10.99.0.12 log prefix "AIRWALL-DENY db: " level warn drop
```

**Step 2.** Confirm the legitimate overlay flow works and the attack does not. From `aw-app01`:

```bash
~/checkdb.sh 10.99.0.12     # app -> db over the overlay: expect 3
```

From `aw-win01`, over the overlay (its tunnel is up, but it is not authorized to the db):

```powershell
Test-NetConnection -ComputerName 10.99.0.12 -Port 5432   # HMI -> db over overlay: expect False
```

**Expected result.** App→db works over the encrypted overlay; the HMI is denied at the hub. Combined with the cloaking from Chapter 06 (which already killed the underlay path), the database is now reachable *only* by the one authorized identity, over an encrypted tunnel.

**Negative test.** Add a rule permitting `10.99.0.21 → 10.99.0.12:5432` (authorize the HMI). The attack succeeds again — you placed the HMI in the database's overlay. Membership is policy; grant it only where a real dependency exists. Remove the rule.

**Cleanup.** Keep the trust policy.

### Lab 7.2 — Confirm the traffic is encrypted

**Objective.** Prove that the app→db flow crosses the underlay encrypted, not in the clear.

**Walkthrough.** On `aw-gw`, watch the underlay while the app queries the database over the overlay.

**Step 1.** In one shell on `aw-gw`, capture the underlay segment for plaintext PostgreSQL and for WireGuard:

```bash
sudo tcpdump -n -i ens34 tcp port 5432 &     # plaintext db traffic on the underlay
sudo tcpdump -n -i ens34 udp port 51820 &    # WireGuard tunnel
```

**Step 2.** From `aw-app01`, run `~/checkdb.sh 10.99.0.12` a few times, then stop the captures (`sudo kill %1 %2`).

**Expected result.** The `tcp port 5432` capture shows **nothing** — no plaintext database traffic crosses the underlay. The `udp port 51820` capture shows the encrypted WireGuard packets carrying it. The application's data never appears in the clear on the wire.

**Negative test.** Point `~/checkdb.sh` back at the underlay address (`~/checkdb.sh 10.10.20.12`); it fails now (the db is cloaked), but had it worked, the `5432` capture would have shown plaintext. The overlay is what moves the traffic off the visible, unencrypted underlay.

**Cleanup.** Stop any remaining captures.

### Lab 7.3 — Default-deny is dark, not just blocked

**Objective.** Appreciate the difference between "blocked" and "dark".

**Walkthrough.** From `aw-win01`, try to even *discover* the database, on both the underlay and the overlay:

```powershell
ping 10.10.20.12    # underlay: no reply (cloaked - invisible)
ping 10.99.0.12     # overlay: no reply (not in a shared overlay - invisible)
```

**Expected result.** The database answers on neither path. To the HMI it does not appear to exist. This is stronger than a firewall "deny": there is no host to probe, no port to scan, no banner to grab.

**Negative test.** Compare with a conventional firewall that `REJECT`s (sends an RST) — that still confirms the host exists. Airwall's default is to be *dark*: unauthorized identities get silence, which yields no reconnaissance signal at all.

**Cleanup.** None.

### Lab 7.4 — Conductor-managed overlays at scale (Design Exercise)

**Objective.** Reason about the capabilities the Conductor provides that hand-managed WireGuard does not.

**Design Exercise.**

1. You distributed keys and wrote peer configs by hand for four devices. Explain why that does not scale to thousands of devices, and what the Conductor automates: identity issuance, overlay membership, key rotation, and revocation.
2. Airwall expresses segmentation as *overlay membership* rather than as allow/deny rules. Contrast the two mental models: what is easier to reason about, and what is easier to get wrong, when policy is "who is in this overlay" versus "which 5-tuples are permitted"?

**Model answer.**

1. Manual key distribution is O(n) configs to write and O(n²) relationships to reason about, with no safe way to rotate or revoke at scale. The Conductor issues and licenses identities, computes the peer relationships from overlay membership, pushes configuration to agents, and can revoke a compromised identity everywhere at once — the operational layer that makes an identity overlay usable beyond a handful of devices.
2. "Who is in this overlay" is a positive, enumerable statement: a device sees exactly its overlay peers and nothing else, so the blast radius of a membership is visible by construction. "Which 5-tuples are permitted" is a growing list that is easy to make too broad and hard to audit. Membership is easier to reason about; its risk is adding a device to an overlay that is larger than its real need, which is why overlays should be small and purpose-built.

**Expected result.** A written comparison of the two models.

**Negative test.** Argue hand-rolled WireGuard is "the same thing" as Airwall. The cryptographic overlay is the same; the identity lifecycle, revocation, and scale management are not — which is most of the operational cost of running one.

**Cleanup.** None.

## Summary and Completion Checklist

- [ ] Trust policy enforced on the hub; app→db over the overlay works, HMI→db denied.
- [ ] Overlay traffic confirmed encrypted on the underlay (no plaintext 5432).
- [ ] The database confirmed *dark* to unauthorized identities, not merely blocked.
- [ ] Conductor-managed overlays and membership-as-policy reasoned through.
