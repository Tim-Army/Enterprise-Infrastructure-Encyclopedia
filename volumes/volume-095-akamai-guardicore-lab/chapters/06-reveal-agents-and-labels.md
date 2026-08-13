# Chapter 06: Reveal, Agents, and Labels

## Learning Objectives

- Describe the Centra architecture and decide where agents go.
- Bring workloads under management, or stand up the identical native enforcement layer.
- Read the Reveal map, including its process-and-user context, before writing a rule.
- Apply Guardicore's flexible key/value labels.

This is the core of the lab. Each exercise carries both tracks. Read the Track 1 steps even if executing Track 2 — the console workflow is what you are ultimately learning.

Guardicore's method is **see, then segment**: label workloads, watch real flows in Reveal (with the process and user that produced them), draft ordered policy, validate it in an alert-only posture, and only then enforce.

## Hands-On Lab

### Lab 6.1 — Centra architecture and agent placement

**Objective.** State what each Centra component does and decide which hosts get an agent.

**Background.**

- **Management** is the console and policy brain. **Aggregators** and **Collectors** gather and correlate flow telemetry from agents (and, optionally, network collectors) into the **Reveal** map. The management plane never sits in the data path.
- The **agent** on each workload reports flows *with process and user context* and programs the **native OS firewall** — `iptables`/`nftables` on Linux, the **Windows Filtering Platform** on Windows.
- A device that can run no agent (the PLC) is not managed directly; it is protected by policy enforced on its managed neighbors.

**Walkthrough.**

**Step 1.** Decide agent placement and justify it:

| Host | Can run an agent? | Managed? | Why |
|:---|:---|:---|:---|
| gc-app01 | Yes (Linux) | **Agent** | Server you control; agent programs nftables and reports process context |
| gc-db01 | Yes (Linux) | **Agent** | Crown jewel; process-scoped rule for `postgres` |
| gc-win01 | Yes (Windows) | **Agent** | HMI; agent programs WFP |
| gc-gw | Yes (Linux) | **Agent** | Router; managed neighbor of the PLC |
| gc-ot01 | **No** | Unmanaged | Cannot take an agent; protected on its neighbors (Chapter 08) |

**Step 2.** State the rule: *if the asset can take an agent and you administer it, manage it; else protect it from its managed neighbors.*

**Expected result.** Four managed hosts, one unmanaged device.

**Negative test.** Plan to install the agent on `gc-ot01`. A real PLC has no OS to host it; forcing an agent onto OT is the classic error. Reassign it.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.2 — Deploy the agent (or stand up the native layer)

**Objective.** Bring the four managed workloads under management — for real, or by standing up the identical native enforcement layer.

**Track 1 — Real Guardicore.**

Prerequisites to verify first:

- Administrative rights on each host.
- **Resolution of and connectivity to the management/aggregator address** from each host — the agent's control channel.
- A supported firewall backend (`iptables`/`nftables`, WFP).
- **A single controller of the native firewall** — no competing firewall product or conflicting GPO.

**Step 1.** In the Centra console, open the agent download/installation page. It provides the OS-specific installer and the management address to register against.

**Step 2 — gc-app01, gc-db01, gc-gw (Linux).** Install and register the agent using the command Centra generates (the skeleton shows only its shape):

```bash
# SKELETON - use the exact installer/command and management address from Centra
sudo ./gc-agent-installer.sh --management <centra-mgmt-fqdn> --token <install-token>
# verify the service is up
systemctl status guardicore-agent 2>/dev/null || systemctl status gc-agent 2>/dev/null
```

**Step 3 — gc-win01 (Windows).** Run the Windows installer (elevated) with the management address, then verify the service:

```powershell
Get-Service | Where-Object { $_.Name -like "*guardicore*" -or $_.Name -like "*gc-agent*" } |
    Format-Table Name, Status, StartType
```

**Step 4.** In the console, confirm the four hosts appear as managed and **online**, initially reporting flows without enforcing. If a host does not appear, check resolution of and reachability to the management address first, then a competing firewall on Windows.

**Track 2 — Native equivalent — stand up the enforcement layer.**

Build the artifact the agent would deploy: a segmentation-ready nftables layer on Linux and an equivalent WFP posture on Windows, held in a logging-only, permissive state that mirrors Guardicore's **alert-only** posture.

**Step 1 — gc-app01, gc-db01, gc-gw.**

```bash
sudo tee /etc/nftables.conf > /dev/null <<'EOF'
#!/usr/sbin/nft -f
flush ruleset

table inet guardicore {
    set app_tier { type ipv4_addr; }
    set db_tier  { type ipv4_addr; }
    set hmi      { type ipv4_addr; }

    chain input {
        type filter hook input priority 0; policy accept;
        ct state established,related accept
        iif "lo" accept
        # --- SEGMENTATION (ALERT-ONLY) ---
        # Log what a block rule WOULD drop, but still accept.
        jump segmentation
    }

    chain segmentation {
        log prefix "GC-ALERT: " level info
        accept
    }
}
EOF
sudo nft -f /etc/nftables.conf
sudo systemctl enable --now nftables
```

On `gc-gw` this `guardicore` table coexists with the `ip nat` table from Chapter 04.

**Step 2 — gc-win01.**

```powershell
Set-NetFirewallProfile -Profile Domain,Private,Public `
    -LogAllowed True -LogBlocked True `
    -LogFileName "%SystemRoot%\System32\LogFiles\Firewall\pfirewall.log" `
    -LogMaxSizeKilobytes 8192
Set-NetFirewallProfile -Profile Domain,Private,Public `
    -DefaultInboundAction Allow -DefaultOutboundAction Allow
Get-NetFirewallProfile | Format-Table Name, Enabled, DefaultInboundAction, LogBlocked, LogAllowed
```

**Step 3.** Record the mapping:

| Guardicore concept | Track 2 native artifact |
|:---|:---|
| Agent | nftables service / Windows Filtering Platform |
| Managed & online | nftables loaded / firewall profile enabled |
| Alert-only rule | segmentation chain ends in `accept` + `log`; WFP default Allow + logging |
| Block rule enforced (Chapter 07) | segmentation chain drops; WFP default Block |
| Labeled group | nftables named `set`; Windows firewall `-RemoteAddress` groups |
| Reveal flow (with process) | `conntrack` + `ss -tnp` (process/user of the socket) |

**Expected result.** Four workloads under management — actually registered (Track 1) or carrying the alert-only native layer (Track 2) — with nothing yet blocked. `~/reach.sh` still shows all REACH.

**Negative test.** On Windows, force the firewall to a conflicting state via GPO and watch policy fail to apply (Track 1) or your profile changes revert (Track 2). A single controller of the native firewall is a prerequisite made tangible.

**Rollback.** Leave the alert-only layer in place.

### Lab 6.3 — Read the Reveal map (with process context)

**Objective.** See what talks to what — and *which process and user* produced each flow — before writing a rule.

**Track 1 — Real Guardicore.**

**Step 1.** Generate representative traffic: run the app→db loop on `gc-app01`, poll the PLC from `gc-win01`, and re-run the Lab 5.3 attack.

```bash
for i in $(seq 1 5); do ~/checkdb.sh >/dev/null; done
```

**Step 2.** Open **Reveal**, set the time window to the last hour, and read the map. Each edge carries not just source, destination, and port, but the **process** and **user** at each end — for example, the legitimate `postgres` process serving 5432 to the `psql` client on `gc-app01`, versus a raw `psql` from the HMI.

**Step 3.** Identify the two legitimate flows and the unwanted ones. The process context is where Guardicore adds signal an address-and-port map lacks: two flows to 5432 can look identical by 5-tuple yet differ entirely by the process and user behind them.

**Track 2 — Native equivalent — build a process-aware flow view.**

**Step 1.** On `gc-gw`, harvest flows; on each endpoint, attribute the socket to a process:

```bash
# who is talking (edge list) - from the choke point
sudo apt -y install conntrack
sudo conntrack -L 2>/dev/null \
  | sed -nE 's/.*src=([0-9.]+) dst=([0-9.]+) sport=[0-9]+ dport=([0-9]+).*/\1 -> \2 :\3/p' \
  | sort | uniq -c | sort -rn
```

```bash
# process + user behind each listening/─connected socket - on gc-db01
sudo ss -tnp state established '( sport = :5432 )'
# and on gc-app01, which process opened the client side:
sudo ss -tnp state established '( dport = :5432 )'
```

**Expected result.** An edge list plus the process/user at each end — the native reconstruction of what Reveal shows. You can see `postgres` serving 5432 to `psql`, and you can tell the app's `psql` from the HMI's.

**Negative test.** Design policy from the topology alone, ignoring process context; you will write a rule that permits "anything on gc-app01 → gc-db01:5432" and miss that a *different* process on gc-app01 (a webshell) could then abuse the same allow. Process context is why Guardicore rules can be tighter than an ACL.

**Rollback.** Keep the map as your specification.

### Lab 6.4 — Label the workloads

**Objective.** Apply Guardicore's flexible key/value labels so policy reads by role, not address.

**Track 1 — Real Guardicore.**

**Step 1.** In the console, assign labels to each asset. Guardicore labels are free-form key/value pairs:

| Host | Labels |
|:---|:---|
| gc-app01 | `Role: Web`, `Application: GCLab`, `Environment: Dev` |
| gc-db01 | `Role: Database`, `Application: GCLab`, `Environment: Dev` |
| gc-win01 | `Role: HMI`, `Application: OT-Supervisory` |
| gc-gw | `Role: Router`, `Application: Infrastructure` |

**Step 2.** Represent the PLC as an asset/IP (`10.10.30.50`) labeled `Role: PLC`, `Application: OT-Supervisory`, even though it runs no agent.

**Track 2 — Native equivalent.** Populate the named sets that stand in for labeled groups:

```bash
sudo nft add element inet guardicore app_tier '{ 10.10.20.11 }'
sudo nft add element inet guardicore db_tier  '{ 10.10.20.12 }'
sudo nft add element inet guardicore hmi      '{ 10.10.20.21 }'
sudo nft list table inet guardicore
```

**Expected result.** Every workload carries labels (Track 1) or belongs to a named set (Track 2); the PLC is a labeled object.

**Negative test.** Mislabel `gc-win01` as `Role: Web`; a later Web→Database allow would then authorize the HMI to reach the database — the exact movement you are stopping. Labels are policy. Correct it.

**Rollback.** Keep the labels/sets for Chapter 07.

## Summary and Completion Checklist

- [ ] Lab 6.1 complete, including its negative test.
- [ ] Lab 6.2 complete: four workloads managed (or the native alert-only layer).
- [ ] Lab 6.3 complete: a process-aware flow view distinguishing legitimate from unwanted flows.
- [ ] Lab 6.4 complete: every workload labeled; the PLC a labeled object.
