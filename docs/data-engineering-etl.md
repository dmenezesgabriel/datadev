# ETL

ETL stands for Extract, Transform, Load. It is a data integration process used to move data from various sources into a centralized data warehouse or database. The ETL process consists of three main steps:

1. **Extract**: In this step, data is collected from different source systems, which can include databases, APIs, flat files, or other data repositories. The goal is to gather all relevant data needed for analysis.

2. **Transform**: Once the data is extracted, it undergoes a series of transformations to clean, format, and structure it according to the requirements of the target system. This may involve data cleansing, normalization, aggregation, and enrichment to ensure data quality and consistency.

3. **Load**: The final step involves loading the transformed data into the target data warehouse or database. This can be done in bulk or incrementally, depending on the use case and system capabilities.

Tool Examples:

- AWS Glue
- Apache Airflow
