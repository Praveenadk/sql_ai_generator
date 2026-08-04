"""
Project : AI SQL Generator
File    : routes.py
Purpose : API Routes
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.executor import SQLExecutor
from app.schemas import (
    GenerateSQLRequest,
    ExecuteSQLRequest,
    ExplainSQLRequest
)
from app.services import SQLService

router = APIRouter(tags=["AI SQL Generator"])


# Sample database schema
DATABASE_SCHEMA = """
customers(
    id,
    customer_name,
    city,
    state,
    email
)

sales(
    id,
    customer_id,
    product,
    quantity,
    sales,
    year
)
"""


@router.post("/generate")
def generate_sql(
    request: GenerateSQLRequest,
    db: Session = Depends(get_db)
):
    try:
        service = SQLService(db)

        return service.generate_sql(
            question=request.question,
            schema=DATABASE_SCHEMA
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.post("/execute")
def execute_sql(
    request: ExecuteSQLRequest,
    db: Session = Depends(get_db)
):
    try:
        executor = SQLExecutor(db)

        return executor.execute(request.sql_query)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.post("/explain")
def explain_sql(
    request: ExplainSQLRequest,
    db: Session = Depends(get_db)
):
    try:
        service = SQLService(db)

        explanation = service.explain_sql(request.sql_query)

        return {
            "success": True,
            "explanation": explanation
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.get("/history")
def query_history(db: Session = Depends(get_db)):
    try:
        service = SQLService(db)

        history = service.get_history()

        return {
            "success": True,
            "count": len(history),
            "data": history
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )