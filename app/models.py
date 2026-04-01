from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()


class UserRole(enum.Enum):
    Viewer = "Viewer"
    Analyst = "Analyst"
    Admin = "Admin"


class RecordType(enum.Enum):
    INCOME = "Income"
    EXPENSE = "Expense"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.Viewer)
    is_active = Column(Boolean, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)

    records = relationship("Record", back_populates="owner")


class FinancialRecord(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True)
    type = Column(Enum(RecordType), nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String(50), nullable=False)
    date = Column(DateTime, nullable=False)
    description = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="records")
