# Chapter 04: MTCTCE — Traffic Control

## Learning Objectives

- Explain the MTCTCE scope and the RouterOS packet flow.
- Filter and mark traffic with the firewall (filter and mangle).
- Shape traffic with simple queues and queue trees.
- Configure the web proxy and address lists.
- Complete a walkthrough for each traffic-control topic.

## Theory and Architecture

**MTCTCE** (Traffic Control Engineer) is about controlling what traffic does inside RouterOS. It
starts with the **packet flow diagram** — the order in which a packet traverses the firewall
(prerouting → input/forward/output → postrouting), NAT, mangle, and queues — because correct
traffic control depends on acting at the right stage. The **firewall filter** permits/denies;
**mangle** marks connections and packets (`mark-connection`, `mark-packet`) so later stages can act
on them; **NAT** translates. **Quality of Service** is delivered by **queues**: **simple queues**
(per-target bandwidth limits) and **queue trees** (hierarchical, using packet marks for granular
shaping and prioritization, often with HTB). MTCTCE also covers the **web proxy** (caching/
filtering HTTP) and **address lists** (dynamic groups for scalable rules). Mastery is knowing
**where** in the flow to mark, match, and shape.

## Design Considerations

Follow the **packet flow** — mark in **mangle prerouting/forward**, then shape in **queues**. Use
**connection marks** first, then **packet marks**, for efficiency. Prefer **queue trees** with
marks for complex QoS, **simple queues** for basic per-user limits. Use **address lists** to keep
rules scalable.

## Implementation and Automation

The labs mark traffic, build simple and tree queues, and use address lists.

## Validation and Troubleshooting

Confirm the traffic-control model:

```text
Packet flow: prerouting -> input/forward/output -> postrouting (+ NAT, mangle, queues).
Mangle: mark-connection then mark-packet. Filter: accept/drop. NAT: translate.
QoS: simple queues (per-target limits) | queue trees (hierarchical, use packet marks, HTB).
Web proxy + address lists. MTCTCE.
```

Common pitfalls: marking packets in the **wrong chain/stage** (no effect); and shaping with a queue
tree but **no packet marks** to match.

## Security and Best Practices

Mark and match at the **correct packet-flow stage**, use **connection+packet marks** for
efficiency, and shape with **queue trees** for fairness. Use **address lists** for scalable,
readable rules. Verify counters to prove rules match.

## Hands-On Lab

MTCTCE walkthroughs. **Shared prerequisites** — a RouterOS node (CHR) passing traffic, in a lab.
**Cost:** none.

### Lab 4.1 — Mark traffic in mangle

**Objective:** Mark a connection and its packets.

```text
/ip firewall mangle add chain=forward protocol=tcp dst-port=443 action=mark-connection new-connection-mark=https-conn
/ip firewall mangle add chain=forward connection-mark=https-conn action=mark-packet new-packet-mark=https-pkt
/ip firewall mangle print stats
```

**Expected result:** HTTPS traffic **connection- and packet-marked** — the basis for shaping.

**Negative test:** mark packets with no **connection mark** first; mark the connection, then packets
— it's efficient and correct.

**Cleanup:** remove the mangle rules.

### Lab 4.2 — Simple queue

**Objective:** Limit a client's bandwidth.

```text
/queue simple add name=guest target=192.168.88.100/32 max-limit=5M/5M
/queue simple print
```

**Expected result:** a **simple queue** capping the client at 5M up/down — per-target rate limit.

**Negative test:** expect fairness with no queue; unshaped traffic can starve others — add a queue.

**Cleanup:** `/queue simple remove guest`.

### Lab 4.3 — Queue tree with marks

**Objective:** Shape by packet mark hierarchically.

```text
/queue tree add name=https-shape parent=global packet-mark=https-pkt max-limit=20M queue=default
/queue tree print
```

**Expected result:** a **queue tree** shaping the marked HTTPS traffic — granular, hierarchical QoS.

**Negative test:** build a queue tree with **no packet mark**; it matches nothing — mark first
(Lab 4.1), then shape.

**Cleanup:** `/queue tree remove https-shape`.

### Lab 4.4 — Address list

**Objective:** Group addresses for scalable rules.

```text
/ip firewall address-list add list=blocked address=203.0.113.0/24
/ip firewall filter add chain=forward src-address-list=blocked action=drop
/ip firewall address-list print
```

**Expected result:** a **blocked** address list referenced by one filter rule — scalable, readable
policy.

**Negative test:** write one rule per address; an **address list** collapses them — use it.

**Cleanup:** remove the filter rule and address list.

### Lab 4.5 — Web proxy

**Objective:** Enable HTTP caching/filtering.

```text
/ip proxy set enabled=yes port=8080
/ip proxy access add dst-host=*.example.com action=deny
/ip proxy print
```

**Expected result:** the **web proxy** enabled with an access rule — HTTP control at the router.

**Negative test:** expect proxy filtering without redirecting traffic to it; also add a NAT
redirect (or set clients) so traffic reaches the proxy.

**Cleanup:** `/ip proxy set enabled=no`.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

MTCTCE covers traffic control via the RouterOS packet flow: mangle marking (connection then
packet), firewall filtering, NAT, and QoS with simple queues and queue trees, plus the web proxy
and address lists. Act at the right flow stage, mark before you shape, and keep rules scalable.

- [ ] I can mark connections and packets in mangle.
- [ ] I can limit bandwidth with a simple queue.
- [ ] I can shape by packet mark with a queue tree.
- [ ] I can use address lists and the web proxy.
- [ ] I completed Labs 4.1–4.5 including each negative test.
