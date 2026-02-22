# Infrastructure - Load Balancer

## Description

A load balancer is a component that distributes incoming network traffic across multiple servers to improve _availability_, _scalability_, and _reliability_.

The load balancer decides which server should handle each request.

It can operate in different layers:

- Layer 4 (Transport Layer): Load balancing based on IP and port (e.g., TCP, UDP)
- Layer 7 (Application Layer): Load balancing based on HTTP attributes (e.g., URL, headers)

Examples:

- Nginx
- HAProxy
- AWS Elastic Load Balancing (ELB)
- Google Cloud Load Balancing

## When to use

- You have more than one server
- You need high availability (if one server goes down, others can take over)
- You expect traffic spikes
- You want zero downtime deployments
- You are running microservices
- You need horizontal scaling

## Pros

- High availability
- Horizontal scalability
- Automatic failover
    - Health checks
- Performance optimization
- Centralized SSL & Security
- Blue-green and canary deployments

## Cons

- Complexity (More infrastructure to manage)
- Potential bottleneck
- Cost
- Debugging complexity (harder to trace requests across multiple servers)
- Stick session issues, can break stateless scaling

## Main Responsibility

- Round-robin ( distribute incoming traffic across multiple backend servers)
- Least Connections (send to server with fewest active connections)
- Health checks (monitor backend server health and stop sending traffic to unhealthy ones)
- Failover (automatically route traffic to healthy servers if one fails)
- Sticky Sessions (route requests from same client to same backend server)
