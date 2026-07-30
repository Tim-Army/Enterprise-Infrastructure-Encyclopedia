# Chapter 06: The Agentless Model and the Learning Phase

## Learning Objectives

- Explain how an agentless platform enforces policy without installing anything on the protected host.
- Bring the estate under management, or prepare the identical native firewalls.
- Run the monitoring/learning phase and derive least-privilege allow rules from observed traffic.
- Review the learned rules before enforcing anything.

This is the core of the lab. Each exercise carries both tracks. For Zero Networks the two tracks are unusually close: the platform enforces by remotely programming the native firewall, so Track 2 programs the very same firewall by hand. What Track 1 adds is the automation — the learning, the rule generation, and the MFA — not a different enforcement engine.

Zero Networks' method is **monitor, learn, least-privilege, then enforce** — and keep administrative ports closed until a just-in-time, MFA-verified grant opens them (Chapter 07).

## Hands-On Lab

### Lab 6.1 — The agentless model

**Objective.** State how Zero Networks enforces without an agent, and what it needs from each host.

**Background.** Zero Networks installs no software on protected workloads. It uses a privileged service account to reach each host's **firewall management interface** — the Windows Firewall (over RPC) on Windows, the host firewall (over SSH) on Linux — reads the host's traffic telemetry, and writes least-privilege rules directly into that native firewall. Consequences:

- The enforcement artifact is the **native OS firewall** — the same `nftables`/Windows Filtering Platform you can inspect and write yourself.
- The platform needs **reachability and privilege** to each host's firewall management path. In this lab that path is the VMnet2 segment and the hosts' own admin credentials.
- A device with **no manageable host firewall** (the PLC) cannot be programmed this way and must be protected from a neighbor (Chapter 08).

**Walkthrough.**

**Step 1.** Classify each host by how it will be protected:

| Host | Manageable firewall? | Protection approach |
|:---|:---|:---|
| zn-app01 | Yes (Linux nftables) | Remote-programmed native firewall |
| zn-db01 | Yes (Linux nftables) | Remote-programmed native firewall |
| zn-win01 | Yes (Windows Firewall) | Remote-programmed native firewall |
| zn-gw | Yes (Linux nftables) | Remote-programmed native firewall; also OT enforcement point |
| zn-ot01 | **No** | Protected from its managed neighbor (Chapter 08) |

**Step 2.** State the model in one sentence: *Zero Networks is the automation that learns least-privilege rules and writes them into the firewall each host already has — and gates admin ports behind MFA.*

**Expected result.** A per-host protection plan.

**Negative test.** Assume the PLC can be protected "like the others" by remote firewall management. It cannot — it exposes no manageable host firewall. That is why Chapter 08 enforces on its neighbor instead.

**Cleanup.** None.

### Lab 6.2 — Bring the estate under management (or prepare the native firewalls)

**Objective.** Establish the management relationship — real, or by preparing the same native firewalls in a monitoring posture.

**Track 1 — Real Zero Networks.** In the console, add the hosts to the deployment and grant the service account the privilege to manage each host's firewall. Confirm each host shows as reachable and in **Monitoring** (learning) state — the platform is observing but not yet enforcing.

**Track 2 — Native equivalent.** Put each host's native firewall into a monitoring posture: enabled, logging, but permissive — the native analogue of "Monitoring".

**Step 1 — zn-app01, zn-db01, zn-gw.**

```bash
sudo apt -y install nftables conntrack
sudo tee /etc/nftables.conf > /dev/null <<'EOF'
#!/usr/sbin/nft -f
flush ruleset
table inet zeronet {
    chain input {
        type filter hook input priority 0; policy accept;   # Monitoring: permissive
        ct state established,related accept
        iif "lo" accept
        # log everything so we can LEARN the allow-list (Lab 6.3)
        log prefix "ZN-LEARN: " level info
    }
}
EOF
sudo nft -f /etc/nftables.conf
sudo systemctl enable --now nftables
```

On `zn-gw`, this `zeronet` table coexists with the `ip nat` table from Chapter 04.

**Step 2 — zn-win01.**

```powershell
Set-NetFirewallProfile -Profile Domain,Private,Public `
    -LogAllowed True -LogBlocked True `
    -LogFileName "%SystemRoot%\System32\LogFiles\Firewall\pfirewall.log" -LogMaxSizeKilobytes 8192
Set-NetFirewallProfile -Profile Domain,Private,Public `
    -DefaultInboundAction Allow -DefaultOutboundAction Allow
```

**Expected result.** Every manageable host is under management (Track 1) or logging in a permissive monitoring posture (Track 2). `~/reach.sh` still shows all REACH.

**Negative test.** Deny the service account the privilege to manage a host's firewall (Track 1), or remove your own admin rights (Track 2); the platform cannot write rules and the host stays unprotected. Agentless still requires privileged reach to the firewall — that is the trade for installing nothing.

**Cleanup.** Leave the monitoring posture in place.

### Lab 6.3 — The learning phase: derive least-privilege rules

**Objective.** Observe real traffic and derive the minimal allow-list — the automation Zero Networks performs over ~30 days, done here in minutes.

**Track 1 — Real Zero Networks.** Leave the hosts in Monitoring for the platform's learning window (default ~30 days). The platform records every observed flow and, at the end, proposes a least-privilege rule set: exactly the ports each host actually served, to exactly the peers that used them.

**Track 2 — Native equivalent.** Generate the representative traffic, then harvest the observed flows into an allow-list.

**Step 1.** Generate the legitimate traffic: run `~/checkdb.sh` a few times on `zn-app01`, poll the PLC from `zn-win01`. (Do **not** run the attack yet — you are learning the *legitimate* baseline.)

**Step 2.** On `zn-gw`, harvest the flows that crossed the estate into a candidate allow-list:

```bash
sudo conntrack -L 2>/dev/null \
  | sed -nE 's/.*src=([0-9.]+) dst=([0-9.]+) sport=[0-9]+ dport=([0-9]+).*/allow \1 -> \2 :\3/p' \
  | sort -u
```

**Expected result.** A short, exact allow-list — the least-privilege policy learned from behavior:

```text
allow 10.10.20.11 -> 10.10.20.12 :5432    (app -> db)
allow 10.10.20.21 -> 10.10.30.50 :502     (hmi -> plc)
```

Note what is **absent**: no rule for HMI→db, and no standing rule for 22 or 3389. Least-privilege is defined by what the estate actually did, not by what someone guessed.

**Negative test.** Run the Lab 5.3 attack *during* the learning window and harvest again; the malicious HMI→db flow now appears in the candidate list. Learning faithfully records whatever happens — so the learning window must observe *clean* traffic, or you will bless an attack path. This is why review (Lab 6.4) is mandatory.

**Cleanup.** Keep the allow-list; Chapter 07 enforces it.

### Lab 6.4 — Review the learned rules

**Objective.** Inspect and correct the learned allow-list before it becomes policy.

**Walkthrough.** Compare the learned list against the Chapter 05 specification. Confirm the two legitimate flows are present and that nothing else is — especially no HMI→db and no standing admin ports. Remove anything learned from noise or from an attack that slipped into the window.

**Expected result.** A reviewed allow-list identical to the legitimate-flows table.

**Negative test.** Accept the learned rules without review. If any unwanted flow occurred during monitoring, you have just codified it as policy. Automation proposes; a human must dispose.

**Cleanup.** Keep the reviewed allow-list.

## Summary and Completion Checklist

- [ ] The agentless, remote-firewall model understood, including its need for privileged reach.
- [ ] Hosts under management (or native firewalls in monitoring posture).
- [ ] A least-privilege allow-list learned from observed traffic.
- [ ] The allow-list reviewed against the legitimate-flows specification.
