# Chapter 06: Integration and Messaging Certifications

## Learning Objectives

- Map the integration portfolio: MQ, App Connect Enterprise, API Connect, DataPower, Cloud Pak for Integration, Sterling File Gateway.
- Understand each product's job in an integration estate.
- Complete runnable MQ labs on the free developer container plus design labs for the rest.

## The integration portfolio

| Certification | Catalog code | Product |
|:---|:---|:---|
| Certified MQ v9.4 Administrator - Professional | Cert-C9008900 | IBM MQ (messaging) |
| Certified Developer - App Connect Enterprise v12.0 | Cert-C9005700 | ACE (integration flows) |
| Certified Solution Implementer - API Connect v10.0.3 | Cert-C0002604 | API Connect (API management) |
| Certified DataPower Gateway v10.x Administrator - Professional | Cert-C9008200 | DataPower (security gateway) |
| Certified Cloud Pak for Integration v16.1.0 Solution Architect - Professional | Cert-C9009000 | CP4I (unified integration) |
| Certified Sterling File Gateway v6.2 Administrator - Professional | Cert-C9006500 | Sterling (managed file transfer) |

The estate: **MQ** moves messages reliably, **ACE** transforms and routes between systems, **API Connect** publishes and governs APIs, **DataPower** secures traffic at the edge, **Sterling File Gateway** does managed file transfer, and **Cloud Pak for Integration** packages them on OpenShift. MQ is the runnable anchor via its free developer container.

## Hands-On Lab

**Shared prerequisites** — the free **IBM MQ Advanced for Developers** container (`icr.io/ibm-messaging/mq`); Docker/Podman. Other products are design-level. **Cost:** none.

### Lab 6.1 — Stand up a queue manager (MQ Administrator)

**Objective:** Run MQ — the administrator's foundation.

```bash
docker run -d --name mqlab -e LICENSE=accept -e MQ_QMGR_NAME=QM1 \
  -e MQ_APP_PASSWORD=labpass -p 1414:1414 -p 9443:9443 \
  icr.io/ibm-messaging/mq:latest
sleep 30
docker exec mqlab dspmq
```

**Expected result:** `QMNAME(QM1) STATUS(Running)` — a live queue manager, the object every MQ exam question assumes. The admin exam is about creating, configuring, and troubleshooting these and their objects.

**Negative test:** `docker exec mqlab dspmq` before startup completes shows the QM `STATUS(Starting)` — MQ objects have lifecycle states the exam expects you to read.

**Rollback:** `docker rm -f mqlab` at chapter end.

### Lab 6.2 — Queues and a round-trip message (MQ Administrator)

**Objective:** Define a queue and prove PUT/GET — MQ's whole reason to exist.

```bash
docker exec mqlab bash -c 'echo "DEFINE QLOCAL(LAB.Q) DEFPSIST(YES)" | runmqsc QM1'
docker exec mqlab bash -c 'echo "hello mq" | /opt/mqm/samp/bin/amqsput LAB.Q QM1'
docker exec mqlab /opt/mqm/samp/bin/amqsget LAB.Q QM1 &
sleep 3; kill %1 2>/dev/null
```

**Expected result:** `DEFINE` succeeds; `amqsput` writes the message; `amqsget` reads back `hello mq` — the persistent local queue with a message put and got. `DEFPSIST(YES)` means the message survives a restart, the persistence concept the exam drills.

**Negative test:** Define the queue with `DEFPSIST(NO)`, put a message, restart the QM — the message is gone; persistence is a per-message/queue property, and the exam tests exactly this.

**Rollback:** Removed with the container.

### Lab 6.3 — Channels connect queue managers (MQ Administrator)

**Objective:** Understand the distributed-messaging construct the exam centers on.

```bash
docker exec mqlab bash -c 'echo "DEFINE CHANNEL(LAB.SVRCONN) CHLTYPE(SVRCONN) TRPTYPE(TCP)
DISPLAY CHSTATUS(LAB.SVRCONN)" | runmqsc QM1'
```

**Expected result:** A server-connection channel defined (the channel type client apps connect through) — channels (SVRCONN for clients, sender/receiver pairs between queue managers), listeners, and their status are the distributed-MQ core the admin exam probes.

**Negative test:** A client connecting with no matching SVRCONN channel or wrong auth gets `MQRC_NOT_AUTHORIZED`/`2035` — the single most common MQ ticket, and a favorite exam scenario.

**Rollback:** Removed with the container.

### Lab 6.4 — ACE integration flows (App Connect Enterprise Developer)

**Objective:** State what an ACE message flow does.

```text
ace> a message flow: input node (MQ/HTTP/file) -> transform (mapping/compute/ESQL/Graphical Data Map)
     -> route -> output node; deployed as a BAR file to an integration server
```

**Expected result:** ACE as the transform-and-route engine: flows built from nodes, mapping between formats (XML/JSON/DFDL), deployed as BAR files — the Developer exam tests flow construction, nodes, and message models, distinct from MQ's transport role.

**Negative test:** Using MQ alone to "transform" a message — MQ moves bytes; ACE transforms them. The exam separates transport from mediation.

**Rollback:** None (design).

### Lab 6.5 — API Connect and DataPower (Solution Implementer / DataPower Admin)

**Objective:** Separate API management from the security gateway.

```text
api connect> design/publish APIs, developer portal, plans & rate limits, analytics (the API lifecycle)
datapower> the hardened gateway enforcing the APIs: TLS, threat protection, message security,
           transformation at the edge (API Connect's gateway is DataPower)
```

**Expected result:** The division: **API Connect** governs the API lifecycle (design, portal, plans), **DataPower** is the gateway that enforces at runtime. They pair — API Connect's enforcement point *is* DataPower — but the exams are separate (Solution Implementer vs Administrator).

**Negative test:** Expecting API Connect to do low-level threat protection itself — that is DataPower's job; the two-product split is the design the exams test.

**Rollback:** None (design).

### Lab 6.6 — Cloud Pak for Integration and Sterling (CP4I Architect / Sterling Admin)

**Objective:** Place the platform and the file-transfer specialist.

```text
cp4i (v16.1.0)> the OpenShift-packaged bundle of MQ + ACE + API Connect + DataPower + Event Streams;
                the Solution Architect credential sizes and composes these capabilities
sterling file gateway (v6.2)> managed file transfer: partner onboarding, routing channels, protocols
                (SFTP/FTPS/AS2), governed B2B file exchange
```

**Expected result:** Cloud Pak for Integration as the unified platform (its architect credential composes the integration capabilities on OpenShift) and Sterling File Gateway as the managed-file-transfer specialist — different problem (files/B2B) from the message/API integration above.

**Negative test:** Using MQ or ACE for large partner file exchange with onboarding/non-repudiation — that is Sterling's domain; matching the workload to the product is the architect's job.

**Rollback:** `docker rm -f mqlab` to finish the chapter.

## Summary and Completion Checklist

- [ ] Integration portfolio mapped: MQ, ACE, API Connect, DataPower, CP4I, Sterling.
- [ ] Live MQ: queue manager, persistent PUT/GET, channels drilled (incl. the 2035 scenario).
- [ ] ACE mediation vs MQ transport, and API Connect vs DataPower, separated.
- [ ] CP4I platform role and Sterling's MFT specialty understood.
