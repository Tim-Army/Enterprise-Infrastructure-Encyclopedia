# Chapter 09: Operations, Troubleshooting, and Teardown

## Learning Objectives

- Diagnose the failures that account for most segmentation tickets.
- Execute a break-glass rollback by four independent mechanisms.
- Tear the lab down and restore every host security control you relaxed.

## Hands-On Lab

### Lab 9.1 — The Xshield troubleshooting playbook

**Objective.** Build the diagnostic reflexes for the failures you will
actually hit — on the real product and on the native equivalent.

**Walkthrough — the five failures that account for most tickets**

**Failure 1 — Agent will not enrol / asset never becomes “Reachable”
(Track 1).** Cause, in order of likelihood: DNS cannot resolve the
instance FQDN; outbound 443 to Xshield is blocked; a competing firewall
product on Windows; a proxy in the path. Diagnose:

```powershell
# Linux
resolvectl query <your-instance>.colortokens.com
curl -sSI https://<your-instance>.colortokens.com | head -1
sudo tail -50 /var/log/colortokens/mtoken.log
# Windows
Resolve-DnsName <your-instance>.colortokens.com
Test-NetConnection <your-instance>.colortokens.com -Port 443
Get-Content "C:\ProgramData\ColorTokens\logs\mtoken.log" -Tail 50
Get-CimInstance -Namespace root\SecurityCenter2 -ClassName FirewallProduct

```

**Failure 2 — Legitimate app broke after Enforce.** You omitted an allow
rule. This is why Observe exists. Diagnose on the destination host:

```bash
sudo journalctl -k | grep "ENFORCE-DROP" | tail -20   # what got dropped and from where

```

The dropped `SRC`/`DPT` tells you the flow you forgot. Add the allow, or
revert to Observe, fix, re-enforce.

**Failure 3 — Attack still succeeds after Enforce.** Usually an
over-broad tag/group (you added the wrong member) or a rule ordering
problem (an early accept shadows the drop). Diagnose:

```bash
sudo nft list ruleset | less     # read top-to-bottom; first match wins per chain
sudo nft list set inet xshield app_tier   # is an attacker's IP wrongly a member?

```

**Failure 4 — OT device unreachable / plant flow broken (Gatekeeper).**
The one legitimate flow is denied — wrong port, wrong source, or
forwarding disabled. Diagnose on `ct-gw`:

```bash
sysctl net.ipv4.ip_forward           # must be 1
sudo nft list chain inet filter forward
sudo journalctl -kf | grep GATEKEEPER-DROP   # is the HMI flow being dropped?

```

**Failure 5 — “It’s slow” on the Windows host.** Not a policy problem —
the VBS/ULM performance mode from Lab 2.2. Verify:

```powershell
Get-CimInstance -Namespace root\Microsoft\Windows\DeviceGuard -ClassName Win32_DeviceGuard |
    Select VirtualizationBasedSecurityStatus

```

**Expected result.** A repeatable, five-check diagnostic routine
covering enrolment, over-tight policy, under-tight policy, OT flow
breakage, and host performance.

**Negative test.** Try to diagnose a dropped flow with no logging
enabled. You are blind — which is why E2 turned on `log`/`LogBlocked`
from the start. Observability is a prerequisite for troubleshooting, not
an afterthought.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 9.2 — Break-glass rollback

**Objective.** Know, cold, how to restore connectivity in seconds when a
policy locks something out — the skill that makes enforcing policy in
production psychologically possible.

**Walkthrough**

**Step 1 — the fastest rollback: management path.** Recall from section
1.2 that VMnet2 keeps a host adapter at `10.10.20.1`. That path
deliberately survives your policies. From the Windows host you can
always reach the Data Center hosts on it to fix a bad rule, even if
east-west is fully denied. Verify it is your lifeline:

```powershell
Test-NetConnection -ComputerName 10.10.20.12 -Port 22   # management SSH survives

```

**Step 2 — per-host revert (nftables).** On any Linux host, drop back to
accept-all in one command:

```bash
sudo nft flush ruleset          # instant: removes all policy
# then reload the intended good config once you have fixed it:
sudo nft -f /etc/nftables.conf

```

**Step 3 — per-host revert (Windows).** Remove the Xshield-group rules
or reset the firewall:

```powershell
Get-NetFirewallRule -Group "Xshield" | Remove-NetFirewallRule       # targeted
# or, nuclear:
netsh advfirewall reset

```

**Step 4 — whole-VM revert (snapshot).** The ultimate break-glass, and
why you snapshotted every VM: **VM → Snapshot → Revert to Snapshot →**
the relevant `Cx-base-*`. Thirty seconds to a known-good state.

**Step 5 — Gatekeeper revert.** On `ct-gw`, the OT policy is on the
forward chain; restoring `C1-base-router` or reloading the permissive
Part C ruleset reopens transit immediately.

**Step 6 — real Xshield break-glass (Track 1).** In the console, move
the affected asset/policy from **Enforce** back to **Observe** —
enforcement stops immediately without uninstalling anything. This is the
product’s equivalent of `nft flush`, and it is why Observe/Enforce is a
reversible state, not a one-way deployment.

**Expected result.** Four independent rollback mechanisms — management
path, per-host flush, snapshot revert, and Observe-mode fallback — any
of which restores service fast.

**Negative test.** Enforce a policy on a host you can only reach
*through* the path that policy blocks, with no management path and no
snapshot. You have locked yourself out and must use the VM console
directly. This is the production nightmare that the retained management
path (Chapter 01 (Topology)) and the Observe-first discipline exist to prevent.
Never enforce without a break-glass.

**Rollback.** Reapply your intended policies after testing rollback.

### Lab 9.3 — Full teardown and host restoration

**Objective.** Cleanly remove the lab and, importantly, restore any host
security controls you disabled in Part A.

**Walkthrough**

**Step 1.** Power off all five VMs cleanly (`sudo shutdown -h now` on
Linux; Start → shut down on Windows).

**Step 2.** Remove the VMs from Workstation and delete their files. In
the library, right-click each VM → **Manage → Delete from Disk**.
Confirm the `D:\VMs\ColorTokens-Lab\` folder is emptied.

**Step 3.** Remove the custom virtual networks if you want the host back
to stock. In the elevated Virtual Network Editor, select **VMnet2** and
**VMnet3** and click **Remove Network**. Leave VMnet8 (NAT) and VMnet1
(host-only) — those are Workstation defaults.

**Step 4.** Remove the host route added in B4:

```powershell
Remove-NetRoute -DestinationPrefix "10.10.30.0/24" -Confirm:$false -PolicyStore PersistentStore

```

**Step 5 — the important one: restore host security.** If you disabled
VBS/Memory Integrity in Lab 2.2, put it back — especially on any
machine you use for real work:

```powershell
bcdedit /set hypervisorlaunchtype auto
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V-All -NoRestart
Enable-WindowsOptionalFeature -Online -FeatureName HypervisorPlatform     -NoRestart
Enable-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform -NoRestart
Restart-Computer

```

After reboot, re-enable **Memory Integrity** in **Windows Security →
Device security → Core isolation**, and verify:

```powershell
Get-CimInstance -Namespace root\Microsoft\Windows\DeviceGuard -ClassName Win32_DeviceGuard |
    Select VirtualizationBasedSecurityStatus     # expect 2 (running) again

```

**Step 6.** Optionally uninstall VMware Workstation via **Settings →
Apps → Installed apps** if you are finished entirely.

**Expected result.** The lab is fully removed and — critically — every
security control you relaxed for the lab is restored. Leaving VBS off on
a work machine after a lab is a real, common mistake; this step closes
it.

**Negative test.** Finish the lab, forget Step 5, and leave Memory
Integrity disabled on your daily driver for months. You have traded a
permanent reduction in your own host’s security for a lab that ended
weeks ago. Restore it.

**Rollback.** This exercise *is* the cleanup.

## Appendix A — Consolidated command reference

**Host (Windows 11) — networking**

```powershell
Get-NetIPAddress -AddressFamily IPv4 | Where InterfaceAlias -like "*VMnet*" |
    Format-Table InterfaceAlias, IPAddress, PrefixLength
New-NetRoute -DestinationPrefix "10.10.30.0/24" -NextHop "10.10.20.254" `
    -InterfaceAlias "VMware Network Adapter VMnet2" -PolicyStore PersistentStore
Get-Service "VMware*" | Format-Table Name, Status, StartType

```

**Linux guests — segmentation**

```bash
sudo nft list ruleset                       # read the whole policy
sudo nft -c -f /etc/nftables.conf           # syntax-check before load
sudo nft -f /etc/nftables.conf              # load
sudo nft flush ruleset                      # BREAK-GLASS: remove all policy
sudo nft add element inet xshield app_tier { 10.10.20.13 }   # tag membership
sudo journalctl -kf | grep -E "XSHIELD|GATEKEEPER"           # watch drops
sudo conntrack -L                           # live flow map source

```

**Windows guest — WFP enforcement**

```powershell
New-NetFirewallRule -DisplayName "..." -Direction Outbound -Action Block `
    -RemoteAddress 10.10.20.12 -Protocol TCP -Group "Xshield"
Get-NetFirewallRule -Group "Xshield" | Format-Table DisplayName, Direction, Action, Enabled
Get-NetFirewallRule -Group "Xshield" | Remove-NetFirewallRule           # break-glass
netsh wfp show filters file="C:\Temp\wfp.xml"
Set-NetFirewallProfile -All -LogBlocked True -LogAllowed True

```

**Real Xshield console (Track 1) — where things live**

| Task | Console location |
|:---|:---|
| Download agent / get Product Key / View CLI | Settings → Agent Download → Downloads |
| See assets and Reachable status | Assets |
| Flow map | Visualize |
| Tags / groups | Asset properties; Groups |
| Observe ↔ Enforce | Asset/policy state toggle |
| Gatekeeper | Gatekeepers / appliance management |

## Appendix B — The Xshield concept ↔ lab artifact map

| Xshield concept | This lab’s Track-2 realization | Exercise |
|:---|:---|:---|
| Host agent (Linux) | `nftables` service | E2, E4, E5 |
| Host agent (Windows) | Windows Filtering Platform via `NetSecurity` / `netsh` | E2, E7 |
| EDR-mediated mode | Design exercise (needs licensed EDR) | E8 |
| Agentless Gatekeeper | `ct-gw` forward-chain policy; default gateway for VMnet3 | F1, F2 |
| Cloud-native mode | Out of lab scope (no cloud) | — |
| Kubernetes mode | Out of lab scope (no cluster) | — |
| Asset / Reachable | Loaded ruleset / enabled firewall profile | E2 |
| Tag / group | nftables named `set`; `-RemoteAddress` groups | E6 |
| Flow map (Visualize) | `conntrack` + firewall logs → edge list / DOT | E3 |
| Observe (simulate) mode | segmentation chain `log … accept`; WFP default Allow + logging | E2, E4 |
| Enforce mode | segmentation chain `log … drop`; WFP default Block | E5, F2 |
| Progressive Segmentation | discover (Lab 6.3) → ring-fence (Lab 6.4) → tighten (Lab 7.2) | E3–E6 |
| Break-glass | `nft flush`, snapshot revert, mgmt path, Observe fallback | G2 |

## Appendix C — Xshield facts used in this lab

The exercises rely on these product characteristics. Verify current
specifics against ColorTokens’ official documentation before any
production decision — product details change.

- **Five enforcement modes:** host agent (programs native OS firewall —
  `iptables`/`nftables` on Linux, Windows Filtering Platform on
  Windows); EDR-mediated (**CrowdStrike, SentinelOne, Microsoft Defender
  for Endpoint**); cloud-native; Kubernetes; **agentless Gatekeeper**
  appliance (VM or hardware) for OT/IoT/legacy.
- **Host-agent footprint:** lightweight — on the order of under 1% CPU
  and under ~100 MB RAM.
- **Agent prerequisites:** administrative rights; DNS resolution of the
  Xshield instance FQDN; **outbound HTTPS on TCP 443** to Xshield;
  **PowerShell 3.1+** on Windows; **no competing controller of the
  native firewall** (no third-party firewall product, no conflicting GPO
  — these must be disabled).
- **Agent download:** console **Settings → Agent Download**; the package
  file name embeds the **Product Key**; keep the original file name for
  agent 8.7.x+ so the key is auto-applied; **View CLI** yields the exact
  per-instance command (FQDN + key).
- **Method:** **Progressive Segmentation** — discover → visualize →
  ring-fence → tighten.
- **Lifecycle:** assets start in **Observe (simulate)** mode and report
  flows without blocking; you move to **Enforce** as a reversible state
  change.
- **Gatekeeper:** deployed as a data-center VM or a shop-floor hardware
  device; becomes the **default gateway** for the devices it protects so
  all their traffic traverses it; enforces on agentless OT/IoT/legacy.
- **Xshield AI Agent:** introduced March 2026; proposes policy from
  observed flows (review before applying).
- **Compliance:** Xshield achieved **FedRAMP Moderate** authorization
  (January 2025).

## Appendix D — Pre-flight checklist

Check before starting each part.

**Before Part A (Chapter 02)**

- [ ] Windows 11 Education, current build
- [ ] 16 GB+ RAM, 4+ cores, 250 GB+ free
- [ ] All ISOs and the Workstation installer downloaded and checksummed

**Before Part C (Chapter 04)**

- [ ] VT-x/AMD-V enabled in firmware (Lab 2.1)
- [ ] Conscious VBS decision made and documented (Lab 2.2)
- [ ] Workstation 17.6.3 installed, licensed-for-free (Lab 2.3)
- [ ] VMnet2 (host-only, no DHCP, 10.10.20.0/24) and VMnet3 (host-only, NO host
  adapter, no DHCP, 10.10.30.0/24) created (Labs 3.2 and 3.3)

**Before Part D (Chapter 05)**

- [ ] All five VMs built with correct static addresses (Labs 4.1–4.5)
- [ ] Baseline snapshots taken on all five (Lab 4.6)
- [ ] Reachability matrix all-UP from ct-gw (Lab 4.6)

**Before Part E (Chapter 06)**

- [ ] Flat-network attack reproduced and documented (Labs 5.1–5.3)
- [ ] Legitimate flow allow-list written down (Lab 5.2)

**Before Part F (Chapter 08)**

- [ ] Database ring-fence enforced and validated (Lab 7.1)
- [ ] Gatekeeper choke point confirmed — no host adapter on VMnet3 (Lab 8.1)

**On completion**

- [ ] Host VBS/Memory Integrity restored if disabled (Lab 9.3)
- [ ] Break-glass rehearsed at least once (Lab 9.2)

## Summary and Completion Checklist

- [ ] Lab 9.1 complete, including its negative test.
- [ ] Lab 9.2 complete, including its negative test.
- [ ] Lab 9.3 complete, including its negative test.
