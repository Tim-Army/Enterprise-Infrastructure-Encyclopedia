# Chapter 06: Xshield Visibility and Ring-Fencing

## Learning Objectives

- Assign the correct Xshield enforcement mode to each asset and justify it.
- Bring workloads under management, or stand up the identical native enforcement layer.
- Discover and visualize real traffic before writing any rule.
- Ring-fence a two-tier application and validate it in Observe mode first.

This is the core of the lab. Each exercise carries both tracks. Read the
Track 1 steps even if you are executing Track 2 — the console workflow
is what you are ultimately learning, and Track 2 exists so the concepts
land on real enforcement primitives while you may lack a tenant.

A reminder of the method you are following, which is ColorTokens’ own:
**Progressive Segmentation** — *discover, visualize, ring-fence, then
tighten* — always moving through **Observe** (simulate) before
**Enforce**.

## Hands-On Lab

### Lab 6.1 — Understand the five enforcement modes and choose per asset

**Objective.** Assign the correct Xshield enforcement mode to each of
the five lab hosts and justify it. This is the single most important
design skill the product demands.

**Background — the five modes**

Xshield’s distinguishing characteristic is the breadth of enforcement it
unifies under one console:

1. **Host agent** — a lightweight agent (under ~1% CPU, under ~100 MB

```text
RAM) that programs the native OS firewall: `iptables`/`nftables` on
Linux, the **Windows Filtering Platform (WFP)** on Windows. Best for
servers and endpoints you administer.

```

2. **EDR-mediated** — enforcement through an EDR you already run:

```text
**CrowdStrike, SentinelOne, or Microsoft Defender for Endpoint**.
Best where those agents are already deployed and you want no new
agent.

```

1. **Cloud-native** — programs cloud provider controls (security

```text
groups, NSGs). Best for cloud VMs.

```

2. **Kubernetes** — enforces at the container/pod layer. Best for

```text
orchestrated workloads.

```

3. **Agentless Gatekeeper** — an appliance (VM or hardware) that

```text
becomes the **default gateway** for devices that cannot take an
agent: OT, IoT, legacy, closed operating systems. Best for the
unpatchable.

```

**Walkthrough**

**Step 1.** For each lab host, decide the mode and the reason. Fill this
in yourself before reading the model answer:

| Host     | Can run an agent? | EDR present? | Correct Xshield mode | Why |
|:---------|:------------------|:-------------|:---------------------|:----|
| ct-app01 |                   |              |                      |     |
| ct-db01  |                   |              |                      |     |
| ct-win01 |                   |              |                      |     |
| ct-ot01  |                   |              |                      |     |
| ct-gw    |                   |              |                      |     |

**Step 2 — model answer:**

| Host | Can run an agent? | EDR present? | Correct Xshield mode | Why |
|:---|:---|:---|:---|:---|
| ct-app01 | Yes (Linux) | No | **Host agent** | Server you control; agent programs nftables |
| ct-db01 | Yes (Linux) | No | **Host agent** | Crown jewel; direct native-firewall enforcement |
| ct-win01 | Yes (Windows) | Possibly | **Host agent** (or **EDR** if Defender for Endpoint is deployed) | Windows workload; agent programs WFP |
| ct-ot01 | **No** | No | **Agentless Gatekeeper** | Cannot take an agent — must be fronted by the Gatekeeper |
| ct-gw | n/a (it *is* the enforcement point for OT) | n/a | Hosts the **Gatekeeper** function | Default gateway for the OT cell |

**Step 3.** State the decision rule you just applied, because you will
reuse it on every future asset:

> If the asset can take an agent and you administer it → host agent.
> Else if a supported EDR is already on it → EDR-mediated. Else if it is
> a cloud VM → cloud-native. Else if it is an orchestrated container →
> Kubernetes. Else (it cannot take an agent) → agentless Gatekeeper.

**Expected result.** A per-asset enforcement plan: agent on the three
servers, Gatekeeper for the PLC.

**Negative test.** Plan to put a host agent on `ct-ot01`. It cannot run
one — no shell, no installer, no third-party software on a real PLC.
Forcing the agent model onto OT is the classic Xshield design error; the
Gatekeeper exists precisely for this asset class. Reassign it.

**Cleanup.** None.

### Lab 6.2 — Onboard the Xshield host agent

**Objective.** Bring the three server workloads under Xshield management
— for real if you have a tenant, or by standing up the identical native
enforcement layer if you do not.

**Track 1 — Real Xshield — onboard ct-app01, ct-db01, ct-win01**

**Prerequisites recap (verify before you touch the console):**

- Administrative rights on each host — you have them (`labadmin` /
  `Administrator`).
- DNS resolution of the Xshield instance FQDN — tested in C1/C4.
- **Outbound HTTPS on TCP 443** from each host to Xshield — tested in
  C1/C4.
- **PowerShell 3.1 or later** on Windows — Server 2022 ships with 5.1,
  satisfied.
- **No competing controller of the native firewall** — no third-party
  firewall product (verified in C4 Step 31), and no GPO forcing the
  Windows firewall.

**Step 1.** Log in to your Xshield console at
`https://<your-instance>.colortokens.com`.

**Step 2.** Navigate to **Settings → Agent Download → Downloads** tab.
Agents are listed by OS flavor: Windows, macOS, Ubuntu, RedHat, CentOS,
SUSE, AIX.

**Step 3.** Note the **Product Key**. The downloaded package’s file name
contains it, and the installer uses it during installation. For agent
versions 8.7.x and later, **keep the original file name** so the key is
picked up automatically; if you rename the file you must supply the key
manually. Alternatively, use **View CLI** to copy the exact per-instance
command, which embeds your FQDN, instance name, and key.

**Step 4 — ct-app01 and ct-db01 (Ubuntu).** Copy the generated DEB and
its CLI command to each host. The instance-specific command has the
shape below; **use the one your console generates**, not this skeleton:

```bash
# Skeleton only — copy the real command with your FQDN + key from Settings > Agent Download > View CLI
sudo dpkg -i ./ct-agent_<version>_<PRODUCTKEY>_amd64.deb

```

Then confirm the agent registered:

```bash
systemctl status ctagent 2>/dev/null || systemctl status colortokens 2>/dev/null
sudo cat /var/log/colortokens/mtoken.log | tail -20     # look for successful registration

```

**Step 5 — ct-win01 (Windows).** Copy the MSI to the host. From an
**elevated** PowerShell, install with `msiexec`. Again, prefer the
console’s **View CLI** command:

```powershell
# Skeleton only - use the exact command from the console
Start-Process msiexec.exe -Wait -ArgumentList `
  '/i C:\Temp\ct-agent_<version>_<PRODUCTKEY>.msi /qn'

```

Verify:

```powershell
Get-Service -Name "*colortoken*","*ctagent*" -ErrorAction SilentlyContinue |
    Format-Table Name, Status, StartType
Get-Content "C:\ProgramData\ColorTokens\logs\mtoken.log" -Tail 20

```

**Step 6.** In the console, open **Assets**. Within a minute or two the
three hosts appear with status **Reachable**. If a host does not reach
**Reachable**, the cause is almost always one of the prerequisites —
check DNS resolution of the instance FQDN and outbound 443 first, then
the presence of a competing firewall product on Windows.

**Step 7.** Crucially, **all new assets start in Observe (simulate) mode
by default** — the agent reports flows but enforces nothing. This is the
safety property that makes agent rollout non-disruptive. Confirm each
asset shows **Observe**, not **Enforce**, in the console.

**Track 2 — Native equivalent — stand up the enforcement layer**

You will build, by hand, the artifact the agent would deploy: a
default-deny-ready nftables layer on the Linux hosts and an equivalent
WFP posture on Windows — but held in a *logging-only, still-permissive*
state that mirrors Xshield **Observe** mode. Enforcement comes in E5.

**Step 1 — ct-app01 and ct-db01.** Install a scaffold ruleset that has
the *structure* of a microsegmentation policy (named sets for peers, a
dedicated segmentation chain) but a final `accept`, so nothing is
blocked yet — the exact semantics of Observe mode.

```bash
sudo tee /etc/nftables.conf > /dev/null <<'EOF'
#!/usr/sbin/nft -f
flush ruleset

table inet xshield {
    # Named sets model Xshield "tags" / groups. Populated in E6.
    set app_tier { type ipv4_addr; }
    set db_tier  { type ipv4_addr; }
    set hmi      { type ipv4_addr; }

    chain input {
        type filter hook input priority 0; policy accept;
        ct state established,related accept
        iif "lo" accept

        # --- SEGMENTATION CHAIN (OBSERVE MODE) ---
        # We LOG what a default-deny policy WOULD drop, but still accept.
        # This is exactly what Xshield Observe mode does: report, do not block.
        jump segmentation
    }

    chain segmentation {
        # In E5 we flip the trailing 'accept' to 'drop' to move to Enforce.
        # For now: log-and-allow, so we can gather the flow map first.
        log prefix "XSHIELD-OBSERVE: " level info
        accept
    }
}
EOF
sudo nft -f /etc/nftables.conf
sudo systemctl enable --now nftables

```

Confirm Observe-mode logging is active without blocking anything:

```bash
sudo nft list table inet xshield
~/reach.sh          # still all REACH - Observe mode blocks nothing

```

**Step 2 — ct-win01.** Put the Windows firewall into the equivalent
posture: enabled, logging allowed and dropped packets, but default
actions left permissive so nothing breaks yet.

```powershell
# Turn on logging for both allowed and dropped connections (Observe-style telemetry)
Set-NetFirewallProfile -Profile Domain,Private,Public `
    -LogAllowed True -LogBlocked True `
    -LogFileName "%SystemRoot%\System32\LogFiles\Firewall\pfirewall.log" `
    -LogMaxSizeKilobytes 8192

# Keep default actions permissive for now (this is 'Observe')
Set-NetFirewallProfile -Profile Domain,Private,Public `
    -DefaultInboundAction Allow -DefaultOutboundAction Allow

Get-NetFirewallProfile | Format-Table Name, Enabled, DefaultInboundAction, LogBlocked, LogAllowed

```

**Step 3.** Record the mapping so the analogy is explicit and you never
lose the thread:

| Xshield concept | Track 2 native artifact |
|:---|:---|
| Host agent | nftables service / Windows Filtering Platform |
| Asset “Reachable” | nftables loaded / firewall profile enabled |
| Observe mode | segmentation chain ends in `accept` + `log`; WFP default Allow + logging |
| Enforce mode (Lab 7.1) | segmentation chain ends in `drop`; WFP default Block |
| Tag / group | nftables named `set`; Windows firewall rule `-RemoteAddress` groups |
| Policy rule | nftables rule / `New-NetFirewallRule` |

**Expected result.** Three workloads under management — actually
enrolled (Track 1) or carrying the equivalent enforcement layer in
Observe posture (Track 2) — with nothing yet blocked. `~/reach.sh` still
shows all `REACH`, exactly as Observe mode should.

**Negative test.** On Windows, set a Group Policy that enforces the
firewall to a conflicting state, or install a third-party firewall, then
observe (Track 1) the asset failing to apply policy, or (Track 2) your
`Set-NetFirewallProfile` changes being reverted by GPO on refresh. This
is the documented Xshield Windows prerequisite — a single controller of
the native firewall — made tangible.

**Cleanup.** Leave the Observe layer in place; E3–E6 build on it.

### Lab 6.3 — Discover and visualize traffic (the flow map)

**Objective.** Use the discovery phase of Progressive Segmentation: see
what actually talks to what, before writing a single rule. You cannot
segment what you cannot see.

**Track 1 — Real Xshield**

**Step 1.** Generate representative traffic so the map has something to
show. From `ct-app01`, exercise the legitimate flow a few times:

```bash
for i in $(seq 1 5); do
  PGPASSWORD='LabAppPassw0rd!' psql -h 10.10.20.12 -U appuser -d ctlab \
    -c "SELECT count(*) FROM customers;" >/dev/null
done

```

From `ct-win01`, poll the PLC a few times (Step from D2). And, to
represent the *unwanted* traffic the map must reveal, run the D3
lateral-movement sweep again.

**Step 2.** In the console, open **Visualize** (the traffic/flow map).
Set the time window to the last hour. You will see nodes for each asset
and directed edges for observed flows, typically color-coded by whether
a policy would allow or deny them.

**Step 3.** Identify, on the map, the two legitimate flows (app→db 5432,
hmi→plc 502) and the unwanted ones (win01→db 5432, win01→ot 502,
app01→win01, etc.). The map is where you *find* the ring-fence boundary
rather than guessing it.

**Step 4.** Optionally invoke the **Xshield AI Agent** (introduced March
2026) to propose a policy from observed flows. Treat its output as a
first draft to review, never as something to apply blind.

**Track 2 — Native equivalent — build your own flow map**

Xshield’s map is drawn from agent-reported flow telemetry. You will
collect the same telemetry with `conntrack` and the firewall logs, then
render it.

**Step 1.** On `ct-gw` — the choke point every east-west and
cross-segment flow crosses — install and watch connection tracking:

```bash
sudo apt -y install conntrack

```

**Step 2.** Generate the same traffic as Track 1: run the legitimate
app→db loop on `ct-app01`, poll the PLC from `ct-win01`, and re-run the
D3 attack sweep.

**Step 3.** On `ct-gw`, harvest the live flow table into a simple edge
list — your flow map as data:

```bash
sudo conntrack -L 2>/dev/null \
  | grep -oE 'src=10\.[0-9.]+ dst=10\.[0-9.]+ sport=[0-9]+ dport=[0-9]+' \
  | awk '{gsub("src=|dst=|dport=","");
          split($1,s,"."); print $2" -> "$4" :dport "$0}' \
  | sed -E 's/ sport=[0-9]+//' \
  | sort -u

```

For a cleaner, deduplicated “who talks to whom on which port” view:

```bash
sudo conntrack -L 2>/dev/null \
  | sed -nE 's/.*src=([0-9.]+) dst=([0-9.]+) sport=[0-9]+ dport=([0-9]+).*/\1 -> \2 :\3/p' \
  | sort | uniq -c | sort -rn

```

Expected — the map reveals both the legitimate and the illegitimate
edges, for example:

```text
   5 10.10.20.11 -> 10.10.20.12 :5432     legitimate  app -> db
   3 10.10.20.21 -> 10.10.30.50 :502      legitimate  hmi -> plc
   1 10.10.20.21 -> 10.10.20.12 :5432     UNWANTED    win -> db  (lateral movement!)
   1 10.10.20.21 -> 10.10.30.50 :502      (also seen from the attack sweep)

```

**Step 4.** Render it visually if you like — pipe the edge list into a
Graphviz DOT file on the host and open it. This is optional but drives
home that a “flow map” is just an edge list with layout:

```bash
sudo conntrack -L 2>/dev/null \
  | sed -nE 's/.*src=([0-9.]+) dst=([0-9.]+) sport=[0-9]+ dport=([0-9]+).*/  "\1" -> "\2" [label="\3"];/p' \
  | sort -u > ~/flowmap.dot
echo 'digraph flows {' | cat - ~/flowmap.dot > ~/flowmap.full.dot && echo '}' >> ~/flowmap.full.dot
cat ~/flowmap.full.dot

```

**Expected result.** A concrete flow map — visual (Track 1) or as an
edge list/DOT graph (Track 2) — that distinguishes the two legitimate
flows from the unwanted lateral-movement flows. You now know exactly
where the ring-fence boundary must sit.

**Negative test.** Try to design a policy *without* the map — from
memory of the topology alone. You will either forget the legitimate
app→db flow (and break the app in E5) or miss an unwanted flow (and
leave a hole). Discovery-before-policy is not ceremony; skipping it is
how real rollouts cause outages.

**Cleanup.** None — keep the map as your policy specification.

### Lab 6.4 — Ring-fence the application (Progressive Segmentation, phase 1)

**Objective.** Draw the first, coarse boundary: allow the two-tier
application to talk internally, deny lateral reach into it from
everything else. Ring-fencing before micro-rules is the ColorTokens
method — contain first, refine later.

**Track 1 — Real Xshield**

**Step 1.** In the console, create a **Group** (a.k.a. application group
/ named group) called `app-ctlab` containing `ct-app01` and `ct-db01`.

**Step 2.** Author a ring-fence policy: - **Intra-group:** allow all
traffic *within* `app-ctlab` (app↔db). - **Ingress:** deny traffic
*into* `app-ctlab` from outside, except the flows you explicitly need
(there are none from outside for this app — the HMI talks to the PLC,
not the app).

**Step 3.** Keep the policy in **Observe** mode. The console will show,
in simulation, which flows the policy *would* deny — critically
including the D3 attack flow win01→db. Verify the simulation denies the
attack and permits app→db before you enforce anything.

**Track 2 — Native equivalent**

You will ring-fence `ct-db01` (the asset most worth protecting) by
populating the tag sets and writing rules that permit only the app tier
— but still in Observe posture, logging what *would* be denied.

**Step 1.** On `ct-db01`, rewrite the ruleset with the ring-fence
expressed, but the segmentation chain still ending in log-and-accept
(Observe):

```bash
sudo tee /etc/nftables.conf > /dev/null <<'EOF'
#!/usr/sbin/nft -f
flush ruleset

define DB_PORT = 5432

table inet xshield {
    set app_tier {
        type ipv4_addr
        elements = { 10.10.20.11 }        # ct-app01 — the ONLY legitimate db client
    }

    chain input {
        type filter hook input priority 0; policy accept;
        ct state established,related accept
        iif "lo" accept
        tcp dport 22 accept                # keep management SSH (break-glass)
        jump segmentation
    }

    chain segmentation {
        # Legitimate: app tier -> database port. Allowed and NOT flagged.
        ip saddr @app_tier tcp dport $DB_PORT accept

        # Everything else to the DB port is UNWANTED. In Observe we log-and-allow.
        tcp dport $DB_PORT log prefix "XSHIELD-WOULD-DENY db: " level warn accept

        accept
    }
}
EOF
sudo nft -f /etc/nftables.conf

```

**Step 2.** Watch the Observe-mode telemetry while you reproduce the
attack. On `ct-db01`:

```bash
sudo journalctl -kf | grep "XSHIELD-WOULD-DENY" &

```

**Step 3.** From `ct-win01` (the attacker), hit the database again:

```powershell
Test-NetConnection -ComputerName 10.10.20.12 -Port 5432

```

Expected on `ct-db01`’s log stream — the policy *reports* the violation
but has not yet blocked it:

```text
XSHIELD-WOULD-DENY db: IN=ens34 SRC=10.10.20.21 DST=10.10.20.12 ... DPT=5432

```

**Step 4.** Confirm the legitimate flow generates **no** would-deny log.
From `ct-app01`:

```text
PGPASSWORD='LabAppPassw0rd!' psql -h 10.10.20.12 -U appuser -d ctlab -c "SELECT 1;" >/dev/null

```

No new `XSHIELD-WOULD-DENY` line appears — proof your ring-fence permits
the app and would deny the attacker. Stop the background log tail with
`kill %1`.

**Expected result.** A ring-fence around the database that, in
simulation/Observe, permits app→db and flags win01→db as a would-be
denial — validated *before* any traffic is actually blocked.

**Negative test.** Add `10.10.20.21` to the `app_tier` set “just to be
safe,” reload, and re-run the attack. The would-deny log goes silent —
you have just re-authorized the exact lateral movement you set out to
stop. Over-broad groups are the most common way a real policy quietly
fails. Remove it.

**Cleanup.** Keep the ring-fence; E5 enforces it.

## Summary and Completion Checklist

- [ ] Lab 6.1 complete, including its negative test.
- [ ] Lab 6.2 complete, including its negative test.
- [ ] Lab 6.3 complete, including its negative test.
- [ ] Lab 6.4 complete, including its negative test.
