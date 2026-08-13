# Chapter 03: Enabling TrustSec

## Learning Objectives

- Register the enforcement device with ISE and establish the CTS/RADIUS trust.
- Define the four Security Groups (SGTs) in ISE.
- Turn on `cts role-based enforcement` on the IOS-XE device.
- Build the equivalent IP-SGT binding table in the Track 2 model.

## Hands-On Lab

### Exercise 3.1 — Define the Security Groups in ISE

**Objective.** Create the SGTs `WEB`, `DB`, `HMI`, `PLC` with the planned values.

**Track 1 — Walkthrough.** In ISE go to **Work Centers → TrustSec → Components → Security Groups** and add each group. The value is the tag number carried on the wire:

```text
Work Centers > TrustSec > Components > Security Groups > Add
  Name: WEB   Value: 10
  Name: DB    Value: 20
  Name: HMI   Value: 30
  Name: PLC   Value: 40
```

**Expected result.** The Security Groups list shows WEB/DB/HMI/PLC alongside the built-in `Unknown (0)` and `TrustSec_Devices (2)`.

**Negative test.** ISE refuses a duplicate value — two groups cannot share tag 10; the tag is the identity, so it must be unique.

**Track 2 — Walkthrough.** Record the same group catalogue as a file the enforcer reads:

```bash
sudo mkdir -p /etc/cts
sudo tee /etc/cts/sgt-names > /dev/null <<'EOF'
10 WEB
20 DB
30 HMI
40 PLC
0  Unknown
EOF
cat /etc/cts/sgt-names
```

**Expected result.** The five names map to their values — the local equivalent of ISE's Security Groups list.

**Rollback.** Keep the definitions.

### Exercise 3.2 — Register the enforcer as a Network Device

**Objective.** Give ISE and the IOS-XE device a shared RADIUS/CTS trust so SGACLs can be downloaded.

**Track 1 — Walkthrough.** In ISE, **Administration → Network Resources → Network Devices → Add**: name `nad`, IP `10.10.0.2`, enable **RADIUS** with a shared secret, and enable **Advanced TrustSec Settings** with a device ID and password. Then on the NAD:

```text
nad(config)# radius server ISE
nad(config-radius-server)#  address ipv4 10.10.0.10 auth-port 1812 acct-port 1813
nad(config-radius-server)#  pac key <shared-secret>
nad(config)# aaa authentication dot1x default group radius
nad(config)# aaa authorization network default group radius
nad(config)# cts credentials id nad password <cts-password>
```

Provision the PAC and confirm the environment data (SGT names/numbers) downloads from ISE:

```bash
show cts environment-data
# CTS Environment Data
# Current state = COMPLETE
# Security Group Name Table: 0-Unknown 10-WEB 20-DB 30-HMI 40-PLC
```

**Expected result.** `Current state = COMPLETE` and the Security Group Name Table lists your SGTs — the NAD has learned the group catalogue from ISE.

**Negative test.** A mismatched `cts credentials` password leaves the environment data in `state = INCOMPLETE`; the NAD never learns the groups, so no SGACL will download later. The trust is the foundation.

**Track 2 — Walkthrough.** The "trust" in the native model is simply that the enforcer host owns the binding table and ruleset; no registration is needed. Confirm the enforcer is ready:

```bash
sudo nft list ruleset | head -1 || echo "nftables ready (empty)"
```

**Rollback.** Keep the registration.

### Exercise 3.3 — Turn on role-based enforcement

**Objective.** Arm the enforcer so that, once SGACLs exist, they are applied.

**Track 1 — Walkthrough.**

```text
nad(config)# cts role-based enforcement
nad(config)# cts role-based enforcement vlan-list 1-4094
```

**Expected result.**

```bash
show cts role-based permissions
# IPv4 Role-based permissions default: Permit IP-00
# (no per-cell SGACLs yet — everything still permitted)
```

Enforcement is on but the matrix is empty, so traffic is still permitted — exactly the flat state Chapter 05 exploits.

**Negative test.** Without `cts role-based enforcement`, SGACLs download but are never applied; `show cts role-based counters` stays empty forever. Enforcement is a separate switch from policy.

**Track 2 — Walkthrough.** Create the nftables scaffold with a default-permit so the model starts flat like the NAD:

```bash
sudo nft add table inet cts
sudo nft add chain inet cts forward '{ type filter hook forward priority 0 ; policy accept ; }'
sudo nft list table inet cts
```

**Expected result.** A `forward` chain with `policy accept` — enforcement armed, matrix empty, traffic still permitted.

**Rollback.** Keep the scaffold; Chapter 05 proves the flat network, Chapter 06 fills the matrix.

## Summary and Completion Checklist

- [ ] SGTs WEB/DB/HMI/PLC defined in ISE (and in the Track 2 names file).
- [ ] Enforcer registered; environment data `COMPLETE`.
- [ ] `cts role-based enforcement` on (Track 2: forward chain armed).
- [ ] Matrix still empty — traffic permitted for now.
