# Masterbrain API

Python backend for the Masterbrain monorepo. This app owns the FastAPI service, the desktop launcher, backend tests, and the PyInstaller packaging flow.

## Setup

```shell
cp .env.example .env
uv sync --dev
```

If you prefer to keep a repo-root `.env`, the backend still loads it as a fallback, but `apps/api/.env` is now the standard location.

## Run

Start the FastAPI server:

```shell
uv run uvicorn masterbrain.fastapi.main:app --reload --host 127.0.0.1 --port 8080
```

Launch the integrated desktop-style local app after building the frontend in `apps/web`:

```shell
uv run masterbrain-desktop
```

You can bind the app to an existing workspace directory:

```shell
uv run masterbrain-desktop --workspace /path/to/project
```

## OpenCode

Code-edit flows require an OpenCode runtime. Either install `opencode` globally, or vendor it locally:

```shell
python3 scripts/vendor_opencode.py
```

## Tests

Run the backend test suite:

```shell
uv run pytest
```

`pytest.ini` excludes `openai` and `qwen` markers by default.

## Packaging

Build the packaged local bundle:

```shell
./scripts/build_desktop_bundle.sh
```

This builds the frontend from `apps/web`, vendors OpenCode into `apps/api/vendor/`, and writes the PyInstaller bundle to `apps/api/dist/Masterbrain/`.
