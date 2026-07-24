# Chapter 03: Azure Administrator — AZ-104

## Learning Objectives

- Place AZ-104 as the anchor of the Azure associate tier and the usual
  real starting point for infrastructure engineers
- Describe the administrator's domain: identity and governance, storage,
  compute, virtual networking, and monitoring
- Configure and verify the core administrator objects from the CLI —
  resource groups, RBAC assignments, storage, virtual machines, and
  virtual networks
- Apply Azure Policy and RBAC as the two distinct governance mechanisms
  they are, and explain when each is the right tool
- Build a study plan anchored in a sandbox subscription rather than in
  reading

## Theory and Architecture

### The anchor certification

**AZ-104, Microsoft Certified: Azure Administrator Associate**, is the
Azure certification most infrastructure engineers should hold first. It
carries no announced retirement date (verified 23 July 2026), it is the
recommended prerequisite named on several other certification pages, and
its subject matter — identity, governance, storage, compute, networking,
monitoring — is the substrate every other Azure role builds on.

Unlike the fundamentals tier (Chapter 02), AZ-104 is a **role-based**
certification and therefore renews annually through the free assessment
described in [Chapter 01](01-the-azure-certification-program-levels-codes-and-renewal.md).

### What the administrator owns

The role spans five areas, and they map cleanly onto day-to-day work:

- **Identity and governance** — Microsoft Entra ID users and groups,
  role-based access control (RBAC), Azure Policy, resource locks, and
  management-group structure.
- **Storage** — storage accounts, blob tiers and lifecycle management,
  Azure Files, shared access signatures, and replication options
  (LRS/ZRS/GRS).
- **Compute** — virtual machines and scale sets, availability sets and
  zones, disks and images, App Service, and container options.
- **Virtual networking** — virtual networks and subnets, network security
  groups, load balancing, DNS, peering, and hybrid connectivity.
- **Monitoring and backup** — Azure Monitor, alerts, Log Analytics, Azure
  Backup, and Site Recovery.

### RBAC and Policy answer different questions

The single most useful conceptual distinction at this level, and one that
separates administrators who understand Azure governance from those who
have merely configured it:

- **RBAC answers "who may act?"** It grants a security principal
  permission to perform operations on a scope. It is about *identity*.
- **Azure Policy answers "what may exist?"** It evaluates resources
  against rules and can audit, deny, or remediate — regardless of who is
  acting, including subscription owners. It is about *resource state*.

A subscription owner has full RBAC rights and still cannot create a
non-compliant resource if a policy denies it. Neither mechanism
substitutes for the other, and designs that try to enforce configuration
standards through RBAC alone consistently fail.

### Scope inheritance

Both mechanisms flow down the hierarchy — management group → subscription
→ resource group → resource. Assign at the highest scope that is correct,
because assignments made at resource level multiply into an unmanageable
estate. This is the same instinct AWS's organizational units reward
(Volume XVII, Chapter 02), expressed in Microsoft's hierarchy.

## Design Considerations

- **Start here, not at AZ-900.** For anyone already administering
  infrastructure, AZ-104 is the certification that changes how you are
  read professionally; the fundamentals tier rarely does.
- **Assign RBAC to groups, never to users.** Individual assignments are
  invisible at scale and outlive the person. This is examinable and it is
  also simply correct.
- **Use Policy for standards, RBAC for permission.** If the requirement is
  "all storage accounts must deny public blob access," that is Policy. If
  it is "the storage team may manage storage accounts," that is RBAC.
- **Learn replication options by failure mode.** LRS, ZRS, and GRS differ
  in *what failure they survive* — a rack, a zone, a region. Memorizing
  the acronyms without the failure each addresses does not survive a
  scenario question.
- **Practice in a subscription you can destroy.** The exam rewards
  procedural fluency, which only comes from building and tearing down
  repeatedly. A budget alert (Chapter 01) makes that safe.

## Implementation and Automation

### Core administrator objects, end to end

```bash
# Resource group — the lifecycle container everything else lives in
az group create --name rg-az104-lab --location eastus
```

```bash
# Storage account, then verify the replication setting explicitly
az storage account create --name staz104lab$RANDOM \
  --resource-group rg-az104-lab --sku Standard_LRS --kind StorageV2
az storage account list --resource-group rg-az104-lab \
  --query '[].{name:name, sku:sku.name, https:enableHttpsTrafficOnly}' -o table
```

```bash
# Virtual network and subnet
az network vnet create --resource-group rg-az104-lab --name vnet-lab \
  --address-prefix 10.10.0.0/16 --subnet-name snet-app --subnet-prefix 10.10.1.0/24
```

### RBAC: assign to a group at the right scope

```bash
# Inspect built-in role definitions before inventing a custom one
az role definition list --query "[?contains(roleName,'Storage')].{role:roleName}" -o table
```

```bash
# Assign at resource-group scope (substitute a group object ID)
az role assignment create --assignee-object-id "<GROUP_OBJECT_ID>" \
  --assignee-principal-type Group --role "Storage Account Contributor" \
  --scope "$(az group show --name rg-az104-lab --query id -o tsv)"
```

### Policy: enforce state regardless of who acts

```bash
# Assign a built-in policy that denies public blob access
az policy assignment create --name deny-public-blob \
  --policy "4fa4b6c0-31ca-4c0d-b10d-24b96f62a751" \
  --scope "$(az group show --name rg-az104-lab --query id -o tsv)"
```

## Validation and Troubleshooting

- **Prove the policy denies, do not assume it.** The negative test in the
  lab below is the point: a policy assignment that has never blocked
  anything is unverified configuration.
- **Check effective access, not assignments.** `az role assignment list
  --assignee <id> --all` shows what a principal actually has across
  scopes, including inherited assignments that a resource-level view
  hides.
- **Read replication from the resource, not the plan.** `sku.name` on a
  storage account states what replication is actually in force; intent
  recorded elsewhere is not evidence.
- **When a deployment fails, distinguish permission from policy.** An RBAC
  failure says the principal lacks rights; a policy failure names the
  policy definition that denied it. The remedies are entirely different,
  and telling them apart quickly is a real administrator skill.

## Security and Best Practices

- Grant the least-privileged built-in role that fits before writing a
  custom role; custom roles are a maintenance burden and are frequently
  over-scoped in practice.
- Never assign Owner at subscription scope for routine work. Use scoped
  Contributor plus Policy for standards.
- Enable resource locks (`CanNotDelete`) on anything whose accidental
  deletion would be expensive, and understand that locks bind even
  Owners — which is the point.
- Storage account keys are effectively root credentials for the data
  plane; prefer Entra ID authentication and shared access signatures with
  short lifetimes, and rotate keys on a schedule.
- Run every lab in the sandbox subscription. The policy lab below
  deliberately blocks resource creation, which is disruptive by design.

## References and Knowledge Checks

**References**

- [Microsoft Certified: Azure Administrator Associate](https://learn.microsoft.com/en-us/credentials/certifications/azure-administrator/) (AZ-104)
- [Azure RBAC documentation](https://learn.microsoft.com/en-us/azure/role-based-access-control/)
- [Azure Policy documentation](https://learn.microsoft.com/en-us/azure/governance/policy/)
- [Appendix — Microsoft Azure Certifications and Course Access](../../volume-97-master-appendices/chapters/09-appendix-microsoft-azure-certifications-and-course-access.md)
- See [Chapter 04](04-azure-network-engineer-az-700.md) for the networking
  depth beyond the administrator's scope, and
  [Chapter 08](08-the-expert-tier-az-305-and-az-400.md) for the architect
  path this leads to.

**Knowledge checks** *(original conceptual review questions — not
reproductions of any Microsoft exam item)*

1. State the question RBAC answers and the question Policy answers, and
   give a requirement that needs each.
2. Why can a subscription Owner be prevented from creating a resource?
3. Distinguish LRS, ZRS, and GRS by the failure each survives.
4. Why should RBAC be assigned to groups rather than users, and at the
   highest correct scope?
5. A deployment fails. How do you tell an RBAC denial from a Policy
   denial, and why does it matter?

## Hands-On Lab

These labs cover the **AZ-104 "Skills measured" outline**, domain by
domain, at its published weights. Each is a walkthrough: run the `az` CLI
command and compare against the stated result. Mapping is in the
[volume README](../README.md#lab-coverage--az-104-azure-administrator).

**Cost note:** a storage account, a small VM, a VNet, and a Recovery
Services vault are minimal but **not free**. Lab 3.24 deletes the whole
resource group, which removes everything. Set a budget alert (Chapter 01)
first.

**Prerequisites**

```bash
az group create --name rg-az104-lab --location eastus
az configure --defaults group=rg-az104-lab location=eastus
```

**Expected result:** JSON with `"provisioningState": "Succeeded"`.

### Domain 1 — Manage Azure identities and governance (20–25%)

### Lab 3.1 — Manage Entra users and groups

```bash
az ad group create --display-name grp-az104 --mail-nickname grp-az104
az ad group show --group grp-az104 --query '{name:displayName, id:id}' -o table
```

**Expected result:** the group with an object ID. (Requires directory
rights; if denied, record that as the finding — user/group management is a
directory permission, not a subscription one.)

### Lab 3.2 — Manage access to Azure resources with built-in roles

```bash
SCOPE=$(az group show --name rg-az104-lab --query id -o tsv)
az role assignment create --assignee-object-id "$(az ad group show --group grp-az104 --query id -o tsv)" \
  --assignee-principal-type Group --role "Reader" --scope "$SCOPE"
az role assignment list --scope "$SCOPE" --query "[?roleDefinitionName=='Reader'].principalName" -o tsv
```

**Expected result:** the assignment appears. Reader is a built-in role —
prefer built-in over custom, and assign to the group, not a user.

### Lab 3.3 — Interpret access assignments

```bash
az role assignment list --scope "$SCOPE" --include-inherited \
  --query '[].{principal:principalName, role:roleDefinitionName, scope:scope}' -o table
```

**Expected result:** a table including assignments inherited from the
subscription — the "interpret" skill is reading effective access, not just
what was set here.

### Lab 3.4 — Implement and manage Azure Policy

```bash
az policy assignment create --name deny-public-blob \
  --policy "4fa4b6c0-31ca-4c0d-b10d-24b96f62a751" --scope "$SCOPE"
az policy assignment list --scope "$SCOPE" --query "[].displayName" -o tsv
```

**Expected result:** the assignment listed. This built-in policy denies
public blob access — Policy governs *what may exist*, independent of RBAC.

### Lab 3.5 — Configure resource locks, groups, and management groups

```bash
az lock create --name lock-az104 --lock-type CanNotDelete \
  --resource-group rg-az104-lab
az lock list --resource-group rg-az104-lab --query "[].{name:name, level:level}" -o table
```

**Expected result:** a `CanNotDelete` lock. It binds even Owners — the
point of a lock. (Removed in cleanup before the group can be deleted.)

### Lab 3.6 — Manage costs with budgets and Advisor

```bash
az consumption budget list --query "[].{name:name, amount:amount}" -o table 2>/dev/null \
  || echo "budgets require billing-scope permissions"
az advisor recommendation list --query "[?category=='Cost'].shortDescription.solution" -o tsv 2>/dev/null | head -3
```

**Expected result:** budgets (from Chapter 01) and any Advisor cost
recommendations, or the permissions note — cost management is a governance
skill.

### Domain 2 — Implement and manage storage (15–20%)

### Lab 3.7 — Create and configure a storage account with redundancy

```bash
SA="staz104$RANDOM"
az storage account create --name "$SA" --sku Standard_LRS --kind StorageV2 \
  --min-tls-version TLS1_2 --allow-blob-public-access false
az storage account show --name "$SA" \
  --query '{sku:sku.name, tls:minimumTlsVersion, public:allowBlobPublicAccess}' -o table
```

**Expected result:** `Standard_LRS TLS1_2 False`. LRS survives a disk;
choose GRS when a stated requirement is region survival.

### Lab 3.8 — Configure storage firewalls and access

```bash
az storage account update --name "$SA" --default-action Deny
az storage account show --name "$SA" --query "networkRuleSet.defaultAction" -o tsv
```

**Expected result:** `Deny`. Default-deny plus explicit allow rules is the
examinable posture for storage network access.

### Lab 3.9 — SAS tokens and access keys

```bash
EXPIRY=$(date -u -v+1H '+%Y-%m-%dT%H:%MZ' 2>/dev/null || date -u -d '+1 hour' '+%Y-%m-%dT%H:%MZ')
az storage account generate-sas --account-name "$SA" --services b --resource-types sco \
  --permissions r --expiry "$EXPIRY" --https-only -o tsv | head -c 40; echo "..."
```

**Expected result:** a SAS string (`sv=...&ss=b&...`). A short-lived,
read-only, HTTPS-only SAS is least privilege for delegated access — prefer
it over sharing account keys.

### Lab 3.10 — Azure Files and Blob: shares, containers, tiers, lifecycle

```bash
KEY=$(az storage account keys list --account-name "$SA" --query "[0].value" -o tsv)
az storage container create --name lab --account-name "$SA" --account-key "$KEY"
az storage container show --name lab --account-name "$SA" --account-key "$KEY" \
  --query "name" -o tsv
```

**Expected result:** `lab`. Then confirm blob versioning is a toggle:

```bash
az storage account blob-service-properties update --account-name "$SA" \
  --enable-versioning true
az storage account blob-service-properties show --account-name "$SA" \
  --query "isVersioningEnabled" -o tsv
```

**Expected result:** `true` — versioning protects against overwrite and is
distinct from soft delete.

### Domain 3 — Deploy and manage Azure compute resources (20–25%)

### Lab 3.11 — Interpret and deploy an ARM/Bicep template

```bash
cat > /tmp/sa.bicep <<'BICEP'
param location string = resourceGroup().location
resource sa 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: 'stbicep${uniqueString(resourceGroup().id)}'
  location: location
  sku: { name: 'Standard_LRS' }
  kind: 'StorageV2'
}
BICEP
az deployment group what-if --resource-group rg-az104-lab --template-file /tmp/sa.bicep | tail -4
```

**Expected result:** `+ create` for one storage account. `what-if`
previews the change without applying it — the habit AZ-104 rewards.

### Lab 3.12 — Create and configure a virtual machine

```bash
az vm create --name vm-az104 --image Ubuntu2204 --size Standard_B1s \
  --admin-username azlab --generate-ssh-keys --public-ip-address ""
az vm show --name vm-az104 --show-details \
  --query '{size:hardwareProfile.vmSize, state:powerState, pip:publicIps}' -o table
```

**Expected result:** `Standard_B1s VM running` with an empty public IP —
no public exposure by default.

### Lab 3.13 — Manage VM disks and sizes

```bash
az vm disk attach --vm-name vm-az104 --name disk-az104 --new --size-gb 8
az vm show --name vm-az104 --query "storageProfile.dataDisks[].{name:name, gb:diskSizeGb}" -o table
```

**Expected result:** an 8 GB data disk. Resizing and attaching disks is
routine VM management; disks bill even when the VM is stopped.

### Lab 3.14 — Scale sets, App Service, and containers

```bash
az appservice plan create --name plan-az104 --sku B1 --is-linux
az webapp create --name webaz104$RANDOM --plan plan-az104 --runtime "NODE:20-lts"
az webapp list --query "[].{name:name, state:state}" -o table
```

**Expected result:** a web app in `Running`. App Service is the PaaS
compute option; scaling is a plan setting, exercised next.

### Lab 3.15 — Configure scaling for an App Service plan

```bash
az appservice plan update --name plan-az104 --number-of-workers 2
az appservice plan show --name plan-az104 --query "sku.capacity" -o tsv
```

**Expected result:** `2`. Manual scale-out is a capacity change on the
plan, not the app.

### Domain 4 — Implement and manage virtual networking (15–20%)

### Lab 3.16 — Create virtual networks, subnets, and peering

```bash
az network vnet create --name vnet-a --address-prefix 10.10.0.0/16 \
  --subnet-name snet-a --subnet-prefix 10.10.1.0/24
az network vnet create --name vnet-b --address-prefix 10.20.0.0/16 \
  --subnet-name snet-b --subnet-prefix 10.20.1.0/24
az network vnet peering create --name a-to-b --vnet-name vnet-a \
  --remote-vnet vnet-b --allow-vnet-access
az network vnet peering show --name a-to-b --vnet-name vnet-a --query "peeringState" -o tsv
```

**Expected result:** `Connected`. Peering is per-direction and **not
transitive** — the fact all Azure topology design turns on.

### Lab 3.17 — NSGs and application security groups

```bash
az network nsg create --name nsg-az104
az network nsg rule create --nsg-name nsg-az104 --name deny-rdp \
  --priority 300 --access Deny --protocol Tcp --destination-port-ranges 3389 \
  --direction Inbound
az network nsg rule list --nsg-name nsg-az104 --query "[].{name:name, access:access, port:destinationPortRange}" -o table
```

**Expected result:** an explicit `Deny` on 3389. NSGs are stateful and
priority-ordered; explicit rules make intent readable.

### Lab 3.18 — UDRs, service endpoints, and private endpoints

```bash
az network route-table create --name rt-az104
az network route-table route create --route-table-name rt-az104 --name to-nva \
  --address-prefix 0.0.0.0/0 --next-hop-type VirtualAppliance --next-hop-ip-address 10.10.1.4
az network route-table route list --route-table-name rt-az104 \
  --query "[].{name:name, prefix:addressPrefix, hop:nextHopType}" -o table
```

**Expected result:** a `0.0.0.0/0` route to a VirtualAppliance — a
user-defined route overriding the default, the way traffic is forced
through a firewall.

### Lab 3.19 — Azure DNS and load balancing

```bash
az network lb create --name lb-az104 --sku Standard \
  --frontend-ip-name fe --backend-pool-name be
az network lb show --name lb-az104 --query "{name:name, sku:sku.name}" -o table
```

**Expected result:** `lb-az104 Standard`. A Standard load balancer is
regional layer-4; DNS (Azure DNS zones) and load balancing are the
name-resolution-and-distribution skills of this domain.

### Domain 5 — Monitor and maintain Azure resources (10–15%)

### Lab 3.20 — Interpret metrics and configure log settings

```bash
az monitor metrics list --resource "$(az vm show --name vm-az104 --query id -o tsv)" \
  --metric "Percentage CPU" --interval PT1M \
  --query "value[0].timeseries[0].data[-1].{time:timeStamp, cpu:average}" -o table
```

**Expected result:** a recent CPU data point. Azure Monitor metrics are
the raw material; reading them is the examinable skill.

### Lab 3.21 — Alert rules and action groups

```bash
az monitor action-group create --name ag-az104 --short-name azlab
az monitor metrics alert create --name cpu-high --scopes "$(az vm show --name vm-az104 --query id -o tsv)" \
  --condition "avg Percentage CPU > 80" --action ag-az104 \
  --description "lab CPU alert"
az monitor metrics alert list --query "[].{name:name, enabled:enabled}" -o table
```

**Expected result:** an enabled alert. An alert wired to an action group
is the monitoring-to-notification path.

### Lab 3.22 — Backup and recovery

```bash
az backup vault create --name rsv-az104 --location eastus
az backup vault show --name rsv-az104 --query "{name:name, state:properties.provisioningState}" -o table
```

**Expected result:** the Recovery Services vault `Succeeded`. A vault plus
a backup policy is the recovery skill; Site Recovery covers replication.

### Lab 3.23 — Negative test: prove Policy denies a privileged principal

```bash
az storage account create --name stbad$RANDOM --sku Standard_LRS --kind StorageV2 \
  --allow-blob-public-access true 2>&1 | tail -3
```

**Expected result:** the create **fails**, the error naming
`RequestDisallowedByPolicy` and the `deny-public-blob` assignment from
Lab 3.4 — even though you have Contributor/Owner rights. That is the
RBAC-versus-Policy distinction proven: Policy blocks what RBAC would
permit.

### Lab 3.24 — Cleanup

```bash
az lock delete --name lock-az104 --resource-group rg-az104-lab
az group delete --name rg-az104-lab --yes --no-wait
az group exists --name rg-az104-lab
```

**Expected result:** `false` shortly after (deletion is async). The lock
must be removed first, or the group delete is itself denied — a final
reminder of what a lock does.

## Lab Verification

Complete this sign-off once the policy has been proven to deny a
non-compliant resource and the resource group has been removed. Until then,
the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

AZ-104 is the anchor of the Azure associate tier and the right first
certification for most infrastructure engineers: no announced retirement,
recommended as a prerequisite elsewhere, and covering the identity,
governance, storage, compute, networking, and monitoring substrate every
other Azure role assumes. Its central conceptual distinction is that
**RBAC governs who may act while Policy governs what may exist** — which
is why a subscription Owner can still be denied. Both inherit down the
management-group hierarchy, so assign at the highest correct scope and to
groups rather than users. Readiness comes from building and destroying a
sandbox repeatedly, not from reading.

- [ ] Can state what RBAC governs and what Policy governs.
- [ ] Has proven a policy denial against a fully privileged principal.
- [ ] Can distinguish an RBAC denial from a Policy denial by its error.
- [ ] Can explain LRS/ZRS/GRS by the failure each survives.
- [ ] Assigns RBAC to groups at the highest correct scope.
- [ ] Completed the hands-on lab, including the negative test and full
      cleanup.
