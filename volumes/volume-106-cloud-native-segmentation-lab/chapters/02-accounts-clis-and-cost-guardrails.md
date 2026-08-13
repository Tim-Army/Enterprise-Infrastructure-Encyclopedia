# Chapter 02: Accounts, CLIs, and Cost Guardrails

## Learning Objectives

- Create or reuse a free-tier account on each cloud you intend to use.
- Install and authenticate the AWS, Azure, and Google Cloud CLIs.
- **Set a budget alert on each cloud before creating a single billable resource.**
- Choose a region and record the identifiers the rest of the lab reuses.

## The order matters

Do the budget alert **first**. A microsegmentation lab is cheap, but a forgotten public IP or a second instance left running for a month is the kind of small, silent charge that teaches an expensive lesson. Every cloud lets you set a spend alert in minutes; there is no reason to skip it.

You only need the sections for the cloud(s) you chose in Chapter 01.

## Hands-On Lab

### Exercise 2.1 — AWS: CLI, identity, and a budget alert

**Objective.** Authenticate the AWS CLI and set a $5 budget alert.

**Walkthrough**
Install the CLI (macOS/Linux shown; see AWS docs for Windows):

```bash
curl -s "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o awscli.zip
unzip -q awscli.zip && sudo ./aws/install
aws --version
aws-cli/2.17.0 Python/3.11.9 Linux/6.8 exe/x86_64
```

Authenticate with an IAM user's access keys (create one in the console under IAM → Users → Security credentials; grant it `AdministratorAccess` for the lab only):

```bash
aws configure
AWS Access Key ID [None]: AKIA...
AWS Secret Access Key [None]: ****
Default region name [None]: us-east-1
Default output format [None]: json

aws sts get-caller-identity
{
    "UserId": "AIDA...",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/lab"
}
```

**Cost note.** Set a budget with an 80% alert. Save this as `budget.json`:

```json
{
  "BudgetName": "microseg-lab",
  "BudgetLimit": { "Amount": "5", "Unit": "USD" },
  "TimeUnit": "MONTHLY",
  "BudgetType": "COST"
}
```

And this as `notify.json` (use your email):

```json
[{
  "Notification": { "NotificationType": "ACTUAL", "ComparisonOperator": "GREATER_THAN", "Threshold": 80 },
  "Subscribers": [{ "SubscriptionType": "EMAIL", "Address": "you@example.com" }]
}]
```

```bash
aws budgets create-budget --account-id 123456789012 \
    --budget file://budget.json --notifications-with-subscribers file://notify.json
aws budgets describe-budgets --account-id 123456789012 --query 'Budgets[].BudgetName'
[ "microseg-lab" ]
```

**Expected result.** `get-caller-identity` returns your account; the budget `microseg-lab` exists.

**Negative test.**

```bash
aws sts get-caller-identity --profile nonexistent
The config profile (nonexistent) could not be found
```

**Rollback.** Nothing billable yet. Keep the budget for the whole lab.

### Exercise 2.2 — Azure: CLI, subscription, and a budget

**Objective.** Authenticate the Azure CLI and set a cost budget on the subscription.

**Walkthrough**

```bash
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
az version
{ "azure-cli": "2.62.0" }

az login
# opens a browser; pick your account
az account show --query '{name:name, id:id}'
{ "name": "Azure subscription 1", "id": "00000000-1111-2222-3333-444444444444" }
```

**Cost note.** Create a $5 budget with an alert at 80%:

```bash
SUB=$(az account show --query id -o tsv)
az consumption budget create --budget-name microseg-lab \
    --amount 5 --category cost --time-grain monthly \
    --start-date 2026-07-01 --end-date 2027-07-01 \
    --scope "/subscriptions/$SUB" 2>/dev/null || \
  echo "If the consumption extension prompts, run: az config set extension.use_dynamic_install=yes_without_prompt"
```

If the CLI budget path is unavailable on your subscription type, set it in the portal under **Cost Management → Budgets** — the point is that an alert exists.

**Expected result.** `az account show` returns your subscription; a $5 budget exists.

**Negative test.**

```bash
az group show -n does-not-exist
Resource group 'does-not-exist' could not be found.
```

**Rollback.** Nothing billable yet.

### Exercise 2.3 — GCP: CLI, project, and a budget

**Objective.** Authenticate the gcloud CLI, create a lab project, and attach a budget.

**Walkthrough**

```bash
curl -sSL https://sdk.cloud.google.com | bash && exec -l $SHELL
gcloud version | head -1
Google Cloud SDK 483.0.0

gcloud auth login          # browser sign-in
gcloud projects create microseg-lab-$RANDOM --name="microseg-lab"
gcloud config set project microseg-lab-XXXXX
gcloud config get-value project
microseg-lab-XXXXX
```

Link billing (required to create instances) and enable the compute API:

```bash
gcloud billing accounts list
ACCOUNT_ID            NAME                OPEN
0X0X0X-0X0X0X-0X0X0X  My Billing Account  True
gcloud billing projects link microseg-lab-XXXXX --billing-account 0X0X0X-0X0X0X-0X0X0X
gcloud services enable compute.googleapis.com
```

**Cost note.** Budgets attach to the billing account:

```bash
gcloud billing budgets create --billing-account=0X0X0X-0X0X0X-0X0X0X \
    --display-name="microseg-lab" --budget-amount=5USD \
    --threshold-rule=percent=0.8
```

**Expected result.** The project exists, billing is linked, `compute.googleapis.com` is enabled, and a $5 budget is attached.

**Negative test.**

```bash
gcloud compute instances list
Listed 0 items.
```

(No error, because the API is enabled — it is simply empty. An unenabled API would error with `Compute Engine API has not been used`.)

**Rollback.** Nothing billable yet. The empty project and budget are free.

## Reusable identifiers

Record these; later chapters reference them:

| Variable | AWS | Azure | GCP |
|:---|:---|:---|:---|
| Region | `us-east-1` | `eastus` | `us-central1` |
| Container | Account `123456789012` | RG `microseg-lab-rg` | Project `microseg-lab-XXXXX` |
| Free-tier size | `t3.micro` | `Standard_B1s` | `e2-micro` |
| Image | Amazon Linux 2023 | Ubuntu 22.04 LTS | Debian 12 |

## Summary and Completion Checklist

- [ ] CLI installed and authenticated for each chosen cloud.
- [ ] **A budget alert exists on every cloud you will use.**
- [ ] Region, container, size, and image recorded.
- [ ] You are ready to build networks in the per-cloud chapter.
