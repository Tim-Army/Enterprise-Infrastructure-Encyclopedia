# Volume CIV Glossary

Definitions for terms introduced in **Volume CIV — Linkerd Build-It-Yourself Lab**.
See the [master glossary](../../GLOSSARY.md) for cross-volume terms.

- **Automatic mTLS** — Linkerd's defining behavior: the moment a workload is meshed, its mesh traffic is mutually authenticated and encrypted, with no configuration (contrast Istio's explicit `PeerAuthentication`).
- **AuthorizationPolicy (Linkerd)** — the resource that binds a `Server` to the authentications (identities or networks) permitted to reach it.
- **default-inbound-policy** — a namespace/workload annotation (`config.linkerd.io/default-inbound-policy`) that sets the default for inbound traffic to meshed pods (for example `deny`, `all-authenticated`, `all-unauthenticated`).
- **Identity** — a workload's mesh identity, issued as a TLS certificate from its Kubernetes ServiceAccount, in the form `<sa>.<ns>.serviceaccount.identity.linkerd.cluster.local`.
- **linkerd viz** — Linkerd's observability extension, providing `edges` (which connections are mTLS), `stat`, `tap` (live requests), and a dashboard.
- **Mesh boundary** — the limit of the mesh: it secures only workloads that run a proxy; un-meshed devices need a control below the mesh.
- **MeshTLSAuthentication** — a Linkerd resource naming a set of authorized mesh identities, referenced by an `AuthorizationPolicy`.
- **micro-proxy** — Linkerd's small, fast Rust data-plane proxy injected beside each meshed workload.
- **Server** — a Linkerd policy resource defining a port on a set of pods; creating one flips that port to deny-by-default until an `AuthorizationPolicy` opens it.
- **ServiceAccount** — the Kubernetes identity a workload runs as; Linkerd derives the workload's mesh identity from it.
- **Single-track** — this volume has no "Track 2" because Linkerd is open source; every command runs the real mesh.
