# Chapter 01: Lab Overview and Topology

## Learning Objectives

- State what this lab builds and the two tracks it is written on (real Xshield tenant, native equivalent).
- Read the topology, address plan, and resource budget for the five-VM estate.
- Assemble the bill of materials before starting.
- Explain why the OT segment deliberately has no host adapter.

## How to Use This Guide

### What this lab is

This is a self-contained, build-it-yourself microsegmentation lab. You
will construct a five–virtual-machine enterprise in miniature on a
single Windows 11 Education laptop or desktop, deliberately break it to
prove that a flat network lets an attacker move sideways, and then apply
ColorTokens Xshield microsegmentation concepts to contain that movement.

The estate you build is intentionally heterogeneous, because that
heterogeneity is the whole reason Xshield exists as a product. You will
end up with modern Linux servers, a Windows server, and an unpatchable
“programmable logic controller” that cannot accept a security agent —
the exact mix that forces an architect to choose a different enforcement
mode per asset.

### An honest scope note — please read this before you start

ColorTokens Xshield is commercial software delivered as a SaaS console.
Two consequences shape this lab, and it is better that you know them on
page one than discover them at exercise fourteen:

1. **There is no public download or self-service trial of the Xshield

```text
agent.** The agent installer is generated per tenant. Its file name
embeds a **Product Key**, and the command line embeds your instance
FQDN. You obtain both from **Settings → Agent Download** inside a
console you have been granted. Nothing on the public internet
substitutes for that.

```

2. **The Xshield console cannot be run locally.** It is multi-tenant

```text
SaaS. There is no on-premises appliance version of the management
plane to import into Workstation.

```

Therefore every exercise in Part E and Part F is written on **two
tracks**:

- **Track 1 — Real Xshield.** The exact console navigation, the real
  agent commands, and the real verification points. Follow this if your
  employer, partner account, or a ColorTokens evaluation has given you a
  tenant. Where a value is tenant-specific, it appears as a placeholder
  such as `<your-instance>.colortokens.com` and the guide tells you
  precisely where in the console to find it.
- **Track 2 — Native equivalent.** A faithful reproduction you can run
  today with no tenant at all, driving the *same underlying enforcement
  primitives the Xshield agent drives*: `nftables` and `iptables` on
  Linux, and the Windows Filtering Platform, reached through
  `netsh advfirewall` and the `NetSecurity` PowerShell module, on
  Windows.

Track 2 is not a cartoon of the product. The ColorTokens host agent does
not invent a packet filter; it programs the native OS firewall. When you
write an nftables rule that permits `ct-app01 → ct-db01` on TCP 5432 and
drops everything else, you are hand-writing the artifact that Xshield’s
policy compiler would have generated for you. The management plane, the
flow-map visualization, the tag algebra, and the policy lifecycle are
what you are buying; the enforcement primitive is the one you can
practice on for free. Knowing exactly what lands on the host makes you
far better at operating the product, and much faster at troubleshooting
it, than someone who has only ever clicked the console.

Exercises that genuinely cannot be reproduced without the product — the
flow map, the AI policy assistant, EDR-mediated enforcement — are marked
****Design Exercise**** and are structured as written analysis with a
model answer, not as pretend clicking.

### Conventions

| Convention | Meaning |
|:---|:---|
| `PS C:\>` | Run on the **Windows 11 host**, in an **elevated** PowerShell |
| `PS C:\Users\Administrator>` | Run inside the **ct-win01** guest VM, elevated |
| `user@ct-gw:~$` | Run inside the named Linux guest as a normal user |
| `#` prefix in a Linux block | Command requires `sudo` / root |
| `<angle brackets>` | A value you must substitute from your own environment |
| ****Design Exercise**** | No tenant required and none simulated; written analysis with model answer |
| ****Track 1**** / ****Track 2**** | Real Xshield path / native-equivalent path |

Every exercise follows the same five-part shape: **Objective**,
**Walkthrough**, **Expected result**, **Negative test**, **Cleanup**. Do
not skip the negative tests. In segmentation work, proving that a thing
is *blocked* is the entire product; proving that a thing is allowed only
proves you have a network.

### Time and effort

| Part | Content | Approximate time |
|:---|:---|:---|
| A | Host preparation and Workstation install | 45–90 min |
| B | Virtual network construction | 20 min |
| C | Building the five VMs | 3–4 hours (mostly unattended installs) |
| D | Baseline application and the flat-network attack | 45 min |
| E | Xshield agent, visibility, tagging, and policy | 3–4 hours |
| F | Gatekeeper and agentless OT segmentation | 90 min |
| G | Operations, troubleshooting, teardown | 45 min |

Budget two comfortable days, or four evenings. Part C is the long pole
and is largely waiting.

## Lab Overview

### Learning objectives

By the end of this lab you will be able to:

1. Explain Xshield’s five enforcement modes — host agent, EDR-mediated,

```text
cloud-native, Kubernetes, and the agentless Gatekeeper appliance —
and **choose the correct one per asset**.

```

2. Describe precisely what the Xshield host agent does to a Linux host

```text
(`iptables`/`nftables`) and to a Windows host (Windows Filtering
Platform), and verify it from the operating system.

```

3. Satisfy the real agent prerequisites: administrative rights, DNS

```text
resolution, outbound HTTPS on 443, PowerShell 3.1 or later, and the
removal of competing controllers of the native firewall.

```

4. Execute the **Progressive Segmentation** method: discover,

```text
visualize, ring-fence, tighten.

```

5. Distinguish **Observe** (simulate) mode from **Enforce** mode, and

```text
use Observe as the safety net it is designed to be.

```

6. Design and validate a **ring-fence** around a two-tier application,

```text
then tighten it to per-service rules.

```

7. Protect a device that **cannot run an agent** by placing a

```text
Gatekeeper-equivalent in front of it as its default gateway, and
default-deny everything else.

```

8. Diagnose the common failure modes and execute a break-glass

```text
rollback.

```

### Topology

Three isolated Layer 2 segments, joined by a single multi-homed Linux
router that doubles as the Gatekeeper-equivalent for the OT cell.

![Lab topology: the Windows 11 host, three VMware virtual networks (VMnet8 NAT “IT/Corporate”, VMnet2 host-only “Data Center”, VMnet3 host-only “OT Cell”), the five virtual machines, and the legitimate versus lateral-movement flows. ct-gw is the sole path between segments and the enforcement choke point for the OT cell.](../../../diagrams/volume-093-colortokens-xshield-lab/chapter-01-lab-topology.svg)

*Figure 1-1. The five-VM IT/OT estate this lab builds: host agents on the Data Center servers, the agentless Gatekeeper (ct-gw) fronting the isolated Modbus PLC, the two legitimate east-west flows allowed, and the compromised-HMI-to-database lateral movement denied.*

A text-only rendering of the same topology follows for reference:

```text
                    ┌──────────────────────────────────────────────┐
                    │   Windows 11 Education host                  │
                    │   VMware Workstation Pro 17.6.3              │
                    │   Roles: admin console + "IT laptop"         │
                    │          (the untrusted lateral-movement     │
                    │           source in Lab 5.3)             │
                    └───┬───────────────────────┬──────────────────┘
                        │ 192.168.170.1         │ 10.10.20.1
                        │ (host vNIC)           │ (host vNIC)
  ══════════════════════╪═══════════════        │
   VMnet8  NAT — "IT / Corporate"               │
   192.168.170.0/24   NAT gw .2                 │
                        │                       │
                  ┌─────┴──────┐                │
                  │  ct-gw     │ .10            │
                  │  Ubuntu    │                │
                  │  22.04     │                │
                  │            │                │
                  │  router +  │ .254           │
                  │ GATEKEEPER ├────────────────┴═══════════════════
                  │ equivalent │   VMnet2  Host-only — "Data Center"
                  │            │   10.10.20.0/24     (no DHCP)
                  │            │        │         │          │
                  │            │   ┌────┴───┐ ┌───┴────┐ ┌───┴─────┐
                  │            │   │ct-app01│ │ct-db01 │ │ct-win01 │
                  │            │   │  .11   │ │  .12   │ │  .21    │
                  │            │   │ nginx  │ │postgres│ │ Win2022 │
                  │            │   │  :80   │ │ :5432  │ │SCADA/HMI│
                  │            │   └────────┘ └────────┘ └─────────┘
                  │            │ .254
                  └─────┬──────┘
  ════════════════════════════════════════════════
   VMnet3  Host-only — "OT Cell"  10.10.30.0/24
   NO host adapter. NO DHCP. Fully isolated.
   Reachable ONLY through ct-gw = the Gatekeeper.
                        │
                  ┌─────┴──────┐
                  │  ct-ot01   │ .50
                  │  "PLC"     │
                  │  Modbus    │
                  │  TCP :502  │
                  │  AGENTLESS │
                  └────────────┘

```

The design choices here are deliberate and each teaches something:

- **VMnet3 has no host virtual adapter.** The Windows host has no Layer
  2 presence in the OT cell. The only way a packet reaches the PLC is
  through `ct-gw`. That is exactly the physical property a real
  Gatekeeper appliance relies on, and it is why “make the Gatekeeper the
  default gateway” is the deployment instruction rather than a
  suggestion.
- **VMnet2 does have a host virtual adapter (10.10.20.1).** This is your
  out-of-band management path. It deliberately survives every policy you
  write. Real segmentation deployments always retain a management
  channel, and the discipline of *knowing* which path is your
  break-glass — rather than discovering it under pressure — is worth
  practising. Lab 9.2 uses it.
- `ct-gw` **is the default gateway for the Data Center segment as
  well.** All east-west traffic between segments and all egress
  traverses it, so you can observe flows at a choke point before you
  ever install an agent. This mirrors how most organizations start:
  netflow at the router, long before agents.

### Address plan

Commit this table to a sticky note. Almost every troubleshooting session
in this lab ends at it.

| Host | Role | VMnet8 — IT/NAT | VMnet2 — Data Center | VMnet3 — OT Cell |
|:---|:---|:---|:---|:---|
| Windows 11 host | Admin console; “IT laptop” | 192.168.170.1 | 10.10.20.1 | *(none — by design)* |
| VMware NAT service | NAT gateway | 192.168.170.2 | — | — |
| **ct-gw** | Router; Gatekeeper-equivalent | 192.168.170.10 | 10.10.20.254 | 10.10.30.254 |
| **ct-app01** | Web/app tier, nginx :80 | — | 10.10.20.11 | — |
| **ct-db01** | PostgreSQL :5432 | — | 10.10.20.12 | — |
| **ct-win01** | Windows workload; SCADA/HMI | — | 10.10.20.21 | — |
| **ct-ot01** | “PLC”, Modbus TCP :502, agentless | — | — | 10.10.30.50 |

DNS for all guests: `192.168.170.2` (the VMware NAT service forwards to
your host’s resolvers). This matters more than it looks — the Xshield
agent must resolve its instance FQDN or it will never enrol, and DNS is
the single most common cause of a stuck agent.

### Resource budget

| VM       | Guest OS                   | vCPU  | RAM         | Disk        | Runs during |
|:---------|:---------------------------|:------|:------------|:------------|:------------|
| ct-gw    | Ubuntu Server 22.04.5 LTS  | 1     | 1024 MB     | 20 GB       | All parts   |
| ct-app01 | Ubuntu Server 22.04.5 LTS  | 1     | 1536 MB     | 20 GB       | D, E, G     |
| ct-db01  | Ubuntu Server 22.04.5 LTS  | 1     | 1536 MB     | 20 GB       | D, E, G     |
| ct-win01 | Windows Server 2022 (Eval) | 2     | 4096 MB     | 60 GB       | E, F, G     |
| ct-ot01  | Ubuntu Server 22.04.5 LTS  | 1     | 768 MB      | 10 GB       | D, F, G     |
|          | **Peak concurrent**        | **6** | **~8.9 GB** | **~130 GB** |             |

**Host minimum:** 4 physical cores, 16 GB RAM, 250 GB free SSD. **Host
comfortable:** 8 cores, 32 GB RAM, 400 GB free NVMe.

On a 16 GB host, do not run all five at once during Part C. Build and
shut down each VM in turn. From Part D onward, all five running
simultaneously fits inside 16 GB with roughly 6 GB left for Windows 11 —
tight but workable. If your host has 8 GB, this lab is not comfortable;
reduce ct-win01 to 3072 MB and expect swapping, or substitute Ubuntu
Desktop for ct-win01 and skip the Windows Filtering Platform exercises
(Labs 7.3 and 7.4) at real cost to the learning.

### Bill of materials

Download everything before you begin. Total download is roughly 8 GB.

| Item | Where | Size | Notes |
|:---|:---|:---|:---|
| VMware Workstation Pro 17.6.3 for Windows | Broadcom Support Portal | ~600 MB | **Free**, no license key, for commercial, educational, and personal use. Requires a free Broadcom account. |
| Ubuntu Server 22.04.5 LTS ISO | `releases.ubuntu.com/jammy/` | ~2.0 GB | File: `ubuntu-22.04.5-live-server-amd64.iso` |
| Windows Server 2022 Evaluation ISO | Microsoft Evaluation Center | ~5.0 GB | 180-day evaluation |
| PuTTY or Windows Terminal + OpenSSH | Built into Windows 11 | — | `ssh` is present by default on Windows 11 |

**A note on Workstation versions**

You asked for **Workstation Pro 17**, and that is what this guide
targets — specifically **17.6.3**, the final 17.x release. You should
know that Broadcom shipped the successor, **VMware Workstation Pro
26H1** (build 25388281), on **14 May 2026**; it moved the Windows
application to a 64-bit binary and added remote connection to ARM-based
ESX hosts. Everything in this lab works identically on 26H1 — the
Virtual Network Editor, the NAT service, host-only networks, and
snapshots are unchanged in every respect this lab touches. Use 17.6.3 as
written, or 26H1 if you prefer to be current; no step needs
modification.

Both are free. Since **11 November 2024**, VMware Workstation Pro has
required no license key for commercial, educational, or personal use.

## Summary and Completion Checklist

- [ ] Topology, address plan, and resource budget understood.
- [ ] Bill of materials downloaded and checksummed.
