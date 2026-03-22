# Quick Start

## Prerequisites

- Node.js `>= 18`
- npm `>= 9`
- Python `>= 3.13`
- `uv`
- OpenCode CLI for source and development mode code editing

## Run the integrated local app

Build the frontend once:

```sh
cd apps/web
npm install
npm run build
```

Then start the backend in desktop mode:

```sh
cd ../api
cp .env.example .env
uv sync
uv run masterbrain-desktop
```

This starts one local process that serves the FastAPI backend and the built web UI, then opens Masterbrain in your default browser.

If you want to open a specific directory immediately:

```sh
uv run masterbrain-desktop --workspace /path/to/project
```

## Development mode

Backend:

```sh
cd apps/api
uv sync --dev
uv run uvicorn masterbrain.fastapi.main:app --reload --host 127.0.0.1 --port 8080
```

Frontend:

```sh
cd apps/web
npm install
npm run dev
```

The Vite dev server runs at `http://localhost:5173` and proxies `/api/*` to `http://127.0.0.1:8080`.

## Environment variables

Create `apps/api/.env` when needed:

```ini
OPENAI_API_KEY=sk-...
DASHSCOPE_API_KEY=sk-...
TAVILY_API_KEY=tvly-...
```

Notes:

- `DASHSCOPE_API_KEY` is required for the default Qwen-based code-edit runtime.
- `OPENAI_API_KEY` is required for OpenAI-backed endpoints and future GPT-based code-edit flows.

## Tests

Run backend tests from `apps/api`:

```sh
uv run pytest
```

`apps/api/pytest.ini` skips API-backed markers by default.
