# Infrastructure - Reverse Proxy

## Description

A reverse proxy is a server that sits between clients and backend servers.

Clients send requests to the reverse proxy, and forwards them to more internal severs. The client never talks directly to the backend servers.

Common reverse proxy technologies:

- NGINX
- Apache HTTP Server
- Traefik

How it works:

1. client sends HTTP request
2. Reverse proxy receives
3. It decides where to forward (based on rules like path, domain, headers)
4. backend process the request
5. Response goes back through the reverse proxy to the client

## When to use

1. Load Balancing:
    - Increase availability and distribute traffic across multiple backend servers

2. SSL Termination:
    - Handle https encryption at the proxy instead of each backend
    - Centralized certificate management

3. Security Layer
    - Hide internal IPs
    - Block malicious traffic
    - Rate limiting

4. Routing and URL Rewriting:
    - Route based on path, domain, headers
    - Rewrite URLs for cleaner APIs

5. Caching:
    - Cache static responses

6. Microservices Gateway:
    - Act as a single entry point for multiple microservices (similar to API Gateway but more focused on routing and load balancing)

## Pros

- Security
    - Backend servers are not directly exposed
    - Easier to implement firewall rules and DDoS protection

- Scalability
    - Horizontal scaling via load balancing

- Centralized concerns
    - Logging
    - Authentication
    - Compression
    - TLS termination
    - Rate limiting

- Performance
    - Connection pooling
    - Caching static content
    - Gzip compression

## Cons

- Single point of failure
    - If not configured in high availability mode, it can bring the whole system down

- Latency
    - One extra network hop adds latency, especially if the reverse proxy is doing heavy processing (e.g. SSL termination, compression)

- More infrastructure complexity
    - Extra components to configure
    - TLS routing, rules, health checks
    - Monitoring needed

- Debugging complexity
    - Harder to trace issues across client, proxy, and backend servers

!!! note "Note"

    In modern cloud architectures, reverse proxies often evolve into:
        - API Gateways
        - Ingress Controllers (Kubernetes)
        - Edge load balancers (Cloud ALB/ELB)

    At scale, you must consider:
        - Health checks
        - Circuit breaking
        - Timeouts
        - Retry policies
        - Sticky sessions
        - Zero-downtime deployments

## Main Responsibility

- Route requests (path/domain-based)
- Terminate TLS/SSL (handle https encryption)
- Cache responses (for static content)
- Compress responses (gzip)
- Add headers (for security or routing)
- Hide backend server details (IP, ports)
