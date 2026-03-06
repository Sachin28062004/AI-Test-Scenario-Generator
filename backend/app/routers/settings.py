from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import database, crud
from app.routers.auth import get_current_user
from app.database.models import User

router = APIRouter(prefix="/api/settings", tags=["settings"])


class SettingsIn(BaseModel):
    grok_api_key: str


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", summary="Save Grok API key")
def save_settings(
    payload: SettingsIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        grok_key_enc = payload.grok_api_key if payload.grok_api_key else None
        settings = crud.save_settings(db, grok_key_enc)
        return {"message": "settings saved", "id": settings.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", summary="Get latest settings")
def get_latest_settings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    s = crud.get_settings(db)
    if not s:
        return {}
    return {
        "has_grok_key": bool(s.grok_api_key_enc),
        "created_at": s.created_at
    }
