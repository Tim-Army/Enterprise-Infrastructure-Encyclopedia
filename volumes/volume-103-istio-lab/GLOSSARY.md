# Volume CIII Glossary

Definitions for terms introduced in **Volume CIII — Istio Build-It-Yourself Lab**.
See the [master glossary](../../GLOSSARY.md) for cross-volume terms.

- **AuthorizationPolicy** — Istio's policy object that permits or denies traffic to a workload by source principal, namespace, and Layer 7 attributes (HTTP method, path, headers, JWT), enforced at the destination's sidecar. Once an ALLOW policy selects a workload, that workload default-denies unmatched traffic.
- **Envoy sidecar** — the proxy Istio injects beside each meshed workload; it terminates mTLS, carries the workload's identity, and enforces authorization.
- **istioctl** — Istio's CLI, used to install the mesh and inspect proxies, certificates, and mTLS status.
- **L7 authorization** — authorizing by application-layer attributes (HTTP method and path) rather than only ports; enforced by the sidecar.
- **Mesh boundary** — the limit of a service mesh: it secures only workloads that run a sidecar. Un-meshed devices (like the PLC) are outside it and need a control below the mesh.
- **mTLS (mutual TLS)** — encrypted, mutually-authenticated transport between meshed workloads; each side proves its identity with a certificate.
- **PeerAuthentication** — the Istio object that sets the mTLS mode (for example STRICT), requiring authenticated, encrypted connections to meshed workloads.
- **Principal** — the authenticated identity of a caller in an AuthorizationPolicy, expressed as `cluster.local/ns/<namespace>/sa/<serviceaccount>`, derived from the mTLS certificate.
- **ServiceAccount** — the Kubernetes identity a workload runs as; Istio derives the workload's SPIFFE identity from it.
- **Sidecar (resource)** — an Istio resource that configures a workload's proxy, including which egress hosts it may reach — used to confine a compromised client.
- **Sidecar injection** — the automatic addition of the Envoy proxy to pods in a namespace labeled `istio-injection=enabled`; a meshed pod shows `2/2` containers.
- **Single-track** — this volume has no "Track 2" because Istio is open source; every command runs the real mesh.
- **SPIFFE** — the standard for cryptographic workload identity Istio uses; a SPIFFE ID (`spiffe://cluster.local/ns/dc/sa/sa-web`) encodes the namespace and ServiceAccount.
