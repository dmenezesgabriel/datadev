# System Architecture - Monolith

## Description

A monolithic architecture is a system where the entire application is built and deployed as a single unit.

All components, such as the user interface (server side rendering), business logic, and data access layer, are tightly integrated and run in the same codebase and are deployed together as one application.

## When to use

- Early-stage startups
- Small to medium systems
- Small engineering teams
- Well understood and stable domain
- Fast time-to-market requirements

If your product is still evolving and you need speed, a monolith is often the best first choice.

## Pros

1. Simplicity
    - One codebase
    - One deployment pipeline
    - Easy local development
    - Lower cognitive load for the team

2. Easier testing
    - No network calls between services
    - Integration tests are straightforward

3. Better performance (Initially)
    - In-memory calls instead of network calls
    - No distributed system overhead

4. Strong consistency
    - Single database
    - ACID transactions are simple

## Cons

1. Scalability Limitations
    - You scale the entire application, even if only one module needs more resources

2. Tight coupling
    - Changes in one module can affect others
    - Harder to evolve independently

3. Slower deployment overtime
    - Longer build times
    - Harder parallel team work

4. Technology lock-in
    - All parts must use the same language and framework

!!! note "Note"

    The problems usually are not the monolith itself, but the way it is structured. A well-structured monolith can be maintainable and scalable for a long time. The key is to modularize (Physical vs Logical Monolith) the codebase and enforce clear boundaries between components.

## Summary

> Any organization that designs a system (defined broadly) will produce a design whose structure is a copy of the organization's communication structure.
> -- Melvin Conway

System architecture tends to reflect team structure. If one team owns everything, a monolith is often natural.

Many successful companies started monolithic, they later decomposed when scaling required it.

## References

- [Article - ConwaysLaw, martin fowler](https://martinfowler.com/bliki/ConwaysLaw.html)
- [Video - MONOLITOS, Programador Lhama](https://www.youtube.com/watch?v=M_fux3vfMQ0&list=WL&index=3)
