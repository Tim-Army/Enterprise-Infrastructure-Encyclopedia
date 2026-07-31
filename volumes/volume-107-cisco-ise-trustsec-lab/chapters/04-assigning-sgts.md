# Chapter 04: Assigning Security Group Tags

## Learning Objectives

- Bind each endpoint's IP to its SGT with a static IP-SGT mapping in ISE.
- Distribute the bindings to the enforcer with **SXP**.
- Confirm the enforcer has learned every IP-SGT binding.
- Build the same binding table in the Track 2 model.

## Two ways to assign a tag

An endpoint gets its SGT in one of three ways: **dynamically** (802.1X/MAB authorization returns an SGT), **statically by IP** (an IP-SGT mapping), or **statically on the port** (`cts manual`). This lab uses **static IP-SGT mappings** — the simplest reproducible method and the one that maps cleanly onto the Track 2 model. The bindings are authored centrally in ISE and pushed to enforcers with **SXP (SGT Exchange Protocol)**, which exists precisely so a device that cannot tag inline can still learn "IP 10.10.1.20 is DB."

## Hands-On Lab

### Exercise 4.1 — Author the IP-SGT bindings

**Objective.** Map each endpoint IP to its SGT.

**Track 1 — Walkthrough.** In ISE, **Work Centers → TrustSec → Components → IP SGT Static Mapping → Add** one row per endpoint:

```text
10.10.1.10  ->  WEB (10)
10.10.1.20  ->  DB  (20)
10.10.1.30  ->  HMI (30)
10.10.1.40  ->  PLC (40)
```

**Expected result.** Four static mappings listed, each tying an address to a group.

**Negative test.** Two mappings for the same IP with different SGTs is rejected — an endpoint has exactly one group at a time; overlapping identity is not allowed.

**Track 2 — Walkthrough.** Record the same bindings as the enforcer's SXP-equivalent table:

```bash
sudo tee /etc/cts/ip-sgt > /dev/null <<'EOF'
10.10.1.10 10
10.10.1.20 20
10.10.1.30 30
10.10.1.40 40
EOF
cat /etc/cts/ip-sgt
```

**Expected result.** Four IP→SGT rows — the local binding table SXP would otherwise distribute.

**Cleanup.** Keep the bindings.

### Exercise 4.2 — Distribute bindings with SXP

**Objective.** Get the bindings from ISE onto the enforcer.

**Track 1 — Walkthrough.** Enable SXP on ISE (as a speaker) and on the NAD (as a listener). On the NAD:

```text
nad(config)# cts sxp enable
nad(config)# cts sxp default password <sxp-password>
nad(config)# cts sxp default source-ip 10.10.0.2
nad(config)# cts sxp connection peer 10.10.0.10 password default mode local listener
```

In ISE, **Work Centers → TrustSec → SXP → SXP Devices** add the NAD as a peer (speaker side). Then verify the connection and the learned bindings:

```bash
show cts sxp connections brief
# Peer_IP 10.10.0.10  Source_IP 10.10.0.2  Conn Status On  Duration ...
show cts role-based sgt-map all
# IP            SGT   Source
# 10.10.1.10    10    SXP
# 10.10.1.20    20    SXP
# 10.10.1.30    30    SXP
# 10.10.1.40    40    SXP
```

**Expected result.** SXP `Conn Status On` and `show cts role-based sgt-map all` lists all four bindings with `Source SXP` — the enforcer now knows every endpoint's group.

**Negative test.** With `mode local listener` on both ends (no speaker), the connection stays `Off`/`Pending` — SXP is directional; one side speaks, the other listens.

**Track 2 — Walkthrough.** Load the binding table into an nftables map keyed by IP so the enforcer can look up a source or destination SGT:

```bash
sudo nft add map inet cts ip2sgt '{ type ipv4_addr : verdict ; }' 2>/dev/null
# Build a named set per SGT for matching (verdict maps come later); first, prove the lookup table:
sudo nft add map inet cts sgtmap '{ type ipv4_addr : mark ; }'
while read ip sgt; do sudo nft add element inet cts sgtmap "{ $ip : $sgt }"; done < /etc/cts/ip-sgt
sudo nft list map inet cts sgtmap
```

**Expected result.** The `sgtmap` lists each IP with its SGT as a packet mark — the enforcer can now resolve any address to a tag, exactly as `show cts role-based sgt-map` does.

**Cleanup.** Keep the map; Chapter 06 uses it to enforce.

### Exercise 4.3 — Confirm tags end to end

**Objective.** Verify a given endpoint resolves to the intended SGT on the enforcer.

**Track 1 — Walkthrough.**

```bash
show cts role-based sgt-map 10.10.1.30
# Active IPv4-SGT Bindings Information
# IP Address   SGT   Source
# 10.10.1.30    30    SXP
```

**Expected result.** `10.10.1.30` resolves to SGT 30 (HMI).

**Track 2 — Walkthrough.**

```bash
sudo nft get element inet cts sgtmap '{ 10.10.1.30 }'
# element ... { 10.10.1.30 : 0x0000001e }   (30)
```

**Expected result.** `10.10.1.30` maps to `0x1e` = 30 (HMI).

**Negative test.** Query an unbound IP:

```bash
sudo nft get element inet cts sgtmap '{ 10.10.1.99 }' 2>&1 | grep -o "No such file or directory" && echo "UNKNOWN (SGT 0)"
```

An unbound address has no tag — it is `Unknown (0)`, the group the default rule will handle.

**Cleanup.** Bindings persist. Teardown is Chapter 09.

## Summary and Completion Checklist

- [ ] Four IP-SGT bindings authored in ISE (and the Track 2 table).
- [ ] SXP connection up; enforcer shows all bindings with source SXP.
- [ ] Each endpoint resolves to its intended SGT.
- [ ] Unbound addresses correctly resolve to Unknown (0).
