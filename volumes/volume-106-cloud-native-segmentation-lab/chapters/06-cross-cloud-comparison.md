# Chapter 06: Cross-Cloud Comparison

## Learning Objectives

- Place AWS, Azure, and GCP native segmentation side by side on the attributes that matter.
- Choose the right identity construct on each cloud (SG / ASG / tag / service account).
- Recognize the model differences that trip up multi-cloud teams.

## The one-page comparison

You built the same estate three times. Here is what actually differs.

| Attribute | AWS Security Group | Azure NSG + ASG | GCP VPC firewall |
|:---|:---|:---|:---|
| **Attachment point** | ENI / instance | Subnet **or** NIC | Network-wide (VPC) |
| **Identity construct** | The SG itself (reference as source) | ASG (group of NICs) | Network tag **or** service account |
| **Explicit deny?** | No — allow-only, implicit deny | Yes — priority-ordered | Yes — priority-ordered |
| **Ordering** | All rules evaluated, any allow wins | First match by ascending priority | First match by ascending priority (deny wins ties differently) |
| **Stateful?** | Yes | Yes | Yes |
| **Stateless option** | NACL (subnet) | none native | none native |
| **Default intra-network** | SG default: allow within same SG only | `AllowVnetInBound` (allow all in VNet) | auto-mode `allow-internal`; custom-mode nothing |
| **Strongest identity** | SG reference | ASG | **Service account** |
| **Logging** | VPC Flow Logs | NSG Flow Logs / VNet Flow Logs | Firewall Rules Logging |

## Hands-On Lab

### Exercise 6.1 — Read the three database rules as one sentence

**Objective.** Confirm that all three clouds now express the *same policy* — "only web reaches db:5432" — in their native grammar.

**Walkthrough**
Pull the effective database rule from each cloud you built:

```bash
# AWS
aws ec2 describe-security-groups --group-ids $DBSG \
    --query 'SecurityGroups[0].IpPermissions[?FromPort==`5432`].UserIdGroupPairs[].GroupId' --output text
sg-<web>

# Azure
az network nsg rule list -g microseg-lab-rg --nsg-name dbNSG \
    --query "[?destinationPortRange=='5432'].{n:name,src:sourceApplicationSecurityGroups[0].id}" -o tsv
allow-web  .../web-asg
deny-mgmt  .../hmi-asg

# GCP
gcloud compute firewall-rules list --filter="network=microseg AND name~db" \
    --format='table(name,priority,sourceServiceAccounts.list(),denied.list(),allowed.list())'
```

**Expected result.** Three different syntaxes, one policy: the database accepts 5432 only from the web identity, and denies the operator. That is the whole lesson of the volume — the primitive changes, the *intent* does not.

**Negative test.** None — this is a read-only comparison.

**Cleanup.** None.

## Choosing the right identity construct

- **AWS:** reference the source **security group**. Never write CIDR rules for east-west traffic if you can name the SG instead.
- **Azure:** create an **ASG per role** and write NSG rules ASG-to-ASG. ASGs decouple the rule from IP addressing exactly like an AWS SG reference.
- **GCP:** prefer **service accounts** over network tags for anything security-relevant. Tags are convenient but any instance-editor can add them; service-account membership is IAM-controlled and far harder to forge.

## The three gotchas that bite multi-cloud teams

1. **AWS NACLs are stateless.** You proved this in Chapter 03 — allowed inbound still needs an allowed ephemeral outbound. SGs, NSGs and GCP rules do not.
2. **Azure evaluates by priority, first match wins.** A broad allow above a specific deny defeats the deny. GCP is the same. AWS is *not* — it evaluates all SG rules and any allow wins (there is no SG deny at all).
3. **GCP firewall rules are network-wide, not per-instance.** A rule with no `target-*` applies to every instance in the VPC. Always scope with a target tag or target service account.

## Summary and Completion Checklist

- [ ] The comparison table understood attribute by attribute.
- [ ] The same policy recognized in three native grammars.
- [ ] The right identity construct chosen per cloud.
- [ ] The three cross-cloud gotchas internalized.
