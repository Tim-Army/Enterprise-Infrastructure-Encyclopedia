# Volume CXXI — Glossary

| Term | Definition |
|:---|:---|
| **AHV** | Nutanix's built-in hypervisor; the platform Flow Network Security enforces on — and the only one. |
| **Application security policy** | The FNS whitelist policy type: a secured application group (by category) with the inbound/outbound flows it may use; everything else to it is denied. |
| **Apply mode** | The enforcing state of an FNS policy — the policy drops what it does not permit, unlike monitor mode. |
| **Category** | A key:value label on a VM (`AppTier: web`, `Environment: corp`). Categories are Flow's entire policy language: rules name categories, never addresses. |
| **Flow Network Security (FNS)** | Nutanix's platform-native microsegmentation for AHV: category-driven policy enforced by every AHV host at the virtual switch, managed in Prism Central, licensed per node. |
| **Forensic quarantine** | The quarantine mode that leaves a compromised VM reachable only by designated forensic tools, so responders can examine a live machine that cannot reach anything else. |
| **Isolation policy** | The FNS policy type forbidding all communication between two categories, outranking application policy. |
| **Monitor mode** | The observe-only state of an FNS policy: every flow the policy would allow or block is visualized, and nothing is dropped. The built-in first half of observe-then-enforce. |
| **nftables bridge family** | The Linux firewall family that filters bridged (L2-forwarded) traffic — the Track 2 stand-in for the AHV virtual switch's enforcement point. |
| **Policy precedence** | Flow's fixed ordering: quarantine beats isolation beats application. The lab models it with rule position: quarantine at the top, isolation next, application permits below. |
| **Prism Central** | The Nutanix management plane holding categories, security policies, and flow visibility for every cluster it manages. Flow policy does not replicate between Prism Central instances — the DR constraint this volume drills. |
| **Quarantine policy** | The built-in FNS policy that removes a VM's connectivity in one category assignment — strict (nothing) or forensic (forensic tools only) — overriding every permit, including established sessions. |
| **Security Central** | Nutanix's SaaS security-posture and flow-analytics service, aggregating visibility across clusters. |
| **Uncategorized VM** | A VM with no category labels: no policy names it, so under applied policy it is default-denied — the model's most common operational ticket, fixed by categorization rather than rule edits. |
| **Virtual switch** | The AHV host's software switch where Flow enforcement happens — beneath every guest, invisible to the workload, and blind to traffic that never crosses it (in-VM activity). |
