
import time

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.logger import get_logger
from app.validator import validate_sql

logger = get_logger(__name__)


class SQLExecutor:

    def __init__(self, db: Session):
        self.db = db

    def execute(self, sql: str) -> dict:
        """
        Execute validated SQL and return results.
        """

        validate_sql(sql)

        start_time = time.perf_counter()

        try:
            result = self.db.execute(text(sql))

            rows = result.mappings().all()

            execution_time = round(
                (time.perf_counter() - start_time) * 1000,
                2
            )

            logger.info(
                "Executed query successfully in %.2f ms",
                execution_time
            )

            return {
                "success": True,
                "rows_returned": len(rows),
                "execution_time_ms": execution_time,
                "data": rows
            }

        except SQLAlchemyError as e:

            logger.exception("Database execution failed")

            return {
                "success": False,
                "error": str(e)
            }

        except Exception as e:

            logger.exception("Unexpected error")

            return {
                "success": False,
                "error": str(e)
            }