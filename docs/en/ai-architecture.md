# Architecture

## High-level runtime split

Masterbrain separates UI concerns, backend coordination, and model execution:

```mermaid
sequenceDiagram
    participant User
    participant Frontend as Frontend UI
    participant Backend as FastAPI backend
    participant LLM as Model runtime
    participant Tool as Tooling / services

    User->>Frontend: Ask, edit, upload, select files
    Frontend->>Backend: Send API request
    Backend->>LLM: Run model-facing logic
    alt Model answers directly
        LLM->>Backend: Stream or return result
    else Model needs a tool
        LLM->>Tool: Invoke tool or helper flow
        Tool->>LLM: Return structured result
        LLM->>Backend: Produce final answer
    end
    Backend->>Frontend: Return response
    Frontend->>User: Render result
```

The backend exists as a coordination layer, not just a proxy. It owns API contracts, environment-specific behavior, key handling, workspace access, and packaging logic.

## Backend responsibilities

`apps/api/src/masterbrain/fastapi/main.py` wires together the application:

- registers all endpoint routers under `/api/endpoints`
- maps model-related exceptions to stable HTTP responses
- resolves the built frontend from `apps/web/dist` when available
- serves the integrated local app in desktop mode

This allows the same backend to support:

- source development
- local integrated app mode
- packaged desktop-style distribution

## Frontend and workspace model

The frontend is a Vue 3 application in `apps/web`. In development it runs through Vite; in integrated mode it is served by FastAPI after a production build.

The key design choice is that the active project is a real directory, not an abstract blob:

- workspace routes perform deterministic file and folder operations
- code-edit routes run AI-assisted edits on top of the current workspace snapshot
- ZIP import and export are handled by the backend against the selected directory

This keeps the model-facing side stateless enough to reason about, while the backend still owns the file-system boundary.

## Endpoint-oriented AI design

Masterbrain organizes AI capabilities around endpoints instead of around one monolithic assistant abstraction.

That means:

- each feature exposes a dedicated request and response schema
- routing stays explicit
- backend and frontend teams can integrate against stable contracts
- a feature can change models internally without changing its public API

The detailed structure is covered in [Code Structure](/en/code-structure) and [Endpoint Overview](/en/endpoints/).
