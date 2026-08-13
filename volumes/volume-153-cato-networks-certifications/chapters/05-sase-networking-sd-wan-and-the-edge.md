# Chapter 05: SASE Networking — SD-WAN and the Edge

## Learning Objectives

- Explain SD-WAN and the problem it solves versus MPLS.
- Understand how sites, users, and cloud connect to the SASE cloud.
- Describe active-active link use and application-aware routing.
- Recognize networking as the connectivity half of SASE.

*Cert relevance: SD-WAN and edge connectivity are the networking half of SASE — core **SASE Expert** and **Deployment & Management** material.*

## SD-WAN versus MPLS

Traditionally, enterprises connected branch offices with **MPLS** — expensive, private, leased circuits from a carrier, with long provisioning times and rigid capacity. MPLS is reliable but costly and slow to change, and it assumes traffic flows to a central data center (which, post-cloud, it no longer does).

**SD-WAN** (Software-Defined WAN) replaces or augments MPLS by intelligently using **ordinary internet links** (broadband, fiber, LTE/5G) — often *multiple* links per site — with software that decides, per application, which link to use. It gives branches cheaper, faster-to-deploy, higher-bandwidth connectivity, and (crucially for SASE) connects each site directly to the **nearest cloud PoP** rather than backhauling to a data center. In Cato's converged model, SD-WAN is not a separate box but a **function of the same edge** that also does security. The lab models link selection.

## Connecting everything to the cloud

SASE networking connects **all** the enterprise's entities to the converged cloud:

- **Sites** — a lightweight edge device (Cato Socket) at each branch connects it to the nearest PoP over its internet links.
- **Mobile/remote users** — a client on the laptop/phone connects the user to the nearest PoP from anywhere.
- **Cloud resources** — cloud datacenters and IaaS connect to the PoPs directly.

Once *everything* connects to the same cloud, any-to-any connectivity (site-to-site, user-to-app, site-to-cloud) is **routed and secured through the PoPs** — one network, one security policy, wherever the endpoints are. This is the networking foundation that makes the [security functions (Chapter 6)](06-sase-security-fwaas-swg-casb.md) universal. The lab is covered within the link exercise.

## Active-active links and application awareness

A signature SD-WAN capability is **active-active link usage** with **application-aware routing**. A site with two internet links does not use one as a cold standby; it uses **both actively**, and the SD-WAN continuously measures each link's real-time quality (latency, jitter, loss) and routes **each application over the best link for it** — a real-time voice call over the low-jitter link, a bulk backup over the high-bandwidth one — and **fails over instantly** (sub-second) if a link degrades, without dropping the session.

This delivers **resilience** (a link failure is invisible) and **performance** (each app gets the link it needs) from commodity internet connections — the MPLS-grade reliability at internet cost that is SD-WAN's core value. The lab models it.

## Hands-On Lab

Python models SD-WAN link selection. **Cost:** none.

### Lab 5.1 — Application-aware active-active link selection

**Objective:** Route each application over the best real-time link, with instant failover.

```bash
python3 - <<'EOF'
# a site with two internet links, measured in real time
links = {
  "fiber":     {"latency": 8,  "jitter": 2,  "loss": 0.1, "bandwidth": 500, "up": True},
  "broadband": {"latency": 25, "jitter": 12, "loss": 0.5, "bandwidth": 200, "up": True},
}
# applications with different needs
apps = [
  ("VoIP call",     "low jitter"),      # real-time: needs low jitter/latency
  ("video backup",  "high bandwidth"),  # bulk: needs bandwidth, tolerates jitter
  ("web browsing",  "balanced"),
]
def choose(need, links):
    up = {k: v for k, v in links.items() if v["up"]}
    if not up: return None
    if need == "low jitter":     return min(up, key=lambda k: up[k]["jitter"] + up[k]["latency"])
    if need == "high bandwidth": return max(up, key=lambda k: up[k]["bandwidth"])
    return min(up, key=lambda k: up[k]["latency"])

print("Site with 2 ACTIVE links (fiber + broadband). Route each app to its best link:\n")
for app, need in apps:
    link = choose(need, links)
    print(f"   {app:14} (needs {need:14}) -> {link}")
print("\nBOTH links active (not one on cold standby) — each APP goes over the best link")
print("for ITS needs: VoIP over low-jitter fiber, bulk backup over high-bandwidth,")
print("browsing over lowest-latency. That's APPLICATION-AWARE routing.\n")

# fiber degrades -> instant failover
print("Now fiber's loss spikes (link degrades):")
links["fiber"]["up"] = False
for app, need in apps:
    link = choose(need, links)
    print(f"   {app:14} -> fails over to {link} (sub-second, session preserved)")
print("\nSD-WAN uses commodity internet links ACTIVE-ACTIVE, measures each in real time,")
print("routes each application over the best link for it, and fails over INSTANTLY when")
print("one degrades — without dropping the call/session. That delivers MPLS-grade")
print("reliability + performance at internet cost, which is SD-WAN's whole value. In")
print("Cato's converged model this is the SAME edge that does security — networking and")
print("security are one, not two boxes. This is the connectivity half of SASE.")
EOF
```

**Expected result:** Two active internet links with each application routed over the best one for its needs (VoIP over low-jitter fiber, backup over high-bandwidth), then instant failover when a link degrades. The SD-WAN lesson is application-aware active-active link usage delivering MPLS-grade reliability and performance from commodity internet, as a function of the same converged edge that provides security.

**Negative test:** Using a second internet link only as a cold standby. It sits idle while the primary is congested, and failover drops sessions; active-active application-aware routing uses both links continuously and fails over sub-second without interrupting the session.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] SD-WAN understood as using commodity internet links intelligently, replacing costly, rigid MPLS.
- [ ] Connecting sites (Socket), users (client), and cloud to the nearest PoP understood as the networking foundation.
- [ ] Active-active links and application-aware routing understood — each app on its best link, instant failover.
- [ ] Networking recognized as the connectivity half of SASE, converged with security on the same edge.
