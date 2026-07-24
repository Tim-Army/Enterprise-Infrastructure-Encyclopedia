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

**Objective:** Build the core administrator objects, then prove that Azure
Policy denies a non-compliant resource even for a principal with full
rights — the distinction at the heart of AZ-104.

**Cost note:** The storage account and virtual network are negligible but
not free. Step 6 deletes the whole resource group, which removes
everything.

**Prerequisites**

- The sandbox subscription and budget alert from Chapter 01.
- Azure CLI authenticated, with rights to assign policy at resource-group
  scope.

**Steps**

1. **Build (15 minutes).** Create the resource group, a storage account,
   and the virtual network from the Implementation section.

   **Expected result:** all three exist; `az storage account list` shows
   the SKU you chose.

2. **Assign policy (10 minutes).** Assign the built-in policy denying
   public blob access at resource-group scope.

   **Expected result:** the assignment appears in
   `az policy assignment list --scope <rg-id>`.

3. **Negative test (15 minutes).** As a principal with Owner or
   Contributor rights, attempt to create a storage account that violates
   the policy — for example with public blob access enabled:

   ```bash
   az storage account create --name stbadpolicy$RANDOM \
     --resource-group rg-az104-lab --sku Standard_LRS --kind StorageV2 \
     --allow-blob-public-access true
   ```

   **Expected result:** the request is **denied**, and the error names the
   policy definition. If it succeeds, the policy is not assigned at the
   scope you think it is — diagnose that before continuing.

4. **Distinguish the failure (10 minutes).** Compare the policy denial's
   error text against an RBAC denial (attempt an action outside your role
   at a scope you do not hold).

   **Expected result:** you can state, from the error alone, which
   mechanism blocked you.

5. **Check effective access (5 minutes).**

   ```bash
   az role assignment list --all \
     --query '[].{principal:principalName, role:roleDefinitionName, scope:scope}' -o table
   ```

   **Expected result:** an accurate picture of inherited assignments, not
   just those made at this resource group.

6. **Cleanup:**

   ```bash
   az policy assignment delete --name deny-public-blob \
     --scope "$(az group show --name rg-az104-lab --query id -o tsv)"
   az group delete --name rg-az104-lab --yes --no-wait
   ```

   Confirm the group is gone and the budget shows no unexpected spend.

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
