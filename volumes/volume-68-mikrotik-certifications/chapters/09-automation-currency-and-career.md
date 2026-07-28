# Chapter 09: Automation, Currency, and Career Paths

## Learning Objectives

- Automate RouterOS with the REST API, scripting, and Ansible.
- Explain MikroTik certificate validity and recertification.
- Track program change, including RouterOS v7 and the newer certificates.
- Plan a MikroTik certificate path and relate it to the encyclopedia's volumes.
- Verify program currency from the authoritative source.

## Theory and Architecture

RouterOS is automatable several ways. **RouterOS v7** adds a **REST API** (`/rest/...` over HTTPS)
returning JSON, alongside the long-standing binary **API** and **RouterOS scripting** (its own
language for on-box automation, scheduler, and event scripts). Off-box, **Ansible** (the
**`community.routeros`** collection) configures RouterOS declaratively, and RouterOS v7's
**container** feature can even run helper workloads on the router. The **CHR** (Cloud Hosted
Router) provides a free RouterOS VM for lab automation and CI. On the program side, MikroTik
certificates are **valid three years** and the program evolves — **RouterOS v7** changed routing
syntax (OSPF, BGP), and newer certificates (**MTCSWE**, **MTCIPv6E**, **MTCEWE**) have been added.
Confirm the current certificates and RouterOS version on mikrotik.com.

## Design Considerations

Prefer the **REST API** (v7) and **Ansible `community.routeros`** for repeatable configuration from
a Git source of truth; use **RouterOS scripting** for on-box automation and scheduling. Test on
**CHR** before hardware. Plan certificates by role from **MTCNA** up, and recertify before the
three-year expiry.

## Implementation and Automation

The labs use the REST API, RouterOS scripting, and verify the current program.

## Validation and Troubleshooting

Confirm the automation and currency facts:

```text
Automation: REST API (v7, /rest, JSON) + binary API + RouterOS scripting + Ansible community.routeros
  + v7 container feature. Lab on CHR (free VM).
Program: certificates valid 3 years; RouterOS v7 changed routing syntax; MTCSWE/MTCIPv6E/MTCEWE newer.
```

Common pitfalls: automating via scraped CLI where the **REST API** returns JSON; and studying **v6
syntax** for v7 routing.

## Security and Best Practices

Secure the **REST/binary API** (HTTPS, restrict access, least-privilege users), keep config in
**Git** and push via **Ansible**, and test on **CHR** first. Recertify on time and track RouterOS
releases. Automate configuration — defensively.

## References and Knowledge Checks

- mikrotik.com/training: the certificate program, schedule, and validity.
- help.mikrotik.com: RouterOS v7, the REST API, and scripting.
- Related encyclopedia volumes: NetBox (LII), Python for Network Engineers (LVIII), Ansible (LIX).

**Knowledge checks**

1. What automation interfaces does RouterOS v7 offer?
2. How long are MikroTik certificates valid?
3. What path suits an ISP engineer?

## Hands-On Lab

Automation and currency walkthroughs. **Shared prerequisites for Labs 9.1–9.3** — a RouterOS v7
node (CHR) with the REST service enabled, `curl`, and `python3`, in a lab. **Cost:** none.

### Lab 9.1 — Use the RouterOS REST API

**Objective:** Read configuration as JSON.

```bash
curl -sk -u "admin:" "https://10.0.0.1/rest/ip/address" 2>/dev/null \
  | python3 -c "import sys,json;d=json.load(sys.stdin);print('IP addresses via REST:', len(d))" 2>/dev/null \
  || echo "RouterOS v7 REST API: GET https://<router>/rest/ip/address returns JSON"
```

**Expected result:** the IP addresses from the **REST API** as JSON — RouterOS v7 is programmable.

**Negative test:** screen-scrape CLI output for automation; the **REST API** returns structured
JSON — use it.

**Cleanup:** none (read-only).

### Lab 9.2 — RouterOS scripting

**Objective:** Automate on-box with a script.

```text
/system script add name=log-clients source={
  :foreach lease in=[/ip dhcp-server lease find] do={
    :log info ("lease: " . [/ip dhcp-server lease get $lease address])
  }
}
/system script run log-clients
/log print where topics~"info"
```

**Expected result:** a **RouterOS script** iterating DHCP leases and logging them — on-box
automation.

**Negative test:** do repetitive tasks by hand; **scripting + scheduler** automate them — script
it.

**Cleanup:** `/system script remove log-clients`.

### Lab 9.3 — Verify the current program

**Objective:** Confirm certificates before study or renewal.

```bash
curl -sSL -A "Mozilla/5.0" "https://mikrotik.com/training/about" \
  | grep -oiE 'MTC[A-Z0-9]+|RouterOS' | sort -u
```

**Expected result:** the current certificates and RouterOS — confirming scope.

**Negative test:** rely on an old certificate list; the program **adds certificates** (MTCSWE/
MTCIPv6E/MTCEWE) — verify on mikrotik.com.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

RouterOS v7 is automatable via the REST API, the binary API, RouterOS scripting, and Ansible
(`community.routeros`), tested free on CHR. MikroTik certificates are valid three years, and the
program evolves (v7 routing syntax, new MTCSWE/MTCIPv6E/MTCEWE). Automate via the API/Ansible, plan
from MTCNA up, and verify the current program.

- [ ] I can use the RouterOS REST API.
- [ ] I can write a RouterOS script.
- [ ] I can explain the automation options and CHR.
- [ ] I can verify the current certificates and validity.
- [ ] I completed Labs 9.1–9.3 including each negative test.
