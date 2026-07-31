#!/usr/bin/env python3
"""Volume CVI (Cloud-Native Segmentation Build-It-Yourself Lab) topology diagram.

Chapter 1 (Lab Overview and Topology): the same three-tier estate (web, db,
hmi) built on AWS, Azure, and GCP, segmented with each cloud's native
primitive. AWS uses security groups that reference each other plus a stateless
NACL; Azure uses NSG rules written by Application Security Group; GCP uses
firewall rules targeting a service account. In every column the legitimate
web -> db:5432 flow is allowed and the hmi -> db lateral flow is denied.

Run from scripts/diagrams:  python3 gen_volume106.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-106-cloud-native-segmentation-lab"


def column(c, x, header_style, header, web_id, db_id, hmi_id, primitive):
    """Render one cloud column: web, db, hmi, an allow and a denied flow."""
    c.plane_bar(x, 100, 290, 24, header_style, header)
    c.node_box(x + 8, 140, 125, 56, "neutral", [
        Line(web_id, 11, 700, "#111827"),
        Line("app tier", 9, 400, "#374151"),
    ])
    c.node_box(x + 157, 140, 125, 56, "data", [
        Line(db_id, 11, 700, "#111827"),
        Line("db · :5432", 9, 700, "#7f1d1d"),
    ])
    c.connector(x + 133, 168, x + 157, 168, "alt",
                label="5432 allow", label_pos=(x + 150, 212))
    c.node_box(x + 8, 232, 125, 56, "neutral", [
        Line(hmi_id, 11, 700, "#111827"),
        Line("operator", 9, 400, "#374151"),
    ])
    c.connector(x + 133, 250, x + 219, 196, "warn",
                label="hmi -> db DENIED", label_pos=(x + 132, 300))
    c.node_box(x + 8, 352, 274, 40, "mgmt", [
        Line(primitive, 9, 700, "#111827"),
    ])


def ch01():
    c = Canvas(980, 470,
        title="Chapter 1 Lab Topology: Cloud-Native Microsegmentation on AWS, Azure, and GCP",
        subtitle="The same three-tier estate on each cloud, segmented with the cloud's own native primitive; web->db:5432 allowed, hmi->db denied by identity",
        svg_title="Chapter 1 lab topology: the same web/db/hmi estate built and segmented natively on AWS, Azure, and GCP",
        svg_desc="Your workstation runs the aws, az, and gcloud CLIs with a budget alert set. The same three-tier "
                 "estate is built on all three clouds: a web app tier, a db PostgreSQL database on 5432, and an hmi "
                 "operator workstation. On AWS the segmentation primitive is a security group that references the web "
                 "security group as the source of 5432, plus a stateless network ACL on the db subnet. On Azure it is "
                 "an NSG rule written by Application Security Group, allowing the web ASG to reach the db ASG on 5432 "
                 "and denying the hmi ASG. On GCP it is a VPC firewall rule targeting the db service account, allowing "
                 "only the web service account on 5432. In every column the legitimate web to db flow on 5432 is "
                 "allowed and the hmi to db lateral-movement flow is denied by identity. The volume is single-track "
                 "because the clouds are real accounts, so cost discipline and a full teardown are part of the lab.")

    c.node_box(30, 54, 930, 34, "mgmt", [
        Line("Your workstation · aws + az + gcloud CLIs · budget alert set before any billable resource", 10, 700, "#111827"),
    ])

    column(c, 30, "warn", "AWS · Security Groups + NACL",
           "web  (web-sg)", "db  (db-sg)", "hmi  (hmi-sg)",
           "db-sg allows 5432 from web-sg · NACL denies mgmt subnet")
    column(c, 350, "alt", "Azure · NSG + ASG",
           "web  (web-asg)", "db  (db-asg)", "hmi  (hmi-asg)",
           "NSG allows web-asg -> db-asg:5432 · denies hmi-asg")
    column(c, 670, "data", "GCP · Firewall + Service Account",
           "web  (web-sa)", "db  (db-sa)", "hmi  (hmi-sa)",
           "rule allows web-sa -> db-sa:5432 · denies all else")

    c.legend(30, 410, [
        ("alt", "Allowed by identity (web -> db:5432)"),
        ("warn", "Lateral movement (hmi -> db, denied)"),
        ("mgmt", "Native segmentation primitive"),
    ])
    c.save(f"{OUT}/chapter-01-lab-topology.svg")


if __name__ == "__main__":
    ch01()
