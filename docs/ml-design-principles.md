# Machine Learning Design Principles

- Ownership
- Security controls
- Fault tolerance
- Recoverability
- Reusability
- Reproducibility
- Resource optimization
- CI/CD, CT (Continuous training)
- Monitoring & Analysis
- Sustainability (minimize environment impact)

## Machine Learning Lifecycle

```mermaid
flowchart
  A[Business Goal] e1@--> B[ML Problem Framing]
  B e2@--> C[Data Processing]
  C e3@--> D[Model Development]
  D e4@--> E[Deployment]
  E e5@--> F[Monitoring]
  F e6@--> A

  e1@{ animate: true }
  e2@{ animate: true }
  e3@{ animate: true }
  e4@{ animate: true }
  e5@{ animate: true }
  e6@{ animate: true }
```

### Business Goal

- Discuss and agree on the level of model expandability
- Monitor model compliance to business requirements
- Validate the data permissions, privacy and license terms
- Determine key performance indicators
- Define overall return on investment (ROI) and opportunity cost

### Machine Learning Problem Framing

```mermaid
flowchart

subgraph Process Data
    A[Collect Data]
end

subgraph Prepare Data
    B[Preprocess Data]
    C[Feature Engineering]
end

D[Train, Tune & Evaluate]
E[Deploy]
F[Monitor]
G[Alarm Manager]
H[Scheduler]
I[Model Registry]

subgraph Feature Stores
    J[Online Feature Store]
    K[Offline Feature Store]
end

A --> B
B --> C
C --> D
D --> E
E --> F
F --> G
G --> H
G --> |Performance Feedback loop|B
A --> |Store artifacts|I
D --> I
I --> |Fetch Artifacts|E
C --> J
J --> |Copy to Offline|K
K --> |Batch Inference|E
J --> |Fetch Features|D
K --> |Fetch Features|D


```
