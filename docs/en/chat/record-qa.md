# Record QA Pattern

Record QA is the pattern where the chat experience needs to answer questions against structured research artifacts such as protocols, records, or discussion threads.

## Design goal

The challenge is that the user may add context in the middle of a conversation:

- start with a plain question
- later inject one or more protocols
- ask follow-up questions about those protocols
- inject records or discussions
- continue the same thread without losing context

The goal is to support that without flattening everything into an opaque prompt.

## Tool-based injection

The preferred pattern is to inject structured context through explicit tool calls.

Conceptual examples:

- `inject_airalogy_protocols`
- `inject_airalogy_records`
- `inject_airalogy_discussions`

Each tool call does two things:

- `arguments` identifies what should be injected, typically by ID
- `content` carries the resolved structured payload back into the conversation

That makes the injection auditable and reversible.

## Why not just append raw text

Using tool calls instead of silently rewriting the prompt gives better system behavior:

- the frontend can show when context was injected
- the backend can control permissions before exposing data
- the model sees explicit boundaries between user questions and injected artifacts
- later debugging is easier because the provenance of context is visible

## Typical conversation shape

```json
{
  "context": {
    "inject_airalogy_protocols": {
      "enabled": true,
      "airalogy_protocol_ids": ["airalogy.id.lab.example.protocol.v.0.0.1"]
    }
  },
  "main_messages": [
    { "role": "user", "content": "Explain this protocol." },
    {
      "role": "assistant",
      "content": "",
      "tool_calls": [
        {
          "id": "call_abc123",
          "type": "function",
          "function": {
            "name": "inject_airalogy_protocols",
            "arguments": "{\"airalogy_protocol_ids\":[\"airalogy.id.lab.example.protocol.v.0.0.1\"]}"
          }
        }
      ]
    },
    {
      "role": "tool",
      "tool_call_id": "call_abc123",
      "content": "{\"airalogy_protocols\":[...]}"
    },
    {
      "role": "assistant",
      "content": "This protocol defines ..."
    }
  ]
}
```

## Relationship to current repo

This page describes a design pattern used by Masterbrain-related chat flows. Not every injection tool is currently exposed as a public endpoint in this repository, but the pattern is still the right way to model structured context that enters a conversation after it has already started.
