# /// script
# requires-python = ">=3.11,<3.13"
# dependencies = [
#     "pandas==2.3.2",
#     "pandas-stubs==2.3.2.250827",
#     "numpy==2.3.2",
#     "pyarrow==22.0.0",
#     "scikit-learn==1.7.1",
#     "xgboost==3.1.2",
#     "mlflow==3.7.0",
# ]
# ///

import logging
import pathlib
import pickle
import sys

import mlflow
import pandas as pd
import xgboost as xgb
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import root_mean_squared_error

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("taxi-duration-training")

MLFLOW_URI = "http://localhost:5000"
BASE_PATH = pathlib.Path("../../machine-learning")
OUTPUT_DIR = BASE_PATH / "artifacts/taxi-trip-duration"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

logger.info("🚀 Setting MLflow tracking URI: %s", MLFLOW_URI)
mlflow.set_tracking_uri(MLFLOW_URI)

logger.info("🧪 Using MLflow experiment: nyc-taxi-experiment")
mlflow.set_experiment("nyc-taxi-experiment")


def read_dataframe(year, month):
    logger.info("📥 Loading data for %04d-%02d", year, month)

    url = (
        "https://d37ci6vzurychx.cloudfront.net/trip-data/"
        f"green_tripdata_{year}-{month:02d}.parquet"
    )
    df = pd.read_parquet(url)

    df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
    df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
    df["duration"] = df.lpep_dropoff_datetime - df.lpep_pickup_datetime
    df.duration = df.duration.apply(lambda td: td.total_seconds() / 60)

    df = df[(df.duration >= 1) & (df.duration <= 60)]

    categorical = ["PULocationID", "DOLocationID"]
    df[categorical] = df[categorical].astype(str)

    logger.info("🧹 Records after filtering: %d", len(df))
    return df


def create_X(df, dv=None):
    categorical = ["PULocationID", "DOLocationID"]
    numerical = ["trip_distance"]

    dicts = df[categorical + numerical].to_dict(orient="records")

    if dv is None:
        logger.info("🧠 Fitting DictVectorizer")
        dv = DictVectorizer(sparse=True)
        X = dv.fit_transform(dicts)
    else:
        logger.info("🔁 Transforming data using existing DictVectorizer")
        X = dv.transform(dicts)

    return X, dv


def train_model(X_train, y_train, X_val, y_val, dv):
    logger.info("🏋️ Starting model training")

    with mlflow.start_run() as run:
        train = xgb.DMatrix(X_train, label=y_train)
        valid = xgb.DMatrix(X_val, label=y_val)

        best_params = {
            "learning_rate": 0.09585355369315604,
            "max_depth": 30,
            "min_child_weight": 1.060597050922164,
            "objective": "reg:squarederror",
            "reg_alpha": 0.018060244040060163,
            "reg_lambda": 0.011658731377413597,
            "seed": 42,
        }

        logger.info("⚙️ Training XGBoost with params: %s", best_params)
        mlflow.log_params(best_params)

        booster = xgb.train(
            params=best_params,
            dtrain=train,
            num_boost_round=30,
            evals=[(valid, "validation")],
            early_stopping_rounds=29,
        )

        y_pred = booster.predict(valid)
        rmse = root_mean_squared_error(y_val, y_pred)

        logger.info("📊 Validation RMSE: %.4f", rmse)
        mlflow.log_metric("rmse", rmse)

        logger.info("💾 Saving preprocessor")
        with open(OUTPUT_DIR / "processor.b", "wb") as f_out:
            pickle.dump(dv, f_out)

        mlflow.log_artifact(
            OUTPUT_DIR / "processor.b", artifact_path="preprocessor"
        )

        logger.info("📦 Logging model to MLflow")
        mlflow.xgboost.log_model(
            booster,
            name="models_mlflow",
            input_example=X_train[:10],
        )

        logger.info("✅ Training finished successfully")
        return run.info.run_id


def run(year, month):
    logger.info("▶️ Pipeline started for %04d-%02d", year, month)

    df_train = read_dataframe(year=year, month=month)

    next_year = year if month < 12 else year + 1
    next_month = month + 1 if month < 12 else 1
    df_val = read_dataframe(year=next_year, month=next_month)

    X_train, dv = create_X(df_train)
    X_val, _ = create_X(df_val, dv)

    target = "duration"
    y_train = df_train[target].values
    y_val = df_val[target].values

    run_id = train_model(X_train, y_train, X_val, y_val, dv)

    logger.info("🎯 MLflow run_id: %s", run_id)

    return run_id


if __name__ == "__main__":
    logger.info("🟢 Script execution started")

    import argparse

    parser = argparse.ArgumentParser(
        description="Train a model to predict taxi trip duration"
    )
    parser.add_argument(
        "--year", type=int, required=True, help="Year of the data to train on"
    )
    parser.add_argument(
        "--month",
        type=int,
        required=True,
        help="Month of the data to train on",
    )
    args = parser.parse_args()

    run_id = run(year=args.year, month=args.month)

    logger.info(f"run_id {run_id}")
