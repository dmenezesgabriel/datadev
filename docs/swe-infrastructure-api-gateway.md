# Infrastructure - API Gateway

## Description

An API Gateway is a server that acts as a single entrypoint for clients to access services (often microservices).

Instead of clients calling multiple services directly, the call the API Gateway, which:

- Routes the requests to correct service
- Handles authentication and authorization
- Applies rate limiting
- Performs request/response transformation
- Aggregate responses for multiple services

In microservices architectures, it prevents clients from needing to know the internal service locations.

Common examples:

- AWS API Gateway
- Kong
- Apigee
- NGINX (when used as gateway)

## When to use

1. Microservices architecture:
    - You have many services and want one external endpoint

2. Cross-cutting concerns need centralization:
    - Authentication (JWT, OAuth)
    - Logging
    - Rate Limiting
    - Caching
    - Monitoring

3. Client-specific APIs:
    - Mobile vs Web vs Internal consumers (Backend-for-Frontend pattern)

4. Security Isolation:
    - Hide internal service details from clients

5. Protocol Translation:
    - Convert between protocols (e.g. REST to gRPC)

## Pros

- Simplify clients
    - Clients call one endpoint instead of many services.
- Centralized security
    - Auth, throttling, and policies in one place.
- Decouples clients from services
    - Internal services can change without breaking external clients
- Observability and control
    - Easier monitoring, analytics and traffic management
- Response aggregation
    - Combine multiple service calls in one response

## Cons

- Single point of failure (if not highly available)
    - Must be replicated and load balanced
- Latency overhead
- Operational complexity
    - Another component to manage and scale
- Risk of violating separation of concerns

## Main responsibility

- Authentication and Authorization (OAuth, JWT)
- Rate limiting per consumer
- API key management
- Request/response transformation
- API versioning
- Monitoring per endpoint
- Developer portal integration
