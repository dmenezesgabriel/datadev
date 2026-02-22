# Infrastructure - Kubernetes

## Description

Kubernetes (k8s) is an open source container orchestration platform.

In simple terms:

Kubernetes manages and automates the deployment, scaling, networking, and lifecycle of containerized applications.

If docker run on one container, Kubernetes manages hundreds or thousands of containers across many machines

It solves problems like:

- Where should containers run?
- How many replicas should exist?
- What happens if a container crashes?
- How do services communicates?
- How we rollout a new version without downtime?

It uses a control loop model:

- You declare desired containers
- Controllers compare actual vs desired
- Controllers reconcile differences

## When to use

- You have multiple microservices
- You need auto-scaling
- You need high availability
- You deploy frequently CI/CD
- You need zero-downtime deployments
- You run workloads across multiple machines
- You need portability across cloud providers

Typical scenarios:

- SaaS platforms
- Microservices architectures
- Machine learning workloads
- large scale web applications
- Event driven systems

## Pros

- High availability
    - Automatically restarts failed containers
- Auto scaling
    - HPA (Horizontal Pod Autoscaler) scales based on metrics
- Rolling updates
    - Zero downtime deployments
- Self-healing
    - Recreates crashed containers
- Infrastructure abstraction
    - Works on AWS, GCP, Azure, on-premises
- Declarative configuration

## Cons

- High Complexity
    - Steep learning curve
- Operational overhead
    - Cluster maintenance, upgrades, network complexity
- Debugging can be hard
    - Distributed systems are inherently complex
- Overkill for small teams

## Core components

### Control Plane

- **API Server**: Entrypoint to the cluster (kubectl interacts with this)
- **etcd**: Key-value store for cluster state
- **Controller Manager**: Runs controllers to maintain cluster state (eg. Replicaset Controller)
- **Scheduler**: Assigns pods to nodes based on resource requirements and constraints

### Worker Nodes

- **Kubelet**: Agent that runs on each node, ensures containers are running
- **Container Runtime**: Docker, containerd, etc. that runs the actual containers
- **Kube Proxy**: Handles networking and load balancing for services

## Core Objects

### Pod

- Smallest deployable unit (one or more containers)
- Shared network and storage
- Ephemeral (can die anytime)

!!! note "Note"

    You rarely create pods directly in production. Instead, you use higher level controllers like Deployments or StatefulSets that manage pods for you.

### ReplicaSet

- Ensures a specified number of pod replicas are running
- If one pod dies, it creates a new one to maintain the desired count

### Deployment

- Manages ReplicaSets and provides declarative updates for pods
- Rolling updates
- Rollbacks
- Version control

### Service

- Provides stable network endpoint for a set of pods
- It solves the problem that Pods are ephemeral, IPs can change.

**Types**:

- ClusterIP (default): Internal access only
- NodePort: Exposes service on a static port on each node
- LoadBalancer: Provisions external load balancer (cloud provider)

### ConfigMap and Secret

- ConfigMap: Store non-sensitive configuration data
- Secret: Store sensitive data (passwords, API keys) with base64 encoding

### Namespace

- Logical isolation for resources

### Ingress

- Manages external access to services, typically HTTP

Example:

- `/api` -> service A
- `/web` -> service B
