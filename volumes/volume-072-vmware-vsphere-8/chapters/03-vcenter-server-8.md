# Chapter 03: vCenter Server 8

## Learning Objectives

- Deploy and configure vCenter Server 8 (VCSA).
- Use identity federation and Single Sign-On.
- Manage inventory, roles, and permissions.
- Automate vCenter 8 with PowerCLI and the REST API.
- Complete a walkthrough for each vCenter 8 topic.

## Theory and Architecture

**vCenter Server 8** remains the **VCSA** (Linux appliance) and keeps the vSphere 7 management
model — a **datacenter → cluster → host/VM** inventory, **SSO** authentication, **role-based**
authorization, the **Content Library**, certificate management, and REST/SOAP APIs. What matures in
8 is **identity federation** — vCenter delegates authentication to an external identity provider
(such as Microsoft Entra ID / ADFS via OIDC), so logins (including **MFA**) happen at the IdP and
vCenter never handles the credentials — the modern, more secure alternative to joining vCenter
directly to Active Directory. vCenter 8 also coordinates the new hardware features (DPU/DSE lifecycle
via vLCM, device groups) and Tanzu **supervisor services** and **workload availability zones**.
Operationally it is administered the same way — PowerCLI, govc, pyvmomi, and the REST API — so
existing automation carries forward with version updates.

## Design Considerations

Deploy **VCSA 8** sized to the environment and protect it (backup, vCenter HA). Prefer **identity
federation** (external IdP + MFA) over direct AD integration for new deployments. Structure the
inventory for operations and assign **least-privilege roles**. Upgrade **vCenter before hosts**.
Automate inventory and access.

## Implementation and Automation

The labs build inventory, reason about identity federation, assign a role, and query vCenter 8 via
the REST API.

## Validation and Troubleshooting

Confirm the vCenter 8 model:

```text
VCSA 8 (Linux appliance). Inventory datacenter->cluster->host/VM. Auth: SSO + identity federation
  (external IdP/OIDC, MFA at the IdP). Authz: least-privilege roles on objects.
Coordinates DPU/DSE lifecycle (vLCM), device groups, Tanzu supervisor services + workload AZs. REST/SOAP APIs.
```

Common pitfalls: joining vCenter directly to AD where **identity federation** is preferable; and
not backing up the **VCSA**.

## Security and Best Practices

Use **identity federation** with **MFA** at the IdP, assign **least-privilege roles**, back up and
protect the **VCSA**, and manage certificates. Upgrade vCenter first. Audit permissions. Security
deepens in Chapter 8.

## Hands-On Lab

vCenter 8 walkthroughs. **Shared prerequisites** — vCenter Server 8 (VCSA) with a host, PowerCLI,
API access, in a lab. **Cost:** none with evaluation.

### Lab 3.1 — Build inventory with PowerCLI

**Objective:** Create a datacenter and cluster.

```powershell
Connect-VIServer vcenter8.lab.local
New-Datacenter -Location (Get-Folder Datacenters) -Name "DC1"
New-Cluster -Location (Get-Datacenter DC1) -Name "Cluster1" -DRSEnabled -HAEnabled
Get-Cluster Cluster1 | Select Name, DrsEnabled, HAEnabled
```

**Expected result:** a **datacenter and DRS/HA cluster** — the vCenter 8 inventory foundation
(same cmdlets as 7).

**Negative test:** add hosts with no cluster; a **cluster** enables the platform features — create
it first.

**Cleanup:** `Remove-Cluster Cluster1 -Confirm:$false; Remove-Datacenter DC1 -Confirm:$false`.

### Lab 3.2 — Identity federation concept

**Objective:** Understand federated authentication.

```text
# Identity federation: vCenter 8 trusts an external IdP (e.g., Entra ID/ADFS via OIDC).
#   Login + MFA happen at the IdP; vCenter never sees the password. Preferred over direct AD join.
"federation: vCenter -> external IdP (OIDC) -> MFA at IdP -> token to vCenter (no password handling)"
```

**Expected result:** the **identity federation** model — external, MFA-capable authentication.

**Negative test:** handle passwords directly by joining vCenter to AD for a new deployment; prefer
**federation** for stronger, centralized auth.

**Cleanup:** none.

### Lab 3.3 — Assign a least-privilege role

**Objective:** Grant scoped permissions.

```powershell
New-VIPermission -Entity (Get-Cluster Cluster1) -Principal "LAB\vm-operators" `
  -Role (Get-VIRole "Virtual machine power user") -Propagate $true
Get-VIPermission -Entity (Get-Cluster Cluster1)
```

**Expected result:** the operators group granted a **scoped role** — least-privilege access.

**Negative test:** grant Administrator at the root; assign a **scoped, least-privilege** role.

**Cleanup:** remove the permission.

### Lab 3.4 — Query vCenter 8 via the REST API

**Objective:** Read inventory programmatically.

```bash
TOKEN=$(curl -sk -u "$VC_CRED" -X POST "https://<vcenter8>/api/session" | tr -d '"')
curl -sk -H "vmware-api-session-id: $TOKEN" "https://<vcenter8>/api/vcenter/cluster" 2>/dev/null \
  | python3 -c "import sys,json;print('clusters:', len(json.load(sys.stdin)))" 2>/dev/null \
  || echo "vCenter 8 REST API: POST /api/session for a token, then GET /api/vcenter/cluster|host|vm"
```

**Expected result:** the cluster inventory from the **vCenter 8 REST API** — programmatic
management (same API family as 7, updated).

**Negative test:** script the GUI; the **REST API** returns JSON — use it (or PowerCLI/govc).

**Cleanup:** none (read-only).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

vCenter Server 8 keeps the VCSA management model (inventory, SSO, roles, APIs) and matures identity
federation (external IdP + MFA), while coordinating the new hardware and Tanzu features. Prefer
federation, assign least privilege, protect the VCSA, upgrade vCenter first, and automate.

- [ ] I can build inventory with PowerCLI.
- [ ] I can explain identity federation.
- [ ] I can assign a least-privilege role.
- [ ] I can query vCenter 8 via the REST API.
- [ ] I completed Labs 3.1–3.4 including each negative test.
