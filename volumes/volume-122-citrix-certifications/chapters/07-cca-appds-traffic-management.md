# Chapter 07: CCA-AppDS-Traffic Management — ADC Administration

## Learning Objectives

- Cover the Traffic Management exam's specific modules: securing the ADC, rewrite/responder/URL transform, content switching, optimization, GSLB, and troubleshooting.
- Drill the CLI shapes the exam's simulations present.
- Complete a walkthrough lab per module.

## The exam in brief

**Certification:** CCA-AppDS via the *Deploy and Manage Citrix ADC 14.x with Traffic Management* exam. 60–70 questions, may include **CLI-environment simulations**, ~10% performance-based, English + Japanese, no prerequisites. **Recommended course:** NS-201 *Citrix NetScaler ADC 14.x Administration* (formerly CNS-225). Foundation modules are in [Chapter 05](05-appds-netscaler-platform-and-load-balancing.md); content-switching and rewrite/responder basics shared with the Gateway exam are in [Chapter 06](06-cca-appds-gateway-secure-remote-access.md) — this chapter adds the TM-specific ground.

## Hands-On Lab

Walkthroughs run against a lab VPX/CPX. **Cost:** none with CPX Express.

### Lab 7.1 — Securing the ADC (securing module)

**Objective:** Lock down management access: AAA for administrators.

```bash
add system user labadmin <password>
bind system user labadmin read-only 100
add system cmdPolicy no_shell DENY "(^shell)|(^shell .*)"
bind system user labadmin no_shell 90
set ns ip 10.150.9.5 -gui SECUREONLY -ssh ENABLED -telnet DISABLED
```

**Expected result:** A scoped administrator (read-only plus an explicit shell deny) and an NSIP that serves HTTPS-only management with telnet off — command policies and per-IP management flags are the securing module's levers; external RADIUS/LDAP/TACACS for admins uses the same policy machinery as user AAA.

**Negative test:** As `labadmin`, try `shell` — denied by the command policy; priority order (lower first) decided it.

**Cleanup:** `rm system user labadmin; rm system cmdPolicy no_shell`.

### Lab 7.2 — URL transform (rewrite/responder/URL-transform module)

**Objective:** Use the third rewriting tool the TM exam adds: URL transformation.

```bash
enable ns feature REWRITE
add transform profile prof_legacy
add transform action act_legacy prof_legacy 100
set transform action act_legacy -reqUrlFrom "http://old.lab.local/(.*)" -reqUrlInto "http://new.lab.local/$1"
add transform policy pol_legacy "HTTP.REQ.HOSTNAME.EQ(\"old.lab.local\")" prof_legacy
bind lb vserver lb_web -policyName pol_legacy -priority 100 -type REQUEST
```

**Expected result:** Requests for the legacy hostname are transparently rewritten to the new one, both request and (with `resUrl*`) response directions — URL transform handles whole-URL translation that rewrite actions would need several policies to express.

**Negative test:** Regex group mismatch (`$2` with one capture group): the transform fails open — transforms need the same regex care as any rewrite.

**Cleanup:** Unbind and remove the transform objects.

### Lab 7.3 — Content switching precedence (content switching module)

**Objective:** Prove rule precedence with overlapping policies.

```bash
add cs vserver cs_tm HTTP 10.150.9.220 80
add cs action act_a -targetLBVserver lb_web
add cs policy pol_path -rule "HTTP.REQ.URL.STARTSWITH(\"/app\")" -action act_a
add cs policy pol_all -rule true -action act_a
bind cs vserver cs_tm -policyName pol_path -priority 100
bind cs vserver cs_tm -policyName pol_all -priority 200
show cs vserver cs_tm
```

**Expected result:** `/app` requests hit `pol_path` (priority 100) even though `pol_all` also matches — priority order, lowest number first, is the entire precedence model; a default LB vserver (`-lbvserver`) catches what no policy claims.

**Negative test:** Swap the priorities; the catch-all now shadows the specific rule — the exam's favorite content-switching trap.

**Cleanup:** Remove the CS lab objects.

### Lab 7.4 — Optimization (optimization module)

**Objective:** Enable compression and front-end optimization deliberately.

```bash
enable ns feature CMP
set cmp parameter -cmpLevel optimal
add cmp policy pol_cmp_text -rule "HTTP.RES.HEADER(\"Content-Type\").CONTAINS(\"text\")" -resAction COMPRESS
bind lb vserver lb_web -policyName pol_cmp_text -priority 100 -type RESPONSE
show cmp policy pol_cmp_text
```

**Expected result:** Text responses leave compressed (verify `Content-Encoding: gzip` from a client); binary types stay untouched by the rule — selective compression is the module's pattern, with front-end optimization (minify/inline) as the HTML-specific extension.

**Negative test:** Compress everything (`-rule true`) and watch already-compressed content (images) burn CPU for nothing — the module is about *selective* optimization.

**Cleanup:** Unbind and remove the compression policy.

### Lab 7.5 — Global server load balancing (GSLB module)

**Objective:** Build the two-site GSLB skeleton.

```bash
enable ns feature GSLB
add gslb site site_a 10.150.9.5 -publicIP 203.0.113.5
add gslb site site_b 198.51.100.5 -publicIP 198.51.100.5
add gslb vserver gv_web HTTP -lbMethod ROUNDROBIN
add gslb service svc_a 203.0.113.100 HTTP 80 -siteName site_a
add gslb service svc_b 198.51.100.100 HTTP 80 -siteName site_b
bind gslb vserver gv_web -serviceName svc_a
bind gslb vserver gv_web -serviceName svc_b
bind gslb vserver gv_web -domainName www.lab.example -TTL 30
show gslb vserver gv_web
```

**Expected result:** A GSLB vserver answering DNS for `www.lab.example` with site-aware answers; the **Metric Exchange Protocol (MEP)** between sites carries health and load so a dead site's answers disappear — DNS-based, not proxy-based, distribution: the module's key distinction.

**Negative test:** Break MEP (block 3011 between sites): each site keeps answering with only local knowledge — GSLB degrades to static DNS, which the exam expects you to recognize.

**Cleanup:** Remove the GSLB lab objects.

### Lab 7.6 — Monitoring with SNMP and AppFlow (troubleshooting module)

**Objective:** Ship health and flow telemetry off the box.

```bash
add snmp trap generic 10.150.0.50 -communityName lab
add snmp manager 10.150.0.50
enable ns feature AppFlow
add appflow collector col_lab -IPAddress 10.150.0.60 -port 4739
add appflow action act_flow -collectors col_lab
add appflow policy pol_flow true act_flow
bind lb vserver lb_web -policyName pol_flow -priority 100 -type REQUEST
```

**Expected result:** SNMP traps head to the manager and per-transaction AppFlow (IPFIX) records reach the collector — `ns.log`, SNMP, and AppFlow are the TM exam's monitoring trio; `stat lb vserver lb_web` confirms counters locally.

**Negative test:** Collector unreachable: AppFlow queues then drops silently; `show appflow collector` is where you look — telemetry needs its own monitoring.

**Cleanup:** Remove the SNMP/AppFlow lab objects.

## Summary and Completion Checklist

- [ ] Management-plane hardening with command policies drilled.
- [ ] URL transform, CS precedence, and selective compression built.
- [ ] GSLB two-site skeleton and MEP behavior exercised; SNMP/AppFlow shipped.
