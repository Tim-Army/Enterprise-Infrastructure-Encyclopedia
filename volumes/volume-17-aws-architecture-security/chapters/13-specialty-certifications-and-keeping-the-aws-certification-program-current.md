# Chapter 13: Specialty Certifications, and Keeping the AWS Certification Program Current

![Two halves. On the left, the specialty tier and what is left of it: Advanced Networking (ANS-C01), retiring 25 August 2026, with certifications already earned staying valid for their full three years but no new ones issued after that date; and Security (SCS-C03), already covered by Chapter 8. Below them, four specialty certifications that have already left the catalog — Machine Learning, Data Analytics, Database, and SAP on AWS — with their subject matter folded into role-based exams such as Machine Learning Engineer and Data Engineer. The tier peaked at six and is down to two, one of which is closing. On the right, a four-step currency check that repeats on a cadence: re-list the levels and certifications from the AWS certification page, re-confirm each exam code from its own page via the Skill Builder exam-prep link, flag retirements and version bumps while distinguishing a language-version retirement from an exam retirement, then update this volume and its appendix.](../../../diagrams/volume-17-aws-architecture-security/chapter-13-specialty-and-currency-map.svg)

*Figure 13-1. A tier in retreat, and the recurring check that keeps this volume's certification map honest as AWS folds specialty subject matter into role-based exams.*

## Learning Objectives

- Identify the two remaining AWS specialty certifications and explain what
  the retirement of Advanced Networking – Specialty (ANS-C01) on
  25 August 2026 does and does not affect.
- Explain why the specialty tier has shrunk from six certifications to two,
  and where the retired specialties' subject matter went.
- Distinguish an exam retirement from a language-version retirement, and
  from a blueprint version bump — three different notices that read
  similarly.
- Run a four-step, primary-source currency check across the whole AWS
  certification program, using the Skill Builder exam-prep link as the
  reliable code source.
- Propagate a currency finding through this volume, the Master Appendices
  course catalog, and the repository's certification blueprint so the map
  does not drift silently.

## Theory and Architecture

Two things close this volume's certification coverage: the **specialty
tier**, which is smaller than most readers expect, and the **maintenance
discipline** that keeps everything Chapters 10 through 12 assert true over
time. They belong together, because the specialty tier is the clearest
evidence that this program moves.

This is study and review material; it reproduces no exam content. Every
code and date below was verified against AWS's own certification pages on
23 July 2026.

### What is left of the specialty tier

| Certification | Code | Status | This volume |
| --- | --- | --- | --- |
| Advanced Networking – Specialty | ANS-C01 | **Retires 25 August 2026** | [3](03-secure-networking-hybrid-connectivity-and-edge.md) |
| Security – Specialty | SCS-C03 | Current | [8](08-security-architecture-detection-and-incident-response.md) |

**Advanced Networking – Specialty (ANS-C01)** validates design and
operation of complex hybrid and multi-account network architectures —
Direct Connect, Transit Gateway, advanced routing, and network security at
scale, the ground
[Chapter 3](03-secure-networking-hybrid-connectivity-and-edge.md) covers.
AWS states the exam is being retired, with three consequences worth
separating:

- **No new certifications** are issued after the retirement date.
- **Certifications already earned remain active** for their standard
  three-year period. A retirement removes the exam, not the credential you
  hold.
- Registration closes at retirement, so a study plan that does not reach a
  test date before **25 August 2026** should not target this exam at all.

**Security – Specialty (SCS-C03)** remains current and is already this
volume's second mapped certification;
[Chapter 8](08-security-architecture-detection-and-incident-response.md)
and [Chapter 9](09-solutions-architect-and-security-training-capstone.md)
carry its material.

### Why the tier shrank

The specialty tier once held six certifications. Four have left the
catalog entirely, and their subject matter did not disappear — it moved
into **role-based** exams:

| Retired specialty | Where the subject matter went |
| --- | --- |
| Machine Learning – Specialty | Machine Learning Engineer – Associate (MLA) |
| Data Analytics – Specialty | Data Engineer – Associate (DEA-C01) |
| Database – Specialty | Folded into role-based associate and professional exams |
| SAP on AWS – Specialty | Withdrawn |

This is a deliberate direction: AWS has been reorganizing the program
around **what a person does** rather than **which technology they
specialize in**. That is why the associate tier grew (Data Engineer, ML
Engineer) while the specialty tier contracted, and why a new
generative-AI credential arrived at *professional* level
([Chapter 12](12-the-professional-tier-solutions-architect-devops-engineer-and-generative-ai-developer.md))
rather than as a specialty.

The practical consequence: **treat any specialty study plan as
perishable**. With one of the two remaining exams closing, the tier is the
least stable place to invest months of preparation.

### Three notices that look alike

A currency check fails if it cannot tell these apart, and all three appear
on AWS certification pages in similar language:

- **Exam retirement** — the certification stops being offered. Example:
  Advanced Networking – Specialty, retiring 25 August 2026. Existing
  credentials remain valid; no new ones are issued.
- **Language-version retirement** — one localized version of an exam ends
  while the exam continues. The Cloud Practitioner page carries such a
  notice for its **Indonesian** version; CLF-C02 itself is unaffected.
  Misreading this as an exam retirement is an easy and consequential error.
- **Blueprint version bump** — the certification continues under a new
  code suffix. Machine Learning Engineer – Associate is mid-transition from
  **MLA-C01** to **MLA-C02**, with registration for the updated version
  opening 1 September 2026. Nothing retires; the tested content is rebuilt.

Read which noun the notice attaches to — the exam, a language, or a
version — before drawing a conclusion.

### Why this program needs a recurring check

Within roughly one program generation: four specialty certifications
retired, two role-based associates were added, SysOps Administrator was
renamed CloudOps Engineer, a generative-AI professional certification was
introduced, one specialty was scheduled for retirement, and one associate
blueprint entered a version transition. A volume that states exam codes
will drift out of true unless someone re-verifies it deliberately, on a
cadence, against primary sources.

## Design Considerations

- **Do not start Advanced Networking now unless you can sit it in time.**
  With registration closing 25 August 2026, a plan that does not reach a
  test date before then should redirect to the networking material for its
  own sake — [Chapter 3](03-secure-networking-hybrid-connectivity-and-edge.md)
  is valuable independent of the credential — or toward SAP-C02, which
  carries substantial network architecture weight.
- **A held credential outlives its exam.** If you already hold Advanced
  Networking, it stays valid for its full three years. Do not rush a
  recertification on the assumption that retirement invalidates it; confirm
  your expiry date in your AWS Certification Account.
- **Prefer role-based exams for durable investment.** Given AWS's
  demonstrated direction, a role-based associate or professional
  certification is a safer multi-year bet than a specialty.
- **Run the check on a cadence, not on demand.** The value is catching
  silent drift — a renamed certification, a bumped suffix, a scheduled
  retirement — before a reader relies on stale material. Schedule it
  alongside the encyclopedia's other certification-currency checks.
- **Primary sources only, and the right primary source.** AWS's
  certification pages no longer print exam codes in body text. The
  reliable code source is the **Skill Builder exam-prep link** on each
  certification page, which embeds the current code. A third-party
  "AWS certification list" is a lead to verify, never a source to cite.
- **Propagate findings completely.** A check that updates only this chapter
  leaves the volume README, the
  [course-catalog appendix](../../volume-97-master-appendices/chapters/08-appendix-aws-certifications-and-course-access.md),
  and [CERTIFICATION_BLUEPRINTS.md](../../../CERTIFICATION_BLUEPRINTS.md)
  stale. Update all of them in one pass.

## Implementation and Automation

### The four-step currency check

```text
# Run on the repository's certification-currency cadence.

1. Re-list levels & certifications
   Source: https://aws.amazon.com/certification/
   Note:   retirement notices appear inside the certification's NAME on
           the landing page, e.g. "... - Specialty (retires August 25, 2026)"
   Output: current lineup per level

2. Re-confirm every exam code
   Source: each certification's own page -> its Skill Builder exam-prep link
   Output: verified code per certification (body text will not show it)

3. Flag retirements & version bumps
   Distinguish: exam retirement | language-version retirement | -C0x bump
   Output: dated findings, each traceable to a primary page

4. Update this volume + appendix + blueprint
   Targets: Volume XVII Chapters 10-13 and README,
            Master Appendices Chapter 08,
            CERTIFICATION_BLUEPRINTS.md
```

### Harvesting every current code in one pass

```bash
# The Skill Builder exam-prep URL on each certification page embeds the
# current exam code. This loop is the primary-source harvest used to
# verify this volume on 23 July 2026.
for s in certified-cloud-practitioner certified-ai-practitioner \
         certified-solutions-architect-associate certified-developer-associate \
         certified-cloudops-engineer-associate certified-data-engineer-associate \
         certified-machine-learning-engineer-associate \
         certified-solutions-architect-professional \
         certified-devops-engineer-professional \
         certified-generative-ai-developer-professional \
         certified-advanced-networking-specialty certified-security-specialty; do
  code=$(curl -s "https://aws.amazon.com/certification/$s/" \
    | grep -oE 'skillbuilder\.aws/[^"]*exam-prep[^"]*' \
    | grep -oE '[A-Z]{3}-[A-Z]?[0-9]{2}' | head -1)
  printf '%-52s %s\n' "$s" "${code:-NOT-FOUND}"
done
```

### A drift log to make the check auditable

```text
# One row per finding, so the next checker inherits a history.

Date       | Item                        | Was              | Now                  | Action
-----------|-----------------------------|------------------|----------------------|--------
2026-07-23 | SysOps Administrator Assoc  | SysOps Admin     | CloudOps Eng SOA-C03 | ch11
2026-07-23 | Advanced Networking ANS-C01 | current          | retires 25 Aug 2026  | ch13
2026-07-23 | ML Engineer Associate       | MLA-C01          | MLA-C02 from 1 Sep   | ch11
2026-07-23 | GenAI Developer Pro         | (did not exist)  | AIP-C01              | ch12
2026-07-23 | Cloud Practitioner          | CLF-C02          | CLF-C02 (Indonesian  | none
           |                             |                  | version retiring)    |
```

## Validation and Troubleshooting

- **A resolving page with a matching code is the pass signal.** For each
  certification, the check passes when its own AWS page resolves and its
  Skill Builder link carries the code this volume states. Anything else is
  a finding.
- **Silence is the failure mode.** The risk is not a wrong answer but an
  unnoticed change. If a check finds nothing, confirm it actually
  re-verified every certification rather than skipping — a check that
  quietly no-ops manufactures false confidence.
- **Read the noun in every notice.** Before recording a retirement, confirm
  whether it attaches to the exam, to a language version, or to a blueprint
  version. The Cloud Practitioner Indonesian notice is the standing example
  of how this goes wrong.
- **Cross-check the three artifacts.** After updating chapters, confirm the
  volume, the appendix, and CERTIFICATION_BLUEPRINTS.md carry the same
  codes and the same dates. A disagreement between them is itself a
  finding.
- **The specialty tier is the canary.** It has changed most and fastest. If
  a check finds further movement there, re-verify the whole program more
  carefully rather than treating it as an isolated edit.

## Security and Best Practices

- Verify only against `aws.amazon.com` and `skillbuilder.aws`. A currency
  check that follows a search result to a look-alike domain defeats its own
  purpose — confirm the host before trusting a code.
- The check reads certification *metadata* — names, codes, levels, dates.
  It never touches exam content, and must stay on that side of the line.
- Do not publish or circulate exam-guide content encountered while
  verifying; linking to AWS's page is the correct way to share a finding.
- Keep the drift log in the repository rather than in a personal note, so
  the next person inherits a verifiable history instead of re-deriving it.
- Register for any exam only through your AWS Certification Account and
  AWS's authorized testing partners, and confirm identification and
  proctoring requirements before exam day.

## References and Knowledge Checks

**References**

- [AWS Certification](https://aws.amazon.com/certification/) — the
  authoritative lineup, with retirement notices carried in certification
  names.
- [AWS Certified Advanced Networking – Specialty](https://aws.amazon.com/certification/certified-advanced-networking-specialty/) —
  ANS-C01, retiring 25 August 2026.
- [AWS Certified Security – Specialty](https://aws.amazon.com/certification/certified-security-specialty/) — SCS-C03.
- [AWS Skill Builder](https://skillbuilder.aws/) — official training; its
  exam-prep links are the reliable code source for the check above.
- [CERTIFICATION_BLUEPRINTS.md](../../../CERTIFICATION_BLUEPRINTS.md) and
  [Appendix — AWS Certifications and Course Access](../../volume-97-master-appendices/chapters/08-appendix-aws-certifications-and-course-access.md) —
  the two artifacts this check keeps in step with the volume.
- See [Chapter 3](03-secure-networking-hybrid-connectivity-and-edge.md)
  for the networking material behind ANS-C01 and
  [Chapter 8](08-security-architecture-detection-and-incident-response.md)
  for SCS-C03.

**Knowledge checks** *(original conceptual review questions — not
reproductions of any AWS exam item)*

1. What happens to a credential you already hold when its exam retires, and
   what stops happening?
2. Name the four specialty certifications that left the catalog and say
   where each one's subject matter went.
3. Distinguish an exam retirement, a language-version retirement, and a
   blueprint version bump, giving a current example of each.
4. Why is the certification page's body text an unreliable source for an
   exam code, and what is the reliable one?
5. A currency check reports no findings. What must you confirm before
   accepting that result?

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **every task in the
AWS Certified Advanced Networking – Specialty (ANS-C01) exam guide** (four
domains, sixteen tasks), each mapped in the volume README's ANS-C01
coverage table. Security – Specialty (SCS-C03) is the volume's security
spine and its topic labs live in Chapters 02–08; this chapter closes with
one integrative program-currency lab (Lab 13.17).

**Shared prerequisites for Labs 13.1–13.16**

- AWS CLI v2 authenticated to a sandbox account with network-admin rights,
  and a default Region set (`aws configure get region`). Labs use
  `export RG=ans-lab` and `export AZ1=$(aws configure get region)a` as
  working names.
- **Cost:** most labs use free or sub-cent resources (VPCs, route tables,
  security groups, Route 53 zones at ~$0.50/zone/month, flow logs). Labs
  that touch billable services — CloudFront, Global Accelerator, NAT
  gateways, Transit Gateway attachments, VPN, Network Firewall — say so and
  end with a cleanup step. Delete resources the same day.
- Every lab ends **`**Lab verified by:** *pending*`** until a human runs it.

### Lab 13.1 — Design a solution that incorporates edge network services for global performance

**Objective:** Put Amazon CloudFront in front of an S3 origin and prove it
terminates at the edge.

```bash
export B=ans-edge-$(aws sts get-caller-identity --query Account --output text)
aws s3 mb "s3://$B"
DIST=$(aws cloudfront create-distribution \
  --origin-domain-name "$B.s3.amazonaws.com" \
  --default-root-object index.html \
  --query 'Distribution.Id' --output text)
aws cloudfront get-distribution --id "$DIST" --query 'Distribution.Status'
```

**Expected result:** a distribution ID and a status of `InProgress`, then
`Deployed` after several minutes. `aws cloudfront get-distribution` returns
a `DomainName` like `d111111abcdef8.cloudfront.net`.

**Negative test:** request a path the origin does not have —
`curl -s -o /dev/null -w '%{http_code}' https://<domain>/missing.html`
returns `403`/`404` from the edge, not a connection error, proving the edge
answered.

**Cleanup:** `aws cloudfront delete-distribution` (after disabling and
waiting for `Deployed`), then `aws s3 rb "s3://$B" --force`. CloudFront is
billed per request and data-out; delete promptly.

### Lab 13.2 — Design DNS solutions for public, private, and hybrid requirements

**Objective:** Create a private hosted zone and resolve a record only from
inside the VPC.

```bash
VPC=$(aws ec2 create-vpc --cidr-block 10.20.0.0/16 --query 'Vpc.VpcId' --output text)
ZID=$(aws route53 create-hosted-zone --name internal.ans. \
  --vpc VPCRegion=$(aws configure get region),VPCId=$VPC \
  --caller-reference "ans-$(date +%s)" --query 'HostedZone.Id' --output text)
aws route53 list-hosted-zones-by-vpc --vpc-id "$VPC" \
  --vpc-region "$(aws configure get region)" --query 'HostedZoneSummaries[].Name'
```

**Expected result:** the private zone `internal.ans.` is listed as
associated with the VPC.

**Negative test:** query the private name from a public resolver —
`dig @8.8.8.8 db.internal.ans +short` returns nothing, proving the zone is
private to the VPC.

**Cleanup:** `aws route53 delete-hosted-zone --id "$ZID"`; delete the VPC.

### Lab 13.3 — Design load balancing for high availability, scalability, and security

**Objective:** Stand up an internet-facing Application Load Balancer across
two subnets and read its scheme.

```bash
ALB=$(aws elbv2 create-load-balancer --name ans-alb \
  --subnets $SUBNET_A $SUBNET_B --security-groups $SG \
  --scheme internet-facing --type application \
  --query 'LoadBalancers[0].LoadBalancerArn' --output text)
aws elbv2 describe-load-balancers --load-balancer-arns "$ALB" \
  --query 'LoadBalancers[0].{Scheme:Scheme,AZs:AvailabilityZones[].ZoneName}'
```

**Expected result:** `Scheme: internet-facing` spanning two Availability
Zones — the minimum for an HA ALB.

**Negative test:** try to create an ALB in a single subnet —
`... --subnets $SUBNET_A` fails with
`At least two subnets in two different Availability Zones must be specified`.

**Cleanup:** `aws elbv2 delete-load-balancer --load-balancer-arn "$ALB"`.

### Lab 13.4 — Define logging and monitoring across AWS and hybrid networks

**Objective:** Enable VPC Flow Logs to CloudWatch and confirm records land.

```bash
aws logs create-log-group --log-group-name /ans/flow-logs
aws ec2 create-flow-logs --resource-type VPC --resource-ids "$VPC" \
  --traffic-type ALL --log-group-name /ans/flow-logs \
  --deliver-logs-permission-arn "$FLOW_ROLE_ARN"
aws ec2 describe-flow-logs --filter Name=resource-id,Values=$VPC \
  --query 'FlowLogs[0].FlowLogStatus'
```

**Expected result:** `FlowLogStatus: ACTIVE`; within ~10 minutes
`aws logs filter-log-events --log-group-name /ans/flow-logs` returns
records with `srcaddr`/`dstaddr`/`action`.

**Negative test:** pass a role without `logs:PutLogEvents` — `FlowLogStatus`
becomes `ACTIVE` but no events ever arrive, the classic silent-failure the
task tests for.

**Cleanup:** delete the flow log and the log group.

### Lab 13.5 — Design routing and connectivity between on-premises and AWS

**Objective:** Model a Site-to-Site VPN by creating a customer gateway and
VPN gateway and reading the proposed tunnels.

```bash
CGW=$(aws ec2 create-customer-gateway --type ipsec.1 \
  --public-ip 203.0.113.10 --bgp-asn 65000 \
  --query 'CustomerGateway.CustomerGatewayId' --output text)
VGW=$(aws ec2 create-vpn-gateway --type ipsec.1 \
  --query 'VpnGateway.VpnGatewayId' --output text)
aws ec2 attach-vpn-gateway --vpn-gateway-id "$VGW" --vpc-id "$VPC"
```

**Expected result:** a customer gateway with ASN 65000 and a VPN gateway
that attaches to the VPC (`State: attached`).

**Negative test:** create the VPN connection with
`--options StaticRoutesOnly=false` but no BGP on the customer side; the
tunnels stay `DOWN`, proving dynamic routing needs a BGP speaker.

**Cleanup:** detach and delete the VPN gateway and customer gateway (VPN
gateways are billed hourly).

### Lab 13.6 — Design multi-account, multi-Region, multi-VPC connectivity

**Objective:** Create a Transit Gateway and attach a VPC — the hub for
scaled connectivity.

```bash
TGW=$(aws ec2 create-transit-gateway --description ans-hub \
  --query 'TransitGateway.TransitGatewayId' --output text)
aws ec2 create-transit-gateway-vpc-attachment \
  --transit-gateway-id "$TGW" --vpc-id "$VPC" --subnet-ids "$SUBNET_A" \
  --query 'TransitGatewayVpcAttachment.State'
```

**Expected result:** the attachment reports `pending` then `available`;
`aws ec2 describe-transit-gateways` shows `State: available`.

**Negative test:** attach a second VPC whose CIDR overlaps the first; the
route in the TGW route table is rejected as a blackhole, demonstrating why
non-overlapping CIDRs are a design constraint.

**Cleanup:** delete the attachment, then the Transit Gateway. Attachments
bill hourly.

### Lab 13.7 — Implement routing and connectivity between on-premises and AWS

**Objective:** Add a route to the VPN gateway and enable route propagation.

```bash
aws ec2 enable-vgw-route-propagation --route-table-id "$RTB" --gateway-id "$VGW"
aws ec2 describe-route-tables --route-table-ids "$RTB" \
  --query 'RouteTables[0].PropagatingVgws'
```

**Expected result:** `PropagatingVgws` lists the VGW, so BGP-learned
on-premises routes populate the table automatically.

**Negative test:** query the route table before enabling propagation —
`PropagatingVgws` is empty and on-prem prefixes are absent, so traffic to
them is dropped.

**Cleanup:** `aws ec2 disable-vgw-route-propagation`.

### Lab 13.8 — Implement multi-account/Region/VPC routing patterns

**Objective:** Give the Transit Gateway an explicit static route and read
the route table.

```bash
TGW_RTB=$(aws ec2 describe-transit-gateway-route-tables \
  --filters Name=transit-gateway-id,Values=$TGW \
  --query 'TransitGatewayRouteTables[0].TransitGatewayRouteTableId' --output text)
aws ec2 create-transit-gateway-route --destination-cidr-block 10.30.0.0/16 \
  --transit-gateway-route-table-id "$TGW_RTB" \
  --transit-gateway-attachment-id "$ATTACH"
aws ec2 search-transit-gateway-routes --transit-gateway-route-table-id "$TGW_RTB" \
  --filters Name=type,Values=static --query 'Routes[].DestinationCidrBlock'
```

**Expected result:** `10.30.0.0/16` appears as a static route with
`State: active`.

**Negative test:** point the route at a detached attachment; its state
shows `blackhole` and traffic to the CIDR is silently dropped.

**Cleanup:** `aws ec2 delete-transit-gateway-route`.

### Lab 13.9 — Implement complex hybrid and multi-account DNS

**Objective:** Create a Route 53 Resolver outbound endpoint and a
forwarding rule for hybrid name resolution.

```bash
EP=$(aws route53resolver create-resolver-endpoint --direction OUTBOUND \
  --security-group-ids "$SG" --name ans-out \
  --ip-addresses SubnetId=$SUBNET_A SubnetId=$SUBNET_B \
  --creator-request-id "ans-$(date +%s)" \
  --query 'ResolverEndpoint.Id' --output text)
aws route53resolver create-resolver-rule --rule-type FORWARD \
  --domain-name corp.example.com --resolver-endpoint-id "$EP" \
  --name ans-fwd --target-ips Ip=192.0.2.10 \
  --creator-request-id "ans-r-$(date +%s)"
```

**Expected result:** an outbound endpoint (`Status: OPERATIONAL`) and a
FORWARD rule sending `corp.example.com` queries to the on-prem resolver.

**Negative test:** forward a domain with no reachable target IP; queries
`SERVFAIL`, showing the rule forwards but the target must answer.

**Cleanup:** delete the resolver rule and endpoint (endpoints bill per ENI
per hour).

### Lab 13.10 — Automate and configure network infrastructure

**Objective:** Deploy a VPC as code with CloudFormation and confirm drift
status.

```bash
cat > /tmp/vpc.yaml <<'YAML'
Resources:
  Net: {Type: AWS::EC2::VPC, Properties: {CidrBlock: 10.40.0.0/16}}
YAML
aws cloudformation deploy --template-file /tmp/vpc.yaml --stack-name ans-net
aws cloudformation detect-stack-drift --stack-name ans-net
aws cloudformation describe-stacks --stack-name ans-net \
  --query 'Stacks[0].StackStatus'
```

**Expected result:** `StackStatus: CREATE_COMPLETE`; drift detection
reports `IN_SYNC` immediately after deployment.

**Negative test:** manually change the VPC's tags in the console, re-run
`detect-stack-drift`; the stack now reports `DRIFTED`, the signal that a
manual change bypassed the pipeline.

**Cleanup:** `aws cloudformation delete-stack --stack-name ans-net`.

### Lab 13.11 — Maintain routing and connectivity on AWS and hybrid networks

**Objective:** Audit a route table for the specific next hop a prefix
resolves to.

```bash
aws ec2 describe-route-tables --route-table-ids "$RTB" \
  --query 'RouteTables[0].Routes[].{Dest:DestinationCidrBlock,GW:GatewayId,TGW:TransitGatewayId,State:State}' \
  --output table
```

**Expected result:** a table where `0.0.0.0/0` points to an internet or NAT
gateway and internal prefixes point to the TGW or VGW, each `State: active`.

**Negative test:** delete the IGW route and re-run; `0.0.0.0/0` disappears
and instances lose internet egress — a maintenance error made visible.

**Cleanup:** restore the default route
(`aws ec2 create-route --destination-cidr-block 0.0.0.0/0 ...`).

### Lab 13.12 — Monitor and analyze network traffic to troubleshoot connectivity

**Objective:** Use VPC Reachability Analyzer to prove (or disprove) a path.

```bash
PATH_ID=$(aws ec2 create-network-insights-path --source "$IGW" \
  --destination "$ENI" --protocol tcp --destination-port 443 \
  --query 'NetworkInsightsPath.NetworkInsightsPathId' --output text)
ANALYSIS=$(aws ec2 start-network-insights-analysis \
  --network-insights-path-id "$PATH_ID" \
  --query 'NetworkInsightsAnalysis.NetworkInsightsAnalysisId' --output text)
aws ec2 describe-network-insights-analyses \
  --network-insights-analysis-ids "$ANALYSIS" \
  --query 'NetworkInsightsAnalyses[0].NetworkPathFound'
```

**Expected result:** `NetworkPathFound: true` when a security group and
route allow 443 to the ENI.

**Negative test:** remove the inbound 443 rule and re-run; the analysis
returns `false` and names the blocking security group in
`ExplanationCode`, pinpointing the fault.

**Cleanup:** delete the analysis and the insights path.

### Lab 13.13 — Optimize AWS networks for performance, reliability, and cost

**Objective:** Replace NAT-gateway data charges for S3 traffic with a free
Gateway VPC endpoint.

```bash
aws ec2 create-vpc-endpoint --vpc-id "$VPC" --vpc-endpoint-type Gateway \
  --service-name "com.amazonaws.$(aws configure get region).s3" \
  --route-table-ids "$RTB" \
  --query 'VpcEndpoint.State'
aws ec2 describe-vpc-endpoints --filters Name=vpc-id,Values=$VPC \
  --query 'VpcEndpoints[].ServiceName'
```

**Expected result:** the S3 endpoint is `available` and a prefix-list route
to S3 appears in the route table — S3 traffic now bypasses the NAT gateway.

**Negative test:** send S3 traffic from a private subnet with no endpoint
and no NAT; the request times out, showing the endpoint (not the internet
path) is what restored — and cheapened — access.

**Cleanup:** `aws ec2 delete-vpc-endpoints --vpc-endpoint-ids ...`.

### Lab 13.14 — Implement network features for security and compliance

**Objective:** Add a stateless deny at the subnet edge with a network ACL
rule.

```bash
NACL=$(aws ec2 describe-network-acls --filters Name=vpc-id,Values=$VPC \
  --query 'NetworkAcls[0].NetworkAclId' --output text)
aws ec2 create-network-acl-entry --network-acl-id "$NACL" --rule-number 90 \
  --protocol tcp --port-range From=23,To=23 --cidr-block 0.0.0.0/0 \
  --rule-action deny --ingress
aws ec2 describe-network-acls --network-acl-ids "$NACL" \
  --query 'NetworkAcls[0].Entries[?RuleNumber==`90`]'
```

**Expected result:** a deny rule for TCP/23 (Telnet) at rule number 90,
evaluated before the default allow.

**Negative test:** place the same deny at rule number 200, *after* an allow
at 100; because NACLs evaluate in order, Telnet is now permitted —
demonstrating rule-order sensitivity.

**Cleanup:** `aws ec2 delete-network-acl-entry --rule-number 90 --ingress`.

### Lab 13.15 — Validate and audit security via network monitoring and logging

**Objective:** Query flow logs for rejected traffic to audit the perimeter.

```bash
aws logs filter-log-events --log-group-name /ans/flow-logs \
  --filter-pattern '[version, account, eni, src, dst, srcport, dstport, protocol, packets, bytes, start, end, action=REJECT, status]' \
  --query 'events[0:5].message'
```

**Expected result:** up to five records whose final field is `REJECT`,
each showing the source that was denied — evidence for a security audit.

**Negative test:** run the same filter with `action=ACCEPT` on a locked-down
subnet with no traffic; zero records return, confirming the filter, not
absence of logging, is what selects rejects.

**Cleanup:** none (read-only query).

### Lab 13.16 — Implement and maintain confidentiality of data and communications

**Objective:** Enforce HTTPS on the ALB by attaching an ACM certificate to
an HTTPS listener.

```bash
aws elbv2 create-listener --load-balancer-arn "$ALB" --protocol HTTPS \
  --port 443 --certificates CertificateArn="$ACM_ARN" \
  --ssl-policy ELBSecurityPolicy-TLS13-1-2-2021-06 \
  --default-actions Type=forward,TargetGroupArn="$TG" \
  --query 'Listeners[0].SslPolicy'
```

**Expected result:** an HTTPS listener on 443 with a TLS 1.2/1.3 security
policy — traffic to the ALB is now encrypted in transit.

**Negative test:** curl the HTTP listener after adding a redirect action —
`curl -sI http://<alb-dns>/` returns `301` to `https://`, proving plaintext
is refused rather than served.

**Cleanup:** delete the listener; the certificate remains in ACM for reuse.

### Lab 13.17 — Program currency check (integrative)

**Objective:** Run one complete, primary-source currency check across the
AWS certification program and produce an auditable drift log — the
maintenance skill this chapter teaches, exercised for real.

**Cost note:** This lab is entirely free; it makes no AWS API calls and
creates no resources.

**Prerequisites**

- Web access to `aws.amazon.com/certification`.
- The four-step check, harvest loop, and drift-log format above.
- This volume's stated codes (Chapters 10–13) to check against.

**Steps**

1. **Re-list (target 10 minutes).** From the AWS certification page, list
   the current certifications by level, reading each name fully so any
   embedded retirement notice is captured.

   **Expected result:** a lineup matching Chapter 10's table, or a
   documented difference.

2. **Harvest codes (target 15 minutes).** Run the harvest loop, or open
   each certification page and read the code from its Skill Builder
   exam-prep link.

   **Expected result:** twelve codes confirmed from primary sources. Any
   `NOT-FOUND` is a finding to chase manually, not to ignore.

3. **Classify notices (target 10 minutes).** For every retirement or update
   notice found, classify it as exam retirement, language-version
   retirement, or version bump, and record which noun it attached to.

   **Expected result:** each notice correctly classified — including at
   least one that is *not* an exam retirement.

4. **Log (target 10 minutes).** Record findings in the drift-log format
   with date, previous state, current state, and the action needed.

   **Expected result:** an auditable log a future checker can build on.

5. **Negative test (target 10 minutes).** Deliberately consult a
   third-party AWS certification listing and compare it against your
   harvest.

   **Expected result:** at least one discrepancy — a retired specialty
   still listed, a pre-rename SysOps title, or a missing Generative AI
   Developer entry. This demonstrates why step 2 uses primary sources.

6. **Close the loop.** Confirm this volume, the appendix, and
   CERTIFICATION_BLUEPRINTS.md agree with your harvest. Any disagreement is
   itself a finding to record.

   **Expected result:** three artifacts in agreement, or logged
   inconsistencies.

7. **Cleanup:** file the drift log with the repository. There is no
   infrastructure to tear down and no spend to check.

## Lab Verification

Complete this sign-off once a full currency check has been run and a drift
log produced. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The AWS specialty tier is down to two certifications: Advanced Networking
(ANS-C01), **retiring 25 August 2026**, and Security (SCS-C03), already
covered by Chapter 8. Retirement ends new certifications but leaves
existing credentials valid for their full three years. Four specialties —
Machine Learning, Data Analytics, Database, and SAP on AWS — have already
left, their subject matter folded into role-based exams, which is the
program's clear direction and a reason to prefer role-based certifications
for durable investment. Because the program moves this fast, this chapter
also defines the four-step currency check: re-list from AWS's certification
page, re-confirm every code via each certification's Skill Builder
exam-prep link, classify each notice as an exam retirement, a
language-version retirement, or a version bump, and propagate findings
through this volume, the appendix, and the blueprint. Primary sources only.

- [ ] Can name the two remaining specialty certifications and ANS-C01's
      retirement date.
- [ ] Knows a retirement ends the exam, not a credential already earned.
- [ ] Can say where each retired specialty's subject matter went.
- [ ] Can distinguish exam retirement, language retirement, and version
      bump with current examples.
- [ ] Can harvest a current exam code from the reliable primary source.
- [ ] Has produced a drift log and confirmed volume, appendix, and
      blueprint agree.
- [ ] Completed the hands-on currency-check lab, including the
      third-party-discrepancy negative test.
