# Infrastructure - Sidecar

## Description

A **sidecar** is a secondary container that runs alongside a main application container (e.g., an API) within the same ECS Task or Kubernetes Pod.
It provides **infrastructure capabilities**, such as logging, monitoring, security, networking, or caching, without embedding those concerns into the application code.
Both containers share the **same lifecycle, network (localhost), and optionally storage volumes**.

Common examples:

- Logging agents (Fluent Bit)
- Metrics exporters (Prometheus exporters)
- Network proxies (Envoy)
- Auth proxies (OAuth2 Proxy)
- Caching services (Redis)
- Secrets agents (Vault)

## When to use

Use a sidecar when an API needs **cross-cutting infrastructure capabilities** that should remain independent from application logic.

Typical scenarios:

- **Centralized logging** (ship logs to CloudWatch, ELK, Datadog)
- **Metrics and observability** (Prometheus exporters)
- **Service mesh networking** (Envoy / mTLS / retries / routing)
- **Authentication / authorization enforcement**
- **Local caching layer for performance**
- **Secrets retrieval and rotation**
- **ML systems**: model downloading, feature fetching, or model monitoring

## Pros

- **Separation of concerns** – application code focuses only on business logic
- **Reusability** – the same sidecar can be reused across many services
- **Standardized infrastructure** – logging, metrics, and security behave consistently
- **Isolation** – infrastructure tooling runs independently from the app
- **Local communication** – containers communicate via `localhost` with very low latency
- **Easier updates** – infrastructure components can be updated without changing the API

## Cons

- **Increased resource usage** – extra CPU and memory per task/pod
- **Operational complexity** – more containers to manage and debug
- **Tighter lifecycle coupling** – sidecar crashes may impact the main application
- **Networking complexity** – traffic routing through proxies may complicate debugging
- **Scaling inefficiency** – sidecar scales with the app even if not strictly needed
