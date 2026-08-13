# Chapter 07: Policy Analysis and Enforcement

## Learning Objectives

- Analyze a candidate policy against captured flows before enforcing it.
- Enforce the policy on the host firewall with `iptables` and `ipset`.
- Enforce the same posture on Windows through the Windows Filtering Platform.

You discovered and auto-generated the policy in Chapter 06. Secure Workload's discipline is to **analyze** it against real traffic before it ever blocks anything — then enforce.

## Hands-On Lab

### Lab 7.1 — Policy analysis: the "what-if" before enforcement

**Objective.** Replay observed flows against the candidate policy and see exactly what it would allow and deny — with nothing yet enforced.

**Track 1 — Real Secure Workload.** Run **policy analysis** in the workspace: the cluster evaluates the candidate policy against live and historical flows and labels each as *permitted* or *escaped/rejected*. You confirm the two legitimate flows are permitted and the attack flow is rejected before you click enforce.

**Track 2 — Native equivalent.** Evaluate a candidate policy against a set of flows — including the attack — without enforcing anything.

**Step 1.** Write the candidate policy (from ADM) and a small flow set that includes the attack, then analyze:

```bash
cat > ~/policy.csv <<'EOF'
10.10.20.11,10.10.20.12,5432
10.10.20.21,10.10.30.50,502
EOF
cat > ~/testflows.csv <<'EOF'
10.10.20.11,10.10.20.12,5432
10.10.20.21,10.10.30.50,502
10.10.20.21,10.10.20.12,5432
10.10.20.11,10.10.30.50,502
EOF
cat > ~/analyze.sh <<'EOF'
#!/usr/bin/env bash
while IFS=, read -r s d p; do
  if grep -qx "$s,$d,$p" ~/policy.csv; then echo "PERMIT  $s -> $d:$p"; else echo "REJECT  $s -> $d:$p"; fi
done < ~/testflows.csv
EOF
chmod +x ~/analyze.sh
~/analyze.sh
```

**Expected result.** The analysis shows the two legitimate flows **PERMIT** and the two attack flows **REJECT** — proof, before enforcement, that the policy permits the app and denies the lateral movement.

**Negative test.** Add the attack flow to `policy.csv` and re-analyze; it flips to PERMIT. Policy analysis is only as good as the policy you feed it — it tells you what *would* happen, so a bad rule is visible here rather than discovered during an outage. Remove it.

**Rollback.** Keep the analyzed policy.

### Lab 7.2 — Enforce on the host firewall with ipset

**Objective.** Enforce the analyzed policy on `cw-db01` using `iptables` and `ipset` — the artifacts the Secure Workload agent programs on Linux.

**Track 1 — Real Secure Workload.** Set the workspace to **enforced**; the agent programs each host's firewall (Linux `iptables`/`ipset`, Windows WFP) with the analyzed policy.

**Track 2 — Native equivalent.** On `cw-db01`, use an `ipset` for the discovered database clients and enforce:

```bash
sudo apt -y install ipset
sudo ipset create db_clients hash:ip
sudo ipset add db_clients 10.10.20.11          # the Web tier, from ADM
sudo iptables -N CW-SEG 2>/dev/null || sudo iptables -F CW-SEG
sudo iptables -A CW-SEG -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
sudo iptables -A CW-SEG -p tcp --dport 22 -s 10.10.20.1 -j ACCEPT     # break-glass mgmt
sudo iptables -A CW-SEG -p tcp --dport 5432 -m set --match-set db_clients src -j ACCEPT
sudo iptables -A CW-SEG -p tcp --dport 5432 -j LOG --log-prefix "CW-DENY db: "
sudo iptables -A CW-SEG -p tcp --dport 5432 -j DROP
# hook it:
sudo iptables -C INPUT -j CW-SEG 2>/dev/null || sudo iptables -A INPUT -j CW-SEG
```

**Step 2.** Confirm the legitimate flow survives and the attack is blocked. From `cw-app01`: `~/checkdb.sh` → `3`. From `cw-win01`: `Test-NetConnection 10.10.20.12 -Port 5432` → **False**.

**Expected result.** App→db works; HMI→db is blocked and logged. Using an `ipset` for the client group is exactly how the agent scales membership without rewriting rules — add a workload to the set, not a new rule.

**Negative test.** `sudo ipset add db_clients 10.10.20.21` (add the HMI) and re-run the attack — it succeeds. The `ipset` is the group; an over-broad group re-authorizes the movement. Remove it: `sudo ipset del db_clients 10.10.20.21`.

**Rollback.** Keep the enforced ruleset.

### Lab 7.3 — Enforce on Windows through the Windows Filtering Platform

**Objective.** Bring `cw-win01` to enforcement so it may only poll the PLC.

**Track 1 — Real Secure Workload.** The agent enforces the analyzed policy on `cw-win01` through WFP.

**Track 2 — Native equivalent.**

```powershell
Set-NetFirewallProfile -Profile Domain,Private,Public `
    -DefaultInboundAction Block -DefaultOutboundAction Block
New-NetFirewallRule -DisplayName "CW HMI->PLC 502" -Direction Outbound `
    -RemoteAddress 10.10.30.50 -Protocol TCP -RemotePort 502 -Action Allow
New-NetFirewallRule -DisplayName "CW DNS out" -Direction Outbound -RemotePort 53 -Protocol UDP -Action Allow
New-NetFirewallRule -DisplayName "CW mgmt RDP in" -Direction Inbound `
    -RemoteAddress 10.10.20.1 -Protocol TCP -LocalPort 3389 -Action Allow
```

**Step 2.** Verify: `Test-NetConnection 10.10.30.50 -Port 502` → True; `Test-NetConnection 10.10.20.12 -Port 5432` → False. The HMI→db attack is now blocked at the source too.

**Expected result.** HMI→PLC 502 works; HMI→db blocked at both ends.

**Negative test.** Remove the management RDP allow and reboot; you may lock yourself out. Re-add it first (Lab 9.2).

**Rollback.** Keep the enforced Windows posture.

### Lab 7.4 — Scopes and cluster-scale ADM (Design Exercise)

**Objective.** Reason about two capabilities with no faithful native stand-in.

**Design Exercise.**

1. **Scopes.** Secure Workload organizes workloads in a hierarchical scope tree and delegates policy authoring per scope. Explain why hierarchy and delegation matter when different teams own the Web, Database, and OT tiers, and what breaks when everything lives in one flat policy.
2. **Cluster-scale ADM.** You performed ADM on four hosts by hand. Explain what the cluster does that you cannot: automatic clustering of thousands of workloads by flow similarity, continuous re-discovery as the application changes, and confidence scoring on proposed rules.

**Model answer.**

1. Hierarchy lets each team author policy for its own scope without seeing or breaking others', while a parent scope sets guardrails. A single flat policy forces every change through one owner, becomes unauditable, and couples unrelated teams — the operational failure that scopes exist to prevent.
2. At scale, clustering by hand is impossible; the cluster groups workloads by behavioral similarity, proposes tiers you would not spot by eye, re-runs as the app changes so the policy tracks reality, and scores each rule so you know which are confident and which need review. That continuous, scored discovery is the product's core value.

**Expected result.** A written justification for scopes and automated ADM.

**Negative test.** Argue hand-written policy is fine because "we know our app." Applications drift, teams change, and undocumented dependencies exist; discovery finds what you do not know, which is exactly where the risk lives.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] Candidate policy analyzed against flows; legitimate permitted, attack rejected — before enforcing.
- [ ] `cw-db01` enforced with `iptables`/`ipset`; app→db works, HMI→db blocked.
- [ ] `cw-win01` enforced through WFP; HMI→PLC 502 works, HMI→db blocked at source.
- [ ] Scopes and cluster-scale ADM reasoned through.
