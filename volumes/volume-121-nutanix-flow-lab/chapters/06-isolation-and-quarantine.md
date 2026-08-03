# Chapter 06: Isolation and Quarantine Policies

## Learning Objectives

- Add an **isolation policy**: `Environment: corp` and `Environment: ot` may never communicate.
- **Quarantine** a compromised VM: one action removes all its connectivity, overriding every permit.
- Release the quarantine and understand the strict-versus-forensic variants.

## Hands-On Lab

### Exercise 6.1 — Isolation policy between environments

**Objective.** Forbid all corp↔ot traffic categorically, regardless of application rules.

**Track 1 — Walkthrough.** Create an isolation environment policy between the two categories and apply it:

```text
pc> Network & Security > Security Policies > Create > Isolation Policy
pc>   isolate Environment:corp  <->  Environment:ot ; Apply
```

**Track 2 — Walkthrough.** Isolation outranks application policy, so its rules are **inserted above** the permits (FNS precedence: quarantine > isolation > application):

```bash
sudo nft insert rule bridge flow vswitch ip saddr @env_corp ip daddr @env_ot counter drop
sudo nft insert rule bridge flow vswitch ip saddr @env_ot ip daddr @env_corp counter drop
```

**Expected result.** Both sanctioned flows still work — web→db is corp-internal and hmi→plc is ot-internal — but any flow crossing the environment boundary is dropped by name:

```bash
sudo ip netns exec hmi bash -c 'nc -z -w2 10.150.0.20 5432 || echo "hmi->db DENIED (isolation)"'
hmi->db DENIED (isolation)
```

**Negative test.** The isolation drop counters advance while the default-deny counter does not — the lateral flow now dies at the isolation policy, one precedence level earlier than in Chapter 05.

**Cleanup.** None — isolation stays.

### Exercise 6.2 — Quarantine the compromised VM

**Objective.** Cut `hmi` off entirely — even its sanctioned flow — in one action.

**Track 1 — Walkthrough.** Quarantine is a built-in policy in Prism Central; applying the **Strict** quarantine category to a VM removes all its network access:

```text
pc> Compute > VMs > hmi > Actions > Quarantine (Strict)
```

**Track 2 — Walkthrough.** Quarantine outranks everything, so its rules sit at the very top — above even the connection-tracking accept, so established sessions die too. Quarantining the VM is a **category assignment**, not a rule edit:

```bash
sudo nft insert rule bridge flow vswitch ip daddr @quarantine counter drop
sudo nft insert rule bridge flow vswitch ip saddr @quarantine counter drop
sudo nft add element bridge flow quarantine '{ 10.150.0.30 }'
```

**Expected result.** The quarantined VM loses everything, including its previously sanctioned flow:

```bash
sudo ip netns exec hmi bash -c 'nc -z -w2 10.150.0.40 502 || echo "hmi->plc DENIED (quarantined)"'
hmi->plc DENIED (quarantined)
```

**Negative test.** The rest of the estate is untouched:

```bash
sudo ip netns exec web bash -c 'nc -z -w2 10.150.0.20 5432 && echo "web->db still OPEN"'
web->db still OPEN
```

**Cleanup.** Next exercise releases the quarantine.

### Exercise 6.3 — Release, and the forensic variant

**Objective.** Restore the remediated VM and understand the two quarantine modes.

**Track 1 — Walkthrough.** Removing the quarantine category restores the VM's normal policy. FNS offers two modes: **Strict** (no connectivity at all) and **Forensic** (reachable only by the tools in the forensic-tools category, so responders can examine a live machine that cannot reach anything else).

```text
pc> Compute > VMs > hmi > Actions > Unquarantine
```

**Track 2 — Walkthrough.** Release is removing the element — the rules never change:

```bash
sudo nft delete element bridge flow quarantine '{ 10.150.0.30 }'
sudo ip netns exec hmi bash -c 'nc -z -w2 10.150.0.40 502 && echo "hmi->plc RESTORED"'
hmi->plc RESTORED
```

**Expected result.** The sanctioned flow returns the moment the category is removed; the lateral path stays dead (isolation still applies). A forensic variant would add one insert above the quarantine drops: `ip saddr <forensic-host> ip daddr @quarantine tcp dport 22 accept`.

**Negative test.**

```bash
sudo ip netns exec hmi bash -c 'nc -z -w2 10.150.0.20 5432 || echo "hmi->db still DENIED"'
hmi->db still DENIED
```

**Cleanup.** Quarantine set is empty again; the machinery stays armed for Chapter 09's operations drills.

## Summary and Completion Checklist

- [ ] Isolation policy applied; corp↔ot dead, sanctioned intra-environment flows alive.
- [ ] Quarantine proven: one category assignment removes all connectivity, beating every permit.
- [ ] Release proven; strict vs forensic modes understood.
