# Chapter 05: ZPA — Zero Trust Access to Private Applications

## Learning Objectives

- Explain **Zscaler Private Access (ZPA)** as VPN-less, zero-trust access that
  connects a user to a single private application, never to the network.
- Describe the ZPA components: **App Connector**, **application segment**,
  **server group**, **segment group**, and the **ZPA Public Service Edge**.
- Explain why App Connectors are **outbound-only** and how that makes private
  apps dark to the internet (no inbound attack surface).
- Build an access policy that grants a user group access to one application by
  identity and posture.
- Diagnose the common ZPA failures: app not reachable, wrong connector, and
  overly broad segments.

## Theory and Architecture

A VPN places a user *on the network*, granting broad reachability and enabling
lateral movement. ZPA inverts this: it brokers a connection between a specific
user and a specific application through the Zero Trust Exchange, and the
application is never exposed to the internet at all. The user reaches an app
they are authorized for; everything else stays invisible.

### The components and the connection flow

- **App Connector** — a lightweight software connector deployed *beside* the
  private apps (in the data center or cloud VPC). It makes **only outbound**
  connections to the ZPA Public Service Edge; it never listens for inbound
  connections.
- **ZPA Public Service Edge** — the broker in the exchange that stitches the
  user's inbound session to the connector's outbound session.
- **Application segment** — the definition of an app: its FQDNs/IPs and ports.
- **Server group** — the connectors that can reach that app.
- **Segment group** — a grouping of application segments for policy.

The flow: the user (via Client Connector) requests an app → the Public Service
Edge authenticates and checks access policy → it signals a suitable App
Connector to dial *out* to the app → the two outbound sessions are stitched. The
app never sees an inbound connection from the internet; there is no listening
port to attack, no inbound firewall hole, and no network membership granted.

### Why outbound-only matters

Because the connector only dials out, the private application has **no inbound
attack surface** — it is dark. This is the structural security win over a VPN or
a published reverse proxy: an attacker cannot reach an app they are not
authorized for because there is nothing listening to reach.

## Design Considerations

- **Segment narrowly.** An application segment spanning a whole subnet
  recreates VPN-style broad reachability. Define apps as tightly as possible —
  specific FQDNs and ports — so access maps to one app.
- **Place connectors close to apps.** Connectors belong next to the workloads
  (per data center, per VPC) so the outbound leg is short and health is local;
  size them for availability (more than one per server group).
- **Policy is identity-first.** Access rules reference user/group and posture,
  not IP — the point is that reachability follows identity.

## Implementation and Automation

### Defining an application and access (portal shape)

```text
# ZPA Portal:
#   App Connector Group "DC-East" (connectors beside the apps)
#   Server Group "DC-East-Servers" -> App Connector Group DC-East
#   Application Segment "HR-App": domains=hr.internal.example.com, tcp/443 -> Server Group DC-East-Servers
#   Access Policy: Allow  user group "HR"  ->  Segment Group containing HR-App  (posture required)
```

### Verifying a connector is outbound-only

```bash
# On the App Connector host, it should hold OUTBOUND sessions to the ZPA cloud
# and LISTEN on nothing inbound for app traffic:
ss -tnp 2>/dev/null | grep -i estab | grep -E 'zpa|443' | head
echo "--- inbound listeners (should be none for app brokering) ---"
ss -tlnp 2>/dev/null | grep -vE '127.0.0.1|::1' | head
```

### The API shape

```bash
# ZPA API (authenticate for your tenant first):
#   GET /mgmtconfig/v1/admin/customers/{id}/application  -> application segments
#   GET .../appConnectorGroup                            -> connector groups
echo "ZPA config is fully API-driven (also a Terraform provider) for automation"
```

## Validation and Troubleshooting

- **App not reachable.** Check the chain: is a healthy connector in the server
  group bound to the segment? Does the access policy allow this user group? Is
  the FQDN inside the segment definition?
- **Reachable but too much is reachable.** The application segment is too broad
  (a subnet or wildcard) — tighten it to specific FQDNs/ports.
- **Connector unhealthy.** Connectors dial out to the ZPA cloud; a blocked
  outbound path (firewall/proxy) makes them unhealthy — they need outbound
  443, not inbound rules.

## Security and Best Practices

- **Keep apps dark** — never publish a private app inbound "as a shortcut";
  the outbound-only connector model is the entire security value.
- **One app per segment where practical** so a grant of access is a grant to
  one application, not a subnet.
- **Require posture** in the access policy so a compromised or non-compliant
  device cannot reach sensitive apps (Chapter 06).

## References and Knowledge Checks

### References

- Zscaler Help Portal — *Private Access (ZPA): App Connectors, Application
  Segments, Server Groups, Access Policy* (`help.zscaler.com`).
- Zscaler ZPA API and Terraform provider documentation.

### Knowledge Checks

- Why does connecting a user to an application (not the network) prevent
  lateral movement that a VPN allows?
- Why are App Connectors outbound-only, and what attack surface does that
  remove?
- What are the roles of application segment, server group, and segment group?
- How does an over-broad application segment undermine the zero-trust model?

## Hands-On Lab

This chapter's labs cover ZPA — defining an application, the access chain, and
verifying the outbound-only connector model. Portal/API steps reference a ZPA
tenant; the connector check runs locally on a connector host. Each ends
**`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 5.1–5.3** — a ZPA tenant for portal steps;
shell access to an App Connector host for the outbound check. **Cost:** none.

### Lab 5.1 — Define an application segment and access (Topic: Private access)

**Objective:** Grant one group access to one app.

```text
# ZPA Portal:
#   Application Segment "HR-App": hr.internal.example.com tcp/443 -> Server Group DC-East
#   Access Policy: Allow user group "HR" -> Segment Group(HR-App)
```

**Expected result:** members of "HR" reach `hr.internal.example.com` and nothing
else; other users cannot reach it at all — ZPA connects an authorized user to a
single application through the exchange, so access follows identity and the app
is not a network destination.

**Negative test:** define the segment as the whole `10.0.0.0/8` subnet;
"HR" now reaches every host in the range — a broad segment recreates VPN-style
reachability and breaks least privilege.

**Cleanup:** remove the lab segment/policy.

### Lab 5.2 — Verify the connector is outbound-only (Topic: Dark apps)

**Objective:** Confirm no inbound attack surface.

```bash
# On the App Connector host:
echo "== outbound sessions to ZPA cloud (expected) =="
ss -tnp 2>/dev/null | grep -i estab | grep 443 | head
echo "== non-loopback inbound listeners for app brokering (expected: none) =="
ss -tlnp 2>/dev/null | grep -vE '127.0.0.1|::1' | grep -v ':22 ' | head
```

**Expected result:** the connector shows **outbound** established sessions to
the ZPA cloud and **no inbound listeners** brokering app traffic — the connector
only dials out, so the private app has no inbound port to attack and is dark to
the internet, the structural advantage over a VPN or published reverse proxy.

**Negative test:** publish the app with an inbound listener/reverse proxy "to
save a hop"; it now has an internet-facing attack surface — the outbound-only
model is exactly what you would be discarding.

**Cleanup:** none (read-only).

### Lab 5.3 — Trace the access chain (Topic: Troubleshooting)

**Objective:** Reason through why an app is or is not reachable.

```text
# Walk the chain for a failing app:
#   1. FQDN inside an application segment?      (segment definition)
#   2. Segment bound to a server group?         (server group)
#   3. Healthy connector in that server group?  (connector health, outbound 443)
#   4. Access policy allows this user group?    (policy + posture)
```

**Expected result:** the first broken link explains the failure — ZPA
reachability is a chain (segment → server group → healthy connector → access
policy), and troubleshooting means checking each link in order rather than
guessing.

**Negative test:** assume a reachability problem is a network route; in ZPA
there is no route to the app — it is brokered, so the fault is always a link in
the segment/connector/policy chain.

**Cleanup:** none.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

ZPA replaces the VPN with brokered, per-application access: an outbound-only App
Connector beside the app, an application segment defining it, a server group and
access policy binding identity to it, and the Public Service Edge stitching the
two outbound sessions. The app is dark to the internet, access follows identity,
and troubleshooting walks the segment→connector→policy chain.

- [ ] Can define an application segment and a group-scoped access policy.
- [ ] Has verified a connector is outbound-only with no inbound listeners.
- [ ] Can walk the ZPA reachability chain to isolate a failure.
- [ ] Understands why narrow segments preserve least privilege.
