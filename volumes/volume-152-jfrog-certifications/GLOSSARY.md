# Volume CLII — Glossary

| Term | Definition |
|:---|:---|
| **Artifactory** | JFrog's universal binary repository manager — stores, versions, and serves every package type (Docker, npm, Maven, PyPI, Go, Helm…) in one system. The single source of truth for binaries. |
| **Build info** | The metadata record of how an artifact was produced (source commit, dependencies, build tool, environment, who and when), attached permanently — making the artifact traceable and auditable. |
| **Curation** | A gate on packages entering the organization: evaluates each public package against policy (malicious? critical CVE? forbidden license? suspiciously new?) and blocks the bad ones before they enter — prevention at the front door. |
| **DevOps Engineer certification** | JFrog's flagship credential (JFrog Artifactory Certified DevOps Engineer) — a proctored, 47-question, 90-minute, 70%-to-pass exam validating repository management, security, and CI/CD together. |
| **Disaster recovery (DR)** | Surviving the loss of an entire site via replication to a second site — distinct from HA, which survives component failures within a site. A mature deployment needs both. |
| **Distribution** | Delivering a release as a signed, immutable release bundle pushed to distribution edges near consumers — fast, scalable delivery to many (or distant, or air-gapped) destinations. |
| **High availability (HA)** | Running Artifactory as a cluster of nodes behind a load balancer so a node failure or maintenance causes no downtime — because the binary hub is on the critical path of every build and deploy. |
| **Immutability** | The property that a published artifact version is fixed bytes forever and cannot be overwritten — the basis for trusting that what you scanned, tested, and promoted is the same artifact throughout. |
| **Impact analysis** | Xray's ability to instantly identify every artifact, build, and deployment containing a newly-disclosed vulnerable component (via build info) — turning a CVE panic into a query. |
| **Local / Remote / Virtual repository** | The three Artifactory repository types: local (your own artifacts), remote (a caching proxy of an upstream public registry), and virtual (an aggregation of several repos behind one URL). |
| **Promotion** | Moving one immutable artifact through environments (dev → staging → prod) without rebuilding — so the exact bytes tested are the exact bytes shipped. Build once, promote many. |
| **Provenance** | Verifiable evidence of where an artifact came from and how it was built (pipeline, source, signature) — letting a consumer trust the artifact is genuine and untampered. |
| **SBOM** | Software Bill of Materials — a complete machine-readable list of every component in an artifact (an ingredients label), increasingly required and auto-generated from the hub's knowledge of contents. |
| **Software supply chain** | The chain of components a piece of software is built from — an attack surface, since compromising one widely-used component compromises everyone who uses it. |
| **Xray** | JFrog's security and compliance scanner — deep recursive scanning of artifacts and all their transitive components for vulnerabilities and license issues, with impact analysis. |
