# Chapter 07: IMA — NetMRI Administrator

## Learning Objectives

- Explain what NetMRI does and what the IMA certifies.
- Summarize the administrator topic areas.
- Discover network devices and inventory.
- Manage configuration/change and compliance, and automate.
- Complete a walkthrough for each NetMRI topic.

## Theory and Architecture

**NetMRI** is Infoblox's **network change and configuration management (NCCM)** and
automation platform: it **discovers** multi-vendor network devices, inventories them,
backs up and tracks **configuration changes**, checks **compliance** against policy, and
**automates** remediation and provisioning (CCS scripts, job automation). The **NetMRI
Administrator (IMA)** validates operating it. Topic areas: **discovery/inventory**,
**configuration and change management**, **compliance/policy**, and **automation**.

## Design Considerations

Let NetMRI **discover** the network (SNMP/CLI credentials), back up configs and diff
**changes**, enforce **compliance policies** (e.g., no telnet, required banners), and
**automate** remediation with CCS scripts and jobs. It is the operations/compliance layer
over the device estate.

## Implementation and Automation

The labs use the NetMRI API for each topic — discovery, config/change, compliance, and
automation.

## Validation and Troubleshooting

Confirm the topic areas:

```text
NetMRI (IMA): discovery/inventory; configuration & change management (backup/diff);
compliance/policy; automation (CCS scripts, jobs). Multi-vendor NCCM.
```

Common pitfalls: discovery without device **credentials** (no config access); and
compliance policies with no remediation.

## Security and Best Practices

Supply **credentials** for full discovery/config access, back up and **diff** every
change, enforce **compliance policies** with remediation, and **automate** repetitive
changes with tested CCS scripts. Restrict who can run automation jobs.

## Hands-On Lab

Per-topic walkthroughs — NetMRI. **Shared prerequisites** — a NetMRI appliance and API
access (`/api/`); credentials configured. Commands shown as NetMRI API patterns.
**Cost:** none beyond a lab appliance.

### Lab 7.1 — Discovery and inventory

**Objective:** List discovered devices.

```bash
curl -sS -k -u admin:admin "https://<netmri>/api/3.5/devices/index?limit=5" \
  | python3 -c "import sys,json;print('devices:',len(json.load(sys.stdin).get('devices',[])))"
```

**Expected result:** discovered **devices** with inventory data — the discovery topic.

**Negative test:** maintain a device spreadsheet; **discovery** reconciles the live
estate — use it.

**Cleanup:** none (read-only).

### Lab 7.2 — Configuration and change management

**Objective:** Review a device's config changes.

```bash
curl -sS -k -u admin:admin "https://<netmri>/api/3.5/config_revisions/index?limit=5" \
  | python3 -c "import sys,json;print('config revisions:',len(json.load(sys.stdin).get('config_revisions',[])))"
```

**Expected result:** tracked **config revisions** (backups + diffs) — the change-
management topic.

**Negative test:** rely on manual config saves; NetMRI **versions and diffs** every
change — let it.

**Cleanup:** none (read-only).

### Lab 7.3 — Compliance and policy

**Objective:** Review policy compliance results.

```bash
curl -sS -k -u admin:admin "https://<netmri>/api/3.5/policy_compliances/index?limit=5" \
  | python3 -c "import sys,json;print('compliance results:',len(json.load(sys.stdin).get('policy_compliances',[])))"
```

**Expected result:** device **compliance** results against policy — the compliance topic.

**Negative test:** audit configs by eye; **policy checks** flag violations automatically —
define and run them.

**Cleanup:** none (read-only).

### Lab 7.4 — Automation

**Objective:** Describe automated remediation.

```text
# CCS (Command Control Scripts) / job automation: run a script across matching devices
#   to remediate a violation (e.g., disable telnet) or provision config.
"job: 'disable telnet' CCS script -> runs on non-compliant devices"
```

**Expected result:** an automation **job/script** remediating across devices — the
automation topic.

**Negative test:** fix each device by hand; **automation** applies the change fleet-wide
consistently — script it.

**Cleanup:** disable the job if it was for the lab.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The IMA certifies operating NetMRI across discovery/inventory, configuration and change
management (backup/diff), compliance/policy, and automation (CCS scripts/jobs) — the
multi-vendor NCCM layer over the network.

- [ ] I can list discovered devices and inventory.
- [ ] I can review config revisions and diffs.
- [ ] I can review policy compliance results.
- [ ] I can describe automated remediation.
- [ ] I completed Labs 7.1–7.4 including each negative test.
