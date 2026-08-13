# Chapter 08: SnowPro Advanced — Administrator

## Learning Objectives

- Explain what the SnowPro Advanced: Administrator certifies and its prerequisite.
- Summarize the exam-guide domains.
- Administer accounts, security, cost, and governance on Snowflake.
- Manage performance monitoring and replication/failover.
- Complete a per-topic walkthrough for each Administrator domain.

## Theory and Architecture

The **SnowPro Advanced: Administrator (ADA-C01)** validates operating a Snowflake
account. It **requires SnowPro Core**. Its exam guide covers **account management**,
**security** (RBAC, network policies, MFA/SSO/SCIM), **cost management** (resource
monitors, warehouse governance), **data governance**, **performance monitoring**,
and **business continuity** (replication and failover).

## Design Considerations

The administrator manages the account end to end: a clean **RBAC hierarchy**,
**network policies** and federated auth, **resource monitors** to cap credit spend,
**governance** (masking, tags, access history), performance monitoring
(`QUERY_HISTORY`, warehouse metrics), and **replication/failover** for DR. Cost
control and security are constant themes.

## Implementation and Automation

The labs below use Snowflake SQL/admin patterns for each domain — account/security,
cost (resource monitors), governance, monitoring, and replication.

## Validation and Troubleshooting

Confirm the exam guide before studying:

```text
learn.snowflake.com/certifications > SnowPro Advanced: Administrator (ADA-C01):
  - account mgmt, security, cost mgmt, governance, performance monitoring, replication/failover
  - requires SnowPro Core
```

Common pitfalls: no **resource monitors** (runaway credits); flat RBAC; and no
**replication** for DR.

## Security and Best Practices

Build a **role hierarchy** (functional + access roles), enforce **network
policies** and SSO/MFA, cap spend with **resource monitors**, govern with masking/
tags/access history, monitor via `QUERY_HISTORY`/`WAREHOUSE_METERING_HISTORY`, and
configure **replication/failover** for business continuity.

## References and Knowledge Checks

- learn.snowflake.com: SnowPro Advanced: Administrator exam guide; account, security, replication docs.

**Knowledge checks**

1. What does the Administrator exam require as a prerequisite?
2. How do resource monitors control cost?
3. What provides business continuity in Snowflake?

## Hands-On Lab

Per-topic walkthroughs — Administrator domains. Run on a free trial (some features
need higher editions).

**Shared prerequisites** — a free Snowflake trial; ACCOUNTADMIN. **Cost:** none.

### Lab 8.1 — Account and security: network policy + RBAC

**Objective:** Restrict access with a network policy and role hierarchy.

```sql
CREATE NETWORK POLICY corp_only ALLOWED_IP_LIST=('203.0.113.0/24');
-- ALTER ACCOUNT SET NETWORK_POLICY = corp_only;   (applies account-wide)
CREATE ROLE app_admin; CREATE ROLE app_read;
GRANT ROLE app_read TO ROLE app_admin;   -- role hierarchy
```

**Expected result:** a network policy and a role hierarchy — the security
administration domain.

**Negative test:** leave the account open to all IPs; a **network policy** limits
access to trusted ranges.

**Rollback:** `DROP NETWORK POLICY IF EXISTS corp_only; DROP ROLE IF EXISTS app_admin; DROP ROLE IF EXISTS app_read;`

### Lab 8.2 — Cost management: resource monitors

**Objective:** Cap credit spend with a resource monitor.

```sql
CREATE RESOURCE MONITOR monthly_cap WITH CREDIT_QUOTA=100
  TRIGGERS ON 90 PERCENT DO NOTIFY
           ON 100 PERCENT DO SUSPEND;
ALTER WAREHOUSE lab_wh SET RESOURCE_MONITOR = monthly_cap;
```

**Expected result:** a resource monitor that notifies at 90% and suspends at 100%
of a 100-credit quota — the cost-management domain.

**Negative test:** run warehouses with no monitor; a runaway query/warehouse burns
credits — **cap with a resource monitor**.

**Rollback:** `ALTER WAREHOUSE lab_wh UNSET RESOURCE_MONITOR; DROP RESOURCE MONITOR IF EXISTS monthly_cap;`

### Lab 8.3 — Data governance

**Objective:** Apply a tag and review access.

```sql
CREATE TAG cost_center;
ALTER WAREHOUSE lab_wh SET TAG cost_center = 'analytics';
-- Governance: masking policies, row access policies, ACCESS_HISTORY, object tagging.
SELECT SYSTEM$GET_TAG('cost_center','lab_wh','WAREHOUSE');
```

**Expected result:** an object tag applied and read — the governance domain
(tags/masking/access history).

**Negative test:** govern by naming conventions alone; **tags + policies** are
enforceable metadata — use them.

**Rollback:** `ALTER WAREHOUSE lab_wh UNSET TAG cost_center; DROP TAG IF EXISTS cost_center;`

### Lab 8.4 — Performance monitoring

**Objective:** Monitor queries and warehouse usage.

```sql
SELECT query_id, warehouse_name, execution_time, bytes_scanned
FROM TABLE(INFORMATION_SCHEMA.QUERY_HISTORY())
ORDER BY execution_time DESC FETCH FIRST 5 ROWS ONLY;
```

**Expected result:** the slowest recent queries with their warehouse and bytes
scanned — the performance-monitoring domain.

**Negative test:** guess at slow queries; **QUERY_HISTORY** shows the facts —
monitor, then tune.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 8.5 — Business continuity: replication and failover

**Objective:** Describe replication/failover for DR.

```sql
-- Database/account replication to a secondary region + failover groups:
-- ALTER DATABASE demo_db ENABLE REPLICATION TO ACCOUNTS myorg.secondary;
-- Failover groups replicate objects + allow promotion of the secondary on outage.
SELECT 'replication + failover groups provide cross-region DR' AS bcp;
```

**Expected result:** the replication/failover-group model for DR — the
business-continuity domain.

**Negative test:** rely on a single region for critical data; **replication +
failover** provide cross-region DR — configure it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The SnowPro Advanced: Administrator (requires Core) certifies operating a Snowflake
account: security (RBAC, network policies, SSO/MFA), cost management (resource
monitors), governance (tags/masking/access history), performance monitoring
(QUERY_HISTORY), and business continuity (replication/failover).

- [ ] I can apply network policies and a role hierarchy.
- [ ] I can cap spend with resource monitors.
- [ ] I can govern with tags/policies and monitor queries.
- [ ] I can describe replication/failover for DR.
- [ ] I completed Labs 8.1–8.5 including each negative test.
