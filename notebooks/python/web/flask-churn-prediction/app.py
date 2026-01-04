# ---
# jupyter:
#   language_info:
#     name: python
# ---

# %% [markdown]
# - [Notebook](notebooks/python/machine-learning/churn-prediction.md)

# %% [markdown]
# Install packages

# %%
# /// script
# requires-python = ">=3.11,<3.13"
# dependencies = [
#     "flask==3.1.2",
#     "scikit-learn==1.7.1",
#     "flask-smorest==0.46.2",
#     "marshmallow==4.1.1",
# ]
# ///

# %% [markdown]
# Import packages

# %%
import pickle
from pathlib import Path

from flask import Flask
from flask.views import MethodView
from flask_smorest import Api, Blueprint
from marshmallow import Schema, fields, validate

# %% [markdown]
# Create app + OpenAPI config

# %%

app = Flask(__name__)

app.config.update(
    API_TITLE="Churn Prediction API",
    API_VERSION="v1",
    OPENAPI_VERSION="3.0.3",
    OPENAPI_URL_PREFIX="/",
    OPENAPI_SWAGGER_UI_PATH="/docs",
    OPENAPI_SWAGGER_UI_URL="https://cdn.jsdelivr.net/npm/swagger-ui-dist/",
)

api = Api(app)

# %% [markdown]
# Load model artifacts

# %%

artifacts_path = Path("../../machine-learning/artifacts/")
model_path = artifacts_path / "predicting-customer-churn/model_C=10.bin"

with open(model_path, "rb") as f_in:
    dict_vectorizer, model = pickle.load(f_in)

# %% [markdown]
# Marshmallow schemas


# %%
class ChurnRequestSchema(Schema):
    gender = fields.Str(
        required=True,
        validate=validate.OneOf(["male", "female"]),
        metadata={"enum": ["male", "female"]},
    )

    seniorcitizen = fields.Int(
        required=True,
        validate=validate.OneOf([0, 1]),
        metadata={"enum": [0, 1]},
    )

    partner = fields.Str(
        required=True,
        validate=validate.OneOf(["yes", "no"]),
        metadata={"enum": ["yes", "no"]},
    )

    dependents = fields.Str(
        required=True,
        validate=validate.OneOf(["yes", "no"]),
        metadata={"enum": ["yes", "no"]},
    )

    phoneservice = fields.Str(
        required=True,
        validate=validate.OneOf(["yes", "no"]),
        metadata={"enum": ["yes", "no"]},
    )

    multiplelines = fields.Str(
        required=True,
        validate=validate.OneOf(["yes", "no", "no_phone_service"]),
        metadata={"enum": ["yes", "no", "no_phone_service"]},
    )

    internetservice = fields.Str(
        required=True,
        validate=validate.OneOf(["dsl", "fiber_optic", "no"]),
        metadata={"enum": ["dsl", "fiber_optic", "no"]},
    )

    onlinesecurity = fields.Str(
        required=True,
        validate=validate.OneOf(["yes", "no", "no_internet_service"]),
        metadata={"enum": ["yes", "no", "no_internet_service"]},
    )

    onlinebackup = fields.Str(
        required=True,
        validate=validate.OneOf(["yes", "no", "no_internet_service"]),
        metadata={"enum": ["yes", "no", "no_internet_service"]},
    )

    deviceprotection = fields.Str(
        required=True,
        validate=validate.OneOf(["yes", "no", "no_internet_service"]),
        metadata={"enum": ["yes", "no", "no_internet_service"]},
    )

    techsupport = fields.Str(
        required=True,
        validate=validate.OneOf(["yes", "no", "no_internet_service"]),
        metadata={"enum": ["yes", "no", "no_internet_service"]},
    )

    streamingtv = fields.Str(
        required=True,
        validate=validate.OneOf(["yes", "no", "no_internet_service"]),
        metadata={"enum": ["yes", "no", "no_internet_service"]},
    )

    streamingmovies = fields.Str(
        required=True,
        validate=validate.OneOf(["yes", "no", "no_internet_service"]),
        metadata={"enum": ["yes", "no", "no_internet_service"]},
    )

    contract = fields.Str(
        required=True,
        validate=validate.OneOf(["month-to-month", "one_year", "two_year"]),
        metadata={"enum": ["month-to-month", "one_year", "two_year"]},
    )

    paperlessbilling = fields.Str(
        required=True,
        validate=validate.OneOf(["yes", "no"]),
        metadata={"enum": ["yes", "no"]},
    )

    paymentmethod = fields.Str(
        required=True,
        validate=validate.OneOf(
            [
                "bank_transfer",
                "credit_card",
                "electronic_check",
                "mailed_check",
            ]
        ),
        metadata={
            "enum": [
                "bank_transfer",
                "credit_card",
                "electronic_check",
                "mailed_check",
            ]
        },
    )

    tenure = fields.Int(
        required=True,
        validate=validate.Range(min=0),
        metadata={"minimum": 0},
    )

    monthlycharges = fields.Float(
        required=True,
        validate=validate.Range(min=0),
        metadata={"minimum": 0},
    )

    totalcharges = fields.Float(
        required=True,
        validate=validate.Range(min=0),
        metadata={"minimum": 0},
    )


class ChurnResponseSchema(Schema):
    churn_probability = fields.Float()
    churn = fields.Bool()


# %% [markdown]
# Blueprint + endpoint

# %%

blp = Blueprint(
    "churn",
    "churn",
    url_prefix="/predict",
    description="Customer churn prediction",
)


@blp.route("/")
class ChurnPrediction(MethodView):

    @blp.arguments(
        ChurnRequestSchema,
        example={
            "gender": "female",
            "seniorcitizen": 0,
            "partner": "yes",
            "dependents": "no",
            "phoneservice": "no",
            "multiplelines": "no_phone_service",
            "internetservice": "dsl",
            "onlinesecurity": "no",
            "onlinebackup": "yes",
            "deviceprotection": "no",
            "techsupport": "no",
            "streamingtv": "no",
            "streamingmovies": "no",
            "contract": "month-to-month",
            "paperlessbilling": "yes",
            "paymentmethod": "electronic_check",
            "tenure": 1,
            "monthlycharges": 29.85,
            "totalcharges": 29.85,
        },
    )
    @blp.response(200, ChurnResponseSchema)
    def post(self, customer):
        """
        Predict customer churn
        """

        X = dict_vectorizer.transform([customer])
        y_pred = model.predict_proba(X)[0, 1]
        churn = y_pred >= 0.5

        return {
            "churn_probability": float(y_pred),
            "churn": bool(churn),
        }


api.register_blueprint(blp)

# %% [markdown]
# Run app

# %%

if __name__ == "__main__":
    app.run(debug=True)

# %% [markdown]
# Run app command
#
# ```sh
# uv run app.py
# ```
