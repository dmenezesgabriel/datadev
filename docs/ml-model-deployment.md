# Deployment

Different ways models serve predictions.

## Types

| Type                       | When used                                         |
| -------------------------- | ------------------------------------------------- |
| **Online inference**       | Real-time APIs (fraud detection, recommendations) |
| **Batch inference**        | Scheduled predictions over datasets               |
| **Asynchronous inference** | Background processing without blocking clients    |
| **Streaming inference**    | Continuous events (Kafka, IoT)                    |

## Online (Real-time)

### When to Use

- You need **instant response** (ms to seconds)
- User is _waiting_ for the prediction
- Decision must happen **synchronously**
- High **business impact** per request

### Examples

- Credit card payment: approve or deny transaction instantly to prevent **fraud**
- Pix transfer: block suspicious transfers before money leaves the account
- Mobile banking app: show **personalized offers** such as credit limit or loans
    - batch: precomputed eligible offers
    - real-time: adjust based on recent user behavior
- Login attempt: detect suspicious device or location and trigger _MFA_
- E-commerce checkout: real-time **risk scoring** before approving purchase

### Implementation

- Lambda (container or zip): low traffic, lightweight inference APIs
- SageMaker Endpoints: managed ML model serving with autoscaling
- SageMaker Serverless Inference: intermittent workloads with unpredictable traffic
- ECS or Fargate: containerized ML APIs for scalable real-time inference
- EKS (Kubernetes): large-scale ML platforms and microservice-based serving
- EC2: custom deployments requiring full infrastructure control
- GPU endpoints (SageMaker, EKS, EC2): deep learning or large model inference

## Batch

### When to Use

- You have a **dataset** (S3, database, warehouse)
- Latency is _not important_ (minutes to hours)
- You want **cheap, large-scale processing**
- Predictions are **recomputed periodically**
- Work is _dataset-oriented_, not per request

### Examples

- Overnight job: recalculate **credit score** for all customers using latest data
- Daily marketing pipeline: decide which customers receive **loan or card offers**
- Monthly risk model: estimate **probability of default** for entire portfolio
- Regulatory reporting: compute risk exposure required by central bank
- Feature store: precompute **customer features** such as income trends and spending patterns
- Retail example: update **recommendations** for all users every night

### Implementation

- Lambda (container): small scheduled batch inference jobs
- SageMaker Batch Transform: large offline dataset inference
- Spark jobs (EMR or Databricks): distributed inference over massive datasets
- ECS or Kubernetes jobs: container-based batch inference pipelines
- Airflow or Step Functions with containers: orchestrated ML pipelines
- EC2 batch workers: custom large-scale batch processing
- Data warehouse SQL models (Snowflake or BigQuery): simple models executed directly in the warehouse

## Streaming

### When to Use

- Data arrives _continuously_ (events, logs, transactions)
- You need **near real-time decisions**
- System is **event-driven** and always running
- Time and order of data matters (windows, late events)
- High **throughput** and low latency

### Examples

- Card transaction stream: detect **fraud patterns** across multiple transactions in seconds
- Pix transactions: identify unusual behavior such as many transfers in short time
- ATM network: detect anomalies such as fraud or machine failures
- Customer activity: update **risk score** continuously as behavior changes
- Trading systems: flag abnormal trading activity instantly
- Ride-sharing: update pricing continuously based on demand

### Implementation

- Kafka and Flink: event-driven continuous inference pipelines
- Kafka and Spark Streaming: real-time stream processing with ML models
- AWS Kinesis and Lambda: lightweight streaming inference on event streams
- Apache Flink or Apache Beam pipelines: advanced large-scale real-time ML pipelines

## Asynchronous Inference

### When to Use

- Request is **too slow** for real-time
- Client should _not wait_ (non-blocking)
- Work can be processed in **background**
- Tasks are **independent** and scalable
- You expect _spiky workloads_

### Examples

- Customer uploads documents: KYC verification with OCR and fraud checks processed in background
- Loan application: full **credit analysis** using multiple models and external data sources
- Insurance claim: analyze images and documents to detect fraud
- Model explainability: generate detailed **explanations** after prediction
- Customer support: analyze thousands of messages using NLP
- Video platform: process uploaded video after upload for moderation or classification

### Implementation

- SageMaker Asynchronous Endpoints: long-running inference requests
- Queue and worker pattern (SQS with ECS or Lambda): background model processing

## Summary

- User is waiting: **Online**
- Process this dataset: **Batch**
- Process these requests later: **Async**
- Events never stop: **Streaming**

## Comparison table

| Aspect           | Online           | Batch                      | Async                | Streaming                     |
| ---------------- | ---------------- | -------------------------- | -------------------- | ----------------------------- |
| Trigger          | API call         | Schedule or event          | Queue or event       | Continuous events             |
| Work unit        | Single request   | Entire dataset             | Single request/task  | Event                         |
| Latency          | ms to seconds    | minutes to hours           | seconds to minutes   | ms to seconds                 |
| User waiting     | Yes              | No                         | No                   | Sometimes                     |
| Scaling          | Autoscaling APIs | Manual or distributed jobs | Horizontal via queue | Distributed stream processors |
| Cost             | Medium to high   | Low                        | Medium               | High (always running)         |
| Complexity       | Medium           | Low to medium              | Medium               | High                          |
| Failure handling | Retry request    | Rerun job                  | Retry per message    | Checkpointing                 |
