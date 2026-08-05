# Volume CLVII — Glossary

| Term | Definition |
|:---|:---|
| **Air-gapping** | Keeping a backup copy isolated from the production network (logically or physically), so even a total network compromise cannot reach it; FortKnox provides an air-gapped SaaS vault. |
| **Anomaly detection** | Cohesity's analysis of backup data for ransomware indicators — a spike in data-change rate, high encryption entropy, mass file modifications — used to detect attacks early and identify the last clean recovery point. |
| **CCPA / CCIP / CCPP / CCSS** | The Cohesity credentials: Certified Protection Associate, Certified Implementation Professional, Certified Protection Professional, and Certified Security Specialist — awarded across the Academy's three tiers. |
| **Clean-room recovery** | Recovering data from a cyber-vault into an isolated, known-clean environment (rather than a still-compromised network), validating it, and then restoring the business — avoiding re-infection. |
| **Cohesity Data Cloud** | Cohesity's unified AI-powered data security and management platform, consolidating backup (DataProtect), files (SmartFiles), cyber-vaulting (FortKnox), and AI (DataHawk/Gaia) on shared, deduplicated, immutable storage. |
| **DataHawk** | Cohesity's AI-powered data-security service — threat detection (ransomware behavior and malware IOCs in backups), sensitive-data classification, and cyber-vaulting integration. |
| **DataLock** | A WORM (write-once, read-many) capability that locks backups for a period under strict controls, so even a Cohesity administrator cannot delete them before expiry — defending against insider threat and compromised admin credentials. |
| **DataProtect** | Cohesity's backup-and-recovery engine — policy-based protection of VMs, databases, NAS, SaaS, and cloud, with replication, archival, and fast/mass recovery; the core of the Data Cloud. |
| **FortKnox** | Cohesity's SaaS cyber-vaulting service — a managed, cloud-based, isolated, immutable, air-gapped copy of data, providing the last-resort clean copy (the extra "1" in 3-2-1-1) and clean-room recovery. |
| **Gaia** | Cohesity's generative-AI capability — conversational, natural-language search over your own backup corpus, turning backup data into a queryable knowledge base. |
| **Immutable snapshot** | A backup copy that cannot be modified or deleted for its retention period — not by an admin, a compromised account, or ransomware — defeating the attacker playbook of deleting backups first. |
| **Instant mass restore** | Recovering many workloads (up to the whole estate) rapidly and at once — exactly what ransomware recovery demands. |
| **Multicloud data management** | Protecting and managing data across on-premises and multiple clouds (AWS/Azure/GCP) with consistent policy, immutability, and recovery; the subject of the Protection Associate — Multicloud certification. |
| **NetBackup** | Veritas's widely-deployed enterprise backup software, added to the Cohesity portfolio via the December 2024 merger; NetBackup Appliances are the integrated hardware-plus-software systems. Certified via Protection Professional. |
| **Policy-based protection** | Driving backup by protection policies (what to protect, frequency/RPO, retention, where copies go) assigned to workloads, rather than per-workload scripting — making protection at scale manageable and auditable. |
| **Ransomware resilience** | Surviving and recovering from ransomware via immutable and air-gapped backups (a clean copy exists), anomaly detection (which copy is clean), and rapid mass restore — making ransomware a recoverable event. |
| **SmartFiles** | Cohesity's software-defined file and object services (NFS/SMB/S3) serving unstructured data from the platform, consolidating NAS sprawl with immutability, anomaly detection, and governance; certified via Implementation Professional. |
| **3-2-1 / 3-2-1-1** | The backup rule of three copies on two media with one off-site; the ransomware-era addition (3-2-1-1) requires at least one immutable, air-gapped copy, with zero recovery errors (3-2-1-1-0). |
| **Veritas merger** | Cohesity's December 2024 merger with Veritas's data-protection business, making it the largest data-protection vendor and adding NetBackup and NetBackup Appliances to the certification portfolio. |
