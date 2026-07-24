# Chapter 06: Infrastructure Professionals — Network Engineer, DevOps Engineer, and Developer

## Learning Objectives

- Identify the three infrastructure-facing professional certifications and
  the role each is written for
- Describe Google Cloud's distinctive networking model — global VPCs,
  regional subnets, and global load balancing — and why it differs from
  other clouds
- Explain the SRE foundations the DevOps Engineer certification assumes:
  SLIs, SLOs, error budgets, and toil reduction
- Describe the developer's surface: Cloud Run, GKE, App Engine, and the
  managed data and messaging services around them
- Choose among the three by the work you do, recognizing where they
  overlap

## Theory and Architecture

### Three certifications, one infrastructure

| Certification | Role |
| --- | --- |
| Professional Cloud Network Engineer | Designs, implements, and manages Google Cloud networks |
| Professional Cloud DevOps Engineer | Builds delivery pipelines and operates services reliably |
| Professional Cloud Developer | Builds, deploys, and instruments cloud-native applications |

All three are **2 hours, $200, 50–60 multiple choice and multiple select
questions**, valid **two years**, no prerequisites (verified
23 July 2026).

### Networking: global VPCs are the differentiator

Google Cloud's networking model differs from AWS's and Azure's in a way
that shapes every design question:

- **A VPC is global.** It spans every region, unlike an AWS VPC or an
  Azure virtual network, which are regional.
- **Subnets are regional**, each with an IP range, and a single VPC can
  hold subnets in many regions that route to each other **without
  peering** — because they are one network.
- **Global load balancing** follows from this: a single anycast IP can
  front backends in multiple regions, which on other clouds requires a
  DNS-based or multi-region construct.

The practical consequence is that Google Cloud needs no hub-and-spoke
topology to connect regions within one VPC. Where hub-and-spoke does
appear, it is usually about **isolating** workloads or inserting
appliances, not about achieving connectivity — the opposite of the driver
on Azure, where peering's non-transitivity forces the pattern
([Volume XXXIII](../../volume-33-microsoft-azure-certifications/README.md),
Chapter 04).

Hybrid connectivity follows the familiar shape: **Cloud VPN** over the
internet, **Cloud Interconnect** (dedicated or partner) for private
capacity with predictable latency, and **Network Connectivity Center** for
managing connectivity at scale. Choose by the stated latency, bandwidth,
and compliance constraints rather than preference.

### DevOps: SRE is the syllabus

Professional Cloud DevOps Engineer is unusual among vendor certifications
in that its conceptual backbone is **Site Reliability Engineering**, not a
product list. The vocabulary is examinable and genuinely useful:

- **SLI** — a measured indicator of service behavior (request latency,
  error rate, availability).
- **SLO** — the target for an SLI over a window ("99.9% of requests under
  300 ms over 28 days").
- **Error budget** — the allowed unreliability implied by the SLO. A 99.9%
  target permits 0.1% failure; that budget is *spendable* on releases and
  risk.
- **Toil** — manual, repetitive, automatable operational work. Reducing it
  is the job.

The error budget is the idea that changes behavior: it converts
"how much risk may we take?" from an argument into arithmetic. When the
budget is exhausted, releases pause; when it is healthy, the team can ship
faster. Expect scenarios that test whether you reason that way.

The product surface — Cloud Build, Artifact Registry, Cloud Deploy, and
the Cloud Operations suite (Monitoring, Logging, Trace, Profiler, Error
Reporting) — sits on top of that reasoning.

### Developer: the application surface

Professional Cloud Developer covers designing, building, deploying, and
instrumenting applications. Its compute choices matter:

| Service | Use when |
| --- | --- |
| Cloud Run | Containerized, request-driven, scale-to-zero; the default for stateless services |
| GKE | Kubernetes semantics genuinely needed — complex orchestration, operators, custom scheduling |
| App Engine | Long-standing PaaS; still examined, less often the new-build answer |
| Cloud Functions | Event-driven single-purpose handlers |

Alongside these: Firestore and Cloud SQL for data, Pub/Sub for messaging,
Secret Manager for credentials, and the Cloud Operations suite for
instrumentation — which is where this certification overlaps with DevOps.

### Where they overlap

Developer and DevOps share instrumentation and delivery pipelines; Network
Engineer and Architect share connectivity design. Holding two adjacent
professional certifications is cheaper than the first, but each carries
its own two-year, $200 renewal — so the second should reflect real role
breadth rather than completeness.

## Design Considerations

- **Do not import a hub-and-spoke instinct.** On Google Cloud a single
  global VPC already connects regions. Reach for multiple VPCs when you
  want isolation, not connectivity.
- **Choose hybrid links by constraint.** Cloud VPN for cost and speed of
  provisioning; Interconnect for predictable latency, high bandwidth, or a
  requirement that traffic avoid the public internet.
- **Set SLOs on user-visible behavior.** An SLO on CPU utilization is not
  an SLO; it measures the system, not the user's experience.
- **Default to Cloud Run for new stateless services.** Reach for GKE when
  Kubernetes semantics are genuinely required — the exam rewards
  recognizing when they are not.
- **Instrument before you need it.** Both Developer and DevOps treat
  observability as a design input, not an afterthought.

## Implementation and Automation

### A global VPC with subnets in two regions

```bash
gcloud compute networks create vpc-global --subnet-mode=custom
gcloud compute networks subnets create snet-us \
  --network=vpc-global --range=10.30.0.0/24 --region=us-central1
gcloud compute networks subnets create snet-eu \
  --network=vpc-global --range=10.31.0.0/24 --region=europe-west1
```

```bash
# One network, subnets in two regions — no peering needed between them
gcloud compute networks subnets list --network=vpc-global \
  --format='table(name, region, ipCidrRange)'
```

### Deploying a service and reading its SLIs

```bash
gcloud run deploy svc-demo --image=us-docker.pkg.dev/cloudrun/container/hello \
  --region=us-central1 --allow-unauthenticated
```

```bash
# Request latency and count are the raw material of an SLI
gcloud monitoring time-series list \
  --filter='metric.type="run.googleapis.com/request_latencies"' \
  --format='value(metric.type)' 2>/dev/null | head -3
```

### Error budget arithmetic

```text
# Convert an SLO into a budget before arguing about release risk.
#
#   SLO 99.9% over 28 days
#   Total minutes      = 28 * 24 * 60          = 40,320
#   Allowed failure    = 40,320 * 0.001        = 40.3 minutes
#
# That 40 minutes is the error budget. Spend it deliberately on
# releases and experiments; when it is gone, stop shipping and
# stabilize. This arithmetic is the whole point of an SLO.
```

## Validation and Troubleshooting

- **Verify cross-region routing rather than assuming it.** The lab proves
  two regional subnets in one VPC reach each other with no peering — the
  fact that distinguishes this platform.
- **Check firewall rules before blaming routing.** Google Cloud VPC
  firewall rules are stateful and evaluated by priority, with an implied
  deny on ingress; connectivity failures inside one VPC are far more often
  firewall than routing.
- **Test an SLO against real data.** An SLO chosen without looking at the
  current SLI distribution is a guess. Read the metric first, then set the
  target.
- **Distinguish a cold start from a latency regression.** On Cloud Run,
  scale-to-zero means first-request latency differs from steady state;
  reading them as one number produces a false regression.
- **Use `gcloud compute network-management connectivity-tests`** to
  diagnose reachability with the platform's own answer rather than
  inference from a failed ping.

## Security and Best Practices

- VPC firewall rules default to denying ingress; write explicit,
  prioritized rules and prefer network tags or service accounts as targets
  over broad IP ranges.
- Use Private Google Access and Private Service Connect so workloads reach
  Google APIs without external IPs — which pairs with the organization
  policy guardrail from [Chapter 05](05-professional-cloud-architect.md).
- Store application credentials in Secret Manager, never in images or
  environment files committed to a repository.
- Run Cloud Run services with a dedicated, least-privileged service
  account rather than the default compute service account, which is
  broadly permissioned.
- Error budgets are a safety mechanism as much as a delivery one: pausing
  releases when the budget is exhausted is the practice, not a suggestion.

## References and Knowledge Checks

**References**

- [Professional Cloud Network Engineer](https://cloud.google.com/certification/cloud-network-engineer)
- [Professional Cloud DevOps Engineer](https://cloud.google.com/certification/cloud-devops-engineer)
- [Professional Cloud Developer](https://cloud.google.com/certification/cloud-developer)
- [Google SRE books](https://sre.google/books/) — the source of the SLI,
  SLO, error budget, and toil vocabulary.
- [Appendix — Google Cloud Certifications and Course Access](../../volume-97-master-appendices/chapters/10-appendix-google-cloud-certifications-and-course-access.md)
- See [Chapter 05](05-professional-cloud-architect.md) for the landing-zone
  design these operate inside.

**Knowledge checks** *(original conceptual review questions — not
reproductions of any Google exam item)*

1. Why does a global VPC change topology design compared with AWS or
   Azure?
2. Define SLI, SLO, and error budget, and compute the budget for a 99.5%
   monthly SLO.
3. Why is an SLO on CPU utilization not really an SLO?
4. Give a case for Cloud Run and a case where GKE is genuinely required.
5. Connectivity fails between two subnets in one VPC. What do you check
   first, and why?

## Hands-On Lab

These labs cover the exam-guide topics for the three infrastructure
professional certifications: **Network Engineer** and **DevOps Engineer**
topic by topic, and **Developer** at section level (its surface is the
same Cloud Run / GKE / integration ground the other two exercise).
Mapping is in the
[volume README](../README.md#lab-coverage--infrastructure-professionals).

**Cost note:** VPC, subnets, routes, and firewall rules are free. Two
`e2-micro` instances and one Cloud Run service are minimal. Lab 6.22
deletes the project.

**Prerequisites**

```bash
export PROJECT_ID="$(gcloud config get-value project)"
gcloud config set project "$PROJECT_ID"
```

**Expected result:** `Updated property [core/project].`

### Lab 6.1 — Designing an overall network architecture *(NE 1.1)*

```bash
gcloud compute networks create vpc-net --subnet-mode=custom
gcloud compute networks describe vpc-net --format='value(name, routingConfig.routingMode)'
```

**Expected result:** `vpc-net REGIONAL`. Custom mode (not auto) is the
architect's default — it means subnets are created deliberately, not one
per region automatically.

### Lab 6.2 — Designing VPC networks *(NE 1.2)*

```bash
gcloud compute networks subnets create snet-us \
  --network=vpc-net --range=10.60.0.0/24 --region=us-central1
gcloud compute networks subnets create snet-eu \
  --network=vpc-net --range=10.61.0.0/24 --region=europe-west1
gcloud compute networks subnets list --network=vpc-net \
  --format='table(name, region, ipCidrRange)'
```

**Expected result:** two subnets, two regions, one network — the global
VPC. No peering is needed between them.

### Lab 6.3 — Designing hybrid and multi-cloud networking *(NE 1.3)*

```bash
gcloud compute routers create rtr-net --network=vpc-net --region=us-central1 \
  --asn=64512
gcloud compute routers describe rtr-net --region=us-central1 \
  --format='value(name, bgp.asn)'
```

**Expected result:** `rtr-net 64512`. Cloud Router with a BGP ASN is the
hybrid-connectivity anchor — VPN and Interconnect both attach to it.

### Lab 6.4 — Designing for GKE networking *(NE 1.4)*

```bash
gcloud compute networks subnets create snet-gke \
  --network=vpc-net --range=10.62.0.0/24 --region=us-central1 \
  --secondary-range=pods=10.100.0.0/16,services=10.101.0.0/20
gcloud compute networks subnets describe snet-gke --region=us-central1 \
  --format='value(secondaryIpRanges[].rangeName)'
```

**Expected result:** `pods;services`. VPC-native GKE needs secondary
ranges for pods and services — designing them up front is topic 1.4.

### Lab 6.5 — Configuring VPCs *(NE 2.1)*

```bash
gcloud compute firewall-rules create allow-net-internal \
  --network=vpc-net --allow=tcp,udp,icmp --source-ranges=10.60.0.0/16
gcloud compute firewall-rules list --filter="network:vpc-net" \
  --format='table(name, direction, sourceRanges.list())'
```

**Expected result:** one INGRESS rule for `10.60.0.0/16`. Ingress is
denied by default, so this rule is what makes the subnets usable.

### Lab 6.6 — Configuring VPC routing *(NE 2.2)*

```bash
gcloud compute routes create rt-default-net \
  --network=vpc-net --destination-range=0.0.0.0/0 \
  --next-hop-gateway=default-internet-gateway --priority=1000
gcloud compute routes list --filter="network:vpc-net" \
  --format='table(name, destRange, priority, nextHopGateway.basename())'
```

**Expected result:** your route plus the system-created subnet routes.
Route selection is longest-prefix then priority — the exam tests that
order.

### Lab 6.7 — Configuring Network Connectivity Center *(NE 2.3, 4.4)*

```bash
gcloud network-connectivity hubs create hub-net --description="lab hub" 2>&1 | head -3
gcloud network-connectivity hubs list --format='value(name, state)' 2>&1 | head -3
```

**Expected result:** a hub in `ACTIVE` state, or an enable-API prompt.
NCC is Google's managed transitive-connectivity fabric — the alternative
to hand-built topologies.

### Lab 6.8 — Configuring and maintaining GKE clusters *(NE 2.4)*

```bash
gcloud container clusters create-auto gke-net --region=us-central1 \
  --network=vpc-net --subnetwork=snet-gke \
  --cluster-secondary-range-name=pods --services-secondary-range-name=services
gcloud container clusters describe gke-net --region=us-central1 \
  --format='value(status, privateClusterConfig.enablePrivateNodes)'
```

**Expected result:** `RUNNING`. This binds the cluster to the secondary
ranges from Lab 6.4 — proof the network design and the cluster agree.

### Lab 6.9 — Configuring load balancing *(NE 3.1)*

```bash
gcloud compute health-checks create http hc-net --port=80
gcloud compute backend-services create bes-net --protocol=HTTP \
  --health-checks=hc-net --global
gcloud compute backend-services describe bes-net --global \
  --format='value(name, loadBalancingScheme, protocol)'
```

**Expected result:** `bes-net EXTERNAL_MANAGED HTTP`. A global external
HTTP(S) load balancer fronts backends in many regions from one anycast IP.

### Lab 6.10 — Configuring Cloud CDN *(NE 3.2)*

```bash
gcloud compute backend-services update bes-net --global --enable-cdn
gcloud compute backend-services describe bes-net --global --format='value(enableCDN)'
```

**Expected result:** `True`. CDN is a flag on the backend service — the
design decision is *which* backend caches, not a separate product.

### Lab 6.11 — Configuring Cloud DNS *(NE 3.3)*

```bash
gcloud dns managed-zones create zone-net --dns-name="lab.example.com." \
  --description="lab" --visibility=private --networks=vpc-net
gcloud dns managed-zones describe zone-net --format='value(name, visibility)'
```

**Expected result:** `zone-net private`. A private zone resolves only
inside the attached VPC — the split-horizon design DNS questions turn on.

### Lab 6.12 — Configuring Cloud Interconnect and VPN *(NE 4.1, 4.2, 4.3)*

```bash
gcloud compute vpn-gateways create vgw-net --network=vpc-net --region=us-central1
gcloud compute vpn-gateways describe vgw-net --region=us-central1 \
  --format='value(name, vpnInterfaces[].ipAddress.list())'
```

**Expected result:** the gateway with two interface IPs (HA VPN is
dual-interface by design). Interconnect and VPN both terminate on
constructs like this and route via the Cloud Router from Lab 6.3.

### Lab 6.13 — Logging and monitoring network operations *(NE 5.1)*

```bash
gcloud compute networks subnets update snet-us --region=us-central1 \
  --enable-flow-logs
gcloud compute networks subnets describe snet-us --region=us-central1 \
  --format='value(logConfig.enable)'
```

**Expected result:** `True`. VPC Flow Logs are the raw material for
network monitoring and are off by default — enabling them is a deliberate,
billable choice.

### Lab 6.14 — Troubleshooting connectivity *(NE 5.2)*

```bash
gcloud compute instances create vm-a --zone=us-central1-a --machine-type=e2-micro \
  --subnet=snet-us --no-address --image-family=debian-12 --image-project=debian-cloud
gcloud network-management connectivity-tests create test-net \
  --source-instance=vm-a --destination-instance=vm-a \
  --protocol=ICMP 2>&1 | head -3
```

**Expected result:** a test created, or an enable-API prompt. Connectivity
Tests give Google's own reachability verdict — the answer to "is it
firewall, route, or destination?"

### Lab 6.15 — Cloud Armor and firewall policies *(NE 6.1, 6.2)*

```bash
gcloud compute security-policies create armor-net --description="lab"
gcloud compute security-policies rules create 1000 \
  --security-policy=armor-net --src-ip-ranges="203.0.113.0/24" --action=deny-403
gcloud compute security-policies describe armor-net \
  --format='value(rules[].action.list())'
```

**Expected result:** `deny-403;allow` (your rule plus the default). Cloud
Armor is edge WAF/DDoS policy, distinct from VPC firewall rules that act
at the instance.

### Lab 6.16 — Packet Mirroring and network appliances *(NE 6.4)*

```bash
gcloud compute packet-mirrorings list --region=us-central1 \
  --format='value(name)' 2>&1 | head -3
```

**Expected result:** an empty list (or enable prompt) on a fresh project.
Packet Mirroring copies traffic to a collector for inspection — the design
hook for a network virtual appliance.

### Lab 6.17 — Bootstrapping and managing the organization *(DevOps 1.1–1.5)*

```bash
gcloud resource-manager org-policies list --project="$PROJECT_ID" \
  --format='table(constraint)' | head -6
```

**Expected result:** effective constraints. Bootstrapping an org is
codifying its hierarchy and guardrails — organization policy is where that
becomes real.

### Lab 6.18 — CI/CD pipelines and secrets *(DevOps 2.1–2.4)*

```bash
echo -n "s3cr3t" | gcloud secrets create lab-secret --data-file=- 2>&1 | head -2
gcloud secrets versions access latest --secret=lab-secret
```

**Expected result:** `s3cr3t`. Secret Manager, not pipeline variables, is
where deployment secrets live — securing the pipeline (topic 2.4) is this.

### Lab 6.19 — SRE practices and error budgets *(DevOps 3.1–3.3)*

```text
# An SLO converts release risk into arithmetic. Fill and compute:
SLO 99.9% over 28 days
  total minutes   = 28 * 24 * 60 = 40,320
  error budget    = 40,320 * 0.001 = ______ minutes
```

**Expected result:** 40.3 minutes. Spend it deliberately on releases;
when exhausted, stop shipping. This is DevOps section 3 in one figure.

### Lab 6.20 — Observability and troubleshooting *(DevOps 4.1–4.5)*

```bash
gcloud run deploy svc-obs \
  --image=us-docker.pkg.dev/cloudrun/container/hello \
  --region=us-central1 --allow-unauthenticated
gcloud logging read 'resource.type="cloud_run_revision"' --limit=3 \
  --format='table(timestamp, severity)'
```

**Expected result:** the service URL, then recent log lines. Telemetry,
logs, metrics, and traces are the four observability topics — logs are the
one on by default.

### Lab 6.21 — Optimizing performance and cost / FinOps *(DevOps 5.1, 5.2)*

```bash
gcloud run services update svc-obs --region=us-central1 --max-instances=2 --cpu=1
gcloud run services describe svc-obs --region=us-central1 \
  --format='value(spec.template.metadata.annotations["autoscaling.knative.dev/maxScale"])'
```

**Expected result:** `2`. Capping max instances is the simplest FinOps
control — it bounds the cost of a traffic spike.

### Lab 6.22 — Negative test and cleanup

Prove VPC firewall default-deny, not routing, is what blocks traffic:

```bash
gcloud compute firewall-rules delete allow-net-internal --quiet
gcloud compute instances create vm-b --zone=us-central1-a --machine-type=e2-micro \
  --subnet=snet-us --no-address --image-family=debian-12 --image-project=debian-cloud
gcloud compute ssh vm-a --zone=us-central1-a --command="ping -c2 -W2 10.60.0.3" 2>&1 | tail -4
```

**Expected result:** the ping **fails** (100% loss) even though both VMs
are in one subnet with valid routes — because ingress is denied by
default once the allow rule is gone. Re-create the rule and the ping
succeeds; that pair is the whole lesson.

```bash
gcloud projects delete "$PROJECT_ID" --quiet
gcloud projects describe "$PROJECT_ID" --format='value(lifecycleState)'
```

**Expected result:** `DELETE_REQUESTED` — the cluster, load balancer,
VPN gateway, Cloud Run service, and network are removed together.

## Lab Verification

Complete this sign-off once cross-region connectivity has been proven
without peering and an error budget computed. Until then, the lab is
unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The three infrastructure-facing professional certifications — Network
Engineer, DevOps Engineer, and Developer — are each 2 hours, $200, and
valid two years. Google Cloud's **global VPC with regional subnets** is
the platform fact that changes network design: regions connect inside one
VPC without peering, so multiple VPCs signal isolation rather than
connectivity, which inverts the driver behind Azure's hub-and-spoke.
DevOps Engineer's backbone is **SRE** — SLIs, SLOs, error budgets, and
toil — where the error budget converts release-risk arguments into
arithmetic. Developer covers the application surface, where Cloud Run is
the default for stateless services and GKE is the answer only when
Kubernetes semantics are genuinely needed. The three overlap at
instrumentation and delivery, but each carries its own two-year renewal.

- [ ] Can explain why a global VPC changes topology design.
- [ ] Can define SLI, SLO, error budget, and toil, and do the arithmetic.
- [ ] Knows why an infrastructure metric makes a poor SLO.
- [ ] Can choose between Cloud Run and GKE from requirements.
- [ ] Has proven cross-region connectivity without peering.
- [ ] Completed the hands-on lab, including the firewall negative test.
