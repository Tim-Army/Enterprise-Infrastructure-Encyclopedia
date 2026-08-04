# Volume CXXX — Glossary

| Term | Definition |
|:---|:---|
| **3-2-1-1-0 rule** | The modern resilient-backup rule: 3 copies, 2 media, 1 offsite, 1 immutable/air-gapped, 0 recovery errors (tested). |
| **Air-gap (logical)** | Keeping backup data unreachable/unwritable from the production network an attacker may control, so a production compromise can't destroy the recovery copy. |
| **Anomaly detection** | Flagging attacks (e.g. ransomware) from unusual patterns in the backup stream — change rate, entropy, file-operation surges. |
| **Application-consistent backup** | A backup taken with the application quiesced (VSS/pre-scripts) so it restores cleanly and immediately, unlike a crash-consistent snapshot. |
| **Cyber resilience** | Designing to recover fast and cleanly on the assumption of breach — the premise of Rubrik Security Cloud. |
| **Data Threat Analytics** | Rubrik's analysis of backups for ransomware/malware indicators, impact scope, and the last clean recovery point. |
| **DSPM (Data Security Posture Management)** | Discovering, classifying, and risk-scoring sensitive data and its access — knowing what data you have and how exposed it is. |
| **Identity resilience** | Protecting and recovering identity systems (Active Directory / Entra ID) — the "and Identity" in Rubrik's platform — so a clean identity fabric can be restored after compromise. |
| **Immutability** | The property that a written backup cannot be modified or deleted (even by an admin) until retention expires — the defense against ransomware destroying backups. |
| **Last clean snapshot** | The most recent recovery point before an attack began; recovering from it (rather than the latest) avoids reinfection. |
| **Mass recovery** | Orchestrated recovery of many systems at once, in dependency order — used after a widespread ransomware event. |
| **RCSA** | Rubrik Certified System Administrator — the active Rubrik certification, validating operational administration of Rubrik Security Cloud. |
| **RCE** | Rubrik Certified Engineer — a retired Rubrik credential (expired on Credly). |
| **Recovery validation** | Test-recovering in isolation and verifying integrity/boot — proving recoverability before it's needed (the "0 errors"). |
| **RTO / RPO** | Recovery Time Objective (tolerable downtime, drives recovery speed/orchestration) and Recovery Point Objective (tolerable data loss, drives snapshot frequency). |
| **Rubrik Backup Service (RBS)** | The lightweight connector/agent on hosts enabling application-consistent backups. |
| **Rubrik Security Cloud (RSC)** | Rubrik's SaaS control plane (policy, search, analytics, orchestration) over local immutable data (clusters/cloud). |
| **SLA Domain** | A reusable protection policy (frequency, retention, archive/replication, immutability); workloads are assigned to it rather than scheduled by hand. |
