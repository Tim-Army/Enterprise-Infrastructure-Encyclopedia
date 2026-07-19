import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-08-containers-platform-engineering"


def ch01():
    c = Canvas(960, 600,
        title="Chapter 1 Hands-On Lab: OCI Image Build, Sign, and a Detected Tampering Attempt",
        subtitle="cosign verifies the original signed digest; the same tag re-pushed with new content has no valid signature",
        svg_title="Chapter 1 lab flow: building, scanning, and cosign-signing a non-root OCI image, then detecting a tampered re-push",
        svg_desc="A minimal distroless Go image is built, pushed to a local registry (localhost:5000/app:1.0.0), "
                  "confirmed running as a non-root user, scanned with syft/trivy, and signed with cosign using a "
                  "local key pair. cosign verify against the signed digest succeeds. As a negative test, the "
                  "Dockerfile is modified and the image rebuilt and pushed under the same tag; verifying the "
                  "original signature against the new digest fails with 'no matching signatures', because the tag "
                  "moved but the digest it now points to was never signed — the mechanism that makes "
                  "digest-pinned, signature-verified deployments safe against a compromised or overwritten tag.")
    c.node_box(60, 140, 220, 110, "mgmt", [
        Line("Build + Push v1.0.0", 12.5, 700, "#111827"),
        Line("distroless, non-root", 10.5, 400, "#374151"),
        Line("localhost:5000/app:1.0.0", 10.5, 400, "#374151"),
    ])
    c.node_box(370, 140, 220, 110, "alt", [
        Line("Scan + Sign", 12.5, 700, "#111827"),
        Line("syft/trivy: few HIGH/CRITICAL", 10.5, 400, "#374151"),
        Line("cosign sign --key cosign.key", 10.5, 400, "#374151"),
    ])
    c.connector(280, 195, 370, 195, "mgmt")
    c.node_box(680, 140, 220, 110, "alt", [
        Line("cosign verify", 12.5, 700, "#111827"),
        Line("verified claims, exit 0", 10.5, 700, "#14532d"),
    ])
    c.connector(590, 195, 680, 195, "alt")
    c.node_box(60, 340, 840, 130, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("Dockerfile modified, rebuilt, and pushed under the same tag 1.0.0 (new digest, same tag)", 11, 400, "#7f1d1d"),
        Line("cosign verify against the new digest → \"no matching signatures\" (the new digest was never signed)", 11, 400, "#7f1d1d"),
        Line("digest-pinned, signature-verified deployment is safe against a compromised or overwritten tag", 11, 400, "#7f1d1d"),
    ])
    c.legend(60, 510, [("mgmt", "Build/push"), ("alt", "Signed + verified"), ("warn", "Tampered re-push (caught)")])
    c.save(f"{OUT}/chapter-01-oci-image-sign-tamper-detection-flow.svg")


def ch02():
    c = Canvas(960, 660,
        title="Chapter 2 Hands-On Lab: Three-Node kind Cluster, etcd Snapshot, and a Simulated Worker Loss",
        subtitle="A stopped worker transitions to NotReady after the grace period; its pods reschedule, then it self-heals on restart",
        svg_title="Chapter 2 lab topology: a kind Kubernetes cluster's control-plane static pods, an etcd snapshot, and a worker-node failure test",
        svg_desc="A three-node kind cluster (one control plane, two workers) runs etcd, kube-apiserver, "
                  "kube-scheduler, and kube-controller-manager as static pods on the control-plane node. etcd "
                  "cluster health is confirmed and a snapshot is taken and verified as structurally valid. A "
                  "trivial hello deployment provides observable state. As a negative test, one worker's container "
                  "is stopped; the node transitions to NotReady after the default node-monitor-grace-period "
                  "(roughly 40 seconds), and any pods scheduled there are marked for eviction and rescheduled onto "
                  "the remaining worker. Restarting the stopped worker returns it to Ready within about a minute "
                  "as kubelet re-registers.")
    c.node_box(370, 110, 220, 130, "mgmt", [
        Line("control-plane node", 13, 700, "#111827"),
        Line("etcd, kube-apiserver", 10.5, 400, "#374151"),
        Line("kube-scheduler, controller-mgr", 10.5, 400, "#374151"),
        Line("etcd snapshot: verified", 10.5, 700, "#1d4ed8"),
    ])
    c.node_box(80, 300, 240, 110, "alt", [
        Line("worker (healthy)", 13, 700, "#111827"),
        Line("hello deployment pod", 10.5, 400, "#374151"),
        Line("status: Ready", 10.5, 700, "#14532d"),
    ])
    c.node_box(640, 300, 260, 110, "warn", [
        Line("worker (negative test)", 12.5, 700, "#111827"),
        Line("docker stop → NotReady (~40s)", 10.5, 700, "#7f1d1d"),
        Line("pods evicted, rescheduled", 10.5, 700, "#7f1d1d"),
    ])
    c.connector(430, 240, 200, 300, "mgmt")
    c.connector(560, 240, 770, 300, "warn")
    c.connector(320, 355, 640, 355, "warn", label="pods rescheduled onto surviving worker")
    c.node_box(80, 470, 820, 90, "neutral", [
        Line("docker start restores the worker; kubelet re-registers and the node returns to Ready within roughly a minute", 11.5, 400, "#374151"),
    ])
    c.legend(80, 600, [("mgmt", "Control plane"), ("alt", "Healthy worker"), ("warn", "Failed worker (negative test)")])
    c.save(f"{OUT}/chapter-02-kind-cluster-etcd-node-loss-topology.svg")


def ch03():
    c = Canvas(960, 660,
        title="Chapter 3 Hands-On Lab: Anti-Affinity, HPA Scale-Out, and a PDB-Blocked Drain",
        subtitle="Three demo-api pods spread across three nodes scale out under load, then a drain is refused below minAvailable",
        svg_title="Chapter 3 lab topology: a workload with required anti-affinity and an HPA, tested against a PodDisruptionBudget-blocked drain",
        svg_desc="demo-api deploys 3 replicas with required pod anti-affinity (one pod per node) and a "
                  "PodDisruptionBudget requiring minAvailable 2. An HPA targeting 50% CPU confirms live metrics "
                  "and scales replicas out under generated load. As a negative test, draining the node holding one "
                  "demo-api pod while only 3 replicas exist is refused: the drain reports 'Cannot evict pod as it "
                  "would violate the pod's disruption budget', because removing that pod would drop available "
                  "replicas below minAvailable 2 and the deployment cannot immediately reschedule a replacement "
                  "onto the now-cordoned node. Uncordoning the node restores normal scheduling.")
    c.node_box(60, 140, 220, 100, "mgmt", [
        Line("Node A", 13, 700, "#111827"),
        Line("demo-api pod (1/3)", 10.5, 400, "#374151"),
    ])
    c.node_box(370, 140, 220, 100, "mgmt", [
        Line("Node B", 13, 700, "#111827"),
        Line("demo-api pod (2/3)", 10.5, 400, "#374151"),
    ])
    c.node_box(680, 140, 220, 100, "warn", [
        Line("Node C (negative test)", 12, 700, "#111827"),
        Line("demo-api pod (3/3)", 10.5, 700, "#7f1d1d"),
    ])
    c.node_box(280, 280, 400, 90, "neutral", [
        Line("PodDisruptionBudget: minAvailable 2", 12.5, 700, "#111827"),
        Line("required anti-affinity: 1 pod per node", 10.5, 400, "#374151"),
    ])
    c.connector(170, 240, 400, 280, "neutral")
    c.connector(480, 240, 460, 280, "neutral")
    c.connector(790, 240, 560, 280, "warn")
    c.node_box(60, 420, 840, 130, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("kubectl drain Node C while only 3 replicas exist total", 11, 400, "#7f1d1d"),
        Line("refused: \"Cannot evict pod as it would violate the pod's disruption budget\"", 11, 400, "#7f1d1d"),
        Line("node cordoned but the pod remains; uncordon restores normal scheduling", 11, 400, "#7f1d1d"),
    ])
    c.legend(60, 600, [("mgmt", "Anti-affinity-spread pod"), ("warn", "Drain target (blocked by PDB)"), ("neutral", "Guardrail")])
    c.save(f"{OUT}/chapter-03-hpa-pdb-drain-topology.svg")


def ch04():
    c = Canvas(960, 600,
        title="Chapter 4 Hands-On Lab: NetworkPolicy Default-Deny, Then a Scoped Allow",
        subtitle="Calico enforces a namespace-wide deny; only an explicit client-to-server rule restores connectivity",
        svg_title="Chapter 4 lab topology: a Kubernetes NetworkPolicy default-deny baseline enforced by Calico, then a scoped allow rule",
        svg_desc="client and server pods in the netpol-lab namespace initially reach each other freely (HTTP 200), "
                  "with no NetworkPolicy in place. A default-deny-all policy (empty podSelector, Ingress and "
                  "Egress) is applied; the same request now times out and fails, confirming Calico is actually "
                  "enforcing the policy rather than it being merely configured. A scoped allow-client-to-server "
                  "policy permitting only that pair on port 8080 is then added; connectivity is restored for "
                  "exactly that path, while any other pod added later to the namespace remains denied by default.")
    c.node_box(80, 150, 220, 100, "mgmt", [
        Line("client pod", 13, 700, "#111827"),
        Line("curlimages/curl", 10.5, 400, "#374151"),
    ])
    c.node_box(660, 150, 220, 100, "mgmt", [
        Line("server pod", 13, 700, "#111827"),
        Line("agnhost netexec :8080", 10.5, 400, "#374151"),
    ])
    c.node_box(340, 260, 280, 90, "neutral", [
        Line("default-deny-all", 12.5, 700, "#111827"),
        Line("podSelector: {} — Ingress+Egress", 10.5, 400, "#374151"),
    ])
    c.connector(300, 200, 340, 290, "warn", label="before policy: 200 OK / after: blocked")
    c.connector(660, 200, 620, 290, "warn")
    c.node_box(300, 400, 360, 90, "alt", [
        Line("allow-client-to-server", 12, 700, "#111827"),
        Line("scoped: client → server:8080 only", 10.5, 700, "#14532d"),
    ])
    c.connector(480, 350, 480, 400, "alt")
    c.node_box(60, 520, 840, 60, "neutral", [
        Line("Result: client → server:8080 restored to 200 OK; every other path in the namespace remains denied by default", 11.5, 400, "#374151"),
    ])
    c.legend(60, 470, [("mgmt", "Pod"), ("warn", "Default-deny (negative test)"), ("alt", "Scoped allow rule")])
    c.save(f"{OUT}/chapter-04-networkpolicy-default-deny-topology.svg")


def ch05():
    c = Canvas(960, 660,
        title="Chapter 5 Hands-On Lab: StatefulSet Per-Ordinal PVCs and Reclaim Behavior",
        subtitle="A recreated pod reattaches its own volume; deleting the PVC directly is what actually destroys the data",
        svg_title="Chapter 5 lab topology: a StatefulSet's stable per-ordinal storage identity, tested through pod, controller, and PVC deletion",
        svg_desc="data-svc-0 and data-svc-1 each write their own hostname identity to their own PVC "
                  "(data-data-svc-0, data-data-svc-1), both Bound. Deleting data-svc-1's pod directly causes the "
                  "StatefulSet controller to recreate it reattached to the same PVC — the identity file still "
                  "reads data-svc-1, not empty. As a negative test, the StatefulSet itself is deleted with "
                  "--cascade=orphan; both PVCs and their bound PVs survive the controller's own deletion, "
                  "preserved by persistentVolumeClaimRetentionPolicy. Only deleting a PVC directly afterward "
                  "actually destroys or releases its bound PV, demonstrating that reclaim policy governs PVC "
                  "deletion specifically, not StatefulSet deletion.")
    c.node_box(60, 140, 240, 110, "mgmt", [
        Line("data-svc-0", 13, 700, "#111827"),
        Line("PVC: data-data-svc-0 (Bound)", 10.5, 400, "#374151"),
        Line("identity: data-svc-0", 10.5, 400, "#374151"),
    ])
    c.node_box(360, 140, 240, 110, "mgmt", [
        Line("data-svc-1", 13, 700, "#111827"),
        Line("PVC: data-data-svc-1 (Bound)", 10.5, 400, "#374151"),
        Line("pod deleted → same PVC reattached", 10, 400, "#374151"),
    ])
    c.connector(600, 195, 700, 195, "alt", label="StatefulSet deleted --cascade=orphan")
    c.node_box(700, 140, 220, 110, "alt", [
        Line("Orphaned PVCs/PVs", 12.5, 700, "#111827"),
        Line("both survive controller deletion", 10.5, 700, "#14532d"),
    ])
    c.node_box(360, 340, 300, 120, "warn", [
        Line("Negative Test", 12, 700, "#7f1d1d"),
        Line("kubectl delete pvc data-data-svc-1", 10.5, 700, "#7f1d1d"),
        Line("bound PV removed or Released", 10.5, 700, "#7f1d1d"),
        Line("(the actual destructive step)", 10, 400, "#7f1d1d"),
    ])
    c.connector(810, 250, 510, 340, "warn")
    c.legend(60, 540, [("mgmt", "Stable per-ordinal identity"), ("alt", "Reclaim-policy-protected"), ("warn", "Direct PVC deletion (destructive)")])
    c.save(f"{OUT}/chapter-05-statefulset-pvc-reclaim-topology.svg")


def ch06():
    c = Canvas(960, 660,
        title="Chapter 6 Hands-On Lab: RBAC, Pod Security Admission Escalation, and a Composable CEL Policy",
        subtitle="A pod that satisfies restricted Pod Security is still independently blocked for missing a memory limit",
        svg_title="Chapter 6 lab flow: RBAC least privilege, Pod Security admission raised from audit to enforce, and a ValidatingAdmissionPolicy negative test",
        svg_desc="ServiceAccount reader is bound to a Role permitting only get/list/watch on ConfigMaps; "
                  "kubectl auth can-i confirms yes for ConfigMaps and no for Secrets. The namespace is labeled for "
                  "Pod Security admission in audit/warn=restricted first: a non-compliant pod is created but "
                  "flagged, not blocked. Raising enforce=restricted then rejects a second non-compliant pod "
                  "outright. As a negative test, a ValidatingAdmissionPolicy requiring every container to declare "
                  "a memory limit is applied; a pod that fully satisfies restricted Pod Security (non-root, "
                  "dropped capabilities, seccomp) but omits the memory limit is still rejected, citing the CEL "
                  "policy — demonstrating that admission controls compose rather than substitute for one another.")
    c.node_box(60, 130, 240, 100, "mgmt", [
        Line("ServiceAccount: reader", 12.5, 700, "#111827"),
        Line("can-i configmaps: yes", 10.5, 700, "#14532d"),
        Line("can-i secrets: no", 10.5, 700, "#7f1d1d"),
    ])
    c.node_box(360, 130, 240, 100, "alt", [
        Line("Pod Security: audit/warn", 12, 700, "#111827"),
        Line("noncompliant pod: created", 10.5, 400, "#374151"),
        Line("(flagged, not blocked)", 10.5, 400, "#374151"),
    ])
    c.node_box(660, 130, 240, 100, "alt", [
        Line("Pod Security: enforce", 12, 700, "#111827"),
        Line("noncompliant-2: rejected", 10.5, 700, "#14532d"),
        Line("outright, at admission", 10.5, 400, "#374151"),
    ])
    c.connector(300, 180, 360, 180, "mgmt")
    c.connector(600, 180, 660, 180, "alt")
    c.node_box(60, 320, 840, 150, "warn", [
        Line("Negative Test — ValidatingAdmissionPolicy", 12.5, 700, "#7f1d1d"),
        Line("require-memory-limit VAP: every container must declare resources.limits.memory (CEL expression)", 11, 400, "#7f1d1d"),
        Line("no-limit-pod: non-root, seccomp RuntimeDefault, capabilities dropped — fully satisfies restricted PSS", 11, 400, "#7f1d1d"),
        Line("still rejected: \"Every container must declare a memory limit.\" — independent, composable controls", 11, 400, "#7f1d1d"),
    ])
    c.legend(60, 550, [("mgmt", "RBAC-scoped identity"), ("alt", "Pod Security admission"), ("warn", "Independent CEL policy (negative test)")])
    c.save(f"{OUT}/chapter-06-rbac-pod-security-vap-flow.svg")


def ch07():
    c = Canvas(960, 660,
        title="Chapter 7 Hands-On Lab: Argo CD GitOps Self-Healing, Blocked by an Independent Signature Policy",
        subtitle="Argo CD reverts manual drift automatically, but Kyverno still blocks pods whose image was never signed",
        svg_title="Chapter 7 lab flow: Argo CD GitOps self-healing reconciliation, with an independent Kyverno image-signature policy blocking admission",
        svg_desc="Argo CD's demo-api Application, synced from a local Git repository with automated sync and "
                  "self-heal enabled, reaches Synced/Healthy. Manually scaling the deployment to 5 replicas "
                  "directly against the cluster (bypassing Git) is reverted back to the Git-declared value of 2 "
                  "within about 30 seconds — self-healing reconciliation. As a negative test, a Kyverno policy "
                  "requiring every pod's image to carry a valid cosign signature from a deliberately impossible "
                  "signer identity is applied; restarting the deployment causes the new ReplicaSet's pods to be "
                  "rejected at admission with 'image verification failed', even though Argo CD's Application still "
                  "reports the manifest as Synced — GitOps sync success and admission-time policy enforcement are "
                  "independent controls.")
    c.node_box(60, 140, 220, 110, "mgmt", [
        Line("Local Git repo", 12.5, 700, "#111827"),
        Line("app/deployment.yaml", 10.5, 400, "#374151"),
        Line("replicas: 2 (declared)", 10.5, 400, "#374151"),
    ])
    c.node_box(370, 140, 220, 110, "alt", [
        Line("Argo CD Application", 12.5, 700, "#111827"),
        Line("Synced / Healthy", 10.5, 700, "#14532d"),
        Line("automated: prune+selfHeal", 10.5, 400, "#374151"),
    ])
    c.connector(280, 195, 370, 195, "mgmt")
    c.node_box(680, 140, 220, 110, "warn", [
        Line("Manual drift", 12.5, 700, "#111827"),
        Line("kubectl scale → replicas=5", 10.5, 700, "#7f1d1d"),
        Line("self-heal reverts to 2 (~30s)", 10.5, 700, "#14532d"),
    ])
    c.connector(590, 195, 680, 195, "warn")
    c.node_box(60, 340, 840, 150, "warn", [
        Line("Negative Test — Kyverno Signature Policy", 12.5, 700, "#7f1d1d"),
        Line("require-signed-images-lab: every pod image must carry a cosign signature from an impossible signer", 11, 400, "#7f1d1d"),
        Line("deployment restart → new ReplicaSet's pods rejected: \"image verification failed\" (FailedCreate)", 11, 400, "#7f1d1d"),
        Line("Argo CD Application still shows Synced — GitOps sync and admission policy enforcement are independent", 11, 400, "#7f1d1d"),
    ])
    c.legend(60, 570, [("mgmt", "Declared source of truth"), ("alt", "GitOps-reconciled state"), ("warn", "Drift / admission-blocked")])
    c.save(f"{OUT}/chapter-07-argocd-selfheal-kyverno-signature-flow.svg")


def ch08():
    c = Canvas(960, 660,
        title="Chapter 8 Hands-On Lab: A Minimal Platform CRD, Self-Service Claims, and Tenant Quota Enforcement",
        subtitle="A WebService claim reconciles into a running Deployment; a second, oversized claim is blocked by the shared ResourceQuota",
        svg_title="Chapter 8 lab flow: a WebService CRD reconciled by a shell-based operator, with a tenant ResourceQuota blocking an over-limit claim",
        svg_desc="A WebService CustomResourceDefinition and a bash reconciliation loop stand in for a compiled "
                  "operator, watching WebService objects and creating matching Deployments. A hello-service claim "
                  "(image + replicas: 2) reconciles to status ready:true and a running 2-replica Deployment — the "
                  "same watch-and-reconcile contract a real operator implements. A tenant ResourceQuota (pods: "
                  "\"3\") is then applied to the team-payments namespace. As a negative test, a second claim "
                  "(oversized-service, replicas: 5) is accepted by the CRD but its ReplicaSet cannot bring all "
                  "pods up — events show 'exceeded quota: tenant-quota' once existing plus new pods would cross "
                  "the pods: 3 ceiling, demonstrating that tenant isolation is enforced by the shared quota "
                  "regardless of what the self-service claim requested.")
    c.node_box(60, 130, 240, 100, "mgmt", [
        Line("WebService CRD", 12.5, 700, "#111827"),
        Line("+ bash reconcile.sh loop", 10.5, 400, "#374151"),
    ])
    c.node_box(360, 130, 240, 100, "alt", [
        Line("hello-service claim", 12.5, 700, "#111827"),
        Line("image + replicas: 2", 10.5, 400, "#374151"),
        Line("status: ready=true", 10.5, 700, "#14532d"),
    ])
    c.connector(300, 180, 360, 180, "mgmt")
    c.node_box(660, 130, 240, 100, "neutral", [
        Line("tenant-quota", 12.5, 700, "#111827"),
        Line("ResourceQuota: pods \"3\"", 10.5, 400, "#374151"),
    ])
    c.connector(600, 180, 660, 180, "alt")
    c.node_box(60, 320, 840, 150, "warn", [
        Line("Negative Test", 12.5, 700, "#7f1d1d"),
        Line("oversized-service claim: image + replicas: 5, submitted to the same team-payments namespace", 11, 400, "#7f1d1d"),
        Line("Deployment created, but ReplicaSet cannot bring all 5 pods up", 11, 400, "#7f1d1d"),
        Line("events: \"exceeded quota: tenant-quota, requested: pods=1, used: pods=3, limited: pods=3\"", 11, 700, "#7f1d1d"),
    ])
    c.node_box(60, 500, 840, 60, "neutral", [
        Line("tenant isolation is enforced by the shared ResourceQuota, regardless of what the self-service claim requested", 11.5, 400, "#374151"),
    ])
    c.legend(60, 590, [("mgmt", "Platform CRD/operator"), ("alt", "Reconciled claim"), ("warn", "Quota-blocked claim")])
    c.save(f"{OUT}/chapter-08-platform-crd-tenant-quota-flow.svg")


def ch09():
    c = Canvas(960, 660,
        title="Chapter 9 Hands-On Lab: Scoped Chaos Respects the PDB; an Over-Broad Selector Bypasses It",
        subtitle="A single-pod kill stays above minAvailable; killing all pods at once drops replicas to zero despite the PDB",
        svg_title="Chapter 9 lab topology: a Prometheus-observed workload tested with a scoped Chaos Mesh experiment and an over-broad negative test",
        svg_desc="demo-api runs 3 replicas with a PodDisruptionBudget requiring minAvailable 2, observed by "
                  "kube-state-metrics through Prometheus. A tightly scoped Chaos Mesh PodChaos experiment "
                  "(mode: one) kills exactly one demo-api pod; a replacement schedules within seconds and total "
                  "pod count never drops below 2, consistent with the PDB. As a negative test, an over-broad "
                  "experiment (mode: all) force-kills all three demo-api pods nearly simultaneously, briefly "
                  "dropping available replicas to 0 despite the minAvailable 2 PDB — because PodChaos kills pods "
                  "directly rather than through the API server's eviction subresource that PDBs actually govern; "
                  "PDBs protect only voluntary, eviction-based disruption, not this kind of direct chaos action.")
    c.node_box(60, 130, 220, 90, "neutral", [
        Line("Prometheus stack", 12.5, 700, "#111827"),
        Line("kube-state-metrics: replicas=3", 10.5, 400, "#374151"),
    ])
    c.node_box(370, 130, 220, 90, "mgmt", [
        Line("demo-api (3 replicas)", 12.5, 700, "#111827"),
        Line("PDB: minAvailable 2", 10.5, 400, "#374151"),
    ])
    c.connector(280, 175, 370, 175, "neutral")
    c.node_box(660, 130, 240, 90, "alt", [
        Line("Scoped chaos: mode: one", 12, 700, "#111827"),
        Line("1 pod killed, replaced fast", 10.5, 700, "#14532d"),
        Line("never below 2 (PDB respected)", 10.5, 400, "#374151"),
    ])
    c.connector(590, 175, 660, 175, "alt")
    c.node_box(60, 320, 840, 150, "warn", [
        Line("Negative Test — mode: all", 12.5, 700, "#7f1d1d"),
        Line("PodChaos force-kills all 3 demo-api pods nearly simultaneously (direct kill, not eviction)", 11, 400, "#7f1d1d"),
        Line("available replicas briefly drop to 0, despite minAvailable: 2 — the PDB never engages", 11, 400, "#7f1d1d"),
        Line("PDBs govern the eviction subresource only; they do not protect against direct force-kill actions", 11, 400, "#7f1d1d"),
    ])
    c.node_box(60, 500, 840, 60, "neutral", [
        Line("Experiment deleted immediately after observation; recovery time compared against the scoped mode: one run", 11.5, 400, "#374151"),
    ])
    c.legend(60, 590, [("mgmt", "PDB-governed workload"), ("alt", "Scoped chaos (respects PDB)"), ("warn", "Over-broad chaos (bypasses PDB)")])
    c.save(f"{OUT}/chapter-09-chaos-mesh-pdb-scope-topology.svg")


ch01(); ch02(); ch03(); ch04(); ch05(); ch06(); ch07(); ch08(); ch09()
