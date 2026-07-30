# Chapter 06: Illumio Visibility, VENs, and Labels

## Learning Objectives

- Explain the split between the PCE and the VEN, and assign the correct enforcement state to each asset.
- Bring workloads under management with a pairing profile, or stand up the identical native enforcement layer.
- Apply Illumio's four-dimensional label model.
- Discover and visualize real traffic in Illumination before writing any rule.

This is the core of the lab. Each exercise carries both tracks. Read the Track 1 steps even if you are executing Track 2 — the console workflow is what you are ultimately learning, and Track 2 exists so the concepts land on real enforcement primitives while you may lack a PCE.

Illumio's method is **model, then enforce**: label every workload, watch real traffic in Illumination, draft policy against the labels, validate it, and only then move workloads from **Visibility Only** to **Full Enforcement**. You never write a rule against an IP address, and you never enforce before you have seen the traffic.

## Hands-On Lab

### Lab 6.1 — The PCE/VEN split and the four enforcement states

**Objective.** State what the PCE does, what the VEN does, and which enforcement state each lab host should start in. This is the design skill the product demands.

**Background.**

- The **PCE (Policy Compute Engine)** holds labels and policy, correlates flow telemetry into the **Illumination** map, and compiles policy into per-workload rules. It never sits in the data path.
- The **VEN (Virtual Enforcement Node)** runs on each workload and programs the **native OS firewall** — `iptables`/`nftables` on Linux, the **Windows Filtering Platform** on Windows. It reports flows to the PCE and applies the rules the PCE compiles.
- Every managed workload sits in one of four **enforcement states**:
  1. **Idle** — VEN installed, firewall untouched, minimal telemetry. The safe first state during rollout.
  2. **Visibility Only** — the VEN reports every flow but enforces nothing. This is the discovery state, and the equivalent of a "simulate" mode.
  3. **Selective Enforcement** — enforce only the services named by an **enforcement boundary**; everything else stays in visibility. Used to phase enforcement in service by service.
  4. **Full Enforcement** — default-deny; only flows explicitly allowed by policy pass.

**Walkthrough.**

**Step 1.** For each lab host, decide the initial enforcement state and why. Fill this in before reading the model answer:

| Host | Can run a VEN? | Correct initial state | Why |
|:---|:---|:---|:---|
| il-app01 | | | |
| il-db01 | | | |
| il-win01 | | | |
| il-gw | | | |
| il-ot01 | | | |

**Step 2 — model answer:**

| Host | Can run a VEN? | Correct initial state | Why |
|:---|:---|:---|:---|
| il-app01 | Yes (Linux) | **Visibility Only** | Managed workload; watch flows before enforcing |
| il-db01 | Yes (Linux) | **Visibility Only** → **Full** | Crown jewel; the first to reach Full Enforcement |
| il-win01 | Yes (Windows) | **Visibility Only** | HMI; VEN programs WFP |
| il-gw | Yes (Linux) | **Visibility Only** | Router; managed neighbor of the PLC |
| il-ot01 | **No** | *Unmanaged workload* | Cannot take a VEN; protected by policy on its managed neighbors (Chapter 08) |

**Step 3.** State the decision rule you just applied:

> If the asset can take a VEN and you administer it → manage it, starting in Visibility Only. Else (it cannot take a VEN) → represent it as an unmanaged workload and enforce its protection on the managed workloads that talk to it.

**Expected result.** A per-asset plan: four managed workloads starting in Visibility Only, one unmanaged workload.

**Negative test.** Plan to install the VEN on `il-ot01`. It cannot run one — a real PLC has no general-purpose OS to host an agent. Forcing the agent model onto OT is the classic segmentation design error; Illumio's answer is the unmanaged-workload model, not an agent. Reassign it.

**Cleanup.** None.

### Lab 6.2 — Pair the VENs (or stand up the native layer)

**Objective.** Bring the four managed workloads under management — for real with a pairing profile if you have a PCE, or by standing up the identical native enforcement layer if you do not.

**Track 1 — Real Illumio.**

Prerequisites to verify before you touch the console:

- Administrative rights on each host — you have them (`labadmin` / `Administrator`).
- DNS resolution of the PCE FQDN — tested in Chapter 04.
- **Outbound TCP to the PCE on 8443** (and 8444 for some deployments) from each host — this is the VEN's control channel.
- A supported firewall backend — `iptables`/`nftables` on Linux, WFP on Windows.
- **No competing controller of the native firewall** — no third-party firewall product, no GPO forcing the Windows firewall to a conflicting state.

**Step 1.** In the PCE, create a **Pairing Profile**: **Infrastructure → Pairing Profiles → Add**. Set the initial state to **Visibility Only** and leave labels unassigned (you will assign them in Lab 6.3, or set defaults here). Click **Generate Key**; the PCE shows a pairing script for Linux and one for Windows, each embedding your PCE FQDN and a one-time **activation (pairing) code**.

**Step 2 — il-app01, il-db01, il-gw (Linux).** Copy the generated Linux pairing command to each host and run it. It downloads and activates the VEN. Use the command your PCE generates; the skeleton only shows its shape:

```bash
# SKELETON — copy the real one-time command from Pairing Profiles > (your profile)
rm -fr /opt/illumio_ven_data/tmp && umask 026 && mkdir -p /opt/illumio_ven_data/tmp && \
curl "https://<pce-fqdn>:8443/api/v27/software/ven/image?pair_script=pair.sh&profile_id=<id>" \
  -o /opt/illumio_ven_data/tmp/pair.sh && \
sudo /opt/illumio_ven_data/tmp/pair.sh \
  --management-server <pce-fqdn>:8443 \
  --activation-code <ACTIVATION_CODE>
```

Confirm the VEN activated and reports healthy:

```bash
sudo /opt/illumio_ven/illumio-ven-ctl status
sudo /opt/illumio_ven/illumio-ven-ctl connectivity-check
```

**Step 3 — il-win01 (Windows).** Run the generated PowerShell pairing script from an **elevated** PowerShell, then verify the service:

```powershell
# SKELETON - use the exact script the PCE generates
Set-ExecutionPolicy -Scope Process Bypass -Force
# (paste the PCE's PowerShell pairing one-liner here)

Get-Service | Where-Object { $_.Name -like "*illumio*" } |
    Format-Table Name, Status, StartType
```

**Step 4.** In the PCE, open **Workloads**. Within a minute or two the four hosts appear as **Online**, each in **Visibility Only**. If a host does not come online, the cause is almost always a prerequisite — check DNS resolution of the PCE FQDN and outbound 8443 first, then a competing firewall product on Windows.

**Track 2 — Native equivalent — stand up the enforcement layer.**

You will build, by hand, the artifact the VEN would deploy: a segmentation-ready nftables layer on the Linux hosts and an equivalent WFP posture on Windows — held in a *logging-only, still-permissive* state that mirrors **Visibility Only**. Enforcement comes in Chapter 07.

**Step 1 — il-app01, il-db01, il-gw.** Install a scaffold ruleset with the *structure* of a microsegmentation policy (named sets for labels, a dedicated segmentation chain) but a final `accept`, so nothing is blocked yet:

```bash
sudo tee /etc/nftables.conf > /dev/null <<'EOF'
#!/usr/sbin/nft -f
flush ruleset

table inet illumio {
    # Named sets model Illumio labels/groups. Populated in Chapter 07.
    set role_web { type ipv4_addr; }
    set role_db  { type ipv4_addr; }
    set role_hmi { type ipv4_addr; }

    chain input {
        type filter hook input priority 0; policy accept;
        ct state established,related accept
        iif "lo" accept

        # --- SEGMENTATION CHAIN (VISIBILITY ONLY) ---
        # Log what a default-deny policy WOULD drop, but still accept.
        # This is exactly what Illumio Visibility Only does: report, do not block.
        jump segmentation
    }

    chain segmentation {
        # In Chapter 07 we flip the trailing 'accept' to 'drop' for Full Enforcement.
        log prefix "ILLUMIO-VIS: " level info
        accept
    }
}
EOF
sudo nft -f /etc/nftables.conf
sudo systemctl enable --now nftables
sudo nft list table inet illumio
```

Note: on `il-gw` this `illumio` table sits alongside the existing `ip nat` table from Chapter 04; both coexist.

**Step 2 — il-win01.** Put the Windows firewall into the equivalent posture: enabled, logging both allowed and dropped packets, default actions still permissive so nothing breaks yet:

```powershell
Set-NetFirewallProfile -Profile Domain,Private,Public `
    -LogAllowed True -LogBlocked True `
    -LogFileName "%SystemRoot%\System32\LogFiles\Firewall\pfirewall.log" `
    -LogMaxSizeKilobytes 8192
Set-NetFirewallProfile -Profile Domain,Private,Public `
    -DefaultInboundAction Allow -DefaultOutboundAction Allow
Get-NetFirewallProfile | Format-Table Name, Enabled, DefaultInboundAction, LogBlocked, LogAllowed
```

**Step 3.** Record the mapping so the analogy stays explicit:

| Illumio concept | Track 2 native artifact |
|:---|:---|
| VEN | nftables service / Windows Filtering Platform |
| Workload "Online" | nftables loaded / firewall profile enabled |
| Visibility Only | segmentation chain ends in `accept` + `log`; WFP default Allow + logging |
| Full Enforcement (Chapter 07) | segmentation chain ends in `drop`; WFP default Block |
| Label / labelled group | nftables named `set`; Windows firewall rule `-RemoteAddress` groups |
| Rule in a ruleset | nftables rule / `New-NetFirewallRule` |
| Provision draft policy | `nft -f` reload / apply the firewall rule |

**Expected result.** Four workloads under management — actually paired in Visibility Only (Track 1) or carrying the equivalent logging-only layer (Track 2) — with nothing yet blocked. `~/reach.sh` still shows all `REACH`.

**Negative test.** On Windows, apply a Group Policy that forces the firewall to a conflicting state, then observe (Track 1) the workload failing to apply policy, or (Track 2) your `Set-NetFirewallProfile` changes being reverted on the next GPO refresh. A single controller of the native firewall is a documented Illumio Windows prerequisite; here it is made tangible.

**Cleanup.** Leave the Visibility-Only layer in place; the rest of the lab builds on it.

### Lab 6.3 — Label the workloads

**Objective.** Apply Illumio's four-dimensional label model so that later policy is written against roles and applications, not addresses.

**Background.** Illumio labels have four dimensions: **Role**, **Application**, **Environment**, and **Location**. Policy references label sets, so a rule like "Web may reach Database on 5432 within ILLab" keeps working when you add a second web server or re-address the estate.

**Track 1 — Real Illumio.**

**Step 1.** In **Workloads**, select each host and assign labels:

| Host | Role | Application | Environment | Location |
|:---|:---|:---|:---|:---|
| il-app01 | Web | ILLab | Development | DC |
| il-db01 | Database | ILLab | Development | DC |
| il-win01 | HMI | OT-Supervisory | Production | DC |
| il-gw | Router | Infrastructure | Production | DC |

**Step 2.** Create an **Unmanaged Workload** (or an **IP List**) named `il-ot01-plc` for the PLC at `10.10.30.50`, labelled Role **PLC**, Application **OT-Supervisory**. Illumio cannot place a VEN there, but it can still be a first-class object in policy.

**Track 2 — Native equivalent.**

Populate the named sets that stand in for labels. On each Linux host, define the address groups you will reference in Chapter 07 (do this now so the policy reads by role, not by address):

```bash
sudo nft add element inet illumio role_web '{ 10.10.20.11 }'
sudo nft add element inet illumio role_db  '{ 10.10.20.12 }'
sudo nft add element inet illumio role_hmi '{ 10.10.20.21 }'
sudo nft list table inet illumio
```

**Expected result.** Every workload carries a Role/Application/Environment/Location label (Track 1) or belongs to a named set (Track 2); the PLC exists as an unmanaged object.

**Negative test.** Label `il-win01` with Role **Web** "because it is on the same segment." Later, a rule permitting Web→Database would silently authorize the HMI to reach the database — the exact lateral movement you are stopping. Labels are policy; get them wrong and the policy is wrong. Correct it to **HMI**.

**Cleanup.** Keep the labels/sets; Chapter 07 uses them.

### Lab 6.4 — Discover traffic in Illumination (build the flow map)

**Objective.** See what actually talks to what before writing a rule. You cannot segment what you cannot see.

**Track 1 — Real Illumio.**

**Step 1.** Generate representative traffic so the map has data. From `il-app01`, run the legitimate query a few times; from `il-win01`, poll the PLC; and re-run the Lab 5.3 lateral-movement attempt to the database:

```bash
for i in $(seq 1 5); do ~/checkdb.sh >/dev/null; done   # app -> db (legit)
```

**Step 2.** In the PCE, open **Illumination** (or **Illumination Plus**). Set the time window to the last hour. Nodes appear for each workload with directed edges for observed flows, colored by whether current policy would allow or block them.

**Step 3.** Identify on the map the two legitimate flows (app→db 5432, hmi→plc 502) and the unwanted ones (win01→db 5432, and any app01→plc). The map is where you *find* the boundary rather than guessing it.

**Track 2 — Native equivalent — build your own flow map.**

Illumination is drawn from VEN-reported flow telemetry. Collect the same telemetry with `conntrack` at the choke point.

**Step 1.** On `il-gw`, install and use connection tracking:

```bash
sudo apt -y install conntrack
```

**Step 2.** Generate the same traffic as Track 1 (app→db loop on `il-app01`, PLC poll from `il-win01`, and the attack attempt win01→db).

**Step 3.** Harvest the live flow table into a deduplicated "who talks to whom on which port" edge list — your flow map as data:

```bash
sudo conntrack -L 2>/dev/null \
  | sed -nE 's/.*src=([0-9.]+) dst=([0-9.]+) sport=[0-9]+ dport=([0-9]+).*/\1 -> \2 :\3/p' \
  | sort | uniq -c | sort -rn
```

**Expected result.** The map reveals both the legitimate and illegitimate edges, for example:

```text
   5 10.10.20.11 -> 10.10.20.12 :5432     legitimate  app -> db
   3 10.10.20.21 -> 10.10.30.50 :502      legitimate  hmi -> plc
   1 10.10.20.21 -> 10.10.20.12 :5432     UNWANTED    win -> db (lateral movement!)
```

You now know exactly where the boundary must sit.

**Negative test.** Try to design policy from the topology alone, without the map. You will either forget the legitimate app→db flow (and break the app in Chapter 07) or miss an unwanted flow (and leave a hole). Discovery-before-policy is not ceremony; skipping it is how real rollouts cause outages.

**Cleanup.** None — keep the map as your policy specification.

## Summary and Completion Checklist

- [ ] Lab 6.1 complete, including its negative test.
- [ ] Lab 6.2 complete: four workloads in Visibility Only (or the native logging-only layer).
- [ ] Lab 6.3 complete: every workload labelled; the PLC an unmanaged object.
- [ ] Lab 6.4 complete: a flow map that distinguishes legitimate from unwanted flows.
