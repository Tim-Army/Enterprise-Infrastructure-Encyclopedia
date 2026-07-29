# Chapter 05: Data and AI Certifications — Data+, DataSys+, and DataAI

## Learning Objectives

- Enumerate the CompTIA data certifications and their current exam codes.
- Distinguish the data-analyst (Data+), data-systems (DataSys+), and advanced (DataAI) roles.
- Describe CompTIA's AI Essentials microcredential line.
- Map the data certifications to the encyclopedia's data and cloud volumes.
- Build a study path for a data or AI-oriented professional.

## Theory and Architecture

CompTIA's **Data and AI** credentials certify analysis, data infrastructure,
and the fast-growing AI skill areas. As verified on comptia.org (26 July
2026):

- **CompTIA Data+** — exam **DA0-002** (V2; DA0-001 retiring) across five
  weighted domains: **Data concepts and environments (20%)**, **Data acquisition
  and preparation (22%)**, **Data analysis (24%)**, **Visualization and
  reporting (20%)**, and **Data governance (14%)** — V2 adds AI concepts (AI
  models, NLP, robotic automation). A 90-question exam (multiple-choice and
  performance-based) over 90 minutes with a **scaled passing score of 675
  (100–900)**; 18–24 months as a data analyst recommended. The **data-analyst**
  credential for turning data into insight — vendor-neutral, complementing tools
  like Power BI (Microsoft PL-300).
- **CompTIA DataSys+** — exam **DS0-001** (V1) across five weighted domains:
  **Database fundamentals (24%)**, **Database deployment (16%)**, **Database
  management and maintenance (25%)**, **Data and database security (23%)**, and
  **Business continuity (12%)**. A 90-question exam (multiple-choice and
  performance-based) over 90 minutes with a **scaled passing score of 700
  (100–900)**; 2–3 years as a database administrator recommended. The
  **database-administrator** credential.
- **CompTIA DataAI (formerly DataX)** — exam **DY0-001** (V1, launched 25 July
  2024). CompTIA's **advanced, expert-level data-science and AI** credential
  (the renamed **DataX**), for senior professionals with roughly **5+ years** of
  experience. It is a **pass/fail** exam of up to **90 questions**
  (multiple-choice and performance-based) over **165 minutes**, offered in
  English and Japanese, and is expected to retire around 2027. Its five weighted
  domains are **Mathematics and statistics (17%)**, **Modeling, analysis, and
  outcomes (24%)**, **Machine learning (24%)**, **Operations and processes
  (22%)**, and **Specialized applications of data science (13%)** — spanning
  statistical and linear-algebra methods, exploratory analysis and model
  iteration, supervised/tree-based/deep/unsupervised learning, the data-science
  life cycle with MLOps and deployment, and specialized areas such as NLP,
  computer vision, and optimization.

Alongside the exam-based data certs, CompTIA offers a broad **AI Essentials**
microcredential line — **AI Essentials**, **AI Fundamentals**, **AI Prompting
Essentials**, **AI Agent Essentials**, **Copilot 365 Essentials**, and
role-specific AI essentials (marketing, sales, help desk, customer support,
agent) — short courses that build foundational, practical AI literacy for a wide
audience. These are **hands-on courses validated by a CompTIA "CompCert"
(Competency Certificate) assessment** rather than proctored coded exams. Most
are short (roughly 2–8 hours) — **AI Agent Essentials**, for example, is a 4–5
hour course on agentic systems (agent workflows, tool and memory management,
guardrails, and human oversight) with practice in CompTIA's proprietary **Agent
Simulator**. The exception is **AI Fundamentals**, a much larger **three-credit
academic course (~50–56 hours)** aimed at institutions and non-technical student
populations, with AI labs and auto-graded feedback. The security-focused AI
certification **SecAI+** (Expansion Series, Chapter 06) sits above this literacy
tier.

## Design Considerations

Choose by role. **Data+** is the entry data-analyst credential; **DataSys+** is
for database administrators; **DataAI** (ex-DataX) is the advanced,
senior-level data-and-AI credential for experienced professionals. The **AI
Essentials** line is deliberately broad and foundational — good for
upskilling non-specialists and building AI literacy across a team, not a
substitute for the deeper data or AI engineering credentials of the cloud
vendors (Azure/AWS/GCP).

Pair CompTIA's vendor-neutral data credentials with the vendor data
certifications elsewhere in the encyclopedia: **Data+** with Microsoft
**PL-300** (Power BI) and the cloud analytics tracks, and **DataSys+** with the
cloud database certifications (Azure DP-300, AWS Database). CompTIA teaches the
vendor-neutral fundamentals those platform certs then apply.

## Implementation and Automation

Verify the data codes and the DataX → DataAI rename from comptia.org:

```bash
for slug in data datasys dataai; do
  code=$(curl -sSL -A "Mozilla/5.0" "https://www.comptia.org/en-us/certifications/$slug/" \
    | grep -oE '\b(DA0-[0-9]{3}|DS0-[0-9]{3}|DY0-[0-9]{3})\b' | sort -u | tr '\n' ' ')
  title=$(curl -sSL -A "Mozilla/5.0" "https://www.comptia.org/en-us/certifications/$slug/" \
    | grep -oE '<title>[^<]*</title>' | head -1)
  echo "$slug -> ${code:-see page} | $title"
done
# data -> DA0-002 ; datasys -> DS0-001 ; dataai -> DY0-001 (formerly DataX)
```

## Validation and Troubleshooting

Map the data certifications:

| Certification | Exam | Role | Complements |
| --- | --- | --- | --- |
| Data+ | DA0-002 | Data analyst | Microsoft PL-300; cloud analytics |
| DataSys+ | DS0-001 | Database administrator | Azure DP-300; AWS Database |
| DataAI (ex-DataX) | DY0-001 | Advanced data/AI (5+ yrs) | Cloud AI/ML certs |
| AI Essentials line | microcredentials | Broad AI literacy | — |

Common pitfalls: studying **Data+ DA0-001** instead of the current **DA0-002**;
looking for **DataX** by name (now **DataAI**); and treating the **AI
Essentials** microcredentials as equivalent to the deeper data-analyst or
cloud AI-engineering certifications — they are foundational literacy
credentials, valuable but different in scope.

## Security and Best Practices

Verify the **current exam versions** (Data+ moved to DA0-002; DataX became
DataAI). Choose the credential by role — analyst (Data+), DBA (DataSys+),
advanced (DataAI) — and use the **AI Essentials** line to build broad,
practical AI literacy across a team. Pair CompTIA's vendor-neutral data
credentials with the vendor data and AI certifications for platform depth, and
apply the **data governance and security** concepts (which Data+ and DataSys+
both cover) to real controls. Plan **CE renewal** (Chapter 08).

## References and Knowledge Checks

- comptia.org: certification pages for Data+, DataSys+, DataAI, and the AI Essentials line.
- Cross-reference: [Volume XXXVIII — Microsoft Certifications Beyond Azure](../volume-038-microsoft-certifications-beyond-azure/README.md) (PL-300, DP family).

**Knowledge checks**

1. What is the current Data+ exam code, and which version did it replace?
2. What was DataAI previously called?
3. How do the AI Essentials microcredentials differ from the data-analyst and cloud AI certifications?

## Hands-On Lab

Per-topic walkthroughs — **one lab for every weighted exam domain** of Data+,
DataSys+, and DataAI.

**Shared prerequisites** — a Linux shell with `python3` (with `statistics`) and
`sqlite3`; `openssl` for one lab. **Cost:** none.

### Lab 5.1 — Data+: Data concepts and environments (20%)

**Objective:** Distinguish data types and structures — the vocabulary of the
domain.

```bash
python3 -c "print([type(x).__name__ for x in (1, 1.5, 'txt', True, [1,2])])"
```

**Expected result:** `['int','float','str','bool','list']` — scalar versus
structured data types across environments.

**Negative test:** treat a CSV of `1,2,3` as integers automatically; parsed
fields are strings until cast.

**Cleanup:** none.

### Lab 5.2 — Data+: Data acquisition and preparation (22%)

**Objective:** Clean raw data — drop blanks and duplicates.

```bash
printf 'id,val\n1,10\n2,\n2,20\n3,30\n' > /tmp/raw.csv
python3 - <<'PY'
import csv
seen=set(); rows=[]
for r in csv.DictReader(open('/tmp/raw.csv')):
    if r['val'] and r['id'] not in seen: seen.add(r['id']); rows.append(r)
print('clean rows:', len(rows))
PY
```

**Expected result:** `clean rows: 3` — a blank row and a duplicate id removed,
the essence of data preparation.

**Negative test:** analyze before cleaning; the blank and duplicate skew every
aggregate.

**Cleanup:** `rm -f /tmp/raw.csv`.

### Lab 5.3 — Data+: Data analysis (24%)

**Objective:** Apply a basic statistical method to a series.

```bash
python3 -c "import statistics as s; d=[10,20,20,30,50]; print('mean',s.mean(d),'median',s.median(d),'stdev',round(s.pstdev(d),2))"
```

**Expected result:** `mean 26 median 20 stdev 13.56` — central tendency and
dispersion, core data analysis.

**Negative test:** report the mean alone for skewed data; the median tells a
different story.

**Cleanup:** none.

### Lab 5.4 — Data+: Visualization and reporting (20%)

**Objective:** Build a text visualization (a bar chart) for a report.

```bash
python3 - <<'PY'
data={'Q1':4,'Q2':7,'Q3':3}
for k,v in data.items(): print(f"{k} | {'#'*v} {v}")
PY
```

**Expected result:** three labeled bars scaled by value — a simple, accessible
visualization for a report.

**Negative test:** use a 3-D exploded pie for three values; it obscures rather
than communicates — avoid deceptive charts.

**Cleanup:** none.

### Lab 5.5 — Data+: Data governance (14%)

**Objective:** Apply a governance control — mask sensitive fields.

```bash
python3 -c "ssn='123-45-6789'; print('masked:', '***-**-'+ssn[-4:])"
```

**Expected result:** `masked: ***-**-6789` — data masking, a governance/privacy
control.

**Negative test:** store full SSNs in a shared report; governance requires
minimization and masking.

**Cleanup:** none.

### Lab 5.6 — DataSys+: Database fundamentals (24%)

**Objective:** Write DDL/DML with ACID-style transaction control.

```bash
sqlite3 /tmp/ds.db "CREATE TABLE acct(id INT PRIMARY KEY, bal INT);
BEGIN; INSERT INTO acct VALUES(1,100); UPDATE acct SET bal=bal-25 WHERE id=1; COMMIT;
SELECT bal FROM acct WHERE id=1;"
```

**Expected result:** `75` — a table, an atomic transaction (BEGIN/COMMIT), and a
query.

**Negative test:** `ROLLBACK` instead of `COMMIT`; the change is discarded — the
A in ACID.

**Cleanup:** `rm -f /tmp/ds.db`.

### Lab 5.7 — DataSys+: Database deployment (16%)

**Objective:** Design and validate a schema against requirements.

```bash
sqlite3 /tmp/dep.db "CREATE TABLE orders(id INT PRIMARY KEY, cust TEXT NOT NULL, total REAL CHECK(total>=0));"
sqlite3 /tmp/dep.db ".schema orders"
```

**Expected result:** the `orders` schema with a NOT NULL and a CHECK constraint —
a deployed, validated design.

**Negative test:** insert `total=-5`; the CHECK constraint rejects it — schema
validation in action.

**Cleanup:** `rm -f /tmp/dep.db`.

### Lab 5.8 — DataSys+: Database management and maintenance (25%)

**Objective:** Monitor and maintain — index and inspect the query plan.

```bash
sqlite3 /tmp/m.db "CREATE TABLE t(k INT); INSERT INTO t VALUES(1),(2),(3);
CREATE INDEX idx_k ON t(k); EXPLAIN QUERY PLAN SELECT * FROM t WHERE k=2;"
```

**Expected result:** a query plan referencing `idx_k` — index maintenance for
performance tuning.

**Negative test:** add indexes to every column; write-heavy tables slow down —
maintenance is a trade-off.

**Cleanup:** `rm -f /tmp/m.db`.

### Lab 5.9 — DataSys+: Data and database security (23%)

**Objective:** Encrypt a database export (data at rest) and set access controls.

```bash
sqlite3 /tmp/s.db "CREATE TABLE u(id INT, pii TEXT); INSERT INTO u VALUES(1,'secret');" 
sqlite3 /tmp/s.db .dump | openssl enc -aes-256-cbc -pbkdf2 -pass pass:Db2026 -out /tmp/dump.enc && chmod 600 /tmp/dump.enc && stat -c '%A' /tmp/dump.enc
```

**Expected result:** an encrypted `.dump.enc` at 600 — encryption at rest plus a
least-privilege file control.

**Negative test:** ship the plaintext `.dump`; database exports carry the same
PII as the live DB.

**Cleanup:** `rm -f /tmp/s.db /tmp/dump.enc`.

### Lab 5.10 — DataSys+: Business continuity (12%)

**Objective:** Back up and restore a database (recovery test).

```bash
sqlite3 /tmp/bc.db "CREATE TABLE t(v INT); INSERT INTO t VALUES(42);"
sqlite3 /tmp/bc.db ".backup /tmp/bc.bak"; rm /tmp/bc.db; sqlite3 /tmp/bc.bak "SELECT v FROM t;"
```

**Expected result:** `42` restored from the backup after the original was
removed — a validated recovery, the heart of business continuity.

**Negative test:** assume a backup file proves recoverability; only a test
restore does.

**Cleanup:** `rm -f /tmp/bc.db /tmp/bc.bak`.

### Lab 5.11 — DataAI: Mathematics and statistics (17%)

**Objective:** Apply a statistical test concept — correlation of two series.

```bash
python3 -c "import statistics as s; x=[1,2,3,4]; y=[2,4,6,8]; print('corr', round(s.correlation(x,y),3))"
```

**Expected result:** `corr 1.0` — a perfect linear correlation, the kind of
statistic DataAI expects you to interpret.

**Negative test:** read correlation as causation; correlation alone proves
neither direction nor cause.

**Cleanup:** none.

### Lab 5.12 — DataAI: Modeling, analysis, and outcomes (24%)

**Objective:** Fit a trivial linear model and evaluate it.

```bash
python3 - <<'PY'
xs=[1,2,3,4]; ys=[3,5,7,9]           # y = 2x + 1
n=len(xs); sx=sum(xs); sy=sum(ys); sxy=sum(a*b for a,b in zip(xs,ys)); sxx=sum(a*a for a in xs)
m=(n*sxy-sx*sy)/(n*sxx-sx*sx); b=(sy-m*sx)/n
print(f"slope={m:.1f} intercept={b:.1f}")
PY
```

**Expected result:** `slope=2.0 intercept=1.0` — a fitted model recovering the
underlying relationship (modeling and outcomes).

**Negative test:** fit a line to non-linear data and trust it; evaluate fit
before relying on a model.

**Cleanup:** none.

### Lab 5.13 — DataAI: Machine learning (24%)

**Objective:** Implement a k-nearest-neighbor classification by hand.

```bash
python3 - <<'PY'
train=[((1,1),'A'),((2,2),'A'),((8,8),'B'),((9,9),'B')]
q=(3,3)
d=sorted(train, key=lambda t:(t[0][0]-q[0])**2+(t[0][1]-q[1])**2)
print('predict:', d[0][1])
PY
```

**Expected result:** `predict: A` — a 1-NN classifier assigning the query to the
nearest labeled point, a foundational supervised-learning method.

**Negative test:** skip feature scaling with mixed units; distance-based models
are dominated by the larger-scale feature.

**Cleanup:** none.

### Lab 5.14 — DataAI: Operations and processes (22%)

**Objective:** Apply the data-science life cycle with version control (MLOps).

```bash
d=$(mktemp -d); cd "$d"; git init -q; echo "model_v1" > model.txt; git add model.txt
git -c user.email=a@b.c -c user.name=ds commit -qm "baseline model"; git log --oneline
```

**Expected result:** a committed model artifact — version control and
reproducibility, core to MLOps operations.

**Negative test:** deploy an unversioned model; you cannot roll back or reproduce
it — an MLOps failure.

**Cleanup:** `rm -rf "$d"`.

### Lab 5.15 — DataAI: Specialized applications of data science (13%)

**Objective:** Apply an NLP primitive — tokenization and term frequency.

```bash
python3 - <<'PY'
from collections import Counter
text="data drives decisions data wins"
print(Counter(text.split()).most_common(2))
PY
```

**Expected result:** `[('data', 2), ...]` — tokenization and term-frequency, an
NLP building block behind TF-IDF and topic modeling.

**Negative test:** treat "Data" and "data" as different tokens; normalize case
before counting.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

CompTIA's data credentials run Data+ (DA0-002, analyst), DataSys+ (DS0-001,
DBA), and the advanced DataAI (DY0-001, formerly DataX), plus a broad AI
Essentials microcredential line. They are vendor-neutral fundamentals that pair with the
vendor data and AI certifications for platform depth.

- [ ] I can list the data certs and current exam codes.
- [ ] I know DataX is now DataAI and Data+ is DA0-002.
- [ ] I can place the AI Essentials line correctly in scope.
- [ ] I can build a data/AI study path with vendor pairings.
- [ ] I completed Labs 5.1–5.2 including each negative test.
