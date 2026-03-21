"""Helpers for LLM provider selection, credential validation, and error mapping."""

from __future__ import annotations

from collections.abc import AsyncGenerator
from typing import Literal, get_args

from fastapi import HTTPException
from openai import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    AuthenticationError,
    BadRequestError,
    PermissionDeniedError,
    RateLimitError,
)

from masterbrain.configs import (
    AvailableOpenAIModel,
    AvailableQwenModel,
    DASHSCOPE_API_KEY,
    OPENAI_API_KEY,
)

ProviderName = Literal["openai", "qwen"]


def detect_model_provider(model_name: str) -> ProviderName:
    """Infer the upstream provider for a supported model name."""

    if model_name in get_args(AvailableOpenAIModel) or model_name.startswith(("gpt-", "o1-")):
        return "openai"
    if model_name in get_args(AvailableQwenModel) or model_name.startswith(
        ("qwen", "qwq", "qvq")
    ):
        return "qwen"
    raise ValueError(f"Unsupported model provider for model `{model_name}`")


def required_api_key_env(model_name: str) -> str:
    """Return the env var name required for the selected model provider."""

    provider = detect_model_provider(model_name)
    if provider == "openai":
        return "OPENAI_API_KEY"
    return "DASHSCOPE_API_KEY"


def missing_api_key_message(model_name: str) -> str | None:
    """Return a user-facing message when the selected provider key is missing."""

    provider = detect_model_provider(model_name)
    if provider == "openai" and not OPENAI_API_KEY.strip():
        return (
            f"OPENAI_API_KEY is not configured. Model `{model_name}` requires a valid OpenAI "
            "API key. Add it to your `.env` file and restart Masterbrain."
        )
    if provider == "qwen" and not DASHSCOPE_API_KEY.strip():
        return (
            f"DASHSCOPE_API_KEY is not configured. Model `{model_name}` requires a valid "
            "DashScope/Qwen API key. Add it to your `.env` file and restart Masterbrain."
        )
    return None


def ensure_model_api_key(model_name: str) -> None:
    """Raise a 400 HTTP error when the selected model provider key is missing."""

    message = missing_api_key_message(model_name)
    if message:
        raise HTTPException(status_code=400, detail=message)


def _extract_provider_error_message(exc: Exception) -> str | None:
    """Try to recover the provider's human-readable message from an SDK exception."""

    body = getattr(exc, "body", None)
    if isinstance(body, dict):
        error = body.get("error")
        if isinstance(error, dict):
            message = error.get("message")
            if isinstance(message, str) and message.strip():
                return message.strip()
        message = body.get("message")
        if isinstance(message, str) and message.strip():
            return message.strip()

    message = str(exc).strip()
    return message or None


def llm_http_exception(exc: Exception, model_name: str | None = None) -> HTTPException:
    """Map SDK/provider failures into user-facing HTTP errors."""

    provider_message = _extract_provider_error_message(exc)

    if isinstance(exc, AuthenticationError):
        if model_name:
            missing_message = missing_api_key_message(model_name)
            if missing_message:
                return HTTPException(status_code=400, detail=missing_message)

            env_name = required_api_key_env(model_name)
            detail = (
                f"{env_name} was rejected by the model provider for `{model_name}`. "
                "Check that the API key is correct, active, and belongs to the expected provider."
            )
            if provider_message:
                detail = f"{detail}\nProvider message: {provider_message}"
            return HTTPException(status_code=401, detail=detail)

        detail = "Model API authentication failed. Check that the corresponding API key is configured correctly."
        if provider_message:
            detail = f"{detail}\nProvider message: {provider_message}"
        return HTTPException(status_code=401, detail=detail)

    if isinstance(exc, PermissionDeniedError):
        detail = provider_message or "The model provider denied this request."
        return HTTPException(status_code=403, detail=detail)

    if isinstance(exc, RateLimitError):
        detail = provider_message or "The model provider rate limit was exceeded."
        return HTTPException(status_code=429, detail=detail)

    if isinstance(exc, APITimeoutError):
        detail = provider_message or "The model request timed out."
        return HTTPException(status_code=504, detail=detail)

    if isinstance(exc, APIConnectionError):
        detail = provider_message or "Masterbrain could not connect to the model provider."
        return HTTPException(status_code=502, detail=detail)

    if isinstance(exc, BadRequestError):
        detail = provider_message or "The model request was rejected as invalid."
        return HTTPException(status_code=400, detail=detail)

    if isinstance(exc, APIStatusError):
        status_code = exc.status_code if isinstance(exc.status_code, int) else 500
        detail = provider_message or "The model provider returned an unexpected error."
        return HTTPException(status_code=status_code, detail=detail)

    detail = provider_message or str(exc) or "Unexpected model runtime error."
    return HTTPException(status_code=500, detail=detail)


async def preflight_text_stream(
    stream: AsyncGenerator[str, None],
    *,
    model_name: str | None = None,
) -> AsyncGenerator[str, None]:
    """Pull the first chunk early so auth/config errors become normal HTTP responses."""

    try:
        first_chunk = await anext(stream)
    except StopAsyncIteration:
        async def empty_stream() -> AsyncGenerator[str, None]:
            if False:
                yield ""

        return empty_stream()
    except HTTPException:
        raise
    except Exception as exc:
        raise llm_http_exception(exc, model_name) from exc

    async def chained_stream() -> AsyncGenerator[str, None]:
        yield first_chunk
        async for chunk in stream:
            yield chunk

    return chained_stream()
