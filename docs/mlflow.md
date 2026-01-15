# MLflow

Allows to organize a experiment into runs and keep track of:

- Parameters
- Metrics
- Metadata
- Artifacts
- Models

Automatically logs extra information about the run like:

- Source code
- Version of the code (git commit)
- Start and end time
- Author

## Backend store

- Local file system
- SQLAlchemy compatible database (MySQL, Postgres, SQLite, etc)

## Artifact store

- Local file system
- Amazon S3
- Azure Blob Storage
- Google Cloud Storage
- HDFS

## MLflow Tracking API

- No tracking server: logs to local file system
- Localhost
- Remote server
