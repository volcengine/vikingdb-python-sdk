# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Any, Mapping, Optional, Type, Union

from pydantic import BaseModel

from ..exceptions import VikingDBError
from ..request_options import RequestOptions
from ..transport import Transport


class VectorClientBase:
    """Shared helper for all Vector clients."""

    def __init__(self, transport: Transport) -> None:
        self._transport = transport

    def _post(
        self,
        path: str,
        payload: Mapping[str, Any],
        response_model: Type[BaseModel],
        *,
        request_options: Optional[RequestOptions] = None,
    ) -> BaseModel:
        response_payload = self._transport.request(
            "POST",
            path,
            json_body=payload,
            options=request_options,
        )
        return response_model.model_validate(response_payload)

    @staticmethod
    def _merge_payload(
        base: Mapping[str, Any],
        request: Union[BaseModel, Mapping[str, Any], None],
    ) -> Mapping[str, Any]:
        if isinstance(request, BaseModel):
            body = request.model_dump(by_alias=True, exclude_none=True)
        elif request is None:
            body = {}
        elif isinstance(request, Mapping):
            body = {key: value for key, value in request.items() if value is not None}
        else:
            raise VikingDBError(f"unsupported request type: {type(request)!r}")

        merged = dict(base)
        merged.update(body)
        return merged
