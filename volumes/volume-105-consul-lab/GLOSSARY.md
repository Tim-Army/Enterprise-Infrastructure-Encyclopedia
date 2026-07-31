# Volume CV Glossary

Definitions for terms introduced in **Volume CV — HashiCorp Consul Build-It-Yourself Lab**.
See the [master glossary](../../GLOSSARY.md) for cross-volume terms.

- **ACLs** — Consul's access-control system for tokens and API/UI authorization; enabled here so the catalog and intentions are protected.
- **connect-inject** — the annotation (`consul.hashicorp.com/connect-inject: "true"`) that opts a Kubernetes workload into the Consul mesh, adding a `consul-dataplane` sidecar.
- **Consul Connect** — Consul's service mesh: it injects an Envoy sidecar and secures service-to-service traffic with mutual TLS and SPIFFE identity.
- **consul-dataplane** — the sidecar proxy container Consul adds to a meshed pod.
- **Intention** — Consul's authorization primitive: a rule that a source service may or may not reach a destination service, written by service name, applied identically to pods and VMs.
- **Intention precedence** — the rule that a more-specific intention (exact source and destination) overrides a wildcard, so a default-deny `* -> *` plus exact allows yields least privilege.
- **L7 intention** — an intention with `permissions` that restrict HTTP methods and paths; requires the destination's protocol declared as `http` via `ServiceDefaults`.
- **Multi-platform** — Consul's defining capability: one mesh, one catalog, and one intention set spanning Kubernetes pods, VMs, and bare metal.
- **ServiceDefaults** — a Consul config entry that sets defaults for a service, including its protocol (`http` is required for L7 intentions).
- **ServiceIntentions** — the Kubernetes custom resource that expresses intentions declaratively.
- **Single-track** — this volume has no "Track 2" because Consul is open source; every command runs the real mesh.
- **SPIFFE identity** — the cryptographic service identity Consul issues, encoding the service name (and namespace/datacenter), portable across platforms.
