# Volume CXLVII — Glossary

| Term | Definition |
|:---|:---|
| **Agentless scanning** | Assessing workloads by snapshotting them through the cloud provider's APIs rather than installing an agent on each — giving complete, day-one coverage of everything in the account with no deployment friction. Wiz's original differentiator. |
| **ASPM** | Application Security Posture Management — securing what developers produce (code, IaC, secrets) before it becomes cloud. The capability behind Wiz Code. |
| **Attack path** | A concrete route through the Security Graph from an entry point (internet exposure, a compromised identity) to a crown jewel (sensitive data, admin privilege), each hop enabled by a real relationship. Has chokepoints — single fixes that sever it. |
| **Chokepoint** | A single node on an attack path whose remediation breaks the whole path — the smallest fix that removes the risk, even if other factors remain. |
| **CIEM** | Cloud Infrastructure Entitlement Management — determining *effective* permissions (assigned policies plus group memberships plus assumable-role chains, minus denies) so hidden privilege escalation is visible. The privilege factor of a toxic combination. |
| **CNAPP** | Cloud-Native Application Protection Platform — the consolidation of CSPM, CWPP, CIEM, and DSPM into one platform, because risk lives in the connections between those domains that separate tools cannot see. |
| **CSPM** | Cloud Security Posture Management — continuously checking cloud configurations against a secure baseline and compliance frameworks (CIS, PCI, SOC 2, HIPAA) and reporting the failures. |
| **CWPP** | Cloud Workload Protection Platform — securing workloads (VMs, containers, functions), including vulnerability and (with Defend) runtime protection. |
| **DSPM** | Data Security Posture Management — discovering and classifying sensitive data (PII, PHI, PCI, secrets) wherever it lives and assessing its exposure. The crown-jewel end of an attack path. |
| **Democratization** | Routing each security issue to the team that owns the resource, in their own workflow (PR/Slack/Jira), rather than funneling everything through a central team — so security scales with the organization. |
| **Effective permissions** | What an identity can *actually* do once the whole graph of policies, groups, and assumable roles is resolved — as opposed to what is directly assigned. The gap is where escalation hides. |
| **Posture Issue** | A Wiz grouping of many related findings into one actionable outcome with a single root cause, owner, and fix (e.g. 180 log4j findings → one base-image fix) — turning a backlog into a to-do list. |
| **Security Graph** | The Wiz substrate: a graph whose nodes are cloud resources and whose edges are their relationships, turning security questions into graph queries and letting attack paths be computed across the whole estate. |
| **Shift-left** | Moving security earlier — from production back toward development — so risk is caught in the pull request (a review comment) rather than in the cloud (a ticket) or at runtime (a breach). |
| **Toxic combination** | A set of individually-common issues that together form serious risk — canonically public exposure + a critical vulnerability + high privilege + access to sensitive data. The combination, not any single factor, is the risk. |
| **Wiz Cloud** | The CNAPP posture pillar — CSPM, CWPP, CIEM, DSPM, and vulnerability management, agentless. The subject of the Cloud Fundamentals exam. |
| **Wiz Code** | The shift-left pillar — scanning code, IaC, and secrets before deployment, with code-to-cloud tracing back to the source line. |
| **Wiz Defend** | The CDR (Cloud Detection and Response) pillar — runtime threat detection and response with graph context. The subject of the Defend Fundamentals exam (60 Q / 150 min / 2-year). |
