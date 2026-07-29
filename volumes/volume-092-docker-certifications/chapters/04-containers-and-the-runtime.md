# Chapter 04: Containers and the Runtime

## Learning Objectives

- Explain the container lifecycle.
- Run containers with common options.
- Execute commands and read logs in a running container.
- Apply resource limits, restart policies, and health checks.
- Complete a walkthrough for each container-runtime topic.

## Theory and Architecture

A **container** is a running instance of an image, isolated by Linux **namespaces** (PID, network, mount,
UTS) and constrained by **cgroups** (CPU, memory). Its **lifecycle**: `docker create` prepares it,
`docker start` runs it, `docker stop` sends SIGTERM then SIGKILL, and `docker rm` removes it (`docker run`
does create+start). Common `run` options: **`-d`** (detached), **`-p host:container`** (publish a port),
**`-e`** (environment variable), **`-v`** (mount a volume, Chapter 05), **`--name`**, and
**`--restart`** (restart policy: `no`, `on-failure`, `always`, `unless-stopped`). You interact with a
running container via **`docker exec`** (run a command inside), **`docker logs`** (view stdout/stderr),
and **`docker stats`** (live resource use). **Resource limits** (`--memory`, `--cpus`) cap consumption; a
**`HEALTHCHECK`** (in the image or `--health-cmd`) lets Docker report a container as healthy/unhealthy.
Understanding the lifecycle and these controls is core to operating containers. This chapter teaches the
runtime with hands-on `docker` walkthroughs.

## Design Considerations

Run one **main process per container** (PID 1 should handle signals for clean shutdown). Publish only the
**ports** you need. Set **resource limits** so one container cannot starve the host. Choose a **restart
policy** for resilience (`unless-stopped`/`on-failure`). Add a **health check** so orchestrators (and
you) know a container is actually serving. Prefer **`exec`** to debug over rebuilding.

## Implementation and Automation

The labs run a container with options, exec and read logs, apply resource limits and a restart policy, and
add a health check — the runtime the domain validates.

## Validation and Troubleshooting

Confirm the runtime:

```text
Container = image instance; namespaces (PID/net/mount) + cgroups (cpu/mem) isolation
Lifecycle: create -> start -> stop (SIGTERM->SIGKILL) -> rm; docker run = create+start
run options: -d -p -e -v --name --restart(no/on-failure/always/unless-stopped)
Interact: docker exec (in-container cmd) | docker logs | docker stats; limits --memory/--cpus; HEALTHCHECK
```

Common pitfalls: running **many processes** in one container without an init (zombies, bad signal
handling); and **no resource limits** so a runaway container exhausts the host.

## Security and Best Practices

Limit resources, publish minimal ports, run as a non-root user (Chapter 08), and add health checks.
Least-privilege containers are safer and more reliable. All work is authorized administration.

## Hands-On Lab

Container-runtime walkthroughs. **Shared prerequisites** — the Docker Engine. **Cost:** none.

### Lab 4.1 — Run a container with options

**Objective:** Detached, named, port-published, with env.

```bash
docker run -d --name api -p 9000:80 -e GREETING=hi --restart unless-stopped nginx:alpine
docker ps --format '{{.Names}}\t{{.Ports}}\t{{.Status}}'
```

```text
api   0.0.0.0:9000->80/tcp   Up 2 seconds
```

**Expected result:** a detached, named container publishing port 9000 with a restart policy.

**Negative test:** run it foreground without `-d` and lose the terminal; use **`-d`** for services.

**Cleanup:** (removed at the end of Lab 4.4).

### Lab 4.2 — Exec and read logs

**Objective:** Inspect a running container.

```bash
docker exec api sh -c 'echo $GREETING; nginx -v'
docker logs --tail 2 api
```

```text
hi
nginx version: nginx/1.27.0
... "GET / HTTP/1.1" 200 ...
```

**Expected result:** `exec` running a command inside the container and `logs` showing its output — live
inspection.

**Negative test:** rebuild the image to add a debug echo; use **`docker exec`** to inspect a running
container.

**Cleanup:** none yet.

### Lab 4.3 — Apply resource limits

**Objective:** Cap CPU and memory.

```bash
docker update --memory 256m --cpus 0.5 api
docker inspect api --format 'mem={{.HostConfig.Memory}} cpus={{.HostConfig.NanoCpus}}'
```

```text
mem=268435456 cpus=500000000
```

**Expected result:** the container capped at 256 MB and 0.5 CPU — bounded resource use.

**Negative test:** run untrusted or heavy containers with **no limits**; set `--memory`/`--cpus` so one
container cannot starve the host.

**Cleanup:** none yet.

### Lab 4.4 — Add a health check

**Objective:** Report container health.

```bash
docker run -d --name web2 --health-cmd 'curl -f http://localhost/ || exit 1' \
  --health-interval 5s nginx:alpine
sleep 8
docker inspect web2 --format '{{.State.Health.Status}}'
```

```text
healthy
```

**Expected result:** the container reporting `healthy` from its health check — orchestrators can act on
it.

**Negative test:** assume a running container is serving traffic; a **health check** confirms it actually
responds.

**Cleanup:**

```bash
docker rm -f api web2
```

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Containers are image instances isolated by namespaces and cgroups, moving through create → start → stop →
rm; they are run with options (`-d`, `-p`, `-e`, `--restart`), inspected with exec, logs, and stats,
bounded with `--memory`/`--cpus`, and made observable with health checks — one main process per container,
minimal ports, and least privilege.

- [ ] I can explain the container lifecycle.
- [ ] I can run a container with common options.
- [ ] I can exec into and read logs from a container.
- [ ] I can apply resource limits and a health check.
- [ ] I completed Labs 4.1–4.4 including each negative test.
