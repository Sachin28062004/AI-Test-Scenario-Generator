from sqlalchemy.orm import Session
from app.database import models


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, username: str, email: str, hashed_password: str):
    user = models.User(username=username, email=email, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_settings(db: Session):
    return db.query(models.Settings).order_by(models.Settings.id.desc()).first()


def save_settings(db: Session, grok_key_enc: str):
    settings = models.Settings(grok_api_key_enc=grok_key_enc)
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
