# Volume XCVIII Glossary

Definitions for terms introduced in **Volume XCVIII — Elisity Build-It-Yourself Lab**.
See the [master glossary](../../GLOSSARY.md) for cross-volume terms.

- **Access switch** — the network device at the access layer that Elisity programs to enforce policy; in this lab modeled by the `el-gw` router as the network enforcement point.
- **Agentless enforcement** — enforcing policy on the network rather than on the endpoint, so protected devices need no installed software.
- **Break-glass** — a pre-arranged recovery path when a policy locks you out: the out-of-band host adapters, a revert to observation, or a snapshot restore. Because enforcement is on the network, break-glass here is a path that does not cross the enforcement point.
- **CMDB source** — a configuration source of record (function, ownership) ingested into the IdentityGraph; modeled in Track 2 by an inventory CSV.
- **el-gw / el-app01 / el-db01 / el-win01 / el-ot01** — the lab's five virtual machines: four-legged router/enforcement point, nginx application tier, PostgreSQL database (on its own segment), Windows SCADA/HMI workload, and the agentless "PLC".
- **Identity-based policy** — policy written against classifications and attributes (AppServer, Database, HMI, PLC) rather than IP addresses, so it survives re-addressing and change.
- **IdentityGraph** — Elisity's continuously-updated classification of every user, device, and workload, fused from existing identity and context sources independent of IP.
- **Identity sources** — the systems Elisity ingests to classify assets: Active Directory / Entra ID, vCenter, ServiceNow / CMDB, Infoblox (IPAM), and EDR.
- **Network enforcement point** — the device where policy is enforced (an access switch in production; `el-gw` in this lab), which all cross-segment traffic crosses.
- **nftables identity groups** — `nftables` sets named by identity classification and populated from the IdentityGraph; the native stand-in for Elisity policy groups.
- **PLC (Programmable Logic Controller)** — an industrial controller that runs no agent; classified from network context and policed by identity at the network, needing no special handling.
- **Policy groups** — named identity classifications that policy references (AppServer, Database, HMI, PLC), decoupling policy from addresses.
- **Track 1 / Track 2** — this volume's dual paths: Track 1 uses real Elisity Cloud with a Virtual Edge on switches; Track 2 builds the IdentityGraph and compiles identity-based ACLs on the router.
- **VBS (Virtualization-Based Security)** — Windows security features, including Memory Integrity (HVCI), that run the Microsoft hypervisor beneath Windows and contend with VMware Workstation for VT-x.
- **Virtual Edge** — Elisity's lightweight on-network connector that lets Elisity Cloud program the access switches; it has no native stand-in and is treated as a Design Exercise.
