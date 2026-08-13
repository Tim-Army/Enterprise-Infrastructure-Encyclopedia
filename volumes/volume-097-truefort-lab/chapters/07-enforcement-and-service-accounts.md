# Chapter 07: Enforcement and Service-Account Binding

## Learning Objectives

- Enforce the application ring-fence and confirm the intended flow survives while the attack is blocked.
- Bind a service account to its sanctioned host *and process/identity*, so a stolen credential is useless elsewhere.
- Enforce the same posture on Windows.

You validated the ring-fence in Chapter 06. Now you enforce it — and add the control that defines TrueFort: policy that follows **identity**, so `svc_app` works only where and as it should.

## Hands-On Lab

### Lab 7.1 — Enforce the application ring-fence

**Objective.** Permit app→db from `tf-app01` only, deny every other path into the database.

**Track 1 — Real TrueFort.** Move the application policy from monitoring to **enforce**. The baselined app→db behavior is permitted; the HMI→db misuse is blocked on the native firewall.

**Track 2 — Native equivalent.** On `tf-db01`, enforce the ring-fence with default-deny:

```bash
sudo tee /etc/nftables.conf > /dev/null <<'EOF'
#!/usr/sbin/nft -f
flush ruleset
table inet truefort {
    chain input {
        type filter hook input priority 0; policy drop;
        ct state established,related accept
        iif "lo" accept
        tcp dport 22 accept
        ip saddr 10.10.20.11 tcp dport 5432 accept   # only the app host
        log prefix "TF-DENY: " level warn
    }
}
EOF
sudo nft -f /etc/nftables.conf
```

**Step 2.** From `tf-app01`: `~/checkdb.sh` → `3`. From `tf-win01`: `Test-NetConnection 10.10.20.12 -Port 5432` → **False**.

**Expected result.** App→db works; the HMI's stolen-credential attempt is blocked at the network before the database ever checks the password.

**Negative test.** The network rule blocks the HMI, but consider: what if the attacker runs *on `tf-app01` itself* (a webshell on the allowed host)? The source-IP rule would let it through. Lab 7.2 closes that gap.

**Rollback.** Keep the ring-fence.

### Lab 7.2 — Bind the service account to its sanctioned identity

**Objective.** Ensure `svc_app` reaches the database only when used by the **sanctioned application process/identity** — not by any other process that happens to run on the app host. This is TrueFort's signature control, done natively with an owner-matched rule.

**Track 1 — Real TrueFort.** TrueFort ties the permitted app→db behavior to the specific application process and service identity it baselined. A different process on `tf-app01` using `svc_app` — a webshell, a curious admin, malware — does not match the baseline and is blocked and alerted, even though it sits on the "allowed" host and holds a valid password.

**Track 2 — Native equivalent — owner-matched egress.** On `tf-app01`, run the application as a dedicated identity and permit only *that identity's* egress to the database. The Linux socket owner UID is the native stand-in for "which process/identity".

**Step 1.** Create the app's service identity and re-home the database probe under it:

```bash
sudo useradd -r -s /usr/sbin/nologin svcapp
sudo install -o svcapp -g svcapp -m 700 -d /opt/svcapp
sudo tee /opt/svcapp/checkdb.sh > /dev/null <<'EOF'
#!/usr/bin/env bash
PGPASSWORD='Svc!AppPassw0rd' psql -h 10.10.20.12 -U svc_app -d tflab -tAc "SELECT count(*) FROM customers;"
EOF
sudo chown svcapp:svcapp /opt/svcapp/checkdb.sh && sudo chmod 750 /opt/svcapp/checkdb.sh
```

**Step 2.** On `tf-app01`, filter **outbound** to the database by socket owner: only `svcapp` may reach `tf-db01:5432`.

```bash
APPUID=$(id -u svcapp)
sudo nft add table inet tf_out
sudo nft add chain inet tf_out output '{ type filter hook output priority 0 ; policy accept ; }'
# only svcapp's UID may egress to the database on 5432; anyone else is dropped + logged
sudo nft add rule inet tf_out output ip daddr 10.10.20.12 tcp dport 5432 meta skuid "$APPUID" accept
sudo nft add rule inet tf_out output ip daddr 10.10.20.12 tcp dport 5432 \
    log prefix "TF-IDENTITY-DENY 5432: " level warn drop
```

**Step 3.** Prove the binding. As the sanctioned identity it works; as any other user, the identical credential fails:

```bash
sudo -u svcapp /opt/svcapp/checkdb.sh        # -> 3  (sanctioned identity)
~/checkdb.sh                                  # as labadmin (a "webshell") -> DROPPED, logged
sudo journalctl -k | grep "TF-IDENTITY-DENY" | tail -2
```

**Expected result.** `svc_app` reaches the database only when used by `svcapp`; the *same credential* run by any other user on the same host is dropped and logged. A stolen service account is now bound to the process identity that earned it — the network path is denied to everyone else even on the allowed host.

**Negative test.** Remove the owner match (`meta skuid`) and re-run `~/checkdb.sh` as labadmin; it succeeds. Without identity binding, any process on the allowed host inherits the service account's access — exactly the lateral-movement gap TrueFort closes. Restore the match.

**Rollback.** Keep the owner-matched rule.

### Lab 7.3 — Enforce on Windows

**Objective.** Bring `tf-win01` to default-deny; it may only poll the PLC.

**Track 1 — Real TrueFort.** Enforce the HMI's baselined behavior (HMI→PLC 502) and deny the rest.

**Track 2 — Native equivalent.**

```powershell
Set-NetFirewallProfile -Profile Domain,Private,Public `
    -DefaultInboundAction Block -DefaultOutboundAction Block
New-NetFirewallRule -DisplayName "TF HMI->PLC 502" -Direction Outbound `
    -RemoteAddress 10.10.30.50 -Protocol TCP -RemotePort 502 -Action Allow
New-NetFirewallRule -DisplayName "TF DNS out" -Direction Outbound -RemotePort 53 -Protocol UDP -Action Allow
New-NetFirewallRule -DisplayName "TF mgmt RDP in" -Direction Inbound `
    -RemoteAddress 10.10.20.1 -Protocol TCP -LocalPort 3389 -Action Allow
```

**Step 2.** Verify: `Test-NetConnection 10.10.30.50 -Port 502` → True; `Test-NetConnection 10.10.20.12 -Port 5432` → False. The stolen-credential attempt from the HMI is now blocked at the source too.

**Expected result.** HMI→PLC 502 works; HMI→db is blocked at both ends.

**Negative test.** Remove the management RDP allow and reboot; you may lock yourself out. Re-add it first (Lab 9.2).

**Rollback.** Keep the enforced Windows posture.

### Lab 7.4 — Behavioral baselining and EDR at scale (Design Exercise)

**Objective.** Reason about the two capabilities with no faithful native stand-in.

**Design Exercise.**

1. TrueFort baselines application *behavior* across a fleet and flags deviations. Explain why behavior is a stronger policy anchor than a static allow-list when applications are updated, scaled, or moved — and what a behavioral baseline can catch that a fixed 5-tuple rule cannot.
2. Track 2 bound the service account to a UID on one host. Explain what EDR-sourced identity telemetry adds at scale: process lineage (what launched the process), user-to-service mapping across thousands of hosts, and correlation of the *same* service account's use everywhere at once.

**Model answer.**

1. Behavior tolerates legitimate change (a patched binary, a new replica, a re-addressed host) while still flagging the abnormal (a service account used from a new process, a server suddenly scanning peers). A fixed 5-tuple rule either breaks on legitimate change or is written so broadly it misses the abnormal. Behavior is the moving target policy that static rules cannot express.
2. At scale you cannot hand-write owner matches per host. EDR telemetry supplies process lineage and identity mapping fleet-wide, so TrueFort can say "this service account is used by exactly these processes on exactly these hosts" and alert the instant it appears anywhere else — the same idea as the UID match, computed continuously across the estate.

**Expected result.** A written justification for behavioral, identity-anchored policy.

**Negative test.** Argue static rules are sufficient because "the app never changes." Real estates change constantly; the rule that never adapts is the rule that is either broken or bypassed.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Application ring-fence enforced; app→db works, HMI→db blocked.
- [ ] Service account bound to its sanctioned identity; the same credential fails from any other process on the allowed host.
- [ ] `tf-win01` enforced; HMI→PLC 502 works, HMI→db blocked at source.
- [ ] Behavioral, identity-anchored policy reasoned through.
