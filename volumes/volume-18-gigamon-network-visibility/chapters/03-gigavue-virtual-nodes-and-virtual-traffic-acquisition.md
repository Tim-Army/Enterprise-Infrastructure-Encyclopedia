# Chapter 03: GigaVUE Virtual Nodes and Virtual Traffic Acquisition

## Learning Objectives

- Explain why physical TAPs and SPAN ports cannot solve east-west
  visibility inside hypervisors, container platforms, and public cloud
  VPCs, and how GigaVUE virtual nodes address that gap.
- Describe the role of the GigaVUE V Series virtual node and how it
  compares functionally to a physical HC/TA Series node.
- Differentiate the cloud-native acquisition mechanisms available across
  VMware, AWS, Azure, and Kubernetes, including the GigaVUE Universal
  Cloud Tap (UCT) and cloud-provider traffic mirroring.
- Explain tunneled traffic delivery (VXLAN/L2GRE) from a virtual tap to a
  V Series node, and why cloud visibility depends on tunneling rather than
  physical cabling.
- Deploy a minimal virtual visibility pipeline in a lab hypervisor
  environment and validate east-west traffic capture.

## Theory and Architecture

### Why physical acquisition breaks down in virtualized and cloud environments

Chapters 01 and 02 assumed a physical link an operator can TAP or mirror.
That assumption fails as soon as two workloads that need to be observed
communicate without ever leaving a hypervisor host — a virtual switch
inside an ESXi host, or a container network namespace inside a Kubernetes
node, routes that traffic entirely in software, and it never crosses a
physical port a TAP could intercept. The same problem exists, in a
different form, in public cloud: an organization does not own or have
physical access to the switching fabric underneath an AWS VPC or an Azure
virtual network, so a physical TAP is not merely inconvenient — it is not
an option at all.

Gigamon addresses this with **virtual and cloud-native acquisition**:
lightweight software components that run inside the hypervisor, container
host, or cloud instance being observed, capture a copy of the traffic
locally, and tunnel that copy to a **GigaVUE V Series** virtual node for
Flow Mapping and GigaSMART processing — the same logical functions a
physical HC Series node performs, running as software instead of on
dedicated ASICs.

### GigaVUE V Series virtual nodes

The GigaVUE V Series node is the virtual-machine (or container)
equivalent of a physical GigaVUE node: it terminates tunneled traffic from
virtual taps, applies Flow Mapping rules, and can run GigaSMART-equivalent
processing applications before forwarding selected traffic onward — either
to tools running in the same virtual/cloud environment or, tunneled again,
back to the physical fabric for centralized processing and delivery. V
Series nodes are deployed as VM images (for VMware, KVM/OpenStack) or
cloud-native instances (AWS, Azure, GCP), and are managed by GigaVUE-FM
alongside physical nodes as a single fabric — an operator authoring a Flow
Map in GigaVUE-FM does not need to reason about whether a given tool port
is physical or virtual; the fabric abstraction ([Chapter 04](04-gigavue-fm-installation-onboarding-security-and-governance.md)) is deliberately
uniform.

### Acquisition mechanisms by environment

| Environment | Primary acquisition mechanism | Notes |
| --- | --- | --- |
| VMware vSphere / ESXi | G-vTAP agent (per-VM virtual tap) or hypervisor-level tapping feeding a V Series node | Captures inter-VM (east-west) traffic on the same host, invisible to any physical TAP |
| KVM / OpenStack | G-vTAP agent equivalent, tunneling to a V Series node | Same east-west visibility goal as VMware, in an OpenStack-managed private cloud |
| AWS | VPC Traffic Mirroring (native AWS feature Gigamon integrates with) or GigaVUE Universal Cloud Tap (UCT), an agentless/lightweight tap that pre-filters at the source | UCT reduces tunneled volume by filtering before traffic leaves the instance, lowering both network egress cost and V Series processing load |
| Azure | Equivalent virtual tap/agent model, tunneling to V Series nodes deployed in the same virtual network | Supports orchestrated deployment via Terraform/Ansible ([Chapter 08](08-hybrid-cloud-visibility-automation-apis-and-integrations.md)) |
| Kubernetes | Container-aware tapping integrated with the GigaVUE Cloud Suite for Kubernetes, capturing pod-to-pod traffic that never traverses a node's physical NIC | Necessary because two pods on the same worker node may communicate entirely within that node's network namespace |

Across every environment, the pattern is consistent: a lightweight
capture component runs as close to the workload as possible, optionally
pre-filters, and **tunnels** the captured traffic — typically over VXLAN
or L2GRE — to a V Series node, which is the first point in the pipeline
capable of full Flow Mapping and GigaSMART-equivalent processing.

### Why tunneling, not cabling

A physical GigaVUE node receives traffic on a directly cabled network
port. A virtual tap has no equivalent physical medium — the "cable" is a
software-defined tunnel across the underlying IP network connecting the
source host (or cloud instance) to the V Series node's tunnel endpoint.
This has real design consequences: tunnel endpoint IP reachability, MTU
(a VXLAN or L2GRE tunnel adds encapsulation overhead that can trigger
fragmentation if the path MTU is not accounted for), and the additional
compute/network cost of encapsulation must all be engineered explicitly,
where a physical TAP simply required a cable run. Pre-filtering with a
tool such as UCT exists specifically to reduce this tunneled volume —
sending only traffic relevant to a subscribed tool, rather than a full
unfiltered copy of every instance's traffic, materially reduces both cloud
egress cost and V Series processing load at scale.

### Uniform fabric, mixed acquisition

The practical outcome for an enterprise running hybrid infrastructure is a
single logical visibility fabric spanning physical data center nodes and
virtual/cloud nodes, all authored from GigaVUE-FM with the same Flow
Mapping concepts introduced in [Chapter 01](01-visibility-architecture-traffic-acquisition-and-tool-delivery.md) and detailed in [Chapter 05](05-ports-flow-mapping-traffic-policy-and-tool-delivery.md). A
security tool consuming NDR telemetry, for example, can receive a
correlated feed built from both a physical data center TAP and a
Kubernetes cluster's pod-to-pod traffic, without the tool itself needing
to understand where each packet originated.

## Design Considerations

- **Decide acquisition scope by blast radius, not convenience.** Tapping
  every VM or every pod indiscriminately generates enormous tunneled
  volume; prioritize workloads handling regulated data, internet-facing
  services, and lateral-movement-sensitive segments (for example,
  identity infrastructure) for east-west visibility first.
- **Budget tunnel overhead and cloud egress cost explicitly.** Unlike a
  physical TAP, every byte a virtual tap captures in a public cloud
  environment can carry a direct network-egress cost if tunneled across
  availability zones or regions to a centralized V Series node. Placing V
  Series nodes per-VPC or per-region, and pre-filtering with UCT before
  tunneling, both reduce this cost meaningfully at scale.
- **Right-size V Series node count and placement to elasticity.** Cloud
  and container workloads scale horizontally on demand; a fixed number of
  V Series nodes sized for average load will bottleneck during a scale-out
  event. Plan for auto-scaling V Series capacity ([Chapter 08](08-hybrid-cloud-visibility-automation-apis-and-integrations.md) covers
  automation) rather than static sizing, especially for environments with
  significant traffic burstiness.
- **Understand what east-west visibility does not replace.** Virtual and
  cloud acquisition adds visibility Chapters 01–02 cannot provide; it does
  not replace physical acquisition for on-premises data center and campus
  segments still built on physical switching. Most mature deployments run
  both concurrently, unified under one fabric.
- **Plan for multi-tenancy in shared virtual/cloud environments.** Where a
  V Series node processes traffic on behalf of multiple business units or
  customers (as in a service-provider or large enterprise multi-tenant
  cloud account structure), Flow Mapping and delivery policy must enforce
  the same tenant isolation the underlying cloud accounts or VPCs already
  provide — a misconfigured map that crosses tenant boundaries is a data
  exposure event, not merely an operational error.

## Implementation and Automation

### Deploying a V Series node (VMware lab pattern)

1. Import the GigaVUE V Series OVA image into the target vSphere
   environment (or the equivalent VM image for the target hypervisor).
2. Assign the V Series VM at least two virtual network interfaces: one for
   management (reachable by GigaVUE-FM) and one for the tunnel endpoint
   that receives virtual-tap traffic.
3. Power on the VM and complete first-boot configuration — management IP
   addressing and the GigaVUE-FM registration address — either through a
   console-based setup prompt or a bootstrap configuration file, depending
   on the deployment automation used ([Chapter 08](08-hybrid-cloud-visibility-automation-apis-and-integrations.md) covers orchestrated
   deployment via Terraform/Ansible).
4. From GigaVUE-FM, confirm the V Series node registers and appears
   alongside physical nodes in the fabric inventory.

### Configuring a virtual tap source (G-vTAP agent pattern)

```yaml
# g-vtap-agent-config.yaml (representative; exact keys vary by release)
agent:
  monitored_interfaces:
    - eth0
  tunnel:
    type: vxlan
    destination: 10.60.5.20   # V Series node tunnel endpoint
    vni: 5001
  filters:
    - description: "exclude east-west health checks"
      action: drop
      match: "udp port 4789"   # avoid recursively tunneling tunnel traffic
```

> Exact agent configuration keys and deployment mechanisms (manifest,
> orchestration template, or GigaVUE-FM-driven push) vary by GigaVUE-FM
> release and target platform; treat this as illustrative of the
> tunnel-endpoint and filtering concepts rather than literal syntax for
> every release.

### Registering a V Series tunnel endpoint and a minimal map in GigaVUE-FM

Once virtual taps are tunneling traffic to a V Series node's tunnel
endpoint, the same Flow Mapping model from [Chapter 02](02-gigavue-appliance-first-deployment-and-fabric-foundations.md) applies: the tunnel
endpoint is treated as a network-port-equivalent source, and a map defines
what traffic (all of it, for a first-touch validation, or filtered per
[Chapter 05](05-ports-flow-mapping-traffic-policy-and-tool-delivery.md)) is forwarded to a tool-port-equivalent destination — either a
tool reachable from the virtual/cloud environment directly, or a tunnel
back toward the physical fabric for centralized delivery.

### AWS UCT pattern (conceptual)

1. Deploy a V Series node (or node group, for elastic scaling) into the
   target VPC or a dedicated visibility VPC reachable from the monitored
   VPCs.
2. Deploy the Universal Cloud Tap agent (or configure native VPC Traffic
   Mirroring sessions, depending on the integration model chosen) on the
   EC2 instances or through the auto-scaling launch template for the
   monitored workloads.
3. Configure a pre-filter at the UCT agent to exclude high-volume,
   low-value traffic (for example, health-check and metrics scrape
   traffic) before tunneling, reducing both egress cost and downstream
   processing load.
4. Register the resulting tunnel source in GigaVUE-FM and author Flow
   Mapping exactly as with any other acquisition source.

## Validation and Troubleshooting

- **V Series node does not register with GigaVUE-FM.** Confirm the
  management interface has outbound reachability to the GigaVUE-FM
  registration address and that any firewall/security-group rules permit
  the registration and heartbeat traffic; this is the most common
  first-deployment failure and is a network-reachability problem, not a
  Flow Mapping problem.
- **Tunnel endpoint receives no traffic despite a healthy virtual tap
  agent.** Confirm the agent's tunnel destination IP and VNI/tunnel-ID
  match the V Series node's configured listener exactly, and confirm no
  security group, NSG, or hypervisor firewall rule blocks the
  encapsulation protocol (UDP for VXLAN) between the source host and the
  V Series node.
- **Fragmented or dropped tunneled packets under load.** Check for an
  MTU mismatch — the VXLAN/L2GRE encapsulation overhead (typically 50+
  bytes) can push an already-near-MTU packet over the path's supported
  size; either raise the path MTU where possible or enable/verify
  fragmentation handling on the tunnel.
- **Unexpectedly high cloud egress cost after enabling virtual
  acquisition.** Audit whether pre-filtering (UCT filters, or agent-level
  filters) is actually excluding low-value high-volume traffic as
  designed; a tap deployed with a permissive "capture everything" filter
  is the most common cause of cost surprises in public cloud.
- **Traffic visible from some pods but not others in Kubernetes.**
  Confirm the container-aware tap component is deployed (as a DaemonSet or
  equivalent) on every worker node hosting monitored pods — a tap
  deployed to a subset of nodes will only see traffic for pods scheduled
  there, which can look like a Flow Mapping gap but is actually a
  deployment-coverage gap.

## Security and Best Practices

- Scope virtual tap agent permissions to the minimum required to read
  interface traffic; do not grant broader host or cloud-account
  permissions than the tapping function requires, consistent with
  least-privilege principles applied everywhere else in this encyclopedia.
- Encrypt or otherwise protect tunnel traffic that crosses a network
  boundary the organization does not fully trust (for example, tunneling
  between cloud regions over the public internet rather than a private
  backbone); tunneled visibility traffic is itself sensitive and should
  not be assumed safe merely because it is encapsulated.
- Enforce tenant and account isolation in Flow Mapping for any
  multi-tenant virtual/cloud deployment, and periodically audit maps
  against the intended tenant boundary rather than assuming initial
  configuration remains correct as the fabric grows.
- Apply the same credential and management-plane hardening to V Series
  nodes as to physical nodes ([Chapter 02](02-gigavue-appliance-first-deployment-and-fabric-foundations.md)) — a virtual node is a full
  fabric participant and an equally valuable target if compromised.
- Track cloud-provider API and IAM permissions granted to Gigamon
  orchestration components ([Chapter 08](08-hybrid-cloud-visibility-automation-apis-and-integrations.md)) under the same change-controlled
  process used for any other automation identity with write access to
  cloud infrastructure.

## References and Knowledge Checks

**References**

- [Gigamon, *GigaVUE V Series* product page](https://www.gigamon.com/products/access-traffic/virtual-nodes/gigavue-v-series.html) — virtual node architecture and
  supported platforms.
- [Gigamon, *GigaVUE Cloud Suite* product page](https://www.gigamon.com/products/access-traffic/cloud-suite.html) — AWS, Azure, GCP,
  OpenStack, VMware, and Kubernetes acquisition models.
- [Gigamon, *GigaVUE Cloud Suite for Kubernetes Data Sheet*](https://www.gigamon.com/content/dam/resource-library/english/data-sheet/ds-gigavue-cloud-suite-for-kubernetes.pdf) — container-aware
  tapping architecture.
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — this volume's
  GigaVUE-FM 6.x baseline, which governs supported V Series and cloud
  integration versions.

**Knowledge checks**

1. Why can a physical TAP never provide visibility into traffic between
   two VMs on the same hypervisor host?
2. What role does tunneling (VXLAN/L2GRE) play in virtual and cloud
   acquisition, and what two engineering concerns does it introduce that
   physical cabling does not?
3. How does pre-filtering at the source (for example, with the Universal
   Cloud Tap) reduce both cost and processing load in a public cloud
   deployment?
4. Why must Kubernetes tapping be deployed to every worker node hosting
   monitored pods, rather than a subset?

## Hands-On Lab

**Objective:** Deploy a minimal virtual visibility pipeline in a lab
hypervisor environment — a virtual tap source feeding a V Series node —
and validate east-west traffic between two lab VMs is captured, including
a negative test demonstrating a coverage gap.

**Prerequisites**

- A lab hypervisor environment (VMware Workstation/ESXi, or an equivalent
  virtualization platform) capable of running at least three VMs: two
  workload VMs that will communicate with each other, and one for the
  V Series node (or a lab-equivalent virtual visibility node image).
- Administrative access to deploy and configure VM network interfaces.
- A packet capture tool available on, or reachable from, the V Series
  node's tool-facing output for validation.
- Isolated lab network segment — do not perform this lab against a
  production hypervisor.

**Steps**

1. Deploy the V Series (or lab-equivalent) node VM with a management
   interface and a tunnel-endpoint interface, and note its tunnel-endpoint
   IP address.
2. Deploy two workload VMs on the same virtual switch/host, and confirm
   they can reach each other directly (for example, with `ping`) —
   this traffic is the east-west traffic a physical TAP could never see.
3. Install and configure a virtual tap agent (or equivalent capture
   component available in your lab platform) on the first workload VM,
   configured to tunnel captured traffic to the V Series node's
   tunnel-endpoint IP.
4. On the V Series node, configure a minimal all-pass Flow Map from the
   tunnel-endpoint source to a designated output (a local capture tool, or
   a tool-facing interface), following the mapping pattern from Chapter
   02.
5. From the second workload VM, generate traffic toward the first
   workload VM (for example, an HTTP request or a sustained `ping`).
6. Observe the capture tool connected to the V Series node's output.
   **Expected result:** the capture shows the inter-VM traffic, confirming
   the virtual tap successfully captured east-west traffic invisible to
   any physical acquisition point and delivered it through the tunnel to
   the V Series node.
7. **Negative test:** stop or disable the virtual tap agent on the first
   workload VM (leaving the map and V Series node otherwise unchanged),
   generate the same inter-VM traffic again, and observe the capture
   tool.
   **Expected result:** no new traffic appears at the capture tool,
   confirming that acquisition coverage — not the map or the V Series
   node — was the point of failure, and reproducing the
   partial-coverage failure mode described in Validation and
   Troubleshooting (analogous to a Kubernetes DaemonSet not covering
   every node).
8. Re-enable the virtual tap agent and confirm traffic resumes at the
   capture tool.
9. **Cleanup:** remove the lab Flow Map and virtual tap agent
   configuration if the environment will be reused, and power off or
   discard the lab VMs if they are disposable.

## Summary and Completion Checklist

Physical TAPs and SPAN ports cannot see traffic that never crosses a
physical wire — inter-VM, inter-pod, and cloud-VPC-internal traffic all
require virtual and cloud-native acquisition instead. The GigaVUE V Series
virtual node performs the same Flow Mapping and processing role as a
physical HC Series node, receiving traffic tunneled from lightweight
virtual tap agents or cloud-native mechanisms such as the Universal Cloud
Tap. The result, when combined with the physical acquisition covered in
Chapters 01–02, is one unified visibility fabric spanning data center,
private cloud, and public cloud, all authored from a common Flow Mapping
model.

- [ ] Can explain why physical TAPs cannot provide east-west visibility in
      virtualized and cloud environments.
- [ ] Can describe the GigaVUE V Series node's role relative to a physical
      HC Series node.
- [ ] Can name the acquisition mechanism appropriate to VMware, AWS,
      Azure, and Kubernetes environments.
- [ ] Can explain why tunneling introduces MTU and cost considerations
      that physical cabling does not.
- [ ] Completed the hands-on lab, including the negative test and
      cleanup.
