# Chapter 07: Policy — Allow, Block, Alert, then Enforce

## Learning Objectives

- Author ordered allow / block / alert rules against labeled groups.
- Validate policy in an alert-only posture before enforcing it.
- Prove that label-based policy scales, and reason about process-scoped rules.
- Enforce on Windows through the Windows Filtering Platform.

You saw the flows in Chapter 06. Now you write the policy that permits the two legitimate ones and denies the rest, validating each change in alert-only before it blocks.

## Hands-On Lab

### Lab 7.1 — Ring-fence the database, alert-only first

**Objective.** Permit Web→Database on 5432, deny every other path into the database — validated in alert-only, then enforced.

**Track 1 — Real Guardicore.**

**Step 1.** Author policy rules scoped by label. First an **allow**: source `Role: Web`, destination `Role: Database`, service PostgreSQL/TCP 5432. Then rely on a default-deny posture (or an explicit **block** to `Role: Database`) for everything else.

**Step 2.** Keep the block posture as **alert-only** first. In Reveal, confirm the alerts show the HMI→db attempt as something a block rule *would* catch, and that the app→db flow raises no alert.

**Step 3.** Once validated, switch the database's protection from alert to **enforce**.

**Track 2 — Native equivalent.**

**Step 1.** On `gc-db01`, express the ring-fence with the segmentation chain still in alert-only (log-and-accept):

```bash
sudo tee /etc/nftables.conf > /dev/null <<'EOF'
#!/usr/sbin/nft -f
flush ruleset
define DB_PORT = 5432
table inet guardicore {
    set app_tier { type ipv4_addr; elements = { 10.10.20.11 } }
    chain input {
        type filter hook input priority 0; policy accept;
        ct state established,related accept
        iif "lo" accept
        tcp dport 22 accept
        jump segmentation
    }
    chain segmentation {
        ip saddr @app_tier tcp dport $DB_PORT accept
        tcp dport $DB_PORT log prefix "GC-WOULD-BLOCK db: " level warn accept
        accept
    }
}
EOF
sudo nft -f /etc/nftables.conf
```

**Step 2.** Watch the alert stream while reproducing the attack. On `gc-db01`: `sudo journalctl -kf | grep "GC-WOULD-BLOCK" &`. From `gc-win01`: `Test-NetConnection 10.10.20.12 -Port 5432`. Expect a `GC-WOULD-BLOCK db:` line for the HMI, and none for the app's own query.

**Step 3.** Enforce: change the segmentation chain so the database port default-denies.

```bash
sudo nft flush chain inet guardicore segmentation
sudo nft add rule inet guardicore segmentation ip saddr @app_tier tcp dport 5432 accept
sudo nft add rule inet guardicore segmentation tcp dport 5432 log prefix "GC-BLOCK db: " level warn drop
sudo nft add rule inet guardicore input tcp dport '{ 5432 }' # (already jumped) - verify:
sudo nft 'add rule inet guardicore input meta l4proto tcp'   # no-op guard; see note
```

Simpler and clearer — set the base policy to drop and permit only what is named:

```bash
sudo nft chain inet guardicore input '{ policy drop; }'
```

**Step 4.** Confirm: `~/checkdb.sh` on `gc-app01` still prints `3`; `Test-NetConnection 10.10.20.12 -Port 5432` from the HMI now fails.

**Expected result.** App→db works; HMI→db is blocked and logged; the attack from Chapter 05 is dead.

**Negative test.** Add `10.10.20.21` to `app_tier` "to be safe" and re-run the attack — it succeeds. An over-broad group re-authorizes the lateral movement. Remove it.

**Cleanup.** Keep the enforced ring-fence.

### Lab 7.2 — Ordered rules and label-based scale

**Objective.** Show that policy written against a label protects a new workload automatically, and that rule order (block before allow) matters.

**Track 1 — Real Guardicore.** A rule naming `Role: Web` protects any new web server the moment it is labeled — no rule edit. A **block** rule for a risky service (say RDP or SMB) placed ahead of broad allows stops that service fleet-wide regardless of later allows.

**Track 2 — Native equivalent (demonstration).**

```bash
# A new 'web' host is authorized simply by joining the set:
sudo nft add element inet guardicore app_tier '{ 10.10.20.13 }'
sudo nft list set inet guardicore app_tier
# ...and de-authorized by leaving it:
sudo nft delete element inet guardicore app_tier '{ 10.10.20.13 }'
```

Order: in nftables the first matching rule wins, so a `drop` for a dangerous port placed before the `accept` fall-through enforces "block wins" — the native analogue of ordering a block rule ahead of allows.

**Expected result.** Membership (the label), not a rule edit, decides access; ordering a block ahead of allows enforces it first.

**Negative test.** Rewrite the rule to name the address `10.10.20.11` directly; it works until the app is rebuilt with a new address, then fails silently. Address-based rules are the debt label-based policy retires. Revert to the set.

**Cleanup.** `app_tier` contains only `10.10.20.11`.

### Lab 7.3 — Enforce on Windows through the Windows Filtering Platform

**Objective.** Bring `gc-win01` to enforcement so nothing may reach the HMI and it may only poll the PLC.

**Track 1 — Real Guardicore.** Author an allow (source `Role: HMI`, destination the PLC asset, service Modbus TCP 502), then enforce on `gc-win01`; the agent programs WFP.

**Track 2 — Native equivalent.**

```powershell
Set-NetFirewallProfile -Profile Domain,Private,Public `
    -DefaultInboundAction Block -DefaultOutboundAction Block
New-NetFirewallRule -DisplayName "GC HMI->PLC 502" -Direction Outbound `
    -RemoteAddress 10.10.30.50 -Protocol TCP -RemotePort 502 -Action Allow
New-NetFirewallRule -DisplayName "GC DNS out" -Direction Outbound `
    -RemotePort 53 -Protocol UDP -Action Allow
New-NetFirewallRule -DisplayName "GC mgmt RDP in" -Direction Inbound `
    -RemoteAddress 10.10.20.1 -Protocol TCP -LocalPort 3389 -Action Allow
```

**Step 2.** Verify:

```powershell
Test-NetConnection -ComputerName 10.10.30.50 -Port 502   # expect True
Test-NetConnection -ComputerName 10.10.20.12 -Port 5432  # expect False
```

**Expected result.** HMI→PLC 502 works; HMI→db 5432 fails at the source. The attack is blocked at both ends — defense in depth.

**Negative test.** Remove the management RDP allow and reboot; you may lock yourself out. Re-add it before continuing. Lab 9.2 rehearses this.

**Cleanup.** Keep the enforced Windows posture.

### Lab 7.4 — Process-scoped policy (Design Exercise)

**Objective.** Reason about a capability with no faithful native stand-in: scoping a rule to a **process**, which Guardicore's agent telemetry makes possible.

**Design Exercise.**

1. The Reveal map shows that 5432 on `gc-db01` is served by the `postgres` process, and the legitimate client on `gc-app01` is `psql` (or the app runtime). Explain how a rule that permits *only the app's process* to reach `postgres` — rather than "any process on gc-app01" — reduces the blast radius if `gc-app01` is compromised by a webshell running as a different user.
2. Contrast this with the native Track 2 rule, which can only match source IP and port. What does the address-and-port rule fail to prevent that the process-scoped rule prevents?

**Model answer.**

1. A process-scoped allow ties the permission to the identity of the workload's software, not merely its address. If an attacker lands a webshell on `gc-app01`, the webshell is a different process (and often a different user) than the sanctioned app; a process-scoped rule does not extend the database permission to it, so the stolen foothold cannot reach 5432 even though it sits on an "allowed" host. The address-and-port rule cannot see this distinction and would let the webshell inherit the app's database access.
2. The native rule permits *anything* on `10.10.20.11` to reach `10.10.20.12:5432`. It cannot prevent a malicious process on the allowed host from using the allow. Process context is the signal that closes that gap, and it is exactly what the agent supplies and a packet filter cannot.

**Expected result.** A written justification for process-scoped policy.

**Negative test.** Argue process scope is unnecessary because "the host is trusted." Trust at host granularity is what lateral movement exploits — a compromised host is still an allowed host. Process scope narrows trust to the software that earned it.

**Cleanup.** None.

## Summary and Completion Checklist

- [ ] `gc-db01` enforced; app→db works, HMI→db blocked, validated in alert-only first.
- [ ] Label-based policy shown to follow membership; block-before-allow ordering understood.
- [ ] `gc-win01` enforced through WFP; HMI→PLC 502 works, HMI→db blocked at source.
- [ ] Process-scoped policy reasoned through.
