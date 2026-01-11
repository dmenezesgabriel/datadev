from typing import Any, Dict

import onnxruntime as ort
from keras_image_helper import create_preprocessor

# Define code outside lambda_handler so it is executed only once
onnx_model_path = "clothing-classification.onnx"
session = ort.InferenceSession(
    onnx_model_path, providers=["CPUExecutionProvider"]
)

inputs = session.get_inputs()
outputs = session.get_outputs()

input_name = inputs[0].name
output_name = outputs[0].name

preprocessor = create_preprocessor("xception", target_size=(299, 299))

classes = [
    "dress",
    "hat",
    "longsleeve",
    "outwear",
    "pants",
    "shirt",
    "shoes",
    "shorts",
    "skirt",
    "t-shirt",
]


def lambda_handler(event: Any, context: Any) -> Dict[str, Any]:
    url = event["url"]
    X = preprocessor.from_url(url)
    session_run = session.run([output_name], {input_name: X})
    predictions_list = session_run[0][0].tolist()
    result = dict(zip(classes, predictions_list))

    return result
