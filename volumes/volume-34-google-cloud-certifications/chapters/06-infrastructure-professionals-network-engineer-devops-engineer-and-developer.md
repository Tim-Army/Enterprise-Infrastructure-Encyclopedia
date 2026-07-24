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

**Objective:** Prove that one global VPC connects regions without peering,
then convert an SLO into an error budget you could actually defend.

**Cost note:** VPC and subnets are free. Two `e2-micro` instances are
minimal; step 6 deletes everything.

**Prerequisites**

- The sandbox project and budget alert from Chapter 01.
- `gcloud` authenticated.

**Steps**

1. **Build the global VPC (15 minutes).** Create `vpc-global` with subnets
   in `us-central1` and `europe-west1`.

   **Expected result:** one network, two regional subnets.

2. **Predict, then verify (10 minutes).** Write down whether a VM in
   `snet-us` can reach a VM in `snet-eu`, and why. Then create one VM in
   each and add a firewall rule permitting internal ICMP:

   ```bash
   gcloud compute firewall-rules create allow-internal-icmp \
     --network=vpc-global --allow=icmp --source-ranges=10.30.0.0/16,10.31.0.0/16
   ```

   **Expected result:** they reach each other with **no peering
   configured** — the platform difference this chapter turns on.

3. **Negative test (10 minutes).** Delete the firewall rule and retry.

   **Expected result:** connectivity fails while routing is unchanged —
   demonstrating that inside one VPC the usual culprit is firewall, not
   routing. Re-create the rule afterward.

4. **Deploy and measure (15 minutes).** Deploy the Cloud Run sample, send
   a handful of requests, and read request latency in Cloud Monitoring.

   **Expected result:** a latency distribution to base an SLI on, with the
   first request visibly slower (cold start).

5. **Compute an error budget (10 minutes).** Choose an SLO from the
   observed latency and compute the monthly error budget in minutes.

   **Expected result:** a defensible SLO and a budget figure you derived
   rather than guessed.

6. **Cleanup:**

   ```bash
   gcloud run services delete svc-demo --region=us-central1 --quiet
   gcloud compute instances delete vm-us vm-eu --zone-flags... --quiet
   gcloud compute networks delete vpc-global --quiet
   ```

   Simplest reliable teardown: delete the whole project. Confirm the
   budget shows no unexpected spend.

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
