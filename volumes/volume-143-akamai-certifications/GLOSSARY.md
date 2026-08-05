# Volume CXLIII — Glossary

| Term | Definition |
|:---|:---|
| **Account Protector** | Akamai's account-abuse defense: detects logins that are credentialed but anomalous against a per-account behavioral baseline — right password, wrong device/location/velocity. |
| **Adaptive Security Engine (ASE)** | App & API Protector's self-tuning WAF engine. Moves the operator's job from writing exceptions to reviewing what the engine decided; adaptive by design, so it must be told which traffic (e.g. pen tests) to exempt from learning. |
| **Akamai Cloud** | The compute/storage cloud grown from the Linode acquisition — positioned as distributed and edge-adjacent, competing for latency-sensitive, distribution-heavy workloads rather than as an everything-cloud. |
| **Akamai Pipeline** | The tool for promoting one property configuration across environments (dev → staging → prod), keeping them provably identical except where deliberately different. |
| **Akamai University: Customer Enablement** | The customer training program: ILT/VILT/custom courses, each earning a Credly badge. Course-is-the-credential — the badge attests completed training, not a proctored exam. |
| **App & API Protector (AAP)** | Akamai's current WAF, successor to Kona Site Defender, with the Adaptive Security Engine and Bot Visibility & Mitigation. A request-level protection layer, distinct from the API Security product. |
| **API Security** | The dedicated product (Noname lineage) providing API discovery, posture assessment, and runtime abuse detection — the inventory/behavior layer the WAF cannot supply. Its Architect credential is Advanced-level. |
| **BOLA** | Broken Object-Level Authorization — a valid authenticated request reading another user's object. Invisible to a WAF (nothing malformed); caught only by a layer that models the API's authorization. |
| **Centra** | The Guardicore management platform: agents/collectors on workloads, the historical flow map, and policy authoring — available SaaS or on-premise (the GCSE On-Premise variant). |
| **Course badge** | A Credly badge earned by completing an Akamai University course. Attests attendance, not exam performance — distinct from the certification tier. |
| **DNS mapping** | Akamai's classic edge-selection method: each DNS lookup is answered with edge servers chosen for that resolver by load, health, and distance. Answers vary and TTLs are short — never hard-code an edge IP. |
| **Flow map** | Centra's visualized history of what actually talks to what. The precondition for segmentation: you cannot safely segment flows you have not mapped. |
| **GCSA / GCSE** | Guardicore Certified Segmentation Administrator (operate the platform) and Engineer (deploy/run the platform) — the intermediate rungs of Akamai's deepest certification ladder, with Advanced and On-Premise variants. |
| **GTM** | Global Traffic Management — intelligent DNS load-balancing and failover across data centers. Real failover time is detection (probe interval × failures) plus TTL drain. |
| **Kona Site Defender (KSD)** | Akamai's previous-generation WAF; its badges persist in the catalog and its rules persist in enterprise runbooks. The AAP lineage. |
| **Label-based policy** | Guardicore's technique: policy written between workload labels (env, app, role, tier) rather than addresses, so it applies automatically to workloads created later. The labeling schema is the examined skill. |
| **Offload** | The fraction of traffic the origin never serves. Byte-weighted, not request-weighted — the number the origin bill and the network see, and the "& Offload" in the Web Performance course title. |
| **Property** | An Akamai delivery configuration built from rules (criteria + behaviors), natively versioned, and activated to the staging network before production. |
| **Site Shield** | Akamai's mechanism for locking an origin to accept traffic only from the edge — the Akamai twin of origin-IP lockdown. Its range list is a feed to automate, not a file to paste. |
| **Staging network** | Real Akamai edges not receiving production traffic, where a property version is tested before production activation. Catches configuration *interactions* that review cannot. |
| **Web Performance & Offload** | The Akamai University course pair whose title encodes the operating philosophy: measure and improve the byte-weighted origin offload, not just page speed. |
