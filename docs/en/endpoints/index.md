# Endpoint Overview

The FastAPI app mounts its public routes under the shared prefix:

```txt
/api/endpoints
```

## Chat and editing

| Route | Purpose |
| --- | --- |
| `POST /chat/qa/language` | Streaming text chat |
| `POST /chat/qa/vision` | Image recognition and interpretation |
| `POST /chat/qa/stt` | Speech-to-text conversion |
| `POST /chat/field_input` | Structured field extraction and slot filling |
| `POST /code_edit` | OpenCode-backed code editing |
| `GET /workspace` | Read current workspace snapshot |
| `POST /workspace/open` | Open a directory path as workspace |
| `POST /workspace/select` | Open a native directory picker when supported |
| `PUT /workspace/file` | Update an existing file |
| `POST /workspace/file` | Create a file |
| `DELETE /workspace/file` | Delete a file |
| `POST /workspace/rename` | Rename a file |
| `POST /workspace/folder` | Create a folder |
| `POST /workspace/import-zip` | Import a ZIP archive into the workspace |
| `GET /workspace/export-zip` | Export the workspace as ZIP |

## Protocol authoring and validation

| Route | Purpose |
| --- | --- |
| `POST /protocol_generation/aimd` | Generate protocol AIMD text |
| `POST /protocol_generation/model` | Generate protocol model code |
| `POST /protocol_generation/assigner` | Generate protocol assigner content |
| `POST /single_protocol_file_generation` | Generate a single protocol file |
| `POST /protocol_check` | Check and improve a protocol |
| `POST /protocol_debug` | Debug a protocol-oriented workflow |

## Research automation and paper generation

| Route | Purpose |
| --- | --- |
| `POST /aira` | Execute one step of the AIRA workflow |
| `POST /paper_generation` | Generate paper markdown from protocol markdown inputs |

## Design principle

Masterbrain uses endpoints as the unit of product capability. Each route family owns:

- its own data contract
- its own model constraints
- its own logic implementation
- its own tests

That makes the backend easier to evolve than a single generic chat endpoint that tries to hide every capability behind prompt engineering alone.
