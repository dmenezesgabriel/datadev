# /// script
# requires-python = ">=3.11,<3.13"
# dependencies = [
#     "python-dotenv==1.2.1",
#     "pandas==2.3.2",
#     "pandas-stubs==2.3.2.250827",
#     "numpy==2.3.2",
#     "scikit-learn==1.7.1",
# ]
# ///

import sys

sys.path.append("../../../../..")

import os
import pathlib
import pickle

import pandas as pd
from dotenv import load_dotenv
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

from notebooks.python.utils.data_extraction.data_extraction import (
    KaggleDataExtractor,
    KaggleExtractionConfig,
)

pd.set_option("display.max_columns", None)

load_dotenv()  # Root directory .env file

BASE_PATH = pathlib.Path("../../../machine-learning")
DATA_DIR = BASE_PATH / "data/predicting-customer-churn"
OUTPUT_DIR = BASE_PATH / "artifacts/predicting-customer-churn"

DATA_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

username = os.getenv("KAGGLE_USERNAME")
api_token = os.getenv("KAGGLE_API_TOKEN")
file_name = "WA_Fn-UseC_-Telco-Customer-Churn.csv"


def load_data():
    extractor = KaggleDataExtractor(username=username, api_token=api_token)

    config = KaggleExtractionConfig(
        dataset_slug="blastchar/telco-customer-churn",
        file_name=file_name,
        destination_path=DATA_DIR,
        output_file_name="churn.csv",
    )

    if not os.path.isfile(DATA_DIR / "churn.csv"):
        extractor.download_dataset(config)

    df = pd.read_csv(DATA_DIR / "churn.csv")

    df.columns = df.columns.str.lower().str.replace(" ", "_")

    categorical_columns = list(df.dtypes[df.dtypes == "object"].index)

    for column in categorical_columns:
        df[column] = df[column].str.lower().str.replace(" ", "_")

    df.totalcharges = pd.to_numeric(df.totalcharges, errors="coerce")
    df.totalcharges = df.totalcharges.fillna(0)

    df.churn = (df.churn == "yes").astype(int)

    return df


def train_model(df):
    numerical = ["tenure", "monthlycharges", "totalcharges"]

    categorical = [
        "gender",
        "seniorcitizen",
        "partner",
        "dependents",
        "phoneservice",
        "multiplelines",
        "internetservice",
        "onlinesecurity",
        "onlinebackup",
        "deviceprotection",
        "techsupport",
        "streamingtv",
        "streamingmovies",
        "contract",
        "paperlessbilling",
        "paymentmethod",
    ]

    y_train = df.churn
    train_dict = df[categorical + numerical].to_dict(orient="records")

    pipeline = make_pipeline(
        DictVectorizer(), LogisticRegression(solver="liblinear")
    )

    pipeline.fit(train_dict, y_train)

    return pipeline


def save_model(pipeline, output_file):
    with open(output_file, "wb") as f_out:
        pickle.dump(pipeline, f_out)


df = load_data()
pipeline = train_model(df)
save_model(pipeline, "model.bin")
