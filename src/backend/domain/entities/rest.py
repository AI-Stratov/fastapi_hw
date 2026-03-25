from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict


class ResponseState(StrEnum):
    success = "success"
    error = "error"


class BaseResponse(BaseModel):
    state: Literal[ResponseState.success, ResponseState.error]
    error_text: str | None = None

    model_config = ConfigDict(use_enum_values=True)


class ResultResponse[T](BaseResponse):
    result: T | None = None


class ErrorSchema(BaseModel):
    detail: str
