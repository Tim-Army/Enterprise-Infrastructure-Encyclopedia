#!/usr/bin/env python3
"""Volume CV (HashiCorp Consul Build-It-Yourself Lab) topology diagram.

Chapter 1 (Lab Overview and Topology): a single Linux host running a kind
Kubernetes cluster with HashiCorp Consul. Meshed services (each with a Consul
Connect sidecar and a SPIFFE identity) are web, api, db, and hmi; the plc is
un-meshed. Service intentions authorize web to db and api and deny the
hmi-to-db lateral movement. Consul's signature: a service on a VM joins the
SAME mesh and obeys the SAME intentions.

Run from scripts/diagrams:  python3 gen_volume105.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-105-consul-lab"


def ch01():
    c = Canvas(960, 500,
        title="Chapter 1 Lab Topology: Multi-Platform Microsegmentation with HashiCorp Consul",
        subtitle="Consul Connect gives each service a SPIFFE identity and mTLS; service intentions authorize by service; the same mesh and intentions span Kubernetes and VMs",
        svg_title="Chapter 1 lab topology: a kind Kubernetes cluster with HashiCorp Consul, meshed services and one un-meshed PLC, plus a VM joining the same mesh",
        svg_desc="A single Linux host runs Docker, kind, kubectl, helm, and the consul CLI. Inside it a kind "
                 "Kubernetes cluster runs Consul servers and Connect. Meshed services web (ServiceAccount web), api "
                 "(api, an HTTP service on 8080), db (db, PostgreSQL on 5432), and hmi (hmi, the operator) each have "
                 "a Consul Connect sidecar and a SPIFFE identity; plc (app=plc, a Modbus listener on 502) is "
                 "un-meshed. Consul secures mesh traffic with mutual TLS and authorizes with service intentions: a "
                 "default-deny wildcard plus exact allows permits web to db on 5432 and web to api on 8080, with an "
                 "L7 intention restricting the api to HTTP GET /get; the compromised-hmi-to-db flow is denied because "
                 "no intention allows it. Consul's defining trait is multi-platform reach: a service running on a VM "
                 "runs a Consul dataplane, joins the same mesh, and obeys the same intentions as the Kubernetes "
                 "services. The un-meshed plc still needs a CNI network policy beneath the mesh.")

    c.node_box(60, 54, 840, 34, "mgmt", [
        Line("Single Linux host · Docker + kind + kubectl + helm + consul", 10.5, 700, "#111827"),
    ])
    c.plane_bar(60, 100, 840, 26, "neutral",
                "kind Kubernetes cluster · Consul servers + Connect · mTLS + service intentions (SPIFFE identity)")

    # Kubernetes meshed services: web + db (top row), api (second row)
    c.plane_bar(70, 156, 300, 24, "alt", "Kubernetes services  (Consul Connect)")
    c.node_box(85, 190, 130, 60, "neutral", [
        Line("web  +sidecar", 11, 700, "#111827"),
        Line("svc: web", 9.5, 700, "#166534"),
        Line("client", 9, 400, "#374151"),
    ])
    c.node_box(232, 190, 130, 60, "data", [
        Line("db  +sidecar", 11, 700, "#111827"),
        Line("svc: db · :5432", 9, 700, "#7f1d1d"),
        Line("PostgreSQL", 8.5, 400, "#374151"),
    ])
    c.node_box(158, 268, 140, 60, "data", [
        Line("api  +sidecar", 11, 700, "#111827"),
        Line("svc: api", 9.5, 700, "#166534"),
        Line("HTTP :8080", 9, 700, "#374151"),
    ])
    c.connector(215, 220, 232, 220, "alt", label="5432 (mTLS, intention allow)", label_pos=(140, 292))
    c.connector(150, 250, 210, 268, "alt", label="8080 (L7 intention: GET /get)", label_pos=(150, 346))

    # operator + un-meshed PLC
    c.plane_bar(500, 156, 380, 24, "data", "operator (meshed) + un-meshed PLC")
    c.node_box(520, 190, 150, 60, "neutral", [
        Line("hmi  +sidecar", 11, 700, "#111827"),
        Line("svc: hmi", 9.5, 700, "#166534"),
        Line("operator", 9, 400, "#374151"),
    ])
    c.node_box(700, 190, 150, 60, "data", [
        Line("plc  NO sidecar", 11, 700, "#111827"),
        Line("app=plc · :502", 9, 700, "#7c2d12"),
        Line("un-meshed", 9, 400, "#374151"),
    ], dashed=True)
    c.connector(670, 220, 700, 220, "alt", label="502 (needs CNI policy)", label_pos=(640, 292))

    # cross-service lateral movement (denied by intention)
    c.connector(520, 300, 372, 300, "warn", label="hmi → db DENIED (no intention allows it)", label_pos=(365, 328))

    # multi-platform: a VM joins the same mesh
    c.raw('<line x1="480" y1="180" x2="480" y2="372" stroke="#33415c" stroke-width="1.2" stroke-dasharray="4 3"/>')
    c.node_box(300, 372, 360, 40, "mgmt", [
        Line("VM service · Consul dataplane · joins the SAME mesh, SAME intentions", 9.5, 700, "#111827"),
    ])

    c.legend(70, 428, [
        ("alt", "Allowed (mTLS + intention)"),
        ("warn", "Lateral movement (denied)"),
        ("mgmt", "Multi-platform reach (VM)"),
    ])
    c.save(f"{OUT}/chapter-01-lab-topology.svg")


if __name__ == "__main__":
    ch01()
