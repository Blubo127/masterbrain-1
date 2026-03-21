# Airalogy Masterbrain

English: [README.md](README.md)

[安装与设置](#安装与设置) • [功能模块](#功能模块) • [API 文档](#api-文档)

## 安装与设置

Airalogy Masterbrain API 使用 FastAPI 进行本地部署。调用 API 之前，需要先启动 FastAPI 服务。

### 1. 安装 `uv`

开始前，请先在本地安装 `uv`。

### 2. 使用 `uv` 同步依赖

```shell
# 生产环境
uv sync

# 开发环境（包含 pytest 等）
uv sync --dev
```

### 3. 设置环境变量

将 `.env.example` 复制为 `.env`，并按说明完成配置。

```shell
cp .env.example .env
```

### 4. 启动 FastAPI 服务

```shell
# 生产环境
uv run uvicorn masterbrain.fastapi.main:app --host 127.0.0.1 --port 8080

# 开发环境
uv run uvicorn masterbrain.fastapi.main:app --reload --host 127.0.0.1 --port 8080
```

端口可以根据实际需要调整。

### 5. 启动 Web 前端

如果需要使用交互式 Web 界面，请在 FastAPI 服务启动后再启动前端。

要求：

- Node.js >= 18
- npm >= 9

```shell
cd src/web

# 安装前端依赖
npm install

# 启动 Vite 开发服务器
npm run dev
```

默认前端地址：

- `http://localhost:5173`

开发模式下，Vite 会将 `/api/*` 请求代理到 `http://127.0.0.1:8080`。

### 6. 构建 Web 前端

```shell
cd src/web
npm run build
```

构建输出目录：

- `src/web/dist/`

## 功能模块

Masterbrain API 提供以下主要功能模块：

### 聊天功能

- **标准聊天**：`/api/endpoints/chat/qa/language` - 提供基础聊天能力
- **视觉功能**：`/api/endpoints/chat/qa/vision` - 支持图像处理与分析
- **语音转文字**：`/api/endpoints/chat/qa/stt` - 支持语音输入转文字
- **字段输入**：`/api/endpoints/chat/field_input` - 提供结构化字段输入处理

### 协议生成

- **AIMD 协议**：`/api/endpoints/protocol_generation/aimd` - AI 模型驱动的协议生成
- **模型协议**：`/api/endpoints/protocol_generation/model` - 模型相关协议生成
- **分配器协议**：`/api/endpoints/protocol_generation/assigner` - 任务分配协议生成
- **单文件生成**：`/api/endpoints/single_protocol_file_generation` - 单协议文件生成

### 协议检查与调试

- **协议检查**：`/api/endpoints/protocol_check` - 校验协议有效性
- **协议调试**：`/api/endpoints/protocol_debug` - 提供协议调试工具

### AIRA 工作流

- **AIRA**：`/api/endpoints/aira` - AIRA 集成工作流

### 论文生成

- **论文生成**：`/api/endpoints/paper_generation` - 论文生成

## API 文档

服务启动后，可以通过以下地址访问 API 文档：

- 默认地址：`http://127.0.0.1:8080/docs`
- 如果修改了 Host 或 Port，请访问对应地址

## 预览

打开 API 文档页面后，可以看到如下界面：

![API 预览界面](docs/images/preview.png)

## 引用

如果您在研究或项目中使用了 Airalogy Masterbrain，或本项目对您的工作有帮助，欢迎引用以下文献：

```bibtex
@misc{yang2025airalogyaiempowereduniversaldata,
      title={Airalogy: AI-empowered universal data digitization for research automation}, 
      author={Zijie Yang and Qiji Zhou and Fang Guo and Sijie Zhang and Yexun Xi and Jinglei Nie and Yudian Zhu and Liping Huang and Chou Wu and Yonghe Xia and Xiaoyu Ma and Yingming Pu and Panzhong Lu and Junshu Pan and Mingtao Chen and Tiannan Guo and Yanmei Dou and Hongyu Chen and Anping Zeng and Jiaxing Huang and Tian Xu and Yue Zhang},
      year={2025},
      eprint={2506.18586},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2506.18586}, 
}
```
