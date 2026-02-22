# System architecture - Microservices

## Description

A microservices architecture is a system design where the application is split into multiple small, independent services.

Each service:

- Has a single business **responsibility**
- Run as its own process
- Is deployed independently
- Often has its own database
- Communicates via network (HTTP, gRPC, messaging)

Example:

- User Service: Manages user accounts and authentication
- Payment Service: Handles payment processing
- Order Service: Manages customer orders

Each can scale independently, be developed by different teams, and use different technologies.

## When to use

- Large systems with growing complexity
- Large engineering teams
- Need for independent deployments and scaling
- Clear domain boundaries
- High scalability requirements
- Multiple teams working in parallel

Microservices are often adopted when monolith becomes a bottleneck in scalability or team velocity.

## Pros

1. Independent Scalability
    - Scale only what needs scaling

2. Team autonomy
    - Each team can deploy independently
    - Each team can choose the best technology stack for their service
    - Each team can release without coordinating with everyone
    - Improves development velocity at scale

3. Fault Isolation
    - If one service fails it may degrade functionality, but the whole system will not necessarily go down

4. Technology flexibility
    - Different services can use different stacks if needed

## Cons

1. Distributed System Complexity
    - Network latency
    - Partial failures
    - **Eventual consistency**: Is a temporary inconsistency window, till all services are updated. Example: User updates their email, but the change is not reflected in the Order Service until the next sync.
    - **Service discovery**: Services run in containers and instances scale up and down, IP addresses change frequently. Instead of hardcoding IP addresses, when a service starts it register itself in a _Service Registry_, then another service queries the registry to find it.
    - Observability challenges
    - Versioning problems

2. Data consistency challenges
    - You loose simple [ACID](./data-engineering-acid.md) transactions across services, now you need _Sagas_, event-driven consistency and idempotency strategies

3. DevOps Overhead
    - Many deployments
    - CI/CD pipelines
    - Monitoring for each service
    - Centralized logging
    - Distributed tracing

4. Higher operational cost
    - More infrastructure
    - More containers
    - More networking

## Summary

> Any organization that designs a system (defined broadly) will produce a design whose structure is a copy of the organization's communication structure.
> -- Melvin Conway

Microservices work best when aligned with bounded contexts (DDD). Example: separating Billing from Order Management because they represent distinct domains.

Not use micro services if:

- You have 3 engineers
- Early product stage
- Unclear domain boundaries

Most large-scale companies started with monoliths and moved to microservices after scale forced them to.

!!! Note "Note"

    Fault Tolerance is the ability of a system to continue operating correctly even when some components fail. The system does not crash entirely just because one part fails.

## References

- [Article - ConwaysLaw, martin fowler](https://martinfowler.com/bliki/ConwaysLaw.html)
- [Microsserviços, Programador Lhama](https://www.youtube.com/watch?v=a5u9z_NEII4)
