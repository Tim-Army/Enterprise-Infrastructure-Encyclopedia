# Volume CXLII — Glossary

| Term | Definition |
|:---|:---|
| **Access** | Cloudflare's ZTNA: per-application, per-request decisions over identity, device posture, and context. A stolen password meets policies that also demand signals a password thief does not hold. |
| **Accreditation (Cloudflare)** | A partner course-completion credential (Sales Professional, Sales Engineer, Configuration Engineer, Services Architect, Workers Developer in development) — distinct from the proctored certification exams, and not interchangeable with them on a résumé. |
| **Anycast** | Announcing the same IPs from every data center, so BGP delivers each user — and each attack source — to the nearest edge site. One mechanism producing both low latency and structural attack distribution. |
| **API Shield** | API protection: discovery of endpoints actually receiving traffic, OpenAPI schema validation at the edge (positive security), and mutual TLS for client authentication. |
| **Application Security Associate** | One of Cloudflare's two certification exams, covering the WAF/DDoS/bot/API family. Hands-on experience "highly recommended"; mechanics unpublished at verification. |
| **Bot score** | A 1 (automated) to 99 (human) signal attached to each request — evidence for rules, not a verdict. Thresholds are set per endpoint by consequence, watching both challenged-humans and passed-bots columns. |
| **Challenge** | The WAF's middle action between log and block: friction a human passes in seconds and most automation does not. Converts "not sure" from a blocking decision into a cheaper one. |
| **`cloudflared` (Tunnel)** | The daemon that connects an origin *out* to the edge, closing all inbound ports. Removes the origin-IP exposure class entirely — and becomes critical infrastructure itself: replicas on different hosts, heartbeat in the paging path. |
| **Durable Object** | A single-instance coordination point with storage — strong consistency for counters, locks, and sessions, at the cost of every request traveling to the one authoritative copy. |
| **Gateway** | The secure web gateway for egress: DNS filtering (cheap, shallow, deploy first), network rules, and HTTP inspection (deep, requires TLS interception and a governed exception list). |
| **Gray-cloud leak** | A DNS-only record publishing the origin's real IP, letting attackers bypass the WAF entirely. Remediation includes rotating the origin IP — history already recorded the old one. |
| **Isolate** | The V8 execution unit behind Workers: millisecond creation inside an already-resident runtime, deployed to every edge location. Removes both cold starts and the region-selection question. |
| **KV** | Eventually consistent key-value storage read everywhere. The propagation window is a contract: fine for flags, wrong for counters, kill switches, and read-after-write. |
| **Managed rulesets** | Cloudflare-maintained WAF rules for known attack classes, deployed through the log → challenge → block ladder with precision measured on your traffic first. |
| **Proxy toggle** | The per-record choice between proxied (through the edge; all protections apply) and DNS-only (direct to origin; the record publishes the origin address). |
| **Rate limiting** | Threshold-per-key-per-window control, derived from measured legitimate p99 with margin. Keys should identify actors, not networks; login endpoints get strict rules keyed on IP *and* username. |
| **Schema validation** | Enforcing an API contract at the edge: requests outside the schema never reach the origin. Positive security — its false positive is the stale schema, which is why discovery and currency precede enforcement. |
| **Service token** | A client ID/secret for non-human access to Access-protected apps. One per consumer, minimally scoped, rotated on calendar, owned by a team — the audit that catches the unowned two-year-old token scoped to `admin`. |
| **Shadow API** | An endpoint receiving traffic that appears in no schema and no documentation. Found only by reconciling observed traffic against the documented inventory — the API-layer twin of the gray-cloud audit. |
| **Tunnel** | See `cloudflared`. |
| **University Pass (Connect 2026)** | The $495 add-on: a training day plus one attempt at both certification exams, in-person proctored, October 19–21 2026 in San Francisco. The only published exam pricing at verification. |
| **WARP** | The device client: on-ramp to Gateway and source of device-posture signals for Access. Unknown posture fails closed — a device that cannot be evaluated cannot claim compliance. |
| **Workers** | Edge compute in isolates at every location. Placement rule: compute next to what it talks to most — user-facing logic at the edge, data-chatty logic at the origin, split when both. |
| **Zero Trust Associate** | The second certification exam, covering the Access/Gateway/WARP/Tunnel family. Mechanics unpublished at verification. |
