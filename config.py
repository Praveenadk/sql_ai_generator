"""
===========================================================
Configuration
===========================================================
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # Database
    DATABASE_URL: str = "sqlite:///./data/sql_generator.db"

    # OpenAI
    OPENAI_API_KEY: str = ""

    # Model
    MODEL_NAME: str = "gpt-4.1-mini"

    # Application
    APP_NAME: str = "AI SQL Generator"

    DEBUG: bool = True

    class Config:
        env_file = ".env"


settings = Settings()
