from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.schema import COUNTERPARTY_KEY_COLUMNS


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ChatRequest(StrictModel):
    message: str = Field(min_length=1, max_length=4000)

    @field_validator("message")
    @classmethod
    def nonblank(cls, value):
        if not value.strip():
            raise ValueError("Message must not be blank.")
        return value.strip()


class FileRequest(StrictModel):
    file: str = Field(min_length=1, max_length=512)
    key_columns: list[str] = Field(default_factory=lambda: list(COUNTERPARTY_KEY_COLUMNS), min_length=1)

    @field_validator("key_columns")
    @classmethod
    def keys(cls, value):
        value = [item.strip() for item in value]
        if any(not item for item in value) or len(set(value)) != len(value):
            raise ValueError("Key columns must be nonblank and unique.")
        return value


class CompareRequest(StrictModel):
    previous_file: str = Field(min_length=1, max_length=512)
    current_file: str = Field(min_length=1, max_length=512)
    key_columns: list[str] = Field(default_factory=lambda: list(COUNTERPARTY_KEY_COLUMNS), min_length=1)
    movement_threshold_pct: float = Field(default=20.0, ge=0, allow_inf_nan=False)
    minimum_absolute_change: float = Field(default=0.0, ge=0, allow_inf_nan=False)
    generate_ai_insights: bool = False
    metrics: list[str] | None = None

    _keys = field_validator("key_columns")(FileRequest.keys.__func__)


class ReportRequest(CompareRequest):
    report_format: Literal["pdf", "xlsx", "both"] = "both"


class ClarificationRequest(StrictModel):
    question: str = Field(min_length=1, max_length=500)
