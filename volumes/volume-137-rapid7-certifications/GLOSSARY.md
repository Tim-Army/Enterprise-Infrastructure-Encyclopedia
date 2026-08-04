# Volume CXXXVII — Glossary

| Term | Definition |
|:---|:---|
| **Aging** | How long findings have been open; a stable open count with rising average age means easy findings close while hard ones accumulate. |
| **Authenticated scan** | A credentialed scan enumerating installed software and patch state directly; typically reveals an order of magnitude more than an unauthenticated scan, at the cost of managing privileged scan accounts. |
| **Collector** | The InsightIDR component receiving and forwarding log data; sized below peak event rate it drops data silently, which presents as quiet rather than as an error. |
| **Deception technology** | Decoys — honeypots, honey users, honey credentials, honey files — whose defining property is that legitimate users have no reason to touch them, making interaction suspicious by construction. |
| **Exception** | A recorded decision not to remediate, requiring a named owner, a reason, any compensating control, and an **expiry date**; without an expiry it is permanent silent risk acceptance. |
| **Insight Agent** | The endpoint agent reporting continuously to the Insight platform, covering assets wherever they are — including the roaming population that scheduled scanning misses. |
| **InsightAppSec** | Rapid7's dynamic application security testing (DAST) product, exercising a running web application. |
| **InsightConnect** | Rapid7's SOAR product, executing playbooks of trigger, enrichment, decision, and action. |
| **InsightIDR** | Rapid7's SIEM and detection/response product, covered by the Certified Specialist exam. |
| **InsightVM** | Rapid7's vulnerability management product, covered by the Certified **Administrator** exam. |
| **Known-exploited** | A vulnerability with evidence of real-world exploitation; the strongest single reprioritization signal, often outweighing a higher base score. |
| **Precision** | Of the alerts fired, the proportion that were real; low precision trains analysts to ignore the alert entirely. |
| **Recall** | Of the real incidents, the proportion alerted on; optimizing precision alone produces a quiet, blind detection that looks excellent. |
| **Scan engine** | The InsightVM component performing network scans; a blocked or misplaced engine makes unreachable assets report as down, which is visually identical to clean. |
| **UBA** | User behavior analytics — baselining per-user normality to catch compromised credentials; weak on new users, novel-but-benign activity, and slow attackers. |
| **Vulnerability Management Lifecycle** | Rapid7's four-stage framing — **Discovery → Analyze → Communicate → Remediate** — which structures Chapters 03–05. |
