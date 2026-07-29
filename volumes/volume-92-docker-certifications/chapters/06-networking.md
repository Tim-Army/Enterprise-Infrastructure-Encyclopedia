# Chapter 06: Networking

## Learning Objectives

- Distinguish the built-in network drivers (bridge, host, none, overlay).
- Create a user-defined bridge network with DNS.
- Publish ports from a container.
- Reason about overlay networks for Swarm.
- Complete a walkthrough for each networking topic.

## Theory and Architecture

The **Networking** domain (~15%) covers how containers communicate. Docker networking uses **drivers**:
**bridge** (the default — a private virtual network on the host; containers get an internal IP and reach
the outside via NAT), **host** (the container shares the host's network stack, no isolation, no port
mapping needed), **none** (no networking), **overlay** (a multi-host network spanning a Swarm so
containers on different nodes communicate), and **macvlan** (a container gets its own MAC/IP on the
physical LAN). On a **user-defined bridge** network, Docker provides **automatic DNS** — containers
resolve each other by **name** — which the default bridge does not. To reach a container from outside the
host you **publish** a port with **`-p host:container`** (which NATs host traffic to the container). For
multi-host clustering, **overlay** networks (with an encrypted option) connect services across the Swarm.
Understanding driver choice, port publishing, and container DNS is the domain's core. This chapter teaches
networking with hands-on `docker` walkthroughs.

## Design Considerations

Use **user-defined bridge** networks (not the default bridge) so containers get **DNS** by name and are
isolated per application. **Publish** only the ports you must expose. Use **host** networking only when you
need the host stack (performance/edge cases) and accept the loss of isolation. Use **overlay** for
multi-host Swarm services (Chapter 07), encrypted where required. Segment applications onto separate
networks.

## Implementation and Automation

The labs create a user-defined network with DNS, publish a port, and reason about host and overlay
drivers — the networking the domain validates.

## Validation and Troubleshooting

Confirm networking:

```text
Drivers: bridge (default, private + NAT) | host (share host stack) | none | overlay (multi-host Swarm) | macvlan
User-defined bridge: automatic DNS -> containers resolve each other by NAME (default bridge does not)
Publish: -p host:container NATs external traffic to the container
Overlay: connects services across Swarm nodes (encryptable)
```

Common pitfalls: relying on the **default bridge** and container IPs (no name DNS) — use a **user-defined**
network; and publishing a port to `0.0.0.0` when it should be internal — bind to localhost or keep it
unpublished.

## Security and Best Practices

Segment apps onto separate user-defined networks, publish minimal ports, and use encrypted overlay where
traffic crosses nodes. Network isolation limits blast radius. All work is authorized administration.

## Hands-On Lab

Networking walkthroughs. **Shared prerequisites** — the Docker Engine. **Cost:** none.

### Lab 6.1 — Create a user-defined bridge with DNS

**Objective:** Resolve containers by name.

```bash
docker network create appnet
docker run -d --name db --network appnet redis:alpine
docker run --rm --network appnet busybox nslookup db | grep -A1 Name
```

```text
Name:      db
Address 1: 172.20.0.2 db.appnet
```

**Expected result:** a second container resolving `db` by name over the user-defined network — automatic
DNS.

**Negative test:** put both on the **default bridge** and resolve by name; it fails — use a
**user-defined** network for DNS.

**Cleanup:**

```bash
docker rm -f db && docker network rm appnet
```

### Lab 6.2 — Publish a port

**Objective:** Reach a container from the host.

```bash
docker run -d --name web -p 127.0.0.1:8082:80 nginx:alpine
docker port web
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8082/
```

```text
80/tcp -> 127.0.0.1:8082
200
```

**Expected result:** the container's port 80 published to localhost:8082 — reachable from the host only.

**Negative test:** publish to `0.0.0.0:8082` for an internal service; bind to **`127.0.0.1`** (or leave
unpublished) to avoid exposing it.

**Cleanup:**

```bash
docker rm -f web
```

### Lab 6.3 — Reason about host vs bridge

**Objective:** Choose the right driver.

```python
python3 - <<'PY'
drivers = {
  "bridge (user-defined)": "isolated private net + DNS by name (default choice)",
  "host":                  "share host stack; no port mapping; no isolation (perf/edge)",
  "none":                  "no networking (fully isolated)",
  "overlay":               "multi-host Swarm services",
  "macvlan":               "container gets its own MAC/IP on the physical LAN",
}
for d, use in drivers.items(): print(f"{d:24}: {use}")
PY
```

**Expected result:** each driver matched to its use — user-defined bridge as the default.

**Negative test:** use **host** networking everywhere for convenience; you lose isolation and port
mapping — prefer **bridge**.

**Cleanup:** none.

### Lab 6.4 — Reason about overlay for multi-host

**Objective:** Connect services across nodes.

```python
python3 - <<'PY'
print("Single host: user-defined bridge connects containers on one host")
print("Multiple hosts (Swarm): OVERLAY network spans nodes -> services on node A talk to node B")
print("docker network create -d overlay --opt encrypted app-overlay")
print("Rule: cross-node service communication needs an OVERLAY network (Chapter 07)")
PY
```

**Expected result:** overlay as the driver for cross-node Swarm communication — bridge is single-host.

**Negative test:** expect a bridge network to span hosts; use an **overlay** network for multi-host.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Docker networking uses drivers — bridge (default, private with NAT), host (shared stack), none, overlay
(multi-host Swarm), and macvlan — where user-defined bridge networks add automatic DNS so containers
resolve each other by name, ports are exposed with `-p host:container`, and overlay networks connect
services across Swarm nodes.

- [ ] I can distinguish the network drivers.
- [ ] I can create a user-defined network with DNS.
- [ ] I can publish a port safely.
- [ ] I can reason about overlay for multi-host.
- [ ] I completed Labs 6.1–6.4 including each negative test.
