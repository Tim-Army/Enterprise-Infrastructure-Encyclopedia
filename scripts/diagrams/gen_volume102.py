#!/usr/bin/env python3
"""Volume CII (Cilium Build-It-Yourself Lab) topology diagram.

Chapter 1 (Lab Overview and Topology): a single Linux host running a kind
Kubernetes cluster with the Cilium CNI (eBPF). Namespace dc holds web
(client), db (PostgreSQL), and api (an HTTP service for the L7 demo);
namespace ot holds hmi (operator) and plc (Modbus). Cilium enforces L3/L4
policy (web->db:5432, hmi->plc:502) and L7 policy (web may only GET /get on
the api), denies the hmi->db lateral movement, and Hubble observes every flow.

Run from scripts/diagrams:  python3 gen_volume102.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-102-cilium-lab"


def ch01():
    c = Canvas(960, 470,
        title="Chapter 1 Lab Topology: Kubernetes Microsegmentation with Cilium (eBPF + L7)",
        subtitle="A kind cluster with the Cilium CNI; identity-based L3/L4 policy plus Layer 7 HTTP and DNS policy, all observed in Hubble",
        svg_title="Chapter 1 lab topology: a kind Kubernetes cluster with Cilium, five pods across two namespaces segmented at L3/L4 and L7",
        svg_desc="A single Linux host runs Docker, kind, kubectl, cilium, and hubble. Inside it a kind Kubernetes "
                 "cluster uses the Cilium CNI with an eBPF dataplane. Namespace dc (data center) holds web (label "
                 "app=web, a client), db (label app=db, PostgreSQL on 5432), and api (label app=api, an HTTP service "
                 "on 8080 used for the Layer 7 demo). Namespace ot (operations) holds hmi (label app=hmi, the "
                 "operator) and plc (label app=plc, a Modbus listener on 502). Cilium permits web to db on TCP 5432 "
                 "and hmi to plc on TCP 502 at Layer 3/4, restricts web to the api at Layer 7 so only HTTP GET /get "
                 "is allowed and POST /post is denied, and denies the compromised-hmi-to-db cross-namespace flow, "
                 "the lateral movement. Hubble observes every flow, its identities, and its verdict.")

    c.node_box(60, 54, 840, 34, "mgmt", [
        Line("Single Linux host · Docker + kind + kubectl + cilium + hubble", 10.5, 700, "#111827"),
    ])
    c.plane_bar(60, 100, 840, 26, "neutral",
                "kind Kubernetes cluster · CNI = Cilium (eBPF) · Hubble observes every flow and verdict")

    # namespace dc: web + db (top row), api (second row)
    c.plane_bar(70, 156, 300, 24, "alt", "namespace: dc  (data center)")
    c.node_box(85, 190, 130, 60, "neutral", [
        Line("web", 12.5, 700, "#111827"),
        Line("app=web", 9.5, 700, "#166534"),
        Line("client", 9, 400, "#374151"),
    ])
    c.node_box(232, 190, 130, 60, "data", [
        Line("db", 12.5, 700, "#111827"),
        Line("app=db", 9.5, 700, "#166534"),
        Line("PostgreSQL :5432", 8.5, 700, "#7f1d1d"),
    ])
    c.node_box(158, 268, 140, 60, "data", [
        Line("api", 12.5, 700, "#111827"),
        Line("app=api", 9.5, 700, "#166534"),
        Line("HTTP :8080", 9, 700, "#374151"),
    ])
    c.connector(215, 220, 232, 220, "alt", label="5432", label_pos=(178, 292))
    c.connector(150, 250, 210, 268, "alt", label="HTTP: GET /get allowed · POST denied (L7)", label_pos=(150, 348))

    # namespace ot: hmi + plc
    c.plane_bar(500, 156, 380, 24, "data", "namespace: ot  (operations)")
    c.node_box(520, 190, 150, 60, "neutral", [
        Line("hmi", 12.5, 700, "#111827"),
        Line("app=hmi", 9.5, 700, "#166534"),
        Line("operator", 9, 400, "#374151"),
    ])
    c.node_box(700, 190, 150, 60, "data", [
        Line("plc", 12.5, 700, "#111827"),
        Line("app=plc", 9.5, 700, "#7c2d12"),
        Line("Modbus :502", 9, 700, "#374151"),
    ], dashed=True)
    c.connector(670, 220, 700, 220, "alt", label="502", label_pos=(678, 292))

    # cross-namespace lateral movement (denied)
    c.connector(520, 300, 372, 300, "warn", label="hmi → db 5432 DENIED (lateral movement)", label_pos=(360, 328))

    c.legend(70, 392, [
        ("alt", "Legitimate flow (allowed)"),
        ("warn", "Lateral movement (denied)"),
        ("neutral", "Pod (app label)"),
    ])
    c.save(f"{OUT}/chapter-01-lab-topology.svg")


if __name__ == "__main__":
    ch01()
