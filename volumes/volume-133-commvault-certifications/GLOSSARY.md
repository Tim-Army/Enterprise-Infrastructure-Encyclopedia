# Volume CXXXIII — Glossary

| Term | Definition |
|:---|:---|
| **Air gap** | Isolation of a backup copy from the production environment — physical (offline media) or logical (separate account/tenant, independent credentials, narrow replication window). |
| **Application-consistent** | A backup taken with the application quiesced and its logs flushed, producing a recoverable state; required for anything transactional. |
| **Auxiliary copy** | A duplicate of a backup to another location or medium; how the 3-2-1 rule is implemented. |
| **Cleanroom Recovery** | Commvault's isolated, on-demand recovery environment built from known-good images — used both for real incident recovery away from a compromised estate and for non-disruptive recovery rehearsal. |
| **Cloud Rewind** | Commvault's capability for rebuilding cloud applications and their dependencies in dependency order, not merely restoring individual resources. |
| **CommCell** | One managed Commvault environment: CommServe, MediaAgents, agents, and storage libraries. |
| **CommServe** | The control plane holding configuration, schedules, job history, and the index; losing it means losing the catalog that makes backup data findable. |
| **Crash-consistent** | A backup equivalent to pulling the power — acceptable for stateless workloads, a risk for databases. |
| **Cycle** | A full backup plus the incrementals depending on it; retention prunes a cycle as a unit, which is why deleting old incrementals frees no space. |
| **Deduplication** | Storing each unique block once and replacing repeats with references; must run *before* compression and encryption or the savings vanish. |
| **DDB (deduplication database)** | The MediaAgent-resident index of block signatures; I/O-intensive (belongs on SSD), critical to protect, and sealed when oversized or corrupted. |
| **GFS** | Grandfather-father-son retention: daily copies kept briefly, weekly longer, monthly/yearly longest. |
| **Immutability** | Storage-layer enforcement (object lock/WORM) preventing modification or deletion until retention expires — including by an administrator, which is the point. |
| **MediaAgent** | The data plane: moves data to storage, owns the DDB, mounts libraries. Placement determines whether the backup window is met. |
| **Plan** | The Command Center object binding what is protected, where copies go, retention, and schedule (historically the storage policy). |
| **Readiverse Academy** | Commvault's training and certification platform, home of the four-tier program introduced June 2026. |
| **RPO / RTO** | Recovery Point Objective (tolerable data loss, set by backup frequency) and Recovery Time Objective (tolerable downtime, set by recovery speed and storage tier). |
| **Synthetic full** | A full backup assembled on the MediaAgent from existing backup data rather than re-read from the client — fast restores with no production impact. |
| **Threat Scan** | Commvault's inspection of protected data for corruption, encryption, or malware, used to identify a genuinely clean recovery point. |
| **3-2-1 rule** | Three copies, two media types, one off-site; extended to 3-2-1-1-0 with one immutable/air-gapped copy and zero verification errors. |
| **Verification ladder** | Escalating proof of recoverability: job success, data verification, synthetic full, test restore, full rehearsal — only the last two prove recovery. |
