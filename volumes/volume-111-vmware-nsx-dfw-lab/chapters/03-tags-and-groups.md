# Chapter 03: Security Tags and Groups

## Learning Objectives

- Apply a security tag to each VM.
- Create NSX groups whose membership is driven dynamically by tag.
- Confirm the groups resolve to the right VMs.
- Model tags and dynamic groups in Track 2.

## Tags first, then dynamic groups

NSX policy is written against **groups**, not VMs, and the best groups compute their membership from **security tags**. Tag a VM `role=db` and it joins the `Database` group automatically; untag it and it leaves. This chapter tags the four VMs and builds the four groups the DFW rules will reference — so the rules never mention an IP or a VM name.

## Hands-On Lab

### Exercise 3.1 — Apply security tags

**Objective.** Tag each VM with its role.

**Track 1 — Walkthrough.** In the NSX UI (Inventory > Tags) or via the Policy API, tag each VM:

```text
nsx> PATCH /policy/api/v1/infra/realized-state/... (or Inventory > Virtual Machines > Actions > Add Tag)
     web -> tag scope=role tag=web
     db  -> tag scope=role tag=db
     hmi -> tag scope=role tag=hmi
     plc -> tag scope=role tag=plc
```

**Expected result.** Each VM shows its `role` tag in the inventory.

**Negative test.** An untagged VM matches no role-based group and therefore no permit rule — with a zero-trust default it is fully isolated. Tagging is what grants a workload its place in the policy.

**Track 2 — Walkthrough.** Record the tags the local rulesets will consult:

```bash
sudo mkdir -p /etc/nsx
sudo tee /etc/nsx/tags > /dev/null <<'EOF'
10.50.1.10 role=web
10.50.1.20 role=db
10.50.1.30 role=hmi
10.50.1.40 role=plc
EOF
cat /etc/nsx/tags
```

**Expected result.** Four IP→tag rows — the Track 2 tag inventory.

**Rollback.** Keep the tags.

### Exercise 3.2 — Create dynamic groups

**Objective.** Define groups that resolve members by tag.

**Track 1 — Walkthrough.** Create four groups, each with a membership criterion "Tag equals role/<value>":

```text
nsx> PUT /policy/api/v1/infra/domains/default/groups/Web
       expression: Condition member_type=VirtualMachine key=Tag operator=EQUALS value="role|web"
nsx> ... /groups/Database  value="role|db"
nsx> ... /groups/Operators value="role|hmi"
nsx> ... /groups/OT        value="role|plc"
```

**Expected result.**

```text
nsx> GET /policy/api/v1/infra/domains/default/groups/Database/members/virtual-machines
     [ db ]      # membership resolved from the tag
```

The `Database` group contains the db VM because it carries `role=db` — no static assignment.

**Negative test.** Move the `role=db` tag to another VM and watch the `Database` group membership follow it — proof membership is computed, not fixed. Restore the tag.

**Track 2 — Walkthrough.** Model each group as an nftables set resolved from the tag file:

```bash
sudo nft add table inet nsx
role_ips() { awk -v t="role=$1" '$2==t{print $1}' /etc/nsx/tags; }
sudo nft add set inet nsx g_web '{ type ipv4_addr ; }'; sudo nft add element inet nsx g_web "{ $(role_ips web) }"
sudo nft add set inet nsx g_db  '{ type ipv4_addr ; }'; sudo nft add element inet nsx g_db  "{ $(role_ips db) }"
sudo nft add set inet nsx g_hmi '{ type ipv4_addr ; }'; sudo nft add element inet nsx g_hmi "{ $(role_ips hmi) }"
sudo nft add set inet nsx g_plc '{ type ipv4_addr ; }'; sudo nft add element inet nsx g_plc "{ $(role_ips plc) }"
sudo nft list set inet nsx g_db
```

**Expected result.** `g_db` contains 10.50.1.20 — the group resolved from the tag inventory.

**Rollback.** Keep the groups.

## Summary and Completion Checklist

- [ ] Each VM tagged with its role.
- [ ] Four dynamic groups (Web/Database/Operators/OT) resolving by tag.
- [ ] Group membership confirmed to follow the tag, not a static list.
- [ ] Track 2 tag inventory and group sets mirror NSX.
