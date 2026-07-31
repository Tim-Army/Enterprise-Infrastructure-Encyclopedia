# Chapter 03: Objects and Policy Install

## Learning Objectives

- Create host objects and service objects with the management API.
- Build a policy package with a single Cleanup rule and install it.
- Confirm the gateway is enforcing the installed policy.
- Model the objects and install step in Track 2.

## Objects first, then a policy you install

Check Point separates *defining* policy (on management) from *enforcing* it (on the gateway). Nothing takes effect until you **install policy**. This chapter creates the objects and installs a minimal policy — a single Cleanup rule that drops everything — so the estate starts default-deny, the opposite end from the flat network you will briefly create in Chapter 04.

## Hands-On Lab

### Exercise 3.1 — Create host and service objects

**Objective.** Name the four endpoints and the two services.

**Track 1 — Walkthrough.** Using `mgmt_cli` (or SmartConsole), create the objects and publish:

```text
mgmt> mgmt_cli add host name web ip-address 10.40.1.10 --session-id "$SID"
mgmt> mgmt_cli add host name db  ip-address 10.40.2.10 --session-id "$SID"
mgmt> mgmt_cli add host name hmi ip-address 10.40.3.10 --session-id "$SID"
mgmt> mgmt_cli add host name plc ip-address 10.40.4.10 --session-id "$SID"
mgmt> mgmt_cli add service-tcp name PGSQL port 5432 --session-id "$SID"
mgmt> mgmt_cli add service-tcp name MODBUS port 502 --session-id "$SID"
mgmt> mgmt_cli publish --session-id "$SID"
```

**Expected result.**

```text
mgmt> mgmt_cli show hosts --session-id "$SID" | grep name
    name: web
    name: db
    name: hmi
    name: plc
```

**Negative test.** A rule that references an object name that was never published fails to install — objects must be published before policy can use them, so unpublished typos are caught at install.

**Track 2 — Walkthrough.**

```bash
sudo mkdir -p /etc/cpg
sudo tee /etc/cpg/objects > /dev/null <<'EOF'
web 10.40.1.10
db  10.40.2.10
hmi 10.40.3.10
plc 10.40.4.10
EOF
sudo nft add table inet cpg
cat /etc/cpg/objects
```

**Expected result.** Four named objects; the `cpg` table exists for the rulebase.

**Cleanup.** Keep the objects.

### Exercise 3.2 — Install a Cleanup-only policy

**Objective.** Start default-deny with a single explicit drop, installed to the gateway.

**Track 1 — Walkthrough.** Add an access layer with only a Cleanup rule (drop, log) and install policy to `gw`:

```text
mgmt> mgmt_cli add access-rule layer "Network" position bottom name "Cleanup rule" \
        action Drop track Log --session-id "$SID"
mgmt> mgmt_cli publish --session-id "$SID"
mgmt> mgmt_cli install-policy policy-package "Standard" access true targets gw --session-id "$SID"
```

**Expected result.**

```text
mgmt> mgmt_cli show access-rulebase name "Network" --session-id "$SID" | grep -E "name|action"
    name: "Cleanup rule"  action: Drop
gw> fw stat
    HOST   POLICY   DATE
    gw     Standard <now>   (policy installed)
```

The gateway is enforcing a drop-everything policy — default-deny, logged.

**Negative test.** With SIC not established (Chapter 02), `install-policy` fails with an authentication/trust error — install requires the trust you built earlier.

**Track 2 — Walkthrough.**

```bash
sudo nft add chain inet cpg forward '{ type filter hook forward priority 0 ; policy drop ; }'
sudo nft add rule inet cpg forward ip saddr 10.40.0.0/16 ip daddr 10.40.0.0/16 log prefix '"CPG-CLEANUP " ' drop
sudo nft list chain inet cpg forward
```

**Expected result.** A default-drop forward chain with a logged cleanup rule — the Track 2 default-deny policy.

**Cleanup.** Keep the policy; Chapter 04 briefly opens it, Chapter 05 tightens it.

## Summary and Completion Checklist

- [ ] Host objects web/db/hmi/plc and services PGSQL/MODBUS created and published.
- [ ] A Cleanup-only policy installed to the gateway (default-deny, logged).
- [ ] Install confirmed with `fw stat` / policy status.
- [ ] Track 2 default-drop chain mirrors the installed policy.
