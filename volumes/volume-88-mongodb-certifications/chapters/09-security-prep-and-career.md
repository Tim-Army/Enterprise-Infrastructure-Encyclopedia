# Chapter 09: Security, Prep, and Career

## Learning Objectives

- Enable authentication and role-based access control (RBAC).
- Reason about TLS and encryption at rest.
- Plan certification prep with MongoDB University Learning Paths.
- Map a MongoDB career across the four Associate tracks.
- Complete a walkthrough for each security-and-career topic.

## Theory and Architecture

Security spans all four certifications, and closing the volume. MongoDB authenticates users with
**SCRAM** (username/password) or x.509/LDAP/Kerberos, and authorizes them with **role-based access
control (RBAC)** — built-in roles (`read`, `readWrite`, `dbAdmin`, `userAdmin`, `clusterAdmin`) and
custom roles scoped to databases. Traffic is protected with **TLS**, and data at rest with **encryption**
(the encrypted storage engine or cloud KMS in Atlas). Network isolation (bind IPs, firewalls, Atlas
access lists) limits exposure. For certification, preparation is built on **free MongoDB University**
courses grouped into **Learning Paths** per role; completing a Learning Path earns **50% off** the exam
(free for students/educators). A MongoDB career ladders across the four **Associate** tracks — Developer,
Data Modeler, DBA, and Atlas Administrator — into senior application, data-architecture, and
database-operations roles. This chapter closes with security, prep, and career walkthroughs.

## Design Considerations

**Enable authentication** on every deployment (never run open), and grant **least-privilege** roles —
`readWrite` on one database, not `root`. Require **TLS** for client and internal traffic, and enable
**encryption at rest** for sensitive data. Restrict **network** exposure. For certification, pick the
Learning Path for your role, use the **50% discount**, and re-study when MongoDB releases a new major
version and refreshes the exam objectives.

## Implementation and Automation

The labs create a scoped user with RBAC, reason about TLS/encryption, and plan the certification path and
career — the security and progression the program validates.

## Validation and Troubleshooting

Confirm security and progression:

```text
Auth: SCRAM (or x.509/LDAP/Kerberos); Authz: RBAC built-in roles + custom (scoped to DB)
TLS in transit; encryption at rest (encrypted storage engine / cloud KMS); network isolation
Prep: free MongoDB University Learning Paths per role; complete a path -> 50% off (students free)
Career: Associate Developer / Data Modeler / DBA / Atlas Admin -> senior app/data/DB roles
```

Common pitfalls: running a deployment with **auth disabled** (open database); and granting `root`/`dbOwner`
where `readWrite` suffices — apply least privilege.

## Security and Best Practices

Authentication, least-privilege RBAC, TLS, encryption at rest, and network isolation are the defensive
baseline for **your own** database. Enable them from the start, even in the lab. All work is authorized
administration.

## Hands-On Lab

Security-and-career walkthroughs. **Shared prerequisites** — a MongoDB instance with `mongosh` (admin
access), and `python3`. **Cost:** none.

### Lab 9.1 — Create a least-privilege user (RBAC)

**Objective:** Grant only the needed role.

```javascript
// mongosh (as admin)
db.getSiblingDB("shop").createUser({
  user: "appuser",
  pwd: passwordPrompt(),
  roles: [ { role: "readWrite", db: "shop" } ]
})
db.getSiblingDB("shop").getUser("appuser").roles
```

```text
[ { role: 'readWrite', db: 'shop' } ]
```

**Expected result:** an `appuser` scoped to `readWrite` on the `shop` database only — least privilege.

**Negative test:** grant the application `root`; a compromised app credential owns the whole cluster —
grant `readWrite` on its database only.

**Cleanup:**

```javascript
// mongosh
db.getSiblingDB("shop").dropUser("appuser")
```

### Lab 9.2 — Reason about TLS and encryption at rest

**Objective:** Protect data in transit and at rest.

```python
python3 - <<'PY'
controls = {
  "TLS in transit":     "encrypt client<->server + intra-cluster traffic (certs)",
  "Encryption at rest": "encrypted storage engine / cloud KMS -> disk theft yields ciphertext",
  "Network isolation":  "bindIp / firewall / Atlas access list -> limit who can even connect",
  "Auth + RBAC":        "SCRAM login + least-privilege roles",
}
for k, v in controls.items(): print(f"{k:20}: {v}")
print("Defense in depth: all four together protect your own database")
PY
```

**Expected result:** the layered controls — TLS, encryption at rest, network isolation, and auth/RBAC —
a defense-in-depth baseline.

**Negative test:** rely on a network firewall alone with auth disabled; enable **authentication** and
TLS regardless of network position.

**Cleanup:** none.

### Lab 9.3 — Plan certification and career

**Objective:** Sequence the four Associate tracks.

```python
python3 - <<'PY'
paths = {
  "Associate Developer":     "app building + drivers + aggregation -> senior developer",
  "Associate Data Modeler":  "schema design -> data architect",
  "Associate DBA":           "self-managed ops (indexes/replication/sharding) -> database engineer",
  "Associate Atlas Admin":   "managed cloud ops -> cloud database administrator",
}
for cert, arc in paths.items(): print(f"{cert:24}: {arc}")
print("Prep: free MongoDB University Learning Path per track -> 50% off exam (students free)")
print("Currency: re-study when a new major version refreshes the exam objectives")
PY
```

**Expected result:** the four Associate tracks mapped to career arcs with a free-prep, discounted-exam
plan.

**Negative test:** pay full price without completing a **Learning Path**; complete one to earn the 50%
discount (or a free exam as a student/educator).

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

MongoDB security is authentication (SCRAM/x.509/LDAP) plus least-privilege RBAC, TLS in transit,
encryption at rest, and network isolation — the defensive baseline for every deployment. Certification
prep runs on free MongoDB University Learning Paths (earning a 50% exam discount, or free for
students/educators), laddering the four Associate tracks into senior application, data, and database
careers.

- [ ] I can create a least-privilege user with RBAC.
- [ ] I can reason about TLS and encryption at rest.
- [ ] I can plan certification prep with Learning Paths.
- [ ] I can map a MongoDB career across the four tracks.
- [ ] I completed Labs 9.1–9.3 including each negative test.
