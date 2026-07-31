# Chapter 09: Operations, Cost Control, and Teardown

## Learning Objectives

- Verify current spend against the budget you set in Chapter 02.
- **Tear down every billable resource on each cloud you used** — completely.
- Confirm the account is back to zero billable resources.
- Capture the operational lessons for running native segmentation for real.

## Do the teardown now

This is the most important chapter in the volume. A microsegmentation lab left running is a small monthly bill that compounds. Run the teardown for **every cloud you touched**, then verify the account is empty. The segmentation objects (SGs, NSGs, firewall rules) are free, but they must be deleted before their networks can be, so the teardown removes everything.

## Hands-On Lab

### Exercise 9.1 — Check spend first

**Objective.** See what the lab actually cost before deleting the evidence.

**Walkthrough**

```bash
# AWS
aws ce get-cost-and-usage --time-period Start=2026-07-01,End=2026-08-01 \
    --granularity MONTHLY --metrics UnblendedCost \
    --query 'ResultsByTime[0].Total.UnblendedCost.Amount' --output text
0.94

# Azure
az consumption usage list --top 5 --query '[].{name:instanceName, cost:pretaxCost}' -o table

# GCP  (billing export/console; quick check via budgets)
gcloud billing budgets list --billing-account=0X0X0X-0X0X0X-0X0X0X \
    --format='value(displayName, amount.specifiedAmount.units)'
microseg-lab   5
```

**Expected result.** A small figure (typically under a dollar for a few hours). If it is higher, something is still running — the teardown below fixes it.

**Cleanup.** This exercise *is* pre-cleanup.

### Exercise 9.2 — AWS teardown

**Objective.** Delete instances, SGs, NACLs, flow logs, and the VPC.

**Walkthrough**

```bash
# Instances first
aws ec2 terminate-instances --instance-ids $WEB $DBI $HMI >/dev/null
aws ec2 wait instance-terminated --instance-ids $WEB $DBI $HMI

# Flow logs + log group
FL=$(aws ec2 describe-flow-logs --filter Name=resource-id,Values=$VPC --query 'FlowLogs[].FlowLogId' --output text)
[ -n "$FL" ] && aws ec2 delete-flow-logs --flow-log-ids $FL
aws logs delete-log-group --log-group-name /vpc/microseg 2>/dev/null

# Custom NACL (subnets revert to default), custom SGs
aws ec2 delete-network-acl --network-acl-id $NACL 2>/dev/null
for G in $WEBSG $DBSG $HMISG $FLAT; do aws ec2 delete-security-group --group-id $G 2>/dev/null; done

# Detach + delete IGW, subnets, route table, VPC
aws ec2 detach-internet-gateway --vpc-id $VPC --internet-gateway-id $IGW
aws ec2 delete-internet-gateway --internet-gateway-id $IGW
for S in $APP $DB $MGMT; do aws ec2 delete-subnet --subnet-id $S; done
aws ec2 delete-route-table --route-table-id $RT 2>/dev/null
aws ec2 delete-vpc --vpc-id $VPC
aws ec2 delete-key-pair --key-name lab ; rm -f lab.pem
```

**Expected result.**

```bash
aws ec2 describe-instances --filters Name=vpc-id,Values=$VPC --query 'Reservations' --output text
# empty
aws ec2 describe-vpcs --vpc-ids $VPC 2>&1 | grep -o InvalidVpcID.NotFound
InvalidVpcID.NotFound
```

The VPC is gone.

**Negative test.** If `delete-vpc` errors with `DependencyViolation`, a resource still references it (a leftover ENI, NAT gateway, or endpoint). List dependencies and remove them:

```bash
aws ec2 describe-network-interfaces --filters Name=vpc-id,Values=$VPC --query 'NetworkInterfaces[].NetworkInterfaceId'
```

**Cleanup.** This is the cleanup.

### Exercise 9.3 — Azure teardown

**Objective.** Delete the entire resource group — the cleanest teardown of the three.

**Walkthrough**
Because everything was created in one resource group, one command removes all of it:

```bash
az group delete -n microseg-lab-rg --yes --no-wait
```

**Expected result.**

```bash
az group exists -n microseg-lab-rg
false
```

(May take a few minutes with `--no-wait`; re-run until `false`.)

**Negative test.** A resource-group delete cascades to every child; there is no partial state to leak. Confirm no stray resources outside the group:

```bash
az resource list --query "[?resourceGroup=='microseg-lab-rg']" -o tsv
# empty
```

**Cleanup.** This is the cleanup. Keep the budget assignment or delete it in the portal.

### Exercise 9.4 — GCP teardown

**Objective.** Delete instances, firewall rules, subnets, VPC, and service accounts — or the whole project.

**Walkthrough**
Fastest: delete the lab project (removes everything and stops all billing):

```bash
gcloud projects delete $PROJECT
```

Or, if you must keep the project, remove resources individually:

```bash
gcloud compute instances delete web db hmi --zone=us-central1-a --quiet
gcloud compute firewall-rules delete allow-ssh allow-internal deny-hmi-db allow-web-db \
    allow-web-db-sa deny-any-db-sa --quiet
for R in web db hmi; do gcloud iam service-accounts delete $R-sa@$PROJECT.iam.gserviceaccount.com --quiet; done
gcloud compute networks subnets delete app db mgmt --region=us-central1 --quiet
gcloud compute networks delete microseg --quiet
```

**Expected result.**

```bash
gcloud compute instances list
Listed 0 items.
gcloud compute networks list --filter='name=microseg' --format='value(name)'
# empty
```

**Negative test.** Deleting the VPC before its firewall rules and instances fails:

```bash
gcloud compute networks delete microseg --quiet
ERROR: ... The network resource 'microseg' is already being used by 'firewall/...'
```

Delete dependents first (as above), then the network.

**Cleanup.** This is the cleanup.

## Operational lessons for production

- **Least privilege by identity, not IP.** SG references, ASGs, and service accounts survive scaling and re-addressing; CIDR rules rot.
- **Default-deny the network floor.** Custom-mode VPCs (GCP) and removing `AllowVnetInBound` overrides (Azure) start you at deny; AWS SGs are deny-by-default already.
- **Log before and after every change.** Chapter 08's loop is the safe way to tighten policy without outages.
- **Guardrails from above.** Hierarchical policies (GCP), Azure Policy, and AWS SCPs/Firewall Manager stop teams from re-opening what you closed.
- **Native + overlay.** Use native controls as the free, always-on floor; add a dedicated product (Volumes XCIII–CV) for workload identity, L7, or one policy across clouds.
- **Automate teardown.** In real accounts, tag lab resources and script their deletion so nothing lingers.

## Final Completion Checklist

- [ ] Spend checked against the budget.
- [ ] **AWS, Azure, and GCP resources fully deleted** for every cloud used.
- [ ] Accounts verified empty of billable resources.
- [ ] Operational lessons captured.
- [ ] Budget alerts left in place (free) as a safety net.
