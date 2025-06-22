FROM mambaorg/micromamba:1.5.8

ENV MAMBA_ROOT_PREFIX=/opt/conda \
    ENV_NAME=build-env

WORKDIR /app

COPY build-environment.yml environment.yml ./
COPY README.md ./
COPY content ./content
COPY config ./config

# Create build environment and install dependencies
RUN micromamba create -y -n $ENV_NAME -f build-environment.yml \
    && micromamba clean -a -y

# Build JupyterLite site
RUN micromamba run -n $ENV_NAME jupyter lite build --contents content --output-dir dist

EXPOSE 8000

CMD ["micromamba", "run", "-n", "build-env", "python", "-m", "http.server", "8000", "--directory", "dist"]