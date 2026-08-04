
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings


# -----------------------------------------------------------
# Database URL
# -----------------------------------------------------------

DATABASE_URL = settings.DATABASE_URL


# -----------------------------------------------------------
# Engine
# -----------------------------------------------------------

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
    if DATABASE_URL.startswith("sqlite")
    else {},
    echo=False,
    future=True,
)


# -----------------------------------------------------------
# Session Factory
# -----------------------------------------------------------

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# -----------------------------------------------------------
# Base Class for ORM Models
# -----------------------------------------------------------

Base = declarative_base()


# -----------------------------------------------------------
# Dependency Injection
# -----------------------------------------------------------

def get_db():
    """
    Creates a new database session for every request.
    Automatically closes the session afterwards.
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
