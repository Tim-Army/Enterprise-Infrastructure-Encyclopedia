# Chapter 06: The HIP Overlay and Cloaking

## Learning Objectives

- Explain the HIP overlay model and map each idea to its WireGuard equivalent.
- Give each protected device a cryptographic identity and connect it to the overlay through a hub.
- Cloak the underlay so protected devices communicate only over the encrypted overlay.

This is the core of the lab. Each exercise carries both tracks. Airwall's method is **put devices on an encrypted, identity-based overlay and go dark on the underlay** — then authorize only the connections you need (Chapter 07).

## Hands-On Lab

### Lab 6.1 — The HIP model, mapped to WireGuard

**Objective.** State the four ideas of the Airwall overlay and their WireGuard equivalents.

**Background.**

| Airwall / HIP idea | WireGuard equivalent (Track 2) |
|:---|:---|
| Cryptographic host identity | A peer's **public key** |
| Airwall Agent (on-host) | The `wg0` interface + key on that host |
| Airwall Gateway (protects agentless devices) | `aw-gw` acting as a WireGuard gateway for the OT cell (Chapter 08) |
| Airwall Conductor (defines overlays/trust) | The hub config on `aw-gw` + its forward policy |
| Overlay network / trust policy | Which peers exist and what the hub forwards between them |
| Encryption everywhere | WireGuard's built-in encryption |
| Cloaking (dark on the underlay) | Host firewall dropping all non-WireGuard underlay traffic |
| Default-deny | Only configured peers exist; unlisted traffic is silently dropped |

**Walkthrough.**

**Step 1.** Decide overlay membership and identity for each device:

| Device | Overlay identity | Overlay IP | How it joins |
|:---|:---|:---|:---|
| aw-gw | hub key | 10.99.0.254 | is the hub |
| aw-app01 | agent key | 10.99.0.11 | agent (WireGuard) |
| aw-db01 | agent key | 10.99.0.12 | agent (WireGuard) |
| aw-win01 | agent key | 10.99.0.21 | agent (WireGuard) |
| aw-ot01 (PLC) | *(no key — agentless)* | via gateway | carried by aw-gw gateway (Chapter 08) |

**Step 2.** State the model: *every protected device gets a cryptographic identity and an encrypted tunnel to the hub; the underlay goes dark; only authorized identities may connect.*

**Expected result.** An overlay membership and identity plan.

**Negative test.** Plan to give the PLC its own agent key. It can run no software — so it cannot hold a key or a tunnel. That is exactly why Airwall Gateways exist, and why Chapter 08 carries the PLC onto the overlay from `aw-gw` instead.

**Cleanup.** None.

### Lab 6.2 — Build the encrypted overlay

**Objective.** Stand up the overlay: a hub on `aw-gw` and an agent on each server and the HMI, each with a cryptographic identity.

**Track 1 — Real Airwall.** In the Conductor, provision an Airwall Agent on each host and license its identity; the Conductor issues each a HIP identity and establishes encrypted connectivity to the overlay. You then place the agents into an overlay network.

**Track 2 — Native equivalent — WireGuard.**

**Step 1 — keys (cryptographic identities).** On each of `aw-gw`, `aw-app01`, `aw-db01`, `aw-win01` (Linux), install WireGuard and generate a keypair:

```bash
sudo apt -y install wireguard
umask 077; wg genkey | tee privatekey | wg pubkey > publickey
cat publickey    # this public key IS this device's cryptographic identity
```

(On Windows `aw-win01`, install WireGuard for Windows and use **Add Tunnel → Add empty tunnel** to generate its keypair.)

**Step 2 — the hub on `aw-gw`.** Create `/etc/wireguard/wg0.conf` with the hub key and a peer entry for each agent (substitute the real public keys):

```bash
sudo tee /etc/wireguard/wg0.conf > /dev/null <<'EOF'
[Interface]
Address = 10.99.0.254/24
ListenPort = 51820
PrivateKey = <aw-gw-private-key>

[Peer]                      # aw-app01
PublicKey = <aw-app01-public-key>
AllowedIPs = 10.99.0.11/32
[Peer]                      # aw-db01
PublicKey = <aw-db01-public-key>
AllowedIPs = 10.99.0.12/32
[Peer]                      # aw-win01
PublicKey = <aw-win01-public-key>
AllowedIPs = 10.99.0.21/32
EOF
sudo systemctl enable --now wg-quick@wg0
sudo wg show
```

**Step 3 — each agent (spoke).** On `aw-app01` (and analogously `aw-db01`), create `wg0` pointing at the hub; route all overlay traffic to it:

```bash
sudo tee /etc/wireguard/wg0.conf > /dev/null <<'EOF'
[Interface]
Address = 10.99.0.11/24
PrivateKey = <aw-app01-private-key>

[Peer]                      # the hub (aw-gw)
PublicKey = <aw-gw-public-key>
Endpoint = 10.10.20.254:51820
AllowedIPs = 10.99.0.0/24
PersistentKeepalive = 25
EOF
sudo systemctl enable --now wg-quick@wg0
```

On `aw-win01`, set the Windows tunnel's Interface Address to `10.99.0.21/24`, Peer PublicKey to the hub's, Endpoint `10.10.20.254:51820`, AllowedIPs `10.99.0.0/24`, and activate it.

**Step 4.** Confirm the overlay is up and encrypted. From `aw-app01`:

```bash
ping -c1 10.99.0.254        # the hub, over the encrypted overlay
ping -c1 10.99.0.12         # aw-db01 over the overlay (routed via the hub)
```

**Expected result.** Each device has a cryptographic identity (public key) and an encrypted tunnel to the hub; overlay addresses (10.99.0.x) are reachable through it.

**Negative test.** Omit a peer's public key from the hub config; that device cannot join — no identity, no connection. Identity is admission; there is no "allow by IP" back door.

**Cleanup.** Keep the overlay; the next lab cloaks the underlay.

### Lab 6.3 — Cloak the underlay

**Objective.** Make protected devices **dark** on the underlay: they communicate only over the encrypted overlay, and are invisible and unaddressable off it.

**Track 1 — Real Airwall.** An Airwall Agent cloaks its host automatically — the host stops responding on the underlay and accepts only overlay traffic. There is nothing to tune; cloaking is the default posture.

**Track 2 — Native equivalent.** On each agent host, add a firewall that permits only WireGuard (to the hub) plus the overlay interface and a break-glass path, and drops everything else on the underlay. On `aw-db01` (the crown jewel, most important to cloak):

```bash
sudo tee /etc/nftables.conf > /dev/null <<'EOF'
#!/usr/sbin/nft -f
flush ruleset
table inet airwall {
    chain input {
        type filter hook input priority 0; policy drop;   # DARK on the underlay
        ct state established,related accept
        iif "lo" accept
        iifname "wg0" accept                       # overlay traffic is welcome
        udp dport 51820 accept                     # the WireGuard tunnel itself
        ip saddr 10.10.20.1 tcp dport 22 accept    # break-glass mgmt only
    }
}
EOF
sudo nft -f /etc/nftables.conf
```

Apply the same posture on `aw-app01` and `aw-win01` (on Windows, set the firewall to block inbound by default and allow only the WireGuard UDP and the break-glass RDP from `10.10.20.1`).

**Step 2.** Prove the device is now dark on the underlay but alive on the overlay. From `aw-win01` (not yet authorized to the db on the overlay):

```powershell
Test-NetConnection -ComputerName 10.10.20.12 -Port 5432   # underlay: expect False (cloaked!)
ping 10.10.20.12                                          # expect no reply (invisible)
```

From `aw-app01` over the overlay:

```bash
~/checkdb.sh 10.99.0.12     # overlay path to the db: expect 3
```

**Expected result.** The database no longer answers on the underlay — the Chapter 05 lateral-movement path (HMI→10.10.20.12:5432) is already dead, because the device is cloaked. Legitimate app→db works over the encrypted overlay. Chapter 07 then restricts *which overlay identities* may connect.

**Negative test.** Remove the `policy drop` (set it back to `accept`) and re-run the HMI's underlay probe; it reaches the database again. Cloaking — going dark by default — is what removes the underlay attack surface. Restore `policy drop`.

**Cleanup.** Keep the cloaked posture on all agents.

## Summary and Completion Checklist

- [ ] The HIP model mapped to WireGuard, including why the PLC needs a gateway.
- [ ] An encrypted overlay built; every agent has a cryptographic identity and a tunnel to the hub.
- [ ] The underlay cloaked; protected devices are dark off the overlay.
- [ ] The Chapter 05 underlay attack path confirmed dead after cloaking.
