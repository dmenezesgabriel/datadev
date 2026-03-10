# Feature Store

## Description

A feature store is a centralized system that stores, manages and serves _machine learning features_ so they can be reused consistently between _training_ and _production_.

Instead of recomputing features every time in spread training scripts, batch jobs and API's, The feature store computes them once and stores for _reuse_.

A proper feature store usually contains:

1. **Feature definitions**:
    - The transformation logic that creates the feature

2. **Offline store**:
    - Used for training datasets
    - Used for batch inference
    - Large historical data stored in system like data lakes or warehouses

3. **Online store**:
    - Low-latency storage during real-time inference
    - Example: Redis, DynamoDB

4. **Feature Pipelines**:
    - Jobs that compute and update features from raw data
    - Example: AWS Glue Jobs, AWS EMR

5. **Feature Serving**:
    - API's or SDKs that allow models to retrieve features consistently

Without a feature store is very common for training features to be generated in one codebase while production features are generated in another. This may cause **training-serving skew**, when model sees different data in production than it saw on training

A feature store ensures:

- The **same feature logic**
- The **same definitions**
- The **same transformations**

## When to Use

1. Multiple models reuse the same features
    - Fraud detection model, recommendation model and churn model could all use `user_lifetime_value`, `transactions_last_7_days`, `avg_purchase_value`

2. Real time inference requires consistent features and they must be available with low latency
    - Credit scoring API
    - Fraud detection
    - Recommendation API

3. The ML organization is scaling
    - Many models exist
    - Many engineers create features
    - reproducibility matters

4. Historical feature reconstruction is needed
    - For training you need features as they existed in a specific time in past to avoid data _leakage_. Feature stores support **point-in-time joins**

## Point In time Correctness.

- `feature_timestamp <= prediction_timestamp`

Without point-in-time corrects the model see data from the "future", and it may cause:

- Training accuracy to become misleading
- Model overfits to leaked information
- Production performance drops
