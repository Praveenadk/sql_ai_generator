
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


# ---------- Generate SQL ----------

class GenerateSQLRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=5,
        max_length=500,
        examples=["Show top 5 customers by sales"]
    )


class GenerateSQLResponse(BaseModel):
    question: str
    generated_sql: str
    model_used: str
    success: bool = True


# ---------- Execute SQL ----------

class ExecuteSQLRequest(BaseModel):
    sql_query: str


class ExecuteSQLResponse(BaseModel):
    rows_returned: int
    execution_time_ms: float
    data: list[dict[str, Any]]
    success: bool


# ---------- Explain SQL ----------

class ExplainSQLRequest(BaseModel):
    sql_query: str


class ExplainSQLResponse(BaseModel):
    explanation: str
    success: bool = True


# ---------- Query History ----------

class QueryHistoryResponse(BaseModel):
    id: int
    question: str
    generated_sql: str
    execution_status: str
    execution_time_ms: float
    model_used: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True


# ---------- Health ----------

class HealthResponse(BaseModel):
    status: str
    application: str
    version: str


# ---------- Generic Response ----------

class APIResponse(BaseModel):
    success: bool
    message: str


# ---------- Error Response ----------

class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    details: str | None = None