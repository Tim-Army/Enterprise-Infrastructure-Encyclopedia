# Chapter 02: ZIA — Secure Web Gateway and TLS Inspection

## Learning Objectives

- Explain the **Zscaler Internet Access (ZIA)** Secure Web Gateway (SWG) as a
  cloud proxy that applies URL, content, and cloud-app policy inline.
- Build a **URL Filtering** policy from URL categories and understand rule
  order and the default block/allow behavior.
- Configure **SSL/TLS inspection** and explain why the Zscaler intermediate
  certificate must be trusted on every endpoint.
- Choose a **traffic-forwarding** method (Client Connector, PAC file, or
  location tunnel) and write a working PAC file.
- Diagnose the two most common SWG failures: an unexpected block and a TLS
  trust error.

## Theory and Architecture

The ZIA Secure Web Gateway is the internet/SaaS data plane of the Zero Trust
Exchange. Every request a forwarded user makes is terminated at the nearest
ZIA service edge, evaluated against policy — URL category, cloud application,
content type, threat verdict, DLP — and only then re-originated to the
destination. Because ZIA is a **forward proxy**, it sees the full URL and, with
TLS inspection enabled, the decrypted payload, which is what lets it enforce
policy that a passthrough firewall cannot.

### URL filtering and categories

Policy is expressed as ordered **URL Filtering** rules matching **URL
categories** (predefined, like *Gambling* or *Malware*, and custom), user and
group, location, and time. Rules are evaluated top-down; the first match wins.
A blocked request receives a Zscaler **end-user notification (block) page**
rather than a silent drop, so the user knows policy — not a network fault —
stopped them.

### TLS/SSL inspection and the trust chain

Most traffic is TLS-encrypted, so without decryption the SWG sees only the
destination host, not the content. **SSL Inspection** makes ZIA the man in the
middle *by policy*: it terminates the client's TLS session presenting a
certificate signed by the **Zscaler intermediate CA**, inspects the plaintext,
then makes its own TLS session to the origin. For the client to trust the
presented certificate, the **Zscaler root/intermediate certificate must be
installed in the endpoint trust store** (pushed by ZCC or by device
management). Without that trust, every inspected site throws a certificate
error — the single most common ZIA rollout problem.

### Traffic forwarding

Traffic reaches ZIA by one of three methods: the **Zscaler Client Connector**
(agent, Chapter 07), a **PAC file** (browser/OS proxy auto-config that sends
matching URLs to the ZIA proxy), or a **location tunnel** (GRE/IPSec from a
site, Chapter 07). A PAC file's `FindProxyForURL(url, host)` returns the proxy
to use — Zscaler for most traffic, `DIRECT` for exceptions.

## Design Considerations

- **Order rules from specific to general.** First-match-wins means a broad
  allow placed above a specific block silently defeats the block.
- **Do not inspect what you must not inspect.** Health, finance, and
  government categories are commonly excluded from TLS inspection by policy for
  privacy/compliance — build SSL-inspection exemptions deliberately.
- **Forwarding method sets the failure mode.** PAC files are easy but
  bypassable; ZCC is enforced but needs deployment. Most enterprises use ZCC
  for roaming users and tunnels for sites.

## Implementation and Automation

### A URL filtering rule (portal + API shape)

```text
# ZIA Admin Portal > Policy > URL & Cloud App Control > URL Filtering:
#   Rule "Block Gambling":  Categories = Gambling; Users = All; Action = Block
#   Rule order: place above any broad "Allow" rule (first match wins)
```

```bash
# ZIA API verification (authenticate first per your cloud's API base):
#   GET /api/v1/urlFilteringRules  -> lists rules in evaluation order
curl -s -b cookie.txt "https://zsapi.<cloud>/api/v1/urlFilteringRules" \
  | python3 -c "import json,sys; [print(r['order'], r['name'], r['action']) for r in json.load(sys.stdin)]"
```

### Verifying TLS inspection from the endpoint

```bash
# With SSL inspection ON, the leaf certificate is issued by the Zscaler
# intermediate, not the site's real CA:
openssl s_client -connect example.com:443 -servername example.com </dev/null 2>/dev/null \
  | openssl x509 -noout -issuer
```

### A minimal PAC file

```javascript
// forward.pac — send everything to ZIA except an internal exception
function FindProxyForURL(url, host) {
    if (isPlainHostName(host) || dnsDomainIs(host, ".internal.example.com"))
        return "DIRECT";
    return "PROXY gateway.zscaler.net:80; DIRECT";
}
```

## Validation and Troubleshooting

- **Unexpected block.** Read the block page — it names the rule and category.
  If the category is wrong, check the URL's categorization (Zscaler publishes a
  lookup) and rule order.
- **Certificate errors everywhere.** The Zscaler intermediate is not trusted on
  the endpoint — deploy it via ZCC/MDM. This is a trust-store problem, not a
  Zscaler outage.
- **Traffic not proxied at all.** The forwarding method is not active: PAC not
  applied, or ZCC not forwarding — confirm with `ip.zscaler.com` (Chapter 01).

## Security and Best Practices

- **Inspect broadly, exempt narrowly and deliberately.** The value of ZIA is in
  the decrypted inspection; every inspection exemption is a blind spot, so
  justify each one.
- **Deploy the Zscaler certificate before enabling inspection**, not after, or
  you break every HTTPS site at once.
- **Default-deny unknown/high-risk categories** (newly registered domains,
  miscategorized, malware) rather than default-allow.

## References and Knowledge Checks

### References

- Zscaler Help Portal — *Internet & SaaS (ZIA): URL Filtering Policy* and *SSL
  Inspection* (`help.zscaler.com`).
- Zscaler Help Portal — *Forwarding Traffic to the Zscaler Service* (PAC files,
  Client Connector, location tunnels).

### Knowledge Checks

- Why can a forward proxy enforce content policy a passthrough firewall cannot?
- What must be true on the endpoint before SSL inspection can be enabled
  without breaking HTTPS?
- In a first-match-wins policy, why does rule order determine behavior?
- Name the three ways traffic is forwarded to ZIA and a trade-off of each.

## Hands-On Lab

This chapter's labs cover the SWG skills — URL policy, TLS inspection and its
trust chain, and PAC-based forwarding. Labs use `curl`, `openssl`, and a small
PAC evaluation; a ZIA tenant is referenced for portal steps but the
verifications run locally. Each ends **`**Lab verified by:** *pending*`** until
a human runs it.

**Shared prerequisites for Labs 2.1–2.3** — `curl`, `openssl`, `python3`.
**Cost:** none.

### Lab 2.1 — Build and test a URL filtering rule (Topic: URL filtering)

**Objective:** Block a category and observe the block page.

```text
# ZIA Portal > Policy > URL & Cloud App Control > URL Filtering:
#   New rule "Block Gambling": Categories=Gambling, Action=Block, above any Allow-all
```

```bash
# From a ZIA-forwarded host, a request to that category returns a Zscaler block page:
curl -sL http://www.example-gambling-category-site.test/ | grep -io "zscaler\|blocked\|not permitted" | head -1
```

**Expected result:** the request to the blocked category returns a Zscaler
end-user notification page (not a silent drop) — URL Filtering is ordered and
first-match-wins, and a block is surfaced to the user so they know policy, not a
network fault, stopped them.

**Negative test:** place a broad "Allow all" rule above the block; the block
never fires — order defeats intent when a general allow precedes a specific
block.

**Rollback:** remove or disable the lab rule.

### Lab 2.2 — Verify TLS inspection and its trust chain (Topic: SSL inspection)

**Objective:** See that an inspected site's certificate is Zscaler-issued.

```bash
openssl s_client -connect example.com:443 -servername example.com </dev/null 2>/dev/null \
  | openssl x509 -noout -issuer -subject
```

**Expected result:** with SSL inspection enabled the **issuer is the Zscaler
intermediate CA** (not the site's public CA) — ZIA terminates and re-originates
TLS by policy, so it can inspect the plaintext; the endpoint trusts the leaf
only because the Zscaler certificate is in its trust store.

**Negative test:** remove the Zscaler certificate from the trust store; every
inspected HTTPS site throws a certificate error — trust must be provisioned
before inspection is enabled.

**Rollback:** none (read-only).

### Lab 2.3 — Write and evaluate a PAC file (Topic: Traffic forwarding)

**Objective:** Route traffic to ZIA with an internal exception.

```bash
cat > forward.pac <<'EOF'
function FindProxyForURL(url, host) {
    if (isPlainHostName(host) || dnsDomainIs(host, ".internal.example.com"))
        return "DIRECT";
    return "PROXY gateway.zscaler.net:80; DIRECT";
}
EOF
# Evaluate the logic without a browser (Node/pactester-style check):
node -e '
const dnsDomainIs=(h,d)=>h.length>=d.length&&h.slice(-d.length)===d;
const isPlainHostName=(h)=>h.indexOf(".")<0;
function FindProxyForURL(url,host){ if(isPlainHostName(host)||dnsDomainIs(host,".internal.example.com")) return "DIRECT"; return "PROXY gateway.zscaler.net:80; DIRECT"; }
console.log("app.internal.example.com ->", FindProxyForURL("https://app.internal.example.com/","app.internal.example.com"));
console.log("www.google.com ->", FindProxyForURL("https://www.google.com/","www.google.com"));
' 2>/dev/null || echo "(node not present; logic: internal->DIRECT, everything else->PROXY)"
```

**Expected result:** internal hosts return `DIRECT` and everything else returns
`PROXY gateway.zscaler.net:80` — a PAC file's `FindProxyForURL` decides
per-request whether traffic goes to the Zscaler proxy or bypasses it, which is
how PAC-based forwarding sends internet traffic to ZIA while letting internal
destinations go direct.

**Negative test:** return `PROXY` for internal hosts too; internal apps get
backhauled through ZIA and may break or add latency — the `DIRECT` exception is
what keeps internal traffic off the proxy.

**Rollback:** `rm -f forward.pac`.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

ZIA's Secure Web Gateway is a cloud forward proxy: it terminates each session,
applies ordered URL and content policy, and — with SSL inspection and its trust
chain in place — enforces on decrypted traffic. Forwarding (ZCC, PAC, or
tunnel) is what puts traffic in front of it, and the two rollout-defining
details are rule order and endpoint trust of the Zscaler certificate.

- [ ] Can build an ordered URL filtering rule and predict first-match behavior.
- [ ] Has verified a Zscaler-issued certificate on an inspected site.
- [ ] Understands why the Zscaler certificate must be trusted before enabling
      inspection.
- [ ] Can write a PAC file that forwards to ZIA with internal exceptions.
