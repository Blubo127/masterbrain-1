# Airalogy Masterbrain

English: [README.md](README.md)

Masterbrain 现在采用轻量 monorepo 结构：

```txt
masterbrain/
├── apps/
│   ├── api/   # FastAPI 后端、桌面启动器、打包脚本、Python 测试
│   └── web/   # Vue 3 + TypeScript 前端
├── docs/
└── README.zh-CN.md
```

## 快速开始

先构建一次前端：

```shell
cd apps/web
npm install
npm run build
```

再初始化后端并启动一体化本地应用：

```shell
cd ../api
cp .env.example .env
uv sync
uv run masterbrain-desktop
```

这会启动一个本地进程，同时提供后端 API 和已构建的 Web UI，并自动在默认浏览器中打开 Masterbrain。

如果你要直接绑定某个工作目录启动：

```shell
uv run masterbrain-desktop --workspace /path/to/project
```

源代码运行模式下，对话改代码功能仍然需要 OpenCode runtime。你可以把 `opencode` 放到系统 `PATH`，或者执行：

```shell
python3 scripts/vendor_opencode.py
```

如果你之前已经在仓库根目录维护了旧的 `.env`，后端仍会兼容加载；新的推荐位置是 `apps/api/.env`。

## 开发模式

在 `apps/api` 中启动后端：

```shell
cd apps/api
uv sync --dev
uv run uvicorn masterbrain.fastapi.main:app --reload --host 127.0.0.1 --port 8080
```

在 `apps/web` 中启动前端：

```shell
cd apps/web
npm install
npm run dev
```

Vite 开发服务器默认运行在 `http://localhost:5173`，并将 `/api/*` 代理到 `http://127.0.0.1:8080`。

## 打包

在 `apps/api` 中构建本地桌面包：

```shell
cd apps/api
./scripts/build_desktop_bundle.sh
```

PyInstaller 输出目录为 `apps/api/dist/Masterbrain/`。

## 测试

在 `apps/api` 中运行后端测试：

```shell
cd apps/api
uv run pytest
```

`apps/api/pytest.ini` 默认会跳过依赖外部 API 的测试标记。

## 应用文档

- 后端：[apps/api/README.md](apps/api/README.md)
- 前端：[apps/web/SETUP.md](apps/web/SETUP.md)

## 引用

如果 Airalogy Masterbrain 对你的研究或项目有帮助，欢迎引用以下论文：

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
