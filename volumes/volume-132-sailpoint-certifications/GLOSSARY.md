# Volume CXXXII — Glossary

| Term | Definition |
|:---|:---|
| **Access profile** | A bundle of entitlements from a single source, given a business-meaningful name; the middle layer between entitlements and roles in Identity Security Cloud. |
| **Aggregation** | Reading accounts and entitlements from a connected source into the identity warehouse. |
| **Authoritative source** | The system of record for who exists (usually HR); it creates and terminates identities, unlike target sources which only contribute accounts. |
| **Birthright access** | Access granted automatically by attribute, with no request or approval — the baseline everyone in a population receives. |
| **Correlation** | Matching an aggregated account to the identity that owns it, so one person's many accounts resolve to one identity. |
| **Entitlement** | A single unit of access on one source: a group membership, an application role, a permission. |
| **Identity Cube** | IdentityIQ's term for an identity — the person plus all correlated accounts and attributes. |
| **Identity Security Cloud (ISC)** | SailPoint's SaaS identity security platform; the product behind the Certified Identity Security Administrator and Engineer certifications. |
| **IdentityIQ (IIQ)** | SailPoint's on-premises identity governance product (Java/Tomcat/database), certified by the IdentityIQ Associate and Engineer exams. |
| **IGA** | Identity Governance and Administration — the discipline of deciding what access is appropriate and proving it, distinct from access management (SSO) and PAM. |
| **JML** | Joiner-Mover-Leaver: the identity lifecycle events that drive automated provisioning and, critically, deprovisioning. |
| **Knowledge Credential** | SailPoint's training-gated, online, adaptive exam (Leader/Professional/Expert); free for the first attempts and the badge never expires. |
| **Orphan account** | An account whose owner is invalid or terminated — an audit finding and a live attack path. |
| **Privilege creep** | Access accumulating over a career because mover events grant new access without revoking the old. |
| **Professional Certification** | SailPoint's proctored, paid, role-based credential ($300–$400, two attempts, 364 days to schedule), renewed every two years. |
| **Recertification Program** | Launched February 2026; extends a SailPoint certification two years through training, projects, and events rather than a re-sit. |
| **Role** | A bundle of access profiles aligned to a job, so approvers review a job rather than raw entitlements. |
| **Role explosion** | The failure state where exceptions have multiplied roles past the point of reviewability (more roles than identities, many single-member). |
| **Rule** | Code (Java/BeanShell) used where a transform cannot express the logic; carries development, deployment, and maintenance cost. |
| **Separation of duties (SoD)** | A policy forbidding a combination of access that would enable fraud, such as creating a vendor and approving payments to it. |
| **Transform** | Declarative, cloud-executed JSON logic that derives or normalizes an attribute value; preferred over a rule wherever possible. |
| **Uncorrelated account** | An aggregated account that matched no identity, usually a data-quality defect or an unowned service account. |
| **Virtual appliance (VA)** | A hardened VM inside your network that bridges on-premises sources to the ISC tenant using outbound-only connections; deployed in redundant clusters. |
| **Workflow** | Cloud automation run by an event trigger (identity created, access granted, campaign finished) to notify, call endpoints, or act. |
