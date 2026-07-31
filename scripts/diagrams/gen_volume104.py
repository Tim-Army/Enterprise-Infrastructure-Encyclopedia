#!/usr/bin/env python3
"""Volume CIV (Linkerd Build-It-Yourself Lab) topology diagram.

Chapter 1 (Lab Overview and Topology): a single Linux host running a kind
Kubernetes cluster with the Linkerd service mesh. Meshed workloads (each with
a Linkerd micro-proxy and a ServiceAccount identity) are web, api, and db in
namespace dc, and hmi in namespace ot; the plc in ot is un-meshed. Automatic
mTLS secures mesh traffic; a Server plus AuthorizationPolicy allows web to db
and api by identity and denies the hmi-to-db lateral movement.

Run from scripts/diagrams:  python3 gen_volume104.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-104-linkerd-lab"


def ch01():
    c = Canvas(960, 470,
        title="Chapter 1 Lab Topology: Kubernetes Microsegmentation with the Linkerd Service Mesh",
        subtitle="Rust micro-proxies give each workload a ServiceAccount identity; automatic zero-config mTLS; Server + AuthorizationPolicy authorize by identity; the PLC is un-meshed",
        svg_title="Chapter 1 lab topology: a kind Kubernetes cluster with the Linkerd service mesh, meshed workloads with proxies and one un-meshed PLC",
        svg_desc="A single Linux host runs Docker, kind, kubectl, and the linkerd CLI. Inside it a kind Kubernetes "
                 "cluster runs the Linkerd control plane. Namespace dc (data center) holds web (ServiceAccount "
                 "sa-web), api (sa-api, an HTTP service), and db (sa-db, PostgreSQL on 5432); each has an injected "
                 "Linkerd Rust micro-proxy and a ServiceAccount identity. Namespace ot (operations) holds hmi "
                 "(sa-hmi, meshed) and plc (app=plc, a Modbus listener on 502) which is deliberately un-meshed with "
                 "no proxy. Linkerd secures all mesh traffic with automatic zero-configuration mutual TLS and "
                 "authorizes by identity: a Server plus AuthorizationPolicy permits web to db on 5432 and web to "
                 "api on 8080, and hmi to the un-meshed plc via egress. The compromised-hmi-to-db flow is denied "
                 "because the sa-hmi identity is not authorized. Because the plc is un-meshed, Linkerd cannot "
                 "enforce on it, so a CNI network policy is paired with the mesh.")

    c.node_box(60, 54, 840, 34, "mgmt", [
        Line("Single Linux host · Docker + kind + kubectl + linkerd", 10.5, 700, "#111827"),
    ])
    c.plane_bar(60, 100, 840, 26, "neutral",
                "kind Kubernetes cluster · Linkerd control plane · Rust micro-proxies · automatic mTLS + Server/AuthorizationPolicy")

    # namespace dc: web + db (top row), api (second row)
    c.plane_bar(70, 156, 300, 24, "alt", "namespace: dc  (linkerd.io/inject)")
    c.node_box(85, 190, 130, 60, "neutral", [
        Line("web  +proxy", 11, 700, "#111827"),
        Line("sa-web", 9.5, 700, "#166534"),
        Line("client", 9, 400, "#374151"),
    ])
    c.node_box(232, 190, 130, 60, "data", [
        Line("db  +proxy", 11, 700, "#111827"),
        Line("sa-db · :5432", 9, 700, "#7f1d1d"),
        Line("PostgreSQL", 8.5, 400, "#374151"),
    ])
    c.node_box(158, 268, 140, 60, "data", [
        Line("api  +proxy", 11, 700, "#111827"),
        Line("sa-api", 9.5, 700, "#166534"),
        Line("HTTP :8080", 9, 700, "#374151"),
    ])
    c.connector(215, 220, 232, 220, "alt", label="5432 (auto mTLS, by identity)", label_pos=(140, 292))
    c.connector(150, 250, 210, 268, "alt", label="8080 (authorized by sa-web identity)", label_pos=(150, 348))

    # namespace ot: hmi (meshed) + plc (un-meshed)
    c.plane_bar(500, 156, 380, 24, "data", "namespace: ot  (hmi meshed, plc un-meshed)")
    c.node_box(520, 190, 150, 60, "neutral", [
        Line("hmi  +proxy", 11, 700, "#111827"),
        Line("sa-hmi", 9.5, 700, "#166534"),
        Line("operator", 9, 400, "#374151"),
    ])
    c.node_box(700, 190, 150, 60, "data", [
        Line("plc  NO proxy", 11, 700, "#111827"),
        Line("app=plc · :502", 9, 700, "#7c2d12"),
        Line("un-meshed", 9, 400, "#374151"),
    ], dashed=True)
    c.connector(670, 220, 700, 220, "alt", label="502 (egress)", label_pos=(650, 292))

    # cross-namespace lateral movement (denied by identity)
    c.connector(520, 300, 372, 300, "warn", label="hmi → db DENIED (sa-hmi identity not authorized)", label_pos=(360, 328))

    c.legend(70, 392, [
        ("alt", "Allowed (auto mTLS + authz)"),
        ("warn", "Lateral movement (denied)"),
        ("neutral", "Meshed pod (proxy)"),
    ])
    c.save(f"{OUT}/chapter-01-lab-topology.svg")


if __name__ == "__main__":
    ch01()
