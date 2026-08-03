# Chapter 04: Categories and Monitor Mode

## Learning Objectives

- Create categories and assign the four VMs — the policy language of Flow.
- Save the security policy in **monitor mode**: visualize every flow without dropping anything.
- Read the monitor telemetry and identify the lateral flow before enforcing.

## Hands-On Lab

### Exercise 4.1 — Create categories and categorize the VMs

**Objective.** Label every VM; policy will name labels, never addresses.

**Track 1 — Walkthrough.** In Prism Central, create category keys and values, then assign them to VMs:

```text
pc> Administration > Categories > add key AppTier (values: web, db, hmi, plc)
pc> Administration > Categories > add key Environment (values: corp, ot)
pc> Compute > VMs > (each VM) > Manage Categories > assign
```

**Track 2 — Walkthrough.** Categories are **named sets** in the host's `bridge` table; assigning a category is adding the VM's address as an element:

```bash
sudo nft add table bridge flow
for s in apptier_web apptier_db apptier_hmi apptier_plc env_corp env_ot quarantine; do
  sudo nft add set bridge flow $s '{ type ipv4_addr; }'
done
sudo nft add element bridge flow apptier_web '{ 10.150.0.10 }'
sudo nft add element bridge flow apptier_db  '{ 10.150.0.20 }'
sudo nft add element bridge flow apptier_hmi '{ 10.150.0.30 }'
sudo nft add element bridge flow apptier_plc '{ 10.150.0.40 }'
sudo nft add element bridge flow env_corp '{ 10.150.0.10, 10.150.0.20 }'
sudo nft add element bridge flow env_ot   '{ 10.150.0.30, 10.150.0.40 }'
```

**Expected result.**

```bash
sudo nft list set bridge flow apptier_web | grep -o "10.150.0.10"
10.150.0.10
```

Every VM carries an `AppTier` and an `Environment` category; the `quarantine` set exists and is empty.

**Negative test.** No behavior changes yet — categories alone enforce nothing, exactly as in Prism Central.

**Cleanup.** None.

### Exercise 4.2 — Write the policy in monitor mode

**Objective.** Express the application policy, but only count and classify — drop nothing.

**Track 1 — Walkthrough.** Create an application security policy securing `AppTier: db` (inbound only from `AppTier: web` on 5432) and one securing `AppTier: plc` (inbound only from `AppTier: hmi` on 502); **save both in monitor mode**:

```text
pc> Network & Security > Security Policies > Create > Application Policy
pc>   secure AppTier:db  — inbound: AppTier:web tcp/5432 ; save in Monitor mode
pc>   secure AppTier:plc — inbound: AppTier:hmi tcp/502  ; save in Monitor mode
```

**Track 2 — Walkthrough.** A count-only chain on the bridge forward hook, `policy accept` — it classifies every flow the policy speaks about, and everything it would have denied, without dropping a packet:

```bash
sudo nft add chain bridge flow monitor '{ type filter hook forward priority 0; policy accept; }'
sudo nft add rule bridge flow monitor ip saddr @apptier_web ip daddr @apptier_db  tcp dport 5432 counter accept
sudo nft add rule bridge flow monitor ip saddr @apptier_hmi ip daddr @apptier_plc tcp dport 502  counter accept
sudo nft add rule bridge flow monitor ip protocol tcp counter
```

The final rule is the "would be denied" bucket: any TCP flow not matched by a sanctioned permit lands there — and is still accepted, because the chain's policy is accept.

**Expected result.** The chain exists with three counters at zero; all traffic still flows.

**Negative test.**

```bash
sudo ip netns exec hmi bash -c 'nc -z -w2 10.150.0.20 5432 && echo "lateral STILL OPEN (monitor mode)"'
lateral STILL OPEN (monitor mode)
```

Monitor mode never blocks — that is its purpose.

**Cleanup.** None.

### Exercise 4.3 — Read the flows before enforcing

**Objective.** Use the monitor telemetry to see the sanctioned flows and discover the lateral one, as Prism Central's flow visualization would.

**Track 1 — Walkthrough.** Open the policy in Prism Central; the flow diagram shows observed traffic into the secured tiers — including a flow from `AppTier: hmi` to `AppTier: db` that no rule sanctions. That discovered flow is the finding.

**Track 2 — Walkthrough.** Generate the day's traffic, then read the counters:

```bash
sudo ip netns exec web bash -c 'nc -z -w2 10.150.0.20 5432'
sudo ip netns exec hmi bash -c 'nc -z -w2 10.150.0.40 502'
sudo ip netns exec hmi bash -c 'nc -z -w2 10.150.0.20 5432'
sudo nft list chain bridge flow monitor | grep counter
```

**Expected result.** The two sanctioned rules show non-zero packets, and the final "would be denied" bucket is also non-zero — the lateral `hmi → db` flow, visible before anything is enforced:

```text
ip saddr @apptier_web ip daddr @apptier_db tcp dport 5432 counter packets 2 bytes 120 accept
ip saddr @apptier_hmi ip daddr @apptier_plc tcp dport 502 counter packets 2 bytes 120 accept
ip protocol tcp counter packets 2 bytes 120
```

**Negative test.** Reset and confirm a quiet estate counts nothing: `sudo nft reset counters table bridge flow >/dev/null` then re-list — counters return to zero until traffic flows again.

**Cleanup.** None — the monitor chain stays until Chapter 05 applies the policy.

## Summary and Completion Checklist

- [ ] Categories created and assigned; policy language is labels, not addresses.
- [ ] Application policy expressed in monitor mode; nothing dropped.
- [ ] Telemetry read: sanctioned flows counted, lateral flow discovered.
