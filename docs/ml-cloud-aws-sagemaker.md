# AWS Sagemaker

## Sagemaker Clarify

Analyze and monitor data [bias](./ml-problems-bias.md#bias) and model expandability to maintain fairness.

### Features

- Bias monitoring
- Exportable reports and graphs detailing bias in Sagemaker Studio
- Alerts in Cloud Watch when bias is above determined thresholds

### Use Cases

- Analyze bias in the input and output data captured from SageMaker real-time endpoints

### Requirements

- Must enable data capture in _Sagemaker Endpoints_

## Sagemaker Lineage Tracker

Track lineage of Machine Learning artifacts, such as datasets, models and experiments.

### Use Cases

- Auditability
- Reproducibility

## Sagemaker Model Monitor

### Features

- sagemaker-model-monitor-analyzer built-in image: custom monitoring jobs for analysis and reporting purposes
