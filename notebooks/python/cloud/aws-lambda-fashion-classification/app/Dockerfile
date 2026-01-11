FROM public.ecr.aws/lambda/python:3.11

ENV UV_PYTHON=/var/lang/bin/python3.11

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin
COPY pyproject.toml uv.lock ./

RUN uv export --format requirements-txt > requirements.txt \
 && uv pip install --system -r requirements.txt \
 && rm requirements.txt

COPY clothing-classification.onnx .
COPY lambda_function.py .

CMD ["lambda_function.lambda_handler"]

