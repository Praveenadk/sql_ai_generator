
import time
from openai import OpenAI
from sqlalchemy.orm import Session

from app.config import settings
from app.logger import get_logger
from app.models import QueryHistory
from app.prompts import (
    SYSTEM_PROMPT,
    sql_generation_prompt,
    sql_explanation_prompt
)
from app.validator import validate_sql

logger = get_logger(__name__)

client = OpenAI(api_key=settings.OPENAI_API_KEY)


class SQLService:

    def __init__(self, db: Session):
        self.db = db

    def generate_sql(self, question: str, schema: str) -> dict:
        start_time = time.perf_counter()

        prompt = sql_generation_prompt(question, schema)

        response = client.chat.completions.create(
            model=settings.MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        sql = response.choices[0].message.content.strip()

        validate_sql(sql)

        execution_time = (time.perf_counter() - start_time) * 1000

        history = QueryHistory(
            question=question,
            generated_sql=sql,
            execution_status="SUCCESS",
            execution_time_ms=execution_time,
            model_used=settings.MODEL_NAME
        )

        self.db.add(history)
        self.db.commit()

        logger.info("SQL generated successfully")

        return {
            "question": question,
            "generated_sql": sql,
            "model_used": settings.MODEL_NAME,
            "success": True
        }

    def explain_sql(self, sql: str) -> str:
        prompt = sql_explanation_prompt(sql)

        response = client.chat.completions.create(
            model=settings.MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "You are a SQL expert."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content.strip()

    def get_history(self):
        return (
            self.db.query(QueryHistory)
            .order_by(QueryHistory.created_at.desc())
            .all()
        )