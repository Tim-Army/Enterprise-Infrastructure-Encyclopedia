# Chapter 04: Azure — Network Security Groups and Application Security Groups

## Learning Objectives

- Build a VNet with three subnets and three free-tier VMs.
- Prove `hmi → db` lateral movement across a permissive default.
- Group NICs into **Application Security Groups (ASGs)** and write NSG rules **by ASG** — identity, not IP.
- Understand NSG **priority ordering** and the default rules that sit beneath yours.

## Prerequisites

Azure CLI authenticated (Chapter 02). All commands use `eastus`. Set up a resource group and helpers:

```bash
az group create -n microseg-lab-rg -l eastus -o table
RG=microseg-lab-rg ; LOC=eastus
MYIP=$(curl -s https://ifconfig.me)
```

## Hands-On Lab

### Exercise 4.1 — Build the VNet and subnets

**Objective.** Create `10.10.0.0/16` with app, db, and mgmt subnets.

**Walkthrough**

```bash
az network vnet create -g $RG -n microseg-vnet --address-prefix 10.10.0.0/16 \
    --subnet-name app --subnet-prefix 10.10.1.0/24 -o none
az network vnet subnet create -g $RG --vnet-name microseg-vnet -n db  --address-prefix 10.10.2.0/24 -o none
az network vnet subnet create -g $RG --vnet-name microseg-vnet -n mgmt --address-prefix 10.10.3.0/24 -o none
```

**Expected result.**

```bash
az network vnet subnet list -g $RG --vnet-name microseg-vnet --query '[].addressPrefix' -o tsv
10.10.1.0/24
10.10.2.0/24
10.10.3.0/24
```

**Negative test.**

```bash
az network vnet subnet create -g $RG --vnet-name microseg-vnet -n bad --address-prefix 10.10.1.0/24 -o none
... Subnet 'bad' is not valid because its IP address range overlaps ...
```

**Cleanup.** Deferred to Chapter 09.

### Exercise 4.2 — Launch three VMs

**Objective.** Create web, db, and hmi VMs on the free-tier `Standard_B1s` size.

**Walkthrough**

```bash
vm() { az vm create -g $RG -n $1 --image Ubuntu2204 --size Standard_B1s \
    --vnet-name microseg-vnet --subnet $2 --admin-username azure \
    --generate-ssh-keys --public-ip-sku Standard -o none && echo "$1 up"; }
vm web  app
vm db   db
vm hmi  mgmt
```

**Cost note.** `B1s` is free-tier-eligible (750 hours/month for 12 months), but three VMs plus their public IPs and disks can exceed the allowance. Tear down promptly (Chapter 09).

Open SSH from your IP on each VM's auto-created NSG, then install PostgreSQL on `db`:

```bash
for N in web db hmi; do az network nsg rule create -g $RG --nsg-name ${N}NSG \
    -n ssh --priority 200 --access Allow --protocol Tcp --destination-port-ranges 22 \
    --source-address-prefixes $MYIP -o none; done

DBIP=$(az vm show -g $RG -n db -d --query publicIps -o tsv)
ssh azure@$DBIP \
    'sudo apt-get update -qq && sudo apt-get install -y postgresql >/dev/null && \
     echo "listen_addresses='"'"'*'"'"'" | sudo tee -a /etc/postgresql/14/main/postgresql.conf && \
     echo "host all all 10.10.0.0/16 trust" | sudo tee -a /etc/postgresql/14/main/pg_hba.conf && \
     sudo systemctl restart postgresql'
```

**Expected result.**

```bash
az vm list -g $RG -d --query '[].{n:name,state:powerState}' -o table
N    State
---  ----------
web  VM running
db   VM running
hmi  VM running
```

**Cleanup.** Deferred to Chapter 09.

### Exercise 4.3 — Prove the lateral movement

**Objective.** Show `hmi → db:5432` succeeds across the permissive default.

**Walkthrough**
By default a VNet allows all intra-VNet traffic (`AllowVnetInBound`, priority 65000). Get private IPs and test:

```bash
DBPRIV=$(az vm show -g $RG -n db --query 'privateIps' -d -o tsv)
HMIP=$(az vm show -g $RG -n hmi -d --query publicIps -o tsv)
WEBIP=$(az vm show -g $RG -n web -d --query publicIps -o tsv)

ssh azure@$HMIP "timeout 5 bash -c '</dev/tcp/$DBPRIV/5432 && echo OPEN'"
OPEN
ssh azure@$WEBIP "timeout 5 bash -c '</dev/tcp/$DBPRIV/5432 && echo OPEN'"
OPEN
```

**Expected result.** Both `OPEN`. The default `AllowVnetInBound` rule is the flat network.

**Negative test.** The rule that permits this is visible and, importantly, sits at priority 65000 — anything you write with a lower number overrides it:

```bash
az network nsg rule list -g $RG --nsg-name dbNSG --include-default \
    --query "[?name=='AllowVnetInBound'].{p:priority,access:access}" -o tsv
65000   Allow
```

**Cleanup.** None.

### Exercise 4.4 — Segment by Application Security Group

**Objective.** Put each VM's NIC into an ASG and write an NSG rule that permits 5432 to the **db ASG from the web ASG**, and denies mgmt.

**Walkthrough**
Create three ASGs and attach each NIC:

```bash
for A in web-asg db-asg hmi-asg; do az network asg create -g $RG -n $A -o none; done
nic() { az vm show -g $RG -n $1 --query 'networkProfile.networkInterfaces[0].id' -o tsv; }
ipcfg() { az network nic show --ids $(nic $1) --query 'ipConfigurations[0].name' -o tsv; }
attach() { az network nic ip-config update --ids $(nic $1) -n $(ipcfg $1) \
    --application-security-groups $2 -o none; }
attach web web-asg ; attach db db-asg ; attach hmi hmi-asg
```

Write the identity rules on the db subnet's NSG. Lower priority number wins; deny mgmt above the allow, and both above the default `AllowVnetInBound`:

```bash
az network nsg rule create -g $RG --nsg-name dbNSG -n deny-mgmt --priority 100 \
    --access Deny --protocol Tcp --destination-port-ranges 5432 \
    --source-asgs hmi-asg --destination-asgs db-asg -o none
az network nsg rule create -g $RG --nsg-name dbNSG -n allow-web --priority 110 \
    --access Allow --protocol Tcp --destination-port-ranges 5432 \
    --source-asgs web-asg --destination-asgs db-asg -o none
```

The rules read **"deny 5432 to db-asg from hmi-asg"** and **"allow 5432 to db-asg from web-asg."** No IPs — pure identity.

**Expected result.**

```bash
az network nsg rule list -g $RG --nsg-name dbNSG \
    --query "[?destinationPortRange=='5432'].{n:name,p:priority,a:access}" -o table
N          P    A
---------  ---  ------
deny-mgmt  100  Deny
allow-web  110  Allow

ssh azure@$WEBIP "timeout 5 bash -c '</dev/tcp/$DBPRIV/5432 && echo OPEN' || echo BLOCKED"
OPEN
ssh azure@$HMIP  "timeout 5 bash -c '</dev/tcp/$DBPRIV/5432 && echo OPEN' || echo BLOCKED"
BLOCKED
```

**Negative test — priority inversion.** Swap the priorities so `allow-web` is broader than intended by lowering `deny-mgmt` below the allow, and observe the ordering bite. Re-create `deny-mgmt` at priority 120 (below `allow-web` at 110):

```bash
az network nsg rule delete -g $RG --nsg-name dbNSG -n deny-mgmt -o none
az network nsg rule create -g $RG --nsg-name dbNSG -n deny-mgmt --priority 120 \
    --access Deny --protocol Tcp --destination-port-ranges 5432 \
    --source-asgs hmi-asg --destination-asgs db-asg -o none
```

This still blocks `hmi` because the source ASG is specific, but it teaches the rule: **the first matching rule by ascending priority wins** — always place a specific deny above a broad allow. Restore `deny-mgmt` to priority 100 when done.

**Cleanup.** Keep the ASGs and rules for Chapter 06; teardown is Chapter 09.

## Summary and Completion Checklist

- [ ] VNet, three subnets, three VMs built.
- [ ] Lateral `hmi → db` demonstrated across `AllowVnetInBound`.
- [ ] Database segmented by **ASG-to-ASG** NSG rules (identity, not IP).
- [ ] NSG priority ordering and default rules understood.
- [ ] Estate left running for Chapter 06.
