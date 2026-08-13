# Chapter 06: The IdentityGraph and Policy Groups

## Learning Objectives

- Explain how Elisity classifies every asset in an IdentityGraph from existing sources.
- Build an IdentityGraph by hand and derive identity-based policy groups from it.
- Author identity-based policy and validate it before enforcing.

This is the core of the lab. Each exercise carries both tracks. Elisity's method is **classify by identity, then enforce on the network**: ingest context from sources you already run, place every user/device/workload in the IdentityGraph, group by identity and attributes, and enforce the resulting policy on the access switch — here, on `el-gw`.

## Hands-On Lab

### Lab 6.1 — Identity sources and the IdentityGraph

**Objective.** State where Elisity's classification comes from and what the IdentityGraph is.

**Background.** Elisity does not ask you to label assets by hand or by IP. It **ingests** from sources you already operate — Active Directory / Entra ID (users and groups), vCenter (VM attributes), ServiceNow / a CMDB (ownership, function), Infoblox (IPAM), and EDR (device posture) — and fuses them into the **IdentityGraph**: a continuously-updated classification of every user, device, and workload by *identity and attributes*, independent of IP address. Policy is then written against those classifications.

**Walkthrough.**

**Step 1.** Identify which real source would classify each lab asset, and the native stand-in you will use:

| Asset | Real Elisity source | Native stand-in (Track 2) |
|:---|:---|:---|
| el-app01 | vCenter tag / CMDB function | inventory CSV row |
| el-db01 | CMDB function = database | inventory CSV row |
| el-win01 | AD computer + CMDB = HMI | inventory CSV row |
| el-ot01 | Profiling + CMDB = PLC | inventory CSV row (no agent needed) |

**Step 2.** Note the crucial property: even `el-ot01`, which runs no agent, is classified — Elisity profiles it from network behavior and context, so the agentless PLC is a first-class identity in the graph.

**Expected result.** A source-to-asset map, and the understanding that classification is *ingested*, not hand-assigned per IP.

**Negative test.** Plan to classify assets by subnet ("everything on 10.10.40.0/24 is a database"). Subnet is not identity; the day a database moves or a non-database lands on that subnet, the policy is wrong. Classify by identity.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.2 — Build the IdentityGraph

**Objective.** Construct the IdentityGraph by hand from a CMDB-style source, so every asset carries an identity and attributes.

**Track 1 — Real Elisity.** In Elisity Cloud, connect the identity sources (Entra ID, vCenter, ServiceNow, Infoblox) and confirm the IdentityGraph populates with each asset's classification and attributes, refreshed continuously.

**Track 2 — Native equivalent.** On `el-gw`, create the CMDB source and a builder that fuses it into a graph of *group → current members*.

**Step 1.** Create the inventory (the CMDB source of truth for identity):

```bash
sudo mkdir -p /etc/elisity
sudo tee /etc/elisity/inventory.csv > /dev/null <<'EOF'
hostname,ip,role,type,owner
el-app01,10.10.20.11,AppServer,linux,app-team
el-db01,10.10.40.40,Database,linux,dba-team
el-win01,10.10.20.21,HMI,windows,ot-team
el-ot01,10.10.30.50,PLC,ot-device,ot-team
EOF
```

**Step 2.** Build the IdentityGraph: derive, per identity group, the set of current member addresses. This is the fusion step Elisity Cloud performs continuously:

```bash
sudo tee /usr/local/bin/build-identitygraph.sh > /dev/null <<'EOF'
#!/usr/bin/env bash
# Fuse the inventory into nftables sets named by identity group (role).
set -euo pipefail
nft list table inet elisity >/dev/null 2>&1 || nft add table inet elisity
for grp in AppServer Database HMI PLC; do
  set="grp_$(echo "$grp" | tr 'A-Z' 'a-z')"
  nft add set inet elisity "$set" '{ type ipv4_addr; }' 2>/dev/null || true
  nft flush set inet elisity "$set"
  awk -F, -v g="$grp" 'NR>1 && $3==g { print $2 }' /etc/elisity/inventory.csv | while read -r ip; do
    nft add element inet elisity "$set" "{ $ip }"
  done
done
echo "IdentityGraph built:"; nft list table inet elisity | grep -A1 'set grp_'
EOF
sudo chmod +x /usr/local/bin/build-identitygraph.sh
sudo /usr/local/bin/build-identitygraph.sh
```

**Expected result.** Four identity groups (`grp_appserver`, `grp_database`, `grp_hmi`, `grp_plc`), each populated with the current members from the source — the native IdentityGraph.

**Negative test.** Add a second app server to the inventory and re-run the builder; it joins `grp_appserver` automatically. Now change `el-win01`'s role to `AppServer` in the CSV and rebuild — the HMI becomes an app server in the graph, and (in Chapter 07) inherits app-server access to the database. The graph is only as correct as its sources; a wrong classification is a wrong policy. Restore it to `HMI`.

**Rollback.** Keep the IdentityGraph; Chapter 07 enforces policy against it.

### Lab 6.3 — Author identity-based policy (validate before enforcing)

**Objective.** Express the two legitimate flows as identity-to-identity policy, and confirm what it would deny before enforcing.

**Track 1 — Real Elisity.** Create **policy groups** matching the IdentityGraph classifications and author policy: *AppServer → Database on 5432 (allow)* and *HMI → PLC on 502 (allow)*, default-deny otherwise. Simulate/monitor first; confirm the HMI→Database flow shows as would-deny.

**Track 2 — Native equivalent.** Write the policy on `el-gw`'s forward path, but keep it observing (log-and-accept) so you can validate before it blocks:

```bash
sudo nft add chain inet elisity forward '{ type filter hook forward priority 0 ; policy accept ; }'
sudo nft add rule inet elisity forward ct state established,related accept
# identity-based allows (reference the IdentityGraph groups):
sudo nft add rule inet elisity forward ip saddr @grp_appserver ip daddr @grp_database tcp dport 5432 accept
sudo nft add rule inet elisity forward ip saddr @grp_hmi ip daddr @grp_plc tcp dport 502 accept
# would-deny logging for cross-segment traffic to the protected assets:
sudo nft add rule inet elisity forward ip daddr @grp_database tcp dport 5432 \
    log prefix "ELISITY-WOULD-DENY db: " level warn
sudo nft add rule inet elisity forward ip daddr @grp_plc tcp dport 502 \
    log prefix "ELISITY-WOULD-DENY plc: " level warn
```

Reproduce the HMI→db attempt from `el-win01` and confirm an `ELISITY-WOULD-DENY db:` line appears while the app's own query raises none.

**Expected result.** Identity-based policy authored and validated in observation: AppServer→Database and HMI→PLC permitted; HMI→Database flagged.

**Negative test.** Write the allow as `ip saddr 10.10.20.11` instead of `@grp_appserver`. It works until the app is re-addressed, then breaks — the exact fragility identity groups remove. Use the group.

**Rollback.** Keep the policy; Chapter 07 enforces it.

## Summary and Completion Checklist

- [ ] Identity sources and the IdentityGraph concept understood, including classification of the agentless PLC.
- [ ] A native IdentityGraph built from a CMDB source into identity groups.
- [ ] Identity-based policy authored and validated in observation before enforcing.
