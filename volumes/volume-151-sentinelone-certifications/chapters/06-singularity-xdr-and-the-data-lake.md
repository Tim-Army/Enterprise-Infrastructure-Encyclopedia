# Chapter 06: Singularity XDR and the Data Lake

## Learning Objectives

- Explain XDR — extended detection across endpoint, identity, cloud, and network.
- Understand cross-surface correlation of a single attack.
- Place the Singularity Data Lake and AI SIEM for log analytics at scale.
- Recognize the value of ingesting third-party telemetry.

*Cert relevance: XDR and the Data Lake extend the endpoint story to the whole environment — advanced **THP** and administration territory.*

## From EDR to XDR

**EDR** ([Chapter 4](04-detection-and-response-edr-workflows.md)) sees the **endpoint**. But modern attacks cross surfaces: an attacker phishes a **credential** (identity), uses it to access a **cloud** workload, pivots across the **network**, and lands on an **endpoint**. Each surface sees only its slice, and a single-surface tool cannot connect them.

**XDR** (Extended Detection and Response) extends detection and the [Storyline (Chapter 3)](03-storyline-autonomous-correlation.md) correlation **across all these surfaces** — **Singularity Endpoint**, **Identity**, **Cloud**, and network telemetry — into *one* cross-surface attack story. The signin from an unusual location (identity), the cloud API call it made (cloud), and the process it spawned on a workstation (endpoint) become **one correlated narrative** instead of three disconnected alerts in three consoles. The lab models cross-surface correlation.

## The Singularity Data Lake and AI SIEM

Correlating across surfaces at enterprise scale needs a place to put and query **all the security telemetry** — which is the **Singularity Data Lake** (built on SentinelOne's Scalyr-derived high-speed log analytics). It ingests security data from across the environment, retains it, and makes it **fast to query** for hunting and investigation.

Layered on the Data Lake is the **AI SIEM** — SentinelOne's move to replace the legacy SIEM. A traditional SIEM is a separate, expensive, slow log-aggregation product that a SOC bolts on. SentinelOne's pitch is a SIEM built *on* the same platform and data lake, **AI-driven** and fast, so detection, hunting, and correlation happen in one place rather than shipping endpoint data to a separate SIEM. This is a strategic direction (competing with [Splunk (XLV)](../../volume-045-splunk-certifications/README.md), Microsoft Sentinel) and increasingly certification-relevant.

## Ingesting third-party telemetry

Crucially, the Data Lake / AI SIEM ingests **third-party telemetry** too — firewall logs, cloud provider logs, other security tools — not just SentinelOne's own. This matters because no single vendor sees everything: XDR is most powerful when it correlates SentinelOne's deep endpoint telemetry *with* the network firewall's logs *and* the cloud's audit trail. Being able to bring in and correlate other sources is what makes the platform a **SOC hub** rather than just an endpoint tool. The lab is covered within the cross-surface exercise.

## Hands-On Lab

Python models cross-surface XDR. **Cost:** none.

### Lab 6.1 — Cross-surface correlation of one attack

**Objective:** Connect events across identity, cloud, and endpoint into one story.

```bash
python3 - <<'EOF'
# events across DIFFERENT surfaces, each alone looks minor; together = one attack
EVENTS = [
  # surface,    event,                                         actor
  ("identity",  "login for user jdoe from new country (Nigeria)", "jdoe"),
  ("identity",  "MFA satisfied via SIM-swapped phone",           "jdoe"),
  ("cloud",     "jdoe's token lists all S3 buckets",             "jdoe"),
  ("cloud",     "jdoe's token downloads 'customer-db-backup'",   "jdoe"),
  ("endpoint",  "jdoe's laptop: powershell exfil to paste site", "jdoe"),
  ("network",   "unrelated: guest wifi DHCP renew",              "guest"),
]
print("SINGLE-SURFACE view (three separate tools, three consoles):")
print("   identity tool: 'unusual login' — maybe just travel? low priority.")
print("   cloud tool:    'bucket listed + downloaded' — jdoe has access, looks normal.")
print("   endpoint tool: 'powershell network connection' — common, low priority.")
print("   -> EACH tool sees a minor, dismissible event. NONE sees the attack.\n")

print("XDR cross-surface correlation (one Storyline across surfaces, by actor 'jdoe'):")
attack = [e for e in EVENTS if e[2] == "jdoe"]
for surface, event, actor in attack:
    print(f"   [{surface:9}] {event}")
print("\n   -> ONE narrative: new-country login + SIM-swap MFA (identity) -> lists &")
print("      downloads the customer DB (cloud) -> exfiltrates via PowerShell (endpoint).")
print("      This is a full account-takeover + data-exfil attack — obvious when the")
print("      surfaces are CORRELATED, invisible when they're siloed.")
print("\nThe unrelated guest-wifi event stays out of the story (different actor).\n")
print("The XDR lesson: modern attacks CROSS surfaces (identity -> cloud -> endpoint),")
print("and each single-surface tool sees only a minor, dismissible slice. Extending")
print("Storyline correlation ACROSS surfaces — on the Singularity Data Lake, ingesting")
print("SentinelOne AND third-party telemetry — turns three ignorable alerts into one")
print("undeniable attack story. That's why XDR + the data lake matter: the attack is")
print("only visible in the correlation.")
EOF
```

**Expected result:** Three surfaces each seeing a minor, dismissible event (unusual login, normal-looking bucket access, common PowerShell connection) that XDR correlates by actor into one undeniable account-takeover-and-exfiltration story. The XDR lesson is that modern attacks cross surfaces and each single-surface tool sees only an ignorable slice — extending Storyline correlation across surfaces on the Data Lake makes the attack visible where siloed tools miss it.

**Negative test:** Running separate endpoint, identity, and cloud tools in separate consoles. Each sees a low-priority event and dismisses it; only cross-surface correlation reveals the account-takeover-and-exfiltration attack spanning all three.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] XDR understood as extending detection and Storyline correlation across endpoint, identity, cloud, and network.
- [ ] Cross-surface correlation understood — connecting a single attack's slices that siloed tools miss.
- [ ] The Singularity Data Lake and AI SIEM placed as scalable log analytics replacing the legacy bolt-on SIEM.
- [ ] Third-party telemetry ingestion recognized as what makes the platform a SOC hub, not just an endpoint tool.
