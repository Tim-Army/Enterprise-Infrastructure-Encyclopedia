# Volume CX Glossary

Definitions for terms introduced in **Volume CX — Check Point CloudGuard Build-It-Yourself Lab**.
See the [master glossary](../../GLOSSARY.md) for cross-volume terms.

- **Access rule** — an ordered rule in the access-control rulebase matching source, destination, service, and action; evaluated top to bottom, first match wins.
- **Cleanup rule** — the final explicit rule in a layer, set to Drop (and Log), making default-deny visible and countable.
- **CloudGuard data-center / dynamic object** — an object whose membership is imported from a cloud, vCenter, or Kubernetes source by **tag** and updates automatically, so a rule follows workloads as they change.
- **Identity Awareness** — the Check Point feature that lets a rule match an **access role** (user, group, or machine identity) as source or destination, adding *who* to the rule.
- **Install policy** — the action that pushes a published policy to a gateway; on Check Point, *publish* saves changes but only *install* changes what the gateway enforces.
- **mgmt_cli** — the Check Point management API CLI used to create objects, edit the rulebase, publish, and install policy programmatically.
- **Policy package** — a named set of policy layers installed to one or more gateways; one package can enforce identically across an estate.
- **Security Gateway** — the Check Point enforcement point that inspects traffic and applies the installed rulebase.
- **SIC (Secure Internal Communication)** — the trust established between management and a gateway; a prerequisite for installing policy.
- **SmartConsole** — the Check Point management GUI for authoring objects and the rulebase and installing policy.
- **Track 1 / Track 2** — the two lab paths: real Check Point Management + Gateway (Track 1) and a native Linux/nftables model of objects, rulebase, and tag sets (Track 2).
