# Chapter 02: Installation and Configuration

## Learning Objectives

- Explain Docker Engine components (dockerd, containerd, CLI).
- Configure the daemon with `daemon.json`.
- Use Docker contexts to target different engines.
- Configure logging drivers.
- Complete a walkthrough for each installation-and-configuration topic.

## Theory and Architecture

The **Installation and Configuration** domain covers standing up and tuning the Docker Engine. The engine
is layered: the **`docker` CLI** talks to the **`dockerd`** daemon (over a Unix socket or TCP), which
manages images, containers, networks, and volumes; `dockerd` in turn drives **containerd** (the container
runtime) and **runc** (the OCI runtime that actually starts containers). The daemon is configured through
**`/etc/docker/daemon.json`** — settings like the **storage driver** (`overlay2`), the default **logging
driver** (`json-file`, `local`, `journald`, `syslog`, `fluentd`), **registry mirrors**, insecure
registries, and live-restore. **Docker contexts** let one CLI target multiple engines (local, a remote
host over SSH, a Swarm) by switching context rather than editing environment variables. **Logging
drivers** decide where container stdout/stderr goes (and whether `docker logs` works — some drivers ship
logs elsewhere). This chapter teaches installation and configuration with hands-on `docker` walkthroughs.

## Design Considerations

Configure the daemon declaratively in **`daemon.json`** (not ad-hoc flags) so it is reproducible. Choose
**`overlay2`** storage (the modern default). Pick a **logging driver** matching your log pipeline — but
know that non-`json-file`/`local` drivers may disable `docker logs`. Use **contexts** to manage
prod/dev/remote engines from one CLI. Secure the daemon socket (Chapter 08) — never expose it unprotected
over TCP.

## Implementation and Automation

The labs read the engine components, set a daemon option, switch contexts, and set a container's logging
driver — the installation and configuration the domain validates.

## Validation and Troubleshooting

Confirm installation and configuration:

```text
CLI -> dockerd (daemon) -> containerd (runtime) -> runc (OCI); socket = /var/run/docker.sock
daemon.json: storage-driver (overlay2), log-driver, registry-mirrors, insecure-registries, live-restore
Contexts: one CLI targets local / remote-SSH / Swarm engines (docker context use)
Logging drivers: json-file/local (docker logs works) | journald/syslog/fluentd (ship elsewhere)
```

Common pitfalls: expecting **`docker logs`** to work with a non-local logging driver; and exposing
**`dockerd`** over unauthenticated TCP (root-equivalent access).

## Security and Best Practices

Configure the daemon in `daemon.json`, protect the socket, and choose logging deliberately. A well-configured
engine is the base for secure operations (Chapter 08). All work is authorized administration of your own
host.

## Hands-On Lab

Installation-and-configuration walkthroughs. **Shared prerequisites** — a host with the Docker Engine and
sudo. **Cost:** none.

### Lab 2.1 — Read the engine components

**Objective:** See the CLI/daemon/runtime split.

```bash
docker info --format 'Server: {{.ServerVersion}}  Runtime: {{.DefaultRuntime}}  Storage: {{.Driver}}'
docker system info --format '{{.LoggingDriver}}'
```

```text
Server: 27.1.1  Runtime: runc  Storage: overlay2
json-file
```

**Expected result:** the daemon version, `runc` runtime, `overlay2` storage, and default logging driver —
the engine's makeup.

**Negative test:** assume the CLI *is* the engine; the **`dockerd`** daemon (via containerd/runc) does
the work — the CLI is a client.

**Rollback:** none (read-only).

### Lab 2.2 — Configure a daemon option

**Objective:** Set a registry mirror declaratively.

```bash
sudo tee /etc/docker/daemon.json >/dev/null <<'JSON'
{
  "storage-driver": "overlay2",
  "log-driver": "local",
  "registry-mirrors": ["https://mirror.example.com"]
}
JSON
sudo systemctl reload docker
docker info --format '{{.RegistryConfig.Mirrors}}'
```

```text
[https://mirror.example.com/]
```

**Expected result:** the daemon picking up the mirror and `local` log driver from `daemon.json` —
reproducible configuration.

**Negative test:** pass one-off flags to `dockerd` by editing the unit file ad hoc; use **`daemon.json`**
for reproducible config.

**Rollback:**

```bash
sudo rm -f /etc/docker/daemon.json && sudo systemctl reload docker
```

### Lab 2.3 — Use a Docker context

**Objective:** Target a different engine from one CLI.

```bash
docker context create remote --docker "host=ssh://ops@build01.example.com"
docker context ls --format '{{.Name}}\t{{.DockerEndpoint}}'
docker context use default
```

```text
default   unix:///var/run/docker.sock
remote   ssh://ops@build01.example.com
```

**Expected result:** a `remote` context created; the CLI can switch between local and remote engines.

**Negative test:** juggle `DOCKER_HOST` environment variables per shell; use **contexts** to switch
engines cleanly.

**Rollback:**

```bash
docker context rm remote
```

### Lab 2.4 — Set a container's logging driver

**Objective:** Control where logs go.

```bash
docker run -d --name loggy --log-driver local --log-opt max-size=10m busybox \
  sh -c 'while true; do echo tick; sleep 1; done'
docker inspect loggy --format '{{.HostConfig.LogConfig.Type}}'
docker logs --tail 2 loggy
```

```text
local
tick
tick
```

**Expected result:** the container using the `local` driver with a size cap, and `docker logs` still
working.

**Negative test:** set `--log-driver none` then expect `docker logs`; that driver **discards** logs — use
`local`/`json-file` if you need `docker logs`.

**Rollback:**

```bash
docker rm -f loggy
```

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Docker Engine is the CLI talking to the `dockerd` daemon, which drives containerd and runc; it is
configured reproducibly through `daemon.json` (storage driver, logging driver, registry mirrors), targeted
across engines with contexts, and its logging driver determines where container output goes and whether
`docker logs` works.

- [ ] I can explain the CLI/daemon/runtime components.
- [ ] I can configure the daemon with daemon.json.
- [ ] I can use Docker contexts.
- [ ] I can set a container's logging driver.
- [ ] I completed Labs 2.1–2.4 including each negative test.
