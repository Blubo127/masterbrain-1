# Record QA 模式

Record QA 指的是对话系统需要围绕结构化科研对象进行问答，例如 protocol、record 或 discussion。

## 设计目标

这个场景的难点在于：上下文不是一开始就固定好的，而是可能在对话中途被用户逐步加入。

例如：

- 用户先问一个普通问题
- 之后选中一个或多个 protocol
- 再基于这些 protocol 继续追问
- 中途再补充 record 或 discussion
- 同一条会话继续向前推进

目标是支持这种动态注入上下文的过程，而不是把所有东西粗暴拼成一段不可追踪的大 prompt。

## 通过工具调用注入上下文

推荐方式是把结构化上下文注入建模为显式工具调用。

概念上常见的工具包括：

- `inject_airalogy_protocols`
- `inject_airalogy_records`
- `inject_airalogy_discussions`

其中：

- `arguments` 用来说明要注入什么，通常是若干 ID
- `content` 用来把解析后的结构化数据放回对话历史

这样做的好处是上下文来源可审计、可解释，也更方便前端展示。

## 为什么不直接把原文拼进 prompt

用工具调用而不是静默拼接文本，有几个很实际的收益：

- 前端可以清楚显示“何时注入了哪些上下文”
- 后端可以在注入前做权限校验
- 模型能明确区分用户问题与外部结构化对象
- 后续调试时能看清上下文来自哪里

## 典型对话形态

```json
{
  "context": {
    "inject_airalogy_protocols": {
      "enabled": true,
      "airalogy_protocol_ids": ["airalogy.id.lab.example.protocol.v.0.0.1"]
    }
  },
  "main_messages": [
    { "role": "user", "content": "请解释这个 protocol。" },
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
      "content": "这个 protocol 主要定义了……"
    }
  ]
}
```

## 与当前仓库的关系

本页描述的是 Masterbrain 相关问答流程的一种设计模式。并不是每一个注入工具都已经作为公开 endpoint 暴露在当前仓库里，但如果后续要把结构化上下文动态接入对话，这仍然是更稳健的建模方式。
