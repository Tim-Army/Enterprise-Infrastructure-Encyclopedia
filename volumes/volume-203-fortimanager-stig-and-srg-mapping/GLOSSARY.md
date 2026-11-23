# Volume CCIII Glossary

Definitions for terms used in **Volume CCIII — FortiManager STIG and SRG Mapping**.
See the [master glossary](../../GLOSSARY.md) for cross-volume terms and the
[Volume CLXXII glossary](../volume-172-disa-srgs-and-stigs/GLOSSARY.md) for
the SRG and STIG terms this volume builds on.

- **Administrator profile** — the set of permissions given to a FortiManager administrator, such as who may edit provisioning templates or install configuration; the command column of the map names the permission that limits each feature.
- **ADOM (administrative domain)** — a FortiManager partition that groups managed devices with their policy packages and objects, so that an administrator's access can be limited to the devices of one domain.
- **Baseline** — the saved state every lab starts from and returns to: the `baseline-203` snapshots of the FortiManager and of its managed FortiGate, and a configuration backup of the FortiManager.
- **Core platform feature** — a FortiManager capability that existed before release 7.0.0, such as management access, administrators, auditing, backup, and the central management functions; the map lists 52 of them apart from the New Features Guide features.
- **FGFM (FortiGate-to-FortiManager protocol)** — the TLS management tunnel between FortiManager and the devices it manages.
- **FIPS-CC mode** — the FortiManager operating mode that restricts the unit to FIPS 140 and Common Criteria validated behavior; it can be enabled only from the console.
- **FortiManager New Features Guide** — Fortinet's per-release-train document listing every feature added to FortiManager, tagged with the patch release that introduced it; it is the version source of the map, because Fortinet publishes no FortiManager feature matrix.
- **Gap lab** — a lab for a requirement the product cannot meet: it proves that the setting is absent, applies the nearest compensating control, and records the disposition.
- **Lab column** — the last column of each SRG table in Chapter 01, which links an SRG ID to the lab that proves it.
- **Network Device Management (NDM) SRG** — the DISA SRG for the management plane of a network device: administrator accounts and authentication, sessions, audit records, configuration-change control, and cryptography; FortiManager, which has no STIG, is assessed against it.
- **No direct requirement** — the label for a FortiManager feature that implements no SRG requirement of its own; if the feature is not needed, it falls under the requirement to prohibit unnecessary functions.
- **Policy package** — a set of policies and objects that FortiManager installs on the devices it manages.
- **Prerequisite** — anything that must exist or be configured before a row's command can meet its requirement, such as an external server, a PKI, the managed devices, or a license; each has an ID (P1 to P23).
- **Provisioning template** — a FortiManager template that changes the configuration of managed devices, so access to it is limited to authorized administrators.
- **Requirement lab** — a lab that configures the setting behind a group of SRG requirements, proves it with a positive test, and proves the control with a negative test.
- **Workflow mode** — the FortiManager mode in which configuration changes are approved and recorded.
- **Workspace mode** — the FortiManager mode that locks an ADOM or a policy package while an administrator changes it.
