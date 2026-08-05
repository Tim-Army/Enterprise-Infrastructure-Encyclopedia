# Volume CXLV — Glossary

| Term | Definition |
|:---|:---|
| **ACA** | Atlassian Certified Associate — the middle credential tier, for professionals who *use* Atlassian apps in their jobs (e.g. Managing Jira Projects for Cloud). |
| **ACH** | Atlassian Certificate Holder — the free, foundational credential tier for app users (e.g. Atlassian Cloud Fundamentals). A genuine first step at zero cost. |
| **ACP** | Atlassian Certified Professional — the top tier, role-based, for solution *administrators* (Jira Administration, Confluence Administration, Cloud Organization Admin). |
| **Admin hub** | `admin.atlassian.com` — the organization admin's console, distinct from any single product's settings, for managing users, security, and billing. |
| **Atlassian Guard** | The organization security layer (formerly Atlassian Access): SSO, SCIM provisioning, enforced policies, and domain verification. Policy can only be enforced on verified domains. |
| **Company-managed project** | A Jira project configured centrally by administrators, sharing workflows, permissions, and fields via schemes across many projects — standardization at the cost of central control. |
| **Designation** | A meta-credential recognizing multiple credentials earned in a related path — a breadth signal, not a single exam. |
| **JQL** | Jira Query Language — powers filters, boards, and dashboards. Performance discipline: put indexed, selective filters (project, status) first and expensive ones (text search) last. |
| **JSM** | Jira Service Management — Jira reshaped for service delivery (ITSM), unified with the development toolchain. Request types, queues, SLAs; agents are licensed, customers are not. |
| **Knowledge rot** | The decay of Confluence content into stale, misleading pages indistinguishable from current ones — worse than missing docs. Fought with templates, review cycles, and archiving. |
| **Marketplace** | Atlassian's third-party app ecosystem. Each app is a dependency and a data-access grant; governance means installing deliberately and auditing by usage, vendor health, and access. |
| **Page restriction** | A Confluence limit on an individual page that can only *narrow* access, never widen it — effective access is the space permission intersected with the page restriction. |
| **Scheme** | A reusable Jira configuration object (workflow, permission, notification, field) shared across many projects. Its power (configure once) is its danger (edit once, change every project using it). |
| **SCIM** | The provisioning protocol that auto-creates, updates, and deprovisions Atlassian users from an identity provider — closing the offboarding hole where departed employees keep access. |
| **SLA (JSM)** | A time commitment on a request with a clock that *pauses* during customer-side waits and *resumes* when the agent holds the ball. Misconfigured pauses misreport agent performance. |
| **Team-managed project** | A Jira project the team configures independently, self-contained rather than scheme-shared — autonomy and speed at the cost of org-wide consistency. |
| **Three-tier structure** | Atlassian's credential model: ACH (free, users) → ACA (users) → ACP (administrators), plus designations. A responsibility ladder, not a difficulty ladder. |
| **Velocity** | The agile throughput metric — a per-team *planning* aid that collapses when used to compare teams or pressure improvement, as estimates inflate (Goodhart's law). |
| **Workflow** | An issue's lifecycle of statuses and transitions, with conditions (who can transition), validators (what's required), and post-functions (what happens after). Model the real process, then stop. |
