from typing import Literal

import mlflow
import uvicorn
from fastapi import FastAPI
from mlflow.tracking import MlflowClient
from pydantic import BaseModel, Field

MLFLOW_TRACKING_URI = "http://mlflow:5000"

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

RUN_ID = "7c9f5938dcdc4db39cde2ca7d62b2c72"
logged_model = f"runs:/{RUN_ID}/model"

model = mlflow.pyfunc.load_model(logged_model)


class Customer(BaseModel):
    gender: Literal["male", "female"]
    seniorcitizen: Literal[0, 1]
    partner: Literal["yes", "no"]
    dependents: Literal["yes", "no"]
    phoneservice: Literal["yes", "no"]
    multiplelines: Literal["no", "yes", "no_phone_service"]
    internetservice: Literal["dsl", "fiber_optic", "no"]
    onlinesecurity: Literal["no", "yes", "no_internet_service"]
    onlinebackup: Literal["no", "yes", "no_internet_service"]
    deviceprotection: Literal["no", "yes", "no_internet_service"]
    techsupport: Literal["no", "yes", "no_internet_service"]
    streamingtv: Literal["no", "yes", "no_internet_service"]
    streamingmovies: Literal["no", "yes", "no_internet_service"]
    contract: Literal["month-to-month", "one_year", "two_year"]
    paperlessbilling: Literal["yes", "no"]
    paymentmethod: Literal[
        "electronic_check",
        "mailed_check",
        "bank_transfer_(automatic)",
        "credit_card_(automatic)",
    ]
    tenure: int = Field(..., ge=0)
    monthlycharges: float = Field(..., ge=0.0)
    totalcharges: float = Field(..., ge=0.0)


class PredictResponse(BaseModel):
    churn_probability: float
    churn: bool


app = FastAPI(title="customer-churn-prediction")


def predict_single(customer):
    result = model.predict_proba(customer)[0, 1]

    return float(result)


@app.post("/predict")
def predict(customer: Customer) -> PredictResponse:
    prob = predict_single(customer.model_dump())

    return PredictResponse(churn_probability=prob, churn=prob >= 0.5)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9696)
