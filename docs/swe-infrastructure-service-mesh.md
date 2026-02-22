# Infrastructure - Service Mesh

## Description

A Service Mesh is an infrastructure layer that manages _service-to-service_ communication in a microservices architecture.

Instead of each service implementing thins like:

- Retries
- Timeouts
- Circuit breaking
- TLS encryption
- Observability
- Traffic routing

Those responsibilities are handled by mesh

It is usually by injecting a sidecar proxy (like Envoy) alongside each service instance. The proxies handle all the network communication, and the service code can focus on business logic.

Popular implementation:

- Istio
- Linkerd
- Consul

## When to use

- You have many services
- Network communication is complex
- Remove networking logic from application code
- You use Kubernetes

## Pros

1. Separation of concerns
    - Network logic is moved out of application code
2. Consistent reliability patterns
    - Retries, timeouts, circuit breakers standardized
3. Strong security
    - mTLS encryption between services
4. Advanced traffic control
    - Canary releases, A/B testing, traffic splitting
5. Deep observability
    - Automatic metrics and tracing

## Cons

1. Operational Complexity
    - Hard to configure and debug
    - Learning curve is high

2. Performance Overhead
    - Sidecar proxies add latency and memory usage

3. Debugging becomes harder
    - More layers

4. Overkill for small systems
    - Adds more problems than it solves in simple architectures

## Summary

- Service mesh is Layer 7 infrastructure control plane for service communication
- It externalizes cross-cutting network concerns
- It relies on sidecar proxies
- It improves security via mTLS and identity-based policies
- It increases operational complexity
- It is not mandatory for microservices — only justified at scale
