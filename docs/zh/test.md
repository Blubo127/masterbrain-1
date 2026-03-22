# Test for `masterbrain`

当前仓库采用 monorepo 结构，后端测试代码位于 `apps/api/tests/`。

在 `apps/api/` 目录下使用 `pytest` 进行测试：

```shell
cd apps/api
uv run pytest
```

测试中分为2种类型：

1. 可以直接运行的测试
2. 需要调用API的测试（例如需要调用`openai`API相关的测试）。此类型的测试往往：1. 依赖于网络环境；2. 运行需要应用第三方API，因而需要支付费用；因此，不适合在每次测试时都运行。

对于后者，此类型的测试在编写的时候需要打上标签，如 `@pytest.mark.openai` 或 `@pytest.mark.qwen`。

例如：

```python
import pytest

@pytest.mark.openai
def test_openai():
    pass
```

默认情况下，由于 `apps/api/pytest.ini` 中设置了：

```ini
addopts = -m "not openai and not qwen"
```

以下命令不会运行如下类型的测试：

- `openai`
- `qwen`

```shell
pytest
```

如果想要运行上述类型的测试，可以使用 `-m` 参数。

```shell
pytest -m "openai"

# or
pytest -m "qwen"
```

**！！！注意！！！：运行 `openai` 类型的测试时，请确保 OpenAI 服务可用并符合使用和法律规范。**
