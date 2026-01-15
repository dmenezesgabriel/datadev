# Machine Learning Pipelines

A.K.A Workflow Orchestration

Is a sequence of steps needed to produce the machine learning model.

```mermaid
flowchart LR
    A[Data Ingestion] e1@--> B[Data Validation]
    B e2@--> C[Data Preprocessing]
    C e3@--> D[Feature Engineering]
    D e4@--> E[Hyperparameter Tuning]
    E e5@--> F[Training final model]
    F e6@-->|save to| G[Model Registry]

    e1@{ animation: fast }
    e2@{ animation: fast }
    e3@{ animation: fast }
    e4@{ animation: fast }
    e5@{ animation: fast }
    e6@{ animation: fast }
```

## Tools

General purpose workflow orchestration tools:

- Airflow
- Prefect
- Mage
- Luigi

ML specific workflow orchestration tools:

- Kubeflow
- MLflow Pipelines
