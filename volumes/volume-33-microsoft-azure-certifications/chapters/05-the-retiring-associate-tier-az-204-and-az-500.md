# Chapter 05: The Retiring Associate Tier — AZ-204 and AZ-500

## Learning Objectives

- State exactly what is retiring, on what date, and what a retirement does
  and does not do to a credential you already hold
- Decide whether to sit AZ-204 or AZ-500 before their retirement dates, or
  redirect that study time
- Describe what each certification covered, since the subject matter
  remains professionally essential after the credential closes
- Identify where the retiring subject matter has moved within Microsoft's
  reorganized program
- Apply a general rule for evaluating any certification that carries a
  published end date

## Theory and Architecture

### The two closing certifications

Verified against Microsoft Learn on **23 July 2026**:

| Certification | Exam | Retires |
| --- | --- | --- |
| Azure Developer Associate | AZ-204 | **31 July 2026** |
| Azure Security Engineer Associate | AZ-500 | **31 August 2026** |

Microsoft's banner on both pages is explicit and worth quoting in
substance: the certification, its related exam, **and its renewal
assessments** all retire on the stated date, after which the certification
can no longer be earned **or renewed**.

That last clause is the consequential one, and it is unusual. For most
vendors — AWS's Advanced Networking specialty, for instance (Volume XVII,
Chapter 13) — a retirement stops new certifications while existing ones
run out their term normally. Here, because Azure role-based certifications
renew **annually** ([Chapter 01](01-the-azure-certification-program-levels-codes-and-renewal.md)),
withdrawing the renewal assessment means a held AZ-204 or AZ-500 will
lapse at its next annual renewal date and cannot be renewed.

A credential you hold today remains valid until its expiry. It simply has
no path forward after that.

### What this means for a study plan

The arithmetic is unforgiving and should be done before any further
reading:

- **AZ-204 retires 31 July 2026.** A study plan not already near
  completion cannot reach a test date. Redirect it.
- **AZ-500 retires 31 August 2026.** A candidate already strong on Azure
  security has a narrow window; anyone starting from scratch does not.
- **Neither will renew.** Even a successful pass buys one annual cycle,
  after which the credential lapses permanently. Weigh that against the
  effort.

For most readers the honest conclusion is to **not start either**, and to
treat the subject matter — which remains entirely current — as
professional development rather than certification preparation.

### AZ-204: what the developer certification covered

The Azure Developer certification spanned participation in all phases of
cloud application development: requirements, design, development,
deployment, security, maintenance, performance tuning, and monitoring.
Its technical surface included Azure compute solutions (App Service,
Functions, container hosting), storage and data access patterns, securing
solutions with Microsoft Entra ID and Key Vault, monitoring and
instrumentation, and integrating third-party services through API
Management, Event Grid, Event Hubs, and Service Bus.

None of that becomes less relevant. The credential is closing; the job is
not.

### AZ-500: what the security certification covered

The Azure Security Engineer implemented, managed, and monitored security
for Azure, multi-cloud, and hybrid environments as part of an end-to-end
infrastructure — identity and access with Entra ID, platform protection
and network security, security operations using Microsoft Defender for
Cloud and its tooling, and data and application security.

### Where the subject matter went

Microsoft has been reorganizing the associate tier around **roles as they
exist now**, and the developer and security content did not disappear so
much as redistribute:

- **Application development on Azure** is increasingly represented by the
  AI-centric developer certifications in
  [Chapter 06](06-the-ai-centric-associate-tier-ai-103-ai-200-and-ab-620.md) —
  Azure AI Apps and Agents Developer (AI-103) and Azure AI Cloud Developer
  (AI-200) — which assume application-development competence and add AI
  workloads on top.
- **Security** is served by Microsoft's dedicated `SC` family, which sits
  outside the Azure-branded lineup: SC-100 (Cybersecurity Architect),
  SC-200 (Security Operations Analyst), and SC-300 (Identity and Access
  Administrator). A reader whose role is Azure security should look there
  rather than at a closing AZ-500.
- **Platform security fundamentals** remain examinable within AZ-104
  ([Chapter 03](03-azure-administrator-az-104.md)) and AZ-305
  ([Chapter 08](08-the-expert-tier-az-305-and-az-400.md)).

## Design Considerations

- **Do the date arithmetic first.** Before any study decision, compare
  your realistic test date against the retirement date. This is a
  five-minute calculation that saves months.
- **Weigh the no-renewal clause explicitly.** A certification that cannot
  be renewed is a depreciating asset. That may still be worth it if an
  employer or contract requires it now, and rarely otherwise.
- **Do not delete the knowledge with the credential.** Both syllabi remain
  accurate descriptions of real work. Keep studying the material; stop
  studying *for the exam*.
- **Redirect security readers to the `SC` family.** It is the durable home
  for Microsoft security certification and carries no equivalent closure.
- **Treat this as the general rule.** Any certification carrying a
  published end date should be evaluated on: can I reach a test date, will
  it renew, and does something durable cover the same ground?

## Implementation and Automation

### Confirming a retirement date yourself

```bash
# Never take a retirement date second-hand. Both certification pages
# state it in a banner rendered into the page HTML.
for c in azure-developer azure-security-engineer; do
  printf '%-26s ' "$c"
  curl -s "https://learn.microsoft.com/en-us/credentials/certifications/$c/" \
    | sed 's/<[^>]*>/ /g' | tr -s ' ' \
    | grep -oE 'This certification[^.]{0,140}\.' | head -1
done
```

### Checking what you already hold and when it expires

```text
# Microsoft Learn profile → Certifications shows each credential's
# expiry date and its renewal window. For a retiring certification,
# confirm whether a renewal assessment is still offered:
#
#   https://learn.microsoft.com/en-us/users/me/credentials
#
# Record, per credential:
#   certification | earned | expires | renewal available? | action
```

### Finding the durable alternative

```bash
# List the SC-family security certifications, which are not part of the
# Azure-branded closure and are the redirect target for AZ-500 readers.
curl -s 'https://learn.microsoft.com/api/catalog/?locale=en-us&type=certifications' \
  | python3 -c 'import sys,json; d=json.load(sys.stdin)
for c in d["certifications"]:
    t=c["title"]
    if "Security" in t or "Identity" in t or "Cybersecurity" in t:
        print(c["certification_type"], "|", t)'
```

## Validation and Troubleshooting

- **Read which nouns the banner covers.** These banners name the
  certification, the exam, *and* the renewal assessments. A banner
  covering only the exam would have different consequences — check rather
  than pattern-matching.
- **"Retired" and "will retire" are different states.** AI-102 and DP-100
  are already retired (Chapter 06); AZ-204 and AZ-500 have future dates
  and remain earnable until then.
- **Verify the no-renewal implication against your own credential.** If
  you hold one of these, confirm the expiry and whether a renewal
  assessment is still offered in your Microsoft Learn profile — that is
  the authoritative record for your account.
- **Do not infer a successor.** Microsoft's pages announce the retirement
  without naming a one-to-one replacement. The redistribution described
  above is an assessment of where the subject matter now lives, not a
  vendor-stated mapping — treat it as guidance and confirm current
  recommendations on Microsoft Learn.

## Security and Best Practices

- Continue applying AZ-500's material regardless of the credential:
  Defender for Cloud, Entra ID conditional access, network protection, and
  data security are operational requirements, not exam topics.
- Do not let a retiring certification justify unauthorized practice
  material to "get it done in time." A rushed pass on a closing credential
  is the weakest possible reason to violate the certification agreement.
- If an employer requires AZ-500 specifically, raise the retirement and
  the no-renewal clause with them early — the requirement itself will need
  updating, and that conversation is better had before the date than
  after.
- Keep the sandbox-subscription discipline from Chapter 01 for any
  security experimentation; Defender and policy changes are disruptive by
  design.

## References and Knowledge Checks

**References**

- [Microsoft Certified: Azure Developer Associate](https://learn.microsoft.com/en-us/credentials/certifications/azure-developer/) (AZ-204 — retires 31 July 2026)
- [Microsoft Certified: Azure Security Engineer Associate](https://learn.microsoft.com/en-us/credentials/certifications/azure-security-engineer/) (AZ-500 — retires 31 August 2026)
- [Certification renewal](https://learn.microsoft.com/en-us/credentials/support/renew-your-microsoft-certification) —
  the annual model whose withdrawal makes these closures permanent.
- [Appendix — Microsoft Azure Certifications and Course Access](../../volume-97-master-appendices/chapters/09-appendix-microsoft-azure-certifications-and-course-access.md)
- See [Chapter 06](06-the-ai-centric-associate-tier-ai-103-ai-200-and-ab-620.md)
  for the certifications that now occupy the developer space, and
  [Chapter 09](09-specialty-certifications-and-certification-operations.md)
  for the currency check that catches changes like these.

**Knowledge checks** *(original conceptual review questions — not
reproductions of any Microsoft exam item)*

1. Name both retiring certifications, their exam codes, and their dates.
2. What three things do the retirement banners cover, and why does the
   third matter more here than for most vendors?
3. Does a retirement invalidate a credential you already hold? What does
   it change?
4. Where should a reader whose role is Azure security direct their
   certification effort instead, and why?
5. State the general rule for evaluating any certification that carries a
   published end date.

## Hands-On Lab

These labs cover the exam-guide domains for both retiring associate
certifications: **AZ-500** (Security Engineer) domain by domain, and
**AZ-204** (Developer) at domain level. Both retire in 2026
([above](#the-two-closing-certifications)); the *subject matter* remains
current, so these labs are worth doing as professional development even
after the credentials close. Each is a walkthrough with the runnable
command and expected result. Mapping is in the
[volume README](../README.md#lab-coverage--the-retiring-associate-tier).

**Cost note:** a Key Vault, a storage account, and a Function App
(consumption plan) are the billable items — all minimal. Lab 5.15 deletes
the resource group.

**Prerequisites**

```bash
az group create --name rg-retire-lab --location eastus
az configure --defaults group=rg-retire-lab location=eastus
```

**Expected result:** `"provisioningState": "Succeeded"`.

### AZ-500 Domain 1 — Secure identity and access (15–20%)

### Lab 5.1 — Managed identity over stored credentials

```bash
az identity create --name id-retire
az identity show --name id-retire --query "{name:name, clientId:clientId, principalId:principalId}" -o table
```

**Expected result:** a user-assigned managed identity with a principal ID.
Managed identities remove stored secrets — the AZ-500 identity default,
and the answer to "how does this app authenticate without a key?"

### Lab 5.2 — Conditional access and RBAC posture

```bash
az role assignment list --assignee "$(az identity show --name id-retire --query principalId -o tsv)" \
  --all --query "[].roleDefinitionName" -o tsv || echo "no roles yet — least privilege by default"
```

**Expected result:** an empty set — a new identity holds nothing until
granted. Least privilege starts from zero, and conditional access gates
the human side.

### AZ-500 Domain 2 — Secure networking (20–25%)

### Lab 5.3 — NSGs, Azure Firewall, and private access

```bash
az network nsg create --name nsg-retire
az network nsg rule create --nsg-name nsg-retire --name deny-inbound \
  --priority 200 --access Deny --direction Inbound --source-address-prefixes Internet \
  --destination-port-ranges '*' --protocol '*'
az network nsg rule show --nsg-name nsg-retire --name deny-inbound --query "access" -o tsv
```

**Expected result:** `Deny`. Network security is layered — NSG at the
subnet/NIC, Azure Firewall at the hub, private endpoints to remove public
exposure.

### AZ-500 Domain 3 — Secure compute, storage, and databases (20–25%)

### Lab 5.4 — Key Vault for secrets, keys, and certificates

```bash
KV="kv-retire-$RANDOM"
az keyvault create --name "$KV" --enable-rbac-authorization true
az keyvault secret set --vault-name "$KV" --name db-conn --value "Server=..." 2>&1 | tail -1 || \
  echo "grant yourself Key Vault Secrets Officer, then retry"
az keyvault show --name "$KV" --query "{name:name, rbac:properties.enableRbacAuthorization, softDelete:properties.enableSoftDelete}" -o table
```

**Expected result:** the vault with `rbac: True` and `softDelete: True`.
RBAC-authorized Key Vault with soft delete is the secure baseline; secrets
never live in code.

### Lab 5.5 — Storage encryption and secure access

```bash
SA="stsec$RANDOM"
az storage account create --name "$SA" --sku Standard_LRS --kind StorageV2 \
  --min-tls-version TLS1_2 --allow-blob-public-access false --https-only true
az storage account show --name "$SA" \
  --query "{tls:minimumTlsVersion, public:allowBlobPublicAccess, https:enableHttpsTrafficOnly}" -o table
```

**Expected result:** `TLS1_2 False True`. Encryption at rest is automatic;
the securable knobs are TLS floor, public-access denial, and HTTPS-only.

### AZ-500 Domain 4 — Secure using Defender for Cloud and Sentinel (30–35%)

### Lab 5.6 — Microsoft Defender for Cloud posture

```bash
az security pricing list --query "value[?pricingTier=='Standard'].name" -o tsv 2>/dev/null | head -5 \
  || echo "Defender plans configurable per resource type"
az security secure-score-controls list --query "value[0].displayName" -o tsv 2>/dev/null \
  || echo "secure score aggregates posture recommendations"
```

**Expected result:** enabled Defender plans (or the notes). Defender for
Cloud provides secure score and workload protection; this domain is the
highest weighted for a reason — it is the operational security surface.

### Lab 5.7 — Microsoft Sentinel (SIEM)

```bash
az monitor log-analytics workspace create --workspace-name law-sentinel
az monitor log-analytics workspace show --workspace-name law-sentinel --query "name" -o tsv
```

**Expected result:** the workspace `law-sentinel`. Sentinel is built on a
Log Analytics workspace; detection rules and playbooks (SOAR) sit on top —
the detection-and-response half of the domain.

### AZ-204 Domain 1 — Develop Azure compute solutions (25–30%)

### Lab 5.8 — Deploy a Function App

```bash
az storage account create --name stfunc$RANDOM --sku Standard_LRS
STF=$(az storage account list --query "[?starts_with(name,'stfunc')].name | [0]" -o tsv)
az functionapp create --name fn-retire-$RANDOM --storage-account "$STF" \
  --consumption-plan-location eastus --runtime node --functions-version 4
az functionapp list --query "[].{name:name, state:state}" -o table
```

**Expected result:** a Function App in `Running`. Functions (event-driven,
consumption-billed) and App Service / container apps are the AZ-204 compute
options.

### Lab 5.9 — App configuration and deployment slots

```bash
APP=$(az functionapp list --query "[0].name" -o tsv)
az functionapp config appsettings set --name "$APP" --settings "FEATURE_FLAG=on" >/dev/null
az functionapp config appsettings list --name "$APP" --query "[?name=='FEATURE_FLAG'].value" -o tsv
```

**Expected result:** `on`. App settings and deployment slots are the
configuration and safe-release mechanisms developers own.

### AZ-204 Domain 2 — Develop for Azure storage (15–20%)

### Lab 5.10 — Blob storage operations

```bash
KEY=$(az storage account keys list --account-name "$STF" --query "[0].value" -o tsv)
az storage container create --name app-data --account-name "$STF" --account-key "$KEY"
az storage container list --account-name "$STF" --account-key "$KEY" --query "[].name" -o tsv
```

**Expected result:** `app-data`. Blob and Cosmos DB access from code
(SDKs, connection via managed identity) is the storage-development skill.

### AZ-204 Domain 3 — Implement Azure security (15–20%)

### Lab 5.11 — Authenticate with managed identity, read from Key Vault

```bash
az role assignment create --assignee "$(az identity show --name id-retire --query principalId -o tsv)" \
  --role "Key Vault Secrets User" --scope "$(az keyvault show --name "$KV" --query id -o tsv)"
az role assignment list --scope "$(az keyvault show --name "$KV" --query id -o tsv)" \
  --query "[?roleDefinitionName=='Key Vault Secrets User'].principalId" -o tsv
```

**Expected result:** the identity's principal ID. The developer pattern:
app uses its managed identity to read a Key Vault secret — no credential in
code.

### AZ-204 Domain 4 — Connect to and consume services (20–25%)

### Lab 5.12 — Service Bus / Event Grid messaging

```bash
az provider show --namespace Microsoft.ServiceBus --query "registrationState" -o tsv
az provider show --namespace Microsoft.EventGrid --query "registrationState" -o tsv
```

**Expected result:** both `Registered`. Service Bus (queues/topics), Event
Grid (events), and Event Hubs (streams) are the integration surface —
choose by message pattern.

### AZ-204 Domain 5 — Monitor and troubleshoot (5–10%)

### Lab 5.13 — Application Insights instrumentation

```bash
az monitor app-insights component create --app ai-retire --location eastus \
  --application-type web 2>&1 | tail -2 || echo "register Microsoft.Insights"
az monitor app-insights component show --app ai-retire \
  --query "{name:name, key:instrumentationKey}" -o table 2>/dev/null | head -3
```

**Expected result:** an Application Insights component (or the register
note). Instrumentation is a development-time decision — observability
designed in, not bolted on.

### Lab 5.14 — Negative test: prove Key Vault RBAC denies without a role

```bash
az keyvault secret show --vault-name "$KV" --name db-conn \
  --query "value" -o tsv 2>&1 | tail -2
```

**Expected result:** if you have not granted yourself a Key Vault data
role, this **fails** with a `Forbidden`/`does not have secrets get`
error — even as subscription Owner, because RBAC-authorized Key Vault
requires a *data-plane* role, not just management rights. That management
vs. data-plane split is the security lesson.

### Lab 5.15 — Cleanup

```bash
az group delete --name rg-retire-lab --yes --no-wait
az group exists --name rg-retire-lab
```

**Expected result:** `false` shortly after — the identity, Key Vault,
storage, Function App, workspace, and Insights removed together.

## Lab Verification

Complete this sign-off once both dates have been confirmed from Microsoft
and a dated decision recorded. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Azure Developer Associate (**AZ-204**) retires **31 July 2026** and Azure
Security Engineer Associate (**AZ-500**) retires **31 August 2026**. Both
banners cover the certification, the exam, and the renewal assessments —
and because Azure role-based certifications renew annually, withdrawing
the renewal assessment means a held credential lapses at its next renewal
and cannot be restored. A credential you hold stays valid to its expiry; it
simply has no path forward. For most readers the correct decision is not to
start either, to keep studying the subject matter — which remains entirely
current — and to redirect certification effort to the AI-centric developer
certifications of Chapter 06 or the durable `SC` security family. The
general rule generalizes: can I reach a test date, will it renew, and does
something durable cover the same ground?

- [ ] Can state both retirement dates and their exam codes.
- [ ] Can explain why the withdrawal of renewal assessments matters more
      in Microsoft's annual model.
- [ ] Knows a retirement does not invalidate a held credential.
- [ ] Can name where developer and security subject matter now lives.
- [ ] Has made and recorded a dated go/no-go decision for both.
- [ ] Completed the hands-on lab, including the third-party-discrepancy
      negative test.
