
SYSTEM_PROMPT = """
You are a Senior SQL Engineer.

Rules:
1. Generate only valid SQL.
2. Return only SQL.
3. Do not add explanations.
4. Use ANSI SQL whenever possible.
5. Use SELECT statements only.
6. Never generate DROP, DELETE, UPDATE, ALTER, INSERT, TRUNCATE or CREATE.
"""


def sql_generation_prompt(question: str, schema: str) -> str:
    return f"""
Database Schema:
{schema}

User Question:
{question}

Generate a SQL query that answers the user's question.

Return only SQL.
""".strip()


def sql_explanation_prompt(sql: str) -> str:
    return f"""
Explain the following SQL query in simple English.

SQL:
{sql}

Explain:
- What tables are used
- What filters are applied
- What aggregations are performed
- What result is returned
""".strip()


def sql_optimization_prompt(sql: str) -> str:
    return f"""
Review this SQL query.

SQL:
{sql}

Suggest:
- Performance improvements
- Better JOIN strategy
- Index recommendations
- Query optimization
""".strip()


def sql_error_prompt(sql: str, error: str) -> str:
    return f"""
The following SQL generated an error.

SQL:
{sql}

Error:
{error}

Explain:
1. Why it failed
2. How to fix it
3. Provide corrected SQL
""".strip()


def result_summary_prompt(question: str, result: str) -> str:
    return f"""
User Question:
{question}

Query Result:
{result}

Summarize the results in business-friendly language.
""".strip()