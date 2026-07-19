# Chapter 03: Secure Networking, Hybrid Connectivity, and Edge

## Learning Objectives

- Design a multi-AZ Amazon VPC with public, private, and isolated subnet
  tiers, and explain how route tables determine each tier's reachability.
- Distinguish security groups from network ACLs and apply each at the
  correct layer of a defense-in-depth network design.
- Choose correctly among VPC peering, AWS Transit Gateway, and AWS
  PrivateLink for a given inter-VPC or service-exposure requirement.
- Compare AWS Site-to-Site VPN and AWS Direct Connect for hybrid
  connectivity, including resiliency models for each.
- Configure edge and global network services — Amazon Route 53, Amazon
  CloudFront, AWS Global Accelerator, and AWS WAF — for a public-facing
  workload.
- Use the VPC Reachability Analyzer and VPC Flow Logs to diagnose
  connectivity failures methodically rather than by trial and error.

## Theory and Architecture

A **Virtual Private Cloud (VPC)** is a logically isolated, customer-defined
network inside an AWS Region. A VPC is assigned one or more IPv4 CIDR
blocks (and optionally an IPv6 block) and is subdivided into **subnets**,
each of which lives entirely within a single Availability Zone. Because a
subnet cannot span AZs, high-availability designs always provision at least
two subnets per tier — one per AZ — with identical route table semantics so
that either AZ can serve traffic if the other fails.

### Subnet tiers and routing

Enterprise VPC designs converge on three subnet tiers, distinguished purely
by their route table, not by any AWS-enforced boundary:

| Tier | Route to internet | Typical contents |
| --- | --- | --- |
| Public | Route `0.0.0.0/0` to an Internet Gateway (IGW) | Load balancers, NAT gateways, bastion/session-manager endpoints |
| Private | Route `0.0.0.0/0` to a NAT gateway in a public subnet | Application servers, ECS/EKS worker nodes, Lambda functions in a VPC |
| Isolated | No route to `0.0.0.0/0` at all | RDS/Aurora instances, ElastiCache, internal-only data stores |

A **route table** is the actual mechanism that makes a subnet "public" or
"private" — the label is a convention, not an AWS property. An **Internet
Gateway** is a horizontally scaled, highly available VPC component that
provides bidirectional internet access; a **NAT gateway** provides
outbound-only internet access for private-subnet resources by translating
their private addresses to its own Elastic IP, and it must itself sit in a
public subnet. This asymmetry — private subnets can reach out, nothing can
reach in — is the basic building block of the three-tier application
architecture used throughout [Chapter 04](04-compute-containers-serverless-and-application-architecture.md).

### Security groups vs. network ACLs

Two independent filtering layers apply to traffic inside a VPC, and
enterprise designs use both rather than choosing one:

| Construct | Applies to | State | Rule evaluation | Typical use |
| --- | --- | --- | --- | --- |
| Security group (SG) | Elastic network interface (ENI) | Stateful — return traffic is automatically allowed | Allow rules only; implicit deny | Primary, fine-grained control; SG-to-SG references express "only my load balancer can reach my app tier" without hardcoding CIDRs |
| Network ACL (NACL) | Subnet | Stateless — return traffic must be explicitly allowed | Allow and explicit deny, evaluated in numbered rule order | Coarse subnet-level guardrail; the only way to explicitly deny a specific CIDR regardless of any SG |

Because a security group can reference another security group as its
source/destination, well-designed VPCs express tier-to-tier trust in terms
of security group IDs (`sg-app` may receive port 443 only from `sg-alb`)
rather than CIDR ranges, which keeps the rule correct even as subnets or
instances change.

### VPC endpoints

A **VPC endpoint** lets resources in private or isolated subnets reach an
AWS service without traversing a NAT gateway or the public internet. There
are two kinds:

- **Gateway endpoints** — supported only for Amazon S3 and DynamoDB. A
  gateway endpoint is a route table target, not an ENI; it has no cost
  beyond normal data transfer.
- **Interface endpoints (AWS PrivateLink)** — an ENI with a private IP
  placed directly in your subnet, supported for most other AWS services
  (Secrets Manager, KMS, ECR, CloudWatch Logs, Systems Manager, and
  hundreds more) and for third-party SaaS services that publish a
  PrivateLink endpoint service. Interface endpoints incur an hourly charge
  per AZ plus data-processing charges.

### Connectivity mesh: peering, Transit Gateway, and PrivateLink

| Mechanism | Topology | Transitive routing | Typical scale |
| --- | --- | --- | --- |
| VPC peering | Point-to-point | No — each pair needs its own peering connection and route table entries | A handful of VPCs |
| AWS Transit Gateway (TGW) | Hub-and-spoke | Yes, governed by TGW route tables | Dozens to thousands of VPCs/accounts |
| AWS PrivateLink | Consumer-to-service, one-directional | N/A — exposes a single service, not a routed network | Many consumers of one shared service |

**VPC peering** connects exactly two VPCs with no transitive routing: if
VPC A peers with VPC B, and B peers with C, A still cannot reach C through
B. This makes peering unwieldy past a handful of VPCs, since the required
peering connections grow combinatorially. **AWS Transit Gateway** solves
this by acting as a Regional routing hub: each VPC, VPN connection, and
Direct Connect gateway attaches to the TGW once, and TGW route tables
control which attachments can reach which — including deliberately
non-transitive segmentation between spokes using separate TGW route tables
and selective route propagation. TGWs can be shared across accounts using
**AWS Resource Access Manager (RAM)**, which is how the Infrastructure OU's
network-hub account from [Chapter 02](02-multi-account-identity-governance-and-landing-zones.md) centrally owns a TGW that every
workload account attaches to.

**AWS PrivateLink** solves a different problem: exposing a specific service
(not a whole network) to many consumer VPCs, including consumers in other
AWS accounts or organizations, without any peering, route table exposure,
or CIDR overlap concern. A producer account creates a Network Load Balancer
in front of the service and registers it as an **endpoint service**;
consumers create an interface endpoint that resolves to a private IP in
their own VPC. This is the standard pattern for shared internal platform
services (a central logging ingestion API, a shared authentication service)
where the consuming teams should see only the service's IP, never the
producer's network.

### Hybrid connectivity

| Mechanism | Path | Typical bandwidth | Setup time | Encryption |
| --- | --- | --- | --- | --- |
| Site-to-Site VPN | IPsec tunnels over the public internet | Up to ~1.25 Gbps per tunnel | Minutes | Native IPsec |
| AWS Direct Connect | Dedicated fiber circuit to an AWS Direct Connect location | 50 Mbps–100 Gbps | Weeks (physical provisioning) | None by default — layer VPN or MACsec on top for encryption in transit |

**AWS Site-to-Site VPN** establishes IPsec tunnels between a customer
gateway (on-premises) and a virtual private gateway or Transit Gateway
(AWS side), typically provisioned as two tunnels for redundancy. It is fast
to stand up and requires no physical circuit, but its throughput and
latency are subject to the public internet path. **AWS Direct Connect**
provisions a dedicated, private network connection from a customer
location (or a Direct Connect Partner) into an AWS Direct Connect location,
bypassing the public internet entirely for lower, more consistent latency
and higher sustained throughput. A **Direct Connect gateway** lets a single
Direct Connect connection reach multiple VPCs across Regions and accounts,
mirroring the hub role Transit Gateway plays for VPC-to-VPC traffic. Direct
Connect traffic is not encrypted by default; enterprises requiring
encryption in transit over Direct Connect layer a VPN over the Direct
Connect private virtual interface (VIF) or use Direct Connect's native
MACsec support at supported locations. A common resilient pattern pairs a
primary Direct Connect connection with a Site-to-Site VPN as an automatic
failover path, since VPN requires no physical lead time.

### Edge and global network services

- **Amazon Route 53** is AWS's authoritative DNS service. Public hosted
  zones resolve internet-facing names; private hosted zones resolve names
  only within associated VPCs (and, via Route 53 Resolver, across
  accounts). Routing policies beyond simple A/CNAME records include
  **weighted** (percentage-based traffic splitting), **latency-based**
  (route to the Region with lowest measured latency), **geolocation**, and
  **failover** (active-passive with health checks) — failover routing is
  covered in depth as a DR mechanism in [Chapter 06](06-reliability-migration-multi-region-and-disaster-recovery.md).
- **Amazon CloudFront** is AWS's content delivery network (CDN), caching
  content at edge locations close to users and reducing load on origin
  infrastructure (S3, an ALB, or a non-AWS origin). An **Origin Access
  Control (OAC)** restricts an S3 origin bucket so it is reachable only
  through CloudFront, not directly over the public internet.
- **AWS Global Accelerator** improves availability and performance for
  non-HTTP or mixed-protocol workloads by anycasting two static IP
  addresses across the AWS global network edge and routing to the closest
  healthy endpoint, with faster failover than DNS-based routing changes
  because it does not depend on client-side DNS cache expiry.
- **AWS WAF** is a Layer 7 web application firewall attached to CloudFront,
  an Application Load Balancer, or API Gateway, evaluating requests against
  managed and custom rule groups (SQL injection, rate-based rules, IP
  reputation lists). **AWS Shield Standard** provides baseline DDoS
  protection automatically for every AWS customer; **AWS Shield Advanced**
  adds enhanced detection, cost protection against scaling charges incurred
  during an attack, and access to the AWS DDoS Response Team, and pairs
  with WAF for automated mitigation.

## Design Considerations

- **Plan CIDR allocation centrally before creating any VPC.** VPC peering
  and Transit Gateway routing both fail (or silently misroute) across
  overlapping CIDR blocks. Assign non-overlapping ranges from a
  centrally managed IP address plan — AWS IP Address Manager (IPAM) — for
  every account and Region before account vending, not after the first
  overlap conflict appears.
- **Reserve subnet capacity generously.** AWS reserves five IP addresses
  per subnet (network address, VPC router, DNS, future use, and broadcast
  reserved for consistency with older protocols). Size subnets for growth,
  particularly for EKS clusters, where each pod can consume an IP address
  under the default VPC CNI.
- **Centralized vs. distributed egress.** Deploying a NAT gateway per AZ
  per VPC is the highly available default but multiplies NAT gateway
  hourly and data-processing charges across dozens of workload accounts. A
  centralized egress VPC — reachable via Transit Gateway, running a shared
  set of NAT gateways or a fleet behind AWS Network Firewall for outbound
  inspection — trades some additional latency and a cross-account
  dependency for materially lower cost and a single point of egress policy
  enforcement.
- **SG-to-SG references over CIDR rules.** Referencing security groups by
  ID instead of hardcoding CIDR blocks keeps rules correct as
  infrastructure changes and makes intent self-documenting in the rule
  itself.
- **Direct Connect resiliency tier.** AWS's resiliency toolkit defines
  models from a single connection (no resiliency) through two connections
  at the same location, two connections at different locations, and four
  connections across two locations for maximum resiliency. Select the
  tier based on the workload's criticality, not on the lowest available
  price — a single Direct Connect connection is a single point of failure
  regardless of how reliable the underlying circuit is individually.
- **PrivateLink over peering for shared internal services.** When the goal
  is "let many consumers reach one service" rather than "let two networks
  freely route to each other," PrivateLink avoids CIDR overlap
  constraints, avoids exposing the producer's internal network topology,
  and scales to many more consumers than peering's linear connection
  growth allows.
- **Hybrid DNS requires Resolver endpoints.** On-premises resolvers cannot
  natively query VPC private hosted zones, and VPC resolvers cannot
  natively query on-premises DNS. Route 53 Resolver inbound and outbound
  endpoints bridge both directions, and Resolver rules control which
  domains are forwarded where.

## Implementation and Automation

### 1. Multi-AZ VPC with public and private subnets (Terraform)

```hcl
resource "aws_vpc" "main" {
  cidr_block           = "10.20.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = { Name = "prod-app-vpc" }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id
}

resource "aws_subnet" "public" {
  for_each                = { "a" = "10.20.0.0/24", "b" = "10.20.1.0/24" }
  vpc_id                  = aws_vpc.main.id
  cidr_block              = each.value
  availability_zone       = "us-east-1${each.key}"
  map_public_ip_on_launch = true
  tags = { Name = "public-${each.key}", Tier = "public" }
}

resource "aws_subnet" "private" {
  for_each          = { "a" = "10.20.10.0/24", "b" = "10.20.11.0/24" }
  vpc_id            = aws_vpc.main.id
  cidr_block        = each.value
  availability_zone = "us-east-1${each.key}"
  tags = { Name = "private-${each.key}", Tier = "private" }
}

resource "aws_eip" "nat" {
  for_each = aws_subnet.public
  domain   = "vpc"
}

resource "aws_nat_gateway" "nat" {
  for_each      = aws_subnet.public
  allocation_id = aws_eip.nat[each.key].id
  subnet_id     = each.value.id
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }
}

resource "aws_route_table" "private" {
  for_each = aws_subnet.private
  vpc_id   = aws_vpc.main.id
  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat[each.key].id
  }
}

resource "aws_route_table_association" "public" {
  for_each       = aws_subnet.public
  subnet_id      = each.value.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "private" {
  for_each       = aws_subnet.private
  subnet_id      = each.value.id
  route_table_id = aws_route_table.private[each.key].id
}
```

### 2. Security groups referencing each other

```hcl
resource "aws_security_group" "alb" {
  name   = "sg-alb"
  vpc_id = aws_vpc.main.id
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "app" {
  name   = "sg-app"
  vpc_id = aws_vpc.main.id
  ingress {
    from_port       = 8443
    to_port         = 8443
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

### 3. Transit Gateway with cross-account sharing (Terraform + CLI)

```hcl
resource "aws_ec2_transit_gateway" "hub" {
  description                    = "network-hub-tgw"
  default_route_table_association = "disable"
  default_route_table_propagation = "disable"
}

resource "aws_ram_resource_share" "tgw_share" {
  name                      = "tgw-share-workloads-ou"
  allow_external_principals = false
}

resource "aws_ram_resource_association" "tgw" {
  resource_arn       = aws_ec2_transit_gateway.hub.arn
  resource_share_arn = aws_ram_resource_share.tgw_share.arn
}

resource "aws_ram_principal_association" "workloads_ou" {
  principal          = "arn:aws:organizations::111122223333:ou/o-example/ou-workloads"
  resource_share_arn = aws_ram_resource_share.tgw_share.arn
}
```

```bash
# From a member/workload account, accept the shared TGW principal association
aws ec2 create-transit-gateway-vpc-attachment \
  --transit-gateway-id tgw-0abc123def456 \
  --vpc-id vpc-0123456789abcdef0 \
  --subnet-ids subnet-0a subnet-0b
```

### 4. Gateway and interface VPC endpoints

```hcl
resource "aws_vpc_endpoint" "s3" {
  vpc_id            = aws_vpc.main.id
  service_name      = "com.amazonaws.us-east-1.s3"
  vpc_endpoint_type = "Gateway"
  route_table_ids   = [for rt in aws_route_table.private : rt.id]
}

resource "aws_vpc_endpoint" "secretsmanager" {
  vpc_id              = aws_vpc.main.id
  service_name        = "com.amazonaws.us-east-1.secretsmanager"
  vpc_endpoint_type   = "Interface"
  subnet_ids          = [for s in aws_subnet.private : s.id]
  security_group_ids  = [aws_security_group.app.id]
  private_dns_enabled = true
}
```

### 5. Route 53 failover routing and a CloudFront distribution

```bash
aws route53 change-resource-record-sets \
  --hosted-zone-id "$ZONE_ID" \
  --change-batch '{
    "Changes": [{
      "Action": "UPSERT",
      "ResourceRecordSet": {
        "Name": "app.example.com",
        "Type": "A",
        "SetIdentifier": "primary",
        "Failover": "PRIMARY",
        "AliasTarget": {
          "HostedZoneId": "Z35SXDOTRQ7X7K",
          "DNSName": "primary-alb-1234567890.us-east-1.elb.amazonaws.com",
          "EvaluateTargetHealth": true
        }
      }
    }]
  }'
```

```hcl
resource "aws_cloudfront_origin_access_control" "oac" {
  name                              = "s3-oac"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

resource "aws_cloudfront_distribution" "site" {
  enabled = true
  origin {
    domain_name              = aws_s3_bucket.site.bucket_regional_domain_name
    origin_id                = "s3-site-origin"
    origin_access_control_id = aws_cloudfront_origin_access_control.oac.id
  }
  default_cache_behavior {
    target_origin_id       = "s3-site-origin"
    viewer_protocol_policy = "redirect-to-https"
    allowed_methods        = ["GET", "HEAD"]
    cached_methods          = ["GET", "HEAD"]
    forwarded_values {
      query_string = false
      cookies { forward = "none" }
    }
  }
  restrictions {
    geo_restriction { restriction_type = "none" }
  }
  viewer_certificate {
    cloudfront_default_certificate = true
  }
}
```

## Validation and Troubleshooting

- **Use the VPC Reachability Analyzer before debugging manually.** `aws
  ec2 create-network-insights-path` followed by `aws ec2
  start-network-insights-analysis` traces the actual hop-by-hop path
  between a source and destination ENI, including which security group or
  route table entry blocks the path — this is faster and more reliable
  than manually re-reading route tables under pressure.
- **Enable VPC Flow Logs at the VPC level, not per-ENI, for troubleshooting
  coverage.** Ship flow logs to CloudWatch Logs or S3 and filter for
  `REJECT` records to confirm whether traffic is actually reaching the ENI
  and being denied, versus never arriving due to a routing gap.
- **Common failure: private subnet has no internet route.** A private
  subnet's route table must point `0.0.0.0/0` at a NAT gateway that itself
  sits in a public subnet with a route to an Internet Gateway. A NAT
  gateway placed in another private subnet, or a route table still
  pointing at the default local-only route, is the most common cause of
  "instance has no outbound internet" tickets.
- **Common failure: SG references the wrong security group ID after a
  resource was recreated.** Terraform-managed security groups that
  reference each other by ID can silently drift if one group is replaced
  (not updated) during an apply; run `terraform plan` and confirm no
  unexpected `-/+` replacement is proposed for a referenced security
  group.
- **Common failure: overlapping CIDR blocks silently break peering or
  TGW routing.** `aws ec2 describe-vpc-peering-connections` and TGW route
  table inspection (`aws ec2 search-transit-gateway-routes`) reveal
  whether a route was actually installed; an overlapping CIDR produces a
  peering connection in `active` state with no working route because AWS
  will not install an ambiguous route.
- **Direct Connect/VPN troubleshooting.** `aws directconnect
  describe-virtual-interfaces` and `aws ec2 describe-vpn-connections`
  report BGP session and tunnel status; a VIF or tunnel in `down` state
  with correct configuration on both ends is most often a BGP ASN or
  pre-shared key mismatch, not an AWS-side fault.

## Security and Best Practices

- Never rely on a VPC's default security group; it permits all traffic
  between members. Create purpose-specific security groups and remove
  resources from the default group.
- Prefer security-group-to-security-group references over broad CIDR
  rules, and never open a database or internal API security group to
  `0.0.0.0/0`.
- Route third-party SaaS and shared internal platform traffic through
  PrivateLink interface endpoints rather than the public internet where a
  PrivateLink endpoint service is available.
- Centralize egress through a shared, inspected NAT/Network Firewall path
  for regulated workloads so outbound traffic is subject to consistent
  DLP/IDS policy rather than each workload account's own uninspected NAT
  gateway.
- Enable VPC Flow Logs on every VPC in every account and ship them to the
  centralized log-archive account established in [Chapter 02](02-multi-account-identity-governance-and-landing-zones.md), not to a
  workload account's own log group.
- Protect every public-facing origin with AWS WAF and, for
  internet-critical workloads, AWS Shield Advanced; restrict direct
  origin access (S3 buckets behind CloudFront, ALBs behind Global
  Accelerator) so the edge service is the only public entry point.
- Enable Route 53 Resolver DNS Firewall on outbound DNS to block
  resolution of known-malicious domains as an additional detective and
  preventive control against command-and-control traffic.

## References and Knowledge Checks

**References**

- Amazon VPC documentation — subnets, route tables, security groups, and
  network ACLs.
- AWS Transit Gateway and AWS PrivateLink documentation.
- AWS Direct Connect and AWS Site-to-Site VPN documentation, including the
  Direct Connect resiliency toolkit.
- Amazon Route 53, Amazon CloudFront, and AWS Global Accelerator
  documentation.
- [CERTIFICATION_BLUEPRINTS.md](../../../CERTIFICATION_BLUEPRINTS.md) —
  this chapter maps to the networking and connectivity domains of the AWS
  Certified Solutions Architect and AWS Certified Security blueprints.

**Knowledge checks**

1. Why can a stateless network ACL rule require an explicit outbound allow
   for return traffic that a stateful security group would allow
   automatically?
2. Why does VPC peering not support transitive routing, and what problem
   does Transit Gateway solve as a result?
3. When is AWS PrivateLink the correct choice over VPC peering for
   exposing a service to multiple consumer accounts?
4. Name two Direct Connect resiliency models and the failure each one
   protects against.

## Hands-On Lab

**Objective:** Build a two-AZ VPC with public and private subnets, apply
security groups that reference each other, verify the path with the VPC
Reachability Analyzer, and confirm a denied path fails as expected.

**Cost implications:** NAT gateways bill hourly (a small per-hour charge
plus per-GB data processing) and an unattached Elastic IP also bills
hourly. This lab provisions two NAT gateways and two Elastic IPs; complete
the cleanup step immediately after validation to avoid ongoing charges. The
Reachability Analyzer itself bills per analysis run at a small flat fee.

**Prerequisites**

- An AWS account (sandbox recommended) with AWS CLI v2 configured and
  permissions for EC2, VPC, and Reachability Analyzer actions.
- Terraform 1.9.x with the AWS provider, or willingness to run the
  equivalent AWS CLI commands directly.

**Steps**

1. Apply the VPC, subnet, NAT gateway, and security group Terraform from
   the Implementation section above (or an equivalent minimal subset),
   then confirm the VPC exists:

   ```bash
   aws ec2 describe-vpcs --filters "Name=tag:Name,Values=prod-app-vpc" \
     --query "Vpcs[0].VpcId" --output text
   ```

   **Expected result:** A `vpc-` ID is returned.

2. Launch a minimal test instance in a private subnet using the `sg-app`
   security group (use a free-tier-eligible `t3.micro` with no public IP):

   ```bash
   aws ec2 run-instances \
     --image-id "$(aws ssm get-parameters --names \
       /aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64 \
       --query 'Parameters[0].Value' --output text)" \
     --instance-type t3.micro \
     --subnet-id <PRIVATE_SUBNET_ID> \
     --security-group-ids <APP_SG_ID> \
     --no-associate-public-ip-address \
     --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=lab-app}]'
   ```

3. Create a Reachability Analyzer path from the ALB security group's
   notional source to the app instance's ENI on port 8443:

   ```bash
   PATH_ID=$(aws ec2 create-network-insights-path \
     --source <ALB_ENI_OR_TEST_SOURCE_ID> \
     --destination <APP_INSTANCE_ENI_ID> \
     --protocol tcp --destination-port 8443 \
     --query "NetworkInsightsPath.NetworkInsightsPathId" --output text)

   aws ec2 start-network-insights-analysis --network-insights-path-id "$PATH_ID"
   ```

   Poll and read the result:

   ```bash
   aws ec2 describe-network-insights-analyses \
     --filters "Name=path-id,Values=$PATH_ID" \
     --query "NetworkInsightsAnalyses[0].[Status,NetworkPathFound]"
   ```

   **Expected result:** `["succeeded", true]`, confirming the security
   group permits the path.

4. **Negative test:** Re-run the analysis targeting a port the app
   security group does not permit (for example, 3389):

   ```bash
   PATH_ID_NEG=$(aws ec2 create-network-insights-path \
     --source <ALB_ENI_OR_TEST_SOURCE_ID> \
     --destination <APP_INSTANCE_ENI_ID> \
     --protocol tcp --destination-port 3389 \
     --query "NetworkInsightsPath.NetworkInsightsPathId" --output text)

   aws ec2 start-network-insights-analysis --network-insights-path-id "$PATH_ID_NEG"
   aws ec2 describe-network-insights-analyses \
     --filters "Name=path-id,Values=$PATH_ID_NEG" \
     --query "NetworkInsightsAnalyses[0].[Status,NetworkPathFound]"
   ```

   **Expected result:** `["succeeded", false]`, with the analysis
   `ExplanationCode` identifying the security group as the blocking
   component. This confirms the security group boundary is enforced, not
   merely assumed.

5. **Cleanup** — terminate the instance and destroy the Terraform-managed
   resources to stop NAT gateway and Elastic IP billing:

   ```bash
   aws ec2 terminate-instances --instance-ids <INSTANCE_ID>
   aws ec2 delete-network-insights-path --network-insights-path-id "$PATH_ID"
   aws ec2 delete-network-insights-path --network-insights-path-id "$PATH_ID_NEG"
   terraform destroy
   ```

   Confirm no NAT gateways remain active:

   ```bash
   aws ec2 describe-nat-gateways \
     --filter "Name=vpc-id,Values=<VPC_ID>" \
     --query "NatGateways[?State!='deleted']"
   ```

   The query must return an empty list.

## Summary and Completion Checklist

A VPC's public, private, and isolated subnet tiers are defined entirely by
route tables, with security groups providing stateful, fine-grained
control layered under coarser, stateless network ACLs. VPC peering,
Transit Gateway, and PrivateLink each solve a distinct connectivity
problem — point-to-point, transitive hub-and-spoke, and one-directional
service exposure, respectively — and Site-to-Site VPN and Direct Connect
offer complementary hybrid connectivity trade-offs between setup speed and
sustained performance. Route 53, CloudFront, Global Accelerator, and AWS
WAF/Shield extend this network design to the AWS global edge, and the VPC
Reachability Analyzer turns network troubleshooting into a repeatable,
evidence-based process instead of manual route table inspection.

- [ ] Can design a multi-AZ VPC with correctly routed public, private, and
      isolated subnets.
- [ ] Can explain the stateful/stateless distinction between security
      groups and network ACLs and apply both correctly.
- [ ] Can choose correctly among VPC peering, Transit Gateway, and
      PrivateLink for a given connectivity requirement.
- [ ] Can compare Site-to-Site VPN and Direct Connect resiliency models.
- [ ] Completed the hands-on lab, including the negative test and cleanup.
