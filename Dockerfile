# ============================
#          BUILDER
# ============================
FROM python:3.11-slim AS builder

ENV PATH="/opt/python/bin:${PATH}"

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        python3-dev \
        pkg-config \
        libcairo2-dev \
        libpango1.0-dev \
        ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv

WORKDIR /app

COPY pyproject.toml .
COPY scripts ./scripts
COPY packages ./packages

# Install project base dependencies
RUN mkdir -p /opt/python && \
    uv pip install --no-cache-dir --prefix=/opt/python .

# Install dev dependency group
RUN uv pip install --no-cache-dir --prefix=/opt/python $(uv pip list --project --group dev --format=freeze) && \
    uv pip install --no-cache-dir --prefix=/opt/python ipykernel

RUN uv run scripts/setup_uv_kernel.py

COPY . .

RUN mkdir -p /opt/kernels && \
    cp -r /root/.local/share/jupyter/kernels/* /opt/kernels/


# ============================
#           RUNTIME
# ============================
FROM python:3.11-slim AS runtime

ENV PATH="/opt/python/bin:/usr/local/bin:${PATH}"

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libcairo2 \
        libpango-1.0-0 \
        libpangocairo-1.0-0 \
        ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /opt/python /opt/python

COPY --from=builder /opt/kernels /root/.local/share/jupyter/kernels

COPY . .

EXPOSE 8888

CMD ["jupyter-lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
