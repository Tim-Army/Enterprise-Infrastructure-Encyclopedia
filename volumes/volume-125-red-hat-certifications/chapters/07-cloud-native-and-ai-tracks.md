# Chapter 07: The Cloud-Native and AI Tracks

## Learning Objectives

- Map the Cloud-Native Applications track (EX188 Developer, EX288 Advanced Developer).
- Understand the new AI track and its provisional status.
- Drill the cloud-native build/deploy concepts these exams test.

## The Cloud-Native Applications track

Red Hat's developer-leaning track: building and deploying containerized applications on OpenShift.

| Level | Credential | Exam |
|:---|:---|:---|
| L1/L2 | Cloud-Native Developer | **EX188** |
| L3 | Advanced Cloud-Native / Enterprise Microservices Developer | **EX288** |
| L4 | Specialists (build/pipeline, service mesh, serverless) | various |
| L5 | RHCA in Cloud-Native | in-track assembly |

**EX188** validates building container images and running them on OpenShift; **EX288** goes to source-to-image, multi-container applications, health probes, and configuration/secrets — developer-side, still 100% performance-based.

## The AI track (new, provisional)

Red Hat added a fifth track for **AI** in the 2026 restructure. At verification (3 August 2026) its **exam codes were still pending** — the track is announced, the credentials are being finalized. Expect it to center on **RHEL AI** (the supported platform for training/serving foundation models) and **OpenShift AI** (the MLOps platform, formerly OpenShift Data Science). Treat any AI-track exam number you see as provisional until it appears on redhat.com; this volume maps the track's shape, not codes it cannot yet verify.

## Hands-On Lab

Container tooling (`podman`, `oc`/`kubectl`) as in [Chapter 06](06-openshift-track-ex280.md). **Cost:** none.

### Lab 7.1 — Build a container image (EX188)

**Objective (task):** "Write a Containerfile, build an image, and run it."

```bash
mkdir -p ~/ex188 && cd ~/ex188
cat > index.html <<'EOF'
<h1>cloud-native lab</h1>
EOF
cat > Containerfile <<'EOF'
FROM registry.access.redhat.com/ubi9/httpd-24
COPY index.html /var/www/html/index.html
EXPOSE 8080
EOF
podman build -t lab-web:1 . 2>/dev/null || docker build -t lab-web:1 .
podman run -d --name cnlab -p 8081:8080 lab-web:1 2>/dev/null || docker run -d --name cnlab -p 8081:80 lab-web:1
sleep 2; curl -s localhost:8081 | head -1; podman rm -f cnlab 2>/dev/null || docker rm -f cnlab
```

**Expected result:** An image built from a Containerfile and serving the page — writing Containerfiles (FROM/COPY/EXPOSE/CMD), building with Podman/Buildah, and running are EX188's foundation. UBI (Universal Base Image) is the Red Hat-sanctioned base.

**Negative test:** `EXPOSE 80` but the ubi9 httpd listens on 8080 — the container serves nothing on the mapped port; matching the image's actual port is the developer's job.

**Cleanup:** `rm -rf ~/ex188`.

### Lab 7.2 — Config and secrets (EX288)

**Objective (task):** "Externalize configuration via a ConfigMap and a Secret."

```bash
kubectl create namespace cn 2>/dev/null
kubectl -n cn create configmap appcfg --from-literal=GREETING=hello
kubectl -n cn create secret generic appsec --from-literal=TOKEN=s3cr3t
kubectl -n cn get configmap appcfg -o jsonpath='{.data.GREETING}'; echo
kubectl -n cn get secret appsec -o jsonpath='{.data.TOKEN}' | base64 -d; echo
```

**Expected result:** A ConfigMap value read back plain and a Secret value base64-decoded — externalizing config (ConfigMaps) and secrets, then injecting them as env vars or volumes, is a central EX288 objective (the twelve-factor "config in the environment" principle).

**Negative test:** Bake the token into the image instead — it ships in every layer, unrotatable; Secrets exist precisely to keep credentials out of images, the lesson EX288 enforces.

**Cleanup:** `kubectl delete namespace cn`.

### Lab 7.3 — Health probes (EX288)

**Objective (task):** "Add readiness and liveness probes to a deployment."

```bash
kubectl create namespace cn 2>/dev/null
kubectl -n cn apply -f - <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata: { name: probed, namespace: cn }
spec:
  replicas: 1
  selector: { matchLabels: { app: probed } }
  template:
    metadata: { labels: { app: probed } }
    spec:
      containers:
        - name: web
          image: httpd
          readinessProbe: { httpGet: { path: /, port: 80 }, initialDelaySeconds: 2 }
          livenessProbe:  { httpGet: { path: /, port: 80 }, periodSeconds: 10 }
EOF
kubectl -n cn rollout status deployment/probed --timeout=60s
kubectl -n cn get deployment probed
```

**Expected result:** The deployment becoming Ready once the readiness probe passes — readiness (gates traffic) vs liveness (restarts a hung container) probes are an EX288 objective and a production must-have.

**Negative test:** A readiness probe pointing at a wrong path/port — the pod runs but never becomes Ready and gets no traffic; "app up but no traffic" is the probe-misconfiguration signature.

**Cleanup:** `kubectl delete namespace cn`.

### Lab 7.4 — AI track orientation (provisional)

**Objective:** State the AI track's likely shape without over-claiming codes.

```text
AI track (exam codes pending at 3 Aug 2026):
  RHEL AI     — supported platform to fine-tune/serve foundation models (InstructLab, granite models)
  OpenShift AI — MLOps: notebooks, pipelines, model serving, GPU scheduling on OpenShift
  verify exam numbers on redhat.com before planning — this track is newest and still settling
```

**Expected result:** The AI track understood as RHEL AI (model platform) + OpenShift AI (MLOps), with the explicit caveat that its exam codes must be verified on redhat.com — the honest boundary for a post-restructure, still-forming track.

**Negative test:** Registering for an "AI track" exam number from a third-party site — provisional/unofficial; only redhat.com confirms the codes for the newest track.

**Cleanup:** None (design).

## Summary and Completion Checklist

- [ ] Cloud-Native track (EX188/EX288) mapped and its build/config/probe concepts drilled.
- [ ] Container image built from a Containerfile; ConfigMap/Secret/probes exercised.
- [ ] AI track's shape understood, with codes flagged as pending official verification.
