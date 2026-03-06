from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from .database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Settings(Base):
    __tablename__ = "settings"
    id = Column(Integer, primary_key=True, index=True)
    grok_api_key_enc = Column("openai_key_enc", Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ExportRecord(Base):
    __tablename__ = "export_records"
    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(String, index=True, default="manual")  # "manual" for user-entered descriptions
    filename = Column(String)
    filepath = Column(String)
    generated_at = Column(DateTime(timezone=True), server_default=func.now())
