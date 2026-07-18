# Chapter 04: Compute, Containers, Serverless, and Application Architecture

## Learning Objectives

- Select among Amazon EC2, Amazon ECS, Amazon EKS, and AWS Lambda for a
  given workload based on operational ownership, scaling profile, and
  cost model.
- Configure an EC2 Auto Scaling group with a launch template and a
  target-tracking scaling policy.
- Deploy a containerized service on Amazon ECS using the Fargate launch
  type and place it behind an Application Load Balancer.
- Build and deploy an AWS Lambda function with least-privilege IAM,
  environment configuration, and an API Gateway front door.
- Apply the AWS Well-Architected Framework to choose the correct load
  balancer type (ALB, NLB, or Gateway Load Balancer) and orchestrate
  multi-step application logic with AWS Step Functions and Amazon
  EventBridge.

## Theory and Architecture

AWS compute options sit on a spectrum from full operating-system control to
fully abstracted execution, and each step along that spectrum trades
customer-managed flexibility for AWS-managed operational burden — directly
extending the shared responsibility model introduced in Chapter 01.

| Compute option | Customer manages | AWS manages | Scaling unit |
| --- | --- | --- | --- |
| Amazon EC2 | Guest OS, runtime, application, patching | Hypervisor, physical host, network virtualization | Instance |
| Amazon ECS/EKS on EC2 | Worker node OS, container runtime config | Orchestration control plane (ECS) or partially (EKS) | Task/pod, with node-level scaling underneath |
| Amazon ECS/EKS on Fargate | Container image and task definition only | Underlying compute entirely | Task/pod |
| AWS Lambda | Function code and configuration only | Everything else, including the runtime environment | Invocation/concurrency |

### Amazon EC2 and Auto Scaling

An **EC2 instance** is a virtual machine backed by a chosen **Amazon
Machine Image (AMI)** and **instance type**, the latter determining the
vCPU/memory/network ratio and, for some families, specialized hardware
(GPU, high-memory, burstable). A **launch template** captures the full
instance configuration — AMI, instance type, security groups, IAM instance
profile, user data — as a versioned, reusable object. An **Auto Scaling
group (ASG)** maintains a fleet of instances launched from a template
across one or more Availability Zones, replacing unhealthy instances
automatically and scaling the fleet size according to a **scaling policy**:
target tracking (hold a metric, such as average CPU utilization, at a set
point), step scaling (add/remove capacity in defined increments as a
metric crosses thresholds), or scheduled scaling (pre-provision for known
traffic patterns). ASGs integrate with Elastic Load Balancing health checks
so that an instance failing application-level health checks — not just an
EC2 status check — is replaced.

### Containers: Amazon ECS and Amazon EKS

**Amazon Elastic Container Service (ECS)** is AWS's native container
orchestrator, using a simpler task-definition and service model tightly
integrated with other AWS services (IAM task roles, Application Load
Balancer target groups, CloudWatch Logs) without exposing Kubernetes API
concepts. **Amazon Elastic Kubernetes Service (EKS)** runs a managed
Kubernetes control plane, giving access to the full Kubernetes ecosystem
(Helm charts, custom controllers, existing Kubernetes tooling) at the cost
of greater operational surface area. Both support two launch types:

- **EC2 launch type** — tasks/pods run on customer-managed EC2 worker
  nodes (an ECS-optimized AMI, or a managed/self-managed EKS node group).
  The customer patches and scales the underlying nodes.
- **AWS Fargate** — a serverless compute engine for containers; AWS
  provisions right-sized compute per task/pod with no customer-visible EC2
  instance to patch or scale. Fargate trades some cost efficiency at very
  high, steady-state utilization for eliminating node-level operations
  entirely.

Container images are stored in **Amazon Elastic Container Registry (ECR)**,
a private, IAM-authenticated registry with support for image scanning
(integrating with Amazon Inspector, covered in Chapter 08) and lifecycle
policies that expire untagged or old images automatically.

### Serverless: AWS Lambda and event-driven architecture

**AWS Lambda** executes customer code in response to an event without any
provisioned server, billed per invocation and per millisecond of execution
(with a free tier). A Lambda function's **execution role** is the IAM role
it assumes at runtime — the single most important security control for a
Lambda function, since an over-broad execution role is a direct path to
privilege escalation if the function itself is compromised through a
dependency or injection vulnerability. Lambda functions can run inside a
VPC (attaching an ENI per concurrent execution in the assigned subnets) to
reach private resources such as an RDS instance, at the cost of ENI
provisioning latency mitigated by Hyperplane networking in current Lambda
runtimes.

Serverless application architecture composes several purpose-built
services rather than one monolithic compute unit:

- **Amazon API Gateway** — a managed front door for REST, HTTP, or
  WebSocket APIs, handling request validation, throttling, authorization
  (IAM, Lambda authorizers, or Amazon Cognito), and integration with
  Lambda, ECS, or any HTTP backend.
- **AWS Step Functions** — orchestrates multi-step workflows as a state
  machine, coordinating Lambda functions, ECS tasks, and other AWS API
  calls with built-in retry, error handling, and parallel/branching logic,
  replacing fragile custom orchestration code.
- **Amazon EventBridge** — a serverless event bus that routes events from
  AWS services, SaaS partners, or custom applications to targets (Lambda,
  Step Functions, SQS) based on pattern-matching rules, decoupling event
  producers from consumers.
- **Amazon SQS / Amazon SNS** — SQS provides durable, at-least-once
  message queuing for point-to-point decoupling and buffering against
  downstream throughput limits; SNS provides pub/sub fan-out to multiple
  subscribers (including SQS queues, Lambda, and HTTPS endpoints).

### Load balancing

| Load balancer | OSI layer | Typical use |
| --- | --- | --- |
| Application Load Balancer (ALB) | Layer 7 (HTTP/HTTPS/WebSocket) | Path/host-based routing, container and Lambda targets, WAF integration |
| Network Load Balancer (NLB) | Layer 4 (TCP/UDP/TLS) | Extreme throughput/low latency, static IP per AZ, PrivateLink service front end |
| Gateway Load Balancer (GWLB) | Layer 3/4, transparent | Inserting third-party or custom traffic-inspection appliances transparently into a traffic path |

An ALB is the default choice for HTTP(S) application traffic because of its
content-based routing and native integration with ECS/EKS target groups
and AWS WAF. An NLB is preferred when raw throughput, ultra-low latency, a
fixed IP per AZ, or non-HTTP TCP/UDP protocols are required, and it is the
mandatory front end for exposing a service through AWS PrivateLink. A GWLB
sits transparently in the traffic path to insert inspection appliances
(a third-party firewall, an IDS) without the traffic's source/destination
appearing to change, commonly paired with the centralized egress VPC
pattern described in Chapter 03.

## Design Considerations

- **Match the compute option to operational appetite, not just cost.**
  Fargate and Lambda cost more per unit of compute than equivalent
  EC2-based capacity at high, steady utilization, but they eliminate node
  patching, capacity planning, and AMI pipeline maintenance — for many
  teams, the eliminated operational labor is worth more than the per-unit
  premium.
- **ECS vs. EKS is a team-capability decision as much as a technical one.**
  Choose EKS when the organization already has Kubernetes expertise, needs
  portability across clouds, or depends on the Kubernetes ecosystem;
  choose ECS when the team wants tighter native AWS integration with a
  smaller operational learning curve and no need for Kubernetes-specific
  tooling.
- **Right-size before enabling aggressive auto scaling.** Auto scaling
  compensates for load variability, not for a fundamentally
  under-provisioned instance type or task size; profile the workload's
  actual CPU/memory ratio first, since scaling out ten under-sized tasks
  is often more expensive and less reliable than scaling out five
  correctly sized ones.
- **VPC-attached Lambda functions add a dependency, not just latency.** A
  Lambda function inside a VPC that needs internet access still requires
  a NAT gateway path through a private subnet — VPC attachment does not
  grant internet access on its own — and it introduces the VPC's
  availability as a new dependency for a function that would otherwise
  have none.
- **Choose the load balancer by protocol and integration need, not
  habit.** Defaulting to ALB for every workload leaves throughput and
  latency on the table for pure TCP services, and defaulting to NLB for
  everything loses path-based routing and WAF integration for HTTP
  workloads.
- **Design for idempotency in event-driven architectures.** SQS's
  at-least-once delivery and Lambda's retry behavior on failure mean a
  message or event can be processed more than once; consumers must be
  idempotent (using a deduplication key or conditional write) rather than
  assuming exactly-once processing.
- **Prefer Step Functions over custom orchestration code for multi-step
  workflows.** Hand-rolled retry/error-handling logic spread across
  multiple Lambda functions is harder to observe and debug than a Step
  Functions state machine, which provides a visual execution history and
  built-in error handling per state.

## Implementation and Automation

### 1. Launch template and Auto Scaling group (Terraform)

```hcl
resource "aws_launch_template" "app" {
  name_prefix   = "app-"
  image_id      = data.aws_ssm_parameter.al2023_ami.value
  instance_type = "t3.small"
  iam_instance_profile {
    name = aws_iam_instance_profile.app.name
  }
  vpc_security_group_ids = [aws_security_group.app.id]
  user_data = base64encode(<<-EOF
    #!/bin/bash
    dnf install -y amazon-cloudwatch-agent
  EOF
  )
}

resource "aws_autoscaling_group" "app" {
  desired_capacity    = 2
  min_size            = 2
  max_size            = 6
  vpc_zone_identifier = [for s in aws_subnet.private : s.id]
  target_group_arns   = [aws_lb_target_group.app.arn]
  health_check_type    = "ELB"
  health_check_grace_period = 60

  launch_template {
    id      = aws_launch_template.app.id
    version = "$Latest"
  }
}

resource "aws_autoscaling_policy" "cpu_target" {
  name                   = "target-tracking-cpu"
  autoscaling_group_name = aws_autoscaling_group.app.name
  policy_type            = "TargetTrackingScaling"
  target_tracking_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ASGAverageCPUUtilization"
    }
    target_value = 60.0
  }
}
```

### 2. ECS Fargate service behind an Application Load Balancer

```hcl
resource "aws_ecs_cluster" "main" {
  name = "app-cluster"
}

resource "aws_ecs_task_definition" "app" {
  family                   = "app"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = "512"
  memory                   = "1024"
  execution_role_arn       = aws_iam_role.ecs_execution.arn
  task_role_arn            = aws_iam_role.ecs_task.arn
  container_definitions = jsonencode([{
    name      = "app"
    image     = "111122223333.dkr.ecr.us-east-1.amazonaws.com/app:latest"
    portMappings = [{ containerPort = 8443, protocol = "tcp" }]
    logConfiguration = {
      logDriver = "awslogs"
      options = {
        "awslogs-group"         = "/ecs/app"
        "awslogs-region"        = "us-east-1"
        "awslogs-stream-prefix" = "app"
      }
    }
  }])
}

resource "aws_ecs_service" "app" {
  name            = "app"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count   = 2
  launch_type     = "FARGATE"

  network_configuration {
    subnets         = [for s in aws_subnet.private : s.id]
    security_groups = [aws_security_group.app.id]
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.app.arn
    container_name    = "app"
    container_port    = 8443
  }
}
```

### 3. A least-privilege Lambda function behind API Gateway

```hcl
resource "aws_iam_role" "lambda_exec" {
  name = "lambda-orders-processor"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "lambda_scoped" {
  name = "scoped-access"
  role = aws_iam_role.lambda_exec.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["dynamodb:PutItem", "dynamodb:GetItem"]
        Resource = aws_dynamodb_table.orders.arn
      },
      {
        Effect   = "Allow"
        Action   = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"]
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })
}

resource "aws_lambda_function" "orders" {
  function_name = "orders-processor"
  role          = aws_iam_role.lambda_exec.arn
  handler       = "index.handler"
  runtime       = "nodejs20.x"
  filename      = "orders-processor.zip"
  timeout       = 10
  memory_size   = 256
  environment {
    variables = { TABLE_NAME = aws_dynamodb_table.orders.name }
  }
}

resource "aws_apigatewayv2_api" "orders_api" {
  name          = "orders-api"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "orders" {
  api_id                 = aws_apigatewayv2_api.orders_api.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.orders.invoke_arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "post_orders" {
  api_id    = aws_apigatewayv2_api.orders_api.id
  route_key = "POST /orders"
  target    = "integrations/${aws_apigatewayv2_integration.orders.id}"
}

resource "aws_apigatewayv2_stage" "prod" {
  api_id      = aws_apigatewayv2_api.orders_api.id
  name        = "prod"
  auto_deploy = true
}
```

### 4. CLI deployment and update commands

```bash
# Build and push a container image to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin 111122223333.dkr.ecr.us-east-1.amazonaws.com
docker build -t app:latest .
docker tag app:latest 111122223333.dkr.ecr.us-east-1.amazonaws.com/app:latest
docker push 111122223333.dkr.ecr.us-east-1.amazonaws.com/app:latest

# Force a new ECS deployment to pick up the new image tag
aws ecs update-service --cluster app-cluster --service app --force-new-deployment

# Update Lambda function code directly from a zip artifact
aws lambda update-function-code \
  --function-name orders-processor \
  --zip-file fileb://orders-processor.zip
```

## Validation and Troubleshooting

- **ASG instances failing health checks in a loop.** Check `aws
  autoscaling describe-scaling-activities` for the termination cause; a
  common root cause is the ALB target group's health-check path returning
  a non-2xx status before the application has finished starting —
  increase `health_check_grace_period` or fix the readiness endpoint.
- **ECS tasks stuck in `PENDING` or repeatedly stopping.** `aws ecs
  describe-tasks --tasks <TASK_ARN>` surfaces a `stoppedReason`; the most
  common causes are the task execution role lacking `ecr:GetAuthorizationToken`
  or `logs:CreateLogStream` permission, or the task's `awsvpc` network
  configuration referencing a subnet with no route to ECR/CloudWatch Logs
  (missing NAT gateway or VPC endpoints, tying back to Chapter 03).
- **Lambda `AccessDeniedException` at runtime, not at invocation.** This
  indicates the execution role is missing a permission the code path
  actually exercises; use `aws iam simulate-principal-policy` against the
  execution role and the specific action to confirm before widening the
  role, rather than defaulting to a broad managed policy.
- **API Gateway returning `403` before reaching Lambda.** Check the
  route's authorizer configuration and resource policy first; a `403`
  with no Lambda invocation recorded in CloudWatch Logs means the request
  never reached the integration.
- **Step Functions execution failed mid-workflow.** The Step Functions
  console/API execution history (`aws stepfunctions
  get-execution-history`) shows the exact state and error cause, which is
  almost always faster to diagnose than reconstructing the failure from
  scattered Lambda logs across multiple functions.
- **Common failure: Fargate task cannot pull image.** A Fargate task in a
  private subnet with no NAT gateway or ECR interface VPC endpoints cannot
  reach ECR or CloudWatch Logs; this surfaces as a `CannotPullContainerError`
  and is a networking gap, not an ECR permissions issue, if the task
  execution role is otherwise correctly scoped.

## Security and Best Practices

- Scope every Lambda execution role and ECS task role to only the actions
  and resources that function or service actually calls; never attach a
  broad managed policy such as `AmazonDynamoDBFullAccess` to a function
  that only performs `GetItem`/`PutItem` on one table.
- Separate the ECS **task role** (permissions the application code uses at
  runtime) from the **task execution role** (permissions ECS itself needs
  to pull the image and write logs) — do not grant application-level
  permissions on the execution role.
- Scan container images in ECR before deployment (Amazon Inspector
  integration, covered further in Chapter 08) and block deployment of
  images with critical unpatched CVEs through a CI/CD gate.
- Store application secrets (database credentials, API keys) in AWS
  Secrets Manager or Systems Manager Parameter Store, referenced by ARN
  in the task definition or Lambda environment configuration — never
  embedded in a container image or Lambda deployment package.
- Enforce HTTPS-only listeners on every ALB and terminate TLS using AWS
  Certificate Manager certificates rather than self-managed certificates
  on individual instances.
- Enable AWS WAF on internet-facing ALBs and API Gateway stages that
  accept unauthenticated traffic, and set API Gateway throttling limits
  to blunt volumetric abuse before it reaches backend compute.
- Set Lambda **reserved concurrency** on functions that call a
  limited-capacity downstream dependency (a small RDS instance, a
  third-party API with a rate limit) to prevent a traffic spike from
  overwhelming that dependency.

## References and Knowledge Checks

**References**

- Amazon EC2 Auto Scaling documentation — launch templates and scaling
  policies.
- Amazon ECS and Amazon EKS documentation, including the Fargate launch
  type.
- AWS Lambda documentation — execution roles, VPC networking, and
  concurrency controls.
- AWS Step Functions and Amazon EventBridge documentation.
- Elastic Load Balancing documentation — Application, Network, and
  Gateway Load Balancers.
- [CERTIFICATION_BLUEPRINTS.md](../../../CERTIFICATION_BLUEPRINTS.md) —
  this chapter maps to the compute and application-architecture domains of
  the AWS Certified Solutions Architect blueprint.

**Knowledge checks**

1. What is the practical operational trade-off between running ECS tasks
   on EC2-launch-type worker nodes versus Fargate?
2. Why is an over-broad Lambda execution role a direct privilege-
   escalation risk rather than only a defense-in-depth concern?
3. When would a Network Load Balancer be the correct choice over an
   Application Load Balancer?
4. Why must event-driven consumers be designed for idempotency even when
   using a durable queue like Amazon SQS?

## Hands-On Lab

**Objective:** Deploy a Lambda function behind an HTTP API Gateway with a
least-privilege execution role, verify successful invocation, and confirm
that removing the required IAM permission produces an authorization
failure.

**Cost implications:** This lab uses AWS Lambda, API Gateway (HTTP API),
and DynamoDB, all of which have perpetual free-tier allowances well beyond
this lab's call volume. No NAT gateway or EC2 instance is required. Cost
exposure is negligible if cleanup is completed, but complete it anyway to
avoid leaving unused resources.

**Prerequisites**

- An AWS account with AWS CLI v2 configured and permissions for Lambda,
  API Gateway, IAM, and DynamoDB.
- A local shell with `zip` available for packaging the function.

**Steps**

1. Create a minimal DynamoDB table and package a simple handler:

   ```bash
   aws dynamodb create-table \
     --table-name lab-orders \
     --attribute-definitions AttributeName=id,AttributeType=S \
     --key-schema AttributeName=id,KeyType=HASH \
     --billing-mode PAY_PER_REQUEST

   cat > index.mjs <<'EOF'
   import { DynamoDBClient, PutItemCommand } from "@aws-sdk/client-dynamodb";
   const client = new DynamoDBClient({});
   export const handler = async (event) => {
     await client.send(new PutItemCommand({
       TableName: process.env.TABLE_NAME,
       Item: { id: { S: Date.now().toString() } }
     }));
     return { statusCode: 200, body: "order recorded" };
   };
   EOF
   zip orders-processor.zip index.mjs
   ```

2. Create the execution role scoped to only `PutItem` on the lab table and
   basic log permissions (adapt the Terraform IAM policy from the
   Implementation section, or apply equivalently via CLI), then create the
   function:

   ```bash
   aws lambda create-function \
     --function-name lab-orders-processor \
     --runtime nodejs20.x \
     --handler index.handler \
     --role "$LAMBDA_ROLE_ARN" \
     --zip-file fileb://orders-processor.zip \
     --environment "Variables={TABLE_NAME=lab-orders}"
   ```

   **Expected result:** JSON output containing `"State": "Active"` (or
   `Pending` transitioning to `Active` on the next `get-function` call).

3. Create an HTTP API and route to the function:

   ```bash
   API_ID=$(aws apigatewayv2 create-api \
     --name lab-orders-api --protocol-type HTTP \
     --target "$(aws lambda get-function --function-name lab-orders-processor \
       --query 'Configuration.FunctionArn' --output text)" \
     --query "ApiId" --output text)

   aws lambda add-permission \
     --function-name lab-orders-processor \
     --statement-id apigw-invoke \
     --action lambda:InvokeFunction \
     --principal apigateway.amazonaws.com \
     --source-arn "arn:aws:execute-api:$(aws configure get region):$(aws sts get-caller-identity --query Account --output text):$API_ID/*/*"
   ```

4. Invoke the deployed endpoint and confirm the record was written:

   ```bash
   curl -s "https://$API_ID.execute-api.$(aws configure get region).amazonaws.com/"
   aws dynamodb scan --table-name lab-orders --select COUNT
   ```

   **Expected result:** The `curl` call returns `order recorded`, and the
   `scan` count is `1` (or higher on repeated invocation).

5. **Negative test:** Remove the DynamoDB `PutItem` permission from the
   role and invoke again:

   ```bash
   aws iam delete-role-policy --role-name <LAMBDA_ROLE_NAME> --policy-name scoped-access
   curl -s -o /dev/null -w "%{http_code}\n" \
     "https://$API_ID.execute-api.$(aws configure get region).amazonaws.com/"
   ```

   **Expected result:** A `502` (Lambda invocation error surfaced through
   API Gateway); `aws logs tail /aws/lambda/lab-orders-processor` shows an
   `AccessDeniedException` from DynamoDB, confirming the least-privilege
   role is what allowed the write in step 4, not an implicit broader grant.

6. **Cleanup:**

   ```bash
   aws apigatewayv2 delete-api --api-id "$API_ID"
   aws lambda delete-function --function-name lab-orders-processor
   aws dynamodb delete-table --table-name lab-orders
   aws iam delete-role --role-name <LAMBDA_ROLE_NAME>
   rm -f orders-processor.zip index.mjs
   ```

   Confirm removal:

   ```bash
   aws lambda get-function --function-name lab-orders-processor
   ```

   The command must return a `ResourceNotFoundException`.

## Summary and Completion Checklist

AWS compute options form a spectrum from EC2's full instance control
through ECS/EKS container orchestration to Lambda's fully abstracted
execution, and the correct choice balances operational ownership against
per-unit cost rather than defaulting to the most abstracted option
everywhere. Auto Scaling groups, ECS services, and Lambda concurrency each
provide a different scaling unit and failure-recovery model. Application,
Network, and Gateway Load Balancers serve distinct traffic patterns, and
Step Functions and EventBridge turn ad hoc orchestration code into
observable, retryable workflow definitions. Every compute option shares
one non-negotiable control: the execution or task role must be scoped to
exactly what the code needs, since an over-broad role converts an
application vulnerability directly into an infrastructure compromise.

- [ ] Can select the correct compute option (EC2, ECS/EKS, Fargate,
      Lambda) for a stated workload profile.
- [ ] Can configure an Auto Scaling group with a target-tracking policy.
- [ ] Can deploy a Fargate service behind an ALB with correctly separated
      task and execution roles.
- [ ] Can build a least-privilege Lambda function behind API Gateway.
- [ ] Completed the hands-on lab, including the negative test and cleanup.
