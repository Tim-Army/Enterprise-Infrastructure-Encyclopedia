# Chapter 03: AWS — Security Groups and Network ACLs

## Learning Objectives

- Build a VPC with three subnets and three free-tier instances.
- Prove that a permissive security group allows `hmi → db` lateral movement.
- Segment the database with a **security group that references another security group** — identity, not IP.
- Add a **stateless Network ACL** as subnet-level defense in depth, and survive its return-traffic trap.

## Prerequisites

CLI authenticated (Chapter 02). All commands use `us-east-1`. Export a couple of helpers:

```bash
export AWS_DEFAULT_REGION=us-east-1
MYIP=$(curl -s https://checkip.amazonaws.com)/32 ; echo "$MYIP"
203.0.113.10/32
```

## Hands-On Lab

### Exercise 3.1 — Build the VPC and subnets

**Objective.** Create `10.10.0.0/16` with app, db, and mgmt subnets and internet access.

**Walkthrough**

```bash
VPC=$(aws ec2 create-vpc --cidr-block 10.10.0.0/16 \
    --tag-specifications 'ResourceType=vpc,Tags=[{Key=Name,Value=microseg}]' \
    --query 'Vpc.VpcId' --output text) ; echo "$VPC"
vpc-0a1b2c3d4e5f

APP=$(aws ec2 create-subnet --vpc-id $VPC --cidr-block 10.10.1.0/24 \
    --query 'Subnet.SubnetId' --output text)
DB=$(aws ec2 create-subnet --vpc-id $VPC --cidr-block 10.10.2.0/24 \
    --query 'Subnet.SubnetId' --output text)
MGMT=$(aws ec2 create-subnet --vpc-id $VPC --cidr-block 10.10.3.0/24 \
    --query 'Subnet.SubnetId' --output text)

IGW=$(aws ec2 create-internet-gateway --query 'InternetGateway.InternetGatewayId' --output text)
aws ec2 attach-internet-gateway --vpc-id $VPC --internet-gateway-id $IGW
RT=$(aws ec2 create-route-table --vpc-id $VPC --query 'RouteTable.RouteTableId' --output text)
aws ec2 create-route --route-table-id $RT --destination-cidr-block 0.0.0.0/0 --gateway-id $IGW >/dev/null
for S in $APP $DB $MGMT; do aws ec2 associate-route-table --subnet-id $S --route-table-id $RT >/dev/null; \
    aws ec2 modify-subnet-attribute --subnet-id $S --map-public-ip-on-launch; done
```

**Expected result.**

```bash
aws ec2 describe-subnets --filters Name=vpc-id,Values=$VPC \
    --query 'Subnets[].CidrBlock' --output text
10.10.1.0/24    10.10.2.0/24    10.10.3.0/24
```

**Negative test.**

```bash
aws ec2 create-subnet --vpc-id $VPC --cidr-block 10.10.1.0/24
An error occurred (InvalidSubnet.Conflict) ... overlaps with another subnet
```

Overlap is rejected — the VPC enforces non-overlapping subnets.

**Rollback.** Deferred to Chapter 09 (the estate must persist across this chapter).

### Exercise 3.2 — Launch three instances behind one permissive SG

**Objective.** Launch web, db, and hmi with a single wide-open security group — the flat network.

**Walkthrough**
Create a key pair and a permissive SG (allow all traffic within the VPC + SSH from your IP):

```bash
aws ec2 create-key-pair --key-name lab --query 'KeyMaterial' --output text > lab.pem
chmod 400 lab.pem
FLAT=$(aws ec2 create-security-group --group-name flat --description "permissive" \
    --vpc-id $VPC --query 'GroupId' --output text)
aws ec2 authorize-security-group-ingress --group-id $FLAT \
    --protocol tcp --port 22 --cidr $MYIP >/dev/null
aws ec2 authorize-security-group-ingress --group-id $FLAT \
    --protocol -1 --cidr 10.10.0.0/16 >/dev/null      # ALL protocols, intra-VPC
```

Find the current Amazon Linux 2023 AMI and launch:

```bash
AMI=$(aws ssm get-parameter \
    --name /aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64 \
    --query 'Parameter.Value' --output text)

launch() { aws ec2 run-instances --image-id $AMI --instance-type t3.micro \
    --key-name lab --security-group-ids $FLAT --subnet-id $2 \
    --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=$1}]" \
    --query 'Instances[0].InstanceId' --output text; }
WEB=$(launch web  $APP)
DBI=$(launch db   $DB)
HMI=$(launch hmi  $MGMT)
```

**Cost note.** Three `t3.micro` instances run here. Free tier covers 750 hours/month of one `t2.micro`/`t3.micro`; three instances may exceed it. Tear down promptly.

On `db`, install PostgreSQL (SSH in using its public IP):

```bash
DBIP=$(aws ec2 describe-instances --instance-ids $DBI \
    --query 'Reservations[0].Instances[0].PublicIpAddress' --output text)
ssh -i lab.pem ec2-user@$DBIP \
    'sudo dnf install -y postgresql15-server >/dev/null && \
     sudo postgresql-setup --initdb >/dev/null && \
     echo "listen_addresses='"'"'*'"'"'" | sudo tee -a /var/lib/pgsql/data/postgresql.conf && \
     echo "host all all 10.10.0.0/16 trust" | sudo tee -a /var/lib/pgsql/data/pg_hba.conf && \
     sudo systemctl enable --now postgresql'
```

**Expected result.**

```bash
aws ec2 describe-instances --filters Name=vpc-id,Values=$VPC \
    --query 'Reservations[].Instances[].[Tags[?Key==`Name`]|[0].Value,State.Name]' --output text
web  running
db   running
hmi  running
```

**Negative test.**

```bash
aws ec2 run-instances --image-id ami-000invalid --instance-type t3.micro
An error occurred (InvalidAMIID.NotFound) ...
```

**Rollback.** Deferred to Chapter 09.

### Exercise 3.3 — Prove the lateral movement

**Objective.** Show that with the flat SG, the operator (`hmi`) reaches the database — the flow to eliminate.

**Walkthrough**
Get private IPs, then test from `hmi` to `db:5432`:

```bash
priv() { aws ec2 describe-instances --instance-ids $1 \
    --query 'Reservations[0].Instances[0].PrivateIpAddress' --output text; }
DBPRIV=$(priv $DBI) ; HMIP=$(aws ec2 describe-instances --instance-ids $HMI \
    --query 'Reservations[0].Instances[0].PublicIpAddress' --output text)

ssh -i lab.pem ec2-user@$HMIP "timeout 5 bash -c '</dev/tcp/$DBPRIV/5432 && echo OPEN'"
OPEN
```

**Expected result.** `OPEN` — the operator workstation can open the database port. This is the lateral path.

**Negative test.** The web tier *should* reach the database (legitimate):

```bash
WEBIP=$(aws ec2 describe-instances --instance-ids $WEB \
    --query 'Reservations[0].Instances[0].PublicIpAddress' --output text)
ssh -i lab.pem ec2-user@$WEBIP "timeout 5 bash -c '</dev/tcp/$DBPRIV/5432 && echo OPEN'"
OPEN
```

Both work now. The goal: keep `web → db` open while closing `hmi → db`.

**Rollback.** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Exercise 3.4 — Segment with security groups that reference each other

**Objective.** Replace the flat SG with three role SGs so the database accepts 5432 **only from the web SG**.

**Walkthrough**
Create a security group per role:

```bash
sg() { aws ec2 create-security-group --group-name $1 --description $1 \
    --vpc-id $VPC --query 'GroupId' --output text; }
WEBSG=$(sg web-sg) ; DBSG=$(sg db-sg) ; HMISG=$(sg hmi-sg)
```

Allow SSH to each from your IP, then the **identity-based** database rule — source is the *web SG*, not a CIDR:

```bash
for G in $WEBSG $DBSG $HMISG; do \
    aws ec2 authorize-security-group-ingress --group-id $G --protocol tcp --port 22 --cidr $MYIP >/dev/null; done

aws ec2 authorize-security-group-ingress --group-id $DBSG \
    --protocol tcp --port 5432 --source-group $WEBSG >/dev/null
```

Read that last rule as **"the database permits 5432 from anything wearing the web security group."** No IP appears; instances can scale and re-address and the rule still holds.

Now move each instance onto its role SG (replacing the flat SG):

```bash
aws ec2 modify-instance-attribute --instance-id $WEB --groups $WEBSG
aws ec2 modify-instance-attribute --instance-id $DBI --groups $DBSG
aws ec2 modify-instance-attribute --instance-id $HMI --groups $HMISG
```

**Expected result.** The database rule references the web SG:

```bash
aws ec2 describe-security-groups --group-ids $DBSG \
    --query 'SecurityGroups[0].IpPermissions[?FromPort==`5432`].UserIdGroupPairs[].GroupId' --output text
sg-<WEBSG id>
```

`web → db` still succeeds; `hmi → db` now fails:

```bash
ssh -i lab.pem ec2-user@$WEBIP "timeout 5 bash -c '</dev/tcp/$DBPRIV/5432 && echo OPEN' || echo BLOCKED"
OPEN
ssh -i lab.pem ec2-user@$HMIP "timeout 5 bash -c '</dev/tcp/$DBPRIV/5432 && echo OPEN' || echo BLOCKED"
BLOCKED
```

The lateral path is closed by identity; the legitimate path is untouched.

**Negative test.** Try to reach 5432 from `hmi` by IP-spoofing intent — there is no rule to add short of re-widening the group. Confirm the implicit deny is doing the work:

```bash
aws ec2 describe-security-groups --group-ids $DBSG \
    --query 'SecurityGroups[0].IpPermissions[?FromPort==`5432`].IpRanges' --output text
# empty — no CIDR grants 5432; only the web SG does
```

**Rollback.** Keep the role SGs for Chapter 06 (comparison) and Chapter 09 (teardown).

### Exercise 3.5 — Defense in depth with a stateless Network ACL

**Objective.** Add a subnet-level NACL on the db subnet that denies the mgmt subnet — and learn the stateless return-traffic trap first-hand.

**Walkthrough**
Security groups already contain the lateral flow; a NACL adds a **coarse, subnet-wide** second layer that a misconfigured SG cannot undo. Create a NACL, associate the db subnet, and write numbered rules:

```bash
NACL=$(aws ec2 create-network-acl --vpc-id $VPC --query 'NetworkAcl.NetworkAclId' --output text)
ASSOC=$(aws ec2 describe-network-acls --filters Name=association.subnet-id,Values=$DB \
    --query 'NetworkAcls[0].Associations[?SubnetId==`'"$DB"'`].NetworkAclAssociationId' --output text)
aws ec2 replace-network-acl-association --association-id $ASSOC --network-acl-id $NACL >/dev/null
```

Ingress: **deny the mgmt subnet first (lower number wins)**, then allow the app subnet to 5432:

```bash
aws ec2 create-network-acl-entry --network-acl-id $NACL --rule-number 90 --protocol -1 \
    --rule-action deny --ingress --cidr-block 10.10.3.0/24
aws ec2 create-network-acl-entry --network-acl-id $NACL --rule-number 100 --protocol tcp \
    --port-range From=5432,To=5432 --rule-action allow --ingress --cidr-block 10.10.1.0/24
```

**The stateless trap.** NACLs do not track connections. Without an egress rule for the **return traffic** (ephemeral ports back to the client), even allowed inbound connections hang. Add it:

```bash
aws ec2 create-network-acl-entry --network-acl-id $NACL --rule-number 100 --protocol tcp \
    --port-range From=1024,To=65535 --rule-action allow --egress --cidr-block 10.10.1.0/24
```

**Expected result.** `web → db` still works (ingress 5432 allowed **and** egress ephemeral allowed); `hmi → db` is denied at the subnet edge even before the SG is consulted:

```bash
ssh -i lab.pem ec2-user@$WEBIP "timeout 5 bash -c '</dev/tcp/$DBPRIV/5432 && echo OPEN' || echo BLOCKED"
OPEN
ssh -i lab.pem ec2-user@$HMIP "timeout 5 bash -c '</dev/tcp/$DBPRIV/5432 && echo OPEN' || echo BLOCKED"
BLOCKED
```

**Negative test — reproduce the trap deliberately.** Delete the egress return rule and watch even the legitimate flow break:

```bash
aws ec2 delete-network-acl-entry --network-acl-id $NACL --rule-number 100 --egress
ssh -i lab.pem ec2-user@$WEBIP "timeout 5 bash -c '</dev/tcp/$DBPRIV/5432 && echo OPEN' || echo BLOCKED"
BLOCKED
```

`web → db` now fails **despite the ingress allow**, because the reply cannot leave. Re-add the egress rule to restore it. This is the number-one NACL mistake — SGs never have it because they are stateful.

**Rollback.** Restore the egress rule if you removed it. Full teardown is Chapter 09.

## Summary and Completion Checklist

- [ ] VPC, three subnets, three instances built.
- [ ] Lateral `hmi → db` demonstrated on the flat SG.
- [ ] Database segmented by a **web-SG-referencing** rule (identity, not IP).
- [ ] NACL added as stateless subnet defense; the return-traffic trap reproduced and fixed.
- [ ] Estate left running for Chapter 06; teardown scheduled for Chapter 09.
