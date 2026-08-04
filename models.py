
from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    Text,
)
from sqlalchemy.orm import relationship
from app.database import Base

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(100), nullable=False)
    city = Column(String(100))
    state = Column(String(100))
    email = Column(String(150), unique=True)
    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
    sales = relationship(
        "Sales",
        back_populates="customer"
    )

class Sales(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(
        Integer,
        ForeignKey("customers.id")
    )
    product = Column(String(100))
    quantity = Column(Integer)
    sales = Column(Float)
    year = Column(Integer)
    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    customer = relationship(
        "Customer",
        back_populates="sales"
    )


class QueryHistory(Base):
    __tablename__ = "query_history"
    id = Column(Integer, primary_key=True, index=True    )
    question = Column( Text,nullable=False )
    generated_sql = Column(Text,nullable=False )
    execution_status = Column(String(20), default="SUCCESS" )
    execution_time_ms = Column( Float, default=0 )
    model_used = Column(String(50) )

    created_at = Column( DateTime, default=datetime.utcnow )
