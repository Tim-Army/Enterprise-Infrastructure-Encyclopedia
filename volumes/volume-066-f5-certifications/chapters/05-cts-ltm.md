# Chapter 05: Technology Specialist — LTM

## Learning Objectives

- Explain the CTS LTM specialization (exams 301a and 301b).
- Design load balancing with methods, priority groups, and persistence.
- Write iRules to customize traffic handling.
- Optimize with SSL and OneConnect, and troubleshoot LTM.
- Complete a walkthrough for each LTM topic.

## Theory and Architecture

The **F5 Certified Technology Specialist, LTM** covers Local Traffic Manager in depth across two
exams: **301a** (Architect, Setup, and Deploy) and **301b** (Maintain and Troubleshoot). LTM is
the core application delivery controller. Beyond basic pools, it adds **advanced load balancing**
(dynamic ratio, least connections, observed/predictive), **priority group activation** (bring in
backup members only when the primary group thins), **persistence** (source-address, cookie, SSL,
universal — keeping a client on one server), **iRules** (Tcl scripts that inspect and act on
traffic at events like `HTTP_REQUEST`), and optimization profiles like **OneConnect** (server-side
connection reuse) and **SSL** (offload/re-encrypt). The 301a exam tests **design and deployment**;
301b tests **maintenance and troubleshooting** (health, statistics, packet capture, iRule
debugging). LTM is where F5's full-proxy power is applied to real applications.

## Design Considerations

Pick persistence to match the app (cookie for HTTP, source-address for non-HTTP). Use **priority
groups** for active/standby backends and **OneConnect** to reduce server load. Reach for **iRules**
only when built-in features cannot express the requirement — they are powerful but add
processing. Monitor with application-aware health checks (HTTP receive strings), not just TCP.

## Implementation and Automation

The labs configure persistence, priority groups, an iRule, OneConnect, and troubleshoot LTM.

## Validation and Troubleshooting

Confirm the LTM model:

```text
LB: round robin/least conn/ratio/observed/predictive. Priority group activation for active/standby.
Persistence: source-addr/cookie/SSL/universal. iRules: event-driven Tcl (HTTP_REQUEST, etc.).
Optimize: OneConnect (server conn reuse), SSL offload/re-encrypt. Exams 301a (design/deploy), 301b (maintain/troubleshoot).
```

Common pitfalls: no **persistence** for a stateful app (users bounce between servers); and
**iRules** where a built-in profile would do.

## Security and Best Practices

Use application-aware **monitors**, appropriate **persistence**, and **SSL** handling that meets
policy. Keep iRules minimal and reviewed. Troubleshoot with statistics and captures, not guesswork.
Authorized administration throughout.

## Hands-On Lab

LTM walkthroughs. **Shared prerequisites** — a BIG-IP VE with LTM and the `web_pool`/`web_vs` from
Chapter 03, in an authorized lab. **Cost:** none.

### Lab 5.1 — Cookie persistence

**Objective:** Keep a client on one server.

```bash
tmsh create ltm persistence cookie web_cookie defaults-from cookie
tmsh modify ltm virtual web_vs persist replace-all-with { web_cookie }
tmsh list ltm virtual web_vs persist
```

**Expected result:** **cookie persistence** on the virtual server — a client's session stays on
one member.

**Negative test:** run a stateful app with no persistence; users **bounce** between servers and
lose sessions — add persistence.

**Cleanup:** `tmsh modify ltm virtual web_vs persist none; tmsh delete ltm persistence cookie web_cookie`.

### Lab 5.2 — Priority group activation

**Objective:** Configure active/standby backends.

```bash
tmsh modify ltm pool web_pool members modify { 10.10.30.11:80 { priority-group 10 } 10.10.30.12:80 { priority-group 5 } }
tmsh modify ltm pool web_pool min-active-members 1
tmsh show ltm pool web_pool
```

**Expected result:** the higher-**priority-group** member serves; the lower one activates only if
the active group drops below the minimum — active/standby backends.

**Negative test:** put all members in one priority group expecting standby behavior; use
**priority-group + min-active-members** for active/standby.

**Cleanup:** reset priority-group to 0 on both members.

### Lab 5.3 — Write an iRule

**Objective:** Redirect HTTP to HTTPS.

```tcl
when HTTP_REQUEST {
    if { [TCP::local_port] == 80 } {
        HTTP::redirect "https://[HTTP::host][HTTP::uri]"
    }
}
```

**Expected result:** an **iRule** redirecting HTTP to HTTPS at the `HTTP_REQUEST` event — custom
traffic handling.

**Negative test:** solve everything with iRules; prefer built-in **profiles/policies** and reserve
iRules for what they cannot express.

**Cleanup:** detach and delete the iRule.

### Lab 5.4 — OneConnect optimization

**Objective:** Reuse server-side connections.

```bash
tmsh create ltm profile one-connect web_oneconnect defaults-from oneconnect
tmsh modify ltm virtual web_vs profiles add { web_oneconnect }
tmsh list ltm virtual web_vs profiles
```

**Expected result:** **OneConnect** enabling server-side connection reuse — fewer connections to
the backend, lower server load.

**Negative test:** open a new server connection per client request at scale; **OneConnect** pools
them — enable it for HTTP.

**Cleanup:** remove and delete the OneConnect profile.

### Lab 5.5 — Troubleshoot with statistics (301b)

**Objective:** Diagnose uneven load.

```bash
tmsh show ltm pool web_pool members
tmsh show ltm virtual web_vs | grep -iE "connections|packets"
```

**Expected result:** per-member and virtual-server **statistics** revealing distribution and
health — the 301b troubleshooting view.

**Negative test:** assume load is even without stats; **verify** with per-member counters and
health.

**Cleanup:** none (read-only).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The CTS LTM specialization (301a design/deploy, 301b maintain/troubleshoot) covers advanced load
balancing, priority groups, persistence, iRules, and optimization (OneConnect, SSL). Match
persistence to the app, use priority groups for standby, keep iRules minimal, and troubleshoot
with statistics.

- [ ] I can configure persistence.
- [ ] I can set up priority group activation.
- [ ] I can write a basic iRule.
- [ ] I can enable OneConnect and troubleshoot with stats.
- [ ] I completed Labs 5.1–5.5 including each negative test.
