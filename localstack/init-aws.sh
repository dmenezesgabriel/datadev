#!/bin/sh
set -e

echo "Creating MLflow S3 bucket..."

aws --endpoint-url=http://localhost:4566 \
    s3 mb s3://mlflow-artifacts || true
