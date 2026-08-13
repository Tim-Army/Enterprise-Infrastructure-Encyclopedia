# Chapter 04: CCSA — Software Blades and Monitoring

## Learning Objectives

- Enable and tune core Software Blades (IPS, Application Control, URL Filtering, Identity Awareness).
- Understand Threat Prevention profiles.
- Monitor gateways and traffic with SmartConsole and CLI.
- Read logs and events for verification.
- Complete a walkthrough for each blade/monitoring topic.

## Theory and Architecture

**Software Blades** are the modular security functions a gateway runs. Core CCSA blades: **IPS**
(intrusion prevention — protections against known exploits), **Application Control** (identify and
control thousands of apps), **URL Filtering** (category-based web policy), and **Identity Awareness**
(map traffic to users/groups via AD, captive portal, or identity agents, so rules use identities not
just IPs). **Threat Prevention** blades (IPS, Anti-Bot, Anti-Virus, Threat Emulation/Extraction) are
governed by **profiles** that set protection actions (Prevent/Detect) and performance. Blades are
enabled on the gateway object and tuned in policy. **Monitoring** spans SmartConsole (Logs & Monitor
views, gateway status, and reports) and the CLI (**cpview** for live stats, **cpstat** for
component status, **fw stat** for policy). Reading **logs and events** turns raw traffic into
verification that policy and blades work — the operational heart of CCSA.

## Design Considerations

Enable only the **blades** the role needs; start Threat Prevention in **Detect**, then move to
**Prevent** after tuning. Use **Identity Awareness** so rules reference users/groups. Monitor with
**cpview**/SmartConsole; build **reports** for stakeholders. Watch gateway CPU/memory when enabling
inspection-heavy blades.

## Implementation and Automation

The labs enable blades, tune Threat Prevention, and monitor.

## Validation and Troubleshooting

Confirm blade and monitoring concepts:

```text
Blades: IPS, Application Control, URL Filtering, Identity Awareness (users in rules), + Threat Prevention (Anti-Bot/AV/Emulation).
Threat Prevention profiles: Detect -> tune -> Prevent. Monitor: SmartConsole (Logs/status/reports) + cpview/cpstat/fw stat (CLI).
```

Common pitfalls: enabling **Prevent** before tuning (false-positive outages); and enabling every
blade at once (gateway overload).

## Security and Best Practices

Enable needed **blades**, tune Threat Prevention from **Detect → Prevent**, use **Identity
Awareness** for user-based policy, and **monitor** with logs/cpview/reports. Watch performance.
Defensive detection and prevention only.

## Hands-On Lab

Blade and monitoring walkthroughs. **Shared prerequisites** — Check Point gateway with policy
installed, SmartConsole. **Cost:** none.

### Lab 4.1 — Enable Application Control and URL Filtering

**Objective:** Add app/web policy.

```text
# Gateway object -> enable Application Control + URL Filtering blades; add a rule:
#   Source: Internal_Net  App/Category: (block "Anonymizer"/"Gambling")  Action: Drop + Log
"AppControl + URLF enabled; rule blocks risky categories with logging"
```

**Expected result:** category/app-based control with logging — Application Control and URL Filtering.

**Negative test:** block a business-critical SaaS category; verify in **logs** and refine — tune,
don't over-block.

**Rollback:** disable the lab rule.

### Lab 4.2 — Enable Identity Awareness

**Objective:** Put users in the policy.

```text
# Enable Identity Awareness -> identity source (AD Query / captive portal / identity agent);
#   rule Source can now be a user/group (e.g., "Finance") instead of an IP.
"Identity Awareness: rules reference AD users/groups, not just IPs"
```

**Expected result:** identity-based rules — policy by **user/group** (least privilege by identity).

**Negative test:** write user-based rules with Identity Awareness **disabled**; they can't match —
enable the blade and a source first.

**Rollback:** none (keep for later labs).

### Lab 4.3 — Tune Threat Prevention (Detect → Prevent)

**Objective:** Safely activate protections.

```text
# Threat Prevention profile: start Optimized in Detect -> review logs for false positives ->
#   switch high-confidence protections to Prevent.
"Threat Prevention: Detect -> tune from logs -> Prevent"
```

**Expected result:** protections moved to **Prevent** after tuning — safe, effective Threat
Prevention.

**Negative test:** set **Prevent** on day one with no tuning; legitimate traffic may break — start
in Detect.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.4 — Monitor with cpview and logs

**Objective:** Verify operations.

```bash
cpview            # live: CPU, memory, connections, throughput, blade stats (q to quit)
fw stat           # installed policy + interfaces
cpstat os -f cpu  2>/dev/null | head || echo "cpview/cpstat/fw stat + SmartConsole logs = monitoring"
```

**Expected result:** live gateway stats and policy status — operational **monitoring**.

**Negative test:** judge gateway health from a ping alone; **cpview/logs** show CPU, drops, and blade
load — monitor properly.

**Rollback:** none (read-only).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Software Blades (IPS, Application Control, URL Filtering, Identity Awareness) add layered security;
Threat Prevention profiles move Detect→Prevent after tuning; monitoring via SmartConsole logs and
cpview/cpstat/fw stat verifies operations.

- [ ] I can enable Application Control and URL Filtering.
- [ ] I can enable Identity Awareness for user-based policy.
- [ ] I can tune Threat Prevention safely.
- [ ] I can monitor with cpview and logs.
- [ ] I completed Labs 4.1–4.4 including each negative test.
