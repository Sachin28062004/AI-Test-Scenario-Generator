from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import database, crud
from app.utils.crypto import encrypt_text, decrypt_text

router = APIRouter(prefix="/api/settings", tags=["settings"])

class SettingsIn(BaseModel):
    jira_domain: str
    jira_email: str
    jira_token: str
    gemini_api_key: str = None

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", summary="Save settings (Jira credentials + Gemini key)")
def save_settings(payload: SettingsIn, db: Session = Depends(get_db)):
    try:
        jira_token_enc = payload.jira_token
        gemini_key_enc = payload.gemini_api_key if payload.gemini_api_key else None
        settings = crud.save_settings(db, payload.jira_domain, payload.jira_email, jira_token_enc, gemini_key_enc)
        return {"message": "settings saved", "id": settings.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", summary="Get latest settings")
def get_latest_settings(db: Session = Depends(get_db)):
    s = crud.get_settings(db)
    if not s:
        return {}
    return {
        "jira_domain": s.jira_domain,
        "jira_email": s.jira_email,
        # do NOT return token in cleartext to frontend — only return presence indicator
        "has_jira_token": bool(s.jira_token_encrypted),
        "has_gemini_key": bool(s.gemini_api_key_encrypted),
        "created_at": s.created_at
    }