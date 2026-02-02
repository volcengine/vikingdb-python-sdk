# coding:utf-8
# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence, Union

from pydantic import Field

from .base import DataApiResponse, Model

__all__ = [
    "ChatMessage",
    "ChatCompletionRequest",
    "ChatCompletionResult",
    "ChatCompletionResponse",
]


class ChatMessage(Model):
    role: str = Field(alias="role")
    content: Any = Field(alias="content")


class ChatCompletionRequest(Model):
    model: str = Field(alias="model")
    messages: Sequence[ChatMessage] = Field(alias="messages")
    model_version: Optional[str] = Field(default=None, alias="model_version")
    thinking: Optional[Any] = Field(default=None, alias="thinking")
    max_tokens: Optional[int] = Field(default=4096, alias="max_tokens")
    temperature: Optional[float] = Field(default=0.1, alias="temperature")
    return_token_usage: Optional[bool] = Field(default=False, alias="return_token_usage")
    api_key: Optional[str] = Field(default=None, alias="api_key")
    stream: Optional[bool] = Field(default=False, alias="stream")


class ChatCompletionResult(Model):
    reasoning_content: Optional[str] = Field(default=None, alias="reasoning_content")
    generated_answer: Optional[str] = Field(default=None, alias="generated_answer")
    usage: Optional[str] = Field(default=None, alias="usage")
    prompt: Optional[str] = Field(default=None, alias="prompt")
    model: Optional[str] = Field(default=None, alias="model")
    finish_reason: Optional[str] = Field(default=None, alias="finish_reason")
    total_tokens: Optional[Any] = Field(default=None, alias="total_tokens")


class ChatCompletionResponse(DataApiResponse):
    result: Optional[ChatCompletionResult] = None
