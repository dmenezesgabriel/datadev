# Deployment & Monitoring

Different ways models serve predictions.

## Types

| Type                    | When used                                         |
| ----------------------- | ------------------------------------------------- |
| **Online inference**    | Real-time APIs (fraud detection, recommendations) |
| **Batch inference**     | Scheduled predictions over datasets               |
| **Streaming inference** | Continuous events (Kafka, IoT)                    |

## ML Inference Infrastructure

### Online (Real-time)

- Lambda (container or zip): low traffic, lightweight inference APIs
- SageMaker Endpoints: managed ML model serving with autoscaling
- SageMaker Serverless Inference: intermittent workloads with unpredictable traffic
- ECS / Fargate: containerized ML APIs for scalable real-time inference
- EKS (Kubernetes): large-scale ML platforms and microservice-based serving
- EC2: custom deployments requiring full infrastructure control
- GPU endpoints (SageMaker / EKS / EC2): deep learning or large model inference

### Batch

- Lambda (container): small scheduled batch inference jobs
- SageMaker Batch Transform: large offline dataset inference
- Spark jobs (EMR / Databricks): distributed inference over massive datasets
- ECS / Kubernetes jobs: container-based batch inference pipelines
- Airflow / Step Functions + containers: orchestrated ML pipelines
- EC2 batch workers: custom large-scale batch processing
- Data warehouse SQL models (Snowflake / BigQuery): simple models executed directly in the warehouse

### Streaming

- Kafka + Flink: event-driven continuous inference pipelines
- Kafka + Spark Streaming: real-time stream processing with ML models
- AWS Kinesis + Lambda: lightweight streaming inference on event streams
- Apache Flink / Apache Beam pipelines: advanced large-scale real-time ML pipelines

### Asynchronous Inference

- SageMaker Asynchronous Endpoints: long-running inference requests
- Queue + worker pattern (SQS + ECS / Lambda): background model processing
