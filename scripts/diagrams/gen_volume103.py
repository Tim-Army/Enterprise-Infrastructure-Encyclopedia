#!/usr/bin/env python3
"""Volume CIII (Istio Build-It-Yourself Lab) topology diagram.

Chapter 1 (Lab Overview and Topology): a single Linux host running a kind
Kubernetes cluster with the Istio service mesh. Meshed workloads (each with
an Envoy sidecar and a SPIFFE identity from its ServiceAccount) are web, api,
and db in namespace dc, and hmi in namespace ot; the plc in ot is un-meshed.
mTLS secures mesh traffic; AuthorizationPolicy authorizes by principal at L4
and L7 and denies the hmi-to-db lateral movement.

Run from scripts/diagrams:  python3 gen_volume103.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-103-istio-lab"


def ch01():
    c = Canvas(960, 480,
        title="Chapter 1 Lab Topology: Kubernetes Microsegmentation with the Istio Service Mesh",
        subtitle="Envoy sidecars give each workload a SPIFFE identity; mTLS everywhere; AuthorizationPolicy authorizes by principal at L4 and L7; the PLC is un-meshed",
        svg_title="Chapter 1 lab topology: a kind Kubernetes cluster with the Istio service mesh, meshed workloads with sidecars and one un-meshed PLC",
        svg_desc="A single Linux host runs Docker, kind, kubectl, and istioctl. Inside it a kind Kubernetes cluster "
                 "runs the Istio control plane, istiod. Namespace dc (data center) holds web (ServiceAccount "
                 "sa-web), api (sa-api, an HTTP service), and db (sa-db, PostgreSQL on 5432); each has an injected "
                 "Envoy sidecar and a SPIFFE identity. Namespace ot (operations) holds hmi (sa-hmi, meshed) and plc "
                 "(app=plc, a Modbus listener on 502) which is deliberately un-meshed with no sidecar. Istio requires "
                 "mutual TLS across the mesh and authorizes by principal: web to db on 5432 at Layer 4, web to api "
                 "restricted to HTTP GET /get at Layer 7 with POST denied, and hmi to the un-meshed plc via egress. "
                 "The compromised-hmi-to-db flow is denied because the sa-hmi principal is not authorized. Because "
                 "the plc is un-meshed, Istio cannot enforce on it directly, so a CNI network policy is paired with "
                 "the mesh.")

    c.node_box(60, 54, 840, 34, "mgmt", [
        Line("Single Linux host · Docker + kind + kubectl + istioctl", 10.5, 700, "#111827"),
    ])
    c.plane_bar(60, 100, 840, 26, "neutral",
                "kind Kubernetes cluster · Istio control plane (istiod) · Envoy sidecars · mTLS + AuthorizationPolicy by principal (SPIFFE)")

    # namespace dc: web + db (top row), api (second row)
    c.plane_bar(70, 156, 300, 24, "alt", "namespace: dc  (istio-injection)")
    c.node_box(85, 190, 130, 60, "neutral", [
        Line("web  +sidecar", 11, 700, "#111827"),
        Line("sa-web", 9.5, 700, "#166534"),
        Line("client", 9, 400, "#374151"),
    ])
    c.node_box(232, 190, 130, 60, "data", [
        Line("db  +sidecar", 11, 700, "#111827"),
        Line("sa-db · :5432", 9, 700, "#7f1d1d"),
        Line("PostgreSQL", 8.5, 400, "#374151"),
    ])
    c.node_box(158, 268, 140, 60, "data", [
        Line("api  +sidecar", 11, 700, "#111827"),
        Line("sa-api", 9.5, 700, "#166534"),
        Line("HTTP :8080", 9, 700, "#374151"),
    ])
    c.connector(215, 220, 232, 220, "alt", label="5432 (mTLS, L4 by principal)", label_pos=(140, 292))
    c.connector(150, 250, 210, 268, "alt", label="HTTP: GET /get allowed · POST denied (L7)", label_pos=(150, 348))

    # namespace ot: hmi (meshed) + plc (un-meshed)
    c.plane_bar(500, 156, 380, 24, "data", "namespace: ot  (hmi meshed, plc un-meshed)")
    c.node_box(520, 190, 150, 60, "neutral", [
        Line("hmi  +sidecar", 11, 700, "#111827"),
        Line("sa-hmi", 9.5, 700, "#166534"),
        Line("operator", 9, 400, "#374151"),
    ])
    c.node_box(700, 190, 150, 60, "data", [
        Line("plc  NO sidecar", 11, 700, "#111827"),
        Line("app=plc · :502", 9, 700, "#7c2d12"),
        Line("un-meshed", 9, 400, "#374151"),
    ], dashed=True)
    c.connector(670, 220, 700, 220, "alt", label="502 (egress)", label_pos=(650, 292))

    # cross-namespace lateral movement (denied by principal)
    c.connector(520, 300, 372, 300, "warn", label="hmi → db DENIED (sa-hmi principal not authorized)", label_pos=(360, 328))

    c.legend(70, 392, [
        ("alt", "Allowed (mTLS + authz)"),
        ("warn", "Lateral movement (denied)"),
        ("neutral", "Meshed pod (sidecar)"),
    ])
    c.save(f"{OUT}/chapter-01-lab-topology.svg")


if __name__ == "__main__":
    ch01()
