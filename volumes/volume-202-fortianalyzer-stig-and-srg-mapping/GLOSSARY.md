# Volume CCII Glossary

Definitions for terms used in **Volume CCII — FortiAnalyzer STIG and SRG Mapping**.
See the [master glossary](../../GLOSSARY.md) for cross-volume terms and the
[Volume CLXXII glossary](../volume-172-disa-srgs-and-stigs/GLOSSARY.md) for
the SRG and STIG terms this volume builds on.

- **ADOM (administrative domain)** — a FortiAnalyzer partition that groups devices and their logs, with its own data policy and disk quota; the Central Log Server retention and storage requirements are set for each ADOM.
- **Alignment category** — the label a crosswalk row carries: same requirement, equivalent requirement, log-source counterpart only, or no Cisco STIG counterpart.
- **Base requirement number** — the first part of an SRG ID (for example `SRG-APP-000065`) that DISA reuses across SRGs for the same underlying requirement; a shared base number suggests, but does not prove, that two requirements are equivalent.
- **Central Log Server SRG** — the DISA SRG for systems that aggregate, store, analyze, and report on log records from other devices; FortiAnalyzer, which has no STIG, is assessed against it.
- **Cisco Secure Network Analytics (SNA)** — Cisco's flow analytics and network detection and response appliance, formerly Stealthwatch; its STIG covers the management plane only, and it is the nearest Cisco appliance to FortiAnalyzer that has a STIG.
- **Core platform feature** — a FortiAnalyzer capability that existed before release 7.0.0, such as log collection, storage, forwarding, and administration; the map lists 53 of them apart from the New Features Guide features.
- **FIPS-CC mode** — the FortiAnalyzer operating mode that restricts the unit to FIPS 140 and Common Criteria validated behavior; it can be enabled only from the console.
- **FortiAnalyzer New Features Guide** — Fortinet's per-release-train document listing every feature added to FortiAnalyzer, tagged with the patch release that introduced it; it is the version source of the map, because Fortinet publishes no FortiAnalyzer feature matrix.
- **Log-source counterpart** — a Cisco STIG rule that governs the sending side of a log-server requirement, such as sending logs to two central log servers or queuing records while the server is unreachable.
- **No direct requirement** — the label for a FortiAnalyzer feature that implements no SRG requirement of its own; if the feature is not needed, it falls under the requirement to disable non-essential capabilities.
- **Prerequisite** — anything that must exist or be configured before a row's setting can meet its requirement, such as an external server, a PKI, the log sources, or a license; each has an ID (P1 to P30) that the map and the crosswalk share.
- **STIG crosswalk** — an alignment of one vendor's STIG rules with another platform's settings through the SRG requirement each rule implements; this volume's crosswalk is anchored on FortiAnalyzer's requirements, because no Cisco STIG implements the Central Log Server SRG.
