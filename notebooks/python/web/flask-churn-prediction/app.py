# ---
# jupyter:
#   language_info:
#     name: python
# ---

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
    loaded_dict_vectorizer, loaded_model = pickle.load(f_in)

# %% [markdown]
# Marshmallow schemas


# %%
class ChurnRequestSchema(Schema):
    gender = fields.Str(
        required=True,
        metadata={"enum": ["male", "female"]},
        validate=validate.OneOf(["male", "female"]),
    )
    seniorcitizen = fields.Int(required=True)
    partner = fields.Str(required=True)
    dependents = fields.Str(required=True)

    phoneservice = fields.Str(required=True)
    multiplelines = fields.Str(required=True)
    internetservice = fields.Str(required=True)

    onlinesecurity = fields.Str(required=True)
    onlinebackup = fields.Str(required=True)
    deviceprotection = fields.Str(required=True)
    techsupport = fields.Str(required=True)

    streamingtv = fields.Str(required=True)
    streamingmovies = fields.Str(required=True)

    contract = fields.Str(required=True)
    paperlessbilling = fields.Str(required=True)
    paymentmethod = fields.Str(required=True)

    tenure = fields.Int(required=True)
    monthlycharges = fields.Float(required=True)
    totalcharges = fields.Float(required=True)


class ChurnResponseSchema(Schema):
    churn_probability = fields.Float()
    churn = fields.Bool()


class RequestErrorSchema(Schema):
    error = fields.Str()
    message = fields.Str()
    details = fields.Dict()


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
            "paymentmethod": "eletronic_check",
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

        X = loaded_dict_vectorizer.transform([customer])
        prob = loaded_model.predict_proba(X)[0, 1]

        return {
            "churn_probability": float(prob),
            "churn": bool(prob >= 0.5),
        }


api.register_blueprint(blp)

# %% [markdown]
# Run app

# %%

if __name__ == "__main__":
    app.run(debug=True)
