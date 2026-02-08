# AWS Sagemaker

## Sagemaker Clarify

Analyze and monitor data [bias](./ml-problems-bias.md#bias) and model expandability to maintain fairness.

### Features

- Bias monitoring. Alerts in Cloud Watch when _bias_ is above determined thresholds
- Continuous monitoring of _feature attribution drift_. Alerts in Cloud Watch when significant feature attribution drift is detected
- Exportable reports and graphs detailing bias in Sagemaker Studio

### Use Cases

- Analyze bias in the input and output data captured from SageMaker real-time endpoints
- Detect changes in how model attributes importance to features (Ex: Model starts relying more on zipcode than before)

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

## Sagemaker Model Registry

Purpose built for storing, versioning and managing Machine Learning models. Allows users to organize models into _model groups_, which act as containers for different versions of a model.

- [Official docs](https://docs.aws.amazon.com/sagemaker/latest/dg/model-registry.html)

### Features

- Manage model versions and associate model versions within a model group
- Catalog models for production
- Associate metadata, such as training metrics, with a model
- Manage the approval status of a model
- Share models with others
- Organize model groups into collections

## Sagemaker Data Wrangler

### Features

- Corrupt image transform: preprocess data by simulating variations in image quality, such as blurring, noise, and compression artifacts. This can help improve the robustness of models to real-world conditions where image quality may vary
- Balanced data: oversample minority classe to resolve class imbalance

## Sagemaker Canvas

## Sagemaker JumpStart

## Sagemaker Auto Model Tuning (AMT)

### Use Cases

- Hyperparameter tunning

## Sagemaker Pipelines

Is a service that allows you to create, automate, and manage end-to-end machine learning workflows. It provides a way to define and orchestrate the various steps involved in the machine learning process, such as data preprocessing, model training, and deployment.

## Sagemaker Endpoints

### Features

- multi-model endpoints: host multiple models on a single endpoint and route inference requests to the appropriate model based on the request content or other criteria. This can help reduce costs and improve resource utilization by sharing infrastructure across multiple models
- Auto-scaling: automatically adjust the number of instances serving the endpoint based on the incoming traffic. This can help ensure that the endpoint can handle varying workloads while optimizing costs by scaling down during periods of low demand.

## Sagemaker Real-Time Inference

### Use Cases

- Low latency applications

## Sagemaker Shadow Testing

### Use Cases

- Test new models in production without impacting end-users

### Features

- Route a copy of live customer data to the new model for evaluation while maintaining the production model's operation. Compare predictions of both models to assess performance

## SageMaker Batch Transform

### Use Cases

- Offline, large-scale batch processing

## Sagemaker Feature Store

### Features

- Fully managed repository for storing, updating and retrieving machine learning features

## Sagemaker Ground Truth

### Features

- Human annotators for labeling data

## Sagemaker Debugger

### Use Cases

- Monitor training jobs in real time, detect issues, and automatically trigger actions such as stopping training or generating alerts.

### Features

- Detect vanishing gradients, GPU underutilization, overfitting, and other common training issues. Provides real-time insights into the training process, allowing users to identify and address issues quickly.
