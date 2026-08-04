#!/usr/bin/env python3
"""Volume CXXXV (Confluent Certification Tracks) program map.

Chapter 1: Confluent's program — two FREE self-paced Fundamentals
Accreditations (Apache Kafka, and the new Apache Flink) as the on-ramp,
then three proctored certifications: CCDAK (developer), CCAAK
(administrator), CCAC (Confluent Cloud operator). 90-minute Honorlock
exams, 2-year validity, 7-day retake wait.

Run from scripts/diagrams:  python3 gen_volume135.py
"""
import sys
sys.path.insert(0, ".")
from labtopo import Canvas, Line

OUT = "../../diagrams/volume-135-confluent-certifications"


def ch01():
    c = Canvas(960, 560,
        title="Chapter 1 Program Map: Confluent Certification (Apache Kafka)",
        subtitle="Free Fundamentals Accreditations as the on-ramp, then three proctored certifications — 90-min Honorlock exams, 2-year validity, 7-day retake wait",
        svg_title="Chapter 1 program map: the Confluent certification program",
        svg_desc="Confluent's certification program begins with two free, self-paced Fundamentals Accreditations, "
                 "one for Apache Kafka and a new one for Apache Flink, each earning a shareable digital badge and "
                 "positioned for those not yet ready for certification. Above them sit three proctored "
                 "certifications: the Confluent Certified Developer for Apache Kafka, CCDAK, for developers and "
                 "solution architects building streaming applications with Kafka's core APIs; the Confluent "
                 "Certified Administrator for Apache Kafka, CCAAK, for professionals who configure, deploy, "
                 "monitor, and support cluster environments; and the Confluent Cloud Certified Operator, CCAC, for "
                 "managing multi-cloud and global Kafka architectures using Cluster Linking, Stream Governance, "
                 "fully managed connectors, and stream processing. All three are 90-minute proctored exams "
                 "administered remotely by Honorlock, requiring Google Chrome, a webcam, a microphone, and a "
                 "government ID, with multiple-choice, matching, and list-order questions. Results appear "
                 "immediately, certifications expire after two years and require recertification, a retake needs a "
                 "seven-day wait, and rescheduling or cancelling requires five or more days notice. Learning paths "
                 "run free fundamentals, then paid intermediate and advanced courses, then the certification. "
                 "Confluent Certification is not affiliated with the Apache Software Foundation. The volume models "
                 "the underlying streaming concepts free in Python.")

    c.node_box(230, 42, 500, 44, "mgmt", [
        Line("Confluent — the commercial platform around Apache Kafka", 10.5, 700, "#111827"),
        Line("event streaming: an append-only, durable, REPLAYABLE log", 8.5, 400, "#374151"),
    ])

    # free on-ramp
    c.node_box(40, 128, 880, 46, "neutral", [
        Line("FREE Fundamentals Accreditations — self-paced · shareable badge · \"not quite ready for Certification?\"", 9.5, 700, "#111827"),
        Line("Apache Kafka  ·  Apache Flink (NEW — stream processing beyond Kafka)", 8.5, 400, "#374151"),
    ])

    # the three certs
    c.node_box(40, 208, 280, 76, "data", [
        Line("CCDAK", 10, 700, "#111827"),
        Line("Certified Developer", 8.5, 400, "#374151"),
        Line("developers + solution architects", 8, 400, "#374151"),
        Line("core APIs · Streams · testing", 8, 400, "#374151"),
    ])
    c.node_box(340, 208, 280, 76, "data", [
        Line("CCAAK", 10, 700, "#111827"),
        Line("Certified Administrator", 8.5, 400, "#374151"),
        Line("manage cluster environments", 8, 400, "#374151"),
        Line("configure · deploy · monitor", 8, 400, "#374151"),
    ])
    c.node_box(640, 208, 280, 76, "alt", [
        Line("CCAC", 10, 700, "#111827"),
        Line("Cloud Certified Operator", 8.5, 400, "#374151"),
        Line("multi-cloud + global", 8, 400, "#374151"),
        Line("Cluster Linking · Governance", 8, 400, "#374151"),
    ])
    c.connector(180, 174, 180, 208, "data", label="", label_pos=(0, 0))
    c.connector(480, 174, 480, 208, "data", label="", label_pos=(0, 0))
    c.connector(780, 174, 780, 208, "alt", label="", label_pos=(0, 0))

    # exam mechanics band
    c.node_box(40, 304, 880, 56, "mgmt", [
        Line("Exam mechanics: 90 minutes · Honorlock remote proctoring · Chrome + webcam + government ID", 8.5, 700, "#111827"),
        Line("multiple-choice / matching / list-order · results immediately · EXPIRES AFTER 2 YEARS", 8.5, 400, "#374151"),
        Line("retake: 7-day wait  ·  reschedule/cancel: 5+ days  ·  accommodations: 21 days notice", 8.5, 400, "#374151"),
    ])

    c.raw('<text x="40" y="398" font-size="9.5" font-weight="700" fill="#991b1b">'
          'Certification Program Agreement is accepted at registration AND at exam start — braindump "practice questions" violate it and can invalidate the credential</text>')
    c.raw('<text x="40" y="417" font-size="9.5" font-weight="400" fill="#374151">'
          'Modeled free in Python: partitioned log &amp; ordering · acks/idempotence/transactions · consumer groups &amp; lag · schema compatibility · Connect · windowing · sizing &amp; ACLs</text>')

    c.legend(40, 448, [
        ("neutral", "Free accreditations"),
        ("data", "Kafka certifications"),
        ("alt", "Cloud certification"),
        ("mgmt", "Program facts"),
    ])
    c.save(f"{OUT}/chapter-01-certification-program.svg")


if __name__ == "__main__":
    ch01()
