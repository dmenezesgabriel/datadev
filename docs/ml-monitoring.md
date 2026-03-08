# Machine Learning Monitoring

## Attributes

- timestamp
- model_version
- request_id
- input_features
- prediction
- prediction_probability

## Data/Feature Quality

Catch data pipeline bugs.

| metric          | example               |
| --------------- | --------------------- |
| missing values  | feature suddenly null |
| range violation | age < 0               |
| category shift  | new country appears   |

## Performance

- Regression: RMSE, MAE, R²
- Classification: Accuracy, Precision, Recall, F1-score, AUC-ROC

Some problems get labels later.

Example:

| Use case        | label delay |
| --------------- | ----------- |
| fraud detection | days        |
| credit default  | months      |
| recommendation  | minutes     |

1. Join prediction_logs + ground_truth_labels
2. Compute metrics:
    - accuracy
    - precision
    - recall
    - auc
    - f1

## Drift

- Data Drift: Changes in data distribution
- Concept Drift: Changes in feature target relationship
- Prediction Drift: Changes in prediction rate. Ex: fraud_rate goes from 1% to 7%

Example:

1. Pull last 10k inference logs
2. Extract features
3. Compare with training dataset distribution
4. Compute drift metric
5. Trigger alert if threshold exceeded

Common methods:

| Method                           | When Used        |
| -------------------------------- | ---------------- |
| KS test                          | numeric features |
| PSI (Population Stability Index) | banking/credit   |
| Chi-square                       | categorical      |

## Operational

Classic service monitoring.

| metric     | meaning            |
| ---------- | ------------------ |
| latency    | inference time     |
| throughput | requests/sec       |
| error rate | failed predictions |
| CPU/GPU    | resource usage     |

Example:

- p95 latency
- request rate

## Explainability

- SHAP
- LIME

## Bias & Fairness

- Model bias/ fairness

## Deployment type

### Batch Deployment

Based on training data or past batch predictions:

- Expected data quality
- Data distribution type (e.g., Gaussian, Poisson)
- Descriptive statistics (mean, median, mode, stddev, min, max, percentiles)

### Non-Batch Deployment

Descriptive statistics and quality:

- Calculate metrics continuously or incrementally

Statistical tests on a continuous data stream:

- Pick a window function (e.g, moving windows or without moving reference) and "compare" windows.

## Common Tools

| Layer          | Tools               |
| -------------- | ------------------- |
| logging        | Kafka, Kinesis      |
| metrics        | Prometheus          |
| monitoring     | EvidentlyAI         |
| data warehouse | Snowflake, BigQuery |
| alerts         | PagerDuty           |
| dashboards     | Grafana             |
