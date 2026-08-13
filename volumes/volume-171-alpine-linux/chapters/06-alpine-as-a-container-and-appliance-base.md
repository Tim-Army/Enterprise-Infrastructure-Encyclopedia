# Chapter 06: Alpine as a Container and Appliance Base

## Learning Objectives

- Explain why Alpine is the dominant container base image and where that pays off.
- Build a minimal container image on Alpine with `apk --no-cache` and a non-root
  user.
- Use a multi-stage build to ship a small runtime image from a larger build image.
- Recognize the musl-related gotchas that surface in containers and know the fixes.

## Theory and Architecture

Most container ecosystems build on Alpine because the base image is a few megabytes
— roughly an order of magnitude smaller than a general-purpose distribution base —
which means faster pulls, smaller registries, and a smaller attack surface per
image. The mechanics that make Alpine a good *host* (musl, BusyBox, `apk`) make it a
good *base layer* too, plus one container-specific idiom: **`apk --no-cache`**, which
installs packages without writing an index into the image layer, keeping the image
small and reproducible.

Alpine is an especially good base when the application is a **statically linked
binary** (Go, Rust, or C compiled static): the binary carries its own dependencies,
so the image is essentially `alpine` plus one file. It is also ideal for **utility
and shell images** where BusyBox already provides what you need.

The friction appears with **dynamically linked, glibc-assuming software**. Language
runtimes with compiled C extensions (many Python and Node packages) ship prebuilt
wheels/binaries for glibc (`manylinux`); on musl they must either use a musl build
(`musllinux` wheels) or compile from source at build time, which is slower and needs
a toolchain. When a project spends more time fighting musl than it saves in image
size, a `-slim` glibc base or a distroless image is the better choice — the decision
is per-workload, not dogma.

## Design Considerations

- **Reach for Alpine when the payload is static or minimal.** Go/Rust binaries,
  shell tools, and single-purpose daemons (the TFTP server of Chapter 05 packaged as
  a container) are the sweet spot.
- **Reconsider for heavy dynamic runtimes.** If a Python/Node image spends the build
  compiling C extensions because no musl wheel exists, measure whether a
  `debian-slim` base is faster overall; image size is not the only cost.
- **Pin the tag.** Build on `alpine:3.24`, not `alpine:latest`, so rebuilds are
  reproducible and a new Alpine release does not silently change your base.
- **Run as non-root.** Create an unprivileged user in the image; nothing about a
  small base excuses running the process as root.
- **Use multi-stage builds** to keep the toolchain out of the runtime image — build
  fat, ship thin.

## Implementation and Automation

A minimal image with a non-root user and no cached index:

```dockerfile
FROM alpine:3.24
RUN apk add --no-cache curl \
 && adduser -D -H appuser
USER appuser
ENTRYPOINT ["curl"]
```

A multi-stage build — compile in a builder, ship a tiny runtime:

```dockerfile
# build stage: full toolchain
FROM golang:1.23-alpine AS build
WORKDIR /src
COPY . .
RUN CGO_ENABLED=0 go build -o /app ./cmd/app

# runtime stage: alpine + one static binary
FROM alpine:3.24
RUN adduser -D appuser
COPY --from=build /app /usr/local/bin/app
USER appuser
ENTRYPOINT ["/usr/local/bin/app"]
```

`CGO_ENABLED=0` produces a static Go binary with no musl/glibc dependency at all, so
the runtime image is `alpine` plus the binary.

## Validation and Troubleshooting

```sh
docker build -t demo:alpine .
docker images demo:alpine                 # tens of MB, not hundreds
docker run --rm demo:alpine --version
docker run --rm demo:alpine id            # not uid 0 if USER is set
```

Common issues:

- **A Python/Node build is slow or fails compiling a wheel.** No musl (`musllinux`)
  wheel exists, so it builds from source; add the build deps as a `--virtual` group
  and delete them in the same layer, or switch to a glibc `-slim` base.
- **A copied glibc binary reports "not found" in the image.** It needs the glibc
  loader; build it static, use a musl build, or add `gcompat` — same musl boundary as
  Chapter 01.
- **DNS behaves differently than on a Debian base.** musl's resolver differs from
  glibc's in some edge cases (search domains, parallel A/AAAA); usually harmless, but
  worth knowing when a container resolves names oddly.
- **The image is bigger than expected.** A cached `apk` index or leftover build deps
  are in a layer; use `--no-cache` and clean build deps in the same `RUN`.

## Security and Best Practices

- **Pin the base tag** and rebuild to pick up Alpine security updates deliberately.
- **`--no-cache`** everywhere in images to keep layers minimal and reproducible.
- **Non-root `USER`** in every image; drop capabilities at runtime as well.
- **Keep the package set minimal** — the small base is the security benefit, so do
  not undo it by installing a full userland you do not need.
- **Scan images** and track Alpine's security database (`secdb`) for the packages you
  ship.

## References and Knowledge Checks

- [Docker Official Images — alpine](https://hub.docker.com/_/alpine) and Alpine wiki
  [Docker](https://wiki.alpinelinux.org/wiki/Docker).
- [musllinux (PEP 656)](https://peps.python.org/pep-0656/) — musl wheels for Python.

**Knowledge checks:**

1. Why is Alpine an excellent base for a static Go binary but a mixed choice for a
   Python image with C extensions?
2. What does `apk --no-cache` do, and why does it matter in an image?
3. Why pin `alpine:3.24` instead of `alpine:latest`?

## Hands-On Lab

**Objective:** Build minimal and multi-stage Alpine images and prove they are small
and non-root.

**Shared prerequisites** — a host with Docker or Podman. **Cost:** none.

### Lab 6.1 — A minimal, non-root image

**Objective:** Build a tiny image that runs as an unprivileged user.

```sh
printf 'FROM alpine:3.24\nRUN apk add --no-cache curl && adduser -D appuser\nUSER appuser\nENTRYPOINT ["id"]\n' > Dockerfile
docker build -t demo:alpine .
docker images demo:alpine
docker run --rm demo:alpine            # uid is appuser, not 0
```

**Expected result:** an image of a few tens of MB whose process runs as `appuser`.

**Negative test:** remove the `USER` line and rebuild; the process runs as root —
a small base does not make root acceptable.

**Rollback:** `docker rmi demo:alpine`.

### Lab 6.2 — Multi-stage build

**Objective:** Ship a runtime image containing only a static binary.

1. Use the multi-stage Dockerfile from Implementation (or any small Go program).
2. Build and compare sizes:

```sh
docker build -t demo:multi .
docker images | grep -E 'golang|demo:multi'   # builder large, runtime tiny
docker run --rm demo:multi --help || true
```

**Expected result:** the `golang` build image is large; the final `demo:multi`
runtime image is `alpine` plus one binary.

**Negative test:** build the binary with `CGO_ENABLED=1` and no musl toolchain in
the runtime image; it fails to run (missing dynamic dependency) — static (`CGO_ENABLED=0`)
is what makes the tiny runtime image work.

**Rollback:** `docker rmi demo:multi` and prune dangling build layers.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Alpine is the dominant container base because it is tiny, and it shines when the
payload is a static binary or a minimal utility image. `apk --no-cache`, a pinned
base tag, a non-root `USER`, and multi-stage builds are the idioms that keep images
small and safe. The musl boundary from Chapter 01 reappears here: glibc-assuming
runtimes and prebuilt wheels can cost more than the size saving, so the base choice
is per-workload.

- [ ] Can build a minimal, non-root Alpine image with `--no-cache`.
- [ ] Can use a multi-stage build to ship a thin runtime image.
- [ ] Can explain when Alpine is the wrong base and why.
- [ ] Completed Labs 6.1–6.2 including each negative test.
