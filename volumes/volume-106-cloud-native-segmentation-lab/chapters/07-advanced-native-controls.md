# Chapter 07: Advanced Native Controls

## Learning Objectives

- Scale AWS rules with **managed prefix lists** instead of repeated CIDRs.
- Enforce guardrails from above with **GCP hierarchical firewall policies**.
- Apply org-wide baselines with **Azure Policy** for NSGs.
- Understand where native controls stop and a dedicated microsegmentation product begins.

## Beyond one VPC

The per-cloud chapters segmented a single network. Real estates have many accounts, subscriptions, or projects, and central security teams that must enforce a floor no application team can undercut. Each cloud has a native answer.

## Hands-On Lab

### Exercise 7.1 — AWS managed prefix lists

**Objective.** Replace a sprawl of admin CIDRs with a single named prefix list referenced by many SGs.

**Walkthrough**

```bash
PL=$(aws ec2 create-managed-prefix-list --prefix-list-name admin-ips \
    --max-entries 10 --address-family IPv4 \
    --entries Cidr=203.0.113.10/32,Description=home Cidr=198.51.100.0/24,Description=office \
    --query 'PrefixList.PrefixListId' --output text)

# Reference the list instead of raw CIDRs
aws ec2 authorize-security-group-ingress --group-id $WEBSG \
    --ip-permissions IpProtocol=tcp,FromPort=22,ToPort=22,PrefixListIds="[{PrefixListId=$PL}]" >/dev/null
```

**Expected result.** Updating `admin-ips` in one place updates every SG that references it:

```bash
aws ec2 modify-managed-prefix-list --prefix-list-id $PL --current-version 1 \
    --add-entries Cidr=192.0.2.0/24,Description=vpn
aws ec2 get-managed-prefix-list-entries --prefix-list-id $PL --query 'Entries[].Cidr' --output text
203.0.113.10/32  198.51.100.0/24  192.0.2.0/24
```

**Negative test.**

```bash
aws ec2 modify-managed-prefix-list --prefix-list-id $PL --current-version 1 \
    --add-entries Cidr=10.0.0.0/8
An error occurred (IncorrectState) ... prefix list has changed; current version is 2
```

Optimistic-concurrency guard — you must pass the current version, which prevents blind overwrites.

**Rollback.**

```bash
aws ec2 delete-managed-prefix-list --prefix-list-id $PL
```

### Exercise 7.2 — GCP hierarchical firewall policies

**Objective.** Enforce an organization/folder-level deny that a project cannot override.

**Walkthrough**
Hierarchical policies attach to an org or folder and evaluate **before** VPC rules. (Requires an organization; if you are on a standalone project, read this as design.)

```bash
gcloud compute firewall-policies create --organization=ORG_ID \
    --short-name=baseline --description="org baseline"
POLICY=$(gcloud compute firewall-policies list --organization=ORG_ID \
    --format='value(name)' --filter='shortName=baseline')

# Deny RDP from the internet, everywhere, before any project rule runs
gcloud compute firewall-policies rules create 1000 --firewall-policy=$POLICY \
    --organization=ORG_ID --direction=INGRESS --action=deny --layer4-configs=tcp:3389 \
    --src-ip-ranges=0.0.0.0/0 --enable-logging

gcloud compute firewall-policies associations create \
    --firewall-policy=$POLICY --organization=ORG_ID --name=org-baseline
```

**Expected result.** The rule evaluates above every project's VPC rules; no project owner can create an allow that beats it. This is the native "central team sets the floor" control.

**Negative test.** A project-level `allow tcp:3389 from 0.0.0.0/0` no longer works — the hierarchical deny wins because it is evaluated first in the policy chain.

**Rollback.**

```bash
gcloud compute firewall-policies associations delete --name=org-baseline --organization=ORG_ID
gcloud compute firewall-policies delete $POLICY --organization=ORG_ID
```

### Exercise 7.3 — Azure Policy as an NSG guardrail

**Objective.** Deny creation of any NSG rule that opens SSH/RDP to the internet, subscription-wide.

**Walkthrough**
Assign the built-in policy that flags/denies management ports from the internet:

```bash
SUB=$(az account show --query id -o tsv)
# Built-in: "Management ports should be closed on your virtual machines" (audit),
# or use a deny effect with the RDP/SSH-from-internet built-in definition:
az policy assignment create --name deny-open-mgmt \
    --scope "/subscriptions/$SUB" \
    --policy "e372f825-a257-4fb8-9175-797a8a8627d6" \
    --params '{"effect":{"value":"Deny"}}'
```

**Expected result.** Any attempt to create an NSG rule allowing `*` → 3389/22 is rejected at deployment time, before the resource exists — a preventive guardrail rather than a detective alert.

**Negative test.**

```bash
az network nsg rule create -g microseg-lab-rg --nsg-name dbNSG -n bad-rdp \
    --priority 150 --access Allow --protocol Tcp --destination-port-ranges 3389 \
    --source-address-prefixes '*' -o none
... RequestDisallowedByPolicy ... deny-open-mgmt
```

**Rollback.**

```bash
az policy assignment delete --name deny-open-mgmt --scope "/subscriptions/$SUB"
```

## Where native controls stop

Native cloud segmentation is excellent for **network-layer, tier-to-tier** policy and is free. It has limits the dedicated products in Volumes XCIII–CV address:

- **No process/identity awareness.** A security group cannot say "only the `postgres` process may listen" — it sees ports, not workloads. Agent-based products (Illumio, ColorTokens, TrueFort) can.
- **No cross-cloud single policy.** Each cloud is its own island; there is no native "one ruleset spanning AWS + Azure + GCP." Overlay products provide that.
- **Coarse east-west inside a subnet.** Without an ASG/SG per instance, intra-subnet traffic is often open. Host-agent microsegmentation reaches per-process granularity.
- **Limited Layer 7.** Native rules are L3/L4. Service meshes (Istio, Linkerd, Consul — Volumes CIII–CV) add L7 identity and mTLS.

The right answer is usually **both**: native controls as the always-on network floor, a dedicated product where you need workload identity, L7, or one policy across clouds.

## Summary and Completion Checklist

- [ ] AWS prefix list built and referenced from an SG.
- [ ] GCP hierarchical policy understood as the central-team floor.
- [ ] Azure Policy guardrail denying open management ports.
- [ ] The boundary between native controls and dedicated products articulated.
