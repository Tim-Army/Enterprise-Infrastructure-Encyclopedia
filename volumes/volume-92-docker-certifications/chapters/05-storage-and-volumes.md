# Chapter 05: Storage and Volumes

## Learning Objectives

- Distinguish volumes, bind mounts, and tmpfs.
- Create and use a named volume for persistent data.
- Use a bind mount for development.
- Explain the storage driver and the copy-on-write layer.
- Complete a walkthrough for each storage-and-volumes topic.

## Theory and Architecture

The **Storage and Volumes** domain (~10%) covers persisting and mounting data. A container's writable
layer is **ephemeral** — it disappears when the container is removed — so persistent data must live in a
mount. Three mount types: a **named volume** (Docker-managed storage under `/var/lib/docker/volumes/`,
the recommended way to persist data — portable, backup-able, driver-pluggable); a **bind mount** (a host
path mounted into the container, ideal for development or sharing host files, but tied to the host layout);
and **tmpfs** (in-memory, non-persistent, for sensitive scratch data). Volumes can use **volume drivers**
to store data on NFS, cloud block storage, etc. Underneath, the **storage driver** (`overlay2`) implements
the image's **copy-on-write** layers: containers share read-only image layers and only their changes are
written to a thin writable layer. Knowing when to use each mount type and how the writable layer behaves
is the domain's core. This chapter teaches storage with hands-on `docker` walkthroughs.

## Design Considerations

Persist stateful data in **named volumes** (not the container's writable layer, which is lost on `rm`).
Use **bind mounts** for development (live code) and config; prefer volumes for production data. Use
**tmpfs** for secrets/scratch that should never hit disk. Choose a **volume driver** for shared/networked
storage. Back up volumes. Keep the image's writable layer small (`overlay2` copy-on-write).

## Implementation and Automation

The labs create a named volume and prove persistence, use a bind mount, and reason about tmpfs and the
storage driver — the storage skills the domain validates.

## Validation and Troubleshooting

Confirm storage and volumes:

```text
Container writable layer = EPHEMERAL (lost on rm) -> persist in a mount
Named volume: Docker-managed, portable, backup-able, driver-pluggable (recommended for data)
Bind mount: host path -> container (dev/config; tied to host layout); tmpfs: in-memory, non-persistent
Storage driver overlay2: copy-on-write; containers share read-only image layers + thin writable layer
```

Common pitfalls: writing important data to the container's **writable layer** (gone on `rm`) — use a
**volume**; and using a **bind mount** in production where a **named volume** is more portable.

## Security and Best Practices

Use tmpfs for secrets that must not persist, back up volumes, and mount read-only where possible
(`:ro`). Managed volumes are safer and more portable than bind mounts. All work is authorized.

## Hands-On Lab

Storage-and-volumes walkthroughs. **Shared prerequisites** — the Docker Engine. **Cost:** none.

### Lab 5.1 — Persist data with a named volume

**Objective:** Survive container removal.

```bash
docker volume create appdata
docker run --rm -v appdata:/data busybox sh -c 'echo "persisted" > /data/file.txt'
docker rm -f $(docker ps -aq --filter volume=appdata) 2>/dev/null
docker run --rm -v appdata:/data busybox cat /data/file.txt
```

```text
persisted
```

**Expected result:** data written by one container is read by another after the first is gone — the volume
persists.

**Negative test:** write the file to the container's own filesystem (no volume) and `--rm` it; the data is
**lost** — use a named volume.

**Cleanup:**

```bash
docker volume rm appdata
```

### Lab 5.2 — Use a bind mount for development

**Objective:** Mount host code into a container.

```bash
mkdir -p /tmp/site && echo "<h1>Dev</h1>" > /tmp/site/index.html
docker run -d --name devweb -p 8081:80 -v /tmp/site:/usr/share/nginx/html:ro nginx:alpine
docker exec devweb cat /usr/share/nginx/html/index.html
```

```text
<h1>Dev</h1>
```

**Expected result:** the host directory mounted read-only into the container — edits on the host appear
inside.

**Negative test:** bake the site into the image and rebuild on every edit during development; a **bind
mount** gives live updates.

**Cleanup:**

```bash
docker rm -f devweb && rm -rf /tmp/site
```

### Lab 5.3 — Reason about tmpfs

**Objective:** Keep scratch data in memory.

```bash
docker run --rm --tmpfs /scratch:size=16m busybox sh -c 'echo secret > /scratch/x; ls -la /scratch'
```

```text
-rw-r--r--  1 root  root  7  x        # exists in memory only; gone when the container stops
```

**Expected result:** an in-memory `tmpfs` mount for scratch/sensitive data that never touches disk.

**Negative test:** write short-lived secrets to a normal volume/disk; use **tmpfs** so they are not
persisted.

**Cleanup:** none (tmpfs is gone with the container).

### Lab 5.4 — Inspect the storage driver

**Objective:** See copy-on-write layering.

```bash
docker info --format 'Storage driver: {{.Driver}}'
docker image inspect nginx:alpine --format '{{len .RootFS.Layers}} layers'
```

```text
Storage driver: overlay2
6 layers
```

**Expected result:** `overlay2` and the image's read-only layer count — the copy-on-write base each
container shares.

**Negative test:** expect each container to copy the whole image; **copy-on-write** shares read-only
layers and writes only diffs.

**Cleanup:** none (read-only).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

A container's writable layer is ephemeral, so persistent data lives in mounts: named volumes
(Docker-managed, portable, recommended for data), bind mounts (host paths for development), and tmpfs
(in-memory for secrets/scratch) — all over an `overlay2` copy-on-write storage driver where containers
share read-only image layers and write only their diffs.

- [ ] I can distinguish volumes, bind mounts, and tmpfs.
- [ ] I can persist data with a named volume.
- [ ] I can use a bind mount for development.
- [ ] I can explain the storage driver and copy-on-write.
- [ ] I completed Labs 5.1–5.4 including each negative test.
