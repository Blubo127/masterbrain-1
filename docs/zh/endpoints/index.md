# Endpoint 总览

FastAPI 应用统一将公共路由挂载在：

```txt
/api/endpoints
```

## Chat 与编辑

| 路由 | 作用 |
| --- | --- |
| `POST /chat/qa/language` | 流式文本对话 |
| `POST /chat/qa/vision` | 图像识别与理解 |
| `POST /chat/qa/stt` | 语音转文本 |
| `POST /chat/field_input` | 结构化字段提取与槽位填充 |
| `POST /code_edit` | 基于 OpenCode 的代码编辑 |
| `GET /workspace` | 获取当前工作区快照 |
| `POST /workspace/open` | 打开指定目录作为工作区 |
| `POST /workspace/select` | 在支持的平台上拉起原生目录选择器 |
| `PUT /workspace/file` | 更新已有文件 |
| `POST /workspace/file` | 创建文件 |
| `DELETE /workspace/file` | 删除文件 |
| `POST /workspace/rename` | 重命名文件 |
| `POST /workspace/folder` | 创建目录 |
| `POST /workspace/import-zip` | 将 ZIP 导入工作区 |
| `GET /workspace/export-zip` | 将工作区导出为 ZIP |

## Protocol 生成与校验

| 路由 | 作用 |
| --- | --- |
| `POST /protocol_generation/aimd` | 生成 protocol AIMD 文本 |
| `POST /protocol_generation/model` | 生成 protocol model 代码 |
| `POST /protocol_generation/assigner` | 生成 protocol assigner 内容 |
| `POST /single_protocol_file_generation` | 生成单文件 protocol |
| `POST /protocol_check` | 检查并改进 protocol |
| `POST /protocol_debug` | 调试 protocol 相关流程 |

## 科研自动化与论文生成

| 路由 | 作用 |
| --- | --- |
| `POST /aira` | 执行 AIRA 工作流中的一个步骤 |
| `POST /paper_generation` | 基于 protocol markdown 生成论文 markdown |

## 设计原则

在 Masterbrain 中，endpoint 是产品能力的基本组织单元。每个 route family 都应当拥有：

- 独立的数据契约
- 独立的模型约束
- 独立的业务逻辑
- 独立的测试

这样比“只有一个万能 chat endpoint，所有能力都藏在 prompt 里”的方案更容易演进，也更容易定位问题。
