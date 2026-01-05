from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from .database import Base

class Settings(Base):
    __tablename__ = "settings"
    id = Column(Integer, primary_key=True, index=True)
    jira_domain = Column(String, nullable=True)
    jira_email = Column(String, nullable=True)
    jira_token_encrypted = Column(Text, nullable=True)  # encrypted token
    gemini_api_key_encrypted = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ExportRecord(Base):
    __tablename__ = "export_records"
    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(String, index=True)
    filename = Column(String)
    filepath = Column(String)
    generated_at = Column(DateTime(timezone=True), server_default=func.now())