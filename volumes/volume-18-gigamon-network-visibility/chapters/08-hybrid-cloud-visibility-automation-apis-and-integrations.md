# Chapter 08: Hybrid Cloud Visibility, Automation, APIs, and Integrations

![Lab flow for this chapter: a service account scoped to read-only access authenticates to the GigaVUE-FM API and successfully queries node inventory and health status. As a negative test, the same read-only token attempts a write operation, creating a new Flow Map; the API rejects the call with an authorization error, confirming the scoped role enforces least privilege at the API layer itself, not merely in the web UI. A second, write-scoped service account performs the identical call successfully, and the new map is visible both via the API and in the web UI, correctly attributed in the audit log.](../../../diagrams/volume-18-gigamon-network-visibility/chapter-08-gigavue-fm-api-scope-flow.svg)

*Figure 8-1. Flow used throughout this chapter's Hands-On Lab: GigaVUE-FM REST API access scoped by service-account role, tested against a write attempt using a read-only token.*

## Learning Objectives

- Explain why a hybrid enterprise fabric — spanning data center, private
  cloud, and multiple public clouds — depends on automation rather than
  manual, per-node configuration.
- Describe GigaVUE-FM's REST API as the automation foundation underlying
  Terraform, Ansible, and custom orchestration integrations.
- Design an automated deployment pattern for elastic GigaVUE V Series
  capacity that scales with monitored cloud workloads.
- Integrate GigaVUE-FM with a SIEM and a ticketing/ITSM platform for
  fabric health events and audit visibility.
- Apply infrastructure-as-code practices (from [Volume I](../../volume-01-enterprise-engineering-foundations/README.md) and [Volume IX](../../volume-09-infrastructure-automation/README.md)) to
  Flow Mapping and fabric configuration, including drift detection.

## Theory and Architecture

### Why hybrid visibility cannot stay manual

Chapters 02–04 established fabric fundamentals using CLI and GigaVUE-FM's
web UI directly — a reasonable approach for initial bring-up and for a
fabric of modest, stable size. A hybrid enterprise fabric spanning
physical data center nodes, private cloud V Series nodes ([Chapter 03](03-gigavue-virtual-nodes-and-virtual-traffic-acquisition.md)),
and elastic public cloud capacity behaves differently: cloud workloads
scale up and down on demand, new VPCs and accounts appear as the
organization's cloud footprint grows, and the acquisition and Flow
Mapping configuration needed to maintain consistent visibility must keep
pace with that change automatically. Manual, UI-driven configuration that
works for a fixed set of forty physical ports does not scale to an
environment where the "right" number of V Series nodes changes hour to
hour with workload demand.

This is the same lesson [Volume I](../../volume-01-enterprise-engineering-foundations/README.md) (repository architecture, automation
architecture) and [Volume IX](../../volume-09-infrastructure-automation/README.md) (infrastructure automation) apply to
infrastructure generally, applied specifically to the visibility fabric:
configuration belongs in version control, applied through a declarative
or API-driven pipeline, not accumulated as a series of undocumented UI
clicks.

### GigaVUE-FM's REST API as the automation foundation

Every capability covered in Chapters 04–07 through the GigaVUE-FM web
UI — node onboarding, Flow Mapping authoring, GigaSMART configuration,
inline bypass settings, RBAC, licensing — is also exposed through
GigaVUE-FM's **REST API**. This matters for three reasons:

1. **Reproducibility.** API-driven configuration can be expressed as code,
   reviewed, versioned, and applied consistently, eliminating the
   "how was this map actually configured" ambiguity that accumulates in
   UI-only environments over time.
2. **Elastic scaling.** Automated V Series node deployment ([Chapter 03](03-gigavue-virtual-nodes-and-virtual-traffic-acquisition.md)) in
   response to cloud auto-scaling events depends on the API to register
   new nodes and apply Flow Mapping without waiting for manual UI
   intervention.
3. **Integration.** SIEM platforms, ticketing systems, and orchestration
   tools consume fabric health, audit, and configuration state through
   the same API surface, rather than through fragile UI scraping or
   manual export.

### Terraform and Ansible integration patterns

Two automation patterns cover most production use cases:

- **Terraform**, used declaratively for infrastructure that has a clear
  desired-state model: V Series node deployment, cloud network
  configuration (VPC peering, security groups/NSGs for tunnel
  reachability), and, in mature deployments, Flow Mapping definitions
  themselves — treating a map as a resource with a defined desired state
  that Terraform reconciles, consistent with the plan/apply separation
  principle from [Volume I](../../volume-01-enterprise-engineering-foundations/README.md).
- **Ansible**, used more often for imperative, sequenced operational
  tasks: bootstrapping a newly onboarded node with a standard baseline
  configuration, orchestrating a phased firmware upgrade across a
  cluster, or applying a bulk Flow Mapping change across many nodes in a
  defined order.

Neither tool is exclusive; many organizations use Terraform to establish
and maintain the fabric's steady-state topology (nodes, licensing,
network connectivity) and Ansible for operational playbooks layered on
top of that steady state (upgrades, bulk changes, incident-response
actions).

### Elastic V Series scaling pattern

A hybrid cloud visibility deployment commonly implements the following
automated pattern, tying together [Chapter 03](03-gigavue-virtual-nodes-and-virtual-traffic-acquisition.md)'s virtual acquisition model
with this chapter's automation layer:

1. A cloud auto-scaling event (a new set of workload instances launched)
   triggers a corresponding automation workflow — either a native cloud
   event (a Lambda-style function reacting to an Auto Scaling Group
   event) or a scheduled reconciliation job.
2. The workflow calls GigaVUE-FM's API (or a Terraform apply against a
   module managing V Series capacity) to provision additional V Series
   node capacity if existing capacity is approaching its licensed or
   processing limit.
3. Virtual tap agents or the Universal Cloud Tap on the new workload
   instances are configured (via the same orchestration tool used to
   launch the instances — a Terraform user-data block or an Ansible
   playbook run as part of instance bootstrap) to tunnel to the
   appropriate V Series tunnel endpoint.
4. GigaVUE-FM applies the standard Flow Mapping policy already defined for
   that workload class, without requiring an operator to manually author
   a new map for every scaling event.

### Ecosystem integrations

GigaVUE-FM's API and native integration connectors commonly feed fabric
health, audit, and application-metadata output into:

- **SIEM platforms** (covered generally in [Volume XI](../../volume-11-observability-enterprise-operations/README.md) observability
  material), consuming both GigaSMART Application Metadata Intelligence
  ([Chapter 06](06-gigasmart-traffic-intelligence-and-packet-transformation.md)) as security-relevant telemetry and GigaVUE-FM's own audit
  and health events as operational telemetry about the visibility fabric
  itself.
- **ITSM/ticketing platforms**, where a fabric health alert (an inline
  tool group failing open, a node losing cluster connectivity) opens a
  tracked incident automatically rather than depending on an operator
  noticing a dashboard.
- **Orchestration and configuration-management tooling**, as described
  above, for both steady-state and event-driven automation.
- **Downstream security tools directly**, in deployments where GigaVUE-FM
  or a node pushes configuration changes (for example, a new Flow Mapping
  rule) in response to a signal from a security tool — a closed-loop
  pattern sometimes called visibility-driven response, where a detection
  tool's finding can trigger a fabric change (for example, elevating a
  suspicious segment's traffic to full packet capture) rather than only
  the reverse direction of data flow this volume has described so far.

## Design Considerations

- **Decide what belongs in Terraform state versus what stays imperative.**
  Not every fabric object benefits from declarative management — highly
  dynamic, event-driven Flow Mapping changes (an incident-response action)
  are often better suited to an imperative Ansible playbook or a direct
  API call than to a Terraform resource whose state file must then be
  reconciled with an out-of-band change.
- **Design idempotent automation from the start.** Any automation that
  provisions V Series capacity, onboards nodes, or applies Flow Mapping
  should be safe to re-run without creating duplicate resources or
  conflicting map definitions — the same idempotency principle
  established in [Volume I](../../volume-01-enterprise-engineering-foundations/README.md)'s automation architecture chapter applies
  directly here.
- **Plan credential and API-token scope narrowly.** An automation identity
  with write access to GigaVUE-FM's API should be scoped to only the
  operations its specific workflow requires (node registration, map
  authoring, read-only health polling), following the least-privilege
  principle already applied to human RBAC in [Chapter 04](04-gigavue-fm-installation-onboarding-security-and-governance.md).
- **Build drift detection into the operating model, not just initial
  deployment.** A fabric managed partly through Terraform and partly
  through ad hoc UI changes accumulates drift silently; a scheduled job
  comparing live GigaVUE-FM configuration against the version-controlled
  source of truth (Terraform state, or an exported configuration
  baseline) catches this before it becomes a production surprise.
- **Treat integration credentials (SIEM export, ITSM webhook, cloud IAM
  roles for V Series automation) as first-class secrets**, managed through
  the same secrets-management practice as any other automation credential
  in the organization, not embedded in playbooks or Terraform
  configuration files in plain text.

## Implementation and Automation

### Authenticating to the GigaVUE-FM REST API

```bash
# Obtain a session token (representative; exact endpoint/payload
# structure varies by GigaVUE-FM release)
curl -sk -X POST "https://fm.example.com/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "automation-svc", "password": "<from-secrets-manager>"}'
```

### Registering a node via API (used by elastic scaling automation)

```bash
curl -sk -X POST "https://fm.example.com/v1/nodes" \
  -H "Authorization: Bearer $FM_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
        "management_ip": "10.60.5.21",
        "credential_id": "vseries-bootstrap-cred",
        "fabric_group": "cloud-visibility-use1"
      }'
```

### Representative Terraform pattern for V Series capacity

```hcl
# gigavue_vseries.tf (illustrative structure)
resource "gigamon_vseries_node" "cloud_use1" {
  count            = var.vseries_node_count
  fabric_group     = "cloud-visibility-use1"
  instance_type    = "m5.xlarge"
  subnet_id        = var.tunnel_endpoint_subnet
  management_vpc   = var.management_vpc_id
}

resource "gigamon_flow_map" "web_tier_https" {
  alias        = "cloud-web-tier-to-ndr"
  source       = gigamon_vseries_node.cloud_use1[0].tunnel_endpoint_id
  destination  = var.ndr_tool_group_id
  rule {
    priority = 10
    action   = "pass"
    match    = "destination-port 443"
  }
}
```

> Provider resource names, arguments, and API endpoint structures shown
> here are illustrative of the automation pattern rather than a literal,
> version-pinned schema; consult the current GigaVUE-FM API reference and
> the maintained Terraform provider documentation for the release in use.

### Ansible playbook pattern for phased firmware upgrade

```yaml
# upgrade-cluster.yml (illustrative structure)
- hosts: gigavue_cluster_members
  serial: 1
  tasks:
    - name: Confirm node health before upgrade
      uri:
        url: "https://fm.example.com/v1/nodes/{{ inventory_hostname }}/health"
        headers:
          Authorization: "Bearer {{ fm_token }}"
      register: pre_health

    - name: Fail fast if node unhealthy before upgrade
      fail:
        msg: "Node unhealthy before upgrade attempt"
      when: pre_health.json.status != "healthy"

    - name: Trigger firmware upgrade
      uri:
        url: "https://fm.example.com/v1/nodes/{{ inventory_hostname }}/upgrade"
        method: POST
        headers:
          Authorization: "Bearer {{ fm_token }}"
        body_format: json
        body: { "target_version": "{{ target_firmware_version }}" }

    - name: Wait for node to report healthy post-upgrade
      uri:
        url: "https://fm.example.com/v1/nodes/{{ inventory_hostname }}/health"
        headers:
          Authorization: "Bearer {{ fm_token }}"
      register: post_health
      until: post_health.json.status == "healthy"
      retries: 30
      delay: 30
```

`serial: 1` deliberately upgrades one cluster member at a time, so a
failed upgrade on one node does not take the entire cluster's visibility
offline simultaneously — the same rolling-upgrade discipline covered
generally in [Volume IX](../../volume-09-infrastructure-automation/README.md).

### SIEM export configuration (conceptual)

```text
GigaVUE-FM UI or API:
Administration > Integrations > SIEM Export
  Destination: siem.example.com:514 (syslog) or HTTPS webhook endpoint
  Event categories: fabric-health, audit, licensing
```

## Validation and Troubleshooting

- **Terraform apply reports drift on every run despite no manual
  changes.** Confirm the provider's read/refresh logic correctly maps
  GigaVUE-FM's live state back to the resource schema; some fabric
  objects (particularly those with server-generated identifiers) require
  explicit `import` handling or lifecycle rules to avoid perpetual
  false-positive drift.
- **Elastic V Series scaling automation provisions capacity but new
  workloads show no visibility.** Confirm the workload bootstrap
  automation actually configures the virtual tap agent's tunnel
  destination to point at the newly provisioned V Series node — a common
  gap is provisioning the node correctly while the workload-side
  automation still points at a stale or default tunnel endpoint from an
  earlier template version.
- **API authentication succeeds but subsequent calls return
  authorization errors.** Confirm the automation service account's RBAC
  role ([Chapter 04](04-gigavue-fm-installation-onboarding-security-and-governance.md)) actually grants the specific API operation being
  called; a role sufficient for read-only health polling will correctly
  reject a node-registration or map-authoring call, which is expected
  least-privilege behavior, not a fault.
- **SIEM receives fabric events with unexpected gaps.** Confirm the
  export configuration's event-category selection actually includes the
  categories the SIEM use case depends on, and confirm network
  reachability (firewall rules) between GigaVUE-FM and the SIEM
  destination has not changed.
- **Ansible playbook upgrade run stalls indefinitely on the health-check
  wait.** Confirm the retry/delay budget is realistic for the platform's
  actual upgrade duration, and check the node's own upgrade log directly
  (via CLI or GigaVUE-FM UI) to distinguish "still upgrading, will
  succeed" from "upgrade failed silently" before assuming the automation
  itself is at fault.

## Security and Best Practices

- Store GigaVUE-FM API credentials and cloud IAM credentials used by
  automation in a dedicated secrets manager, never committed to a
  Terraform or Ansible repository in plain text, consistent with the
  automation-architecture practices in [Volume I](../../volume-01-enterprise-engineering-foundations/README.md) and [Volume IX](../../volume-09-infrastructure-automation/README.md).
- Scope every automation service account narrowly ([Chapter 04](04-gigavue-fm-installation-onboarding-security-and-governance.md)'s RBAC
  model applied to non-human identities), and rotate its credentials on
  the same cadence as other automation identities with write access to
  security-relevant infrastructure.
- Prefer short-lived, federated credentials (OIDC-based, where the
  platform supports it) over long-lived static API tokens for automation
  reaching GigaVUE-FM's API from a CI/CD pipeline, mirroring the OIDC
  federation pattern from [Volume I](../../volume-01-enterprise-engineering-foundations/README.md)'s automation architecture chapter.
- Require code review for changes to version-controlled Flow Mapping and
  fabric-provisioning definitions, with the same rigor as any other
  infrastructure-as-code change affecting production traffic handling.
- Log every API-driven configuration change with the calling identity
  captured in GigaVUE-FM's audit trail ([Chapter 04](04-gigavue-fm-installation-onboarding-security-and-governance.md)), and reconcile
  automation-driven changes against the audit log periodically to detect
  automation misbehavior early.
- Validate that closed-loop, detection-triggered fabric changes (the
  visibility-driven response pattern) include a rate limit or approval
  gate appropriate to their blast radius — an automated response acting
  on a false positive should not be able to silently degrade visibility
  fabric-wide.

## References and Knowledge Checks

**References**

- [Gigamon, *GigaVUE-FM REST API Reference*](https://docs.gigamon.com/ref-api/Content/apiref/apiref.html) — full endpoint and
  authentication documentation for the release in use.
- [Gigamon, Terraform and Ansible integration documentation and published
  provider/module repositories.](https://docs.gigamon.com/gvd-preview/Content/GigamonValidatedDesigns/GVDs/GigaVUE-FMAutomationUsingAnsbile.html)
- [Volume I — Enterprise Engineering Foundations](../../volume-01-enterprise-engineering-foundations/README.md),
  [Chapter 03](03-gigavue-virtual-nodes-and-virtual-traffic-acquisition.md) (Automation Architecture) — plan/apply separation, OIDC
  federation, and declarative-versus-imperative automation principles
  applied throughout this chapter.
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — this volume's
  GigaVUE-FM 6.x baseline.

**Knowledge checks**

1. Why does a hybrid cloud visibility fabric require automation in a way
   that a small, stable physical fabric does not strictly require?
2. Give one example of a fabric object better suited to declarative
   (Terraform) management and one better suited to imperative (Ansible)
   management, with a one-sentence justification for each.
3. In the elastic V Series scaling pattern, what specific step is most
   commonly missed, producing a "node provisioned but no visibility"
   symptom?
4. Why should automation service accounts follow the same least-privilege
   RBAC scoping principle established for human administrators in
   [Chapter 04](04-gigavue-fm-installation-onboarding-security-and-governance.md)?

## Hands-On Lab

**Objective:** Use the GigaVUE-FM REST API to perform a read-only health
query and an authenticated configuration change against a lab fabric,
validating both a successful narrowly-scoped automation credential and a
deliberately over-scoped call that should be rejected.

**Prerequisites**

- A lab GigaVUE-FM instance from [Chapter 04](04-gigavue-fm-installation-onboarding-security-and-governance.md), with at least one onboarded
  lab node.
- `curl` or an equivalent HTTP client, and (optionally) `jq` for readable
  JSON output.
- Ability to create a scoped API service account/role in GigaVUE-FM,
  following the RBAC pattern from [Chapter 04](04-gigavue-fm-installation-onboarding-security-and-governance.md).

**Steps**

1. In GigaVUE-FM, create a service account with a role scoped to
   read-only access on the lab fabric group only (no Flow Mapping write
   permission), following the RBAC pattern from [Chapter 04](04-gigavue-fm-installation-onboarding-security-and-governance.md).
2. Authenticate to the API using this scoped account and store the
   returned token in a shell variable:

   ```bash
   FM_TOKEN=$(curl -sk -X POST "https://<lab-fm-address>/v1/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"username": "lab-readonly-svc", "password": "<lab-password>"}' \
     | jq -r '.token')
   ```

3. Perform a read-only health query against the lab node:

   ```bash
   curl -sk "https://<lab-fm-address>/v1/nodes" \
     -H "Authorization: Bearer $FM_TOKEN" | jq .
   ```

   **Expected result:** the call succeeds and returns the lab node's
   inventory and health status in JSON.
4. **Negative test:** attempt a write operation (for example, creating a
   new Flow Map) using the same read-only-scoped token:

   ```bash
   curl -sk -X POST "https://<lab-fm-address>/v1/maps" \
     -H "Authorization: Bearer $FM_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"alias": "api-test-map", "source": "1/1/x1", "destination": "1/1/g1"}'
   ```

   **Expected result:** the API rejects the call with an authorization
   error, confirming the scoped role correctly enforces least privilege
   at the API layer, not merely in the web UI.
5. Create a second service account scoped with Flow Mapping write
   permission on the lab fabric group, authenticate as that account, and
   repeat the map-creation call.
   **Expected result:** the call succeeds, and the new map is visible
   both via the API (`GET /v1/maps`) and in the GigaVUE-FM web UI,
   confirming API-driven and UI-driven configuration operate on the same
   underlying fabric state.
6. Confirm the map-creation event appears in GigaVUE-FM's audit log
   attributed to the correct service account identity.
7. **Cleanup:** delete the test map via the API, and remove or disable
   both lab service accounts created for this exercise if they will not
   be reused in later chapters.

   ```bash
   curl -sk -X DELETE "https://<lab-fm-address>/v1/maps/api-test-map" \
     -H "Authorization: Bearer $FM_TOKEN_WRITE"
   ```

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

A hybrid enterprise visibility fabric outgrows manual, UI-driven
configuration the moment cloud elasticity and multi-account, multi-region
scale enter the picture. GigaVUE-FM's REST API is the automation
foundation everything else builds on — Terraform for declarative,
steady-state fabric topology, Ansible for sequenced operational tasks, and
native integrations feeding SIEM and ITSM platforms fabric health and
security-relevant telemetry. The same infrastructure-as-code discipline
established in [Volume I](../../volume-01-enterprise-engineering-foundations/README.md) — idempotency, least-privilege automation
identities, code review, and drift detection — applies directly to Flow
Mapping and fabric provisioning, and is what allows the fabric to keep
pace with a cloud environment that changes far faster than any manual
process could track.

- [ ] Can explain why hybrid cloud visibility requires automation beyond
      what a stable physical fabric needs.
- [ ] Can describe GigaVUE-FM's REST API role and how Terraform and
      Ansible each fit into fabric automation.
- [ ] Can walk through the elastic V Series scaling pattern end to end.
- [ ] Can explain least-privilege scoping for automation service accounts
      and why it matters as much as human RBAC.
- [ ] Completed the hands-on lab, including the negative test and
      cleanup.
