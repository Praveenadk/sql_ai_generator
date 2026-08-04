"""
Project : AI SQL Generator
File    : validator.py
Purpose : SQL Validation
"""

import re

ALLOWED_COMMANDS = {"SELECT"}

BLOCKED_KEYWORDS = {
    "DROP",
    "DELETE",
    "UPDATE",
    "INSERT",
    "ALTER",
    "TRUNCATE",
    "CREATE",
    "REPLACE",
    "GRANT",
    "REVOKE",
    "EXEC",
    "EXECUTE",
    "MERGE"
}


class SQLValidationError(Exception):
    """Raised when SQL validation fails."""
    pass


def validate_sql(sql: str) -> bool:
    """
    Validate generated SQL.

    Returns:
        True if SQL is safe.

    Raises:
        SQLValidationError
    """

    if not sql:
        raise SQLValidationError("SQL query is empty.")

    sql = sql.strip()

    first_word = sql.split()[0].upper()

    if first_word not in ALLOWED_COMMANDS:
        raise SQLValidationError(
            f"Only SELECT queries are allowed. Found '{first_word}'."
        )

    sql_upper = sql.upper()

    for keyword in BLOCKED_KEYWORDS:
        if re.search(rf"\\b{keyword}\\b", sql_upper):
            raise SQLValidationError(
                f"Blocked keyword detected: {keyword}"
            )

    if ";" in sql[:-1]:
        raise SQLValidationError(
            "Multiple SQL statements are not allowed."
        )

    return True
