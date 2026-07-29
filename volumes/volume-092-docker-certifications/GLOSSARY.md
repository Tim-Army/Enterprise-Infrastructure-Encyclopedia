# Volume XCII Glossary

Definitions for terms introduced in **Volume XCII — Docker Certification Tracks**.
See the [master glossary](../../GLOSSARY.md) for cross-volume terms.

- **Bind mount** — a host directory mounted into a container, tied to the host's layout.
- **Container** — a running instance of an image, isolated by Linux namespaces and cgroups.
- **daemon.json** — the Docker daemon configuration file (storage driver, logging driver, registry mirrors).
- **Docker Certified Associate (DCA)** — Docker's foundational certification, now overseen by Mirantis.
- **Docker Content Trust (DCT)** — the mechanism (via Notary) that signs images on push and verifies them on pull.
- **dockerd / containerd / runc** — the Docker daemon, the container runtime, and the OCI runtime that starts containers.
- **DOMC (discrete-option multiple-choice)** — an exam format presenting statements one at a time for a Yes/No answer, with no going back.
- **Dockerfile** — the recipe that builds an image (FROM, RUN, COPY, CMD, ENTRYPOINT, …).
- **Image** — a read-only, layered template from which containers are instantiated.
- **Multi-stage build** — a Dockerfile with multiple FROM stages that keeps build tools out of the final image.
- **Named volume** — Docker-managed persistent storage, the recommended way to persist container data.
- **Overlay network** — a multi-host network driver that connects services across a Swarm.
- **overlay2** — Docker's default copy-on-write storage driver.
- **Service** — in Swarm, a declared set of replicas of an image that Docker keeps running.
- **Stack** — a multi-service application defined in a Compose file and deployed to a Swarm.
- **Swarm** — Docker's built-in orchestrator, with manager (Raft) and worker nodes.
- **tmpfs mount** — an in-memory, non-persistent mount for scratch or sensitive data.
- **User-defined bridge network** — a private network that provides automatic DNS resolution by container name.
