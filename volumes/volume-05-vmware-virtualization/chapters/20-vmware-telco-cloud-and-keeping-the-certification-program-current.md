# Chapter 20: VMware Telco Cloud, and Keeping the Certification Program Current

![Two halves. On the left, the three Telco Cloud specialist skills exams on the older 5V0 generation — Telco Cloud Platform Specialist (5V0-36.22), Telco Cloud NFV Specialist (5V0-37.22), and Telco Cloud Automation Specialist (5V0-44.21) — targeting service-provider network-functions virtualization outside the mainstream vSphere and VCF paths. On the right, a four-step currency check that repeats on a cadence: re-list the tiers and tracks from Broadcom's certification pages, re-confirm every exam code against its own page, flag retirements and new generations, and update this volume and its appendix. An arrow returns from step four to step one.](../../../diagrams/volume-05-vmware-virtualization/chapter-20-telco-and-program-currency-map.svg)

*Figure 20-1. A niche specialist track and the recurring check that keeps the whole VMware certification map in this volume honest — the program churns, so the check repeats.*

## Learning Objectives

- Identify the three VMware Telco Cloud specialist skills exams — Platform
  (5V0-36.22), NFV (5V0-37.22), and Automation (5V0-44.21) — and place them
  as a service-provider niche outside the mainstream vSphere/VCF and NSX
  paths.
- Explain what the `5V0` specialist-skills code family is and how it
  differs from the `2V0`/`6V0` professional and `3V0` advanced families in
  earlier chapters.
- Explain why the VMware certification program requires a recurring
  currency check, using the program's own recent churn (the Broadcom
  acquisition, VCF 9.0's new role series, generational code changes) as the
  evidence.
- Run a four-step currency check against Broadcom's primary sources that
  re-verifies the tiers, every exam code, retirements, and this volume's
  and appendix's accuracy — and know why third-party summaries are not
  acceptable sources for it.
- Feed the check's findings back into this volume, its Master Appendices
  course catalog, and the repository's certification blueprint, keeping the
  whole VMware map current rather than letting it drift silently.

## Theory and Architecture

Two things belong at the end of this volume's certification coverage: the
one remaining VMware track it has not addressed — **Telco Cloud** — and the
discipline that keeps everything the volume claims about the program *true*
over time. They are paired here deliberately: Telco Cloud is a small, older
niche whose exams are most likely to change availability quietly, which
makes it the natural example for why a recurring currency check matters.

As with every preparation chapter here, this is study and review material.
It names exam codes verified against Broadcom's certification pages; it does
not reproduce exam content. Confirm current codes, availability, and
blueprints directly before scheduling — this chapter's second half exists
precisely because that confirmation is not optional.

### The Telco Cloud specialist skills exams

VMware Telco Cloud targets communications service providers running
**network functions virtualization (NFV)** — the virtualized 4G/5G core and
RAN workloads that run on a telco-grade platform built from vSphere, NSX,
and VMware's Telco Cloud products. Three specialist skills exams cover it:

| Exam | Code | Scope |
| --- | --- | --- |
| Telco Cloud Platform Specialist | 5V0-36.22 | The CaaS/telco platform layer on vSphere + NSX |
| Telco Cloud NFV Specialist | 5V0-37.22 | NFV infrastructure — the virtualized network-functions layer |
| Telco Cloud Automation Specialist | 5V0-44.21 | Telco Cloud Automation (TCA) orchestration of network functions |

These are a **service-provider specialization**, not a step in the
vSphere/VCF/NSX progression the rest of this volume follows. A general
enterprise administrator does not need them; an engineer at a mobile
operator or NFV integrator does. They build on the vSphere and NSX
foundations this volume teaches (Chapters 1–11), but their subject matter —
telco platform, NFV infrastructure, TCA orchestration — sits outside it.

### The `5V0` code family, in context

This volume has now touched four VMware exam-code families, and the prefix
is a reliable signal of tier and scope:

- **`2V0`** — mainstream professional (VCP): broad, role-defining
  (Chapters 12–17).
- **`6V0`** — specialist professional: narrow single-product VCP (VCP-AVI,
  VCP-PCS, Chapter 17).
- **`3V0`** — advanced (VCAP): advanced depth, design or deploy
  (Chapter 18).
- **`5V0`** — **specialist skills**: focused skills exams for a specific
  solution area, this chapter's Telco Cloud exams among them. Their older
  `.21`/`.22` generation dates flag that they trail the current product
  releases, which is exactly the kind of fact a currency check must
  re-confirm.

### Why the program needs a recurring currency check

The rest of this chapter is not about an exam. It is about a maintenance
discipline, and it is here because the VMware certification program has
churned more than almost any other on this shelf:

- The **Broadcom acquisition** reorganized the entire program — renaming
  VCDX to Distinguished Expert, restructuring VCP around VVF/VCF, and
  moving training to Learning@Broadcom.
- **VCF 9.0** introduced an entirely new eight-exam advanced role series
  (Chapter 18) on `.25`/`.26` codes that did not exist a generation ago.
- Individual exams change generation — VCP-DCV sits on vSphere 8 while the
  VVF/VCF exams moved to 9.0 — and specialist exams like Telco Cloud's can
  be retired quietly as their products age.

A volume that states exam codes will drift out of true unless someone
re-verifies it. This volume's answer is a scheduled check, run on the same
cadence as the repository's other certification-currency checks, against
Broadcom's own pages — never third-party summaries, which drift worse than
the vendor and have been found wrong during exactly these checks elsewhere
in this encyclopedia.

## Design Considerations

- **Take a Telco Cloud exam only for a service-provider role.** These are a
  genuine specialization. For enterprise vSphere/VCF/NSX work they are off
  the path; pursue them when the job is NFV, a virtualized mobile core, or
  a telco platform integration, and skip them otherwise.
- **Confirm Telco Cloud availability before planning.** Because the `5V0`
  Telco exams are on an older generation, they are among the most likely in
  this volume to be retired or renumbered. Verify each still exists on
  Broadcom's page before investing study time — do not assume from this
  chapter that 5V0-36.22, 5V0-37.22, and 5V0-44.21 are all still live.
- **Run the currency check on a cadence, not on demand.** The value of the
  check is that it catches silent drift — an exam retired, a code bumped a
  generation, a new role added — before a reader relies on stale
  information. Schedule it; do not wait for a reader to hit a dead link.
- **Primary sources only.** The check is worthless if it trusts aggregator
  sites. Every code is confirmed against its own exam page on Broadcom, and
  the tier/track list against Broadcom's certification landing pages. A
  third-party "2026 VMware certification guide" is a lead to verify, never
  a source to cite.
- **Feed findings all the way through.** A currency check that updates only
  this chapter leaves the volume README, the study plans, the
  [Master Appendices course catalog](../../volume-97-master-appendices/chapters/07-appendix-vmware-broadcom-certifications-and-course-access.md),
  and [CERTIFICATION_BLUEPRINTS.md](../../../CERTIFICATION_BLUEPRINTS.md)
  stale. Propagate every change to all of them in one pass.

## Implementation and Automation

### The four-step currency check

```text
# Run on the repository's certification-currency cadence. Each step's
# output feeds the next; step 4 closes the loop back to this volume.

1. Re-list tiers & tracks
   Source: Broadcom certification landing pages
   Output: current set of VCP / VCAP / Distinguished Expert / specialist
           credentials and their tracks (vSphere, VCF, NSX, Avi, PCS,
           Telco Cloud)

2. Re-confirm every exam code
   Source: each exam's own page (never a third-party summary)
   Output: verified code per exam; note any that no longer resolve

3. Flag retirements & new generations
   Output: exams retired or superseded (with any published end date),
           and new codes/roles that have appeared since last check

4. Update this volume + appendix
   Targets: Volume V chapters, README exam tables & study plans,
            Master Appendices Chapter 07 course catalog,
            CERTIFICATION_BLUEPRINTS.md
```

### Harvesting codes from Broadcom's own data source

```bash
# Broadcom's certification pages inject the exam code from a JSON API
# rather than in the raw HTML, so a plain fetch of the page misses it.
# Query the education-program JSON endpoint per certification slug and
# read the code out — the primary-source method used to verify this
# volume. Replace <slug> with the certification's URL slug.
curl -s 'https://www.broadcom.com/api/getjson?url=support/education/vmware/certification/<slug>&locale=en-us&type=education_program' \
  | grep -oE '[0-9]V0-[0-9]{2}\.[0-9]{2}'
```

### A drift log to make the check auditable

```text
# Record each check so drift is visible over time. One row per finding.

Date       | Exam / item          | Was          | Now / status      | Action
-----------|----------------------|--------------|-------------------|--------
2026-07-22 | VCF role series      | (absent)     | 3V0-11.26 … 25.25 | added ch18
2026-07-22 | VCDX                 | VCDX code    | Distinguished Exp | added ch19
2026-07-22 | Telco Cloud (5V0)    | —            | still live        | added ch20
```

## Validation and Troubleshooting

- **A resolving exam page is the pass signal.** For each code, the check
  passes when the exam's own Broadcom page resolves and shows that code. A
  page that 404s or shows a different code is the finding — record it in the
  drift log and trace it to a retirement or a generation bump.
- **Silence is the failure mode.** The risk this check addresses is not a
  wrong answer but an unnoticed change. If a check finds nothing, confirm it
  actually re-verified every code rather than skipping — a check that
  quietly no-ops is worse than none, because it manufactures false
  confidence.
- **Cross-check the appendix and blueprint.** After updating chapters,
  verify the [course catalog appendix](../../volume-97-master-appendices/chapters/07-appendix-vmware-broadcom-certifications-and-course-access.md)
  and [CERTIFICATION_BLUEPRINTS.md](../../../CERTIFICATION_BLUEPRINTS.md)
  carry the same codes and the same retirements. A mismatch between them and
  this volume is itself a drift finding.
- **Telco Cloud is the canary.** Of everything this volume tracks, the
  `5V0` Telco exams are the likeliest to change first. If a check finds one
  retired, treat it as a prompt to re-verify the whole program more
  carefully, not as an isolated edit.

## Security and Best Practices

- Verify only against Broadcom's official domains; a currency check that
  follows a link from a search result to a look-alike site defeats its own
  purpose. Confirm you are on `broadcom.com` before trusting a code.
- Do not publish or circulate any exam content encountered while verifying —
  the check reads certification and exam-guide *metadata* (codes, names,
  tiers), never exam items, and must stay on that side of the line.
- Register for any Telco Cloud exam only through Broadcom's authorized
  testing partner, and confirm current identification and proctoring
  requirements from the official portal before exam day.
- Keep the drift log with the repository, not in a personal note — the
  point is that the next person to run the check inherits a verifiable
  history rather than re-deriving it from scratch.

## References and Knowledge Checks

**References**

- [Broadcom Education Services — VMware certification](https://www.broadcom.com/support/education/vmware) —
  the authoritative certification landing pages and per-exam guides for the
  Telco Cloud specialist exams (5V0-36.22, 5V0-37.22, 5V0-44.21) and for
  the whole program the currency check re-verifies.
- [VMware Telco Cloud documentation](https://techdocs.broadcom.com/us/en/vmware-sonp/telco-cloud.html) —
  product reference for the Telco Cloud Platform, NFV, and Automation
  exams.
- [CERTIFICATION_BLUEPRINTS.md](../../../CERTIFICATION_BLUEPRINTS.md) —
  the repository's certification-to-volume mapping that the check keeps
  current.
- [Appendix — VMware and Broadcom Certifications and Course Access](../../volume-97-master-appendices/chapters/07-appendix-vmware-broadcom-certifications-and-course-access.md) —
  the course catalog the check updates alongside this volume.
- See [Chapters 17–19](17-completing-the-vcp-tier-dcv-vcf-architect-avi-and-private-cloud-security.md)
  for the VCP, VCAP, and Distinguished Expert tiers this check verifies.

**Knowledge checks** *(original conceptual review questions — not
reproductions of any Broadcom exam item)*

1. Name the three Telco Cloud specialist exams and explain why they are off
   the path for a general enterprise administrator.
2. Distinguish the `2V0`, `6V0`, `3V0`, and `5V0` code families by tier and
   scope, giving one exam in each.
3. Give three specific changes in the VMware program since the Broadcom
   acquisition that justify a recurring currency check.
4. Walk through the four-step currency check and explain why step 2 forbids
   third-party summaries as sources.
5. Why are the `5V0` Telco Cloud exams described as the "canary" for this
   volume's currency, and what should finding one retired trigger?

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **every objective in
the three Telco Cloud specialist-skills exam guides** — Telco Cloud
Automation (5V0-44.21, 42), Telco Cloud NFV (5V0-37.22, 31), and Telco
Cloud Platform (5V0-36.22, 25) — each mapped in the volume README's
coverage tables. These are older knowledge-format exams, so each objective's
lab is a **read-only inspection walkthrough**: one real command that
surfaces the concept the objective tests, with the common misconception as
the negative test. The chapter closes with the program-currency lab (20.99).

**Shared prerequisites for Labs 20.1–20.98**

- A VMware Telco Cloud lab: Telco Cloud Automation (TCA) Manager reachable
  at `$TCA` with an `Authorization` header in `$T`; a TKG/CaaS cluster with
  `kubectl` context set; VMware Cloud Director (for NFV) at `$VCD`; and
  `govc` pointed at the underlying vSphere. All labs are read-only.
- **Cost:** none; no lab creates or deletes resources.

**Telco Cloud Automation (5V0-44.21) — Labs 20.1–20.42**

### Lab 20.1 — Role of TCA within the NFV architecture (Objective 1.1)

**Objective:** Read TCA's role as the NFV orchestrator/VNFM.

```bash
curl -sk -H "$T" "$TCA/hybridity/api/vims" | jq -r '.[] | "\(.vimName)\t\(.vimType)"'
```

**Expected result:** the virtual infrastructure managers (VIMs) TCA drives —
TCA is the orchestration/VNF-manager layer above them, per ETSI MANO.

**Negative test:** treating TCA as a VIM itself is wrong; it orchestrates
VIMs (vSphere, VCD, Kubernetes), it is not one.

### Lab 20.2 — Role of OVF within a network function (Objective 1.2)

**Objective:** Read the OVF a VNF descriptor references.

```bash
curl -sk -H "$T" "$TCA/telco/api/catalogs/networkfunction" | jq -r '.[] | .name' | head
```

**Expected result:** VNF catalog entries whose descriptors package an OVF —
OVF is the VM image/packaging format a VNF is instantiated from.

**Negative test:** a CNF uses a Helm chart, not an OVF; conflating the two
packaging formats is the trap.

### Lab 20.3 — Role of a Helm chart with a CNF (Objective 1.3)

**Objective:** List the Helm releases backing a CNF.

```bash
helm list -A -o json | jq -r '.[] | "\(.name)\t\(.chart)"'
```

**Expected result:** Helm releases — a CNF is deployed and lifecycle-managed
as a Helm chart on Kubernetes.

**Negative test:** expecting an OVF for a CNF; container network functions
have no OVF — Helm/images are their packaging.

### Lab 20.4 — Life Cycle Management events (Objective 1.4)

**Objective:** Read LCM operation history for a network function.

```bash
curl -sk -H "$T" "$TCA/telco/api/nslcm/v2/vnf_lcm_op_occs" | jq -r '.[] | "\(.operation)\t\(.operationState)"' | head
```

**Expected result:** LCM operations (INSTANTIATE, SCALE, HEAL, TERMINATE)
with state — the managed lifecycle events TCA drives.

**Negative test:** a manual VM power-on is not an LCM event; LCM is the
orchestrated, descriptor-driven operation set.

### Lab 20.5 — Characteristics of self-healing (Objective 1.5)

**Objective:** Read the healing policy on a network function.

```bash
curl -sk -H "$T" "$TCA/telco/api/nslcm/v2/vnf_instances" | jq -r '.[] | "\(.vnfInstanceName)\t\(.instantiationState)"' | head
```

**Expected result:** instances whose descriptor defines healing — TCA
detects a failed VNF/CNF and re-instantiates it automatically.

**Negative test:** vSphere HA restarts a VM but does not re-run VNF
onboarding; TCA self-healing restores the network function, not just the VM.

### Lab 20.6 — TCA distributed architecture (Objective 2.1)

**Objective:** Read the TCA Manager / TCA control-plane appliances.

```bash
curl -sk -H "$T" "$TCA/hybridity/api/nodes" | jq -r '.[] | "\(.role)\t\(.status)"'
```

**Expected result:** TCA-Manager and TCA-CP (control plane) nodes — TCA is
distributed, with a central Manager and per-VIM control-plane instances.

**Negative test:** expecting a single monolithic appliance; the TCA-CP is
deployed near each VIM for local orchestration.

### Lab 20.7 — Why a TCA control-plane element is required (Objective 2.2)

**Objective:** Read the TCA-CP registered against a VIM.

```bash
curl -sk -H "$T" "$TCA/hybridity/api/vims" | jq -r '.[] | "\(.vimName)\tcp:\(.tcaCpAssociated // false)"'
```

**Expected result:** each VIM associated with a TCA-CP — the CP executes
orchestration workflows locally at the VIM.

**Negative test:** a VIM with no TCA-CP cannot run CaaS/infra automation;
the CP is the required local executor.

### Lab 20.8 — Integrate a VIM infrastructure (Objective 2.4)

**Objective:** Read a registered VIM's connection detail.

```bash
curl -sk -H "$T" "$TCA/hybridity/api/vims" | jq -r '.[] | "\(.vimName)\t\(.vimType)\t\(.vimUrl)"'
```

**Expected result:** VIMs (VC_VIM / VCD_VIM / KUBERNETES) with their URLs —
the integration TCA needs to place workloads.

**Negative test:** registering a VIM with wrong credentials shows a
connection-error status; integration requires reachable, authenticated
endpoints.

### Lab 20.9 — Integrate vRO with virtual infrastructures (Objective 2.5)

**Objective:** Read the vRealize Orchestrator endpoint TCA calls for
extensibility.

```bash
curl -sk -H "$T" "$TCA/hybridity/api/service/vro/endpoints" | jq -r '.[] | .name' 2>/dev/null
```

**Expected result:** the vRO endpoint(s) — TCA invokes vRO workflows for
custom infrastructure automation during onboarding.

**Negative test:** expecting TCA to run arbitrary scripts natively; complex
custom automation is delegated to vRO workflows.

### Lab 20.10 — Tags in TCA (Objective 2.6)

**Objective:** Read the tags TCA uses for placement and RBAC filtering.

```bash
curl -sk -H "$T" "$TCA/hybridity/api/tags" | jq -r '.[] | "\(.name)=\(.value)"' | head
```

**Expected result:** key/value tags — TCA uses them for resource placement
and tag-based permission filtering.

**Negative test:** untagged resources fall outside tag-scoped permissions and
placement policies; tags are the selector.

### Lab 20.11 — Verify the VIM connection URL (Objective 3.1)

**Objective:** Confirm the reachable URL for a VIM before workload
placement.

```bash
curl -sk -H "$T" "$TCA/hybridity/api/vims" | jq -r '.[] | .vimUrl'
```

**Expected result:** each VIM's endpoint URL — the value that must resolve
and authenticate for TCA to place workloads.

**Negative test:** an unreachable VIM URL blocks all placement to that VIM;
verify the URL, not just the credentials.

### Lab 20.12 — Configure a compute profile for a VIM (Objective 3.2)

**Objective:** Read the compute profiles that scope CaaS placement.

```bash
curl -sk -H "$T" "$TCA/telco/api/infra/compute/profiles" | jq -r '.[] | .name' 2>/dev/null
```

**Expected result:** compute profiles mapping clusters/resource pools to
CaaS — the placement scope for cluster nodes.

**Negative test:** deploying a workload cluster with no matching compute
profile fails placement; the profile is a prerequisite.

### Lab 20.13 — Business benefits of automated CaaS (Objective 4.1)

**Objective:** Read the CaaS clusters TCA manages as one fleet.

```bash
curl -sk -H "$T" "$TCA/telco/api/caas/v1/clusters" | jq -r '.[] | "\(.clusterName)\t\(.status)"'
```

**Expected result:** managed Kubernetes clusters — automated CaaS delivers
consistent, repeatable clusters at telco scale (the business benefit).

**Negative test:** hand-built clusters drift and do not scale to hundreds of
sites; automation is the benefit.

### Lab 20.14 — Kubernetes vs Tanzu Kubernetes (Objective 4.2)

**Objective:** Read the TKG cluster's distribution.

```bash
kubectl get tanzukubernetesclusters -A 2>/dev/null || kubectl get clusters -A
```

**Expected result:** TKG-managed clusters — Tanzu Kubernetes is VMware's
supported, lifecycle-managed Kubernetes distribution atop upstream k8s.

**Negative test:** upstream vanilla Kubernetes has no TKG lifecycle
integration with TCA; TCA manages TKG clusters specifically.

### Lab 20.15 — TKG cluster types (Objective 4.3)

**Objective:** Distinguish management vs workload clusters.

```bash
kubectl config get-contexts -o name
kubectl get clusters -A 2>/dev/null | grep -iE 'mgmt|management|workload'
```

**Expected result:** a management cluster (runs Cluster API) and workload
clusters (run CNFs) — the two TKG cluster roles.

**Negative test:** running CNFs on the management cluster is unsupported;
workloads belong on workload clusters.

### Lab 20.16 — Deploy a Management cluster (Objective 4.4)

**Objective:** Confirm the management cluster is up and serving Cluster API.

```bash
kubectl get pods -n capi-system 2>/dev/null
kubectl get clusters -A 2>/dev/null
```

**Expected result:** Cluster API controllers `Running` in the management
cluster — it is the control plane that provisions workload clusters.

**Negative test:** a management cluster with Cluster API pods crashing cannot
create workload clusters; it is the prerequisite for all CaaS.

### Lab 20.17 — Deploy a Workload cluster (Objective 4.5)

**Objective:** Read a workload cluster's nodes and readiness.

```bash
kubectl get nodes -o wide
kubectl get machinedeployments -A 2>/dev/null
```

**Expected result:** worker nodes `Ready` — a workload cluster provisioned
by the management cluster, ready for CNFs.

**Negative test:** nodes stuck `NotReady` usually mean a CNI or compute-
profile issue; the cluster is not usable until nodes are Ready.

### Lab 20.18 — Scale a node pool (Objective 4.6)

**Objective:** Read the node pool's current and desired replica count.

```bash
kubectl get machinedeployments -A -o custom-columns=NAME:.metadata.name,REPLICAS:.spec.replicas,READY:.status.readyReplicas 2>/dev/null
```

**Expected result:** the node-pool replica counts — scaling a pool changes
`spec.replicas` and Cluster API adds/removes nodes.

**Negative test:** editing nodes directly (kubeadm) instead of the node pool
is not reconciled by Cluster API and drifts; scale via the pool.

### Lab 20.19 — CaaS with no internet connectivity (Objective 4.7)

**Objective:** Confirm the local (air-gapped) image registry the clusters
pull from.

```bash
kubectl get pods -A -o jsonpath='{range .items[*]}{.spec.containers[*].image}{"\n"}{end}' | sort -u | head
```

**Expected result:** images pulled from a local Harbor registry, not the
internet — the prerequisite for air-gapped CaaS.

**Negative test:** a cluster whose images reference `docker.io` cannot deploy
air-gapped; images must be mirrored locally first.

### Lab 20.20 — Integrate Harbor with TCA (Objective 5.1)

**Objective:** Confirm the Harbor registry TCA/partners use.

```bash
curl -sk "$HARBOR/api/v2.0/health" | jq -r '.status'
curl -sk -u "$HARBOR_CRED" "$HARBOR/api/v2.0/projects" | jq -r '.[].name' | head
```

**Expected result:** Harbor `healthy` with projects — the private registry
that stores CNF images and Helm charts for onboarding.

**Negative test:** onboarding a CNF whose chart references an unreachable
registry fails image pull; Harbor integration must be reachable.

### Lab 20.21 — Business benefit of infrastructure automation (Objective 6.1)

**Objective:** Read the infra-automation (SDDC) tasks TCA has run.

```bash
curl -sk -H "$T" "$TCA/telco/api/infra/tasks" | jq -r '.[] | "\(.type)\t\(.status)"' 2>/dev/null | head
```

**Expected result:** automated infra tasks (host add, cluster config) — the
benefit is repeatable, error-free infrastructure at many sites.

**Negative test:** manual per-site infrastructure build does not scale to a
telco edge footprint; automation is the benefit.

### Lab 20.22 — Infrastructure automation versioning (Objective 6.2)

**Objective:** Read the versioned infrastructure automation designs.

```bash
curl -sk -H "$T" "$TCA/telco/api/infra/designs" | jq -r '.[] | "\(.name)\tv\(.version)"' 2>/dev/null | head
```

**Expected result:** infra designs with version numbers — automation is
versioned so a site can be built to a known, repeatable spec.

**Negative test:** an unversioned ad-hoc build cannot be reproduced or
rolled back; versioning is what makes it deterministic.

### Lab 20.23 — Network services vs network functions (Objective 7.1)

**Objective:** Distinguish an NS from its member NFs.

```bash
curl -sk -H "$T" "$TCA/telco/api/nslcm/v2/ns_instances" | jq -r '.[] | "\(.nsInstanceName)\tNFs:\(.vnfInstance | length)"' 2>/dev/null
```

**Expected result:** network-service instances each composed of multiple
network functions — an NS orchestrates and connects NFs.

**Negative test:** treating an NS as a single NF misses the
service-composition and connectivity an NSD defines.

### Lab 20.24 — CNF vs VNF (Objective 7.2)

**Objective:** Classify onboarded functions by type.

```bash
curl -sk -H "$T" "$TCA/telco/api/catalogs/networkfunction" | jq -r '.[] | "\(.name)\t\(.nfType // .type)"' | head
```

**Expected result:** functions tagged VNF (VM-based) or CNF (container-
based) — the two network-function packaging models.

**Negative test:** a CNF cannot run on a bare VIM without Kubernetes; VNF and
CNF have different infrastructure requirements.

### Lab 20.25 — Characteristics of NFD and NSD (Objective 7.3)

**Objective:** Read a network-function descriptor and a network-service
descriptor.

```bash
curl -sk -H "$T" "$TCA/telco/api/catalogs/networkfunction" | jq -r '.[0] | .name, .infraRequirements' 2>/dev/null
```

**Expected result:** the NFD (function packaging + infra requirements) and
NSD (service composition) — the TOSCA/descriptor artifacts onboarding uses.

**Negative test:** onboarding without a valid descriptor fails; the NFD/NSD
is the contract TCA instantiates from.

### Lab 20.26 — Identify a descriptor attribute (Objective 7.4)

**Objective:** Read a specific attribute from a descriptor.

```bash
curl -sk -H "$T" "$TCA/telco/api/catalogs/networkfunction" | jq -r '.[0].infraRequirements.nodeComponents' 2>/dev/null
```

**Expected result:** attributes such as node components, resources, and
policies — the fields a descriptor question asks you to locate.

**Negative test:** an attribute in the wrong descriptor section is ignored at
instantiation; attribute placement matters.

### Lab 20.27 — Onboard a network function (Objective 7.5)

**Objective:** Read the catalog to confirm a function is onboarded.

```bash
curl -sk -H "$T" "$TCA/telco/api/catalogs/networkfunction" | jq -r '.[] | "\(.name)\t\(.onboardingState // "ONBOARDED")"' | head
```

**Expected result:** functions in an onboarded state — onboarding uploads the
descriptor + artifacts into the catalog, ready to instantiate.

**Negative test:** an onboarding with a missing artifact stays in an error
state and cannot be instantiated; all referenced artifacts must be present.

### Lab 20.28 — Prerequisites for onboarding a network service (Objective 7.6)

**Objective:** Confirm the member NFs an NSD requires exist first.

```bash
curl -sk -H "$T" "$TCA/telco/api/catalogs/networkservice" | jq -r '.[0].nestedNfd // .[0].name' 2>/dev/null
```

**Expected result:** the NFs referenced by the NSD — all must be onboarded
before the network service can be.

**Negative test:** onboarding an NSD that references a missing NFD fails; the
member functions are a prerequisite.

### Lab 20.29 — Role of late binding (Objective 7.7)

**Objective:** Read where infrastructure values are bound at instantiation,
not design.

```bash
curl -sk -H "$T" "$TCA/telco/api/catalogs/networkfunction" | jq -r '.[0].infraRequirements' 2>/dev/null | head
```

**Expected result:** infra requirements resolved at instantiate time (VIM,
network, compute profile) — late binding defers placement decisions until
deployment.

**Negative test:** hard-coding a VIM in the descriptor defeats late binding
and prevents reusing the descriptor across sites.

### Lab 20.30 — Instantiate a VNF (Objective 7.9)

**Objective:** Read a VNF instance and its state.

```bash
curl -sk -H "$T" "$TCA/telco/api/nslcm/v2/vnf_instances" | jq -r '.[] | "\(.vnfInstanceName)\t\(.instantiationState)"' | head
```

**Expected result:** VNF instances in `INSTANTIATED` — instantiation places
the VNF onto a VIM per its descriptor and late-bound inputs.

**Negative test:** instantiating without required late-bound inputs (network,
compute) fails; the inputs complete the descriptor.

### Lab 20.31 — Network function inventory (Objective 7.11)

**Objective:** Read the inventory of instantiated functions.

```bash
curl -sk -H "$T" "$TCA/telco/api/nslcm/v2/vnf_instances" | jq -r 'length'
```

**Expected result:** the count and detail of live network functions — TCA's
inventory of what is deployed where.

**Negative test:** relying on VIM inventory alone misses TCA's function-level
metadata (descriptor, LCM history); TCA's inventory is authoritative for NFs.

### Lab 20.32 — vCenter's role in credentials (Objective 8.1)

**Objective:** Read the vCenter VIM that supplies infrastructure
credentials.

```bash
curl -sk -H "$T" "$TCA/hybridity/api/vims" | jq -r '.[] | select(.vimType=="VC_VIM") | "\(.vimName)\t\(.username)"'
```

**Expected result:** the vCenter VIM and its service account — vCenter
authenticates TCA's infrastructure operations for VNF placement.

**Negative test:** an expired vCenter credential blocks VNF instantiation;
the VIM credential is the auth path to infrastructure.

### Lab 20.33 — Create a role within TCA (Objective 8.2)

**Objective:** Read the TCA roles available for assignment.

```bash
curl -sk -H "$T" "$TCA/hybridity/api/rbac/roles" | jq -r '.[] | .name' 2>/dev/null | head
```

**Expected result:** roles (system and custom) — a role is a named set of
TCA privileges assigned to a user/group.

**Negative test:** granting individual privileges instead of a role is
unmanageable at scale; roles are the unit of RBAC.

### Lab 20.34 — Create a permission within TCA (Objective 8.3)

**Objective:** Read a permission (role bound to a principal and scope).

```bash
curl -sk -H "$T" "$TCA/hybridity/api/rbac/permissions" | jq -r '.[] | "\(.principal)\t\(.role)"' 2>/dev/null | head
```

**Expected result:** principal→role bindings — a permission grants a role to
a user/group over a scope.

**Negative test:** a role with no permission binding grants nothing; the
permission is what activates the role for a user.

### Lab 20.35 — Tag-based permission filtering (Objective 8.4)

**Objective:** Read a permission scoped by tag.

```bash
curl -sk -H "$T" "$TCA/hybridity/api/rbac/permissions" | jq -r '.[] | select(.tags) | "\(.principal)\ttags:\(.tags)"' 2>/dev/null | head
```

**Expected result:** permissions whose scope is a tag filter — a user sees
only resources carrying the matching tag.

**Negative test:** without a tag filter, a permission spans all resources;
tag filtering is what narrows visibility per tenant/site.

### Lab 20.36 — Steps after upgrading TCA (Objective 9.1)

**Objective:** Confirm post-upgrade component versions align.

```bash
curl -sk -H "$T" "$TCA/hybridity/api/nodes" | jq -r '.[] | "\(.role)\t\(.version)"'
```

**Expected result:** TCA-Manager and TCA-CP on matching, post-upgrade
versions — after upgrading Manager, each CP must be upgraded to match.

**Negative test:** a TCA-CP left on the old version after a Manager upgrade
causes orchestration errors; version alignment is a required post-step.

### Lab 20.37 — LCM events for a VNF (Objective 9.2)

**Objective:** Read the VNF's LCM operation set.

```bash
curl -sk -H "$T" "$TCA/telco/api/nslcm/v2/vnf_lcm_op_occs?vnfInstanceId=<id>" | jq -r '.[].operation' 2>/dev/null
```

**Expected result:** VNF LCM events (instantiate, scale, heal, terminate,
modify) — the VM-based function's managed lifecycle.

**Negative test:** a VNF update replaces/upgrades the VM image, distinct from
a CNF's Helm-based update — the mechanisms differ by type.

### Lab 20.38 — LCM events for a CNF (Objective 9.3)

**Objective:** Read the CNF's Helm-driven lifecycle.

```bash
helm history <cnf-release> -n <ns> 2>/dev/null
```

**Expected result:** the CNF's Helm revision history — CNF LCM events are
Helm install/upgrade/rollback operations on Kubernetes.

**Negative test:** power-cycling CNF pods is not an LCM event; the descriptor/
Helm-driven operations are.

### Lab 20.39 — LCM events for a network service (Objective 9.4)

**Objective:** Read the NS-level LCM operations.

```bash
curl -sk -H "$T" "$TCA/telco/api/nslcm/v2/ns_lcm_op_occs" | jq -r '.[] | "\(.operation)\t\(.operationState)"' 2>/dev/null | head
```

**Expected result:** NS LCM operations spanning its member NFs — an NS-level
scale or heal cascades to the functions it composes.

**Negative test:** healing one member NF is not the same as an NS-level
operation; NS LCM coordinates across members.

### Lab 20.40 — CNF update vs VNF update (Objective 9.5)

**Objective:** Contrast the two update mechanisms.

```bash
helm get metadata <cnf-release> -n <ns> 2>/dev/null | grep -i version
curl -sk -H "$T" "$TCA/telco/api/catalogs/networkfunction" | jq -r '.[] | "\(.name)\t\(.nfType)"' | head
```

**Expected result:** a CNF update = Helm chart upgrade (rolling pods); a VNF
update = new VM image/descriptor version — different rollback semantics.

**Negative test:** applying a VNF-style image swap to a CNF is meaningless;
each type's update path is distinct.

### Lab 20.41 — Healing a network function (Objective 9.6)

**Objective:** Read the healing capability configured on an instance.

```bash
curl -sk -H "$T" "$TCA/telco/api/nslcm/v2/vnf_instances" | jq -r '.[] | "\(.vnfInstanceName)\t\(.instantiationState)"' | head
```

**Expected result:** instances whose descriptor enables heal — TCA
re-instantiates a failed function to its descriptor's desired state.

**Negative test:** healing restores to the descriptor, not to a manually
drifted state; out-of-band changes are lost on heal.

### Lab 20.42 — Identify the log to view for a problem (Objective 10.4)

**Objective:** Locate the correct TCA log for a symptom.

```bash
curl -sk -H "$T" "$TCA/hybridity/api/admin/support/bundle" -X POST 2>/dev/null | jq -r '.id'
# then: TCA-Manager (app.log), TCA-CP (postboot/hybridity), K8s (kubectl logs)
```

**Expected result:** a support bundle whose logs map to the fault layer —
Manager logs for orchestration, TCA-CP for VIM operations, kubectl for CNF
pods.

**Negative test:** reading only the Manager log for a CNF pod crash misses
the Kubernetes logs where the real error is; match the log to the layer.

**Telco Cloud NFV (5V0-37.22) — Labs 20.43–20.73 (VMware Cloud Director for NFV)**

### Lab 20.43 — Key functions of Telco Cloud (Objective 1.1)

**Objective:** Read the Telco Cloud NFV stack's top-level function set.

```bash
curl -sk -H "Accept: application/*+json;version=38.0" -H "$VT" "$VCD/api/query?type=organization" | jq -r '.record[].name' 2>/dev/null | head
```

**Expected result:** the multi-tenant organizations Cloud Director serves —
Telco Cloud provides tenant isolation, self-service, and NFV workload
hosting.

**Negative test:** treating Telco Cloud as a single-tenant vSphere ignores
the multi-tenancy VCD adds — a core function.

### Lab 20.44 — Components of Telco Cloud Infrastructure (Objective 1.2)

**Objective:** Read the underlying vCenter/NSX the infrastructure is built
on.

```bash
curl -sk -H "$VT" "$VCD/api/admin/extension/vimServerReferences" -H "Accept: application/*+json;version=38.0" | jq -r '.vimServerReference[].name' 2>/dev/null
```

**Expected result:** the vCenter(s) and NSX Manager backing VCD — the
compute/network components of the Telco Cloud Infrastructure.

**Negative test:** VCD with no attached vCenter has no compute to allocate;
the VIM components are foundational.

### Lab 20.45 — Deployment options (Objective 1.3)

**Objective:** Read the VCD cell/appliance topology.

```bash
curl -sk -H "$VT" "$VCD/api/admin" -H "Accept: application/*+json;version=38.0" | jq -r '.otherAttributes // "cells"' 2>/dev/null
govc about 2>/dev/null | grep -i version
```

**Expected result:** the VCD cell(s) fronting the infrastructure — deployment
options range from a single appliance to a multi-cell HA cluster.

**Negative test:** a single VCD cell is not highly available; a telco
deployment uses multiple cells behind a load balancer.

### Lab 20.46 — VMware Cloud Director architecture components (Objective 1.4)

**Objective:** Read the provider VDCs that abstract vCenter resources.

```bash
curl -sk -H "$VT" "$VCD/api/query?type=providerVdc" -H "Accept: application/*+json;version=38.0" | jq -r '.record[].name' 2>/dev/null
```

**Expected result:** provider VDCs — VCD's architecture maps vCenter
clusters into provider VDCs, then carves org VDCs for tenants.

**Negative test:** exposing vCenter directly to tenants breaks multi-tenancy;
the provider/org VDC abstraction is the architecture.

### Lab 20.47 — Key VCD components (Objective 2.2)

**Objective:** Read the VCD database/cell and NSX integration.

```bash
curl -sk -H "$VT" "$VCD/api/query?type=edgeGateway" -H "Accept: application/*+json;version=38.0" | jq -r '.record[].name' 2>/dev/null | head
```

**Expected result:** edge gateways (NSX-backed) — key components include the
cells, the database, and the NSX edge/network services.

**Negative test:** VCD networking without NSX integration cannot provide
tenant edge services; NSX is a key component.

### Lab 20.48 — Physical and virtual infrastructure characteristics (Objective 3.1)

**Objective:** Read the physical hosts backing the virtual infrastructure.

```bash
govc host.info -json 2>/dev/null | jq -r '.hostSystems[]?.summary.hardware | "\(.model)\t\(.numCpuCores)core"' 2>/dev/null | head
```

**Expected result:** physical host models/cores under the virtual layer —
NFVI runs virtual functions on abstracted physical hardware.

**Negative test:** assuming unlimited virtual capacity ignores the physical
ceiling the virtual layer is bounded by.

### Lab 20.49 — NFVI advantages and components (Objective 3.2)

**Objective:** Read the NFVI compute/storage/network trio.

```bash
govc datastore.info 2>/dev/null | grep -iE 'Name|Type' | head -6
```

**Expected result:** NFVI storage (and by extension compute + network) — NFVI
pools these so VNFs run on shared, elastic infrastructure.

**Negative test:** dedicating hardware per VNF forfeits the consolidation and
elasticity NFVI's shared pool provides.

### Lab 20.50 — Network virtualization in NFVI (Objective 3.3)

**Objective:** Read the NSX overlay providing NFVI networking.

```bash
curl -sk -H "$VT" "$VCD/api/query?type=orgVdcNetwork" -H "Accept: application/*+json;version=38.0" | jq -r '.record[].name' 2>/dev/null | head
```

**Expected result:** org VDC networks (NSX overlay segments) — network
virtualization decouples VNF connectivity from physical topology.

**Negative test:** VLAN-only networking cannot scale to per-tenant isolation
across the NFVI; the overlay is what virtualizes it.

### Lab 20.51 — NFVI requirements on VMware Cloud Director (Objective 3.4)

**Objective:** Read the provider VDC resource guarantees NFVI needs.

```bash
curl -sk -H "$VT" "$VCD/api/query?type=providerVdc" -H "Accept: application/*+json;version=38.0" | jq -r '.record[] | "\(.name)\tcpu:\(.cpuAllocationMhz // "n/a")"' 2>/dev/null
```

**Expected result:** provider VDC CPU/memory backing — NFVI on VCD requires
guaranteed, policy-backed resources for deterministic VNF performance.

**Negative test:** over-committing a provider VDC beyond NFVI's guarantees
risks VNF performance SLAs.

### Lab 20.52 — Key networking use cases (Objective 3.5)

**Objective:** Read the edge/routed vs isolated network types.

```bash
curl -sk -H "$VT" "$VCD/api/query?type=orgVdcNetwork" -H "Accept: application/*+json;version=38.0" | jq -r '.record[] | "\(.name)\t\(.linkType // "?")"' 2>/dev/null | head
```

**Expected result:** routed (edge-connected), isolated, and imported network
types — the connectivity patterns VNFs use.

**Negative test:** placing a VNF that needs north-south routing on an isolated
network strands it; match the network type to the use case.

### Lab 20.53 — Storage options of VMware Cloud Director (Objective 3.6)

**Objective:** Read the storage policies exposed to tenants.

```bash
curl -sk -H "$VT" "$VCD/api/query?type=orgVdcStorageProfile" -H "Accept: application/*+json;version=38.0" | jq -r '.record[].name' 2>/dev/null | head
```

**Expected result:** storage profiles (vSAN/VMFS tiers) — VCD offers tiered
storage to tenants via policies.

**Negative test:** a single storage tier cannot meet mixed VNF latency needs;
policies expose the tiers.

### Lab 20.54 — Function of resource pools (Objective 4.2)

**Objective:** Read the resource pools backing org VDCs.

```bash
govc pool.info -json '*/Resources/*' 2>/dev/null | jq -r '.resourcePools[]?.name' 2>/dev/null | head
```

**Expected result:** resource pools with CPU/memory reservations — they carve
provider capacity into guaranteed slices for org VDCs.

**Negative test:** without resource pools, tenants contend uncontrolled;
pools enforce the allocation.

### Lab 20.55 — vSAN storage policy characteristics (Objective 4.3)

**Objective:** Read a vSAN storage policy's rules.

```bash
govc storage.policy.info 2>/dev/null | head -15
```

**Expected result:** policies with FTT/stripe/space-reservation rules — vSAN
policy defines per-object availability and performance.

**Negative test:** FTT=0 gives no redundancy; a VNF's storage policy must
match its availability requirement.

### Lab 20.56 — How compute resources are provided to VCD (Objective 4.4)

**Objective:** Read the provider VDC → org VDC compute mapping.

```bash
curl -sk -H "$VT" "$VCD/api/query?type=orgVdc" -H "Accept: application/*+json;version=38.0" | jq -r '.record[] | "\(.name)\tcpuUsed:\(.cpuUsedMhz // 0)"' 2>/dev/null | head
```

**Expected result:** org VDCs drawing CPU from a provider VDC — compute flows
provider VDC → org VDC per the allocation model.

**Negative test:** an org VDC cannot exceed its provider VDC's capacity; the
provider is the source.

### Lab 20.57 — How storage resources are provided to VCD (Objective 4.5)

**Objective:** Read org VDC storage allocation.

```bash
curl -sk -H "$VT" "$VCD/api/query?type=orgVdcStorageProfile" -H "Accept: application/*+json;version=38.0" | jq -r '.record[] | "\(.name)\tlimit:\(.storageLimitMB // 0)MB"' 2>/dev/null | head
```

**Expected result:** per-org-VDC storage-profile limits — storage is
provided as a capped policy allocation to each tenant.

**Negative test:** an unlimited tenant storage grant risks provider
exhaustion; the limit is the control.

### Lab 20.58 — VMware Cloud Director organizations (Objective 4.6)

**Objective:** Read the organizations (tenants).

```bash
curl -sk -H "$VT" "$VCD/api/query?type=organization" -H "Accept: application/*+json;version=38.0" | jq -r '.record[] | "\(.name)\t\(.isEnabled)"' 2>/dev/null | head
```

**Expected result:** enabled organizations — an org is the top-level
tenant boundary with its own users, catalogs, and VDCs.

**Negative test:** cross-org resource sharing is disallowed by default; the
org is the isolation boundary.

### Lab 20.59 — Organization VDC characteristics (Objective 4.7)

**Objective:** Read an org VDC's allocation and capacity.

```bash
curl -sk -H "$VT" "$VCD/api/query?type=orgVdc" -H "Accept: application/*+json;version=38.0" | jq -r '.record[] | "\(.name)\t\(.allocationModel)"' 2>/dev/null | head
```

**Expected result:** org VDCs with their allocation model — an org VDC is a
tenant's slice of provider compute/storage/network.

**Negative test:** deploying tenant workloads directly to a provider VDC
bypasses tenant accounting; workloads belong in org VDCs.

### Lab 20.60 — Organization VDC allocation models (Objective 4.8)

**Objective:** Distinguish the allocation models in use.

```bash
curl -sk -H "$VT" "$VCD/api/query?type=orgVdc" -H "Accept: application/*+json;version=38.0" | jq -r '.record[].allocationModel' 2>/dev/null | sort | uniq -c
```

**Expected result:** models (AllocationPool, PayAsYouGo/Allocation VApp,
ReservationPool, Flex) — each trades guarantee vs elasticity differently.

**Negative test:** PayAsYouGo gives no capacity guarantee; a VNF needing
reserved performance requires a reservation model.

### Lab 20.61 — Types of allocatable resources (Objective 4.9)

**Objective:** Read the CPU/memory/storage a VDC allocates.

```bash
curl -sk -H "$VT" "$VCD/api/query?type=orgVdc" -H "Accept: application/*+json;version=38.0" | jq -r '.record[0] | "cpu:\(.cpuLimitMhz)\tmem:\(.memoryLimitMB)\tstorage:profiles"' 2>/dev/null
```

**Expected result:** CPU, memory, and storage as the allocatable resource
types — plus network via edge/NSX.

**Negative test:** allocating CPU/memory without a storage profile leaves the
VDC unable to place disks; all types are needed.

### Lab 20.62 — Adding and modifying catalog elements (Objective 4.11)

**Objective:** Read a catalog's templates/media.

```bash
curl -sk -H "$VT" "$VCD/api/query?type=catalog" -H "Accept: application/*+json;version=38.0" | jq -r '.record[].name' 2>/dev/null | head
```

**Expected result:** catalogs of vApp templates and media — VNF images are
published to catalogs for tenant self-service instantiation.

**Negative test:** a catalog with no published template offers nothing to
deploy; elements must be added first.

### Lab 20.63 — Characteristics of vApps (Objective 4.12)

**Objective:** Read a vApp and its member VMs.

```bash
curl -sk -H "$VT" "$VCD/api/query?type=vApp" -H "Accept: application/*+json;version=38.0" | jq -r '.record[] | "\(.name)\t\(.numberOfVMs // 0)VMs"' 2>/dev/null | head
```

**Expected result:** vApps grouping VMs with shared networking/start-order —
a VNF often maps to a vApp of related VMs.

**Negative test:** managing member VMs independently loses the vApp's
start-order and network encapsulation.

### Lab 20.64 — Networking use cases in VCD (Objective 4.14)

**Objective:** Read the edge gateway services (NAT, firewall, VPN).

```bash
curl -sk -H "$VT" "$VCD/api/query?type=edgeGateway" -H "Accept: application/*+json;version=38.0" | jq -r '.record[].name' 2>/dev/null | head
```

**Expected result:** edge gateways delivering NAT/firewall/load-balancing/VPN
— the tenant networking use cases VCD supports via NSX edges.

**Negative test:** expecting L2 stretch without an NSX-backed network fails;
the use case dictates the network object.

### Lab 20.65 — NSX-T architecture in VCD (Objective 4.17)

**Objective:** Read the NSX-backed networks and their transport.

```bash
curl -sk -H "$VT" "$VCD/api/query?type=orgVdcNetwork" -H "Accept: application/*+json;version=38.0" | jq -r '.record[] | "\(.name)\t\(.linkType)"' 2>/dev/null | head
```

**Expected result:** overlay-backed org networks — VCD uses NSX-T Tier-0/
Tier-1 gateways and overlay segments for tenant networking.

**Negative test:** NSX-V constructs do not apply; current VCD networking is
NSX-T (now "NSX") architecture.

### Lab 20.66 — VCD supported features (Objective 4.18)

**Objective:** Read the API version to confirm supported feature set.

```bash
curl -sk "$VCD/api/versions" | jq -r '.versionInfo[].version' 2>/dev/null | tail -3
```

**Expected result:** supported API versions — the version gates which
features (data solutions, container service extension) are available.

**Negative test:** calling a feature from a newer API version than the cell
supports returns an error; features track the version.

### Lab 20.67 — Networking between VDCs (Objective 4.19)

**Objective:** Read data-center groups that span VDCs.

```bash
curl -sk -H "$VT" "$VCD/cloudapi/1.0.0/vdcGroups" | jq -r '.values[].name' 2>/dev/null | head
```

**Expected result:** VDC groups enabling shared networks across org VDCs —
the mechanism (and its complexity) for inter-VDC connectivity.

**Negative test:** routing between isolated org VDCs without a VDC group or
external network is not possible; connectivity must be explicit.

### Lab 20.68 — Key resources to manage (Objective 5.1)

**Objective:** Read the managed resource inventory.

```bash
for t in providerVdc orgVdc edgeGateway; do
  echo -n "$t: "; curl -sk -H "$VT" "$VCD/api/query?type=$t" -H "Accept: application/*+json;version=38.0" | jq -r '.total // (.record|length)' 2>/dev/null
done
```

**Expected result:** counts of provider VDCs, org VDCs, and edges — the key
resource classes an operator monitors.

**Negative test:** monitoring VMs alone misses provider-capacity and edge
health that gate every tenant.

### Lab 20.69 — vRealize Operations Manager features (Objective 5.2)

**Objective:** Read the vROps adapter monitoring the Telco Cloud.

```bash
curl -sk -H "vRealizeOpsToken $opsToken" -H 'Accept: application/json' \
  "https://vrops.lab/suite-api/api/adapters" | jq -r '.adapterInstancesInfoDto[].resourceKey.name' 2>/dev/null | head
```

**Expected result:** vROps adapters (vCenter, VCD, NSX) — vROps provides
capacity, performance, and health analytics across the NFV stack.

**Negative test:** without the VCD adapter, tenant-level metrics are missing;
the adapter set defines vROps' visibility.

### Lab 20.70 — Purpose of the vROps Tenant App (Objective 5.3)

**Objective:** Confirm the Tenant App that exposes per-tenant metrics.

```bash
curl -sk "https://vrops-tenant.lab/api/health" 2>/dev/null | head -1
```

**Expected result:** the Tenant App responding — it surfaces org-scoped
dashboards/metering so tenants see only their own resources.

**Negative test:** giving tenants the full vROps exposes other tenants' data;
the Tenant App enforces the org boundary.

### Lab 20.71 — Steps to monitor VCD with vROps (Objective 5.4)

**Objective:** Confirm the VCD management pack is collecting.

```bash
curl -sk -H "vRealizeOpsToken $opsToken" -H 'Accept: application/json' \
  "https://vrops.lab/suite-api/api/adapters" | jq -r '.adapterInstancesInfoDto[] | select(.resourceKey.adapterKindKey|test("VCD|CloudDirector")) | .collectorState' 2>/dev/null
```

**Expected result:** the VCD adapter in a collecting state — monitoring
requires installing the pack, adding the adapter, and validating collection.

**Negative test:** an adapter added but not collecting shows empty
dashboards; collection state must be verified.

### Lab 20.72 — Use of logs in VMware Cloud Director (Objective 6.3)

**Objective:** Locate the VCD cell logs for troubleshooting.

```bash
# on a VCD cell
ls -1 /opt/vmware/vcloud-director/logs/ 2>/dev/null | grep -iE 'vcloud|cell' | head
```

**Expected result:** cell logs (`vcloud-container-info.log`, debug) — the
authoritative record for VCD-side faults.

**Negative test:** reading vCenter logs for a VCD API error misses the cell
log where the actual failure is; match the log to the layer.

### Lab 20.73 — Characteristics of role-based access (Objective 7.1)

**Objective:** Read VCD roles and rights.

```bash
curl -sk -H "$VT" "$VCD/api/query?type=role" -H "Accept: application/*+json;version=38.0" | jq -r '.record[].name' 2>/dev/null | head
```

**Expected result:** provider and tenant roles (System Administrator,
Organization Administrator, vApp User) — RBAC scoped by org.

**Negative test:** a tenant role cannot perform provider operations; VCD RBAC
separates provider from tenant scope.

**Telco Cloud Platform (5V0-36.22) — Labs 20.74–20.98 (vSphere + Tanzu + TCA)**

### Lab 20.74 — TCP architecture (Objective 1.1)

**Objective:** Read the TCP stack layers (vSphere → Tanzu → TCA).

```bash
govc about 2>/dev/null | grep -i version
kubectl get nodes 2>/dev/null | head -3
```

**Expected result:** vSphere version and Kubernetes nodes — TCP layers CaaS
(Tanzu) on vSphere, orchestrated by TCA.

**Negative test:** treating TCP as just Kubernetes ignores the vSphere NFVI
and TCA orchestration layers it depends on.

### Lab 20.75 — TCA architecture (Objective 1.2)

**Objective:** Read the TCA Manager/CP roles (as in Lab 20.6).

```bash
curl -sk -H "$T" "$TCA/hybridity/api/nodes" | jq -r '.[] | "\(.role)\t\(.version)"'
```

**Expected result:** TCA-Manager and TCA-CP — the distributed orchestration
layer TCP is driven by.

**Negative test:** a TCP site with no TCA-CP cannot automate CaaS/infra; the
CP is required locally.

### Lab 20.76 — TCA deployment (Objective 1.3)

**Objective:** Read the VIMs TCA drives in the TCP deployment.

```bash
curl -sk -H "$T" "$TCA/hybridity/api/vims" | jq -r '.[] | "\(.vimName)\t\(.vimType)"'
```

**Expected result:** vCenter and Kubernetes VIMs — a TCP deployment registers
the vSphere VIM and the CaaS clusters TCA manages.

**Negative test:** a deployment missing the Kubernetes VIM cannot onboard
CNFs; both VIM types are needed for TCP.

### Lab 20.77 — vSphere architecture (Objective 1.4)

**Objective:** Read the vCenter/ESXi structure underneath TCP.

```bash
govc ls / 2>/dev/null
govc host.info 2>/dev/null | grep -iE 'Name|Cluster' | head
```

**Expected result:** datacenters/clusters/hosts — vSphere is the compute
foundation Tanzu and VNFs run on.

**Negative test:** assuming TCP abstracts vSphere entirely; vSphere
constructs (clusters, DRS) still govern placement.

### Lab 20.78 — Key vSphere components (Objective 2.1)

**Objective:** Read vCenter, ESXi, and the distributed switch.

```bash
govc dvs.portgroup.info 2>/dev/null | grep -i name | head
```

**Expected result:** the VDS port groups — vCenter (management), ESXi
(hypervisor), and the VDS (networking) are the key components.

**Negative test:** standard switches per host do not scale for TCP; the VDS
is the standard component.

### Lab 20.79 — vSphere networking options (Objective 2.2)

**Objective:** Read the network backings available to VNF VMs.

```bash
govc ls -t Network / 2>/dev/null | head
```

**Expected result:** port groups / NSX segments / SR-IOV networks — the
networking options a VNF attaches to.

**Negative test:** a latency-sensitive VNF on a standard port group misses
SR-IOV/DPDK acceleration; the option must match the requirement.

### Lab 20.80 — vSphere storage options (Objective 2.3)

**Objective:** Read the datastore types available.

```bash
govc datastore.info 2>/dev/null | grep -iE 'Name|Type' | head
```

**Expected result:** vSAN / VMFS / NFS datastores — the storage options for
VNF disks and CaaS persistent volumes.

**Negative test:** placing a stateful CNF's PV on non-redundant local storage
risks data loss; the storage option must meet durability needs.

### Lab 20.81 — Role of containers in TCP (Objective 2.4)

**Objective:** Read the running containerized network functions.

```bash
kubectl get pods -A 2>/dev/null | grep -ivE 'kube-system|capi' | head
```

**Expected result:** CNF pods — containers package modern network functions
for density and fast lifecycle vs VMs.

**Negative test:** running a CNF as a VM forfeits container density and
rolling-update speed; the container is the point.

### Lab 20.82 — Kubernetes architecture (Objective 2.5)

**Objective:** Read the control-plane and worker components.

```bash
kubectl get pods -n kube-system 2>/dev/null | grep -iE 'apiserver|etcd|scheduler|controller' | head
```

**Expected result:** api-server, etcd, scheduler, controller-manager — the
Kubernetes control plane that schedules CNFs.

**Negative test:** a failed etcd loses cluster state; the control-plane
components are the architecture's core.

### Lab 20.83 — Role of nodes and clusters (Objective 2.6)

**Objective:** Read nodes and their roles.

```bash
kubectl get nodes -o custom-columns=NAME:.metadata.name,ROLE:.metadata.labels.node-role\\.kubernetes\\.io/control-plane 2>/dev/null
```

**Expected result:** control-plane and worker nodes forming a cluster — nodes
provide capacity, the cluster provides scheduling/HA.

**Negative test:** scheduling CNFs onto control-plane nodes is discouraged;
workers carry the workload.

### Lab 20.84 — Supporting components of Kubernetes (Objective 2.7)

**Objective:** Read the CNI, CSI, and DNS add-ons.

```bash
kubectl get pods -A 2>/dev/null | grep -iE 'antrea|calico|csi|coredns' | head
```

**Expected result:** CNI (network), CSI (storage), CoreDNS — the supporting
components that make a cluster usable for CNFs.

**Negative test:** a cluster with no CNI leaves pods `NotReady`; the add-ons
are prerequisites, not optional.

### Lab 20.85 — Tanzu Kubernetes architecture (Objective 2.8)

**Objective:** Read the Cluster API objects behind a TKG cluster.

```bash
kubectl get clusters,machinedeployments -A 2>/dev/null | head
```

**Expected result:** Cluster/MachineDeployment objects — TKG uses Cluster API
for declarative, lifecycle-managed clusters.

**Negative test:** editing nodes outside Cluster API drifts from the declared
state; TKG reconciles to the spec.

### Lab 20.86 — Types of network functions (Objective 2.9)

**Objective:** Classify onboarded functions (VNF/CNF) as in Lab 20.24.

```bash
curl -sk -H "$T" "$TCA/telco/api/catalogs/networkfunction" | jq -r '.[] | "\(.name)\t\(.nfType // .type)"' | head
```

**Expected result:** VNF (VM) and CNF (container) types — TCP hosts both,
each with its own infrastructure requirements.

**Negative test:** onboarding a CNF against a VM-only VIM fails; the type
dictates the target VIM.

### Lab 20.87 — Key vSphere operations for VNFs (Objective 2.11)

**Objective:** Read VNF VM power/placement state.

```bash
govc vm.info -json 2>/dev/null | jq -r '.virtualMachines[]? | "\(.name)\t\(.runtime.powerState)"' 2>/dev/null | head
```

**Expected result:** VNF VMs with power state — vSphere operations (power,
vMotion, snapshot) apply to VNF VMs.

**Negative test:** vMotioning a VNF with SR-IOV/passthrough is restricted;
some vSphere operations are constrained by VNF device use.

### Lab 20.88 — Special requirements of containers for NFs (Objective 2.12)

**Objective:** Read pod resource/hugepage/SR-IOV requests on a CNF.

```bash
kubectl get pods -A -o json 2>/dev/null | jq -r '.items[] | select(.spec.containers[].resources.limits | has("hugepages-1Gi") or has("intel.com/sriov")) | .metadata.name' 2>/dev/null | head
```

**Expected result:** CNF pods requesting hugepages / SR-IOV VFs — telco CNFs
need special resources for data-plane performance.

**Negative test:** a data-plane CNF on a node without SR-IOV/hugepages runs
slowly or fails to schedule; the requirements are hard.

### Lab 20.89 — Type of descriptors for containers (Objective 2.13)

**Objective:** Read the Helm chart / CSAR descriptor of a CNF.

```bash
helm show chart <cnf-chart> 2>/dev/null | grep -iE 'name|version'
```

**Expected result:** the Helm chart metadata (the CNF descriptor) — CNFs use
Helm charts packaged in a CSAR for onboarding.

**Negative test:** a CNF onboarded with a VNFD (VM descriptor) instead of a
Helm-based CSAR is invalid; the descriptor type must match the function type.

### Lab 20.90 — Role of Harbor (Objective 2.14)

**Objective:** Confirm Harbor as the image/chart registry (as in Lab 20.20).

```bash
curl -sk "$HARBOR/api/v2.0/health" | jq -r '.status'
```

**Expected result:** Harbor `healthy` — it stores the container images and
Helm charts CNFs are pulled from, including for air-gapped sites.

**Negative test:** a CNF whose images reference an external registry cannot
deploy air-gapped; Harbor holds the local copies.

### Lab 20.91 — Requirements for infrastructure (Objective 4.1)

**Objective:** Read host capacity against CaaS node requirements.

```bash
govc host.info -json 2>/dev/null | jq -r '.hostSystems[]?.summary.hardware | "\(.numCpuCores)core\t\(.memorySize/1073741824|floor)GB"' 2>/dev/null | head
```

**Expected result:** host cores/RAM — infrastructure must meet the CaaS
node-pool and VNF flavor requirements before onboarding.

**Negative test:** undersized hosts cannot place a large node pool; the infra
requirement gates deployment.

### Lab 20.92 — Process of deploying VMs (Objective 4.2)

**Objective:** Read a deployed VNF VM and its template origin.

```bash
govc vm.info -json 2>/dev/null | jq -r '.virtualMachines[]? | "\(.name)\t\(.config.guestFullName)"' 2>/dev/null | head
```

**Expected result:** VNF VMs cloned from an OVF/template — VM deploy clones
from the catalog template, then customizes.

**Negative test:** building a VNF VM by hand skips the descriptor-driven
customization TCA applies; use the onboarding flow.

### Lab 20.93 — VM onboarding requirements (Objective 4.3)

**Objective:** Read the infra requirements block of a VNF descriptor.

```bash
curl -sk -H "$T" "$TCA/telco/api/catalogs/networkfunction" | jq -r '.[0].infraRequirements' 2>/dev/null | head
```

**Expected result:** the VNF's required flavor, networks, and node
components — onboarding validates these against the target VIM.

**Negative test:** onboarding a VNF whose required network is absent fails;
the requirements must be satisfiable at the VIM.

### Lab 20.94 — CNF onboarding requirements (Objective 4.4)

**Objective:** Read the CNF's Kubernetes/Helm prerequisites.

```bash
helm show values <cnf-chart> 2>/dev/null | grep -iE 'sriov|hugepage|nodeSelector|storageClass' | head
```

**Expected result:** the chart's required node selectors, SR-IOV, and storage
class — a CNF onboards only where these prerequisites exist.

**Negative test:** installing the chart on a cluster missing the required
storage class leaves PVCs pending; prerequisites must be met.

### Lab 20.95 — Late-binding concepts (Objective 5.1)

**Objective:** Read where inputs are bound at instantiation (as in Lab
20.29).

```bash
curl -sk -H "$T" "$TCA/telco/api/catalogs/networkfunction" | jq -r '.[0].infraRequirements.nodeComponents // "late-bound"' 2>/dev/null | head
```

**Expected result:** infra values resolved at deploy time — late binding lets
one descriptor deploy across many sites with site-specific inputs.

**Negative test:** hard-coding site values in the descriptor breaks reuse;
late binding is what makes it portable.

### Lab 20.96 — Use of logs in TCP (Objective 6.4)

**Objective:** Locate the log for a TCP-layer fault.

```bash
kubectl logs -n <ns> <cnf-pod> --tail=20 2>/dev/null
curl -sk -H "$T" "$TCA/hybridity/api/admin/support/bundle" -X POST 2>/dev/null | jq -r '.id'
```

**Expected result:** CNF pod logs (Kubernetes layer) and a TCA support bundle
(orchestration layer) — match the log to the failing layer.

**Negative test:** reading vSphere logs for a CNF crash misses the pod log
where the container error is; layer matters.

### Lab 20.97 — CLI tools for troubleshooting (Objective 6.5)

**Objective:** Confirm the TCP troubleshooting CLI set.

```bash
kubectl version --short 2>/dev/null; helm version --short 2>/dev/null; govc about 2>/dev/null | grep -i version
```

**Expected result:** `kubectl` (Kubernetes), `helm` (CNF), and `govc`
(vSphere) responding — the CLI tools spanning TCP's layers.

**Negative test:** using only `kubectl` cannot diagnose a vSphere placement
fault; each tool addresses its own layer.

### Lab 20.98 — VNF life cycle management (Objective 7.1)

**Objective:** Read the VNF's LCM operation occurrences (as in Lab 20.37).

```bash
curl -sk -H "$T" "$TCA/telco/api/nslcm/v2/vnf_lcm_op_occs" | jq -r '.[] | "\(.operation)\t\(.operationState)"' 2>/dev/null | head
```

**Expected result:** the VNF's instantiate/scale/heal/terminate history —
LCM is the descriptor-driven lifecycle TCA enforces on the VNF.

**Negative test:** a manual VM edit is outside LCM and is lost on the next
heal/update; LCM is the managed path.

### Lab 20.99 — Program currency check (integrative)

**Objective:** Run one complete currency check against Broadcom's primary
sources for a subset of this volume's exams, producing a drift log — the
maintenance skill this chapter teaches, exercised for real.

**Prerequisites**

- Web access to Broadcom's certification pages.
- The four-step check and the drift-log format from the Implementation
  section.
- This volume's current exam codes (Chapters 12–20) to check against.

**Steps**

1. **Re-list (target 15 minutes).** From Broadcom's certification landing
   pages, list the current VMware credential tiers and tracks. Compare
   against this volume's coverage (VCP, VCAP, Distinguished Expert, Avi,
   PCS, Telco Cloud).

   **Expected result:** a current tier/track list, with any credential this
   volume omits or names differently noted.

2. **Re-confirm codes (target 20 minutes).** For at least five exams across
   different families (one each of `2V0`, `6V0`, `3V0`, `5V0`, plus one
   more), open each exam's own Broadcom page and confirm the code matches
   this volume.

   **Expected result:** each code confirmed, or a mismatch recorded — do
   not accept a code from anything but the exam's own page.

3. **Flag changes (target 10 minutes).** Note any exam whose page does not
   resolve or shows a new code or generation, and any published retirement
   or end date.

   **Expected result:** a list of findings, empty or not, each traceable to
   a primary source.

4. **Log (target 10 minutes).** Record every finding in the drift-log
   format, with date, what it was, what it is now, and the action needed in
   this volume, the appendix, and the blueprint.

   **Expected result:** an auditable drift log a future checker can build
   on.

5. **Verify the loop closes.** For one finding (or, if none, one code you
   confirmed unchanged), confirm this volume, the appendix, and
   CERTIFICATION_BLUEPRINTS.md all agree. A disagreement is itself a
   finding.

   **Expected result:** the three sources are consistent, or the
   inconsistency is logged.

6. **Cleanup:** file the drift log with the repository; there is no
   infrastructure to tear down.

## Lab Verification

Complete this sign-off once a currency check has been run end to end and a
drift log produced. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

VMware Telco Cloud is the service-provider specialization the rest of this
volume does not cover: three `5V0` specialist skills exams — Platform
(5V0-36.22), NFV (5V0-37.22), and Automation (5V0-44.21) — on an older
generation, relevant to NFV and virtualized-core work and off the path for
general enterprise administration. Their age makes them the canary for the
program's churn, which is why this chapter pairs them with a four-step
currency check: re-list the tiers, re-confirm every code against its own
Broadcom page, flag retirements and new generations, and propagate every
change through this volume, the Master Appendices course catalog, and the
repository blueprint. The program has changed enough since the Broadcom
acquisition that this check is maintenance, not optional — and its cardinal
rule is primary sources only.

- [ ] Can name the three Telco Cloud exams and who should take them.
- [ ] Can distinguish the `2V0`/`6V0`/`3V0`/`5V0` code families by tier and
      scope.
- [ ] Can justify a recurring currency check from the program's own churn.
- [ ] Can run the four-step check against Broadcom's primary sources.
- [ ] Understands why third-party summaries are never acceptable sources.
- [ ] Has produced a drift log and confirmed the volume, appendix, and
      blueprint agree.
- [ ] Completed the hands-on currency-check lab.
