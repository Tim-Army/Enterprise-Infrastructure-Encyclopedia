# Chapter 07: Orchestration with Swarm

## Learning Objectives

- Initialize a Swarm and explain manager/worker nodes.
- Create a replicated service.
- Deploy a multi-service stack.
- Perform a rolling update and use secrets.
- Complete a walkthrough for each Swarm topic.

## Theory and Architecture

The **Orchestration** domain is the largest (~25%), and **Docker Swarm** is Docker's built-in
orchestrator. **`docker swarm init`** turns a host into a Swarm with a **manager** node; other hosts join
as **managers** (which maintain the cluster state via Raft consensus — use an odd number) or **workers**
(which run tasks). Instead of individual containers you declare **services** — `docker service create`
runs **N replicas** (tasks) of an image and keeps them running, rescheduling on failure. A **stack** is a
multi-service application defined in a **Compose file** and deployed with `docker stack deploy` — the
declarative way to run an app. Swarm performs **rolling updates** (update replicas in batches with delays
and rollback on failure) so deployments are zero-downtime. **Secrets** and **configs** are first-class:
secrets are encrypted at rest and mounted into only the services that need them. Understanding services,
stacks, nodes, scaling, updates, and secrets is the heart of the orchestration domain. This chapter
teaches Swarm with hands-on `docker` walkthroughs.

## Design Considerations

Use an **odd number of managers** (3 or 5) for Raft quorum; keep managers separate from heavy workloads.
Declare apps as **services**/**stacks** (desired replica count), not hand-run containers. Use **rolling
updates** with `--update-parallelism` and `--update-delay` and automatic **rollback**. Store credentials
as **secrets** (not env vars or image layers). Publish services through the routing mesh and place
replicas across nodes for resilience.

## Implementation and Automation

The labs initialize a Swarm, create and scale a service, deploy a stack, and perform a rolling update with
a secret — the orchestration the largest domain validates.

## Validation and Troubleshooting

Confirm Swarm orchestration:

```text
docker swarm init -> manager (Raft, odd number); workers run tasks
Service: docker service create --replicas N (declares desired state; reschedules on failure)
Stack: multi-service Compose file -> docker stack deploy (declarative app)
Rolling update: --update-parallelism/--update-delay + rollback; Secrets: encrypted, mounted per service
```

Common pitfalls: an **even** number of managers (Raft can lose quorum); and running raw **containers**
instead of **services** (no self-healing or scaling).

## Security and Best Practices

Store credentials as **secrets** (encrypted, scoped), keep an odd manager quorum, and roll updates with
rollback. Swarm's declarative desired state is resilient. All work is authorized administration of your
own cluster.

## Hands-On Lab

Swarm walkthroughs. **Shared prerequisites** — the Docker Engine (single node is fine for Swarm labs).
**Cost:** none.

### Lab 7.1 — Initialize a Swarm

**Objective:** Turn the host into a manager.

```bash
docker swarm init --advertise-addr 127.0.0.1 >/dev/null
docker node ls --format '{{.Hostname}}\t{{.ManagerStatus}}\t{{.Status}}'
```

```text
docker-desktop   Leader   Ready
```

**Expected result:** a single-node Swarm with this host as the manager **Leader** — orchestration is
active.

**Negative test:** run a two-manager Swarm and expect quorum on one failure; use an **odd** number of
managers.

**Rollback:** (Swarm left active for the chapter; `docker swarm leave --force` at the end).

### Lab 7.2 — Create and scale a service

**Objective:** Run N replicas of an image.

```bash
docker service create --name web --replicas 3 -p 8083:80 nginx:alpine >/dev/null
docker service ls --format '{{.Name}}\t{{.Mode}}\t{{.Replicas}}'
docker service scale web=5 >/dev/null
docker service ls --format '{{.Name}}\t{{.Replicas}}'
```

```text
web   replicated   3/3
web   5/5
```

**Expected result:** a replicated service scaled from 3 to 5 tasks — declarative, self-healing scaling.

**Negative test:** run three `docker run` containers by hand; a **service** reschedules failed tasks and
scales — containers do not.

**Rollback:**

```bash
docker service rm web
```

### Lab 7.3 — Deploy a stack

**Objective:** Declare a multi-service app.

```bash
cat > stack.yml <<'YML'
services:
  web:
    image: nginx:alpine
    ports: ["8084:80"]
    deploy: { replicas: 2 }
  redis:
    image: redis:alpine
YML
docker stack deploy -c stack.yml demo
docker stack services demo --format '{{.Name}}\t{{.Replicas}}'
```

```text
demo_web     2/2
demo_redis   1/1
```

**Expected result:** a two-service stack deployed declaratively from a Compose file.

**Negative test:** start each service with separate `service create` commands; a **stack** deploys the
whole app declaratively.

**Rollback:**

```bash
docker stack rm demo && rm -f stack.yml
```

### Lab 7.4 — Rolling update with a secret

**Objective:** Update with zero downtime and a secret.

```bash
printf 'S3cret' | docker secret create api_key -
docker service create --name app --replicas 3 --secret api_key \
  --update-parallelism 1 --update-delay 5s nginx:alpine >/dev/null
docker service update --image nginx:1.27-alpine app >/dev/null
docker service inspect app --format '{{.Spec.UpdateConfig.Parallelism}} at a time'
```

```text
1 at a time
```

**Expected result:** a service with a mounted secret, updated one replica at a time — zero-downtime
rollout.

**Negative test:** put the API key in an environment variable or image layer; use a Swarm **secret**
(encrypted, scoped).

**Rollback:**

```bash
docker service rm app && docker secret rm api_key && docker swarm leave --force
```

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Docker Swarm orchestrates containers as services (N replicas kept running and rescheduled) across
manager (odd-numbered Raft quorum) and worker nodes, deploys multi-service stacks declaratively from
Compose files, performs batched rolling updates with rollback, and mounts encrypted secrets into only the
services that need them.

- [ ] I can initialize a Swarm and explain node roles.
- [ ] I can create and scale a replicated service.
- [ ] I can deploy a multi-service stack.
- [ ] I can perform a rolling update with a secret.
- [ ] I completed Labs 7.1–7.4 including each negative test.
