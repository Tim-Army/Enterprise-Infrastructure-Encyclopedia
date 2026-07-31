#!/usr/bin/env python3
"""Volume CI (Calico Build-It-Yourself Lab) topology diagram.

Chapter 1 (Lab Overview and Topology): a single Linux host running a kind
Kubernetes cluster with the Calico CNI. Two namespaces, dc and ot, hold four
pods -- web and db in dc, hmi and plc in ot. Calico policy permits web->db on
5432 and hmi->plc on 502 and denies the compromised-hmi-to-db cross-namespace
lateral movement. Calico also protects the node with a HostEndpoint and
external endpoints with NetworkSets.

Run from scripts/diagrams:  python3 gen_volume101.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-101-calico-lab"


def ch01():
    c = Canvas(960, 480,
        title="Chapter 1 Lab Topology: Kubernetes Microsegmentation with Calico",
        subtitle="A kind cluster with the Calico CNI; label-based NetworkPolicy allows web->db and hmi->plc and denies the cross-namespace hmi->db lateral movement",
        svg_title="Chapter 1 lab topology: a kind Kubernetes cluster with Calico, four pods across two namespaces segmented by label-based policy",
        svg_desc="A single Linux host (an Ubuntu VM, a cloud VM, or WSL2) runs Docker, kind, kubectl, and "
                 "calicoctl. Inside it a kind Kubernetes cluster uses the Calico CNI as its dataplane and policy "
                 "engine. Two namespaces hold four pods. Namespace dc (data center) holds web (label app=web, a "
                 "client) and db (label app=db, PostgreSQL on 5432). Namespace ot (operations) holds hmi (label "
                 "app=hmi, the operator) and plc (label app=plc, a Modbus listener on 502). Calico policy permits "
                 "web to db on TCP 5432 and hmi to plc on TCP 502, and denies the compromised-hmi-to-db "
                 "cross-namespace flow on 5432, which is the lateral movement. Calico also protects the cluster "
                 "node itself with a HostEndpoint and governs flows to endpoints outside the cluster with "
                 "NetworkSets.")

    c.node_box(60, 56, 840, 36, "mgmt", [
        Line("Single Linux host · Ubuntu 22.04 VM / cloud VM / WSL2 · Docker + kind + kubectl + calicoctl", 10.5, 700, "#111827"),
    ])
    c.plane_bar(60, 104, 840, 26, "neutral",
                "kind Kubernetes cluster · CNI = Calico · a HostEndpoint protects the node, NetworkSets govern external endpoints")

    # namespace dc
    c.plane_bar(80, 162, 380, 26, "alt", "namespace: dc  (data center)")
    c.node_box(100, 204, 160, 74, "neutral", [
        Line("web", 13, 700, "#111827"),
        Line("app=web", 10, 700, "#166534"),
        Line("client", 9.5, 400, "#374151"),
    ])
    c.node_box(290, 204, 160, 74, "data", [
        Line("db", 13, 700, "#111827"),
        Line("app=db", 10, 700, "#166534"),
        Line("PostgreSQL :5432", 9.5, 700, "#7f1d1d"),
    ])
    c.connector(260, 241, 290, 241, "alt", label="5432", label_pos=(258, 300))

    # namespace ot
    c.plane_bar(500, 162, 380, 26, "data", "namespace: ot  (operations)")
    c.node_box(520, 204, 160, 74, "neutral", [
        Line("hmi", 13, 700, "#111827"),
        Line("app=hmi", 10, 700, "#166534"),
        Line("operator", 9.5, 400, "#374151"),
    ])
    c.node_box(710, 204, 160, 74, "data", [
        Line("plc", 13, 700, "#111827"),
        Line("app=plc", 10, 700, "#7c2d12"),
        Line("Modbus :502", 9.5, 700, "#374151"),
    ], dashed=True)
    c.connector(680, 241, 710, 241, "alt", label="502", label_pos=(688, 300))

    # cross-namespace lateral movement (denied)
    c.connector(520, 320, 450, 320, "warn", label="hmi → db 5432 DENIED (lateral movement)", label_pos=(300, 348))

    c.legend(80, 392, [
        ("alt", "Legitimate flow (allowed)"),
        ("warn", "Lateral movement (denied)"),
        ("neutral", "Pod (app label)"),
    ])
    c.save(f"{OUT}/chapter-01-lab-topology.svg")


if __name__ == "__main__":
    ch01()
