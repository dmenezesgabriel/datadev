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

## References

- [posit quarto](https://www.youtube.com/watch?v=_VKxTPWDhA4&list=PL9HYL-VRX0oQZPzhJR022G_bV4vynT4Ol)
