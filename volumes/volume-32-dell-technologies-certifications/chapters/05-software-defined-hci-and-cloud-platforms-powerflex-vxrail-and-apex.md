# Chapter 05: Software-Defined, HCI, and Cloud Platforms — PowerFlex, VxRail, and APEX

## Learning Objectives

- Explain PowerFlex's software-defined block architecture (SDS/SDC,
  protection domains, storage pools) and its Operate/Deploy/Design
  ladder
- Operate and deploy VxRail as the VMware-integrated HCI standard,
  connecting Volume V's vSphere depth
- Position the APEX cloud platforms (Azure, Red Hat OpenShift, Azure
  Local) and Azure Stack Hub integrated systems
- Map the codes: PowerFlex D-PWF-OE-01/DY-A-00/RDY-A-00/DS-01; VxRail
  D-VXR-OE-01/DY-01/DS-01; VxBlock D-VXB-DY-A-24; APEX D-AX-DY-A-00 /
  D-AX-RH-A-00 / D-AXAZL-A-00; Azure Stack Hub D-ISAZ-A-01; cloud
  design D-CI-DS-23 / D-CS-DS-23 atop D-CIS-FN-01

## Theory and Architecture

### PowerFlex: block storage as a distributed system

PowerFlex pools server-local storage into a distributed block service:
**SDS** (server contributing storage), **SDC** (consumer kernel
client), MDM cluster as control plane; **protection domains** and
**storage pools** bound failure and performance domains; mesh
rebuild makes node loss a bandwidth event, not an outage. It scales
to extreme IOPS on commodity PowerEdge — the software-defined
counterpoint to Chapter 04's arrays, deployable rack-scale (the
RDY achievement covers the engineered rack).

### VxRail: vSphere with the lifecycle solved

VxRail is HCI with VMware vSAN under vCenter — its differentiator is
**LCM**: validated full-stack releases (ESXi, vSAN, firmware, VxRail
Manager) applied as one upgrade object. Operate lives in day-2:
cluster health, capacity, node add/remove, and the VxRail Manager
plugin; Deploy certifies first-run and network prerequisites
(the classic deploy-day failure is DNS/VLAN prep, not the appliance);
Design sizes nodes and topologies against Volume V's workload math.

### APEX and the Azure/OpenShift platforms

The APEX cloud-platform exams certify Dell-engineered stacks that
run hyperscaler control planes on-premises: **Azure** (and Azure
Local on AX nodes), **Red Hat OpenShift** — plus the Azure Stack Hub
integrated system credential for the established estate. The pattern
to learn once: Dell owns the hardware/lifecycle layer; the cloud
vendor owns the control plane; the exams live at the integration
seam (networking prerequisites, identity, lifecycle coordination).

## Design Considerations

- PowerFlex when the requirement is scale/IOPS with server economics;
  VxRail when the operating model is vSphere; APEX platforms when
  the control plane must be Azure/OpenShift — write the operating
  model down before the hardware
- Protection domains and fault sets mirror rack/power topology or
  they lie; VxRail cluster boundaries are vSphere HA domains (Volume
  V rules apply unchanged)
- Never hand-patch components inside lifecycle-managed stacks; the
  validated bundle is the unit of change (Volume XII's doctrine)

## Implementation and Automation

```text
# PowerFlex CLI (scli) shape of the Operate exam
scli --query_cluster                       # MDM health
scli --query_all_sds; scli --query_all_sdc
scli --add_volume --protection_domain pd1 --storage_pool sp1 \
     --size_gb 512 --volume_name vol-app1
scli --map_volume_to_sdc --volume_name vol-app1 --sdc_ip 10.30.10.31

# VxRail day-2 checks live in vCenter + VxRail Manager API
GET /rest/vxm/v1/system            # version, health
GET /rest/vxm/v1/hosts             # node inventory
POST /rest/vxm/v1/lcm/upgrade      # the one upgrade object
```

## Validation and Troubleshooting

- PowerFlex: MDM cluster state, then SDS/device rebuild backlog —
  rebuild bandwidth is the health metric; SDC mapping verified from
  the host
- VxRail: Skyline/VxRail Manager health before vSphere-level
  theories; LCM precheck output is the deploy-day oracle
- APEX/Azure Local: validate the seam — Arc/portal registration,
  identity, and update rings — before either vendor's stack alone
- All: the Volume XXVI lab's network (VLAN/MTU) checklist catches
  most first-run failures

## Security and Best Practices

- Management planes (MDM, VxRail Manager, cloud portals) on the
  management VLAN with MFA-backed identity
- PowerFlex: separate MDM credentials from SDS hosts; VxRail: vCenter
  SSO hardening per Volume V; APEX: least-privilege cloud RBAC at
  the seam
- Lifecycle bundles verified by signature; no out-of-band drivers

## References and Knowledge Checks

- Exam descriptions for the twelve codes mapped above (Dell Learning
  catalog)
- PowerFlex admin guide; VxRail admin/deploy guides and this
  encyclopedia's VxRail walkthroughs; APEX platform docs

Knowledge checks:

1. Why is PowerFlex rebuild time a function of cluster size, and what
   does that do to protection-domain design?
2. Name three first-run prerequisites VxRail Deploy weights heavily
   and where this encyclopedia rehearses them.
3. For APEX Cloud Platform for Azure, who owns what — and where do
   the exam's hard questions therefore live?

## Hands-On Lab

This chapter carries a topic-level walkthrough lab spanning the **software-defined,
HCI, and cloud exams — Cloud Infrastructure/Services Foundations and Design
(D-CIS-FN-01, D-CI-DS-23, D-CS-DS-23), PowerFlex (D-PWF-*), VxRail (D-VXR-*),
VxBlock (D-VXB-DY-A-24), and APEX/Azure (D-AX-*, D-AXAZL-A-00, D-ISAZ-A-01)** —
mapped in the volume README's coverage tables. Labs use the PowerFlex `scli`, the
VxRail Manager API, and cloud-platform tooling. Each ends
**`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 5.1–5.9** — a PowerFlex cluster (MDM/SDS/SDC), a
VxRail cluster with VxRail Manager and vCenter, and access to an APEX Cloud Platform.
**Cost:** none beyond lab resources.

### Lab 5.1 — PowerFlex provisioning (PowerFlex Operate)

**Objective:** Create a PowerFlex volume and map it to an SDC.

```text
scli --login --username admin --password $PW
scli --query_all
scli --add_volume --protection_domain_name PD1 --storage_pool_name SP1 --size_gb 100 --volume_name LAB-VOL
scli --map_volume_to_sdc --volume_name LAB-VOL --sdc_ip 10.0.0.71
```

**Expected result:** the volume created in the storage pool and mapped to the SDC —
**PowerFlex** is software-defined block storage: **SDS** nodes pool local drives,
**SDC** clients consume volumes, and the **MDM** cluster coordinates; it scales
linearly and can run two-layer (separate) or HCI (collapsed) topologies.

**Negative test:** map a volume to an SDC whose driver is not installed/registered;
the host has no block device — the SDC must be a registered PowerFlex client.

**Cleanup:** `scli --unmap_volume_from_sdc ...` then `scli --remove_volume
--volume_name LAB-VOL`.

### Lab 5.2 — PowerFlex protection domains and fault sets (PowerFlex Implementation)

**Objective:** Read protection domains, storage pools, and fault sets.

```text
scli --query_properties --object_type PROTECTION_DOMAIN --all_objects
scli --query_fault_sets --protection_domain_name PD1
scli --query_storage_pool --protection_domain_name PD1 --storage_pool_name SP1
```

**Expected result:** the protection domain, its fault sets, and pool rebuild/rebalance
state — a **protection domain** bounds a failure/rebuild domain; **fault sets** group
SDS that share failure risk (a rack/PSU) so PowerFlex's mesh mirroring never places
both copies in one fault set.

**Negative test:** place all SDS in one fault set; a rack failure can take both mirror
copies — fault sets must reflect real independent failure domains.

**Cleanup:** none (read-only).

### Lab 5.3 — VxRail deployment (VxRail Deploy)

**Objective:** Read the VxRail cluster and its build state via the API.

```bash
curl -sk -u admin:$PW "https://$VXRM/rest/vxm/v1/system" | jq '{version, health, installed_time}'
curl -sk -u admin:$PW "https://$VXRM/rest/vxm/v1/hosts" | jq -r '.[]? | "\(.serial_number) \(.health)"' | head
```

**Expected result:** the VxRail system version/health and its nodes — **VxRail** is
the jointly-engineered Dell/VMware HCI appliance: **VxRail Manager** automates the
first-run build (vSAN, vCenter, networking) and node add, so a cluster deploys as one
integrated system.

**Negative test:** add a node whose firmware/model is not on the VxRail compatible
baseline; VxRail Manager blocks the expansion — the node must match the cluster's
validated version.

**Cleanup:** none (read-only).

### Lab 5.4 — VxRail lifecycle management (VxRail Operate)

**Objective:** Read the VxRail LCM (Continuously Validated State) status.

```bash
curl -sk -u admin:$PW "https://$VXRM/rest/vxm/v1/lcm/upgrade/status" 2>/dev/null | jq '.'
curl -sk -u admin:$PW "https://$VXRM/rest/vxm/v1/system/available-bundles" 2>/dev/null | jq -r '.[]?.version' | head
```

**Expected result:** the LCM status and available update bundles — VxRail's value is
**lifecycle management**: a single **Continuously Validated State** bundle updates
firmware, ESXi, vSAN, and VxRail Manager together as a tested unit, avoiding the
interop matrix guesswork of build-your-own.

**Negative test:** patch ESXi manually outside VxRail LCM; the cluster drifts from its
validated state and future LCM updates flag it — VxRail must be updated through its
LCM.

**Cleanup:** none (read-only).

### Lab 5.5 — VxBlock converged infrastructure (VxBlock Deploy)

**Objective:** Read the VxBlock's converged components and RCM.

```text
show version
show inventory
```

**Expected result:** the compute (PowerEdge/UCS), network (MDS/Nexus), and storage
(PowerMax/PowerStore) components — **VxBlock** is converged (not hyperconverged)
infrastructure: pre-engineered, factory-integrated compute + network + SAN storage,
lifecycle-managed as one system against a **Release Certification Matrix (RCM)**.

**Negative test:** update a component off the RCM; the system falls out of its
certified/supported state — VxBlock changes follow the RCM.

**Cleanup:** none (read-only).

### Lab 5.6 — APEX Cloud Platform for Microsoft Azure (APEX Azure Implementation)

**Objective:** Read the APEX Cloud Platform for Azure (Azure Local) deployment.

```bash
az stack-hci cluster show --name LAB-CLUSTER --resource-group RG 2>/dev/null | jq '{status, reportedProperties}' 2>/dev/null
```

**Expected result:** the Azure Local (Azure Stack HCI) cluster registered to Azure —
**APEX Cloud Platform for Microsoft Azure** is a turnkey Dell system running Azure
Local: Azure Arc-enabled, managed from the Azure portal, with Dell's integrated
lifecycle for the hardware/software stack.

**Negative test:** a cluster not registered/Arc-connected to Azure cannot be managed
from the portal — Azure registration is required for the cloud-managed model.

**Cleanup:** none (read-only).

### Lab 5.7 — APEX Cloud Platform for Red Hat OpenShift (APEX OpenShift Implementation)

**Objective:** Read the OpenShift cluster on the APEX platform.

```bash
oc get nodes -o wide | head
oc get clusterversion
```

**Expected result:** the OpenShift nodes and cluster version — **APEX Cloud Platform
for Red Hat OpenShift** is a Dell-integrated bare-metal OpenShift system with
automated lifecycle for the hardware and the OpenShift stack, for containerized/
cloud-native workloads on-prem.

**Negative test:** expect Dell integrated lifecycle on a self-installed OpenShift on
generic hardware; the APEX automation and validated stack are what the platform adds
— it is more than OpenShift-on-servers.

**Cleanup:** none (read-only).

### Lab 5.8 — Cloud Infrastructure and Services foundations (Cloud Foundations)

**Objective:** Identify the cloud service and deployment models in use.

```bash
kubectl get pods -A 2>/dev/null | head
virsh list --all 2>/dev/null | head
```

**Expected result:** the VMs (IaaS) and containers (PaaS) underpinning services —
**Cloud Infrastructure and Services** foundations cover the service models (IaaS/PaaS/
SaaS), deployment models (private/public/hybrid), and the enabling technologies
(virtualization, SDN/SDS, orchestration, service management) that Dell's cloud
platforms deliver.

**Negative test:** classify a managed SaaS as IaaS and plan to patch its OS; you
cannot — the service model sets the boundary of control, a core foundations concept.

**Cleanup:** none (read-only).

### Lab 5.9 — Integrated System for Microsoft Azure Stack Hub (Azure Stack Hub)

**Objective:** Read the Azure Stack Hub integrated system's status.

```bash
az stack-hci -h >/dev/null 2>&1; echo "Azure Stack Hub: hybrid Azure services on-prem"
curl -sk -u admin:$PW "https://$ASH/metadata/endpoints?api-version=2015-01-01" 2>/dev/null | jq '.' | head
```

**Expected result:** the Azure Stack Hub endpoints — the **Dell Integrated System for
Microsoft Azure Stack Hub** runs a consistent subset of Azure services in the customer
data center (disconnected or connected), Dell-integrated and lifecycle-managed, for
sovereign/edge/regulated Azure workloads.

**Negative test:** expect the full public-Azure service catalog on Azure Stack Hub;
only the supported on-prem subset is available — the hybrid model is consistent but
not identical to public Azure.

**Cleanup:** none (read-only).

## Lab Verification

Verification means the VxRail prereq sheet would pass a real
first-run validator (every record named), the LCM narrative has
gates and rollback, and the PowerFlex volume survived an SDS loss
with rebuild evidence (or the runbook proves each step against the
guides).

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

- [ ] PowerFlex control/data plane and rebuild model operated
- [ ] VxRail LCM discipline and deploy prerequisites drilled
- [ ] APEX seam-ownership articulated per platform
- [ ] All chapter codes recorded from the verified table
