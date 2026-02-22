# Deployment Strategies - Rolling Deployment

## Description

A rolling update is a deployment strategy where a new version of an application is gradually rolled out to replace the old version without downtime.

## When to use

- When zero downtime is required but immediate full replacement is not necessary
- For stateful or stateless applications where gradual replacement is safe

## Pros

- No downtime
- Reduced risk
- Resource efficient
    - No need to provision a full new environment upfront

## Cons

- Longer deployment time
- Potential version mismatch
    - Different servers may run different versions temporarily, which can cause issues if your app isn’t backward compatible.
- Rollback complexity
    - Rolling back partially updated systems can be tricky if multiple versions are running simultaneously.

## Comparison of Deployment Strategies

| Strategy        | How It Works in Practice                                                                                                                        | User Impact / Traffic Handling                                                                    | Pros                                                                   | Cons                                                            |
| --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- | --------------------------------------------------------------- |
| **Blue-Green**  | Two separate environments: **Blue** (current) and **Green** (new). Traffic is switched instantly from Blue → Green when Green is ready.         | Users see either 100% old (Blue) or 100% new (Green). No mixing.                                  | Instant rollback (switch back to Blue), zero downtime.                 | Requires double infrastructure (both environments active).      |
| **Canary**      | Deploy new version to a small subset of servers or users (e.g., 10%). Gradually increase to 50%, then 100%.                                     | Some users see the new version, others still on old. Weighted routing needed (e.g., 10% traffic). | Detects issues early, lower risk than full rollout.                    | Needs careful monitoring, may expose bugs to early users.       |
| **Rolling**     | Gradually replace old servers with new ones (e.g., 2 of 10 servers at a time).                                                                  | Users may hit old or new instances randomly while rollout is ongoing.                             | No extra infrastructure, zero downtime.                                | Mixed-version issues possible, rollout takes longer.            |
| **A/B Testing** | Run two versions simultaneously for comparison (e.g., Feature A vs Feature B). Users are assigned to a variant, usually via cookies or session. | Users see one version only (based on assignment), not for full deployment.                        | Ideal for experimenting with features, measure performance/engagement. | Not for full version replacement; only for feature experiments. |

!!! note "Note"

    - **Blue-Green**: Users never see a half-updated system; either full old or full new. Very safe but expensive.
    - **Canary**: Users are “weighted” by traffic percentages. E.g., 10% of requests go to the new version first.
    - **Rolling**: Users may hit mixed versions during rollout; your app must handle backward compatibility.
    - **A/B**: Only used for experiments, not for production version upgrade; traffic split is deterministic per user/session.
