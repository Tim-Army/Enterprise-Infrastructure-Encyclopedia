# Chapter 03: Images, Registry, and the Dockerfile

## Learning Objectives

- Write a Dockerfile and build an image.
- Explain image layers and the build cache.
- Tag and push images to a registry.
- Use multi-stage builds to shrink images.
- Complete a walkthrough for each image-and-registry topic.

## Theory and Architecture

The **Image Creation, Management, and Registry** domain (~20%) covers building and distributing images.
A **Dockerfile** is the recipe: **`FROM`** picks a base image, **`RUN`** executes build steps,
**`COPY`/`ADD`** bring in files, **`ENV`**/**`ARG`** set variables, **`EXPOSE`** documents ports, and
**`CMD`**/**`ENTRYPOINT`** define what runs. Each instruction creates a **layer** (a read-only diff);
layers are **cached** and reused across builds, so ordering instructions from least- to most-frequently
changed speeds builds. Images are named **`registry/repository:tag`** (default registry Docker Hub); you
**`docker tag`** and **`docker push`** to publish, and **`docker pull`** to fetch. A **multi-stage build**
uses several `FROM` stages so build tools stay in an early stage and only the artifact is copied into a
small final image. A **`.dockerignore`** keeps unneeded files out of the build context. This chapter
teaches images and registries with hands-on `docker` walkthroughs.

## Design Considerations

Order Dockerfile instructions to **maximize cache reuse** (copy dependency manifests and install before
copying source). Use small **base images** (alpine/distroless) and **multi-stage** builds to shrink the
final image and attack surface. **Tag** images meaningfully (version, not just `latest`) and push to a
registry. Add a **`.dockerignore`**. Pin base image versions for reproducibility, and scan images
(Chapter 08).

## Implementation and Automation

The labs build an image from a Dockerfile, observe layer caching, tag and reason about pushing, and use a
multi-stage build — the image skills the domain validates.

## Validation and Troubleshooting

Confirm images and registry:

```text
Dockerfile: FROM/RUN/COPY/ENV/EXPOSE/CMD/ENTRYPOINT -> each instruction = a cached layer
Build cache: order least- to most-changed; copy manifests + install before source
Naming: registry/repository:tag (default Docker Hub); docker tag / push / pull
Multi-stage: build tools in early stage; copy only the artifact into a small final image; .dockerignore
```

Common pitfalls: copying **source before installing dependencies** (busts the cache every build); and
shipping the **build toolchain** in the final image (bloat + attack surface) — use **multi-stage**.

## Security and Best Practices

Small, multi-stage images reduce attack surface; pin base versions and **scan** images (Chapter 08).
Do not bake secrets into layers (they persist in history). All work is authorized.

## Hands-On Lab

Image-and-registry walkthroughs. **Shared prerequisites** — the Docker Engine and a working directory.
**Cost:** none.

### Lab 3.1 — Build an image from a Dockerfile

**Objective:** Turn a recipe into an image.

```bash
mkdir app && cd app
cat > Dockerfile <<'DF'
FROM alpine:3.20
RUN apk add --no-cache curl
COPY hello.sh /usr/local/bin/hello
ENTRYPOINT ["/usr/local/bin/hello"]
DF
echo -e '#!/bin/sh\necho "Hello from a container"' > hello.sh && chmod +x hello.sh
docker build -t myapp:1.0 .
docker run --rm myapp:1.0
```

```text
=> naming to docker.io/library/myapp:1.0
Hello from a container
```

**Expected result:** an image built from the Dockerfile that runs the script — a working container image.

**Negative test:** run `apk add` inside a running container each time instead of in the image; **bake** it
into the Dockerfile so the image is reproducible.

**Cleanup:** (removed at the end of Lab 3.4).

### Lab 3.2 — Observe layer caching

**Objective:** See the cache reuse.

```bash
docker build -t myapp:1.0 .    # second build, no changes
```

```text
 => CACHED [2/3] RUN apk add --no-cache curl
 => CACHED [3/3] COPY hello.sh /usr/local/bin/hello
 => naming to docker.io/library/myapp:1.0
```

**Expected result:** every layer served from **CACHED** on an unchanged rebuild — fast, deterministic
builds.

**Negative test:** put `COPY . .` before `RUN apk add`; any source change **busts** the install cache —
copy manifests/install first.

**Cleanup:** none yet.

### Lab 3.3 — Tag and reason about pushing

**Objective:** Name an image for a registry.

```bash
docker tag myapp:1.0 registry.example.com/team/myapp:1.0
docker image ls --format '{{.Repository}}:{{.Tag}}' | grep myapp
```

```text
registry.example.com/team/myapp:1.0
myapp:1.0
# docker login registry.example.com && docker push registry.example.com/team/myapp:1.0
```

**Expected result:** the image tagged for a private registry, ready to `docker push` after `docker login`.

**Negative test:** rely on the `latest` tag for releases; **version** tags (`1.0`) make deployments
reproducible.

**Cleanup:** none yet.

### Lab 3.4 — Shrink with a multi-stage build

**Objective:** Keep build tools out of the final image.

```bash
cat > Dockerfile.multi <<'DF'
FROM golang:1.22 AS build
WORKDIR /src
RUN echo 'package main; func main(){println("hi")}' > main.go && go build -o /app main.go
FROM alpine:3.20
COPY --from=build /app /app
ENTRYPOINT ["/app"]
DF
docker build -f Dockerfile.multi -t myapp:slim .
docker image ls --format '{{.Repository}}:{{.Tag}}\t{{.Size}}' | grep myapp
```

```text
myapp:slim   8.2MB      # only the binary + alpine, not the Go toolchain
myapp:1.0   12MB
```

**Expected result:** the multi-stage `slim` image containing only the compiled binary on alpine — no Go
toolchain.

**Negative test:** ship the `golang:1.22` build image to production; use a **multi-stage** build to copy
only the artifact.

**Cleanup:**

```bash
cd .. && rm -rf app && docker rmi -f myapp:1.0 myapp:slim registry.example.com/team/myapp:1.0 2>/dev/null
```

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Docker images are built from a Dockerfile whose instructions each create a cached layer (ordered least- to
most-changed for cache reuse), named `registry/repository:tag` and distributed with tag/push/pull, and
kept small and low-attack-surface with multi-stage builds and `.dockerignore` — with meaningful version
tags and pinned base images.

- [ ] I can write a Dockerfile and build an image.
- [ ] I can explain layers and observe the build cache.
- [ ] I can tag and reason about pushing to a registry.
- [ ] I can shrink an image with a multi-stage build.
- [ ] I completed Labs 3.1–3.4 including each negative test.
