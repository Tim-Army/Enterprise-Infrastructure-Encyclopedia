# Chapter 07: Enforcement and Just-in-Time MFA

## Learning Objectives

- Enforce the learned least-privilege rules and confirm the intended flows survive while the attack is blocked.
- Close the administrative ports and open them only just-in-time, after multi-factor authentication.
- Enforce the same posture on Windows, including just-in-time RDP.

You learned and reviewed the allow-list in Chapter 06. Now you enforce it — and add the control that defines Zero Networks: administrative ports that are closed until an authenticated, time-boxed grant opens them.

## Hands-On Lab

### Lab 7.1 — Enforce the learned rules

**Objective.** Flip the estate from monitoring to default-deny, permitting only the reviewed allow-list.

**Track 1 — Real Zero Networks.** Move the hosts from **Monitoring** to **Protected**. The platform writes the reviewed least-privilege rules into each host's firewall and sets the default to deny. Because the rules came from observed traffic, correctly-behaving applications keep working.

**Track 2 — Native equivalent.** On `zn-db01`, enforce the reviewed allow-list with a default-deny base:

```bash
sudo tee /etc/nftables.conf > /dev/null <<'EOF'
#!/usr/sbin/nft -f
flush ruleset
table inet zeronet {
    set app_tier { type ipv4_addr; elements = { 10.10.20.11 } }
    chain input {
        type filter hook input priority 0; policy drop;   # default-deny
        ct state established,related accept
        iif "lo" accept
        # learned least-privilege rule:
        ip saddr @app_tier tcp dport 5432 accept
        # NOTE: no standing rule for tcp/22 - admin access is just-in-time only (Lab 7.2)
        log prefix "ZN-DENY: " level warn
    }
}
EOF
sudo nft -f /etc/nftables.conf
```

**Step 2.** Confirm the legitimate flow survives and the attack — and standing SSH — are now blocked. From `zn-app01`: `~/checkdb.sh` → `3`. From `zn-win01`:

```powershell
Test-NetConnection -ComputerName 10.10.20.12 -Port 5432   # expect False (lateral movement blocked)
Test-NetConnection -ComputerName 10.10.20.12 -Port 22     # expect False (admin port closed by default)
```

**Expected result.** App→db works; HMI→db and standing SSH to the database are both blocked. The attack from Chapter 05 is dead, and the administrative surface is closed.

**Negative test.** Add a standing `tcp dport 22 accept` "so admins can always get in". You have re-opened the most abused lateral-movement port to every host on the segment. Remove it — admin access comes from Lab 7.2, not a standing rule.

**Rollback.** Keep the enforced ruleset.

### Lab 7.2 — Just-in-time MFA for privileged ports

**Objective.** Keep SSH closed by default and open it, for one source and a short window, only after an authenticated request — the control that gives Zero Networks its name.

**Track 1 — Real Zero Networks.** In the console, mark SSH (and RDP, WinRM, SMB) as **MFA-protected**. Thereafter a connection to a protected port is denied until the requesting user completes MFA; the platform then opens the port for that source for a time-boxed session and closes it automatically when the session ends.

**Track 2 — Native equivalent.** Build the same behavior: SSH is default-denied, and a **grant** opens it for one source for a fixed window, then auto-reverts. The human running the grant stands in for the MFA challenge (a person who has proven who they are).

**Step 1.** On `zn-db01`, add a named set for just-in-time grants and reference it before the deny:

```bash
sudo nft add set inet zeronet jit_ssh '{ type ipv4_addr ; flags timeout ; }'
sudo nft add rule inet zeronet input ip saddr @jit_ssh tcp dport 22 accept
```

The `timeout` flag means any address added to `jit_ssh` is automatically removed when its timeout expires — the native equivalent of a time-boxed session.

**Step 2.** Create the grant script — your "MFA-verified, just-in-time" access. Running it is the human gate:

```bash
cat > ~/zn-grant.sh <<'EOF'
#!/usr/bin/env bash
# Usage: zn-grant.sh <source-ip> <seconds>   (represents an MFA-verified JIT session)
SRC="$1"; TTL="${2:-120}"
sudo nft add element inet zeronet jit_ssh "{ $SRC timeout ${TTL}s }"
echo "Granted SSH from $SRC for ${TTL}s (auto-revokes)."
EOF
chmod +x ~/zn-grant.sh
```

**Step 3.** Prove the gate. First confirm SSH is closed from the admin host (`10.10.20.1`):

```bash
nc -vz 10.10.20.1-side  # from the Windows host: Test-NetConnection 10.10.20.12 -Port 22  -> False
```

Now "authenticate" and grant a 120-second window, then connect within it:

```bash
~/zn-grant.sh 10.10.20.1 120
# from the admin host, SSH now succeeds — for 120 seconds only
```

**Step 4.** Wait for the window to expire (or check `sudo nft list set inet zeronet jit_ssh` — the entry disappears), and confirm SSH is closed again.

**Expected result.** SSH to the database is closed by default, opens for exactly the granted source and duration after an authenticated request, and closes itself automatically. No standing administrative port exists.

**Negative test.** Grant with no timeout (`nft add element inet zeronet jit_ssh '{ 10.10.20.1 }'`). The port stays open indefinitely — you have recreated the standing admin port just-in-time was meant to eliminate. Always grant with a timeout.

**Rollback.** `sudo nft flush set inet zeronet jit_ssh`.

### Lab 7.3 — Enforce and gate RDP on Windows

**Objective.** Bring `zn-win01` to default-deny and make RDP just-in-time.

**Track 1 — Real Zero Networks.** Protect `zn-win01`; mark RDP (3389) MFA-protected. RDP is denied until an MFA-verified grant opens it for the requesting source.

**Track 2 — Native equivalent.**

```powershell
Set-NetFirewallProfile -Profile Domain,Private,Public `
    -DefaultInboundAction Block -DefaultOutboundAction Block
# Allow the one legitimate job: HMI -> PLC on Modbus 502
New-NetFirewallRule -DisplayName "ZN HMI->PLC 502" -Direction Outbound `
    -RemoteAddress 10.10.30.50 -Protocol TCP -RemotePort 502 -Action Allow
New-NetFirewallRule -DisplayName "ZN DNS out" -Direction Outbound -RemotePort 53 -Protocol UDP -Action Allow
# RDP is DISABLED by default - no standing inbound 3389 rule.
```

Grant just-in-time RDP as a time-boxed rule you add on request and remove after (a scheduled task can auto-remove it):

```powershell
# "MFA-verified" JIT grant: open RDP from the admin host for 2 minutes
New-NetFirewallRule -DisplayName "ZN JIT RDP" -Direction Inbound `
    -RemoteAddress 10.10.20.1 -Protocol TCP -LocalPort 3389 -Action Allow
Start-Job { Start-Sleep 120; Remove-NetFirewallRule -DisplayName "ZN JIT RDP" } | Out-Null
```

**Expected result.** RDP to the HMI is closed by default and opens only for the granted source and window.

**Negative test.** Leave the JIT RDP rule in place permanently; you have a standing admin port again. The auto-remove job is the point.

**Rollback.** `Remove-NetFirewallRule -DisplayName "ZN JIT RDP" -ErrorAction SilentlyContinue`.

### Lab 7.4 — Learning and identity at scale (Design Exercise)

**Objective.** Reason about the two capabilities with no faithful native stand-in: automatic rule learning across thousands of hosts, and the real MFA identity flow.

**Design Exercise.**

1. In this lab you learned rules from a handful of flows in minutes. Explain why a real deployment monitors for ~30 days before enforcing, and what fails if the window is too short (or observes abnormal traffic).
2. Track 2 represents MFA by "a human runs the grant script." Explain what a real MFA flow adds that the script cannot: identity binding (who), a second factor (proof), and an audit trail (accountability). Why is gating on *identity* stronger than gating on source IP alone?

**Model answer.**

1. Thirty days is chosen to capture periodic but legitimate traffic — month-end batch jobs, weekly backups, quarterly processes — that a short window would miss and then wrongly block on enforcement. Too short a window under-learns and causes outages; a window that observes an incident over-learns and blesses attack paths. The length trades completeness against the risk of learning bad behavior, which is why review is mandatory.
2. A real MFA grant binds the open port to a *person* who proved a second factor, and records that grant for audit. Source-IP gating only proves a packet came from an address — which an attacker who owns that host also satisfies. Identity-plus-MFA makes the administrative session attributable and requires proof the attacker usually lacks, turning "any process on an allowed host" into "this authenticated administrator, now, for two minutes."

**Expected result.** A written justification for the learning window and identity-based gating.

**Negative test.** Argue IP-based JIT is "good enough". It stops standing exposure but not an attacker operating from the very host an admin uses; identity and a second factor are what close that gap.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Learned rules enforced; app→db works, HMI→db and standing SSH blocked.
- [ ] Just-in-time MFA for SSH built and proven to auto-revoke.
- [ ] RDP on Windows default-denied and gated just-in-time.
- [ ] The learning window and identity-based gating reasoned through.
