# Yaste

A simple Pastebin-like utility.

The app consists of:

* A Python Fast-API backend
* A Vue.js optional frontend

## Backend

Configure the backend via the `config.toml` (or `yaml`) file. See the `config.toml.example`.

Install and run with `uv`:

```bash
YASTE_CONFIG=./config.toml uv run yaste
```

### Push a file

With the development url:

```bash
curl -X POST http://localhost:8001/create --data-binary '@your_file'
```

## Frontend

Build the frontend with `bun`:

```bash
bun --cwd=frontend install
bun --cwd=frontend run build
```

And reference the path of the `dist` directory in the `config.toml`:

```toml
[frontend]
path = "./frontend/dist"
```

### Development

If you want to run the development server, you can give the python API server url:

```bash
VITE_API_SERVER=http://localhost:8001 bun --cwd=frontend run dev
```
