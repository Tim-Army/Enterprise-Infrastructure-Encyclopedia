# Chapter 05: Cloud Identity — PingOne

## Learning Objectives

- Explain IDaaS and the shift of identity to the cloud.
- Distinguish PingOne from PingOne Advanced Identity Cloud.
- Understand multi-tenancy and the cloud operating model.
- Recognize the trade-offs of cloud versus on-premises identity.

*Cert relevance: PingOne and Advanced Identity Cloud are the **cloud** certifications (PingOne 75% pass mark; Advanced Identity Cloud 70%).*

## Identity as a service

**PingOne** is Ping's **IDaaS** (Identity-as-a-Service) — the identity platform delivered from the cloud rather than software you install and run. Instead of standing up PingFederate and PingDirectory servers yourself, you consume identity as a **cloud service**: SSO, MFA, directory, and orchestration, hosted and operated by Ping, configured through a web console.

The appeal is the same as any SaaS: **no infrastructure to run**, automatic updates, elastic scale, and faster deployment. For CIAM especially ([Chapter 2](02-identity-and-access-management-fundamentals.md)) — where you might serve millions of customers with spiky, unpredictable load — cloud elasticity is a major advantage over sizing on-prem hardware for peak. **PingOne** provides SSO and MFA as a service; the broader **PingOne** family adds DaVinci (orchestration), Protect (threat), and more.

## PingOne versus Advanced Identity Cloud

A distinction the merger created and the exams test:

| | **PingOne** | **PingOne Advanced Identity Cloud** |
|:---|:---|:---|
| Origin | Ping | ForgeRock (Identity Cloud, rebranded) |
| Is | Ping's cloud IDaaS (SSO, MFA, and family) | The full ForgeRock IAM stack, delivered as SaaS |
| Strength | Cloud-native SSO/MFA, DaVinci orchestration | Deep, configurable IAM (AM/IDM/DS) as a managed tenant |

**PingOne Advanced Identity Cloud** is the former **ForgeRock Identity Cloud** — the full, richly-configurable ForgeRock IAM platform (access management, identity management, directory) delivered as a managed **multi-tenant** SaaS. It suits organizations wanting ForgeRock's depth without operating it. The two cloud offerings reflect the merged portfolio's two heritages, and knowing which fits a scenario is exam-relevant. The lab models the cloud-versus-on-prem decision.

## Multi-tenancy and the operating model

Cloud identity is **multi-tenant** — many customer organizations share the platform, isolated into separate **tenants**. This shifts the operating model: Ping runs the infrastructure, applies updates, and guarantees availability, while you configure *your tenant* (your users, apps, policies, branding). You trade **control** (you cannot tweak the underlying servers) for **operational relief** (you do not have to). Administering a tenant — the **Advanced Identity Cloud** certification's focus — is about configuration, not infrastructure. The lab models the trade-off.

## Hands-On Lab

Python models the cloud identity decision. **Cost:** none.

### Lab 5.1 — Cloud IDaaS versus on-premises, and elastic scale

**Objective:** Weigh the cloud-versus-on-prem trade-off, especially for CIAM load.

```bash
python3 - <<'EOF'
# CIAM login load over a day — spiky and unpredictable (a retail sale, a Monday morning)
HOURLY_LOGINS = [200, 150, 100, 100, 300, 900, 2000, 3500, 5000, 4200,
                 3000, 2800, 2600, 2400, 2200, 2600, 4800, 6000, 3500, 2000,
                 1200, 800, 500, 300]   # peak ~6000/hr
PEAK = max(HOURLY_LOGINS)
AVG = sum(HOURLY_LOGINS)//len(HOURLY_LOGINS)

print(f"CIAM login load: peak {PEAK}/hr, average {AVG}/hr (spiky, unpredictable)\n")
print("ON-PREMISES (you size the hardware):")
print(f"   must provision for PEAK ({PEAK}/hr) + headroom, or logins fail at the spike.")
capacity = int(PEAK*1.3)
util = 100*AVG/capacity
print(f"   provision ~{capacity}/hr capacity -> average utilization only {util:.0f}%")
print(f"   -> you PAY for peak hardware that sits {100-util:.0f}% idle most of the time,")
print("      AND a bigger-than-expected spike still overwhelms it.\n")
print("CLOUD IDaaS (PingOne — elastic):")
print(f"   the platform scales to the {PEAK}/hr spike automatically, back down at night.")
print("   you pay for what you USE, not for peak hardware idling.")
print("   an unexpected 2x spike is absorbed by Ping's elastic capacity, not your rack.")
print("\nThe cloud trade-off:")
print("  GAIN: no infrastructure to run/patch/scale, elastic to spikes, fast to deploy,")
print("        pay-per-use. Huge for CIAM's unpredictable, millions-of-users load.")
print("  GIVE UP: deep control of the underlying servers (you configure your TENANT,")
print("        not the infrastructure); data residency + customization within limits.")
print("\nFor spiky CIAM, cloud elasticity usually wins. For a bounded workforce with")
print("strict on-prem/data-residency needs, self-hosted PingFederate/PingDirectory may")
print("fit better. PingOne (cloud) and Advanced Identity Cloud (ForgeRock depth as SaaS)")
print("are the cloud options; the choice is control-vs-operational-relief.")
EOF
```

**Expected result:** On-prem identity forced to provision for peak CIAM load (leaving most capacity idle and still risking bigger spikes), versus cloud IDaaS scaling elastically and billing per use. The cloud lesson is that IDaaS trades deep infrastructure control for operational relief and elasticity — a strong fit for spiky, unpredictable CIAM load, while bounded on-prem-constrained workloads may still self-host.

**Negative test:** Sizing on-prem identity hardware for average load. The peak-hour login spike overwhelms it and logins fail; provisioning for peak instead leaves expensive capacity idle — cloud elasticity absorbs the spikes without either problem.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] IDaaS understood as identity delivered from the cloud — no infrastructure to run, elastic, updated automatically.
- [ ] PingOne distinguished from PingOne Advanced Identity Cloud (the rebranded ForgeRock Identity Cloud).
- [ ] Multi-tenancy and the configure-your-tenant operating model understood as trading control for operational relief.
- [ ] The cloud-versus-on-prem trade-off recognized, with cloud elasticity a strong fit for spiky CIAM load.
