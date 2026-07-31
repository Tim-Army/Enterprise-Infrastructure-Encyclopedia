# Chapter 08: Beyond Pods — HostEndpoints and NetworkSets

## Learning Objectives

- Govern flows to an endpoint *outside* the cluster with a `NetworkSet` and a `GlobalNetworkPolicy`.
- Understand how a `HostEndpoint` extends Calico policy to the node itself, and why failsafe ports matter.
- Validate the external-endpoint control.

## The problem restated

Every other lab in this series ends with the agentless PLC — a device that runs no agent. In Kubernetes the analog is an endpoint Calico does **not** run a CNI on: something **outside the cluster**. A pod cannot be the only kind of thing you segment; real estates have external databases, SaaS endpoints, and OT devices on the wire. Calico governs those with **NetworkSets** (named groups of external IPs/CIDRs) and enforces policy for the node itself with **HostEndpoints**.

## Hands-On Lab

### Lab 8.1 — Govern egress to an external "PLC" with a NetworkSet

**Objective.** Treat an external device as the agentless PLC and permit only `hmi` to reach it, cluster-wide.

**Walkthrough**

**Step 1.** Define the external PLC as a `GlobalNetworkSet` (substitute the real device IP; here a documentation address stands in):

```bash
calicoctl apply -f - <<'EOF'
apiVersion: projectcalico.org/v3
kind: GlobalNetworkSet
metadata:
  name: external-plc
  labels: { role: external-plc }
spec:
  nets: [ "203.0.113.50/32" ]
EOF
```

**Step 2.** Write an egress guardrail: only `app=hmi` may reach the external PLC on 502; no other pod may reach it at all:

```bash
calicoctl apply -f - <<'EOF'
apiVersion: projectcalico.org/v3
kind: GlobalNetworkPolicy
metadata: { name: security.external-plc }
spec:
  tier: security
  order: 20
  selector: all()
  types: [ Egress ]
  egress:
    - action: Allow
      source: { selector: app == 'hmi' }
      destination: { selector: role == 'external-plc', ports: [ 502 ] }
    - action: Deny
      destination: { selector: role == 'external-plc' }
    - action: Allow      # do not disturb any other egress (DNS, cluster, internet)
EOF
```

**Step 3.** Confirm the intent from the policy model (the external IP is not reachable in the lab, so verify by policy, not by packet): only `app=hmi` egress to `role==external-plc:502` is Allowed; every other pod's egress to it is Denied; all other egress is untouched.

```bash
calicoctl get globalnetworkpolicy security.external-plc -o yaml | grep -A3 "destination:"
```

**Expected result.** A cluster-wide egress rule that authorizes only the operator to reach the external PLC, on Modbus only, and forbids every other workload — the Kubernetes-native version of "only the HMI talks to the PLC," extended to a device Calico does not run on.

**Negative test.** Remove the trailing `Allow` and every pod's DNS and internet egress breaks, because the policy now denies-by-default on egress for `all()`. The trailing `Allow` is what scopes the guardrail to the PLC and leaves everything else alone. Restore it.

**Cleanup.** Keep the external-PLC guardrail.

### Lab 8.2 — HostEndpoints: policy for the node itself

**Objective.** Understand how Calico extends policy to the node, and why you must respect failsafe ports.

**Walkthrough**

**Step 1.** List the automatic host endpoints (Calico can manage the node's own interfaces):

```bash
calicoctl get heps -o wide 2>/dev/null || echo "no HostEndpoints configured yet"
```

**Step 2.** Understand the model without locking yourself out. A `HostEndpoint` applies `GlobalNetworkPolicy` (with `applyOnForward`) to traffic to/from the **node**, letting Calico protect the host the same way it protects pods — the closest Kubernetes analog to the host-agent platforms in this series enforcing on a server's own firewall.

> **Caution — read before applying a HostEndpoint.** On a single-node kind cluster, a HostEndpoint with a restrictive policy and no allowances can sever the Kubernetes control plane and lock you out of your own cluster. Calico mitigates this with **failsafe ports** (by default it always permits SSH, DNS, the Kubernetes API, BGP, and etcd inbound/outbound), but you must still explicitly allow anything else the node needs. For that reason, treat HostEndpoint enforcement as a production capability to design carefully rather than something to switch on casually in a single-node lab.

**Step 3 — Design Exercise.** Write the `HostEndpoint` and a `GlobalNetworkPolicy` you *would* apply to a real worker node to permit only the node's required services (kubelet, NodePorts you use) and deny the rest — and list which failsafe ports keep you from being locked out while you do.

**Expected result.** A clear understanding that Calico policy is not limited to pods: it reaches the node, with failsafe ports as the safety net.

**Negative test.** Apply an all-deny HostEndpoint policy on the single kind node without allowing the API server and you lose `kubectl` to the cluster; only failsafe ports (and a cluster rebuild) save you. This is why the step above is a design exercise, not a live apply.

**Cleanup.** No HostEndpoint was applied; nothing to undo.

### Lab 8.3 — Validate the whole segmentation

**Objective.** Confirm the end state.

**Walkthrough**

```bash
kubectl exec -n dc web -- nc -z -w2 db.dc 5432 && echo "web -> db  ALLOWED"
kubectl exec -n ot hmi -- nc -z -w2 plc.ot 502 && echo "hmi -> plc ALLOWED"
kubectl exec -n ot hmi -- nc -z -w2 db.dc 5432 || echo "hmi -> db  BLOCKED"
kubectl exec -n dc web -- nc -z -w2 plc.ot 502 || echo "web -> plc BLOCKED"
```

**Expected result.**

| Flow | Before (Chapter 05) | After |
|:---|:---|:---|
| web→db 5432 | REACH | **ALLOWED** (label policy) |
| hmi→plc 502 | REACH | **ALLOWED** (label policy) |
| hmi→db 5432 | REACH | **BLOCKED** (namespace + security tier) |
| web→plc 502 | REACH | **BLOCKED** (default-deny) |
| any→external-plc 502 | n/a | **only hmi**, cluster-wide |

Both legitimate flows work; the lateral movement is blocked in two independent places (the namespace policy and the security tier); and even an external device is governed by identity, not address.

**Negative test.** Delete the `security` tier policy and re-test `hmi → db`; it stays blocked by the namespace policy. Two independent controls is defense in depth — either alone would stop the attack, and removing one does not open the hole.

**Cleanup.** Leave the policies for Chapter 09.

## Summary and Completion Checklist

- [ ] An external endpoint governed by a `NetworkSet` + `GlobalNetworkPolicy`, reachable only by the HMI.
- [ ] The `HostEndpoint` model and failsafe ports understood (as a design exercise, not a live lock-out).
- [ ] End-to-end validation table reproduced.
- [ ] You can explain how Calico segments beyond pods.
