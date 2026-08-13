# Chapter 05: The Segmentation Rulebase

## Learning Objectives

- Replace the any-any accept with least-privilege access rules.
- Permit only web→db (PGSQL) and hmi→plc (MODBUS); rely on the Cleanup rule for everything else.
- Install the policy and confirm the ordering.
- Build the equivalent ordered ruleset in Track 2.

## An ordered rulebase with a Cleanup drop

Check Point evaluates the access rulebase **top to bottom**; the first matching rule wins, and the final **Cleanup rule** drops anything unmatched. Microsegmentation is: author the exact permits above the Cleanup rule, remove the any-any accept, and install. The Cleanup rule makes default-deny explicit and logged.

## Hands-On Lab

### Exercise 5.1 — Author the two permit rules

**Objective.** Add narrow permits for web→db and hmi→plc above the Cleanup rule.

**Track 1 — Walkthrough.**

```text
mgmt> mgmt_cli add access-rule layer "Network" position 1 name "web-to-db" \
        source web destination db service PGSQL action Accept track Log --session-id "$SID"
mgmt> mgmt_cli add access-rule layer "Network" position 2 name "hmi-to-plc" \
        source hmi destination plc service MODBUS action Accept track Log --session-id "$SID"
mgmt> mgmt_cli publish --session-id "$SID"
```

**Expected result.**

```text
mgmt> mgmt_cli show access-rulebase name "Network" --session-id "$SID" | grep -E "name|action"
    name: "web-to-db"    action: Accept
    name: "hmi-to-plc"   action: Accept
    name: "allow-all"    action: Accept     <-- still present, removed next
    name: "Cleanup rule" action: Drop
```

**Negative test.** Using service `Any` instead of `PGSQL` would permit every port from web to db — scope the service. Source object + destination object + service is what makes this microsegmentation.

**Track 2 — Walkthrough.**

```bash
sudo nft flush chain inet cpg forward
sudo nft add rule inet cpg forward ip saddr 10.40.1.10 ip daddr 10.40.2.10 tcp dport 5432 accept
sudo nft add rule inet cpg forward ip saddr 10.40.3.10 ip daddr 10.40.4.10 tcp dport 502 accept
```

**Expected result.** Two accept rules — the exact legitimate flows.

**Rollback.** Keep the permits.

### Exercise 5.2 — Remove the any-any accept and install

**Objective.** Delete the flat rule so the Cleanup rule governs everything else, including hmi→db.

**Track 1 — Walkthrough.**

```text
mgmt> mgmt_cli delete access-rule name "allow-all" layer "Network" --session-id "$SID"
mgmt> mgmt_cli publish --session-id "$SID"
mgmt> mgmt_cli install-policy policy-package "Standard" access true targets gw --session-id "$SID"
```

**Expected result.**

```text
mgmt> mgmt_cli show access-rulebase name "Network" --session-id "$SID" | grep name
    name: "web-to-db"
    name: "hmi-to-plc"
    name: "Cleanup rule"
# hmi->db now falls through to the Cleanup drop
```

**Negative test.** Leaving `allow-all` in place keeps permitting hmi→db regardless of the specific rules — a broad accept above the specifics defeats least privilege. It must be removed and the policy re-installed; editing without installing changes nothing on the gateway.

**Track 2 — Walkthrough.**

```bash
sudo nft add rule inet cpg forward ip saddr 10.40.3.10 ip daddr 10.40.2.10 log prefix '"CPG-DENY " ' drop
sudo nft add rule inet cpg forward ip saddr 10.40.0.0/16 ip daddr 10.40.0.0/16 log prefix '"CPG-CLEANUP " ' drop
sudo nft list chain inet cpg forward
```

**Expected result.** The chain permits the two flows and logs-and-drops the lateral flow and all other east-west traffic.

**Rollback.** Keep the ruleset; Chapter 06 converts it to tag-based objects.

## Summary and Completion Checklist

- [ ] web→db (PGSQL) and hmi→plc (MODBUS) permitted with scoped services.
- [ ] any-any accept removed; Cleanup rule governs the rest.
- [ ] Policy installed (edits take effect only on install).
- [ ] Track 2 ordered ruleset matches the rulebase.
