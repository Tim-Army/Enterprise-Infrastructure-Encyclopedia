# Volume CLXIX — Glossary

| Term | Definition |
|:---|:---|
| **Content Platform (HCP)** | Hitachi Vantara's object storage — stores objects (data + rich metadata + ID) in a flat namespace over HTTP/S3, at massive scale, with durability and WORM/retention; for archives, backups, and unstructured data. |
| **Dynamic Provisioning** | Hitachi's thin provisioning — present a volume of a given virtual size but consume physical capacity only as data is written (allowing over-provisioning), requiring active pool-capacity monitoring. |
| **Dynamic Tiering** | Hitachi's automatic tiering — moves hot (frequently accessed) data to fast media (flash) and cold data to slower/cheaper media, optimizing cost and performance without manual effort. |
| **HCE exam** | A Certification-credential exam (HCE-xxxx) — high-stakes, closed-book, proctored (onsite/remote), validating hands-on real-world skills; earns Specialist or Expert level. |
| **HQT exam** | A Qualification-credential exam (HQT-xxxx) — medium-stakes, some open-book/unproctored, validating foundational/role-based knowledge; earns Associate or Professional level (e.g. HQT-6742, VSP 360 Storage Administration, 35Q/60min/65%/$100). |
| **HVCP** | Hitachi Vantara Certified Professional — the certification program, split into Qualification credentials (HQT exams) and Certification credentials (HCE exams) across four levels and multiple tracks. |
| **LDEV / LUN** | A logical device / logical unit — a logical volume carved from a pool and presented (mapped) to a host over the SAN; the unit of block storage an administrator provisions. |
| **Ops Center** | Hitachi's unified storage-management suite — Administrator (manage/provision), Automator (automate via templates/self-service), Protector (orchestrate snapshots+replication), Analyzer (performance/capacity analytics). |
| **Pentaho** | Hitachi Vantara's data software — Pentaho Data Integration (PDI, visual ETL: transformations + jobs) and Pentaho Business Analytics (reporting, dashboards, OLAP); the data track of the portfolio. |
| **Pentaho Data Integration (PDI)** | Pentaho's ETL tool (historically Kettle) — build transformations (input → transform steps → output, visually) orchestrated by jobs, to move and transform data. |
| **Storage virtualization** | Hitachi's signature VSP capability — a VSP can virtualize other (including third-party) storage arrays behind it, presenting them as one managed pool and applying VSP data services across them. |
| **SVOS** | Storage Virtualization Operating System — the software running a VSP array, providing provisioning, data services, and virtualization. |
| **Thin Image / ShadowImage** | Hitachi local copy technologies — Thin Image = space-efficient point-in-time snapshots; ShadowImage = full local clones — for fast recovery, backup, and test/dev within an array. |
| **TrueCopy** | Hitachi synchronous remote replication — every write commits to both local and remote arrays before acknowledging, giving RPO = 0 (zero data loss) but requiring low latency (metro distance). |
| **Universal Replicator** | Hitachi asynchronous remote replication — writes replicate to the remote array with a small lag, giving a small RPO over any distance without slowing the application. |
| **RPO / RTO** | Recovery Point Objective (how much data, in time, you can afford to lose) and Recovery Time Objective (how quickly you must recover) — the metrics that drive replication and DR design. |
| **UCP (Unified Compute Platform)** | Hitachi's converged infrastructure — pre-integrated, validated compute + networking + storage as an engineered system with single support, scaled per layer (vs hyperconverged, which combines compute+storage in nodes). |
| **VSP (Virtual Storage Platform)** | Hitachi Vantara's enterprise block-storage line (VSP 5000, Midrange, One Block, VSP 360) — redundant (dual controllers, mirrored cache, RAID), with storage virtualization; the platform most storage certifications center on. |
| **VSP One File** | Hitachi Vantara's file storage / NAS — presents shared file systems over NFS/SMB with quotas and permissions, for user shares and file workloads. |
