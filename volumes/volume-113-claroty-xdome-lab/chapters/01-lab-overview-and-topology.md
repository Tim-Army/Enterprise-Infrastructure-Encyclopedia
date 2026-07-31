# Chapter 01: Lab Overview and Topology

![Lab topology: a passive collector on a SPAN feeds Claroty xDome, which discovers assets, baselines traffic, forms virtual zones, and derives a least-privilege policy pushed to an integrated enforcer (firewall/NAC). The sanctioned baseline permits web-to-db:5432 and hmi-to-plc:502; the never-baselined hmi-to-db flow is denied by the derived policy and flagged as a deviation.](../../../diagrams/volume-113-claroty-xdome-lab/chapter-01-lab-topology.svg)

*Figure 1-1. Claroty's observe-then-enforce loop: a passive collector baselines what normally talks to what, xDome derives a zone policy from the sanctioned baseline, and an integrated enforcer applies allow-only-baseline — so the operator's unbaselined path to the database is both denied and flagged as a deviation.*

## Learning Objectives

- State what this lab builds and how Claroty xDome segments OT by **observing traffic first**, then enforcing allow-only-baseline.
- Understand passive discovery, **virtual zones**, and **enforcement via integration**.
- Understand the two tracks — a design view of xDome, and a buildable native observe-then-enforce model.
- Read the lab topology and the zone plan.

## How to Use This Guide

### What this lab is

This is a build-it-yourself microsegmentation lab modeled on **Claroty xDome**, whose method is different from the firewalls and brokers of the earlier volumes: Claroty is primarily a **passive, visibility-driven** platform. A collector watches a **SPAN/mirror** of OT traffic, discovers every asset and every conversation without touching the network, and builds a **communication baseline** of what normally talks to what. From that baseline you group assets into **virtual zones** and derive a **least-privilege segmentation policy** — and because Claroty does not sit inline, it **enforces through integration**: it hands the policy to a firewall, NAC, or switch that does the blocking.

The lesson of this volume is the **observe-then-enforce loop**: watch the legitimate traffic, turn the baseline into a policy that permits only what was seen, push it to an enforcer, and everything else — including the operator's lateral move to the database — is denied *and* flagged as a deviation from the baseline. Claroty xDome is a commercial SaaS with no open evaluation, so this volume is **two-track**:

- **Track 1 — the real product (design level).** How xDome discovers assets from a collector/SPAN, builds zones, recommends policy, and pushes it to an integrated enforcer, described accurately at the architecture level.
- **Track 2 — a buildable native model.** One Linux host where a **passive collector** captures traffic from a mirror, builds a communication matrix, derives a least-privilege nftables policy, and an "integrated enforcer" applies it — a working reproduction of observe-then-enforce.

### The moving parts

| Part | What it is | Claroty construct |
|:---|:---|:---|
| **Collector / SPAN** | Passive tap that sees all traffic without inline placement | xDome collector on a mirror port |
| **Asset inventory** | Every discovered device, passively fingerprinted | xDome asset inventory |
| **Communication baseline** | The matrix of who-talks-to-whom, learned | Baseline / network map |
| **Virtual zone** | A group of assets sharing a policy | xDome zone |
| **Segmentation policy** | Allow-only-baseline rules pushed to an enforcer | xDome policy + integration |

Two ideas carry the volume:

- **Observe first, enforce second.** The policy is *derived* from real traffic, not authored blind — so it fits the plant and does not break legitimate flows.
- **Passive discovery, integrated enforcement.** Claroty sees everything and blocks nothing itself; the enforcer (firewall/NAC) applies the policy it produces.

### Topology

```text
                        +------------------------+
                        |  Claroty xDome         |  discovery, baseline,
                        |  (analysis + policy)   |  zones, policy
                        +----+--------------+----+
              SPAN/mirror     |              | policy (integration)
              (passive)       |              v
        +----------------- collector    +---- enforcer (firewall/NAC) ----+
        |  zones routed via the enforcer     | applies allow-only-baseline |
        |  web 10.70.1.10   db 10.70.2.20 :5432                           |
        |  hmi 10.70.3.30   plc 10.70.4.40 :502                           |
        +-----------------------------------------------------------------+
   baseline (legit):  web->db:5432 ,  hmi->plc:502
   deviation (denied + flagged):  hmi->db  (never in the baseline)
```

### The zone and baseline plan

| Asset | Address | Virtual zone | In the legitimate baseline |
|:---|:---|:---|:---|
| web | 10.70.1.10 | `IT-App` | web → db:5432 |
| db | 10.70.2.20 | `IT-Data` | (receives from web) |
| hmi | 10.70.3.30 | `OT-Ops` | hmi → plc:502 |
| plc | 10.70.4.40 | `OT-Control` | (receives from hmi) |

The baseline contains only the two legitimate flows; `hmi → db` is never observed as legitimate, so the derived policy denies it and xDome flags any attempt as a deviation.

## Conventions

| Convention | Meaning |
|:---|:---|
| **Track 1** | Design-level steps on real Claroty xDome |
| **Track 2** | Buildable steps on the native observe-then-enforce model |
| `xdome>` | xDome action (orientation only) |
| `bash` block | Bare commands; output follows on the next line |

Every exercise follows the same shape: **Objective**, **Walkthrough** (per track), **Expected result**, **Negative test**, **Cleanup**.

## Summary and Completion Checklist

- [ ] The observe-then-enforce loop understood.
- [ ] Passive discovery, virtual zones, and integrated enforcement internalized.
- [ ] Track chosen (Track 2 is the buildable one).
- [ ] Topology and baseline plan read.
