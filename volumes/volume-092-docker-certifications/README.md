# Volume XCII — Docker Certification Tracks

> The Docker certification program in one volume — the Docker Certified Associate (DCA) across its six
> weighted exam domains: orchestration, images and registry, installation and configuration, networking,
> security, and storage — with hands-on `docker` CLI labs, verified against Mirantis training.

## Overview

Volume XCII maps the **Docker** certification program — the credential for building, running, and
operating containers with **Docker**, the platform that popularized containerization. The program centers
on the **Docker Certified Associate (DCA)**, now overseen by **Mirantis** (which acquired the Docker
Enterprise Platform business in November 2019). The exam is a foundational, industry-wide benchmark of
real-world Docker skills across six weighted domains. This volume **completes** the encyclopedia's DevOps
& observability cluster and complements Containers and Platform Engineering (VIII) and the CNCF/Kubernetes
volume (XLI).

This is a **certification-tracks** volume, like the other vendor volumes (XXXIX–XCI): it maps the program
— the credential and its exam domains — and teaches each with a hands-on `docker` walkthrough. The
certification and exam details were **verified against Mirantis training (training.mirantis.com) on 29
July 2026** (the DCA certification and registration pages); third-party exam-dump sites were excluded as
sources.

Chapters follow the exam domains:

- **Chapter 01** frames the program — the DCA exam, Mirantis delivery, the domains and weights, and the image/container model.
- **Chapter 02** takes **Installation and Configuration** — the Docker Engine, the daemon, contexts, and logging.
- **Chapter 03** takes **Image Creation, Management, and Registry** — the Dockerfile, builds, layers, tags, and registries.
- **Chapter 04** takes **containers and the runtime** — the run lifecycle, exec, logs, limits, and health checks.
- **Chapter 05** takes **Storage and Volumes** — volumes, bind mounts, tmpfs, and storage drivers.
- **Chapter 06** takes **Networking** — bridge, host, overlay, none, port publishing, and DNS.
- **Chapter 07** takes **Orchestration with Swarm** — services, stacks, nodes, replicas, and rolling updates.
- **Chapter 08** takes **Orchestration with Kubernetes and Security** — Kubernetes basics and container security.
- **Chapter 09** takes **certification prep, currency, and career**.

Every chapter follows the standard structure defined in
[templates/chapter.md](../../templates/chapter.md) and enforced by
[EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md), including per-topic hands-on labs and
knowledge checks.

> **Scope.** Docker container development and operations are authorized platform work — building,
> running, and securing your own containers and clusters. The security material (image scanning, content
> trust, secrets, rootless mode, and least privilege) is framed as defensive hardening of your own
> workloads.

## Chapters

1. [The Docker Certification Program](chapters/01-the-docker-certification-program.md) — the DCA exam, Mirantis, domains and weights, the container model.
2. [Installation and Configuration](chapters/02-installation-and-configuration.md) — the Docker Engine, daemon, contexts, logging drivers.
3. [Images, Registry, and the Dockerfile](chapters/03-images-registry-and-dockerfile.md) — builds, layers, tags, multi-stage, push/pull.
4. [Containers and the Runtime](chapters/04-containers-and-the-runtime.md) — run lifecycle, exec, logs, resource limits, health checks.
5. [Storage and Volumes](chapters/05-storage-and-volumes.md) — named volumes, bind mounts, tmpfs, storage drivers.
6. [Networking](chapters/06-networking.md) — bridge, host, overlay, none, port publishing, user-defined networks, DNS.
7. [Orchestration with Swarm](chapters/07-orchestration-with-swarm.md) — services, stacks, nodes, replicas, rolling updates, secrets.
8. [Orchestration with Kubernetes and Security](chapters/08-kubernetes-and-security.md) — Kubernetes basics, scanning, content trust, secrets, rootless.
9. [Certification Prep, Currency, and Career](chapters/09-certification-prep-currency-and-career.md) — Mirantis training, the DOMC format, renewal, career.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this volume.

## Certification alignment

This volume *is* the certification map for Docker, recorded in
[CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md) and the Master Appendices
course-catalog appendix. Every chapter carries one hands-on `docker` walkthrough lab per exam domain,
verified against Mirantis training on 29 July 2026.
