# Lite Notebooks

## Usage

### Local

Requirements:

- Docker

- **Build**:

```sh
docker build -t jupyterlite-local .
```

- **Run**:

```sh
docker run -p 8000:8000 jupyterlite-local
```

- **Inspect**:

```sh
docker run --rm -it jupyterlite-local /bin/bash
```
