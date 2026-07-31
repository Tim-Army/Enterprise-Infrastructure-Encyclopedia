# Chapter 05: GCP — VPC Firewall Rules, Tags, and Service Accounts

## Learning Objectives

- Build a custom-mode VPC with three subnets and three free-tier instances.
- Prove `hmi → db` lateral movement across the default `allow-internal` rule.
- Segment with **firewall rules targeting network tags**, then upgrade to the stronger **service-account** target.
- Understand GCP's network-wide, priority-ordered firewall model versus AWS/Azure's per-NIC model.

## Prerequisites

gcloud authenticated with the lab project (Chapter 02). All commands use `us-central1`.

```bash
PROJECT=$(gcloud config get-value project)
gcloud config set compute/region us-central1
MYIP=$(curl -s https://ifconfig.me)
```

## Hands-On Lab

### Exercise 5.1 — Build the VPC and subnets

**Objective.** Create a custom-mode VPC `microseg` with three subnets.

**Walkthrough**

```bash
gcloud compute networks create microseg --subnet-mode=custom
gcloud compute networks subnets create app  --network=microseg --range=10.10.1.0/24 --region=us-central1
gcloud compute networks subnets create db   --network=microseg --range=10.10.2.0/24 --region=us-central1
gcloud compute networks subnets create mgmt --network=microseg --range=10.10.3.0/24 --region=us-central1
```

**Expected result.**

```bash
gcloud compute networks subnets list --network=microseg --format='value(name,ipCidrRange)'
app   10.10.1.0/24
db    10.10.2.0/24
mgmt  10.10.3.0/24
```

**Negative test.**

```bash
gcloud compute networks subnets create dup --network=microseg --range=10.10.1.0/24 --region=us-central1
ERROR: ... Invalid IP CIDR range: 10.10.1.0/24 conflicts with ...
```

**Cleanup.** Deferred to Chapter 09.

### Exercise 5.2 — Launch three instances with tags and service accounts

**Objective.** Create web, db, and hmi `e2-micro` instances, each with a network tag **and** a dedicated service account.

**Walkthrough**
Create per-role service accounts (used as the stronger firewall target later):

```bash
for R in web db hmi; do gcloud iam service-accounts create $R-sa \
    --display-name="$R"; done
SA() { echo "$1-sa@$PROJECT.iam.gserviceaccount.com"; }
```

Launch, tagging each instance and binding its service account:

```bash
vm() { gcloud compute instances create $1 --zone=us-central1-a --machine-type=e2-micro \
    --subnet=$2 --tags=$1 --service-account=$(SA $1) \
    --scopes=cloud-platform --image-family=debian-12 --image-project=debian-cloud; }
vm web  app
vm db   db
vm hmi  mgmt
```

**Cost note.** `e2-micro` in select US regions is free-tier (one per month). Three instances exceed the single-instance allowance — tear down promptly (Chapter 09).

Add SSH-from-your-IP and install PostgreSQL on `db`:

```bash
gcloud compute firewall-rules create allow-ssh --network=microseg \
    --allow=tcp:22 --source-ranges=$MYIP/32
gcloud compute ssh db --zone=us-central1-a --command \
    'sudo apt-get update -qq && sudo apt-get install -y postgresql >/dev/null && \
     echo "listen_addresses='"'"'*'"'"'" | sudo tee -a /etc/postgresql/15/main/postgresql.conf && \
     echo "host all all 10.10.0.0/16 trust" | sudo tee -a /etc/postgresql/15/main/pg_hba.conf && \
     sudo systemctl restart postgresql'
```

**Expected result.**

```bash
gcloud compute instances list --format='value(name,status)'
web   RUNNING
db    RUNNING
hmi   RUNNING
```

**Cleanup.** Deferred to Chapter 09.

### Exercise 5.3 — Prove the lateral movement

**Objective.** Show `hmi → db:5432` succeeds under the implicit flat network.

**Walkthrough**
A custom-mode VPC has **no** automatic `allow-internal` rule, so first reproduce the "flat" default that auto-mode VPCs ship with — a broad intra-VPC allow:

```bash
gcloud compute firewall-rules create allow-internal --network=microseg \
    --allow=tcp,udp,icmp --source-ranges=10.10.0.0/16
DBPRIV=$(gcloud compute instances describe db --zone=us-central1-a \
    --format='value(networkInterfaces[0].networkIP)')
gcloud compute ssh hmi --zone=us-central1-a --command \
    "timeout 5 bash -c '</dev/tcp/$DBPRIV/5432 && echo OPEN'"
OPEN
```

**Expected result.** `OPEN` from `hmi` — the broad `allow-internal` rule is the flat network.

**Negative test.** `web` reaches it too (legitimate):

```bash
gcloud compute ssh web --zone=us-central1-a --command \
    "timeout 5 bash -c '</dev/tcp/$DBPRIV/5432 && echo OPEN'"
OPEN
```

**Cleanup.** None.

### Exercise 5.4 — Segment with tag-targeted, then service-account-targeted rules

**Objective.** Restrict 5432 to `db` so only `web` may reach it, first by network tag, then by the stronger service-account identity.

**Walkthrough**
GCP firewall rules are **network-wide and priority-ordered** (lower number wins; default priority 1000). Remove the broad allow's coverage of 5432 by adding a **higher-priority deny** for mgmt and a targeted allow for web. First, tag-based:

```bash
# Deny mgmt->db:5432 (priority 900, beats allow-internal at 1000)
gcloud compute firewall-rules create deny-hmi-db --network=microseg --priority=900 \
    --direction=INGRESS --action=DENY --rules=tcp:5432 \
    --source-tags=hmi --target-tags=db
# Allow web->db:5432 (priority 800)
gcloud compute firewall-rules create allow-web-db --network=microseg --priority=800 \
    --direction=INGRESS --action=ALLOW --rules=tcp:5432 \
    --source-tags=web --target-tags=db
```

Read: **"deny 5432 to tag `db` from tag `hmi`"** and **"allow 5432 to tag `db` from tag `web`."**

**Upgrade to service accounts.** Tags can be set by anyone who can edit an instance; a service account is a harder identity to forge. Replace the tag rules with SA-targeted ones:

```bash
gcloud compute firewall-rules create allow-web-db-sa --network=microseg --priority=790 \
    --direction=INGRESS --action=ALLOW --rules=tcp:5432 \
    --source-service-accounts=$(SA web) --target-service-accounts=$(SA db)
gcloud compute firewall-rules create deny-any-db-sa --network=microseg --priority=910 \
    --direction=INGRESS --action=DENY --rules=tcp:5432 \
    --target-service-accounts=$(SA db)
```

Now the database's own service-account identity gates it: only the web service account is allowed; everything else (including `hmi`) is denied at priority 910, beneath the web allow at 790.

**Expected result.**

```bash
gcloud compute ssh web --zone=us-central1-a --command \
    "timeout 5 bash -c '</dev/tcp/$DBPRIV/5432 && echo OPEN' || echo BLOCKED"
OPEN
gcloud compute ssh hmi --zone=us-central1-a --command \
    "timeout 5 bash -c '</dev/tcp/$DBPRIV/5432 && echo OPEN' || echo BLOCKED"
BLOCKED
```

**Negative test — priority proves the model.** Raise the deny above the allow to show ordering controls the outcome:

```bash
gcloud compute firewall-rules update deny-any-db-sa --priority=700
gcloud compute ssh web --zone=us-central1-a --command \
    "timeout 5 bash -c '</dev/tcp/$DBPRIV/5432 && echo OPEN' || echo BLOCKED"
BLOCKED
```

Now even `web` is blocked, because the deny (700) beats the allow (790). Restore `deny-any-db-sa` to priority 910. This is GCP's whole model in one experiment: **priority, not specificity, decides.**

**Cleanup.** Keep the rules for Chapter 06; teardown is Chapter 09.

## Summary and Completion Checklist

- [ ] Custom VPC, three subnets, three instances built.
- [ ] Lateral `hmi → db` demonstrated across a broad `allow-internal`.
- [ ] Database segmented by **network tags**, then by the stronger **service-account** target.
- [ ] GCP's network-wide, priority-ordered model understood.
- [ ] Estate left running for Chapter 06.
