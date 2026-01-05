from sqlalchemy.orm import Session
from app.database import models

def get_settings(db: Session):
    settings = db.query(models.Settings).order_by(models.Settings.id.desc()).first()
    return settings

def save_settings(db: Session, jira_domain: str, jira_email: str, jira_token_enc: str, gemini_key_enc: str):
    settings = models.Settings(
        jira_domain=jira_domain,
        jira_email=jira_email,
        jira_token_encrypted=jira_token_enc,
        gemini_api_key_encrypted=gemini_key_enc
    )
    db.add(settings)
    db.commit()
    db.refresh(settings)
    return settings

def save_export_record(db: Session, ticket_id: str, filename: str, filepath: str):
    rec = models.ExportRecord(ticket_id=ticket_id, filename=filename, filepath=filepath)
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec

def list_exports(db: Session, limit=50):
    return db.query(models.ExportRecord).order_by(models.ExportRecord.generated_at.desc()).limit(limit).all()
