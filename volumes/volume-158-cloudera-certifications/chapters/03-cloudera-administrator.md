# Chapter 03: Cloudera Administrator (On-Premises and Cloud)

## Learning Objectives

- Explain the Administrator role — installing, operating, and securing CDP.
- Describe Cloudera Manager and cluster lifecycle management.
- Understand the on-premises versus cloud administrator distinction.
- Recognize capacity, maintenance, and governance duties.

*Cert relevance: two certifications — Administrator on premises and Administrator Cloud — validate this role.*

## The administrator role

The **Cloudera Administrator** installs, configures, operates, and maintains the platform — the person who keeps CDP running reliably for everyone else. Cloudera certifies this role **twice**: **Administrator on premises** (managing CDP in your own data center) and **Administrator Cloud** (managing CDP in the public cloud), reflecting that the operational tasks differ by deployment. The on-prem admin manages **clusters** directly — hardware, the stack, capacity; the cloud admin manages CDP's cloud form (environments, data hubs, auto-scaling, cloud infrastructure integration). Both share the core duties of a data-platform operator. The lab models the role.

## Cloudera Manager and the cluster lifecycle

The administrator's primary tool (on-prem) is **Cloudera Manager** — the console for **deploying, configuring, managing, and monitoring** clusters. Through it, the admin:

- **Installs and configures** the CDP stack and its services.
- **Manages and operates clusters** — starting/stopping services, applying configuration, monitoring health.
- **Performs maintenance** — upgrades, patching, adding/removing nodes, troubleshooting.
- **Monitors** health and performance, responding to alerts.

Cloudera Manager centralizes what would otherwise be dozens of independently-administered open-source components into one management plane — the administrator operates the *platform*, not each Hadoop daemon by hand. The lab models cluster management.

## On-premises versus cloud

The two administrator certifications reflect a real split:

- **On-premises** — you manage the **physical/virtual clusters**: capacity planning against fixed hardware, the full stack, storage, and the data-center realities. Deep control, deep responsibility.
- **Cloud** — you manage CDP's **cloud-native** form: provisioning environments, elastic **auto-scaling** (spin compute up for a job, down after), integrating with cloud storage and IAM, and controlling **cloud cost**. The platform handles more of the undifferentiated heavy lifting; you manage its cloud footprint.

Cloudera's **hybrid** nature ([Chapter 2](02-the-cloudera-data-platform.md)) means many organizations run **both**, and an administrator may need both skill sets. The lab models the distinction.

## Capacity, maintenance, and governance

Across both, the administrator owns:

- **Capacity management** — ensuring resources meet demand (on-prem: plan hardware; cloud: right-size and auto-scale).
- **Cluster maintenance** — keeping the platform patched, upgraded, and healthy.
- **Users and security/governance** — managing user access and applying the [SDX (Ranger/Atlas)](02-the-cloudera-data-platform.md) security and governance model.

The administrator is the reliability-and-security backbone of the data platform — everything the engineers, operators, and analysts do depends on it. The lab synthesizes.

## Hands-On Lab

Python models cluster operations and on-prem-vs-cloud capacity. **Cost:** none.

### Lab 3.1 — On-prem fixed capacity vs cloud auto-scaling

**Objective:** See the administrator's capacity duty differ by deployment.

```bash
python3 - <<'EOF'
# a workload demand curve over a day; on-prem fixed hardware vs cloud auto-scaling
demand = [10, 12, 40, 90, 85, 30, 15]   # compute units needed per period (a batch peak midday)
ONPREM_CAPACITY = 90   # must provision for the PEAK (fixed hardware)

print("Workload demand over a day (compute units):", demand, "\n")
print("ON-PREMISES admin — fixed hardware, must provision for PEAK:")
idle = sum(ONPREM_CAPACITY - d for d in demand)
print(f"   provisioned: {ONPREM_CAPACITY} units (24/7) to handle the midday peak of {max(demand)}")
print(f"   idle capacity across the day: {idle} unit-periods = paid-for but UNUSED")
print(f"   duty: capacity PLANNING against fixed hardware; add nodes when growth demands\n")

print("CLOUD admin — auto-scaling, match capacity to demand:")
cloud_used = sum(demand)
print(f"   scale compute UP for the peak, DOWN after -> provision ~= demand each period")
print(f"   used: {cloud_used} unit-periods (vs {ONPREM_CAPACITY*len(demand)} reserved on-prem)")
savings = 100*(1 - cloud_used/(ONPREM_CAPACITY*len(demand)))
print(f"   ~{savings:.0f}% less compute paid for; duty: right-size, auto-scale, control cloud COST\n")
print("Cloudera certifies the admin role TWICE — on-prem vs cloud — because the duties differ:")
print("  ON-PREM: manage physical CLUSTERS + Cloudera Manager; plan capacity for the PEAK.")
print("  CLOUD:   manage CDP's cloud form; AUTO-SCALE + control cost; elastic, not fixed.")
print("Both share: install/operate, maintenance/upgrades, users, and SDX security/governance.")
print("Cloudera's HYBRID nature means many orgs run BOTH — hence two administrator certs.")
EOF
```

**Expected result:** On-premises provisioning for the peak (90 units, large idle capacity paid for around the clock) versus cloud auto-scaling matching capacity to demand (far less compute paid for). The administrator lesson is that Cloudera certifies the role twice because the duties differ — on-prem admins plan fixed-cluster capacity for the peak via Cloudera Manager, cloud admins auto-scale and control cost — while both share install/operate, maintenance, users, and SDX governance, and hybrid organizations often need both.

**Negative test:** Managing a cloud CDP deployment with an on-prem, provision-for-peak mindset. You would over-provision and overspend; cloud administration means auto-scaling to demand and controlling cost, a distinct skill set certified separately.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] The administrator role understood — installing, operating, securing, and maintaining CDP.
- [ ] Cloudera Manager and the cluster lifecycle (deploy, configure, monitor, maintain) understood.
- [ ] The on-premises versus cloud distinction understood — fixed clusters versus elastic auto-scaling.
- [ ] Capacity, maintenance, users, and SDX governance recognized as the administrator's duties.
