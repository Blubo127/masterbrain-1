# 对话数据结构

Masterbrain 中不少对话相关流程都建立在 OpenAI 风格的消息历史之上。这种格式已经成为多模态对话和工具调用的事实标准，因此也适合作为 Masterbrain 的基础消息模型。

## Message 角色

一段对话历史本质上是一个消息数组，每条消息至少包含 `role` 和 `content`。

常见角色包括：

- `system`：系统行为或工作流说明
- `user`：用户输入
- `assistant`：模型输出
- `tool`：工具返回结果

## 基础示例

普通文本对话：

```json
[
  { "role": "user", "content": "你是谁？" },
  { "role": "assistant", "content": "我是 Airalogy Masterbrain。" }
]
```

多模态输入：

```json
[
  {
    "role": "user",
    "content": [
      { "type": "text", "text": "这张图里是什么？" },
      { "type": "image_url", "image_url": "https://example.com/image.png" }
    ]
  }
]
```

## 工具调用模式

当对话需要工具时，assistant 会先发出工具调用，tool 再返回结构化结果，最后 assistant 基于该结果继续回答。

```json
[
  { "role": "user", "content": "PCR 出现杂带通常是什么原因？" },
  {
    "role": "assistant",
    "content": "",
    "tool_calls": [
      {
        "id": "call_abc123",
        "type": "function",
        "function": {
          "name": "airalogy_search",
          "arguments": "{\"keywords\":[\"PCR\",\"杂带\"]}"
        }
      }
    ]
  },
  {
    "role": "tool",
    "tool_call_id": "call_abc123",
    "content": "{\"search_result\":\"可能原因包括污染或引物二聚体。\"}"
  },
  {
    "role": "assistant",
    "content": "常见原因包括污染或引物二聚体。"
  }
]
```

对于单一工具调用，这个流程常被称为 `UATA`：

- User Message
- Assistant Tool Call Message
- Tool Message
- Assistant Message

## 为什么要把工具结果单独放出来

这种结构的价值在于主对话历史保持简洁。工具内部可能有复杂的处理过程，但主线程只需要知道：

- 调用了哪个工具
- 工具返回了什么
- assistant 最终如何利用这个结果

这样做的好处包括：

- 工具内部实现可以独立优化
- 前端更容易展示工具调用过程
- 排查问题时可以快速判断问题出在模型还是工具
- 日志和审计边界更清晰

## 元数据封装

在一些设计文档中，消息历史还会被包在更完整的对话文档里，附带如下元数据：

- `chat_id`
- `user_id`
- 时间戳
- 选用模型
- workflow context
- human feedback

当前仓库并没有强制所有 endpoint 共用一个统一的 `ChatDoc` 类型，但这个设计思想仍然成立：消息历史应当可移植，外围元数据应当显式存在，而不是隐含在 prompt 中。
