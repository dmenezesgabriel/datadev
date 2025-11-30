# ============================
#       BUILDER STAGE
# ============================
FROM python:3.11-slim AS builder

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

RUN mkdir -p /opt/python && \
    uv pip install --no-cache-dir --prefix=/opt/python . --group dev

RUN uv run scripts/setup_uv_kernel.py

COPY . .

# ============================
#       RUNTIME STAGE
# ============================
FROM python:3.11-slim AS runtime

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libcairo2 \
        libpango-1.0-0 \
        libpangocairo-1.0-0 \
        ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /opt/python /usr/local

COPY . .

ENV PATH="/usr/local/bin:${PATH}"

EXPOSE 8888

CMD ["jupyter-lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
