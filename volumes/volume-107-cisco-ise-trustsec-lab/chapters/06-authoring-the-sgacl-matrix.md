# Chapter 06: Authoring the SGACL Matrix

## Learning Objectives

- Write SGACLs that permit only the two legitimate flows.
- Place them in the egress policy matrix at the correct source/destination cells.
- Set the matrix default to deny so unlisted flows fail closed.
- Build the equivalent tag-to-tag ruleset in the Track 2 model.

## The matrix is the policy

An SGACL is an access list keyed on *(source SGT → destination SGT)*. The **egress policy matrix** is the grid of those cells: the row is the source group, the column is the destination group, and the cell holds the SGACL applied when a packet from the row-group is destined for the column-group. Fill only the cells you must permit and set the default cell to **Deny IP** — the fabric then fails closed, which is the posture microsegmentation exists to achieve.

The target matrix for this estate:

| src ↓ \ dst → | WEB (10) | DB (20) | HMI (30) | PLC (40) |
|:---|:---|:---|:---|:---|
| **WEB (10)** | — | **Permit 5432** | Deny | Deny |
| **DB (20)** | Deny | — | Deny | Deny |
| **HMI (30)** | Deny | **Deny** | — | **Permit 502** |
| **PLC (40)** | Deny | Deny | Deny | — |
| default | Deny IP | Deny IP | Deny IP | Deny IP |

The two bold permits are the legitimate flows; the bold `HMI→DB Deny` is the lateral movement.

## Hands-On Lab

### Exercise 6.1 — Create the SGACLs

**Objective.** Define the two permit SGACLs.

**Track 1 — Walkthrough.** In ISE, **Work Centers → TrustSec → Components → Security Group ACLs → Add**:

```text
Name: WEB-to-DB
  permit tcp dst eq 5432
  deny ip

Name: HMI-to-PLC
  permit tcp dst eq 502
  deny ip
```

**Expected result.** Two SGACLs listed, each a short permit-then-deny content block.

**Negative test.** An SGACL that ends with `permit ip` (no trailing deny) leaks everything after its specific line — always end a microsegmentation SGACL with `deny ip` so only the named ports pass.

**Track 2 — Walkthrough.** Represent each SGACL as an nftables rule fragment matched later by tag:

```bash
# these are the "contents"; the matrix (Ex 6.2) binds them to src/dst tag pairs
echo 'WEB-to-DB : tcp dport 5432 accept ; drop'
echo 'HMI-to-PLC: tcp dport 502  accept ; drop'
```

**Expected result.** Two named intents that Exercise 6.2 wires into the tag matrix.

**Rollback.** Keep the SGACLs.

### Exercise 6.2 — Place them in the matrix and set default deny

**Objective.** Bind each SGACL to its cell and make unlisted cells deny.

**Track 1 — Walkthrough.** In **Work Centers → TrustSec → Policy → Egress Policy → Matrix**, click the cell and assign the SGACL:

```text
Cell WEB(10) -> DB(20)  : SGACL = WEB-to-DB   , Final = Deny IP
Cell HMI(30) -> PLC(40) : SGACL = HMI-to-PLC  , Final = Deny IP
Matrix > Default cell   : Deny IP
```

Push the matrix to enforcers (**Deploy**), then verify locally:

```bash
show cts role-based permissions
# IPv4 Role-based permissions default: Deny IP-00
# SGT 10 -> SGT 20: WEB-to-DB-10
# SGT 30 -> SGT 40: HMI-to-PLC-10
```

**Expected result.** The default is now `Deny IP`, and only the two cells carry a permit SGACL. Everything else — including `HMI(30) → DB(20)` — falls through to the default deny.

**Negative test.** Leave the matrix default at `Permit IP` and note that the lateral flow would still pass despite the specific permits — the **default cell** is what makes the fabric fail closed. A permit-default matrix is an allow-list with a hole.

**Track 2 — Walkthrough.** Implement the matrix as nftables rules that read the source and destination SGT from the binding map and apply the tag-pair verdict, with a default drop:

```bash
# resolve src/dst SGT into marks, then match tag pairs
sudo nft flush chain inet cts forward
sudo nft add rule inet cts forward ip saddr . ip daddr vmap { } 2>/dev/null || true

# WEB(10) -> DB(20) : permit 5432
sudo nft add rule inet cts forward ip saddr 10.10.1.10 ip daddr 10.10.1.20 tcp dport 5432 accept
# HMI(30) -> PLC(40): permit 502
sudo nft add rule inet cts forward ip saddr 10.10.1.30 ip daddr 10.10.1.40 tcp dport 502 accept
# default: deny east-west within the fabric
sudo nft add rule inet cts forward ip saddr 10.10.1.0/24 ip daddr 10.10.1.0/24 drop
sudo nft chain inet cts forward '{ policy accept ; }'
sudo nft list chain inet cts forward
```

**Expected result.** The forward chain permits exactly the two flows and drops all other intra-fabric traffic — the Track 2 default-deny matrix.

**Rollback.** Keep the ruleset; Chapter 07 verifies enforcement, Chapter 09 tears it down.

## Summary and Completion Checklist

- [ ] Two SGACLs (WEB-to-DB, HMI-to-PLC) authored, each ending in deny.
- [ ] Matrix cells populated; default set to Deny IP.
- [ ] Track 2 forward chain implements the same tag-pair matrix with default drop.
- [ ] Matrix deployed to the enforcer (enforcement proven next chapter).
