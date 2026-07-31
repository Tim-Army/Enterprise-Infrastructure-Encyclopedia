# Volume CII Glossary

Definitions for terms introduced in **Volume CII — Cilium Build-It-Yourself Lab**.
See the [master glossary](../../GLOSSARY.md) for cross-volume terms.

- **cilium CLI** — the command-line tool that installs Cilium into a cluster, manages Hubble, and reports status.
- **CiliumClusterwideNetworkPolicy (CCNP)** — a Cilium policy that is cluster-wide rather than namespaced; its selectors must include the namespace label to be precise.
- **CiliumNetworkPolicy (CNP)** — Cilium's namespaced policy object, which extends Kubernetes NetworkPolicy with identity selectors and Layer 7 rules.
- **eBPF** — the Linux kernel technology Cilium uses to enforce policy and process packets, in place of iptables.
- **FQDN policy** — a Cilium egress rule (`toFQDNs`) that permits traffic to a destination by DNS **name**; Cilium learns the name's addresses by proxying the pod's DNS.
- **Hubble** — Cilium's observability layer, which reports every flow with source/destination identity, verdict, and Layer 7 detail, via a CLI and a service-map UI.
- **Identity (security identity)** — a numeric identity Cilium derives from a workload's labels and enforces on in eBPF, so policy follows the workload rather than its IP.
- **kind** — "Kubernetes in Docker"; runs a full cluster as containers on one host.
- **L3/L4 policy** — policy on addresses/identities and ports; the layer standard Kubernetes NetworkPolicy operates at.
- **L7-aware policy** — policy that inspects application-layer protocol detail (HTTP method/path, DNS names, Kafka, gRPC); Cilium's distinguishing capability, enforced via an in-kernel proxy.
- **Verdict** — Hubble's label for what happened to a flow: `FORWARDED` (allowed) or `DROPPED` (denied), reported in the same identity terms as policy.
