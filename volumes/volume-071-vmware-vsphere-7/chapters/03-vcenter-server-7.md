# Chapter 03: vCenter Server 7

## Learning Objectives

- Deploy the vCenter Server Appliance (VCSA) 7.
- Build the inventory (datacenters, clusters, hosts).
- Configure Single Sign-On, users, and roles/permissions.
- Manage vCenter with PowerCLI and the REST API.
- Complete a walkthrough for each vCenter topic.

## Theory and Architecture

**vCenter Server 7** — deployed as the **VCSA** (a hardened Linux appliance; the Windows install is
gone) — is the management plane. It provides a hierarchical **inventory**: a **datacenter** contains
**clusters** (groups of hosts sharing vMotion/DRS/HA), which contain **hosts** and **VMs**, plus
**folders** for organization. Authentication runs through **vCenter Single Sign-On (SSO)** with a
default identity source (`vsphere.local`) and optional external ones (Active Directory, LDAP, and,
in later builds, **identity federation**). Authorization uses **roles** (sets of privileges) granted
to **users/groups** on inventory **objects**, with propagation down the hierarchy — the basis of
least-privilege administration. vCenter also runs the services behind clustering, the **Content
Library**, certificate management (the **VMCA**), and the **REST/SOAP APIs** that PowerCLI, govc, and
pyvmomi drive. vCenter is the single source of truth for the platform.

## Design Considerations

Deploy **VCSA** sized to the environment and protect it (it is critical — back it up, consider
vCenter HA). Structure the **inventory** to match operations and permissions. Integrate **SSO** with
**Active Directory/identity federation** and assign **least-privilege roles** on the right objects.
Automate inventory and permissions with the API.

## Implementation and Automation

The labs build inventory, assign a role/permission, and query vCenter via PowerCLI/REST.

## Validation and Troubleshooting

Confirm the vCenter model:

```text
VCSA (Linux appliance; no Windows vCenter). Inventory: datacenter -> cluster -> host/VM (+ folders).
Auth: SSO (vsphere.local + AD/LDAP/federation). Authz: roles (privileges) on objects, propagated.
Services: clustering, Content Library, VMCA certs, REST/SOAP APIs.
```

Common pitfalls: granting broad **Administrator** everywhere instead of **least-privilege** roles;
and not backing up the **VCSA** (single point of truth).

## Security and Best Practices

Integrate SSO with **AD/federation**, assign **least-privilege roles** on scoped objects, back up
and protect the **VCSA**, and manage **certificates** properly. Audit permissions. Automate to keep
inventory and access consistent. Security deepens in Chapter 8.

## Hands-On Lab

vCenter walkthroughs. **Shared prerequisites** — a vCenter Server 7 (VCSA) with a host, PowerCLI
(`Connect-VIServer`), and API access, in a lab. **Cost:** none with evaluation.

### Lab 3.1 — Build the inventory with PowerCLI

**Objective:** Create a datacenter and cluster.

```powershell
Connect-VIServer vcenter.lab.local
New-Datacenter -Location (Get-Folder Datacenters) -Name "DC1"
New-Cluster -Location (Get-Datacenter DC1) -Name "Cluster1" -DRSEnabled -HAEnabled
Get-Cluster Cluster1
```

**Expected result:** a **datacenter and DRS/HA cluster** created via PowerCLI — the inventory
foundation.

**Negative test:** add hosts with no cluster; a **cluster** enables vMotion/DRS/HA — create it
first.

**Rollback:** `Remove-Cluster Cluster1 -Confirm:$false; Remove-Datacenter DC1 -Confirm:$false`.

### Lab 3.2 — Add a host

**Objective:** Bring an ESXi host under management.

```powershell
Add-VMHost esxi01.lab.local -Location (Get-Cluster Cluster1) -User root -Password '***' -Force
Get-VMHost | Select Name, ConnectionState, Version
```

**Expected result:** the ESXi host **connected** to the cluster — a managed host.

**Negative test:** manage the host only via its Host Client; **add it to vCenter** for
clustering/features.

**Rollback:** `Remove-VMHost esxi01.lab.local -Confirm:$false`.

### Lab 3.3 — Assign a least-privilege role

**Objective:** Grant scoped permissions.

```powershell
New-VIPermission -Entity (Get-Cluster Cluster1) -Principal "LAB\vm-operators" `
  -Role (Get-VIRole "Virtual machine power user") -Propagate $true
Get-VIPermission -Entity (Get-Cluster Cluster1)
```

**Expected result:** the **vm-operators** group granted a scoped role on the cluster — least-
privilege access.

**Negative test:** grant **Administrator** at the vCenter root to operators; assign a **scoped,
least-privilege** role instead.

**Rollback:** `Get-VIPermission -Entity (Get-Cluster Cluster1) | Where {$_.Principal -match 'vm-operators'} | Remove-VIPermission -Confirm:$false`.

### Lab 3.4 — Query vCenter via the REST API

**Objective:** Read inventory programmatically.

```bash
TOKEN=$(curl -sk -u "$VC_CRED" -X POST "https://<vcenter>/api/session" | tr -d '"')
curl -sk -H "vmware-api-session-id: $TOKEN" "https://<vcenter>/api/vcenter/host" 2>/dev/null \
  | python3 -c "import sys,json;print('hosts:', len(json.load(sys.stdin)))" 2>/dev/null \
  || echo "vCenter REST API: POST /api/session for a token, then GET /api/vcenter/host|vm|cluster"
```

**Expected result:** the host inventory from the **vCenter REST API** — programmatic management.

**Negative test:** script against the GUI; the **REST API** returns JSON — use it (or PowerCLI/govc).

**Rollback:** none (read-only).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

vCenter Server 7 (VCSA appliance) is the management plane: a datacenter→cluster→host inventory, SSO
authentication with AD/federation, least-privilege roles on scoped objects, and REST/SOAP APIs for
automation. Structure the inventory for operations, assign least privilege, protect the VCSA, and
automate.

- [ ] I can build inventory with PowerCLI.
- [ ] I can add a host to a cluster.
- [ ] I can assign a least-privilege role.
- [ ] I can query vCenter via the REST API.
- [ ] I completed Labs 3.1–3.4 including each negative test.
