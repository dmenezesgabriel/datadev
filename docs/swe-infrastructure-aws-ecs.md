# Infrastructure - AWS ECS

## Description

Amazon ECS is a fully managed container orchestration service provided by AWS.

It allows to run and manage Docker containers in the cloud without managing the orchestration logic yourself.

ECS helps with:

- Deploy containers
- Scale them automatically
- Load balance traffic
- Handle failures
- Integrate with other AWS services (ALB, IAM, CloudWatch)

You define:

- What containers to run (task definition)
- How much CPU/memory they need
- How many copies (tasks) to run

And ECS takes care of the rest

## When to use

- You are fully in AWS ecosystem
- You want simpler alternatives to Kubernetes
- You want tight integration with AWS services
- You team does not need Kubernetes complexity
- You want serverless containers (with Fargate)

Avoid if:

- You need multi-cloud portability
- You need advanced orchestration features (like custom schedulers, complex networking)

## Pros

- Fully managed by AWS
    - No control plane
- Deep AWS integration
    - ALB, IAM, CloudWatch, Secrets Manager
- Simpler than Kubernetes
- Fargate option
- Good for microservices and batch jobs

## Cons

- AWS vendor lock-in
- Smaller ecosystem than Kubernetes
- Less flexible than Kubernetes
- Fargate can be more expensive for long-running workloads

## Core Objects

### Cluster

- A logical grouping of compute capacity (EC2 instances or Fargate) where tasks run

### Task Definition

Blueprints for your container:

- Docker image
- CPU/memory requirements
- Environment variables
- Ports
- Logging configuration
- IAM roles

!!! note "Note"

    Close to a pod spec in Kubernetes.

### Task

- An instance of a task definition running on the cluster

!!! note "Note"

    Similar to a pod in Kubernetes.

### Service

- Manages long-running tasks
- Ensures desired number of tasks are running
- Auto-scaling
- Load balancing (with ALB)
- Rolling deployments

If one task crashes, ecs will automatically start a new one to maintain the desired count.

!!! note "Note"

    Services are used for stateless applications. For batch jobs, you can run standalone tasks without a service.
    They are similar to Deployments in Kubernetes.
