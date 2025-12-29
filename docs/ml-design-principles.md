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

- Stablish Machine Learning roles and responsibilities
- Prepare an profile template
  - Document resources required
- Establish model improvement strategies
  - Experiments
  - Hyper-parameter optimization
- Establish a lineage tracker system
  - Pipelines
  - Feature Store
  - Model Registry
- Establish feedback loops across ML lifecycle phases
  - Model monitoring
- Review fairness and expandability
- Design data encryption and obfuscation
  - PII
  - Masking
- Use APIs to abstract changes from model breaking application consumption
  - API Gateway
- Adopt a machine learning microservice strategy
  - Serverless functions
  - Serverless containers
- Define relevant evaluation metrics
- Identify if machine learning is the right solution
- Consider AI services and pre-trained models

**Architecture**:

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
F --> |Detect Drift, etc|G
G --> |Run monitoring on schedule|H
G --> |Performance Feedback loop Ex: Adjust bias|B
G --> |Active Learning Loop Ex: New data|D
A --> |Store artifacts|I
D --> |Store Model Version|I
I --> |Fetch Artifacts|E
C --> |Store Features|J
J --> |Copy to Offline|K
K --> |Batch Inference|E
J --> |Fetch Features|D
K --> |Fetch Features|D
```

### Data Processing

- Profile data to improve quality
  - Data wrangling
  - Data exploration
- Create tracking and version control mechanisms
  - Model Registry
  - Experiments
  - Code versioning on Git
- Ensure least privilege access
- Secure data and modeling environment

#### Data Collection

- Label: Set target variable values
- Ingest: Can be stream, batch or other methods
- Aggregate: Data can come from multiple sources

#### Data Preparation

**Data Preprocessing**:

- Clean: Missing data & Outliers
- Partition: Partition by dimension to efficient access
- Scale: Should use a distributed system like spark?
- Unbias & Balance: Deal with over representation of classes
- Augment: Add new or additional data

**Feature Engineering**:

- Feature Selection: Which features are most important
- Feature Transformation: Normalization, Encoding, etc
- Feature Creation: Transform the features you have in another ways
- Feature Extraction: Extract information from an address field
