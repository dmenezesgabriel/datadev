import pickle
from typing import Any, Dict

with open("model_C=10.bin", "rb") as f_in:
    loaded_dict_vectorizer, loaded_model = pickle.load(f_in)


def predict_single(customer: Any) -> Any:
    X = loaded_dict_vectorizer.transform([customer])
    result = loaded_model.predict_proba(X)[0, 1]
    return float(result)


def lambda_handler(event: Any, context: Any) -> Dict[str, Any]:
    print("Parameters: ", event)
    customer = event["customer"]
    churn_probability = predict_single(customer)

    return {
        "churn_probability": churn_probability,
        "churn": bool(churn_probability >= 0.5),
    }
