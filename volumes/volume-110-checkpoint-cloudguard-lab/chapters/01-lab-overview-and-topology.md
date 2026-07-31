# Chapter 01: Lab Overview and Topology

![Lab topology: a Check Point management server installs an ordered rulebase to a Security Gateway enforcing it over four segments — web (seg APP, role=web), db (seg DB, role=db, :5432), hmi (seg MGMT, role=hmi), plc (seg OT, role=plc, :502). Rules permit web-to-db PGSQL and hmi-to-plc MODBUS; the Cleanup rule drops the hmi-to-db lateral flow. Tag-based dynamic objects make policy follow workloads.](../../../diagrams/volume-110-checkpoint-cloudguard-lab/chapter-01-lab-topology.svg)

*Figure 1-1. Check Point separates management from enforcement: the management server defines and installs the ordered rulebase, the Security Gateway enforces it with an explicit Cleanup drop closing the operator's lateral path, and CloudGuard tag-based objects make the policy follow the workloads.*

## Learning Objectives

- State what this lab builds and how Check Point CloudGuard segments with a **management/gateway split** and a single ordered **rulebase**.
- Understand **network objects** versus **dynamic / data-center objects** that follow workload tags.
- Understand the two tracks — a real Check Point Management + Gateway, and a native Linux/nftables model.
- Read the lab topology, the object plan, and the rulebase plan.

## How to Use This Guide

### What this lab is

This is a build-it-yourself microsegmentation lab on **Check Point CloudGuard**, using the Check Point enforcement model:

- A **management server** (SmartConsole / the management API) where you define **objects** and a single ordered **access-control rulebase**, and from which you **install policy**.
- A **Security Gateway** placed between the segments that enforces the installed rulebase on east-west traffic.
- **CloudGuard data-center / dynamic objects** — objects whose membership is imported from a cloud or virtualization platform by **tag**, so a rule written against a tag automatically follows workloads as they are created, moved, or re-addressed.

The lab segments a four-tier estate (web/db/hmi/plc) first with static network objects, then converts the policy to **tag-based dynamic objects** so it follows the workloads. Check Point is commercial, so this volume is **two-track**:

- **Track 1 — the real thing.** A Check Point **Management** server and **Security Gateway** (15-day evaluation), driven through SmartConsole and the `mgmt_cli` management API.
- **Track 2 — the native model.** One Linux host with **nftables** whose objects, ordered rules, and a tag-updated set reproduce the rulebase and dynamic-object behavior with no Check Point software.

### The moving parts

| Part | What it is | Check Point construct |
|:---|:---|:---|
| **Host / network object** | A named host or subnet used in rules | SmartConsole object / `mgmt_cli add host` |
| **Service** | The port/protocol a rule matches | TCP service object |
| **Access rule** | Ordered rule: source, destination, service, action | Access-control rulebase |
| **Cleanup rule** | The final explicit drop | Last rule in the layer |
| **Dynamic / data-center object** | A group whose members come from cloud/vCenter tags | CloudGuard object |

Two ideas carry the volume:

- **Ordered rulebase with an explicit cleanup drop.** Rules are evaluated top to bottom; the last rule is an explicit *Cleanup rule* that drops everything unmatched — default-deny you can see and log.
- **Objects follow workloads by tag.** A dynamic object written against a tag updates automatically, so `WEB → DB` keeps meaning the right thing as the estate changes — the series' lesson in Check Point's object model.

### Topology

```text
              +-----------------------+        +----------------------+
              |  Check Point Mgmt     |  policy | SmartConsole /       |
              |  (SmartConsole/API)   |<------->| mgmt_cli             |
              +-----------+-----------+  install +----------------------+
                          | install-policy
              +-----------v-----------+
              |  Security Gateway     |  enforces the rulebase east-west
              +--+-----+------+----+--+
        seg APP _/    |      |     \_ seg OT
         +-----+  seg DB   seg MGMT  +-----+
         | web |  +----+    +-----+  | plc |
         +-----+  | db |    | hmi |  +-----+
                  +----+    +-----+
   legit:  APP->DB tcp/5432 ,  MGMT->OT tcp/502
   denied: MGMT->DB (lateral) ,  everything else (Cleanup rule)
```

### The object and rulebase plan

| Endpoint | Segment | Object | Tag (Ch 06) | Address |
|:---|:---|:---|:---|:---|
| web | APP | `web` | `role=web` | 10.40.1.10 |
| db | DB | `db` | `role=db` | 10.40.2.10 |
| hmi | MGMT | `hmi` | `role=hmi` | 10.40.3.10 |
| plc | OT | `plc` | `role=plc` | 10.40.4.10 |

The rulebase permits `web → db` (PostgreSQL) and `hmi → plc` (Modbus); the Cleanup rule drops everything else, including the `hmi → db` lateral flow.

## Conventions

| Convention | Meaning |
|:---|:---|
| **Track 1** | Steps on real Check Point Management + Gateway (SmartConsole / `mgmt_cli`) |
| **Track 2** | Steps on the native Linux/nftables model |
| `mgmt>` / `gw>` | Management API host / gateway CLI (orientation only) |
| `bash` block | Bare commands; output follows on the next line |

Every exercise follows the same shape: **Objective**, **Walkthrough** (per track), **Expected result**, **Negative test**, **Cleanup**.

## Summary and Completion Checklist

- [ ] The management/gateway split and ordered rulebase understood.
- [ ] Network objects versus tag-based dynamic objects clear.
- [ ] Track chosen (or both).
- [ ] Topology, object plan, and rulebase plan read.
