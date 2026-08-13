# Chapter 08: Dynamic Membership, Scale, and the Boundary

## Learning Objectives

- Onboard a new workload by tag alone — no rule edit.
- Understand how DFW scales across hosts and how it integrates identity and context.
- Recognize what even a distributed firewall cannot segment, and pair it with a complementary control.

## Hands-On Lab

### Exercise 8.1 — Onboard a new workload by tag

**Objective.** Add a second web server and have it gain access automatically.

**Track 1 — Walkthrough.** Deploy a new VM, tag it `role=web`; it joins the `Web` group and the `web-to-db` rule covers it instantly — no rule edit, no re-publish of the rule itself:

```text
nsx> tag new-web -> role=web
# new-web immediately can reach Database:5432; membership did the work
```

**Expected result.** The new server reaches db:5432 the moment it is tagged; removing the tag removes the access. Onboarding is a tagging action.

**Track 2 — Walkthrough.**

```bash
# a new web instance appears and is tagged
echo "10.50.1.11 role=web" | sudo tee -a /etc/nsx/tags >/dev/null
sudo ip netns exec db nft add element inet vnic g_web '{ 10.50.1.11 }'
sudo ip netns exec db nft get element inet vnic g_web '{ 10.50.1.11 }'
```

**Expected result.** 10.50.1.11 is now in db's `g_web` set and may reach 5432 — the rule is unchanged; only membership grew.

**Negative test.** Assume onboarding a server requires editing the firewall. It does not — that is the entire value of tag-driven groups: scale without touching rules.

**Rollback.** Remove the test element and tag line.

### Exercise 8.2 — Scale and context (design)

**Objective.** Understand DFW at estate scale and its richer match criteria.

**Design walkthrough.** The same policy is enforced on **every prepared host**, so a VM keeps its rules when it vMotions to another host — enforcement travels with the workload. Beyond tags, NSX groups can match VM name, OS, or **Identity Firewall** (AD user/group), and **context profiles** add Layer 7 App-ID and FQDN matching, so a rule can say "Web may reach Database, PostgreSQL protocol only" at L7. Central management (NSX policy, or vRealize/Aria automation) authors once and enforces estate-wide.

**Expected result (on paper).** A design note: tags for what, Identity Firewall for who, context profiles for L7 — all enforced distributed at every vNIC and following the VM across hosts.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Exercise 8.3 — The boundary

**Objective.** Identify traffic even DFW cannot segment, and cover it.

**Track 1 & 2 — Walkthrough.** DFW enforces at the vNIC of **managed, NSX-attached VMs**. It does not by itself cover:

- **Physical/bare-metal servers and appliances** with no NSX vNIC — reach these with NSX Gateway Firewall, a physical firewall, or host agents.
- **Containers** unless NSX is integrated with the container platform (Antrea/NCP).
- **Unmanaged hypervisors** or VMs on non-prepared hosts.

```bash
# a bare-metal peer with no vNIC DFW is outside distributed enforcement
echo "10.50.1.200 (physical, no DFW)  -> must be covered by a gateway or host agent"
```

**Expected result.** A boundary note: DFW is the strongest east-west control for NSX-managed VMs; pair it with NSX Gateway Firewall for north-south and physical, container integration for pods, and host-based microsegmentation (Volumes XCIII–CVI) for anything off the managed fabric.

**Negative test.** Assume DFW covers every workload in the data center. It covers NSX-attached VMs; a physical database with no vNIC is not enforced by DFW and needs a complementary control.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] A new workload onboarded by tag alone.
- [ ] DFW scale, vMotion-follows-workload, Identity Firewall, and L7 context understood.
- [ ] The un-managed / physical boundary recognized and paired with a control.
