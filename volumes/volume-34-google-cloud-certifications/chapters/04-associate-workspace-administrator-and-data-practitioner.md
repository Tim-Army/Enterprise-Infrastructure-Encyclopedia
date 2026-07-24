# Chapter 04: Associate Google Workspace Administrator and Data Practitioner

## Learning Objectives

- Identify the two associate certifications beyond Cloud Engineer and the
  distinct roles they serve
- Explain that Google Workspace Administrator sits at **associate** level,
  and why older references may place it differently
- Describe the Workspace administrator's domain — the collaboration
  platform, not the cloud platform
- Describe what Data Practitioner validates and where it sits relative to
  the professional data certifications
- Choose among the three associate certifications by the work you actually
  do

## Theory and Architecture

### Three associate certifications, three different products

Google's associate level holds three certifications, and a reader who
assumes they are three flavors of the same thing will choose badly:

| Certification | Product surface |
| --- | --- |
| Cloud Engineer | Google Cloud Platform — compute, network, storage, IAM ([Chapter 03](03-associate-cloud-engineer.md)) |
| Google Workspace Administrator | Google Workspace — the collaboration suite |
| Data Practitioner | Google Cloud's data services, at a practitioner level |

All three are **2 hours, $125, 50–60 multiple choice and multiple select
questions**, valid **three years**, with no prerequisites (verified
23 July 2026).

### Google Workspace Administrator: a different platform

This certification covers **Google Workspace** — Gmail, Drive, Calendar,
Meet, and the admin console that governs them — rather than Google Cloud
Platform. The subject is the collaboration estate: user and group
provisioning, organizational units, service configuration, mail routing
and compliance, endpoint and data-security controls, and the admin
console's audit and reporting surface.

Two things worth flagging:

- **It sits at associate level.** Google's certification page lists it
  under Associate certifications. Older references may present Workspace
  administration differently, and because Google Cloud certifications have
  **no exam codes** ([Chapter 01](01-the-google-cloud-certification-program-levels-and-validity.md)),
  a re-leveling leaves no version number behind to signal the change.
  Confirm the level on the page rather than from recollection.
- **It is largely orthogonal to the rest of this volume.** A Google Cloud
  infrastructure engineer gains little from it, and a Workspace
  administrator gains little from Associate Cloud Engineer. They are
  different jobs that happen to share a vendor.

### Data Practitioner: the data on-ramp

**Data Practitioner** validates working ability with Google Cloud's data
services at a practitioner rather than architect level — preparing,
storing, and analyzing data using the platform's managed services, and
understanding the shape of the data lifecycle on Google Cloud.

It is the on-ramp to the professional data certifications in
[Chapter 08](08-data-and-ml-professionals-data-engineer-database-engineer-and-machine-learning-engineer.md):
Data Engineer, Cloud Database Engineer, and Machine Learning Engineer. Its
place in the program mirrors DP-900's on Azure — the cheap way to test
whether the data domain suits you before committing to a professional
credential — except that it sits at associate rather than foundational
level, so it assumes real hands-on work rather than vocabulary alone.

Note the Next '26 refresh named **Google Cloud's data and analytics stack**
specifically ([Chapter 01](01-the-google-cloud-certification-program-levels-and-validity.md)).
Of everything in this volume, Data Practitioner and the professional data
certifications are the most likely to have moved recently — read the exam
guide.

### Choosing among the three

- Running infrastructure on Google Cloud → **Cloud Engineer**.
- Administering the collaboration suite → **Google Workspace
  Administrator**.
- Working with data on Google Cloud, without yet being an architect →
  **Data Practitioner**.

Holding two of these is unusual and generally reflects a genuinely split
role rather than a stronger portfolio.

## Design Considerations

- **Confirm the level before planning.** With no exam codes, Workspace
  Administrator's associate placement is exactly the kind of fact that
  goes stale silently in third-party material.
- **Do not treat Workspace as a Google Cloud stepping stone.** It is a
  different product with a different admin surface; it does not prepare
  you for Cloud Engineer, and Cloud Engineer does not prepare you for it.
- **Use Data Practitioner as a decision point.** If the professional data
  track appeals but the commitment feels large, this is the cheaper test —
  and unlike a foundational credential it certifies actual practice.
- **Read the data exam guides carefully right now.** The Next '26 refresh
  names the data and analytics stack; material predating it may omit
  examined products.
- **Three-year validity applies to all three.** These are cheaper to hold
  than any professional certification (Chapter 05 onward), which run two
  years.

## Implementation and Automation

### Confirming a certification's level from the source

```bash
# With no exam codes, the level on Google's own page is the fact to check.
curl -sL -A "Mozilla/5.0" https://cloud.google.com/learn/certification \
  | sed 's/<[^>]*>/\n/g' | grep -n -A 12 '^Associate certification$' | head -20
```

### Data Practitioner: reading a dataset's shape

```bash
# BigQuery is the center of Google Cloud's analytics stack
bq ls --project_id=<PROJECT_ID>
```

```bash
# Inspect a table's schema and row count before querying it
bq show --schema --format=prettyjson <PROJECT_ID>:<DATASET>.<TABLE>
```

```bash
# A dry run reports bytes scanned without incurring query cost —
# the single most useful habit in BigQuery work
bq query --use_legacy_sql=false --dry_run \
  'SELECT COUNT(*) FROM `<PROJECT_ID>.<DATASET>.<TABLE>`'
```

### Workspace: the admin surface is not gcloud

```text
# Google Workspace administration happens in the Admin console
# (admin.google.com) and the Admin SDK, not in gcloud. That separation
# is itself the point: a Google Cloud engineer's tooling does not carry
# over. The Admin SDK Directory API is the programmatic surface:
#
#   https://developers.google.com/admin-sdk/directory
```

## Validation and Troubleshooting

- **Level check first.** Before building a study plan around Workspace
  Administrator, confirm on Google's certification page that it still sits
  at associate level and still exists under that name.
- **Always dry-run a BigQuery query.** `--dry_run` reports bytes scanned
  before you pay for them. A query that scans a partitioned table without
  a partition filter is the classic surprise cost, and the dry run exposes
  it.
- **Distinguish dataset location errors from permission errors.** BigQuery
  datasets are regional; querying across incompatible locations fails in a
  way that looks like a permissions problem but is not.
- **Do not test Workspace changes on a live tenant.** Unlike a Google Cloud
  project, a Workspace tenant usually holds real users and real mail. Use a
  trial tenant or a dedicated organizational unit.

## Security and Best Practices

- Workspace administration touches real user mail and files. Scope admin
  roles narrowly, prefer delegated admin roles over super-admin, and
  enable two-step verification on any account holding them.
- Data work touches real data. Apply least privilege on BigQuery datasets
  and Cloud Storage buckets, and prefer authorized views over granting
  table-level access when sharing analysis.
- BigQuery costs scale with bytes scanned, not rows returned. Dry-run
  first, filter on partition columns, and avoid `SELECT *` on wide tables —
  this is both an examinable practice and the main way study labs become
  expensive.
- Keep the sandbox project and budget alert from Chapter 01 active for all
  data labs.

## References and Knowledge Checks

**References**

- [Associate Google Workspace Administrator](https://cloud.google.com/certification/associate-google-workspace-administrator)
- [Associate Data Practitioner](https://cloud.google.com/learn/certification/data-practitioner)
- [Google Cloud certification](https://cloud.google.com/learn/certification) —
  the level groupings, and the Next '26 refresh notice.
- [Appendix — Google Cloud Certifications and Course Access](../../volume-97-master-appendices/chapters/10-appendix-google-cloud-certifications-and-course-access.md)
- See [Chapter 08](08-data-and-ml-professionals-data-engineer-database-engineer-and-machine-learning-engineer.md)
  for the professional data certifications Data Practitioner leads to.

**Knowledge checks** *(original conceptual review questions — not
reproductions of any Google exam item)*

1. Name the three associate certifications and the product surface each
   covers.
2. Why is Workspace Administrator's level worth confirming, and what makes
   that harder in Google's program than in Azure's?
3. Where does Data Practitioner sit relative to the professional data
   certifications, and how does it compare to Azure's DP-900?
4. Why does a BigQuery dry run matter before running a query?
5. Why is a Workspace tenant a worse place to experiment than a Google
   Cloud project?

## Hands-On Lab

**Objective:** Confirm the associate lineup and levels from the source,
then build the BigQuery cost-control habit that the data track depends on.

**Cost note:** `bq ls`, `bq show`, and `--dry_run` are free. The single
real query in step 4 scans a small public dataset; keep the filter in
place.

**Prerequisites**

- The sandbox project and budget alert from Chapter 01.
- `gcloud` and `bq` authenticated.

**Steps**

1. **Confirm the levels (10 minutes).** Run the certification-page query
   and read the Associate section.

   **Expected result:** Cloud Engineer, Google Workspace Administrator,
   and Data Practitioner listed as associate — or a documented difference.

2. **Explore a public dataset (10 minutes).**

   ```bash
   bq show --schema --format=prettyjson bigquery-public-data:samples.shakespeare
   ```

   **Expected result:** the schema printed, with no query cost incurred.

3. **Dry-run first (10 minutes).**

   ```bash
   bq query --use_legacy_sql=false --dry_run \
     'SELECT word, word_count FROM `bigquery-public-data.samples.shakespeare` WHERE corpus = "hamlet"'
   ```

   **Expected result:** a bytes-scanned estimate and explicitly no data
   returned — the number you should always see before paying.

4. **Run it (5 minutes).** Remove `--dry_run` and run the same query.

   **Expected result:** results returned, and bytes billed matching the
   estimate.

5. **Negative test (10 minutes).** Dry-run a deliberately unfiltered query
   against a large public table, for example a `SELECT *` with no `WHERE`.

   **Expected result:** a dramatically larger bytes-scanned figure — the
   concrete demonstration of why the dry run is the habit. **Do not run it
   without `--dry_run`.**

6. **Cleanup:** no resources were created; public datasets need no
   teardown. Confirm the budget shows only the small step-4 query.

## Lab Verification

Complete this sign-off once the levels have been confirmed from Google's
page and the dry-run cost difference observed. Until then, the lab is
unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Beyond Cloud Engineer, the associate tier holds **Google Workspace
Administrator** — which covers the collaboration suite rather than Google
Cloud Platform, and sits at associate level, a placement worth confirming
because the program's lack of exam codes hides re-leveling — and **Data
Practitioner**, the practitioner-level on-ramp to the professional data
certifications. All three are $125, two hours, and valid three years, with
no prerequisites. They serve genuinely different jobs, so choose by the
product surface you work on rather than collecting them. Because the Next
'26 refresh names the data and analytics stack directly, the data exam
guides are the ones most worth re-reading before committing study time.

- [ ] Can name the three associate certifications and their product
      surfaces.
- [ ] Knows Workspace Administrator is associate-level and why that needs
      confirming.
- [ ] Can place Data Practitioner relative to the professional data track.
- [ ] Uses `--dry_run` before any BigQuery query.
- [ ] Knows why a Workspace tenant is a poor experimentation target.
- [ ] Completed the hands-on lab, including the unfiltered-query dry-run
      negative test.
