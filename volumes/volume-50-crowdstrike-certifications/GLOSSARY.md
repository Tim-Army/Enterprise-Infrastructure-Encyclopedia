# Volume L Glossary

Definitions for terms used in **Volume L — CrowdStrike Certification Tracks**,
alphabetized. See also the [volume index](INDEX.md) and the
[master glossary](../../GLOSSARY.md) for cross-volume terminology.

**AID (Agent ID)** — The unique identifier a Falcon sensor assigns to a host;
anchor investigations on the AID, not the reusable hostname. Used in Chapters 02–03.

**CID (Customer ID)** — The tenant identifier a sensor reports to; set at or after
install with `falconctl`. Used in Chapter 02.

**CQL (CrowdStrike Query Language)** — The query language for Falcon event search and
Next-Gen SIEM (filtering, aggregation, stacking). Used in Chapters 04–06.

**CSPM / CWP / CIEM** — Cloud Security Posture Management (misconfig), Cloud Workload
Protection (runtime), Cloud Infrastructure Entitlement Management (permissions) — the
pillars of Falcon Cloud Security. Used in Chapter 08.

**Falcon Cloud Security** — CrowdStrike's cloud-security module spanning CSPM, CWP,
and CIEM across AWS/Azure/GCP. Used in Chapter 08.

**Falcon Fusion SOAR** — Falcon's built-in security orchestration, automation, and
response (workflows). Used in Chapters 02, 06, 07.

**Falcon Identity Protection** — CrowdStrike's identity-threat module that scores and
gates authentication with Zero Trust policy. Used in Chapter 07.

**FalconPy** — The official CrowdStrike Python SDK (`crowdstrike-falconpy`) wrapping
the Falcon REST API. Used throughout.

**falconctl** — The Falcon sensor command-line tool for configuration and status
(e.g., reading the CID/AID). Used in Chapter 02.

**GraphQL API** — The query interface for Falcon Identity Protection data and
mutations. Used in Chapter 07.

**Next-Gen SIEM** — Falcon's SIEM built on a scalable log platform, queried with CQL;
the CCSA/CCSE domain. Used in Chapters 05–06.

**RFM (Reduced Functionality Mode)** — A degraded sensor state (often from a kernel/OS
mismatch) that reduces protection; find and remediate RFM hosts. Used in Chapter 02.

**RTR (Real Time Response)** — Falcon's live remote-shell capability for
investigation and remediation, under audited least privilege. Used in Chapter 03.

**Sensor** — The lightweight Falcon agent on endpoints/workloads that streams
telemetry to the cloud and enforces policy. Used in Chapters 02, 08.

**Step-up MFA** — Requiring additional authentication on elevated risk instead of
hard-blocking; the core Identity Protection control. Used in Chapter 07.

**Zero Trust** — The "never trust, always verify" model Identity Protection applies to
every authentication. Used in Chapter 07.
