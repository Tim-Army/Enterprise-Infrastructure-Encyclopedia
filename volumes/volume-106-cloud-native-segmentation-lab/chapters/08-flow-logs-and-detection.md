# Chapter 08: Flow Logs and Detection

## Learning Objectives

- Enable native flow logging on each cloud you built.
- Read a flow record and locate the `hmi → db` denial you created.
- Understand the difference between *allowed* and *denied/rejected* flow records.
- Use flow logs to write policy from observed traffic — the same "observe then enforce" loop the agent-based products automate.

## Why flow logs matter to segmentation

Every segmentation decision should be evidence-based. Before you deny a flow you want proof it is unused; after you deny it you want proof the denial is working and nothing legitimate broke. Native flow logs give you both, for free (you pay only for the log storage). This chapter turns on logging and reads back the exact denial from the per-cloud chapters.

## Hands-On Lab

### Exercise 8.1 — AWS VPC Flow Logs

**Objective.** Log rejected traffic to CloudWatch and find the `hmi → db:5432` REJECT.

**Walkthrough**
Create a log group, a role, and a flow log capturing **rejected** traffic:

```bash
aws logs create-log-group --log-group-name /vpc/microseg
aws ec2 create-flow-logs --resource-type VPC --resource-ids $VPC \
    --traffic-type REJECT --log-group-name /vpc/microseg \
    --deliver-logs-permission-arn arn:aws:iam::123456789012:role/flowlogsRole
```

Regenerate the denied flow from `hmi`, wait for delivery (~1–2 min), then query:

```bash
ssh -i lab.pem ec2-user@$HMIP "timeout 3 bash -c '</dev/tcp/$DBPRIV/5432' 2>/dev/null; true"
aws logs filter-log-events --log-group-name /vpc/microseg \
    --filter-pattern '"5432" "REJECT"' --query 'events[-1].message' --output text
2 123456789012 eni-hmi 10.10.3.x 10.10.2.y 49512 5432 6 1 40 ... REJECT OK
```

**Expected result.** A REJECT record for destination port 5432 from the mgmt subnet address — the very lateral flow you blocked, now visible as a denial.

**Negative test.** The legitimate `web → db` flow does **not** appear in a REJECT-only log:

```bash
ssh -i lab.pem ec2-user@$WEBIP "timeout 3 bash -c '</dev/tcp/$DBPRIV/5432'; true"
aws logs filter-log-events --log-group-name /vpc/microseg \
    --filter-pattern '"5432" "ACCEPT"' --query 'events' --output text
# empty — this log captures REJECT only; switch traffic-type to ALL to see accepts
```

**Cleanup.** Flow logs and the log group are deleted in Chapter 09.

### Exercise 8.2 — Azure NSG / VNet Flow Logs

**Objective.** Enable VNet flow logs and confirm the deny rule is counted.

**Walkthrough**
Azure's current model is **VNet flow logs** (the successor to NSG flow logs) delivered to a storage account, analyzed with Traffic Analytics. Enable via Network Watcher:

```bash
az storage account create -g microseg-lab-rg -n microsegflow$RANDOM -l eastus --sku Standard_LRS -o none
SA=$(az storage account list -g microseg-lab-rg --query "[?starts_with(name,'microsegflow')].id" -o tsv)
az network watcher flow-log create -l eastus -g microseg-lab-rg \
    --name dbflow --vnet microseg-vnet --storage-account $SA --enabled true -o none
```

Regenerate the denied flow, then inspect the effective rules that produced the drop:

```bash
NIC=$(az vm show -g microseg-lab-rg -n db --query 'networkProfile.networkInterfaces[0].id' -o tsv)
az network nic list-effective-nsg --ids $NIC \
    --query "value[0].effectiveSecurityRules[?destinationPortRange=='5432'].{n:name,a:access}" -o table
N          A
---------  ------
deny-mgmt  Deny
allow-web  Allow
```

**Expected result.** The effective ruleset shows `deny-mgmt` (Deny) above `allow-web` (Allow) on 5432; the flow log storage account begins receiving records within a few minutes.

**Negative test.** Disable the flow log and confirm collection stops:

```bash
az network watcher flow-log update -l eastus -g microseg-lab-rg --name dbflow --enabled false -o none
az network watcher flow-log show -l eastus -g microseg-lab-rg --name dbflow --query enabled -o tsv
false
```

**Cleanup.** The storage account and flow log are removed in Chapter 09.

### Exercise 8.3 — GCP Firewall Rules Logging

**Objective.** Enable logging on the deny rule and read the denied connection in Cloud Logging.

**Walkthrough**
Turn on logging for the deny rule you built in Chapter 05, regenerate the flow, and query:

```bash
gcloud compute firewall-rules update deny-any-db-sa --enable-logging
gcloud compute ssh hmi --zone=us-central1-a --command \
    "timeout 3 bash -c '</dev/tcp/$DBPRIV/5432' 2>/dev/null; true"

gcloud logging read \
  'resource.type=gce_subnetwork AND jsonPayload.rule_details.action=DENY AND jsonPayload.connection.dest_port=5432' \
  --limit=1 --format='value(jsonPayload.connection.src_ip, jsonPayload.rule_details.reference)'
10.10.3.x   network:microseg/firewall:deny-any-db-sa
```

**Expected result.** A DENY log entry naming the source (mgmt address) and the exact rule (`deny-any-db-sa`) that dropped it.

**Negative test.** Query for the `web → db` allow with logging enabled on the allow rule — it appears as ALLOW, confirming logs distinguish permitted from denied:

```bash
gcloud compute firewall-rules update allow-web-db-sa --enable-logging
gcloud compute ssh web --zone=us-central1-a --command "timeout 3 bash -c '</dev/tcp/$DBPRIV/5432'; true"
gcloud logging read 'jsonPayload.rule_details.action=ALLOW AND jsonPayload.connection.dest_port=5432' \
    --limit=1 --format='value(jsonPayload.rule_details.reference)'
network:microseg/firewall:allow-web-db-sa
```

**Cleanup.** Logging is disabled implicitly when the rules are deleted in Chapter 09.

## Observe, then enforce

You have now closed the loop the dedicated products automate: turn on logging, watch what actually flows, keep the legitimate paths, deny the rest, and confirm the denial in the log. On native controls this is a manual loop; the value proposition of an Illumio or a Guardicore (Volumes XCIV–XCV) is that it draws the traffic map and *proposes* the ruleset for you. The mechanics you just practiced are the same — only the automation differs.

## Summary and Completion Checklist

- [ ] Flow logging enabled on each cloud you built.
- [ ] The `hmi → db` denial located in the flow record.
- [ ] Allowed vs denied records distinguished.
- [ ] The observe-then-enforce loop understood as the manual form of what agent products automate.
