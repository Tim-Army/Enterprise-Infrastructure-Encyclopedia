# Chapter 01: The Docker Certification Program

## Learning Objectives

- Describe the Docker Certified Associate credential and its six weighted domains.
- Explain the exam format (including DOMC), cost, delivery, and validity.
- Explain the image and container model.
- Reason about where the DCA fits.
- Complete a walkthrough for each program-orientation topic.

## Theory and Architecture

**Docker** popularized containerization, and the **Docker Certified Associate (DCA)** is its foundational
credential — now overseen by **Mirantis**, which acquired the Docker Enterprise Platform business in
November 2019. The exam validates real-world Docker skills across **six weighted domains**:
**Orchestration (~25%)**, **Image Creation, Management, and Registry (~20%)**, **Installation and
Configuration (~15%)**, **Networking (~15%)**, **Security (~15%)**, and **Storage and Volumes (~10%)**.
Its format is distinctive: **13 standard multiple-choice** questions plus **42 discrete-option
multiple-choice (DOMC)** questions in **90 minutes**. In **DOMC**, statements are shown one at a time and
you answer **Yes/No** to each — you cannot go back, so precise knowledge matters. The exam costs **$199
USD** (one attempt), is registered through **Mirantis training**, and the credential is **valid for two
years**. Mirantis recommends **6–12 months** of Docker experience and offers a **bootcamp**. The core
model to internalize: an **image** is a read-only, layered template; a **container** is a running
instance of an image, isolated by Linux **namespaces** and **cgroups**. This chapter orients you on a
local Docker Engine so the domains map to real commands.

## Design Considerations

Prepare across **all six domains**, weighting study by their exam weight (**orchestration** and **images**
are the largest). Practice the **DOMC** style — answer each statement decisively (no going back). Get
**hands-on** with a local Docker Engine (the CLI is what the exam tests). Plan for the **two-year**
validity and the **$199** single-attempt exam.

## Implementation and Automation

The labs confirm the Docker version, run a first container, and map the exam domains — the orientation
every DCA candidate needs before the deeper chapters.

## Validation and Troubleshooting

Confirm the program map:

```text
Credential: Docker Certified Associate (DCA) — overseen by Mirantis (acquired Docker Enterprise 2019)
Exam: 13 multiple-choice + 42 DOMC (Yes/No, one at a time, no going back) / 90 min / $199 / valid 2 years
Domains (weights): Orchestration 25% | Images & Registry 20% | Install & Config 15% | Networking 15% |
                   Security 15% | Storage & Volumes 10%
Model: image (read-only layers) -> container (running instance); namespaces + cgroups isolation
```

Common pitfalls: under-studying the **orchestration** and **image** domains (the heaviest weights); and
being surprised by **DOMC** (you answer each statement Yes/No and cannot revisit).

## Security and Best Practices

The DCA validates building and operating **your own** containers securely. Run the daemon and containers
with least privilege (Chapter 08). All work in this volume is authorized administration.

## Hands-On Lab

Program-orientation walkthroughs. **Shared prerequisites** — a local **Docker Engine** (or Docker
Desktop) with the `docker` CLI, and `python3`. **Cost:** none (Docker Engine is free).

### Lab 1.1 — Confirm the Docker version

**Objective:** Verify the runtime the exam assumes.

```bash
docker version --format '{{.Server.Version}}'
docker info --format '{{.Driver}} / {{.CgroupVersion}}'
```

```text
27.1.1
overlay2 / 2
```

**Expected result:** the Docker Engine version and storage/cgroup drivers — the platform the DCA tests.

**Negative test:** study only with an online playground and never run `docker` locally; the exam is
**hands-on knowledge** — practice with the CLI.

**Rollback:** none (read-only).

### Lab 1.2 — Run a first container

**Objective:** See the image → container model.

```bash
docker run --rm hello-world | head -3
docker run -d --name web -p 8080:80 nginx:alpine
docker ps --format '{{.Names}}\t{{.Image}}\t{{.Status}}'
```

```text
Hello from Docker!
web   nginx:alpine   Up 2 seconds
```

**Expected result:** a throwaway container and a running nginx from an image — the container lifecycle in
miniature.

**Negative test:** install nginx directly on the host to "test containers"; **run it as a container**
from an image.

**Rollback:**

```bash
docker rm -f web
```

### Lab 1.3 — Map the exam domains and weights

**Objective:** Reason about where to focus.

```python
python3 - <<'PY'
weights = {"Orchestration":25, "Image Creation/Registry":20, "Installation & Config":15,
           "Networking":15, "Security":15, "Storage & Volumes":10}
for d, w in sorted(weights.items(), key=lambda kv:-kv[1]):
    print(f"{d:26}: {w}%")
print("Total:", sum(weights.values()), "%; format: 13 MC + 42 DOMC / 90 min / $199 / valid 2 yrs")
PY
```

**Expected result:** the six domains ranked by weight — orchestration and images first.

**Negative test:** spend equal time on storage (10%) and orchestration (25%); weight study by **exam
weight**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Docker Certified Associate, overseen by Mirantis, is a 90-minute exam of 13 multiple-choice and 42
discrete-option (Yes/No) questions for $199, valid two years, across six weighted domains — orchestration,
images and registry, installation and configuration, networking, security, and storage — all grounded in
the image (read-only layers) to container (running, isolated instance) model.

- [ ] I can describe the DCA credential and its six weighted domains.
- [ ] I can explain the exam format including DOMC.
- [ ] I can explain the image and container model.
- [ ] I completed Labs 1.1–1.3 including each negative test.
