# /// script
# requires-python = ">=3.11,<3.13"
# dependencies = [
# "evidently==0.7.20",
# "joblib>=1.5.3",
# "mlflow==3.7.0",
# "numpy==2.3.2",
# "pandas==2.3.2",
# "pandas-stubs==2.3.2.250827",
# "prefect==3.6.11",
# "psycopg==3.3.2",
# "psycopg-binary==3.3.2",
# "pyarrow==22.0.0",
# "requests==2.32.5",
# "scikit-learn==1.7.1",
# "tqdm==4.67.1",
# "xgboost==3.1.2",
# ]
# ///


import datetime
import logging
import pathlib
import random
import time

import joblib
import pandas as pd
import psycopg
from evidently import DataDefinition, Dataset, Report
from evidently.metrics import (
    DriftedColumnsCount,
    MissingValueCount,
    ValueDrift,
)
from prefect import flow, task

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s"
)

BASE_PATH = pathlib.Path("../../machine-learning")
DATA_DIR = BASE_PATH / "data/taxi-trip-duration"
OUTPUT_DIR = BASE_PATH / "artifacts/taxi-trip-duration"

DATA_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

SEND_TIMEOUT = 10
CONNECTION_STRING = "host=localhost port=5433 user=metrics password=metrics"

CONNECTION_STRING_DB = f"{CONNECTION_STRING} dbname=metrics"


rand = random.Random()

create_table_statement = """
DROP TABLE IF EXISTS metrics;
CREATE TABLE metrics(
    timestamp TIMESTAMP,
    prediction_drift FLOAT,
    num_drifted_columns INTEGER,
    share_missing_values float
)
"""

reference_data = pd.read_parquet(DATA_DIR / "reference.parquet")
with open(OUTPUT_DIR / "lin_reg.bin", "rb") as f_in:
    model = joblib.load(f_in)

raw_data = pd.read_parquet(DATA_DIR / "green_tripdata_2022-02.parquet")

begin = datetime.datetime(2022, 2, 1, 0, 0)
num_features = [
    "passenger_count",
    "trip_distance",
    "fare_amount",
    "total_amount",
]
cat_features = ["PULocationID", "DOLocationID"]
data_definition = DataDefinition(
    numerical_columns=num_features + ["prediction"],
    categorical_columns=cat_features,
)
report = Report(
    metrics=[
        ValueDrift(column="prediction"),
        DriftedColumnsCount(),
        MissingValueCount(column="prediction"),
    ]
)


@task
def prep_db():
    with psycopg.connect(CONNECTION_STRING, autocommit=True) as conn:
        res = conn.execute("SELECT 1 FROM pg_database WHERE datname='test'")
        if len(res.fetchall()) == 0:
            conn.execute("CREATE DATABASE test")
        with psycopg.connect(CONNECTION_STRING_DB) as conn:
            conn.execute(create_table_statement)


@task
def calculate_metrics(i):
    current_data = raw_data[
        (raw_data.lpep_pickup_datetime >= (begin + datetime.timedelta(i)))
        & (raw_data.lpep_pickup_datetime < begin + datetime.timedelta(i + 1))
    ]

    current_data["prediction"] = model.predict(
        current_data[num_features + cat_features].fillna(0)
    )

    current_dataset = Dataset.from_pandas(
        current_data, data_definition=data_definition
    )
    reference_dataset = Dataset.from_pandas(
        reference_data, data_definition=data_definition
    )

    run = report.run(
        reference_data=reference_dataset, current_data=current_dataset
    )

    result = run.dict()

    prediction_drift = result["metrics"][0]["value"]
    num_drifted_columns = result["metrics"][1]["value"]["count"]
    share_missing_values = result["metrics"][2]["value"]["share"]

    with psycopg.connect(CONNECTION_STRING_DB, autocommit=True) as conn:
        with conn.cursor() as curr:
            curr.execute(
                "insert into metrics(timestamp, prediction_drift, num_drifted_columns, share_missing_values) values (%s, %s, %s, %s)",
                (
                    begin + datetime.timedelta(i),
                    prediction_drift,
                    num_drifted_columns,
                    share_missing_values,
                ),
            )


@flow
def batch_monitoring_backfill():
    prep_db()
    last_send = datetime.datetime.now() - datetime.timedelta(seconds=10)
    for i in range(0, 27):
        calculate_metrics(i)

        new_send = datetime.datetime.now()
        seconds_elapsed = (new_send - last_send).total_seconds()
        if seconds_elapsed < SEND_TIMEOUT:
            time.sleep(SEND_TIMEOUT - seconds_elapsed)
        while last_send < new_send:
            last_send = last_send + datetime.timedelta(seconds=10)
        logging.info("data sent")


if __name__ == "__main__":
    batch_monitoring_backfill()
