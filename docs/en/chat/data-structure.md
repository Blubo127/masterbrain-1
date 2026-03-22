# Chat Data Structure

Many chat-oriented flows in Masterbrain use OpenAI-style message histories as their foundation. This keeps the project compatible with the message format that has become the de facto standard for multimodal chat and tool calling.

## Message roles

A conversation history is a list of messages with a `role` and `content`.

Common roles:

- `system`: behavior or workflow instructions
- `user`: human input
- `assistant`: model output
- `tool`: structured tool result returned to the model

## Basic examples

Simple text exchange:

```json
[
  { "role": "user", "content": "Who are you?" },
  { "role": "assistant", "content": "I am Airalogy Masterbrain." }
]
```

Multimodal user input:

```json
[
  {
    "role": "user",
    "content": [
      { "type": "text", "text": "What is in this image?" },
      { "type": "image_url", "image_url": "https://example.com/image.png" }
    ]
  }
]
```

## Tool-calling pattern

When a workflow needs a tool, the assistant emits a tool call, the tool responds, and the assistant uses that result to continue the conversation.

```json
[
  { "role": "user", "content": "Why are there nonspecific PCR bands?" },
  {
    "role": "assistant",
    "content": "",
    "tool_calls": [
      {
        "id": "call_abc123",
        "type": "function",
        "function": {
          "name": "airalogy_search",
          "arguments": "{\"keywords\":[\"PCR\",\"nonspecific bands\"]}"
        }
      }
    ]
  },
  {
    "role": "tool",
    "tool_call_id": "call_abc123",
    "content": "{\"search_result\":\"Possible contamination or primer dimer formation.\"}"
  },
  {
    "role": "assistant",
    "content": "Possible causes include contamination or primer dimer formation."
  }
]
```

For a single tool, this is often described as the `UATA` pattern:

- User message
- Assistant tool-call message
- Tool message
- Assistant final message

## Why the tool result is isolated

This structure keeps the main conversation history compact. A tool can perform complex internal work, but the parent conversation only needs the tool invocation and the returned result.

That separation matters because it lets you:

- optimize the tool without rewriting the main chat format
- log internal tool behavior independently
- keep frontend rendering simple
- preserve a stable audit trail of user-visible reasoning steps

## Metadata wrapper

Some project documents refer to a full chat document that wraps message history with metadata such as:

- `chat_id`
- `user_id`
- timestamps
- chosen model
- workflow context
- human feedback

The current repository does not force every endpoint into one single shared payload type, but the design idea remains useful: keep message history portable, and keep surrounding metadata explicit.
