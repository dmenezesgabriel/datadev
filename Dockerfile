# ============================
#          BUILDER
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
        curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv using pip (more reliable in Docker)
RUN pip install --no-cache-dir uv

WORKDIR /app

COPY pyproject.toml .
COPY scripts ./scripts
COPY packages ./packages

# Install project dependencies and dev dependencies
RUN mkdir -p /opt/python && \
    uv pip install --no-cache-dir --prefix=/opt/python --group dev .


# ============================
#           RUNTIME
# ============================
FROM python:3.11-slim AS runtime

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libcairo2 \
        libpango-1.0-0 \
        libpangocairo-1.0-0 \
        ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install uv using pip
RUN pip install --no-cache-dir uv

# Pre-install Python versions for uv kernels
RUN uv python install 3.11 3.12 3.13

WORKDIR /app

# Copy installed Python packages from builder
COPY --from=builder /opt/python /opt/python

# Set PATH and PYTHONPATH to use installed packages
ENV PATH="/opt/python/bin:/usr/local/bin:${PATH}"
ENV PYTHONPATH="/opt/python/lib/python3.11/site-packages:${PYTHONPATH}"

# Copy the entire application
COPY . .

# Setup kernels - unset PYTHONPATH to avoid conflicts
RUN env -u PYTHONPATH python scripts/setup_uv_kernel.py

EXPOSE 8888

# Change working directory for notebooks to avoid sys.path issues
WORKDIR /workspace

CMD ["jupyter-lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--notebook-dir=/app"]